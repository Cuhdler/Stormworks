"""Pruefstand fuer das Seeradar (lua/seeradar.lua, Chip 'Figet Marena Seeradar'): Radar 6 am Mast (gespiegelt, RS -1,
Winkel ab Sockel), Schirm folgt dem Gimbal mit 0,03 rad je Tick, Strahl 0,1 U breit; je Ziel im Strahl alle 2 Ticks
eine Meldung mit Rauschen (+-0,001 U Winkel, +-1 % Entfernung), sonst bleibt der alte Eintrag mit wachsender 'Zeit
seit Meldung'. Hoechstens 6 Ziele (die naechsten). Schiff faehrt, Kurs ueber den Kompass (zaehlt gegen den
Uhrzeigersinn: Kompass = -Kurs).
"""
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from test_lage import lade  # noqa: E402
from test_schiff import pruefe  # noqa: E402
from build_schiff import minify, LUA_DIR, LUA_LIMIT  # noqa: E402
from build_lage import kopf  # noqa: E402
import build_seeradar  # noqa: E402

PR = {n: v for n, v, _ in build_seeradar.PROPS}
PR.update({"Schreiber Port": 0, "Schreiber Zeichen": 3000})
WR = lambda v: (v + .5) % 1 - .5


def lauf(ziele, secs=30, kurs=0.0, tempo=10.0, tippen=None, seed=1, drehen=2, waffe=0, aus=None):
    """ziele: Liste dicts (e, n, h, ve, vn, bis s) in der Welt relativ zum Startort des Schiffs; tippen(t, g) -> (x, y)
    Pixel oder None; waffe = am Bildschirm gewaehlte Waffe (Bedienung Zahl 2); aus: Liste, bekommt je Tick die Ausgaenge.
    -> (Lua-Globals, io, Liste der Gimbal-Befehle)"""
    random.seed(seed)
    src = kopf(minify(open(os.path.join(LUA_DIR, "seeradar.lua"), encoding="utf-8").read()), "sr")
    pr = dict(PR)
    pr["Bild drehen"] = drehen
    _, g, io = lade(src, pr)
    io["w"] = (96, 96)
    px, pz, al = 0.0, 0.0, 3.0
    kopf_r = 0.0                       # Schirm-Stellung im Radar-Rahmen (U)
    befehl = 0.0
    alt = {}                           # Eintraege je Platz: [R, a0, e0, t0]
    gb = []
    for t in range(int(60 * secs)):
        px += tempo * math.sin(kurs * 2 * math.pi) / 60
        pz += tempo * math.cos(kurs * 2 * math.pi) / 60
        kopf_r = WR(kopf_r + max(-.03 / (2 * math.pi), min(.03 / (2 * math.pi), WR(befehl - kopf_r))))
        strahl = WR(-kopf_r)           # Strahl ab Bug (gespiegelt)
        sicht = []
        for k, z in enumerate(ziele):
            if t / 60 > z.get("bis", 1e9):
                continue
            e, n = z["e"] + z.get("ve", 0) * t / 60 - px, z["n"] + z.get("vn", 0) * t / 60 - pz
            R = math.hypot(e, n)
            b = WR(math.atan2(e, n) / (2 * math.pi) - kurs)
            if abs(WR(b - strahl)) < 0.05:
                sicht.append((R, k, b, math.atan2(z["h"] - al - 2.25, R) / (2 * math.pi)))
        sicht.sort()
        n_ = {}
        b_ = {}
        for i in range(1, 6):
            if i <= len(sicht):
                R, k, b, el = sicht[i - 1]
                if t % 2 == 0 or k not in alt:
                    alt[k] = [R * (1 + random.uniform(-.01, .01)), WR(-(b + random.uniform(-.001, .001))),
                              el + random.uniform(-.001, .001), 0.0]
                else:
                    alt[k][3] += 1 / 60
                n_.update({4 * i - 3: alt[k][0], 4 * i - 2: alt[k][1], 4 * i - 1: alt[k][2], 4 * i: alt[k][3]})
                b_[i] = True
        n_.update({25: px, 26: al, 27: pz, 28: 0.0, 29: 0.0, 30: -kurs})
        tp = tippen(t, g) if tippen else None
        if tp:
            b_[32] = True
            n_[21], n_[22] = tp
        n_[23] = waffe
        io["n"], io["b"] = n_, b_
        io["on"].clear()
        g.onTick()
        befehl = io["on"].get(1, 0.0)
        gb.append((befehl, io["on"].get(2, 0.0)))
        if aus is not None:
            aus.append(dict(io["on"]))
    return g, io, gb


