"""Prueft den Chip "Figet Marena Flossen" (lua/flossen.lua) in einem einfachen Bewegungsmodell des Schiffs:
Heben, Nicken, Rollen mit Rueckstellung durch das Wasser, Daempfung, Wellen; jede Flosse drueckt mit cf*v^2*Ausschlag
(+ = nach oben) an ihrer Stelle (vorn hebt die Nase, hinten senkt sie; rechts hebt die rechte Seite).
Die Rumpf-Werte sind geschaetzt (Perioden 3 s Nicken/Heben, 5 s Rollen) - der Test prueft Vorzeichen, Daempfung und
dass die Regelung bei allen Tempi ruhig bleibt, nicht die genauen Zahlen.
"""
import math
import os
import sys
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_flossen  # noqa: E402
from test_schiff import load as lade, pruefe  # noqa: E402

PR = {n: v for n, v, _ in build_flossen.PROPS}
# Flossen: (Ausgang 1-6, Nick-Hebel, Roll-Hebel, Anzahl, Wirkrichtung); Nick-Hebel + = vor dem Schwerpunkt, Roll + = rechts;
# Wirkrichtung wie im Spiel (Test-Chip 02.10.): bei allen Flossen + = Vorderkante hoch = nach oben
# hinten: eine mittlere + eine grosse (12 statt 8 Flaeche) je Seite = 2.5 mittlere
# vorn-Mitte (v1.5): je eine grosse (1.5 mittlere) bei (+-9,-21,-2), 9 m vor dem Sensor
FLOSSEN = [(1, 1.0, -0.06, 2, 1), (2, 1.0, 0.06, 2, 1), (3, -1.1, -0.6, 2.5, 1), (4, -1.1, 0.6, 2.5, 1), (5, -0.6, -0.55, 1, 1), (6, -0.6, 0.55, 1, 1),
           (7, 0.56, -0.55, 1.5, 1), (8, 0.56, 0.55, 1.5, 1)]
LS = 22.0       # Heck-Flossen/Schrauben hinter dem Sensor (m)


class Rumpf:
    def __init__(self, v, welle=1.0, richtung=1.0, schlagseite=0.0, traeg=0.25, messer=False, sog=0.0):
        self.v, self.welle, self.richtung, self.schlag = v, welle, richtung, schlagseite
        # messer: Liquid Meter am Heck auf Schrauben-Hoehe (Kanal 20); sog: so tief (m) zieht alle 6 s fuer ~1 s das Wasser
        # unter dem Heck weg (Fahrt 02.10. 17:40, Schiff dabei gerade); tief: Schraube unter der Oberflaeche (m, normal 2)
        self.messer, self.sog, self.tief = messer, sog, 2.0
        # traeg: die Flossen folgen dem Befehl verzoegert (s); hs: Heck gegenueber der Welle (m, + = hoeher = Schrauben naeher an der Luft)
        self.traeg, self.ist, self.hs = traeg, {}, 0.0
        self.z = self.w = self.th = self.q = self.ro = self.p = 0.0
        self.t = 0.0
        self.KZ, self.CZ = (2 * math.pi / 3) ** 2, 0.8
        self.KT, self.CT = (2 * math.pi / 3) ** 2, 0.6
        self.KR, self.CR = (2 * math.pi / 5) ** 2, 0.3
        self.CF = 0.0061                     # alle 4 vorderen voll bei 30 m/s ~ 5 Grad Nick

    def sensor(self):
        s = {2: 10 + self.z, 13: self.v, 15: self.th / 360, 16: -self.ro / 360}
        if self.messer:
            s[20] = self.tief            # wie Andres Messer: meldet die Tiefe (+ unter Wasser), 'Heck-Wasser Richtung' -1
        return s

    def schritt(self, aus, dt=1 / 60):
        self.t += dt
        a = self.welle
        zw = 0.5 * a * math.sin(2 * math.pi * self.t / 4.0)
        tw = 3.0 * a * math.sin(2 * math.pi * self.t / 4.0 + 1.2)
        rw = 2.0 * a * math.sin(2 * math.pi * self.t / 6.5)
        fz = mz = mr = 0.0
        for i, ln, lr, n, wr in FLOSSEN:
            self.ist[i] = self.ist.get(i, 0.0) + (aus.get(i, 0.0) - self.ist.get(i, 0.0)) * min(1.0, dt / max(self.traeg, dt))
            f = n * self.CF * self.v ** 2 * self.ist[i] * self.richtung * wr
            fz += 0.04 * f
            mz += ln * f
            mr -= 0.19 * lr * f / 0.6
        self.w += (-self.KZ * (self.z - zw) - self.CZ * self.w + fz) * dt
        self.z += self.w * dt
        self.q += (-self.KT * (self.th - tw) - self.CT * self.q + mz) * dt
        self.th += self.q * dt
        self.p += (-self.KR * (self.ro - rw - self.schlag) - self.CR * self.p + mr) * dt
        self.ro += self.p * dt
        self.hs = (self.z - LS * math.radians(self.th)) - (zw - LS * math.radians(tw))
        ph = (self.t % 6.0) / 1.2
        mulde = self.sog * math.sin(math.pi * ph) ** 2 if ph < 1 else 0.0
        self.tief = 2.0 - self.hs - mulde


