"""Pruefstand fuer die kleinen Skripte im KI-Chip: ki_kleber.lua (Schalter, Start-Verzoegerung, Ziel) und
ki_lenkung.lua (Lenkwinkel der Lenk-Variante), ki_status.lua (zeichnet ohne Fehler).
Aufruf (mit lupa): python landkreuzer/tools/test_ki_teile.py
"""
import os
import sys

from lupa import lua53

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
import build_mc  # noqa: E402
import build_ki  # noqa: E402

LUA = os.path.join(os.path.dirname(HIER), "lua")


def lade(name, props):
    rt = lua53.LuaRuntime(unpack_returned_tuples=True)
    g = rt.globals()
    io = {"n": {}, "b": {}, "on": {}, "draw": []}
    rt.execute("input={} output={} property={} screen={}")
    g.input.getNumber = lambda i: float(io["n"].get(i, 0.0))
    g.input.getBool = lambda i: bool(io["b"].get(i, False))
    g.output.setNumber = lambda i, v: io["on"].__setitem__(i, v)
    g.output.setBool = lambda i, v: io["on"].__setitem__(100 + i, v)
    g.property.getNumber = lambda s: props[s]
    for f in ("setColor", "drawClear", "drawText", "drawRectF", "drawLine", "drawRect"):
        setattr(g.screen, f, (lambda n: (lambda *a: io["draw"].append((n,) + tuple(a))))(f))
    g.screen.getWidth = lambda: io.get("w", 64)
    g.screen.getHeight = lambda: io.get("h", 96)
    src = build_mc.minify(open(os.path.join(LUA, name + ".lua"), encoding="utf-8").read())
    assert len(src) <= 8192, (name, len(src))
    for verboten in ("select(", "pcall(", "print(", "setmetatable(", "unpack(", '"'):
        assert verboten not in src.replace("table.unpack(", ""), (name, verboten)
    rt.execute(src)
    return g, io


def tick(g, io, n=None, b=None):
    io["n"], io["b"], io["on"] = n or {}, b or {}, {}
    g.onTick()
    return dict(io["on"])


def test_kleber():
    pr = {n: v for n, v, _ in build_ki.PROPS_KLEBER}
    g, io = lade("ki_kleber", pr)
    rueck = []
    # Start-Verzoegerung 10 s: vorher weder KI noch Waffen frei, danach beides (Schalter aus = KI darf)
    o = [tick(g, io, {1: 100.0, 3: 200.0}) for _ in range(599)]
    rueck.append(("vor 10 s: KI aus, Waffen aus", not o[-1].get(101) and not o[-1].get(110)))
    o = [tick(g, io, {1: 100.0, 3: 200.0}) for _ in range(3000)]
    rueck.append(("nach 10 s: KI an, Waffen noch aus (bis 60 s)", o[1].get(101) and not o[-1].get(110)))
    o = [tick(g, io, {1: 100.0, 3: 200.0}) for _ in range(2)]
    rueck.append(("nach 60 s: Waffen frei", o[-1].get(101) and o[-1].get(110)))
    o = tick(g, io, {1: 100.0, 3: 200.0}, {1: True, 3: True})
    rueck.append(("Schalter 'Waffen sperren' und 'KI Pause' an: beides aus", not o.get(101) and not o.get(110)))
    o = tick(g, io, {1: 100.0, 3: 200.0}, {4: True})
    rueck.append(("'Nach Hause' wird durchgereicht", o.get(106) is True))
    # Ziel: BC-Ziel 900 m Ost / 1200 m Nord (1500 m), AC-Ziel -360/480 (600 m): das naehere (AC), in Weltkoordinaten
    o = tick(g, io, {1: 100.0, 3: 200.0, 21: 900.0, 22: 1200.0, 23: 50.0, 24: -360.0, 25: 480.0, 26: 30.0},
             {5: True, 6: True})
    rueck.append(("Ziel = naeheres (AC), Welt %.0f/%.0f, Hoehe %.0f" % (o.get(20, 0), o.get(21, 0), o.get(22, 0)),
                  o.get(104) and abs(o[20] + 260) < 1e-6 and abs(o[21] - 680) < 1e-6 and abs(o[22] - 30) < 1e-6))
    # Schutzzone 300 m um den Startpunkt (100/200): Flak-L-Ziel 50/50 daneben -> kein Master Arm, Bool 11
    o = tick(g, io, {1: 100.0, 3: 200.0, 28: 50.0, 29: 50.0, 30: 60.0, 31: 2000.0, 32: 0.0}, {7: True, 8: True})
    rueck.append(("Schutzzone: Flak-Ziel 70 m vom Startpunkt -> Waffen schweigen (%s), Anzeige (%s)"
                  % (o.get(110), o.get(111)), o.get(110) is False and o.get(111) is True))
    o = tick(g, io, {1: 100.0, 3: 200.0, 31: 2000.0, 32: 0.0}, {8: True})
    rueck.append(("Schutzzone: nur Flak-R-Ziel 2 km weg -> Waffen frei (%s)" % o.get(110), o.get(110) is True))
    o = tick(g, io, {1: 900.0, 3: 200.0, 21: -700.0, 22: 100.0, 23: 50.0}, {5: True})
    rueck.append(("Schutzzone: Panzer 800 m weg, BC-Ziel bei der Basis -> kein Schuss, KI faehrt nicht hin (%s/%s)"
                  % (o.get(110), o.get(104)), o.get(110) is False and not o.get(104)))
    o = tick(g, io, {1: 100.0, 3: 200.0, 21: 300.0, 22: 400.0, 23: 50.0}, {5: True})
    rueck.append(("nur BC-Ziel: dieses", o.get(104) and abs(o[20] - 400) < 1e-6 and abs(o[21] - 600) < 1e-6))
    o = tick(g, io, {1: 100.0, 3: 200.0})
    rueck.append(("kein Ziel: ungueltig", not o.get(104)))
    hb = pr["Heim Batterie"]
    o = tick(g, io, {1: 100.0, 3: 200.0, 27: hb - 0.05})
    o2 = tick(g, io, {1: 100.0, 3: 200.0, 27: hb + 0.05})
    o3 = tick(g, io, {1: 100.0, 3: 200.0, 27: hb + 0.15})
    o4 = tick(g, io, {1: 100.0, 3: 200.0, 27: 0.0})
    rueck.append(("Batterie %.0f %%: nach Hause (%s), %.0f %%: bleibt (%s), %.0f %%: wieder normal (%s), 0 = unbekannt (%s)"
                  % (100 * hb - 5, o.get(106), 100 * hb + 5, o2.get(106), 100 * hb + 15, o3.get(106), o4.get(106)),
                  o.get(106) is True and o2.get(106) is True and o3.get(106) is False and o4.get(106) is False))
    return rueck