def kontakte(g):
    out = []
    for c in g.K.values():
        out.append({"e": c.p[1], "n": c.p[2], "h": c.h, "a": c.a, "v": c.v, "s": c.s})
    return out


def test_seeradar():
    rueck = []
    src = kopf(minify(open(os.path.join(LUA_DIR, "seeradar.lua"), encoding="utf-8").read()), "sr")
    rueck.append(("Skript %d Zeichen (hoechstens %d)" % (len(src), LUA_LIMIT), len(src) <= LUA_LIMIT))
    ziele = [dict(e=2000 * math.sin(.125 * 2 * math.pi), n=2000 * math.cos(.125 * 2 * math.pi), h=-2, ve=8),   # Schiff
             dict(e=-3000, n=300, h=15),                                                                     # Land
             dict(e=500, n=1400, h=150, ve=-20),                                                             # Heli
             dict(e=-1200, n=-1500, h=3, bis=15),                                                            # Boot weg
             dict(e=10, n=20, h=10, vn=10)]                                                                  # eigenes Deck
    g, io, gb = lauf(ziele, secs=30, drehen=0)
    k = kontakte(g)
    py = 10 * 30

    def nahe(e, n, r=120):
        return [c for c in k if math.hypot(c["e"] - e, c["n"] - n) < r]
    s_ = nahe(ziele[0]["e"] + 8 * 30, ziele[0]["n"], 150)
    l_ = nahe(-3000, 300)
    h_ = nahe(500 - 20 * 30, 1400, 200)
    b_ = nahe(-1200, -1500)
    rueck.append(("Schiff 2 km, 8 m/s: ein Kontakt, See (Art 0), Hoehe %.1f m" % (s_[0]["h"] if s_ else 99),
                  len(s_) == 1 and s_[0]["a"] == 0))
    rueck.append(("Bodenziel 3 km, 15 m hoch: Land (Art 1), Hoehe %.1f m" % (l_[0]["h"] if l_ else 99),
                  len(l_) == 1 and l_[0]["a"] == 1))
    rueck.append(("Heli 150 m hoch: Luft (Art 2, nicht gezeigt)", len(h_) >= 1 and all(c["a"] == 2 for c in h_)))
    rueck.append(("Boot verschwindet bei 15 s: nach 30 s vom Schirm (12 s vergessen)", not b_))
    rueck.append(("Eigenes Deck (22 m) zaehlt nicht", not nahe(10, py + 20, 40)))
    # schnelles Boot (20 m/s) quer: bleibt ein Kontakt
    g4, _, _ = lauf([dict(e=-1500, n=1800, h=0, ve=20)], secs=30, tempo=5)
    k4 = kontakte(g4)
    rueck.append(("Boot 20 m/s quer in 2,3 km: ein Kontakt (%d), See" % len(k4), len(k4) == 1 and k4[0]["a"] == 0))
    rueck.append(("Kontakte gesamt %d (erwartet 3)" % len(k), len(k) == 3))
    seiten = [b for b, _ in gb]
    runden = sum(abs(WR(b - a)) for a, b in zip(seiten, seiten[1:]))
    rueck.append(("Gimbal: Hoehe 0, Seite kreist (%.1f Runden in 30 s, hoechstens 7,5)" % runden,
                  all(p == 0 for _, p in gb) and 6 <= runden <= 7.6))
    # Bild: Bug oben; Schiff rechts voraus bei 45 Grad, Bodenziel links (Reichweite 4 km)
    io["draw"].clear()
    g.onDraw()
    d = io["draw"]
    punkte = []
    farbe = None
    for x in d:
        if x[0] == "c":
            farbe = x[1:4]
        if x[0] == "rf" and x[3] == 2:
            punkte.append((x[1] + 1, x[2] + 1, farbe))
    r = 47
    blau = [(x, y) for x, y, f in punkte if f[2] > f[1]]
    gruen = [(x, y) for x, y, f in punkte if f[1] > f[2]]
    rueck.append(("Bild (Reichweite %g): Schiff blau rechts oben, Bodenziel gruen links (%d blau, %d gruen)" % (
                  g.rr, len(blau), len(gruen)),
                  g.rr == 10000 and len(blau) == 1 and len(gruen) == 1 and blau[0][0] > 48 + 3 and blau[0][1] < 48 - 3
                  and gruen[0][0] < 48 - 8))
    # Kurs 90 Grad (Ost): ein Ziel genau im Norden liegt links
    g2, io2, _ = lauf([dict(e=0, n=2500, h=0)], secs=12, kurs=0.25, tempo=0, drehen=0)
    io2["draw"].clear()
    g2.onDraw()
    pk = [x for x in io2["draw"] if x[0] == "rf" and x[3] == 2]
    rueck.append(("Kurs Ost: Ziel im Norden links auf dem Schirm", len(pk) == 1 and pk[0][1] < 48 - 8 and abs(pk[0][2] + 1 - 48) < 5))
    # Bild drehen 2 (Monitor liegt flach links neben dem Sitz): Schiff unten links, Schrift unten rechts, Bug-Strich
    # nach unten
    g5, io5, _ = lauf(ziele, secs=30, drehen=2)
    io5["draw"].clear()
    g5.onDraw()
    d5 = io5["draw"]
    farbe, bl, schrift = None, [], []
    for x in d5:
        if x[0] == "c":
            farbe = x[1:5]
        if x[0] == "rf" and x[3] == 2 and farbe[2] > farbe[1]:
            bl.append((x[1] + 1, x[2] + 1))
        if x[0] == "rf" and x[3] == 1:
            schrift.append((x[1], x[2]))
    bug = [x for x, f in zip(d5, [None] + d5) if x[0] == "l" and abs(x[1] - 48) < 1 and abs(x[2] - 48) < 1 and abs(x[3] - 48) < 1]
    rueck.append(("Bild drehen 2: Schiff unten links (%s), Schrift unten rechts, Bug-Strich nach unten" % (bl,),
                  len(bl) == 1 and bl[0][0] < 48 - 3 and bl[0][1] > 48 + 3 and schrift
                  and min(x for x, _ in schrift) > 48 + 20 and min(y for _, y in schrift) > 48 + 20
                  and any(l[4] > 48 + 40 for l in bug)))
    # Zoom selbst: zwei Boote 300 m auseinander in 1,5 km -> 2,5 km (bei 5 km laegen sie unter 5 Pixel auseinander)
    boote = [dict(e=-150, n=1500, h=0), dict(e=150, n=1500, h=0)]
    g6, _, _ = lauf(boote, secs=15, tempo=0)
    rueck.append(("Zoom selbst: zwei Boote 300 m auseinander in 1,5 km -> 2,5 km (%g)" % g6.rr, g6.rr == 2500))
    g7, _, _ = lauf([dict(e=-150, n=1500, h=0)], secs=15, tempo=0)
    rueck.append(("Zoom selbst: ein Boot -> 10 km (%g)" % g7.rr, g7.rr == 10000))

    def tipp_auf(e, n, ab_s):
        def f(t, g):
            if int(ab_s * 60) <= t < int(ab_s * 60) + 2:
                R, rg = 47, g.rr
                d = math.hypot(e, n)
                b = math.atan2(e, n)
                lx, ly = d / rg * R * math.sin(b), d / rg * R * math.cos(b)
                return 48 - lx, 48 + ly          # Bild drehen 2
            return None
        return f
    # Antippen mit BC gewaehlt: BC schiesst 20 s darauf, dann Automatik
    aus = []
    lauf(boote, secs=40, tempo=0, waffe=1, tippen=tipp_auf(-150, 1500, 12), aus=aus)
    t0 = 12 * 60 + 2
    a = aus[t0]
    rueck.append(("Tippen mit BC gewaehlt: Kanone 1, Ziel %.0f/%.0f (soll -150/1500), Kennung %d" % (
                  a.get(4, 0), a.get(5, 0), a.get(7, 0)),
                  a.get(3) == 1 and abs(a.get(4, 0) + 150) < 60 and abs(a.get(5, 0) - 1500) < 60 and a.get(7) == 101))
    ende = next((t for t in range(t0, len(aus)) if aus[t].get(3) == 0), None)
    rueck.append(("... nach 20 s wieder Automatik (nach %.1f s)" % ((ende - t0) / 60 if ende else -1),
                  ende is not None and 19.5 < (ende - t0) / 60 < 20.5))
    rueck.append(("... keine Koordinaten ausgegeben", not any(o.get(101) for o in aus)))
    # Ziel verschwindet: Kanone gibt nach ~1,5 Runden auf
    aus = []
    lauf([dict(e=-150, n=1500, h=0, bis=16), dict(e=150, n=1500, h=0)], secs=40, tempo=0, waffe=2,
         tippen=tipp_auf(-150, 1500, 12), aus=aus)
    ende = next((t for t in range(t0, len(aus)) if aus[t].get(3) == 0), None)
    rueck.append(("Ziel weg (ab 16 s): AC gibt nach %.1f s auf (Kanone war 2: %s)" % (
                  (ende - t0) / 60 if ende else -1, aus[t0].get(3) == 2),
                  aus[t0].get(3) == 2 and ende is not None and (ende - t0) / 60 < 12))
    # Antippen ohne Kanone: Koordinaten X/Y
    aus = []
    g8, io8, _ = lauf(boote, secs=14, tempo=0, waffe=0, tippen=tipp_auf(150, 1500, 12), aus=aus)
    a = aus[-1]
    rueck.append(("Tippen ohne Kanone: Koordinaten X %.0f / Y %.0f (soll 150/1500), Kanone 0" % (a.get(8, 0), a.get(9, 0)),
                  a.get(101) and abs(a.get(8, 0) - 150) < 60 and abs(a.get(9, 0) - 1500) < 60 and a.get(3, 0) == 0))
    io8["draw"].clear()
    g8.onDraw()
    rot = [x for x in io8["draw"] if x[0] == "r"]
    rueck.append(("... Auswahl rot umrandet", len(rot) == 1))
    # v2.1: Ziel hinter der Reichweite (auf dem Rand) antippen: drittes Boot in 4 km, Reichweite bleibt 2,5 km
    def tipp_rand(e, n, ab_s):
        def f(t, g):
            if int(ab_s * 60) <= t < int(ab_s * 60) + 2:
                b = math.atan2(e, n)
                return 48 - 47 * math.sin(b), 48 + 47 * math.cos(b)          # Bild drehen 2, auf dem Rand
            return None
        return f
    aus = []
    gr, ior, _ = lauf(boote + [dict(e=2000, n=3500, h=0)], secs=14, tempo=0, waffe=0, tippen=tipp_rand(2000, 3500, 12),
                      aus=aus)
    a = aus[-1]
    rueck.append(("Rand-Ziel (4 km bei %g km): antippbar, Koordinaten %.0f/%.0f (soll 2000/3500)" % (
                  gr.rr / 1000, a.get(8, 0), a.get(9, 0)),
                  gr.rr == 2500 and a.get(101) and abs(a.get(8, 0) - 2000) < 80 and abs(a.get(9, 0) - 3500) < 80))
    ior["draw"].clear()
    gr.onDraw()
    rot = [x for x in ior["draw"] if x[0] == "r"]
    rueck.append(("... auf dem Rand rot umrandet", len(rot) == 1 and abs(math.hypot(rot[0][1] + 3.5 - 48, rot[0][2] + 3.5 - 48) - 47) < 3))
    # daneben tippen = abwaehlen
    g9, _, _ = lauf(boote, secs=14, tempo=0, waffe=1, tippen=lambda t, g: (5, 5) if t in (12 * 60, 12 * 60 + 1) else None)
    rueck.append(("Daneben tippen: nichts gewaehlt, keine Kanone", g9.sel is None and g9.dw == 0))
    # UEBERGABE: Bedienung durchreichen, Kanone 1 ersetzen
    src2 = minify(open(os.path.join(LUA_DIR, "uebergabe.lua"), encoding="utf-8").read())
    _, gu, iou = lade(src2, PR)
    ein_n = {i: float(i * 10) for i in range(1, 26)}
    ein_n[2] = 1
    ein_b = {i: (i % 3 == 0) for i in range(1, 17)}
    ein_b[1] = True
    iou["n"], iou["b"] = dict(ein_n), dict(ein_b)
    gu.onTick()
    gleich = all(iou["on"].get(i) == ein_n[i] for i in range(1, 26)) and all(
        bool(iou["on"].get(100 + i)) == ein_b[i] for i in range(1, 17))
    n2 = dict(ein_n)
    n2.update({26: 1, 27: 500.0, 28: 600.0, 29: 15.0, 30: 101.0, 31: 0.0, 32: 0.0})
    iou["n"], iou["b"] = n2, dict(ein_b)
    iou["on"].clear()
    gu.onTick()
    o = iou["on"]
    ersetzt = (o.get(7) == 101 and o.get(8) == 500 and o.get(9) == 600 and o.get(10) == 15 and o.get(105) is True
               and o.get(109) is True and o.get(3) == 9 and o.get(4) == 500 and o.get(11) == ein_n[11] and o.get(117))
    rueck.append(("Uebergabe: ohne Seeradar-Ziel alles durchgereicht; mit: BC-Ziel, Feuer frei, Kamera ersetzt",
                  gleich and ersetzt))
    iou["draw"].clear()
    iou["w"] = (32, 64)
    gu.onDraw()
    return pruefe(rueck)


if __name__ == "__main__":
    print("ALLES OK" if test_seeradar() else "FEHLER")