def fahrt(v_kn, props=None, welle=1.0, richtung=1.0, sek=40):
    _, g, io = lade("flossen.lua", dict(PR, **(props or {})))
    he = Rumpf(v_kn / 1.944, welle, richtung)
    th, ro, w, sat, http = [], [], [], 0, []
    for k in range(int(60 * sek)):
        io["n"] = he.sensor()
        io["on"].clear()
        g.onTick()
        aus = dict(io["on"])
        he.schritt(aus)
        while io["http"]:
            http.append(io["http"].pop(0))
            g.httpReply(http[-1][0], http[-1][1], "ok")
        if k > 600:
            th.append(he.th); ro.append(he.ro); w.append(he.w)
            sat += sum(1 for i in range(1, 7) if abs(aus.get(i, 0)) > 0.99)
    rms = lambda l: math.sqrt(sum(x * x for x in l) / len(l)) if l else 0.0
    return rms(th), rms(ro), rms(w), sat / max(1, len(th)) / 6, http


def test_flossen():
    rueck, ok = [], True
    for v in (10, 25, 45, 70):
        t0, r0, w0, _, _ = fahrt(v, {"Flossen an": 0})
        t1, r1, w1, sat, _ = fahrt(v)
        tf, rf, wf, _, _ = fahrt(v, richtung=-1.0)
        # bei langsamer Fahrt ist die Flossenkraft (~ v^2) zu klein: dort nur 'nicht schlechter'
        besser = (t1 < 0.8 * t0 and r1 < 0.8 * r0 if v >= 20 else t1 <= t0 and r1 <= r0) and w1 <= 1.02 * w0
        rueck.append(("%2d kn: Nick %.2f -> %.2f Grad, Roll %.2f -> %.2f Grad, Steigen %.2f -> %.2f m/s (falsch herum Nick %.2f), voll %2.0f %%"
                      % (v, t0, t1, r0, r1, w0, w1, tf, sat * 100), besser and tf > t1))
    # langsam: Flossen bleiben gerade
    _, g, io = lade("flossen.lua", PR)
    he = Rumpf(2 / 1.944)
    for _ in range(120):
        io["n"] = he.sensor(); io["on"].clear(); g.onTick(); he.schritt(dict(io["on"]))
    rueck.append(("2 kn: Flossen stehen gerade", all(abs(io["on"].get(i, 1)) < 1e-9 for i in range(1, 9))))
    # Schiff liegt still schief (rechts tief, Nase hoch) bei 45 kn ohne Wellen: Flossen richten es auf
    _, g, io = lade("flossen.lua", PR)
    he = Rumpf(45 / 1.944, welle=0.0)
    he.th, he.ro = 3.0, 3.0
    for _ in range(60 * 10):
        io["n"] = he.sensor(); io["on"].clear(); g.onTick(); he.schritt(dict(io["on"]))
    o = io["on"]
    rueck.append(("schief (Nase +3, rechts tief 3 Grad) -> nach 10 s Nick %.2f, Roll %.2f" % (he.th, he.ro), abs(he.th) < 0.5 and abs(he.ro) < 0.5))
    # dauernde Schlagseite links (-2 Grad, z. B. Beladung) bei 40 kn: der I-Anteil nimmt sie weg; wie v1.1 gepolt schaukelt es
    for name, props, soll in (("richtig", {}, True), ("wie v1.1 (links -1, rechts 1)", {"Richtung links": -1, "Richtung rechts": 1}, False),
                              ("wie v1.2 (links 1, rechts -1)", {"Richtung links": 1, "Richtung rechts": -1}, False)):
        _, g, io = lade("flossen.lua", dict(PR, **props))
        he = Rumpf(40 / 1.944, welle=0.5, schlagseite=-2.0)
        ro, th = [], []
        for k in range(60 * 60):
            io["n"] = he.sensor(); io["on"].clear(); g.onTick(); he.schritt(dict(io["on"]))
            if k > 60 * 40:
                ro.append(he.ro); th.append(he.th)
        mro, mth = sum(ro) / len(ro), max(abs(x) for x in th)
        rueck.append(("Schlagseite -2 Grad, %s: Roll im Mittel %+.2f, Nick hoechstens %.1f" % (name, mro, mth),
                      (abs(mro) < 1.0 and mth < 3) if soll else (abs(mro) > 1.5 and mth > 3)))   # ohne Flossen -2.3; bei 40 kn reicht die Kraft nicht ganz
    # Testmodus: im Stand alle Flossen auf Vorderkante hoch (links +, rechts - wegen Spiegelung)
    _, g, io = lade("flossen.lua", dict(PR, **{"Flossen Test": 1}))
    he = Rumpf(0.0)
    io["n"] = he.sensor(); io["on"].clear(); g.onTick()
    o = dict(io["on"])
    rueck.append(("Flossen Test 1: im Stand links %+.1f, rechts %+.1f (alle Vorderkanten hoch)" % (o[1], o[2]),
                  all(abs(o[i] - 0.7) < 1e-9 for i in range(1, 9))))
    # Wellenschlag (alle 5 s Bug 0.3 s hochgeworfen, Flossen 0.25 s verzoegert): das Heck (Schrauben) bleibt unten -
    # v1.3 drueckte danach den Bug runter und hebelte das Heck bis 1.4 m hoch (schlimmer als ohne Flossen: 0.8 m)
    for v in (40, 60):
        erg = {}
        for name, props in (("aus", {"Flossen an": 0}), ("an", {})):
            _, g, io = lade("flossen.lua", dict(PR, **props))
            he = Rumpf(v / 1.944, welle=0.0)
            hs = []
            for k in range(60 * 30):
                io["n"] = he.sensor(); io["on"].clear(); g.onTick(); he.schritt(dict(io["on"]))
                if (he.t % 5.0) < 0.3:
                    he.q += 45 / 60; he.w += 6 / 60
                if k > 300:
                    hs.append(he.hs)
            erg[name] = max(hs)
        rueck.append(("Wellenschlag %d kn: Heck steigt hoechstens %.2f m (ohne Flossen %.2f m)" % (v, erg["an"], erg["aus"]),
                      erg["an"] < 0.5 and erg["an"] < 0.6 * erg["aus"]))
    # Wasser zieht unter dem Heck weg (alle 6 s 1.6 m), Schiff liegt gerade: ohne Messer sieht der Chip nichts, mit Messer
    # drueckt er das Heck rechtzeitig runter
    # (v1.6: die Flossen bewegen das schwere Heck in der kurzen Zeit nur wenig - Fahrt 02.10. 18:07: selbst dauernd voll
    # runter hielt die Schrauben in hohen Wellen nicht im Wasser; hier zaehlt: hilft etwas, drueckt nicht dauernd)
    erg = {}
    for name, mess, sog in (("ohne Messer", False, 1.6), ("mit Messer", True, 1.6), ("ruhig", True, 0.0)):
        _, g, io = lade("flossen.lua", PR)
        he = Rumpf(45 / 1.944, welle=0.0, messer=mess, sog=sog)
        ti, hi = [], []
        for k in range(60 * 36):
            io["n"] = he.sensor(); io["on"].clear(); g.onTick(); o = dict(io["on"]); he.schritt(o)
            if k > 300:
                ti.append(he.tief)
                hi.append(o.get(3, 0.0))
        erg[name] = (min(ti), sum(1 for x in ti if x < 0.8) / len(ti) * 100, sum(hi) / len(hi))
    rueck.append(("Wasser zieht weg (1.6 m), 45 kn: Schraube flachste %.2f m / %.1f %% flacher 0.8 m ohne Messer -> %.2f m / %.1f %% mit"
                  % (erg["ohne Messer"][:2] + erg["mit Messer"][:2]),
                  erg["mit Messer"][0] > erg["ohne Messer"][0] + 0.1 and erg["mit Messer"][1] < erg["ohne Messer"][1]))
    rueck.append(("Messer, ruhige Fahrt (Schraube 2 m tief): hintere Flossen im Mittel %.3f (nicht dauernd runter wie v1.5)" % erg["ruhig"][2],
                  abs(erg["ruhig"][2]) < 0.05))
    # Schreiber
    _, _, _, _, http = fahrt(45, sek=5)
    zeilen = [z for _, b in http for z in urllib.parse.parse_qs(urllib.parse.urlparse(b).query)["d"][0].split(";")]
    rueck.append(("Schreiber: %d Zeilen in 5 s an Port %d, je 17 Werte" % (len(zeilen), PR["Log Port"]),
                  len(zeilen) >= 290 and all(len(z.split(",")) == 17 for z in zeilen) and all(p == PR["Log Port"] for p, _ in http)))
    return pruefe(rueck)


if __name__ == "__main__":
    ok = test_flossen()
    print("ALLES OK" if ok else "FEHLER")
    sys.exit(0 if ok else 1)
