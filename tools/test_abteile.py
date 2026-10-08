"""Pruefstand fuer die Abteil-Anzeige (lua/abteile_sammler.lua + lua/abteile.lua): Packen, Abteile und Tanks erkennen,
Schotten, Lenzpumpen, Sprit/Verbrauch, Batterie."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from test_lage import lade  # noqa: E402
from test_schiff import pruefe  # noqa: E402
from build_schiff import minify, LUA_DIR  # noqa: E402
import build_abteile as ba  # noqa: E402

PR = {n: v for n, v, _ in ba.PROPS}
TANK = [k - 1 for k in ba.TANKS]      # Index 0-17


class Anlage:
    def __init__(self):
        q = lambda n: minify(open(os.path.join(LUA_DIR, n), encoding="utf-8").read())
        _, self.gs, self.ios = lade(q("abteile_sammler.lua"), {})
        _, self.ga, self.ioa = lade(q("abteile.lua"), PR)
        self.ioa["w"] = (288, 160)

    def tick(self, liter, kap, touch=None, knopf=False, auto=False, fluss=(0.0, 0.0, 0.0), batt=(0.9, 0.9),
             tueren=(True,) * 5):
        """liter/kap: je Sensor 1-18; fluss/batt wie an den Formel-Bausteinen im Chip zusammengefasst"""
        self.ios["n"] = {i + 1: liter[9 + i] for i in range(9)}
        self.ios["n"].update({10 + i: kap[9 + i] for i in range(9)})
        self.gs.onTick()
        n = {i + 1: self.ios["on"].get(i + 1, 0.0) for i in range(9)}
        n[32] = self.ios["on"].get(32, 0.0)
        n.update({10 + i: liter[i] for i in range(9)})
        n.update({19 + i: kap[i] for i in range(9)})
        if touch:
            n[28], n[29] = touch
        n[30] = sum(max(f, 0.0) for f in fluss)
        n[31] = max(batt)
        self.ioa["n"] = n
        self.ioa["b"] = {1: touch is not None, 2: knopf, 3: auto}
        self.ioa["b"].update({4 + k: tueren[k] for k in range(5)})
        self.ga.onTick()
        return bool(self.ioa["on"].get(101))

    def texte(self):
        self.ioa["draw"].clear()
        self.ga.onDraw()
        return [e[3] for e in self.ioa["draw"] if e[0] == "t"]


def hafen():
    """Abteile trocken; 8 Tanks wie gespawnt (98,5 % voll), je Seite einer, links/rechts gleich gross."""
    kap = [40000.0] * 2 + [90000.0] * 2 + [5600.0] * 2 + [9000.0] * 2 + [70000.0] * 2 + [14200.0, 14200.0] \
        + [12000.0] * 2 + [17600.0] * 2 + [150000.0] * 2
    lit = [0.0] * 18
    for i in TANK:
        lit[i] = kap[i] * 0.985
    return lit, kap


def test_abteile():
    r = []
    a = Anlage()
    lit, kap = hafen()
    auf = a.tick(lit, kap, auto=True)
    for _ in range(30):
        a.tick(lit, kap, auto=True)
    t = a.texte()
    r.append(("Hafen, Tanks voll: kein WASSER!, Schotten bleiben auf, Pumpen aus", auf and a.tick(lit, kap, auto=True)
              and not a.ga.wz and not a.ioa["on"].get(103) and "WASSER!" not in t))
    r.append(("5 Abteile (nur Abteil-Sensoren), Namen ohne Seite wenn beide Sensoren im selben Raum %s" % t[1:12],
              len(a.ga.GL) == 5 and "BUG" in t and "MASCHINE" in t and "SEITE" in t))
    sprit = [x for x in t if x.startswith("SPRIT")]
    soll = sum(lit[i] for i in TANK)
    tanks = [x for x in t if x in ("98%", "99%")]
    r.append(("Sprit gesamt %s (soll %.0f L, 8 Tanks als Balken %s, Zeilen SB/BB)" % (sprit, soll, tanks),
              sprit and ("98%" in sprit[0] or "99%" in sprit[0]) and abs(a.ga.sp - soll) < 0.5 and len(tanks) == 8
              and "SB" in t and "BB" in t and "BUG" in t))
    r.append(("Batterie 90 %", "BATTERIE  90%" in t))
    # Verbrauch: 2 L/s ueber 4 Minuten aus allen Tanks gleichmaessig
    gesamt = soll
    for sek in range(240):
        for _ in range(60):
            a.tick(lit, kap)
        for i in TANK:
            lit[i] -= 2.0 * lit[i] / gesamt
        gesamt -= 2.0
    t = a.texte()
    vb = [x for x in t if x.startswith("VERBR")]
    r.append(("Verbrauch etwa 2 L/s und Restzeit %s (Rest %.0f L = %.1f h)" % (vb, gesamt, gesamt / 2 / 3600),
              vb and abs(a.ga.vb - 2.0) < 0.02 and "H" in vb[0]))
    # wenig Verbrauch: 0,2 L/s
    for sek in range(150):
        for _ in range(60):
            a.tick(lit, kap)
        for i in TANK:
            lit[i] -= 0.2 * lit[i] / gesamt
        gesamt -= 0.2
    r.append(("wenig Verbrauch 0,2 L/s erkannt (%.3f)" % a.ga.vb, abs(a.ga.vb - 0.2) < 0.01))
    # Wasser im Seitenabteil links 2 %: eigene Zeile, unter 'Auto zu'
    lit2 = list(lit)
    lit2[12] = 24.0
    a.tick(lit2, kap)
    auf = a.tick(lit2, kap)           # Sammler schickt abwechselnd gepackt / Liter
    t = a.texte()
    r.append(("Seite links 0,2 %%: eigene Zeile 'SEITE BB' 0.2%%, Schotten bleiben auf (%s)" % t[1:15],
              auf and len(a.ga.GL) == 6 and "SEITE BB" in t and "0.2%" in t))
    # Maschinenraum 10 % -> Schotten selbst zu
    lit2[16] = lit2[17] = 15000.0
    a.tick(lit2, kap)
    auf = a.tick(lit2, kap)
    r.append(("Maschinenraum 10 %: Schotten gehen selbst zu, WASSER!", not auf and a.ga.wz))
    t = a.texte()
    r.append(("Tueren-Kaestchen vom Schotten-Chip '1AUF'..'5AUF', Feld 'ALLE AUF'", "1AUF" in t and "5AUF" in t
              and "ALLE AUF" in t))
    a.tick(lit2, kap, touch=(240, 150))
    for _ in range(30):
        auf = a.tick(lit2, kap)
    r.append(("Feld unten rechts antippen: Schotten auf und bleiben auf", auf))
    a.tick(lit2, kap, knopf=True)
    r.append(("Knopf: wieder zu", not a.tick(lit2, kap)))
    a.tick(lit2, kap, touch=(50, 50))
    r.append(("Tippen auf den Grundriss schaltet nicht", not a.tick(lit2, kap)))
    # nicht dicht (Bug)
    kap3 = list(kap)
    kap3[0] = kap3[1] = 0.0
    lit3 = list(lit2)
    lit3[0] = lit3[1] = 3.5            # Sensoren 3,5 m ueber dem Wasser (z. B. Luke offen)
    a.tick(lit3, kap3)
    t = a.texte()
    r.append(("Bug nicht dicht, Sensoren ueber Wasser: 'BUG BB'/'BUG SB' OFFEN", t.count("OFFEN") == 2 and "BUG BB" in t
              and "BUG SB" in t))
    lit3[0] = -1.2                    # Sensor 1,2 m unter der Wasserlinie: Leck
    a.tick(lit3, kap3)
    t = a.texte()
    r.append(("Loch unter Wasser: 'LECK' (rot), zaehlt als voll", "LECK" in t and a.ga.wz))
    # Packen: groesste Kapazitaet, voll
    kap4, lit4 = list(kap), list(lit)
    kap4[17] = lit4[17] = 1500000.0
    a.tick(lit4, kap4)
    if a.ios["on"].get(32) == 1:
        a.tick(lit4, kap4)
    v = a.ios["on"].get(9)
    r.append(("Packen 1,5 Mio L voll = %d (exakt als 32-bit-Zahl)" % v, v == 7500 * 1000 + 999 and v < 2 ** 24))
    # Lenzpumpen: nur mit Schalter, ab 0,3 %, 20 s Nachlauf; Fluss und Summe
    b = Anlage()
    lit, kap = hafen()
    lw = list(lit)
    lw[8] = lw[9] = 700.0          # Abteil Mitte 1 %
    b.tick(lw, kap)
    r.append(("Wasser, Schalter aus: Pumpen aus", not b.ioa["on"].get(103)))
    for _ in range(60):
        b.tick(lw, kap, auto=True, fluss=(30.0, 10.0, 10.0))
    t = b.texte()
    r.append(("Schalter an: Pumpen an, 50 L/s, 1 s = 50 L raus %s" % [x for x in t if "PUMPEN" in x or "RAUS" in x],
              b.ioa["on"].get(103) is True and "PUMPEN AN    50.0L/S" in t and "RAUS 50 L" in t and "AUTO AN" in t))
    for _ in range(19 * 60):
        b.tick(lit, kap, auto=True)
    r.append(("trocken: 19 s spaeter noch an (Nachlauf)", b.ioa["on"].get(103) is True))
    for _ in range(2 * 60):
        b.tick(lit, kap, auto=True)
    r.append(("nach 20 s aus", b.ioa["on"].get(103) is False))
    b.tick(lw, kap, auto=False, batt=(0.15, 0.0))
    t = b.texte()
    r.append(("Schalter aus: aus, 'AUTO AUS (SCHALTER)'; Batterie 15 %", b.ioa["on"].get(103) is False
              and "AUTO AUS (SCHALTER)" in t and "BATTERIE  15%" in t))
    # Auto zu schon ab 0,5 %
    c = Anlage()
    lit, kap = hafen()
    c.tick(lit, kap)
    lw = list(lit)
    lw[0] = lw[1] = 0.006 * kap[0]     # Bug 0,6 %
    c.tick(lw, kap)
    r.append(("Bug 0,6 %: alle Schotten zu", not c.tick(lw, kap)))
    lw[0] = lw[1] = 0.003 * kap[0]
    d = Anlage()
    d.tick(lit, kap)
    d.tick(lw, kap)
    r.append(("Bug 0,3 %: Schotten bleiben auf", d.tick(lw, kap)))
    return pruefe(r)


if __name__ == "__main__":
    print("ALLES OK" if test_abteile() else "FEHLER")
