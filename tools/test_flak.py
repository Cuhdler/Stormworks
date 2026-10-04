"""Pruefstand fuer die Flak-Chips der Figet Marena (lua/flakradar.lua + lua/flak.lua v1.3), Lua 5.3 wie im Spiel.
- v1.3: Ziel-Vorgabe der Lagezentrale (Ort des ersten Objekts mit Fehler 'vfehler' m) und 'Feuer frei' kommen
  wie vom Bildschirm-Chip
Nach dem Swifter-Pruefstand (stormworks_flugpanzer/tools/waffen_test.py, test_flak) fuers Schiff:
- Schiff faehrt (Tempo, Kurs), schaukelt (Nick/Roll); der Physik-Sensor liefert Position, Kompass (gegen den
  Uhrzeigersinn), Nick, Roll, Hoehe wie im Spiel
- Radar (Basic) auf dem Flak-Turm im manuellen Modus: Strahl 'fov' breit/hoch (U), folgt dem Gimbal-Befehl mit
  hoechstens 0,2865 U/s, meldet alle 2 Ticks, was im Strahl ist (Winkel ab Sockel, Hoehe gegen das Deck)
- Drehkranz traege (lag), Rohre folgen sofort; 2 Heavy Autocannons abwechselnd (99/min je Rohr)
- Geschosse wie im Spiel: Weg += v/60, v *= (1-d), Steigen -= g/60; Zeitzuender: Fragmentation platzt nach der
  eingestellten Zeit - gezaehlt wird, wie nah am Ziel (Splitter-Wirkung ca. 8 m)
"""
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_flak  # noqa: E402
import build_lage  # noqa: E402
import sperrprofil  # noqa: E402
from test_schiff import load, pruefe  # noqa: E402

PR = {n: v for n, v, _ in build_flak.PROPS}
PR.update({n: v for n, v, _ in build_lage.SCHREIBER_PROPS})
PR["Schreiber Port"] = 0            # Schreiber aus (nur der Schreiber-Test schaltet ihn ein)
PROFIL = None


def profil_l():
    global PROFIL
    if PROFIL is None:
        PROFIL = sperrprofil.profil(-10, -105, 18)
    return PROFIL


