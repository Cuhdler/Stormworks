"""Pruefstand fuer den Simulator (sim/swsim.py). Aufruf: python sim/test_sim.py   (braucht lupa)

- test_bausteine: kleiner Test-Chip (mit build_mc.MC gebaut): Takt (1 Tick je Baustein), Formel, Composite lesen/
  schreiben (Luecken bleiben), Umschalter, Puls, Druck-Schalter, Schwelle, Lua (Eigenschaft, onDraw, Absturz)
- test_alle_chips: jeder Chip aus allen Fahrzeugen und aus dem Spiel-Ordner microprocessors laedt und laeuft
- test_schiffsfuehrung: Chip "Figet Marena Schiffsfuehrung" aus der Fahrzeugdatei gegen lua/schiff.lua direkt
  (tools/test_schiff.py): Takt "sofort" Tick fuer Tick gleich; Takt "spiel" gleich, wenn man die Eingaenge um die
  Bausteine bis zum Skript verschiebt (An/Aus 4 Ticks, Zahlen 8 Ticks - abgezaehlt in tools/build_schiff.py)
- test_kleine_chips: Licht, Schotten, Abteile Sammler aus der Fahrzeugdatei gegen ihre lua/-Datei direkt
- test_netz: Kabel der Figet Marena, Anschluss-Lage gegen tools/kabel_flossen.py, verworfene Kabel, sieben Chips
  zusammen (Sitz -> Autopilot -> Schiffsfuehrung -> Pumpen; Wasser -> Sammler -> Abteile -> Schotten -> Tueren)
- test_mehrspieler: Host + Gast (Modell vermutet): gleiche Fuehler -> gleiche Anzeige; Bedrohung fehlt beim Gast ->
  Licht dort nur nach jedem Zwischenstand rot
Nur Chips ohne Waffen werden mit Szenarien geprueft.
"""
import contextlib
import io
import os
import re
import shutil
import sys
import tempfile
import time

HIER = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HIER)
sys.path.insert(0, HIER)
sys.path.insert(0, os.path.join(ROOT, "tools"))
import swsim  # noqa: E402
import fahrzeug  # noqa: E402
from swsim import Chip, composite, SimFehler  # noqa: E402
from lupa.lua53 import LuaRuntime  # noqa: E402
import test_schiff as ts  # noqa: E402  (Motormodell, Schiff-Pruefstand, Lua-Sperren)
from build_schiff import MC, minify, LUA_DIR  # noqa: E402

FZ = "Figet Marena"
MOT = ["L1", "L2", "R1", "R2"]


def pruefe(checks):
    ok = True
    for name, res in checks:
        print("%-60s %s" % (name, "ok" if res else "FEHLER"))
        ok &= bool(res)
    return ok


def nah(a, b, tol=1e-5):
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


def direkt(datei, props, drop_local=False):
    """lua/<datei> wie im Pruefstand der tools/ (eigenes Lua, nicht der Simulator). Rueckgabe (onTick, io)."""
    rt = LuaRuntime(unpack_returned_tuples=True)
    g = rt.globals()
    e = {"n": {}, "b": {}, "on": {}}
    g.input = rt.table(getNumber=lambda i: float(e["n"].get(i, 0.0)), getBool=lambda i: bool(e["b"].get(i, False)))
    g.output = rt.table(setNumber=lambda i, v: e["on"].__setitem__(i, v), setBool=lambda i, v: e["on"].__setitem__(100 + i, v))
    g.property = rt.table(getNumber=lambda s: props[s], getBool=lambda s: bool(props[s]))
    g["async"] = rt.table(httpGet=lambda p, s: None)
    ts.sperren(rt)
    with open(os.path.join(LUA_DIR, datei), encoding="utf-8") as f:
        rt.execute(minify(f.read(), drop_local=drop_local))
    return g.onTick, e


# ---- 1. Bausteine ----------------------------------------------------------------------------------------------------

LUA_TEST = """
z=0
function onTick()
  z=z+1
  output.setNumber(1,input.getNumber(1)*2+property.getNumber('Sieben'))
  output.setBool(1,z>=3)
  if input.getBool(2) then print('weg') end
end
function onDraw() screen.drawText(1,1,'Z'..z) end
"""