def test_lenkung():
    pr = {n: v for n, v, _ in build_ki.PROPS_LENKUNG}
    g, io = lade("ki_lenkung", pr)
    rueck = []
    # voller Rechts-Befehl im Stand: nach 2 s 25 Grad = 0,278 (Signal 1 = 90 Grad), hinten gegenlaeufig
    for _ in range(120):
        o = tick(g, io, {29: 1.0, 30: 0.5, 32: 2.0})
    rueck.append(("rechts, langsam: vorn %.3f, hinten %.3f (25 Grad = 0,278)" % (o[1], o[2]),
                  abs(o[1] - 25 / 90) < 1e-3 and abs(o[2] + 25 / 90) < 1e-3))
    # schwenkt hoechstens 30 Grad/s: nach 0,5 s von +25 auf -25 Grad erst bei +10
    for _ in range(30):
        o = tick(g, io, {29: -1.0, 30: 0.5, 32: 2.0})
    rueck.append(("Schwenk-Tempo 30 Grad/s: nach 0,5 s %.1f Grad" % (o[1] * 90), abs(o[1] * 90 - 10) < 0.6))
    # schnell (20 m/s): halber Winkel
    for _ in range(300):
        o = tick(g, io, {29: 1.0, 30: 1.0, 32: 20.0})
    rueck.append(("rechts bei 20 m/s: %.1f Grad (halb)" % (o[1] * 90), abs(o[1] * 90 - 12.5) < 0.2))
    return rueck


def test_status():
    rueck = []
    g, io = lade("ki_status", {n: v for n, v, _ in build_ki.props()})
    for w, h in ((64, 96), (288, 160)):
        io["w"], io["h"] = w, h
        ok = True
        for z in range(10):
            tick(g, io, {1: 1.0, 26: float(z), 27: 2.0, 29: 1.0, 9: 25.0, 16: 0.5, 30: 0.5, 31: -0.5, 32: 6.0}, {1: True, 10: True})
            io["draw"] = []
            g.onDraw()
            ok &= len(io["draw"]) > 3
        rueck.append(("Status zeichnet auf %dx%d" % (w, h), ok))
    return rueck


def main():
    ok = True
    for t in (test_kleber, test_lenkung, test_status):
        for txt, g in t():
            print("%-75s %s" % (txt, "ok" if g else "FEHLER"))
            ok &= bool(g)
    print("ALLES OK" if ok else "FEHLER")
    return ok


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
