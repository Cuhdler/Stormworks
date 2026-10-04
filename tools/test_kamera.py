"""Pruefstand fuer die Dachkamera (lua/kamera.lua, Chip 'Figet Marena Kamera'): Camera Stabilized auf dem Bruecken-Dach.
Kamera-Modell nach Andres Log 04.10. 15:01: Pivot/Pitch sind Tempo-Eingaenge mit Totzone 0,1 (darueber 0,106 U/s je 1,
8 Ticks Verzug); Composite 4/5 = Neigung/Drehung des Kopfs in U relativ zum Spawnen (Start: senkrecht nach oben).
Unbekannt und darum in Varianten: wohin Drehung 0 zeigt, in welche Richtung die Drehung waechst, zu welcher Seite die
Kamera bei positivem Pitch kippt. Laser: trifft das Meer (Hoehe 0) beim Blick nach unten; nach achtern trifft er bis
~7 Grad unter waagerecht den eigenen Mast (9 m); ohne Treffer 4000.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from test_lage import lade  # noqa: E402
from test_schiff import pruefe  # noqa: E402
from build_schiff import minify, LUA_DIR  # noqa: E402
import build_kamera  # noqa: E402

PR = {n: v for n, v, _ in build_kamera.PROPS}
PR.update({"Schreiber Port": 0, "Schreiber Zeichen": 3000})
WR = lambda v: (v + .5) % 1 - .5


def lauf(var, ziele, secs=20, hd=0.1, wahl=1, own=(0.0, 0.0), kv=0.106, rel=False, sicht=None, h6=(), aus=None, korr_an=True):
    """var = (Drehrichtung s, Kipp-Seite p, Drehung 0 ab Bug o); ziele: Liste (ab s, Ost, Nord, Hoehe ueber dem Meer, Tempo
    Ost, Nord) relativ zum Schiff; rel = Laser-Ziel relativ zur Kamera melden.
    -> (Liste je Tick (t, Fehler Richtung U, Fehler Hoehe U, Bildwinkel rad, Entfernung, Phase), Lua-Globals)"""
    s_, p_, o_ = var
    src = minify(open(os.path.join(LUA_DIR, "kamera.lua"), encoding="utf-8").read())
    _, g, io = lade(src, PR)
    px, py, pz = 100.0, 7.0, 200.0
    k4, k5 = 0.0, 0.0
    puffer = [(0.0, 0.0)] * 8                     # 8 Ticks Verzug
    eff = lambda c: (1 if c > 0 else -1) * max(0.0, abs(c) - 0.1) * kv / 60
    out = []
    zt = [list(z) for z in ziele]
    for t in range(60 * secs):
        px, pz = px + own[0] / 60, pz + own[1] / 60
        puffer.append((io["on"].get(1, 0.0), io["on"].get(2, 0.0)))
        cy_, cp_ = puffer.pop(0)
        k5 += eff(cy_)
        k4 += eff(cp_)
        k4 = max(-0.5, min(0.5, k4))
        el = 0.25 - abs(k4)
        blick = WR(o_ + s_ * k5 + (0.5 if p_ * k4 < 0 else 0.0))     # Richtung ab Bug (Uhrzeigersinn)
        h = hd * 2 * math.pi
        cx, cz, cy = px + 5.75 * math.sin(h), pz + 5.75 * math.cos(h), py + 1.5
        b = (hd + blick) * 2 * math.pi
        ew = el * 2 * math.pi
        n = {7: 0.0, 8: 0.0, 9: 0.0, 10: k4, 11: k5, 32: 4000.0}
        if abs(WR(blick - 0.5)) < 0.1 and ew > -0.12:
            n[32] = 9.0                                                 # Mast
        elif ew < -1e-3:
            d = cy / math.sin(-ew)
            if d < 3900:
                hx, hz = cx + d * math.cos(ew) * math.sin(b), cz + d * math.cos(ew) * math.cos(b)
                n[7], n[8], n[9], n[32] = (hx - cx, -cy, hz - cz, d) if rel else (hx, 0.0, hz, d)
        aktiv = [z for z in zt if t >= z[0] * 60]
        for z in zt:
            z[1] += z[4] / 60 - own[0] / 60
            z[2] += z[5] / 60 - own[1] / 60
        if aktiv:
            z = aktiv[-1]
            n.update({2: wahl, 3: 1, 4: z[1], 5: z[2], 6: z[3]})
        else:
            n.update({2: wahl, 3: 0})
        n.update({23: hd, 26: px, 27: py, 28: pz, 29: 0.0, 30: 0.0})
        bl = sicht(t) if sicht else (0.0, 15 / 360)
        n.update({12: bl[0], 13: bl[1]})
        io["n"], io["b"] = n, {1: t in h6, 2: True, 3: korr_an}
        io["on"].clear()
        g.onTick()
        fov = PR["FOV weit rad"] - io["on"].get(3, 0.0) * (PR["FOV weit rad"] - PR["FOV eng rad"])
        if aus is not None:
            aus.append(dict(io["on"]))
        if aktiv:
            z = aktiv[-1]
            dE, dN, dU = px + z[1] - cx, pz + z[2] - cz, z[3] - cy
            ho = math.hypot(dE, dN)
            fr = WR(math.atan2(dE, dN) / (2 * math.pi) - (hd + blick))
            fe = math.atan2(dU, ho) / (2 * math.pi) - el
            out.append((t, fr, fe, fov, math.hypot(ho, dU), g.ph))
        else:
            out.append((t, None, None, fov, 0, g.ph))
    return out, g


def test_kamera():
    rueck = []
    varianten = [((1, 1, 0.0), False), ((-1, 1, 0.0), False), ((1, -1, 0.25), False), ((-1, -1, 0.3), True),
                 ((1, 1, 0.5), False)]          # die letzte schaut zuerst nach achtern: Laser trifft den Mast
    for var, rel in varianten:
        # Schiff 2 km rechts voraus, faehrt quer; wir fahren 15 m/s
        ziele = [(0, 2000 * math.sin(.5), 2000 * math.cos(.5), 2.0, -6.0, 4.0)]
        r, g = lauf(var, ziele, secs=30, own=(0.0, 15.0), rel=rel)
        k = [q for q in r if q[0] > 20 * 60 and q[1] is not None]
        fr = max(abs(q[1]) for q in k)
        fe = max(abs(q[2]) for q in k)
        fov = sorted(q[3] for q in k)[len(k) // 2]
        teil = 40 / k[-1][4] / (fov / 3)
        bereit = next((q[0] for q in r if q[5] == 9), None)
        rueck.append(("Dachkamera %s%s: Messfahrt fertig nach %.1f s (Versuche %d, Tempo %.3f U/s), danach Fehler Richtung "
                      "%.4f U, Hoehe %.4f U; Schiff fuellt %.0f %% des mittleren Drittels" % (
                          var, " Laser relativ" if rel else "", (bereit or 0) / 60, g.nv, g.kv, fr, fe, teil * 100),
                      bereit is not None and bereit < 15 * 60 and fr < 0.003 and fe < 0.003 and 0.3 <= teil <= 0.7))
        # Flugzeug 1,5 km links, 300 m hoch, 80 m/s (Flak R)
        r2, _ = lauf(var, [(0, -1000.0, 1100.0, 300.0, 80.0, 20.0)], secs=30, wahl=4)
        k2 = [q for q in r2 if q[0] > 22 * 60 and q[1] is not None]
        fr2 = sorted(abs(q[1]) for q in k2)[int(len(k2) * .9)]
        fe2 = sorted(abs(q[2]) for q in k2)[int(len(k2) * .9)]
        rueck.append(("  Flugzeug 1,5 km, 300 m hoch, 80 m/s: Fehler Richtung %.4f / Hoehe %.4f U (90 %%)" % (fr2, fe2),
                      fr2 < 0.005 and fe2 < 0.005))
    # Korrektur per Blick (v2.0): Mitte bei X 0 / Y 15 Grad. 8-10 s: 2 Grad rechts vom Fadenkreuz (im Kreis 4 Grad);
    # 10-12 s: 20 Grad daneben (Umschauen - nichts); 12-14 s: 2 Grad unter dem Fadenkreuz; 15 s: Hotkey 6 kurz (0);
    # 17-19,5 s: auf eine andere Stelle schauen (X 3, Y 10 Grad) und Hotkey 6 2 s halten -> Mitte gelernt
    def sicht_(t):
        s_ = t / 60
        if 8 <= s_ < 10:
            return 5 / 360, 15 / 360
        if 10 <= s_ < 12:
            return 20 / 360, 15 / 360
        if 12 <= s_ < 14:
            return 0.0, 10 / 360
        if 17 <= s_:
            return 3 / 360, 10 / 360
        return 0.0, 15 / 360
    out = []
    ziele = [(0, 2000 * math.sin(.5), 2000 * math.cos(.5), 2.0, -6.0, 4.0)]
    r4, g4 = lauf((1, 1, 0.0), ziele, secs=21, wahl=2, sicht=sicht_, h6=set(range(15 * 60, 15 * 60 + 20)) |
                  set(range(17 * 60, 19 * 60 + 30)), aus=out)
    kx = lambda t: out[t].get(8, 0.0)           # AC = Waffe 2: Zahl 6 seitlich, 7 Hoehe -> hier Kanal 2+2w = 6
    k6 = lambda t: (out[t].get(6, 0.0), out[t].get(7, 0.0))
    a, b_, c, d, e = k6(int(8 * 60) - 1), k6(int(10 * 60) - 1), k6(int(12 * 60) - 1), k6(int(14 * 60) - 1), k6(int(16 * 60))
    rueck.append(("Korrektur AC: 5 Grad rechts 2 s -> %.5f U (soll ~0,0004); Umschauen 20 Grad -> %.5f U (bleibt); 5 Grad unten -> Hoehe "
                  "%.5f U; Hotkey 6 kurz -> %.5f/%.5f" % (b_[0] - a[0], c[0] - b_[0], d[1] - c[1], e[0], e[1]),
                  0.0003 < b_[0] - a[0] < 0.0005 and abs(c[0] - b_[0]) < 1e-9 and -0.0005 < d[1] - c[1] < -0.0003 and e == (0.0, 0.0)
                  and all(abs(out[t].get(4, 0.0)) < 1e-12 for t in range(len(out)))))
    rueck.append(("Hotkey 6 2 s gehalten: Mitte gelernt (X %.1f / Y %.1f Grad, soll 3 / 10)" % (g4.mx * 360, g4.my * 360),
                  abs(g4.mx * 360 - 3) < 0.01 and abs(g4.my * 360 - 10) < 0.01))
    g4.onDraw()
    # Knopf 'Aim correction' aus (Standard): Blick neben das Fadenkreuz aendert nichts, Ausgang 0
    out2 = []
    lauf((1, 1, 0.0), ziele, secs=15, wahl=2, sicht=sicht_, aus=out2, korr_an=False)
    rueck.append(("Knopf Zielkorrektur aus: Korrektur bleibt 0", all(abs(o.get(6, 0.0)) + abs(o.get(7, 0.0)) == 0 for o in out2)))
    r3, _ = lauf((1, 1, 0.0), [], secs=12, wahl=0)
    rueck.append(("ohne Waffe: weit (%.2f rad)" % r3[-1][3], abs(r3[-1][3] - PR["FOV ohne Ziel rad"]) < 0.05))
    return pruefe(rueck)


if __name__ == "__main__":
    print("ALLES OK" if test_kamera() else "FEHLER")