def test_chip_xml():
    mc = MC("Test", "Test-Chip fuer den Simulator", 4, 4)
    an = mc.node("An", 1, 0, "", 0, 0, (-8, 0))
    x = mc.node("X", 1, 1, "", 1, 0, (-8, 1))
    y = mc.node("Y", 1, 1, "", 2, 0, (-8, 2))
    absturz = mc.node("Absturz", 1, 0, "", 3, 0, (-8, 3))
    n1 = mc.comp(0, (0, 0), {}, [(an, 0)])
    n2 = mc.comp(0, (1, 0), {}, [(n1, 0)])
    n3 = mc.comp(0, (2, 0), {}, [(n2, 0)])
    mc.node("Kette", 0, 0, "", 0, 1, (8, 0), (n3, 0))
    f = mc.comp(10, (0, 1), {"e": "x*y+z"}, [(x, 0), (y, 0)])
    mc.node("Formel", 0, 1, "", 1, 1, (8, 1), (f, 0))
    sieben = mc.comp(34, (0, 2), {"n": "Sieben"}, extra='<v text="7" value="7"/>')
    c0 = mc.comp(40, (0, 3), {"count": 6}, [("in1", (sieben, 0)), ("in6", (sieben, 0))])
    c1 = mc.comp(40, (1, 3), {"count": 3, "offset": 4}, [("inc", (c0, 0)), ("in1", (x, 0)), ("in3", (y, 0))])
    mc.node("Comp", 0, 5, "", 2, 1, (8, 2), (c1, 0))
    rd = mc.comp(31, (2, 3), {"i": 6}, [(c1, 0)])
    mc.node("Lesen", 0, 1, "", 3, 1, (8, 3), (rd, 0))
    um = mc.comp(22, (0, 4), {}, [(x, 0), (y, 0), (an, 0)])
    mc.node("Umschalter", 0, 1, "", 0, 2, (8, 4), (um, 0))
    pu = mc.comp(48, (0, 5), {}, [(an, 0)])
    mc.node("Puls", 0, 0, "", 1, 2, (8, 5), (pu, 0))
    tg = mc.comp(28, (0, 6), {}, [(an, 0)])
    mc.node("Taster", 0, 0, "", 2, 2, (8, 6), (tg, 0))
    sw = mc.comp(12, (0, 7), {}, [(x, 0)], extra='<min text="2" value="2"/><max text="5" value="5"/>')
    mc.node("Schwelle", 0, 0, "", 3, 2, (8, 7), (sw, 0))
    lw = mc.comp(41, (3, 0), {"count": 2}, [("inc", (c1, 0)), (an, 0), (absturz, 0)])
    lua = mc.comp(56, (4, 0), {"script": LUA_TEST}, [(lw, 0)])
    mc.node("Lua", 0, 5, "", 0, 3, (8, 8), (lua, 0))
    mc.node("Bild", 0, 6, "", 1, 3, (8, 9), (lua, 1))
    return mc.xml()


def test_bausteine():
    text = test_chip_xml()
    d = swsim.chipdef(text)
    r = []

    def kette(**opt):
        c = Chip(d, **opt)
        for _ in range(5):
            c.tick()
        c.setze("An", True)
        for k in range(8):
            c.tick()
            if c.lese("Kette") is False:
                return k, c.verzoegerung("An", "Kette")
        return None, None
    r.append(("Takt spiel: 3x NICHT -> Ausgang 2 Ticks spaeter %s" % (kette(),), kette() == (2, 2)))
    r.append(("Takt sofort: 3x NICHT im selben Tick", kette(takt="sofort") == (0, 0)))
    r.append(("bruecken_takt: Ein- und Ausgang je 1 Tick mehr", kette(bruecken_takt=True) == (4, 4)))
    c = Chip(d)
    c.setze("X", 3.0)
    c.setze("Y", 4.0)
    for _ in range(4):
        c.tick()
    comp = c.lese("Comp")
    r.append(("Formel x*y+z (z offen = 0): 12", c.lese("Formel") == 12.0))
    r.append(("Composite schreiben: Kanal 5/7 neu, 6 bleibt vom Grund (Luecke)", comp.n[:7] == [7, 0, 0, 0, 3, 7, 4]))
    r.append(("Composite lesen i=6 = Kanal 7", c.lese("Lesen") == 4.0))
    r.append(("Zahlen-Umschalter aus = in2", c.lese("Umschalter") == 4.0))
    r.append(("Schwelle 2..5 bei 3: an", c.lese("Schwelle") is True))
    puls, taster, um = [], [], []
    for k in range(12):
        c.setze("An", k in (2, 3, 4, 8, 9))
        c.tick()
        puls.append(c.lese("Puls"))
        taster.append(c.lese("Taster"))
        um.append(c.lese("Umschalter"))
    r.append(("Umschalter an = in1", um[3] == 3.0 and um[6] == 4.0))
    r.append(("Puls: je Einschalten genau ein Tick an", [k for k, v in enumerate(puls) if v] == [2, 8]))
    r.append(("Druck-Schalter: schaltet bei jedem Einschalten um", taster == [False] * 2 + [True] * 6 + [False] * 4))
    c.setze("X", 0.1)
    c.tick()
    c.tick()
    r.append(("32-Bit-Zahlen wie im Spiel (0.1 -> %.10f)" % c.lese("Formel"), c.lese("Formel") != 0.4 and nah(c.lese("Formel"), 0.4, 1e-7)))
    lua = c.lese("Lua")
    texte = swsim.texte(c.lese("Bild"))
    r.append(("Lua: Eingang*2 + Eigenschaft 'Sieben' (7*2+7), Zaehler", lua.n[0] == 21.0 and lua.b[0] is True))
    r.append(("Lua onDraw: Text %s" % texte, texte == ["Z%d" % c.ticks]))
    c.setze("Absturz", True)
    for _ in range(3):
        c.tick()
    f = c.fehler()
    r.append(("print() fehlt wie im Spiel: Skript stoppt, Fehler gemeldet", len(f) == 1 and "print" in f[0]))
    try:
        Chip(swsim.chipdef(text.replace('<c type="48">', '<c type="99">')))
        meldung = ""
    except SimFehler as e:
        meldung = str(e)
    r.append(("unbekannter Baustein: klare Meldung", "Baustein-Typ 99" in meldung and "Test" in meldung))
    from ausdruck import zahl_formel as zf, logik_formel as lf
    r.append(("Formeln: ^ % atan2 len clamp min mit 3 Werten", zf("-x^2", 1)(3) == -9 and zf("(1-x)%1*360", 1)(0.25) == 270
              and nah(zf("atan2(a-x,b-y)/pi2", 8)(0, 0, 0, 0, 1, 1, 0, 0), 0.125) and zf("len(a-x,b-y)", 8)(0, 0, 0, 0, 3, 4, 0, 0) == 5
              and zf("clamp(x,-z,z)", 3)(5, 0, 2) == 2 and zf("min(x,y,z)", 3)(3, 1, 2) == 1))
    r.append(("An/Aus-Formel ((y&z)|w)&a und x&(!y)", lf("((y&z)|w)&a", 8)(0, 1, 1, 0, 1, 0, 0, 0) and lf("x&(!y)", 4)(1, 0, 0, 0)))
    return pruefe(r)