def lauf(start, vel, secs=40, own=(0.0, 15.0, 0.0), hdg=0.0, roll=0.0, nick=0.0, fov=(0.02, 0.02), lag=0.3,
         profil=True, props=None, ziele=None, seed=1, vorgabe=True, frei=True, vfehler=(40.0, -30.0, 20.0),
         drift=None, einzel=(), prf=None, see=False, rmax=6000, weiche=1, bc=None, melder=True, lad_log=None, korr=(0.0, 0.0)):
    """start/vel: Ziel relativ zu uns (Ost, Nord, Hoch m) und sein Welt-Tempo; own = unser Welt-Tempo; hdg = Kurs Grad;
    prf = Sperrprofil (sonst Flak L); see = Schiffsziel: Einschlag auf dem Wasser zaehlt (Abstand zum Ziel waagerecht);
    rmax = Reichweite des Turm-Radars; 'Lader Zeit s' > 0 in props = Battle Cannon mit Lade-Ablauf (bc = Zeiten in Ticks,
    melder = 'Contains Ammo' der Zufuehrungen angeschlossen, lad_log = Liste fuer Lade-Ereignisse);
    roll/nick = Amplitude Grad (Periode 7 s / 5 s); ziele = weitere Objekte [(start, vel)], z. B. Schiffe.
    -> dict mit Kennzahlen"""
    rnd = random.Random(seed)
    pr = dict(PR)
    pr.update(props or {})
    _, gA, ioA = load("flakradar.lua", pr)
    _, gF, ioF = load("flak.lua", pr)
    pf = prf or profil_l()
    gF.PRF = ",".join(str(v) for v in pf) if profil else "0"
    for g, q in ((gA, "fLr"), (gF, "fLf")):
        g.LQ, (g.LT, g.LO) = q, build_lage.TAKT[q]
    v0, d, gg = pr["AA v0"], pr["AA Drag"], pr["Geschoss g"]
    obj = [[list(start), list(vel)]] + [[list(s), list(v)] for s, v in (ziele or [])]
    S = [100.0, 200.0, 8.0]                  # unser Ort in der Welt (Ost, Nord, Hoch)
    ar, tw, dy, dp, gy, gp = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
    bullets, bursts, schuss, gesperrt = [], [], 0, 0
    schuss_je, schuss_t, einschlag, treffer = {}, [], [], 0
    ld, cdr, kam = True, {"L": 0, "R": 0}, []
    lader, geladen = pr.get("Lader Zeit s", 0) > 0, {"L": False, "R": False}
    # Battle Cannon (Andres Log 04.10.: Verschluss 216 Ticks offen, 'Loaded' 79 Ticks nach dem Schliessen): Verschluss
    # oeffnet in 'auf' Ticks, schliesst in 'zu'; Zufuehrung -> Rohr 'rein' Ticks (Verschluss ganz offen, Feed an);
    # Weiche -> Zufuehrung ihrer Seite 'weiche' Ticks (wenn die leer ist); Magazin -> Weiche 'nach' Ticks. Beim Spawnen
    # Rohre leer, Zufuehrungen und Weiche voll (wie im Log: erst nach 296 Ticks geladen)
    # 'sitz': so lange nach dem Verlassen der Zufuehrung muss der Verschluss noch offen bleiben, sonst rutscht die Granate
    # zurueck (prueft das Lernen des Nachlaufs)
    bz = dict({"auf": 40, "zu": 79, "rein": 10, "weiche": 20, "nach": 30, "sitz": 0}, **(bc or {}))
    t_rein = {"L": -1e9, "R": -1e9}
    offen, im_rohr, zuf, zt, rt = {"L": 0.0, "R": 0.0}, {"L": False, "R": False}, {"L": True, "R": True}, 0, {"L": 0, "R": 0}
    w_voll, w_t, w_ziel = True, 0, None
    if lader:
        ld = False
    for t in range(60 * secs):
        rl = roll * math.sin(2 * math.pi * t / 420) / 360       # U, + rechte Seite unten
        nk = nick * math.sin(2 * math.pi * t / 300) / 360       # U, + Nase hoch
        h = hdg / 360
        S = [S[i] + own[i] / 60 for i in range(3)]
        for o in obj:
            o[0] = [o[0][i] + (o[1][i] - own[i]) / 60 for i in range(3)]
        smax = 0.2865 / 60
        dd = ((gy - dy + 0.5) % 1) - 0.5
        dy = ((dy + max(-smax, min(smax, dd)) + 0.5) % 1) - 0.5
        dp += max(-smax, min(smax, max(-0.125, min(0.125, gp)) - dp))
        n = {4: ar, 8: S[0], 12: -h, 16: nk, 20: -rl, 24: S[2], 28: dy, 32: S[1]}
        o0 = obj[0][0]
        vf = vfehler
        if drift and t > 60 * drift[0]:
            # die Vorgabe der Lagezentrale weicht ab drift[0] s immer weiter ab (drift[1] m/s), gleiche Zielnummer
            vf = [vfehler[i] + drift[1] * (t / 60 - drift[0]) for i in range(3)]
        n.update({25: 1, 29: o0[0] + vf[0], 30: o0[1] + vf[1], 31: S[2] + o0[2] + vf[2]})
        b = {10: vorgabe, 11: frei, 12: t in einzel}     # 12: Einzelschuss (Leertaste) einen Tick
        orte = []
        for k, (o, _) in enumerate(obj):
            R = math.sqrt(sum(c * c for c in o))
            yaw = math.atan2(o[0], o[1]) / (2 * math.pi)
            elw = math.asin(o[2] / R) / (2 * math.pi)
            azb = ((yaw - h - ar + 0.5) % 1) - 0.5                # ab Sockel (Radar dreht mit dem Turm)
            th = (azb + ar) * 2 * math.pi                         # Richtung ab Bug
            el = elw - (nk * math.cos(th) - rl * math.sin(th))    # gegen das Deck
            seen = t % 2 == 0 and abs(((azb - dy + 0.5) % 1) - 0.5) < fov[0] / 2 and abs(el - dp) < fov[1] / 2
            if seen and R < rmax:
                orte.append((R, azb, el))
        # wie das Radar: hoechstens 6 Ortungen auf den Plaetzen 1-6 (bei mehr eine zufaellige Auswahl - im Spiel kamen nahe
        # und 6 km ferne gemischt), die Kanaele dahinter tragen Turm, Physik, Vorgabe (04.10.: mit mehr als 6 Objekten
        # ueberschrieb der Pruefstand Vorgabe und Einzelschuss)
        if len(orte) > 6:
            orte = rnd.sample(orte, 6)
        for i, (R, azb, el) in enumerate(orte, 1):
            n[i * 4 - 3] = R * (1 + rnd.uniform(-1, 1) * 0.002)
            n[i * 4 - 2] = azb + rnd.uniform(-1, 1) * 0.0003
            n[i * 4 - 1] = el + rnd.uniform(-1, 1) * 0.0003
            b[i] = True
        ioA["n"], ioA["b"] = n, b
        ioA["on"].clear()
        gA.onTick()
        oa = {k: v for k, v in ioA["on"].items() if k < 100}
        ob = {k - 100: v for k, v in ioA["on"].items() if k > 100}
        gy, gp = oa.get(1, 0.0), oa.get(2, 0.0)
        ioF["n"], ioF["b"] = {**oa, 26: 500, 27: korr[0], 28: korr[1]}, {**ob, 3: ld, 5: lader and geladen["R"],
                                               6: lader and melder and zuf["L"], 7: lader and melder and zuf["R"]}
        ioF["on"].clear()
        gF.onTick()
        out = {k: v for k, v in ioF["on"].items() if k < 100}
        # Kamera (v2.6 Auto-Zoom): Bildwinkel aus dem Zoom-Ausgang, Versatz Turm -> Ziel jetzt (die Kamera schaut mit dem
        # Turm; der Hoehe nach folgt sie dem Ziel)
        kfov = pr["Kamera FOV weit rad"] - out.get(19, 0.0) * (pr["Kamera FOV weit rad"] - pr["Kamera FOV eng rad"])
        o0r = obj[0][0]
        kaz = ((math.atan2(o0r[0], o0r[1]) / (2 * math.pi) - h - ar + 0.5) % 1) - 0.5
        kam.append((t, kfov, abs(kaz) * 2 * math.pi, math.sqrt(sum(c * c for c in o0r))))
        feuer = {"L": ioF["on"].get(101, False), "R": ioF["on"].get(105, False)}
        # Drehkranz traege
        tw += (out.get(1, 0) - tw) / max(1.0, lag * 60)
        ar = ((ar + tw / 60 + 0.5) % 1) - 0.5
        pe = out.get(2, 0) * 0.25                              # Rohr gegen das Deck (U)
        # Rohre (Flak v2.0): eigener Abzug je Rohr, jedes laedt 38 Ticks nach (gemessen 04.10.); 'Loaded' links kurz aus
        if lader:
            # Battle Cannon (zwei Rohre, ein Magazin, Weiche; weiche=1: Bool 7 an = rechts)
            fd = ioF["on"].get(103, False)
            vs = {"L": ioF["on"].get(106, False), "R": ioF["on"].get(108, False)}
            ws = "R" if ioF["on"].get(107, False) == (weiche > 0) else "L"
            for sd in "LR":
                offen[sd] = min(1.0, offen[sd] + 1 / bz["auf"]) if vs[sd] else max(0.0, offen[sd] - 1 / bz["zu"])
                if offen[sd] >= 1 and fd and zuf[sd] and not im_rohr[sd]:
                    rt[sd] += 1
                    if rt[sd] >= bz["rein"]:
                        zuf[sd], im_rohr[sd], rt[sd], t_rein[sd] = False, True, 0, t
                        if lad_log is not None:
                            lad_log.append((t, sd, "rein"))
                else:
                    rt[sd] = 0
                if not vs[sd] and im_rohr[sd] and t - t_rein[sd] < bz["sitz"] and not zuf[sd]:
                    zuf[sd], im_rohr[sd] = True, False
                    if lad_log is not None:
                        lad_log.append((t, sd, "zurueck"))
                gl = im_rohr[sd] and offen[sd] <= 0
                if gl and not geladen[sd] and lad_log is not None:
                    lad_log.append((t, sd, "geladen"))
                geladen[sd] = gl
            if ws != w_ziel:
                w_ziel, w_t = ws, 0
            if w_voll and not zuf[ws]:
                w_t += 1
                if w_t >= bz["weiche"]:
                    zuf[ws], w_voll, w_t = True, False, 0
                    if lad_log is not None:
                        lad_log.append((t, ws, "zufuehrung"))
            if not w_voll:
                zt += 1
                if zt >= bz["nach"]:
                    w_voll, zt = True, 0
            schiessen = [sd for sd in "LR" if feuer[sd] and geladen[sd]]
            for sd in schiessen:
                geladen[sd] = im_rohr[sd] = False
            ld = geladen["L"]
        else:
            for sd in "LR":
                cdr[sd] -= 1
            ld = cdr["L"] < 35
            schiessen = [q for q in "LR" if feuer[q] and cdr[q] <= 0]
            for sd in schiessen:
                cdr[sd] = 38
                if sd == "L":
                    ld = False
        for sd in schiessen:
            schuss += 1
            schuss_je[sd] = schuss_je.get(sd, 0) + 1
            schuss_t.append(t)
            gb = ((ar + 0.5) % 1) - 0.5
            k = int(round(gb * 72)) % 72
            if pe * 360 < pf[k] - 0.5:
                gesperrt += 1
            th = gb * 2 * math.pi
            pw = pe + (nk * math.cos(th) - rl * math.sin(th))   # Rohr in der Welt
            gw = (h + gb) * 2 * math.pi
            dirv = [math.cos(pw * 2 * math.pi) * math.sin(gw), math.cos(pw * 2 * math.pi) * math.cos(gw),
                    math.sin(pw * 2 * math.pi)]
            fz = out.get(4, 0)
            bullets.append({"a": -1e9, "p": [S[0], S[1], S[2] - pr["AA Radar ueber Rohr m"]], "v": [v0 * dirv[i] + own[i] for i in range(3)], "n": 0,
                            "fz": int(round(fz * 60)) if fz > 0 else (3600 if see else 600), "min": 1e9})
        ziel_w = [S[i] + obj[0][0][i] for i in range(3)]          # Luftziel in der Welt
        for bl in bullets:
            if bl["n"] < 0:
                continue
            bl["p"] = [bl["p"][i] + bl["v"][i] / 60 for i in range(3)]
            bl["v"] = [bl["v"][0] * (1 - d), bl["v"][1] * (1 - d), bl["v"][2] * (1 - d) - gg / 60]
            bl["n"] += 1
            dist = math.sqrt(sum((ziel_w[i] - bl["p"][i]) ** 2 for i in range(3)))
            bl["min"] = min(bl["min"], dist)
            if see:
                # Vorbeiflug am Ziel (laengs auf seiner Hoehe): Rumpf getroffen, wenn hoechstens 5 m seitlich und 2,5 m
                # ueber/unter dem Zielpunkt (Schiffe 10-40 m lang, Rumpf ~5 m hoch)
                vh = math.hypot(bl["v"][0], bl["v"][1]) or 1.0
                ux, uy = bl["v"][0] / vh, bl["v"][1] / vh
                rx, ry = bl["p"][0] - ziel_w[0], bl["p"][1] - ziel_w[1]
                a = rx * ux + ry * uy
                if bl["a"] < 0 <= a and abs(-rx * uy + ry * ux) < 5 and abs(bl["p"][2] - ziel_w[2]) < 2.5:
                    treffer += 1
                bl["a"] = a
            if see and bl["v"][2] < 0 and bl["p"][2] <= ziel_w[2]:
                # Schiffsziel: Einschlag auf Hoehe des Ziels - waagerechter Abstand
                bursts.append(math.hypot(ziel_w[0] - bl["p"][0], ziel_w[1] - bl["p"][1]))
                einschlag.append((bl["p"][0] - ziel_w[0], bl["p"][1] - ziel_w[1], ziel_w[0] - S[0], ziel_w[1] - S[1], bl["n"]))
                bl["n"] = -1
                continue
            if bl["n"] >= bl["fz"]:
                bursts.append(dist)
                bl["n"] = -1
    nah = sum(1 for x in bursts if x < 8)
    abst = [b - a for a, b in zip(schuss_t, schuss_t[1:])]
    return {"turm": ar, "treffer": treffer, "einschlag": einschlag, "je": schuss_je, "abst": sorted(abst)[len(abst) // 2] if abst else 0, "http": ioA["http"] + ioF["http"], "schuss": schuss, "nah": nah, "bursts": len(bursts), "gesperrt": gesperrt,
            "bestes": min([b["min"] for b in bullets] or [1e9]), "median": sorted(bursts)[len(bursts) // 2] if bursts else 1e9,
            "kam": kam}


def kamera(r, ab_s, groesse):
    """Auto-Zoom: Anteil der Ticks ab ab_s, in denen das Ziel im Bild ist; Median Bildwinkel und Bildanteil des Ziels."""
    k = [q for q in r["kam"] if q[0] >= ab_s * 60]
    drin = sum(1 for _, fv, off, R in k if off + groesse / 2 / R < fv / 2) / max(len(k), 1)
    fvs = sorted(q[1] for q in k)
    teil = sorted(groesse / q[3] / q[1] for q in k)
    return drin, fvs[len(fvs) // 2], teil[len(teil) // 2]


def test_flak():
    rueck = []
    # 1. Flugzeug kreuzt in 1,2 km, 150 m hoch, 100 m/s; wir fahren 30 kn nach Norden, ruhige See
    r = lauf((-1500.0, 1200.0, 150.0), (100.0, 0.0, 0.0), secs=35)
    rueck.append(("Flugzeug kreuzt (1,2 km, 100 m/s), 30 kn, ruhig: %d Schuss, %d von %d Zerlegungen naeher 8 m (Median %.0f m)"
                  % (r["schuss"], r["nah"], r["bursts"], r["median"]), r["schuss"] > 10 and r["nah"] >= r["bursts"] * 0.3))
    # 2. dasselbe bei Seegang: Roll 6 Grad, Nick 2 Grad
    r2 = lauf((-1500.0, 1200.0, 150.0), (100.0, 0.0, 0.0), secs=35, roll=6, nick=2)
    rueck.append(("  dasselbe mit Seegang (Roll 6, Nick 2 Grad): %d von %d naeher 8 m (Median %.0f m)"
                  % (r2["nah"], r2["bursts"], r2["median"]), r2["nah"] >= r2["bursts"] * 0.3))
    # 3. Hubschrauber schwebt in 600 m, 40 m hoch (seitlich hinten links)
    r3 = lauf((-450.0, -400.0, 40.0), (0.0, 0.0, 0.0), secs=25, own=(0.0, 0.0, 0.0))
    rueck.append(("Hubschrauber schwebt (600 m, 40 m hoch): %d Schuss, %d von %d naeher 8 m"
                  % (r3["schuss"], r3["nah"], r3["bursts"]), r3["nah"] >= r3["bursts"] * 0.5 and r3["schuss"] > 5))
    # 4. nur Schiffe in der Naehe, Vorgabe (faelschlich) auf ein Schiff: nie feuern
    r4 = lauf((-600.0, 300.0, 1.0), (5.0, 8.0, 0.0), secs=25, ziele=[((800.0, -200.0, 2.0), (-6.0, 0.0, 0.0))])
    rueck.append(("Vorgabe auf ein Schiff (600 m, 1 m hoch): kein Schuss (%d)" % r4["schuss"], r4["schuss"] == 0))
    # 7. zwei Flieger, Vorgabe auf den weiteren: die Flak nimmt den vorgegebenen, nicht den naeheren
    r7 = lauf((1800.0, 900.0, 250.0), (-90.0, 0.0, 0.0), secs=30, ziele=[((-700.0, 500.0, 120.0), (0.0, -60.0, 0.0))])
    rueck.append(("zwei Flieger, Vorgabe auf den weiteren (2 km): %d Schuss, %d von %d am vorgegebenen naeher 8 m"
                  % (r7["schuss"], r7["nah"], r7["bursts"]), r7["schuss"] > 10 and r7["nah"] >= r7["bursts"] * 0.3))
    # 9. Hardlock: die Vorgabe weicht nach 8 s langsam ab (8 m/s, nach 30 s 180 m), die Flak bleibt auf ihrer Spur
    r10 = lauf((-1500.0, 1200.0, 150.0), (100.0, 0.0, 0.0), secs=30, drift=(8, 8.0))
    rueck.append(("Hardlock: Vorgabe weicht 180 m ab, Flak bleibt drauf: %d von %d naeher 8 m" % (r10["nah"], r10["bursts"]),
                  r10["schuss"] > 10 and r10["nah"] >= r10["bursts"] * 0.3))
    # 10. Sicherung: die eigene Spur liegt weit neben der Vorgabe (Vorgabe springt 1 km weg) -> nach 2 s kein Feuer mehr
    r11 = lauf((-1500.0, 1200.0, 150.0), (100.0, 0.0, 0.0), secs=30, drift=(10, 1e5))
    r12 = lauf((-1500.0, 1200.0, 150.0), (100.0, 0.0, 0.0), secs=10)
    rueck.append(("Sicherung: Vorgabe 1 km daneben -> nach 2 s Feuerpause (%d Schuss in 30 s statt %d in 10 s + 20 s)"
                  % (r11["schuss"], r12["schuss"]), r11["schuss"] <= r12["schuss"] + 8))
    # 11. Andres Hafen-Log: Vorgabe auf einen Heli (250 m, 120 m hoch), 130 m daneben ein stehendes Ding (180 m, 12 m
    #     hoch, naeher): die Flak darf das Ding nicht fangen
    r13 = lauf((-150.0, 200.0, 120.0), (6.0, 4.0, 0.0), secs=20, own=(0.0, 0.0, 0.0),
               ziele=[((-170.0, 60.0, 12.0), (0.0, 0.0, 0.0))], vfehler=(10.0, -8.0, 5.0))
    rueck.append(("Hafen: Vorgabe Heli 250 m, stehendes Ding 130 m daneben: %d von %d Zerlegungen am Heli naeher 8 m"
                  % (r13["nah"], r13["bursts"]), r13["schuss"] > 5 and r13["nah"] >= r13["bursts"] * 0.3))
    # 12. Schreiber v2: Hafen-Fall mit weiteren Dingen - Pakete im Takt, unter 'Schreiber Zeichen', nichts verworfen,
    # keine Luecken, jede Zeile passt zu ihrer Spaltenliste
    from test_lage import schreiber_pruefen
    r14 = lauf((-150.0, 200.0, 120.0), (6.0, 4.0, 0.0), secs=12, own=(0.0, 0.0, 0.0), props={"Schreiber Port": 8768},
               ziele=[((x, y, 5.0), (0.0, 0.0, 0.0)) for x, y in ((-170, 60), (-300, 250), (-90, 400), (-400, -50),
                                                                      (-250, 150), (-120, 320))], vfehler=(10.0, -8.0, 5.0))
    je, doppelt, luecken, fehler, zeilen = schreiber_pruefen([(i, b) for i, (_, b) in enumerate(r14["http"])],
                                                             PR["Schreiber Zeichen"])
    rueck.append(("Schreiber: %s, Zeilen %s, Luecken %s, Fehler %s" % (
        {q: (e["pakete"], e["max"], e["x"]) for q, e in sorted(je.items())}, dict(sorted(zeilen.items())),
        {k: v for k, v in luecken.items() if v}, fehler[:3]),
        set(je) == {"fLr", "fLf"} and all(e["x"] == 0 and e["max"] <= PR["Schreiber Zeichen"] + 200 for e in je.values())
        and not any(luecken.values()) and not fehler))
    # 13. Einzelschuss (Leertaste): ohne Ziel und ohne Feuer frei je Druck genau ein Schuss, nie ins Sperrprofil;
    # mit Ziel und Feuer frei stoert er die Automatik nicht
    r16 = lauf((-1500.0, 1200.0, 150.0), (100.0, 0.0, 0.0), secs=15, vorgabe=False, frei=False, einzel=(200, 500, 800))
    r17 = lauf((-1500.0, 1200.0, 150.0), (100.0, 0.0, 0.0), secs=35, einzel=(900, 1200))
    rueck.append(("Einzelschuss ohne Ziel: 3 Druecke = %d Schuss (%d gesperrt); mit Ziel und Automatik: %d Schuss, %d von %d "
                  "naeher 8 m (ohne Einzelschuss %d / %d)" % (r16["schuss"], r16["gesperrt"], r17["schuss"], r17["nah"], r17["bursts"],
                                                       r["schuss"], r["nah"]),
                  r16["schuss"] == 3 and r16["gesperrt"] == 0 and r17["schuss"] >= r["schuss"] and r17["nah"] >= r["nah"] - 3))
    # 14. Rohre abwechselnd (Flak v2.0): beide feuern, im Mittel alle ~19 Ticks ein Schuss (nicht 2 gleichzeitig)
    rueck.append(("Rohre abwechselnd: links %d, rechts %d Schuss, Abstand Median %d Ticks" % (
        r17["je"].get("L", 0), r17["je"].get("R", 0), r17["abst"]),
        abs(r17["je"].get("L", 0) - r17["je"].get("R", 0)) <= 3 and 16 <= r17["abst"] <= 22))
    # 15. Auto-Zoom (v2.6): Flugzeug kreuzt in 1,2 km - ab 8 s im Bild (trotz Vorhalt), herangezoomt
    dr, fvm, tm = kamera(r, 8, 20)
    rueck.append(("Auto-Zoom Flugzeug 1,2 km: im Bild %.0f %%, Bildwinkel Median %.3f rad, Ziel fuellt %.0f %% der Breite" % (
        dr * 100, fvm, tm * 100), dr >= 0.95 and fvm < 0.5 and tm >= 0.05))
    # 8. ohne 'Feuer frei' / ohne Vorgabe: kein Schuss
    r8 = lauf((-1500.0, 1200.0, 150.0), (100.0, 0.0, 0.0), secs=20, frei=False)
    r9 = lauf((-1500.0, 1200.0, 150.0), (100.0, 0.0, 0.0), secs=20, vorgabe=False)
    rueck.append(("ohne Feuer frei: kein Schuss (%d); ohne Vorgabe: kein Schuss (%d)" % (r8["schuss"], r9["schuss"]),
                  r8["schuss"] == 0 and r9["schuss"] == 0))
    # 5. Ziel tief ueber dem Mast (vorn, 8 Grad): Sperrprofil -> kein Schuss in den Mast
    r5 = lauf((150.0, 1400.0, 200.0), (0.0, -60.0, 0.0), secs=12)
    rueck.append(("Ziel vorn tief ueber dem Mast: kein Schuss ins Sperrprofil (%d Schuss, %d gesperrt)" % (r5["schuss"], r5["gesperrt"]),
                  r5["gesperrt"] == 0))
    # 6. Rohr-Test
    _, gF, ioF = load("flak.lua", dict(PR, **{"Test Rohre": 1}))
    ioF["n"], ioF["b"] = {16: 0.1}, {1: True, 2: True}
    ioF["on"].clear()
    gF.onTick()
    o = dict(ioF["on"])
    rueck.append(("Test Rohre: Rohre 20 Grad hoch (%.3f/%.3f), Turm dreht nach vorn (%.2f), kein Feuer"
                  % (o.get(2, 0), o.get(3, 0), o.get(1, 0)),
                  abs(o.get(2, 0) - 20 / 90) < 1e-6 and abs(o.get(3, 0) - 20 / 90) < 1e-6 and o.get(1, 0) < 0 and not o.get(101)))
    return pruefe(rueck)


if __name__ == "__main__":
    ok = test_flak()
    print("ALLES OK" if ok else "FEHLER")
    sys.exit(0 if ok else 1)
