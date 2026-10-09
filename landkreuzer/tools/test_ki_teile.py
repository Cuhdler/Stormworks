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
    rt.execute("input={} output={} property={} screen={} async={}")
    g["async"].httpGet = lambda port, url: io.setdefault("http", []).append((port, url))
    def kanal(i):
        assert 1 <= int(i) <= 32 and int(i) == i, "Composite-Kanal %r gibt es nicht (nur 1-32)" % (i,)
        return int(i)
    g.input.getNumber = lambda i: float(io["n"].get(kanal(i), 0.0))
    g.input.getBool = lambda i: bool(io["b"].get(kanal(i), False))
    g.output.setNumber = lambda i, v: io["on"].__setitem__(kanal(i), v)
    g.output.setBool = lambda i, v: io["on"].__setitem__(100 + kanal(i), v)
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
    # Start-Verzoegerung: vorher weder KI noch Waffen frei, danach beides (Schalter aus = KI darf)
    sv, wv = int(pr["Start Verzoegerung s"] * 60), int(pr["Waffen Verzoegerung s"] * 60)
    o = [tick(g, io, {1: 100.0, 3: 200.0}) for _ in range(sv - 1)]
    rueck.append(("vor %d s: KI aus, Waffen aus" % (sv // 60), not o[-1].get(101) and not o[-1].get(110)))
    o = [tick(g, io, {1: 100.0, 3: 200.0}) for _ in range(wv - sv)]
    rueck.append(("nach %d s: KI an, Waffen noch aus (bis %d s)" % (sv // 60, wv // 60), o[1].get(101) and not o[-1].get(110)))
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
    o = tick(g, io, {1: 100.0, 3: 200.0, 28: 50.0, 29: 50.0, 30: 2000.0, 31: 0.0}, {7: True, 8: True})
    rueck.append(("Schutzzone: Flak-Ziel 70 m vom Startpunkt -> Waffen schweigen (%s), Anzeige (%s), Chaff erlaubt (%s)"
                  % (o.get(110), o.get(111), o.get(112)), o.get(110) is False and o.get(111) is True and o.get(112) is True))
    o = tick(g, io, {1: 100.0, 3: 200.0, 30: 2000.0, 31: 0.0}, {8: True})
    rueck.append(("Schutzzone: nur Flak-R-Ziel 2 km weg -> Waffen frei (%s)" % o.get(110), o.get(110) is True))
    # Freund-Punkt der Karte bei Ost 2100 / Nord 200 (Zahl 4/5, Zahl 12 = 1): dasselbe Ziel -> Waffen schweigen
    o = tick(g, io, {1: 100.0, 3: 200.0, 30: 2000.0, 31: 0.0, 4: 2100.0, 5: 200.0, 12: 1.0}, {8: True})
    rueck.append(("Freund-Punkt der Karte: Ziel dort -> Waffen schweigen (%s)" % o.get(110), o.get(110) is False))
    o = tick(g, io, {1: 900.0, 3: 200.0, 21: -700.0, 22: 100.0, 23: 50.0}, {5: True})
    rueck.append(("Schutzzone: Panzer 800 m weg, BC-Ziel bei der Basis -> kein Schuss, KI faehrt nicht hin (%s/%s)"
                  % (o.get(110), o.get(104)), o.get(110) is False and not o.get(104)))
    o = tick(g, io, {1: 100.0, 3: 200.0, 21: 300.0, 22: 400.0, 23: 50.0}, {5: True})
    rueck.append(("nur BC-Ziel: dieses", o.get(104) and abs(o[20] - 400) < 1e-6 and abs(o[21] - 600) < 1e-6))
    o = tick(g, io, {1: 100.0, 3: 200.0})
    rueck.append(("kein Ziel: ungueltig, kein Auto-Chaff (%s)" % o.get(112), not o.get(104) and o.get(112) is False))
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
    # rueckwaerts: rechtsherum drehen = Achsen nach links einschlagen
    for _ in range(300):
        o = tick(g, io, {28: -3.0, 29: 1.0, 30: -0.5, 32: 2.0})
    rueck.append(("rueckwaerts rechtsherum: vorn %.3f (links eingeschlagen)" % o[1], o[1] < -0.1 and o[2] > 0.1))
    # auf der Stelle drehen (Soll-Tempo 0, Fahrbefehl vom Halte-Regler leicht negativ): wie vorwaerts einschlagen
    for _ in range(300):
        o = tick(g, io, {28: 0.0, 29: 1.0, 30: -0.08, 32: 0.3})
    rueck.append(("auf der Stelle rechtsherum (Fahrbefehl -0,08): vorn %.3f (rechts eingeschlagen)" % o[1],
                  o[1] > 0.1 and o[2] < -0.1))
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
            tick(g, io, {1: 1.0, 6: -0.01, 26: float(z), 27: 2.0, 29: 1.0, 9: 25.0, 16: 0.5, 30: 0.5, 31: -0.5, 32: 6.0},
                 {1: True, 10: True, 13: True})
            io["draw"] = []
            g.onDraw()
            ok &= len(io["draw"]) > 3
        texte = " | ".join(str(d[3]) for d in io["draw"] if d[0] == "drawText")
        # Tempo (Zahl 32) muss ankommen; Roll -0,01 U mit 'Roll Richtung' -1 = 3,6 Grad rechts tief -> R+4
        ok &= ("V 6.0/" in texte or "V 6/" in texte) and (w > 100 or "R+4" in texte and "L!" in texte)
        rueck.append(("Status zeichnet auf %dx%d (Tempo, Roll, umgelernt): %s" % (w, h, texte[:50]), ok))
    return rueck


def test_status_batterie():
    """Restzeit: Batterie faellt 1 % je Minute -> bei 87 % etwa 87 Minuten."""
    g, io = lade("ki_status", {n: v for n, v, _ in build_ki.props()})
    io["w"], io["h"] = 64, 96
    b = 0.9
    for _ in range(3 * 3600):
        b -= 0.01 / 3600
        tick(g, io, {1: 1.0, 16: b, 26: 2.0, 32: 5.0}, {1: True})
    io["draw"] = []
    g.onDraw()
    t = [d[3] for d in io["draw"] if d[0] == "drawText" and "BAT" in str(d[3])]
    return [("Batterie-Restzeit (1 %%/min, %.0f %%): %s" % (b * 100, t), t and t[0].endswith(" %dM" % round(b / 0.01)))]


def test_status_schreiber():
    """Schreiber im Status-Skript: mit Port 8768 gehen Pakete an den waffen_logger (Messstelle 'ki', je Zeile Tick + 28
    Werte); mit Port 0 nichts."""
    rueck = []
    for port in (0, 8768):
        pr = {n: v for n, v, _ in build_ki.props()}
        pr["Schreiber Port"] = port
        g, io = lade("ki_status", pr)
        for _ in range(100):
            tick(g, io, {1: 10.0, 3: 20.0, 26: 2.0, 32: 5.0, 9: 30.0}, {1: True})
        http = io.get("http", [])
        if port == 0:
            rueck.append(("Schreiber aus (Port 0): %d Pakete" % len(http), not http))
        else:
            import urllib.parse
            q = urllib.parse.parse_qs(urllib.parse.urlparse(http[0][1]).query) if http else {}
            zeile = q.get("d", [""])[0].split(";")[0].split(",")
            rueck.append(("Schreiber an: %d Pakete an Port %s, Messstelle %s, %d Werte je Zeile" % (
                len(http), http[0][0] if http else "-", q.get("q"), len(zeile) - 1),
                http and http[0][0] == 8768 and q.get("q") == ["ki"] and len(zeile) - 1 == 28))
    return rueck


def test_status_vorzeichen():
    """Vorzeichen aus der Spur (Status zeigt rot K / N / D!): Kreis rechtsherum am Hang, 20 s; einmal alles richtig,
    einmal Kompass gespiegelt, Nick umgedreht und Lenkbefehl falsch herum."""
    import math
    rueck = []
    pr = {n: v for n, v, _ in build_ki.props()}
    for falsch in (False, True):
        g, io = lade("ki_status", pr)
        io["w"], io["h"] = 64, 96
        x = z = 0.0
        for t in range(1200):
            kurs = (t / 60 * 6) % 360                 # 6 Grad/s rechtsherum, 8 m/s, Gelaende steigt nach Norden (10 %)
            x += 8 / 60 * math.sin(math.radians(kurs))
            z += 8 / 60 * math.cos(math.radians(kurs))
            steig = 0.1 * math.cos(math.radians(kurs))                       # Steigung in Fahrtrichtung
            kom = -kurs / 360 * (-1 if falsch else 1)                       # 'Kompass Richtung' -1: Kurs = -Kompass
            nick = math.degrees(math.atan(steig)) / 360 * (-1 if falsch else 1) * pr["Nick Richtung"]
            tick(g, io, {1: x, 2: 40 + 0.1 * z, 3: z, 4: kom, 5: nick, 26: 2.0, 30: -0.5 if falsch else 0.5, 31: 0.6,
                         32: 8.0}, {1: True})
        io["draw"] = []
        g.onDraw()
        farbe, rot = None, set()
        for d in io["draw"]:
            if d[0] == "setColor":
                farbe = d[1:4]
            elif d[0] == "drawText" and farbe == (255, 60, 60) and str(d[3]):
                rot.add(str(d[3])[:1] if str(d[3])[:1] in "NK" else str(d[3]))
        soll = {"N", "K", "D!"} if falsch else set()
        io["w"], io["h"] = 288, 160
        io["draw"] = []
        g.onDraw()
        helm = " ".join(str(d[3]) for d in io["draw"] if d[0] == "drawText")
        rueck.append(("Helm-Zeile (%s): %s" % ("falsch" if falsch else "richtig", helm[-20:]),
                      ("K! N! D!" in helm) == falsch and ("!" in helm) == falsch))
        rueck.append(("Vorzeichen im Status (%s): rot %s" % ("alles falsch" if falsch else "alles richtig",
                                                          sorted(rot) or "nichts"), rot == soll))
    return rueck


def main():
    ok = True
    for t in (test_kleber, test_lenkung, test_status, test_status_batterie, test_status_schreiber,
              test_status_vorzeichen):
        for txt, g in t():
            print("%-75s %s" % (txt, "ok" if g else "FEHLER"))
            ok &= bool(g)
    print("ALLES OK" if ok else "FEHLER")
    return ok


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