# ---- 2. alle Chips laden ---------------------------------------------------------------------------------------------

def test_alle_chips():
    t0 = time.time()
    chips, fehler, lua_fehler, typen = 0, [], 0, set()
    dateien = swsim.chip_dateien() + sorted(f for f in os.listdir(swsim.FAHRZEUGE) if f.endswith(".xml"))
    for f in dateien:
        pfad = f if os.path.isabs(f) else os.path.join(swsim.FAHRZEUGE, f)
        s = open(pfad, encoding="utf-8", errors="replace", newline="").read()
        for m in re.finditer(r"<microprocessor(?:_definition)?\b.*?</microprocessor(?:_definition)?>", s, re.S):
            try:
                c = Chip(swsim.chipdef(m.group(0)))
                for _ in range(10):
                    c.tick()
                chips += 1
                typen |= set(c.cdef.typen())
                lua_fehler += len(c.fehler())
            except Exception as e:                          # noqa: BLE001 - jeder Fehler zaehlt hier
                fehler.append("%s: %s" % (os.path.basename(pfad), e))
    for f in fehler[:5]:
        print("   ", f)
    print("   %d Chips, Baustein-Typen %s, %d Skripte stoppen ohne Eingaenge (Lua-Fehler), %.1f s" % (
        chips, " ".join(map(str, sorted(typen))), lua_fehler, time.time() - t0))
    return pruefe([("alle %d Chips (Fahrzeuge + microprocessors) laden und laufen 10 Ticks" % chips, chips > 100 and not fehler),
                   ("jeder vorkommende Baustein-Typ ist bekannt", typen <= set(swsim.TYPEN))])


# ---- 3. Schiffsfuehrung ----------------------------------------------------------------------------------------------

def _schiff_def():
    return swsim.chip_aus_fahrzeug(FZ, "Figet Marena Schiffsfuehrung").cdef


class SimSchiff:
    """Wie tools/test_schiff.Schiff, aber der Chip aus der Fahrzeugdatei rechnet (alle Bausteine und 3 Skripte)."""
    TAKT, F32 = "sofort", False

    def __init__(self, motoren):
        self.chip = Chip(_schiff_def(), takt=self.TAKT, float32=self.F32)
        self.mo, self.mess, self.out = motoren, [(0.0, 0.0, 0.0, 0.0)] * 4, {}

    def setze(self, ad=0.0, ws=0.0, bug=0.0, h1=False, h2=False, h4=False, tempo=8.0, kurs=0.25):
        c = self.chip
        c.setze("Sitz", composite({1: ad, 2: ws, 3: bug}, {1: h1, 2: h2, 4: h4, 32: True}))
        c.setze("Physik-Sensor", composite({13: tempo, 17: kurs}))
        for i, n in enumerate(MOT):
            c.setze("Motor %s RPS" % n, self.mess[i][0])
            c.setze("Motor %s Zylinder" % n, composite({3: self.mess[i][1], 1: self.mess[i][2], 2: self.mess[i][3]}))

    def tick(self, ad=0.0, ws=0.0, bug=0.0, h1=False, h2=False, last=1.0, h4=False):
        self.setze(ad, ws, bug, h1, h2, h4)
        a = self.chip.tick()
        self.mess = [mo.schritt(a["Luft %s" % n], a["Treibstoff %s" % n], a["Kupplung %s" % n], a["Anlasser %s" % n], last)
                     for mo, n in zip(self.mo, MOT)]
        o = self.innen()
        o["rps"] = [mo.rps for mo in self.mo]
        o["aussen"] = a
        self.out = o
        return o

    def innen(self):
        """Ausgang des Skripts schiff.lua im Chip als dict wie im Pruefstand (Zahl k, An/Aus 100+k)."""
        blk = self.chip.lua[1]
        o = {k + 1: v for k, v in enumerate(blk.aus_n)}
        o.update({101 + k: v for k, v in enumerate(blk.aus_b)})
        return o

    def helm(self):
        return swsim.texte(self.chip.lese("Helm"), 288, 160)


