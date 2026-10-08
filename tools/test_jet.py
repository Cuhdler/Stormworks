"""Pruefstand fuer den ferngesteuerten Jet: lua/jet.lua (Chip im Jet) und lua/jet_steuerung.lua (Chip im Schiff).
- Jet: Lage aus den Kipp-Werten des verkehrt eingebauten Physik-Sensors, Elevon-Mischung, Notprogramm ohne Funk,
  Start-Nick, Sprit; einfaches Dreh-Modell (Ruderwirkung ~ Tempo^2, Daempfung) fuer Querlage und Nick
- Schiff: Maus-Knueppel mit Totzone, Gas/Zoom, Tasten, Lebenszeichen, Kamera-Frequenz, Anzeige ohne Eingaenge
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from test_lage import lade  # noqa: E402
from test_schiff import pruefe  # noqa: E402
from build_schiff import minify, LUA_DIR  # noqa: E402
from build_lage import SCHREIBER_PROPS  # noqa: E402
import build_jet as bj  # noqa: E402

PJ = {n: v for n, v, _ in bj.PROPS_JET}
PS = {n: v for n, v, _ in bj.PROPS_ST}
PS.update({n: v for n, v, _ in SCHREIBER_PROPS})
PS["Schreiber Port"] = 0


def src(n):
    return minify(open(os.path.join(LUA_DIR, n), encoding="utf-8").read())


class Jet:
    """Jet-Chip mit einfachem Dreh-Modell: Querlage/Nick (Grad) folgen den Rudern."""
    def __init__(self, v=60.0, th=0.0, ph=0.0):
        _, self.g, self.io = lade(src("jet.lua"), PJ)
        self.v, self.th, self.ph, self.q, self.p = v, th, ph, 0.0, 0.0
        self.hb = 0
        self.tank = 400.0

    def tick(self, quer=0.0, nick=0.0, gas=0.5, funk=True, booster=False, an=True, seite=0.0):
        if funk:
            self.hb += 1
        io = self.io
        io["n"] = {1: quer, 2: nick, 3: gas, 4: seite, 5: 0.0, 6: float(self.hb), 20: 100.0, 21: 300.0, 22: 200.0,
                   23: self.v, 24: -self.th / 360.0, 25: -self.ph / 360.0, 26: 0.1, 27: self.tank}
        io["b"] = {1: an, 2: booster, 3: False, 4: True}
        self.g.onTick()
        o = io["on"]
        l, r = o[1], o[2]
        e, a = (l + r) / 2, (l - r) / 2
        k = (self.v / 60.0) ** 2
        self.p += (300 * a * k - 4 * self.p) / 60
        self.q += (150 * e * k - 4 * self.q) / 60
        self.ph += self.p / 60
        self.th += self.q / 60
        return o


def test_jet():
    r = []
    j = Jet(th=90.0)
    o = j.tick()
    r.append(("Jet steht senkrecht (Kippung z -0,25): Nick 90 Grad gemeldet (%.1f)" % o[14], abs(o[14] - 90) < 1e-6))
    j = Jet()
    o = j.tick(nick=1.0)
    r.append(("Knueppel hoch: beide Elevons gleich (Hoehenruder) %.2f / %.2f" % (o[1], o[2]), o[1] > 0.5 and abs(o[1] - o[2]) < 1e-9))
    j = Jet()
    o = j.tick(quer=1.0)
    r.append(("Knueppel rechts: Elevons gegenlaeufig %.2f / %.2f" % (o[1], o[2]), o[1] > 0.5 and abs(o[1] + o[2]) < 0.2))
    # Querlage 60 Grad halten (Regler + Dreh-Modell), bei 30 / 60 / 120 m/s
    for v in (30.0, 60.0, 120.0):
        j = Jet(v=v)
        mx = 0
        for t in range(6 * 60):
            j.tick(quer=1.0)
            mx = max(mx, j.ph)
        r.append(("Querlage 60 Grad bei %3d m/s: %.1f Grad, Ueberschwingen %.1f" % (v, j.ph, mx - 60),
                  abs(j.ph - 60) < 5 and mx - 60 < 12))
    j = Jet(ph=40.0, th=-20.0)
    for t in range(8 * 60):
        j.tick()
    r.append(("Knueppel los: Fluegel gerade (%.1f), Nick auf Trimmung + Kurve (%.1f)" % (j.ph, j.th),
              abs(j.ph) < 3 and abs(j.th - 4) < 3))
    # Notprogramm
    j = Jet(ph=30.0)
    for t in range(30):
        j.tick(quer=1.0, gas=0.9)
    for t in range(6 * 60):
        o = j.tick(quer=1.0, gas=0.9, funk=False)
    r.append(("Funk weg: Notprogramm (Flugdaten Bool 12), Fluegel gerade (%.1f), Gas 0,6 (%.2f)" % (j.ph, o[4]),
              o[112] is True and abs(j.ph) < 5 and abs(o[4] - 0.6) < 1e-9))
    o = j.tick(quer=1.0, gas=0.9)
    r.append(("Funk wieder da: Notprogramm aus, Gas 0,9", o[112] is False and abs(o[4] - 0.9) < 1e-9))
    # Start-Nick
    j = Jet(th=90.0, v=40.0)          # Tempo kurz nach dem Zuenden
    j.tick()
    j.tick(booster=True)
    o = j.tick(booster=True)
    r.append(("Booster: Zuendung durchgereicht", o[102] is True))
    nts = []
    for t in range(4 * 60):
        j.tick()
        nts.append(j.th)
    r.append(("Start: erst ~45 Grad Nick halten (nach 2 s %.0f Grad)" % nts[120], 30 < nts[120] < 70))
    # Sprit, Triebwerk aus
    j = Jet()
    j.tick()
    j.tank = 100.0
    o = j.tick(an=False)
    r.append(("Sprit 25 %% (%.0f), Triebwerk aus: Gas 0, Verdichter aus" % o[18], abs(o[18] - 25) < 1e-6 and o[4] == 0
              and o[101] is False))
    r.append(("Frequenzen Befehle/Daten 7301/7302, Senden an", o[6] == 7301 and o[7] == 7302 and o[105] is True))

    # --- Schiff ---
    _, g, io = lade(src("jet_steuerung.lua"), PS)
    io["w"] = (96, 96)

    def st(lx=0.0, ly=0.0, ws=0.0, ad=0.0, pf=0.0, hk=(), leer=False, sitz=True, echo=None, fd=None):
        n = {1: ad, 2: ws, 3: 0.0, 4: pf, 5: lx, 6: ly, 7: 0.0, 8: 0.0, 9: 1.0}
        n.update(fd or {11: 250.0, 12: 50.0, 13: 0.25, 14: 3.0, 15: 10.0, 16: 3000.0, 17: 4000.0, 18: 80.0, 21: 1.0})
        n[20] = float(echo if echo is not None else st.e)
        io["n"] = n
        io["b"] = {k + 1: (k + 1) in hk for k in range(6)}
        io["b"].update({7: leer, 8: sitz})
        g.onTick()
        st.e += 1
        return io["on"]
    st.e = 0
    o = st(lx=0.04, ly=0.03)
    r.append(("Blick halb rechts/oben: Quer %.2f, Nick %.2f (Totzone 0,1)" % (o[1], o[2]), abs(o[1] - (0.5 - 0.1) / 0.9) < 1e-6
              and abs(o[2] - (0.5 - 0.1) / 0.9) < 1e-6))
    o = st(lx=0.004)
    r.append(("Blick fast mittig: in der Totzone 0", o[1] == 0))
    o = st(lx=0.04, sitz=False)
    r.append(("Sitz leer: Knueppel 0", o[1] == 0 and o[2] == 0))
    for _ in range(60):
        o = st(ws=1.0)
    r.append(("W 1 s: Gas 0,4 (%.2f)" % o[3], abs(o[3] - 0.4) < 1e-6))
    o = st(leer=True)
    r.append(("Leertaste ohne Triebwerk: keine Booster", o[102] is False))
    st(hk=(1,))
    o = st(leer=True)
    r.append(("Hotkey 1 Triebwerk an, Leertaste: Booster", o[101] is True and o[102] is True))
    r.append(("Magnete beim Laden an", o[104] is True))
    st(hk=(3,))
    o = st()
    r.append(("Hotkey 3: Magnete aus", o[104] is False))
    r.append(("Kamera vorn: Video-Frequenz 7301", o[12] == 7301))
    st(hk=(4,))
    o = st()
    r.append(("Hotkey 4: Kamera unten, Video-Frequenz 7302", o[12] == 7302))
    hb1 = o[6]
    o = st()
    r.append(("Lebenszeichen zaehlt hoch", o[6] == hb1 + 1))
    for _ in range(70):
        st(echo=5)
    io["draw"].clear()
    g.onDraw()
    t = [e[3] for e in io["draw"] if e[0] == "t"]
    r.append(("Echo steht 70 Ticks: 'KEIN SIGNAL'; Anzeige %s" % t, "KEIN SIGNAL" in t and " 97KN" in t and " 250M" in t
              and "5.0KM" in t))
    return pruefe(r)


if __name__ == "__main__":
    print("ALLES OK" if test_jet() else "FEHLER")