def _aussen_soll(o):
    """Ausgaenge des Chips, wie sie aus dem Skript-Ausgang o entstehen (build_schiff.py)."""
    s = {}
    for i, n in enumerate(MOT):
        s["Luft %s" % n], s["Treibstoff %s" % n], s["Kupplung %s" % n] = o[3 * i + 1], o[3 * i + 2], o[3 * i + 3]
        s["Anlasser %s" % n] = o[102 + i]
    s.update({"Ruder": o[13], "Bugstrahlruder": o[14], "Motor L an": o[101], "Motor R an": o[101], "Rueckwaerts L": o[106],
              "Rueckwaerts R": o[107], "Getriebe A": o[109], "Getriebe B": o[110], "Getriebe C": o[111]})
    return s


def _andre_pruefungen(takt):
    """tools/test_schiff.py test_motor + test_system, aber mit dem Chip aus der Fahrzeugdatei. -> (ok, gesamt, Fehlzeilen)"""
    SimSchiff.TAKT, SimSchiff.F32 = takt, takt == "spiel"
    alt = ts.Schiff
    ts.Schiff = SimSchiff
    puffer = io.StringIO()
    try:
        with contextlib.redirect_stdout(puffer):
            ts.test_motor()
            ts.test_system()
    finally:
        ts.Schiff = alt
    zeilen = [z for z in puffer.getvalue().splitlines() if z.rstrip().endswith((" ok", " FEHLER"))]
    return sum(z.rstrip().endswith(" ok") for z in zeilen), len(zeilen), [z.rstrip() for z in zeilen if z.rstrip().endswith("FEHLER")]


def test_schiffsfuehrung():
    r = []
    chip_eig = Chip(_schiff_def(), float32=False).eigenschaften["zahl"]
    anders = {k for k, v in chip_eig.items() if ts.PR.get(k) != v}
    r.append(("Eigenschaften im Fahrzeug = build_schiff.py (%d)" % len(chip_eig), not anders))
    ts.PR.update(chip_eig)
    # (a) Takt sofort, 32-Bit aus, mit Motormodell: Tick fuer Tick gleich (test_motor-Ablauf, 95 s)
    mo_r = [ts.Motor(), ts.Motor(fehlt=True), ts.Motor(fehlt=True), ts.Motor(fehlt=True)]
    mo_s = [ts.Motor(), ts.Motor(fehlt=True), ts.Motor(fehlt=True), ts.Motor(fehlt=True)]
    ref, sim = ts.Schiff(mo_r), SimSchiff(mo_s)
    abw = 0
    for k in range(60 * 95):
        sek = k / 60
        mo_r[0].tmp = mo_s[0].tmp = 105.0 if 45 <= sek < 60 else 60.0
        ws = 1.0 if 20 <= sek < 24 else (-1.0 if 35 <= sek < 37 else (1.0 if 62 <= sek < 64 else 0.0))
        last = 0.0 if 62 <= sek < 75 else 1.0
        h1 = (1 <= sek < 1.05) or (85 <= sek < 85.05)
        o = ref.tick(ws=ws, h1=h1, last=last)
        s = sim.tick(ws=ws, h1=h1, last=last)
        soll = _aussen_soll(o)
        abw += sum(s["aussen"][k2] != v for k2, v in soll.items())
        abw += sum(s[c] != o.get(c, 0.0) for c in range(1, 33))
    r.append(("Takt sofort, 5700 Ticks mit Motormodell: Chip = schiff.lua (%d Abweichungen)" % abw, abw == 0))
    r.append(("   Helm-Anzeige gleich: %s" % sim.helm(), sim.helm() == ref.helm()))
    ok, n, fz = _andre_pruefungen("sofort")
    r.append(("Takt sofort: tools/test_schiff.py motor+system mit dem Chip %d/%d ok" % (ok, n), ok == n and n >= 20))

    # (b) Takt spiel: offene Schleife (keine Motoren). Das Skript sieht An/Aus vom Sitz 4 Ticks, Zahlen 8 Ticks spaeter
    # (Bausteine davor, abgezaehlt in build_schiff.py); Wellen-Skript 1 Tick davor. Bezug: dieselben Skripte direkt.
    SimSchiff.TAKT, SimSchiff.F32 = "spiel", False
    sim = SimSchiff([ts.Motor(fehlt=True)] * 4)
    pr = dict(ts.PR)
    w_tick, w_io = direkt("wellen.lua", pr)
    s_tick, s_io = direkt("schiff.lua", pr, drop_local=True)
    ein = []
    abw_i = abw_a = 0
    wl, lauf_o = {}, None
    for k in range(60 * 70):
        sek = k / 60
        ad = -1.0 if 30 <= sek < 32 else 0.0
        ws = 1.0 if 10 <= sek < 14 else (-1.0 if 40 <= sek < 46 else 0.0)
        e = dict(ad=ad, ws=ws, bug=1.0 if 33 <= sek < 34 else 0.0, h1=1 <= sek < 1.05, h2=60 <= sek < 60.05, h4=False)
        ein.append(e)
        sim.setze(**e)
        a = sim.chip.tick()

        def alt(d):
            return ein[k - d] if k >= d else None

        def comp(zn, ab):
            n = {i: 0.0 for i in range(1, 33)}
            b = {i: False for i in range(1, 33)}
            if zn:
                n.update({1: zn["ad"], 2: zn["ws"], 3: zn["bug"], 5: 8.0, 6: 0.25})
            if ab:
                b.update({1: ab["h1"], 2: ab["h2"], 4: ab["h4"], 8: True})
            return n, b
        # Wellen-Skript sieht Zahlen 6, An/Aus 2 Ticks alt; sein Gas-Abzug kommt 4, die Schaltsperre 3 Ticks spaeter an
        w_io["n"], w_io["b"] = comp(alt(6), alt(2))
        w_io["on"].clear()
        w_tick()
        wl[k] = (w_io["on"].get(1, 0.0), bool(w_io["on"].get(101, False)))
        n, b = comp(alt(8), alt(4))
        n[24], b[9] = wl.get(k - 4, (0.0, False))[0], wl.get(k - 3, (0.0, False))[1]
        s_io["n"], s_io["b"] = n, b
        s_io["on"].clear()
        s_tick()
        o = {c: s_io["on"].get(c, 0.0) for c in range(1, 33)}
        o.update({100 + c: bool(s_io["on"].get(100 + c, False)) for c in range(1, 33)})
        innen = sim.innen()
        abw_i += sum(innen[c] != o[c] for c in o)
        if lauf_o is not None:
            soll = _aussen_soll(lauf_o)
            abw_a += sum(a[k2] != v for k2, v in soll.items())
        lauf_o = o
    r.append(("Takt spiel, 4200 Ticks: Skript im Chip = schiff.lua mit 4/8 Ticks Versatz (%d)" % abw_i, abw_i == 0))
    r.append(("   Chip-Ausgaenge 1 Tick nach dem Skript (Composite lesen) (%d)" % abw_a, abw_a == 0))
    # (c) Verzoegerung Hotkey 1 -> Pumpen an: gemessen gegen die Zahl der Bausteine
    c = Chip(_schiff_def())
    c.setze("Sitz", composite(None, {32: True}))
    for _ in range(10):
        c.tick()
    c.setze("Sitz", composite(None, {1: True, 32: True}))
    gemessen = None
    for k in range(20):
        c.tick()
        if gemessen is None and c.lese("Motor L an"):
            gemessen = k
        c.setze("Sitz", composite(None, {32: True}))
    v = c.verzoegerung("Sitz", "Motor L an")
    r.append(("Hotkey 1 -> 'Motor L an' nach %s Ticks (6 Bausteine: %s)" % (gemessen, v), gemessen == v == 5))
    ok, n, fz = _andre_pruefungen("spiel")
    erg = pruefe(r)
    print("   Info: Takt spiel mit Motormodell: %d von %d Pruefungen aus tools/test_schiff.py ok; abweichend:" % (ok, n))
    for z in fz:
        print("      " + z.rsplit(" ", 1)[0].rstrip())
    return erg


# ---- 4. kleine Chips -------------------------------------------------------------------------------------------------

def _vergleich(name, datei, eingaben, zu_lua, aus_lua, ticks):
    """Chip 'name' aus der Fahrzeugdatei (Takt spiel, 32 Bit) gegen lua/<datei> direkt.
    eingaben(t) -> {Eingang: Wert}; zu_lua(eingaben) -> (Zahlen, An/Aus) wie das Skript sie sieht;
    aus_lua: {Ausgang: Funktion(Skript-Ausgang) -> erwarteter Wert}. Rueckgabe (Abweichungen, Verzoegerungen)."""
    c = swsim.chip_aus_fahrzeug(FZ, name)
    lt, lio = direkt(datei, c.eigenschaften["zahl"])
    erste = list(eingaben(0))[0]
    vz = {a: c.verzoegerung(erste, a) for a in aus_lua}
    sim, ref = [], []
    vorher = None
    for t in range(ticks):
        e = eingaben(t)
        for k, v in e.items():
            c.setze(k, v)
        sim.append(c.tick())
        lio["n"], lio["b"] = zu_lua(vorher) if vorher else ({}, {})     # das Skript sieht den Eingang 1 Tick spaeter
        lt()
        ref.append(dict(lio["on"]))
        vorher = e
    abw = 0
    for a, f in aus_lua.items():
        d = vz[a] - 1
        for t in range(1, ticks - d):
            ist, soll = sim[t + d][a], f(ref[t])
            if isinstance(soll, dict):                      # Composite: {Kanal: Zahl oder An/Aus}
                gleich = all(nah(ist.n[k - 1], v) if isinstance(v, float) else ist.b[k - 1] == v for k, v in soll.items())
            else:
                gleich = nah(ist, soll) if isinstance(soll, float) else ist == soll
            abw += not gleich
    return abw, vz


def test_kleine_chips():
    r = []
    # Licht: Uhr + Bedrohung (Lage-Composite Bool 25)
    def licht_ein(t):
        return {"Uhr": ((t // 30) % 24) / 24.0, "Lage": composite(None, {25: 400 <= t < 410})}
    abw, vz = _vergleich("Figet Marena Licht", "licht.lua", licht_ein,
                         lambda e: ({1: e["Uhr"]}, {25: e["Lage"].b[24]}),
                         {"Licht": lambda o: {i: float(o.get(i, 0.0)) for i in range(1, 7)},
                          "Licht Steuerraum": lambda o: {i - 3: float(o.get(i, 0.0)) for i in (4, 5, 6)}}, 1200)
    r.append(("Licht: Chip = licht.lua, Ausgaenge %s Ticks spaeter (%d)" % (vz, abw), abw == 0 and vz == {"Licht": 1, "Licht Steuerraum": 3}))
    c = swsim.chip_aus_fahrzeug(FZ, "Figet Marena Licht")
    c.setze("Uhr", 0.5)
    for _ in range(5):
        c.tick()
    r.append(("   Mittag: Farbe 1/0.92/0.8 %s" % ["%.3f" % v for v in c.lese("Licht").n[:3]],
              all(nah(a, b) for a, b in zip(c.lese("Licht").n[:3], (1, 0.92, 0.8)))))
    # Schotten: Alle auf + 5 Kippschalter
    def schotten_ein(t):
        e = {"Alle auf": t < 100 or 200 <= t < 300}
        e.update({"Knopf Wand %d" % (k + 1): (t // (37 + 11 * k)) % 2 == 1 for k in range(5)})
        return e
    abw, vz = _vergleich("Figet Marena Schotten", "schotten.lua", schotten_ein,
                         lambda e: ({}, {1 + k: v for k, v in enumerate([e["Alle auf"]] + [e["Knopf Wand %d" % (k + 1)] for k in range(5)])}),
                         dict({"Tueren Wand %d" % (k + 1): (lambda o, k=k: bool(o.get(101 + k))) for k in range(5)},
                              Zustand=lambda o: {1 + k: bool(o.get(101 + k)) for k in range(5)}), 600)
    r.append(("Schotten: Chip = schotten.lua (Tueren %d, Zustand %d Ticks spaeter) (%d)" % (vz["Tueren Wand 1"], vz["Zustand"], abw),
              abw == 0 and vz["Tueren Wand 1"] == 2 and vz["Zustand"] == 1))
    # Abteile Sammler: 9 Liquid Meter (Fuellstand, Kapazitaet)
    def sammler_ein(t):
        e = {"Fuellstand %d" % (10 + k): (t * (k + 1) * 0.37) % 900 for k in range(9)}
        e.update({"Kapazitaet %d" % (10 + k): 1000.0 if k != 4 else 50.0 for k in range(9)})
        return e
    abw, vz = _vergleich("Figet Marena Abteile Sammler", "abteile_sammler.lua", sammler_ein,
                         lambda e: (dict([(1 + k, e["Fuellstand %d" % (10 + k)]) for k in range(9)] +
                                         [(10 + k, e["Kapazitaet %d" % (10 + k)]) for k in range(9)]), {}),
                         {"Abteile": lambda o: {i: float(o.get(i, 0.0)) for i in list(range(1, 10)) + [32]}}, 300)
    r.append(("Abteile Sammler: Chip = abteile_sammler.lua (%d)" % abw, abw == 0 and vz == {"Abteile": 1}))
    return pruefe(r)


# ---- 5. Fahrzeug-Netz ------------------------------------------------------------------------------------------------

NETZ_CHIPS = ["Figet Marena Autopilot", "Figet Marena Schiffsfuehrung", "Figet Marena Flossen", "Figet Marena Abteile Sammler",
              "Figet Marena Abteile", "Figet Marena Schotten", "Figet Marena Licht"]
TUEREN = [(-4, -12, 3), (4, -12, 3), (-10, 5, -13), (10, 5, -13), (-11, -12, -15), (11, -12, -15), (-5, -12, -29),
          (5, -12, -29), (-9, -12, -53), (9, -12, -53)]


def wasser_szenario(wasser_ab=300, h1=30):
    """Sitz: Hotkey 1 bei Tick h1; alle Liquid Meter dicht (1000 L) und leer; ab 'wasser_ab' 50 L Wasser im Abteil
    SEITE BB (Sensor 13, ueber den Sammler); Uhr Mittag."""
    def sz(fz, t):
        if t == 0:
            for tl in [t2 for t2 in fz.daten.teile if t2.d == "water_measure"]:
                g = swsim.TeilGriff(fz, tl)
                g.setze("Fluid Capacity", 1000.0)
                g.setze("Liquid Level", 0.0)
            fz.teil(d="clock").setze("Time", 0.5)
        fz.teil(d="seat_compact", pos=(0, 17, -10)).setze("Seat data", composite(None, {1: h1 <= t < h1 + 3}))
        if t == wasser_ab:
            fz.teil(d="water_measure", pos=(-18, -15, -40)).setze("Liquid Level", 50.0)
    return sz


def _spiel_knoten(d):
    """Anschluesse (Label, Position im Teil) direkt aus den Spieldaten rom/data/definitions/<d>.xml."""
    pfad = os.path.join(fahrzeug.SPIEL_DEF, d + ".xml")
    if not os.path.exists(pfad):
        return []
    txt = open(pfad, encoding="utf-8", errors="replace").read()
    out = []
    for m in re.finditer(r'<logic_node [^>]*?label="([^"]*)"[^>]*>(.*?)</logic_node>', txt, re.S):
        p = re.search(r"<position([^/]*)/>", m.group(2))
        out.append((m.group(1), fahrzeug.xyz(p.group(1) if p else "")))
    return out


def _lage_vergleich(d):
    sys.path.append(os.path.join(ROOT, "landkreuzer", "tools"))
    import fz as lk
    meine = {}
    for an in d.anschluesse:
        t = d.teile[an.teil]
        meine.setdefault((t.d, t.vp, an.label), set()).add(an.welt)
    spiel = {}
    gleich = anders = 0
    for _, teile in lk.Fahrzeug.lesen(d.pfad).koerper:
        for t in teile:
            if t.d == "microprocessor":
                knoten = [(lab, w) for lab, _, _, w in lk.chip_knoten(t)]
            else:
                if t.d not in spiel:
                    spiel[t.d] = _spiel_knoten(t.d)
                knoten = [(lab, t.lokal_zu_welt(p)) for lab, p in spiel[t.d]]
            for lab, w in knoten:
                if w in meine.get((t.d, t.vp, lab), ()):
                    gleich += 1
                else:
                    anders += 1
    return gleich, anders


def test_netz():
    r = []
    t0 = time.time()
    swsim.FahrzeugDaten._cache.clear()
    d = swsim.FahrzeugDaten.lesen(FZ)
    t_datei = time.time() - t0
    r.append(("Figet Marena: alle %d Kabel treffen einen Anschluss (verworfen %d)" % (len(d.kabel), len(d.verworfen)),
              len(d.kabel) > 500 and not d.verworfen and not d.mehrdeutig))
    # Anschluss-Lage gegen landkreuzer/tools/fz.py (eigener Leser der Datei) mit den Spieldaten (rom/data/definitions)
    gleich, anders = _lage_vergleich(d)
    r.append(("Anschluss-Lage wie landkreuzer/tools/fz.py + Spieldaten (%d gleich, %d anders)" % (gleich, anders),
              gleich > 2000 and anders == 0))
    s = open(d.pfad, encoding="utf-8", newline="").read()
    # verworfenes Kabel erkennen: Kopie der Datei mit einem Kabel ins Leere (nur in einem Temp-Ordner)
    tmp = tempfile.mkdtemp(prefix="swsim_")
    try:
        p = os.path.join(tmp, "Probe.xml")
        k = '<logic_node_link type="1"><voxel_pos_0 x="99" y="99" z="99"/><voxel_pos_1 y="-12" z="-41"/></logic_node_link>'
        with open(p, "w", encoding="utf-8", newline="") as f:
            f.write(s.replace("</logic_node_links>", k + "</logic_node_links>"))
        v = swsim.FahrzeugDaten.lesen(p).verworfen
        r.append(("Kabel ins Leere wird gemeldet (wie das Spiel es verwirft)", len(v) == 1 and v[0].a == (99, 99, 99)))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    for name in ("KI Landkreuzer", "small Jet"):
        try:
            v = swsim.FahrzeugDaten.lesen(name).verworfen
            print("   Info: %s: %d Kabel verworfen %s" % (name, len(v), "; ".join(d.kabel_text(k) for k in v)))
        except SimFehler as e:
            print("   Info:", e)
    # sieben Chips zusammen
    t0 = time.time()
    fz = swsim.Fahrzeug(FZ, chips=NETZ_CHIPS)
    t_lade = time.time() - t0
    pumpe = fz.teil(d="water_pump", pos=(-11, -19, -85))
    an_bei, zu_bei, offen = None, None, False
    t0 = time.time()
    sz = wasser_szenario()
    for t in range(600):
        fz.tick(1, sz)
        if an_bei is None and pumpe.lese("On/Off"):
            an_bei = t
        tueren = [fz.teil(d="door", pos=p).lese("Open/Close") for p in TUEREN]
        if t == 299:
            offen = all(tueren)
        if zu_bei is None and t >= 300 and not any(tueren):
            zu_bei = t
    t_lauf = time.time() - t0
    ap, sf = fz.chip("Figet Marena Autopilot"), fz.chip("Figet Marena Schiffsfuehrung")
    soll = 30 + ap.verzoegerung("Sitz", "Sitz aus") + 1 + sf.verzoegerung("Sitz", "Motor L an")
    r.append(("Sitz H1 -> Autopilot -> Schiffsfuehrung -> Pumpe an: Tick %s (Bausteine+Kabel: %d)" % (an_bei, soll), an_bei == soll))
    r.append(("Schotten-Tueren beim Laden auf (Abteile -> Schotten -> 10 Tueren)", offen))
    r.append(("Wasser SEITE BB: Sammler -> Abteile -> Schotten -> Tueren zu nach %s Ticks" % (zu_bei - 300 if zu_bei else None),
              zu_bei is not None and zu_bei - 300 <= 15))
    lampe = fz.teil(d="small_light_rgb", pos=(-17, 1, 0)).lese("Color Data")
    r.append(("Licht: Lampe bekommt Mittags-Farbe", all(nah(a, b) for a, b in zip(lampe.n[:3], (1, 0.92, 0.8)))))
    bild = fz.teil(d="monitor_9", pos=(8, 21, -23)).texte("Video Signal", 288, 160)
    r.append(("Abteil-Monitor zeichnet (%d Texte, z. B. %s)" % (len(bild), bild[:3]), any("SEITE" in z for z in bild)))
    fehl = [z for z in fz.bericht() if z.startswith("FEHLER")]
    for z in fehl:
        print("   ", z)
    r.append(("keine Lua-Fehler in den 7 Chips", not fehl))
    print("   Info: Datei lesen %.2f s, 7 Chips anlegen %.2f s, 600 Ticks mit Szenario %.2f s (%.0f Ticks/s)" % (
        t_datei, t_lade, t_lauf, 600 / t_lauf))
    # Takt sofort: dieselbe Kette im selben Tick
    fz = swsim.Fahrzeug(FZ, chips=NETZ_CHIPS[:2], takt="sofort")
    pumpe = fz.teil(d="water_pump", pos=(-11, -19, -85))
    sz = wasser_szenario()
    an_sofort = None
    for t in range(60):
        fz.tick(1, sz)
        if an_sofort is None and pumpe.lese("On/Off"):
            an_sofort = t
    r.append(("Takt sofort: Sitz H1 -> Pumpe an im selben Tick (%s)" % an_sofort, an_sofort == 30))
    # HTTP: Fahrtenschreiber im Helm-Skript (Log Port 8766) - Anfragen mitschreiben, Antwort im naechsten Tick
    fz = swsim.Fahrzeug(FZ, chips=["Figet Marena Schiffsfuehrung"], http_antwort=lambda port, text: "ok")
    fz.tick(120)
    log = fz.http_log
    ohne = swsim.Fahrzeug(FZ, chips=["Figet Marena Schiffsfuehrung"])
    ohne.tick(120)
    r.append(("HTTP: %d Anfragen an Port 8766 beantwortet (ohne Antwort: %d, wartet)" % (len(log), len(ohne.http_log)),
              len(log) >= 20 and all(e[2] == 8766 and e[3].startswith("/l?d=") and e[4] == "ok" for e in log)
              and len(ohne.http_log) == 1))
    t0 = time.time()
    ganz = swsim.Fahrzeug(FZ)
    print("   Info: ganzes Fahrzeug (%d Chips) laden %.2f s" % (len(ganz.laufend), time.time() - t0))
    r.append(("ganzes Fahrzeug mit allen Chips laedt", len(ganz.laufend) == len(d.chips())))
    return pruefe(r)


# ---- 6. Mehrspieler --------------------------------------------------------------------------------------------------

def test_mehrspieler():
    r = []
    # (a) gleiche Fuehler: Gast zeigt dasselbe (Fahrt 09.10.: Abteile-Monitor beim Mitspieler richtig)
    mp = swsim.Mehrspieler(FZ, chips=["Figet Marena Abteile Sammler", "Figet Marena Abteile", "Figet Marena Schotten"],
                           abgleich_ticks=120)
    gleich = True
    sz = wasser_szenario()
    for t in range(600):
        mp.tick(1, sz)
        for p in TUEREN[:2]:
            gleich &= mp.host.teil(d="door", pos=p).lese("Open/Close") == mp.gast.teil(d="door", pos=p).lese("Open/Close")
    bh = mp.host.teil(d="monitor_9", pos=(8, 21, -23)).texte("Video Signal", 288, 160)
    bg = mp.gast.teil(d="monitor_9", pos=(8, 21, -23)).texte("Video Signal", 288, 160)
    r.append(("gleiche Fuehler: Tueren bei Host und Gast jeden Tick gleich", gleich))
    r.append(("gleiche Fuehler: Abteil-Monitor beim Gast wie beim Host", bh == bg and len(bh) > 3))

    # (b) Bedrohung (Lage-Chip, nicht simuliert) kommt beim Gast nicht an: Licht Steuerraum nur nach Zwischenstand rot
    def bedrohung(fz, t):
        if t == 0:
            fz.teil(d="clock").setze("Time", 0.5)
        fz.teil(name="Figet Marena Lage").setze("Lage", composite(None, {25: t >= 60}))

    def rot_anteil(n):
        mp = swsim.Mehrspieler(FZ, chips=["Figet Marena Licht"], abgleich_ticks=n, gast_fuehler={"Figet Marena Lage": "fehlt"})
        h = g = 0
        for t in range(3600):
            mp.tick(1, bedrohung)
            if t >= 600:
                h += mp.host.teil(d="small_light_rgb", pos=(4, 25, -25)).lese("Color Data").n[1] == 0.0
                g += mp.gast.teil(d="small_light_rgb", pos=(4, 25, -25)).lese("Color Data").n[1] == 0.0
        return h / 3000, g / 3000
    erg = {n: rot_anteil(n) for n in (0, 120, 600)}
    print("   Info: Anteil 'rot' Steuerraum (Host, Gast) je Zwischenstand-Abstand: %s" % {n: ("%.2f" % h, "%.2f" % g) for n, (h, g) in erg.items()})
    r.append(("Host: Bedrohung -> Steuerraum immer rot", all(h == 1.0 for h, _ in erg.values())))
    r.append(("Gast ohne Abgleich: nie rot (Lua-Zustand nicht geteilt)", erg[0][1] == 0.0))
    r.append(("Gast, Zwischenstand alle 120 Ticks: rot haelt 5 s -> immer rot", erg[120][1] == 1.0))
    r.append(("Gast, alle 600 Ticks: nur etwa die Haelfte rot (%.2f)" % erg[600][1], 0.4 <= erg[600][1] <= 0.6))
    return pruefe(r)


if __name__ == "__main__":
    ok = True
    for f in (test_bausteine, test_alle_chips, test_schiffsfuehrung, test_kleine_chips, test_netz, test_mehrspieler):
        print("== %s" % f.__name__)
        ok &= f()
    print("ALLES OK" if ok else "FEHLER")
