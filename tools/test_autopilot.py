"""Pruefstand fuer den Autopiloten (lua/autopilot.lua, Chip 'Figet Marena Autopilot').
- Schiff: Fahrhebel und Ruder wie die Schiffsfuehrung (schiff.lua: W/S mal 'Hebel Tempo', Hotkey 1 Motoren, Hotkey 2
  Stopp, Ruder = A/D mal 'Ruder max' mit 'Ruder Tempo'); Tempo folgt dem Hebel (30 m/s * Wurzel Hebel, 25 s), Drehrate
  dem Ruder (bis 4,5 Grad/s bei 15 m/s, 3 s); Stroemung dreht das Schiff ein wenig
- der Umschalter im Chip: Autopilot an (Bool 1) -> Achse 1/2 = Zahl 3/4 vom Skript, sonst vom Sitz
- Karte: map.mapToScreen / screenToMap linear ('zoom' km ueber die Bildbreite), Laser: Strahl gegen eine runde Insel
- v1.1: Control Handle (Blick X/Y, Leertaste, W/S, Pfeile, Hotkey 1/2, besetzt), Knopf Anti-Kollision
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from test_lage import lade  # noqa: E402
from test_schiff import pruefe  # noqa: E402
from build_schiff import minify, LUA_DIR, LUA_LIMIT  # noqa: E402
from build_lage import kopf, SCHREIBER_PROPS  # noqa: E402
import build_autopilot as ba  # noqa: E402

PR = {n: v for n, v, _ in ba.PROPS}
PR.update({n: v for n, v, _ in SCHREIBER_PROPS})
PR["Schreiber Port"] = 0
KN = 0.5144
NICK = -2.28 / 360


class Welt:
    def __init__(self, hd=0.0, insel=None, drift=0.0):
        src = minify(open(os.path.join(LUA_DIR, "autopilot.lua"), encoding="utf-8").read())
        self.rt, self.g, self.io = lade(src, PR)
        self.io["w"] = (160, 96)
        g = self.g

        def m2s(cx, cy, z, w, h, wx, wy):
            k = w / (z * 1000.0)
            return w / 2 + (wx - cx) * k, h / 2 - (wy - cy) * k

        def s2m(cx, cy, z, w, h, px, py):
            k = w / (z * 1000.0)
            return cx + (px - w / 2) / k, cy - (py - h / 2) / k
        g.map = self.rt.table(mapToScreen=m2s, screenToMap=s2m)
        g.screen.drawMap = lambda *a: self.io["draw"].append(("map",) + tuple(a))
        self.x = self.y = 0.0
        self.hd, self.v, self.r = hd, 0.0, 0.0
        self.hb, self.on, self.ru, self.k1 = 0.0, False, 0.0, False
        self.insel, self.drift = insel, drift
        self.laser = 0.0
        self.t = 0
        self.min_insel = 1e9
        self.hb_diff = 0.0

    def out(self, i):
        return self.io["on"].get(i, 0.0)

    def tick(self, ad=0.0, ws=0.0, h1=False, h2=False, griff=None, knopf=False, reset=False, ak=False):
        """griff: None = niemand am Griff, sonst dict lx/ly (Blick U), sp (Leertaste), ws, pf (Pfeil), k1/k2 (Hotkeys)"""
        io = self.io
        gr = griff or {}
        io["n"] = {1: ad, 2: ws, 7: self.x, 8: 7.45, 9: self.y, 10: NICK, 11: -self.hd / 360.0, 12: self.v,
                   13: gr.get("lx", 0.0), 14: gr.get("ly", 0.0), 15: self.laser, 16: gr.get("ws", 0.0),
                   17: gr.get("pf", 0.0)}
        io["b"] = {1: h1, 2: h2, 10: gr.get("sp", False), 11: knopf, 12: reset, 13: ak, 14: griff is not None,
                   15: gr.get("k1", False), 16: gr.get("k2", False), 17: gr.get("k3", False), 18: gr.get("k4", False)}
        self.g.onTick()
        ap = bool(self.out(101))
        a1 = self.out(3) if ap else ad
        a2 = self.out(4) if ap else ws
        # Schiffsfuehrung
        if h1 and not self.k1:
            self.on = not self.on
        self.k1 = h1
        self.hb = max(-0.5, min(1.0, self.hb + a2 * 0.25 / 60))
        if h2 or not self.on:
            self.hb = 0.0
        self.ru += max(-1 / 60, min(1 / 60, a1 * 0.5 - self.ru))
        # Bewegung
        vss = 30 * math.sqrt(max(self.hb, 0.0)) if self.on else 0.0
        self.v += (vss - self.v) / (25 * 60)
        rss = self.ru / 0.5 * min(self.v, 15.0) * 0.3 + self.drift
        self.r += (rss - self.r) / (3 * 60)
        self.hd = (self.hd + self.r / 60) % 360
        self.x += self.v * math.sin(math.radians(self.hd)) / 60
        self.y += self.v * math.cos(math.radians(self.hd)) / 60
        # Laser (Pivot vom Skript, Strahl ab dem Bug 25,5 m vor dem Physik-Sensor)
        self.laser = 0.0
        if self.insel:
            cx, cy, rr = self.insel
            lx = self.x + 25.5 * math.sin(math.radians(self.hd))
            ly = self.y + 25.5 * math.cos(math.radians(self.hd))
            b = math.radians(self.hd + self.out(1) * 360)
            dx, dy = math.sin(b), math.cos(b)
            fx, fy = cx - lx, cy - ly
            t = fx * dx + fy * dy
            q = rr * rr - (fx * fx + fy * fy - t * t)
            if t > 0 and q > 0 and t - math.sqrt(q) < 4000:
                self.laser = t - math.sqrt(q)
            self.min_insel = min(self.min_insel, math.hypot(fx, fy) - rr)
        self.t += 1
        return ap

    def draw(self):
        self.io["draw"].clear()
        self.g.onDraw()
        return self.io["draw"]

    def lauf(self, sek, **kw):
        for _ in range(int(sek * 60)):
            self.tick(**kw)

    def km(self):
        return self.v / KN


def fehler(a, b):
    return (a - b + 180) % 360 - 180


def anfahren(hd=0.0, insel=None, drift=0.0, ws_s=3.0):
    """Motoren an, W gedrueckt halten, 60 s fahren lassen."""
    w = Welt(hd, insel, drift)
    w.tick(h1=True)
    w.lauf(ws_s, ws=1.0)
    w.lauf(60)
    return w


def test_autopilot():
    rueck = []
    src = kopf(minify(open(os.path.join(LUA_DIR, "autopilot.lua"), encoding="utf-8").read()), "ap")
    rueck.append(("Skript %d Zeichen (hoechstens %d)" % (len(src), LUA_LIMIT), len(src) <= LUA_LIMIT))

    # aus: Umschalter auf Sitz, Hebel wird mitgerechnet
    w = anfahren()
    rueck.append(("aus: Umschalter aus, Schiff faehrt von Hand %.1f kn" % w.km(), not w.out(101) and w.km() > 15))
    rueck.append(("Hebel mitgerechnet = Hebel der Schiffsfuehrung", abs(w.g.hb - w.hb) < 1e-9))

    # an: Kurs und Tempo halten trotz Stroemung
    w = anfahren(hd=40.0, drift=0.4)
    v0, hd0 = w.v, w.hd
    w.tick(knopf=True)
    w.lauf(90)
    rueck.append(("an: Soll = Kurs/Tempo beim Einschalten, haelt Kurs gegen Stroemung (Fehler %.2f Grad)"
                  % fehler(w.hd, hd0), w.out(101) and abs(fehler(w.hd, hd0)) < 1.5 and abs(w.g.kz - hd0) < 1))
    rueck.append(("haelt Tempo (%.1f kn, Soll %.1f kn)" % (w.km(), v0 / KN), abs(w.v - v0) < 0.5))
    rueck.append(("Hebel mitgerechnet = Hebel der Schiffsfuehrung (an)", abs(w.g.hb - w.hb) < 1e-9))

    # D 3 s: Soll-Kurs +30 Grad; Kurs folgt ohne grosses Ueberschwingen
    w.lauf(3, ad=1.0)
    soll = w.g.kz
    mx = 0.0
    for _ in range(60 * 60):
        w.tick()
        mx = max(mx, fehler(w.hd, soll))
    rueck.append(("D 3 s: Soll-Kurs +%.0f Grad, erreicht (Fehler %.2f), Ueberschwingen %.1f Grad"
                  % (fehler(soll, hd0), fehler(w.hd, soll), mx),
                  abs(fehler(soll, hd0) - 30) < 1 and abs(fehler(w.hd, soll)) < 1.5 and mx < 6))
    # W 2 s: Soll-Tempo +10 kn
    vs = w.g.vz
    w.lauf(2, ws=1.0)
    rueck.append(("W 2 s: Soll-Tempo +%.1f kn" % ((w.g.vz - vs) / KN), abs((w.g.vz - vs) / KN - 10) < 0.2))
    w.lauf(150)
    rueck.append(("Tempo folgt (%.1f kn, Soll %.1f kn)" % (w.km(), w.g.vz / KN), abs(w.v - w.g.vz) < 0.6))
    # Hotkey 2: aus
    w.tick(h2=True)
    rueck.append(("Hotkey 2 (Stopp): Autopilot aus, Hebel 0", not w.out(101) and w.hb == 0 and w.g.hb == 0))

    # Knopf zweimal: aus
    w = anfahren()
    w.tick(knopf=True)
    w.lauf(1)
    w.tick(knopf=True)
    w.lauf(1)
    rueck.append(("Knopf: an, nochmal: aus", not w.out(101)))

    # Griff: Kreuz per Blick, Leertaste setzt / loescht; Karte steht, solange der Griff gehalten wird
    w = anfahren(hd=0.0)
    gx, gy = PR["Blick X U"], PR["Blick Y U"]
    blick = {"lx": gx / 2, "ly": gy / 2}
    w.lauf(0.5, griff=blick)
    m0 = (w.g.MX, w.g.MY)
    rueck.append(("Griff: Kreuz bei Blick halb rechts/oben = (%d, %d)" % (w.g.CX, w.g.CY), (w.g.CX, w.g.CY) == (120, 25)))
    w.lauf(0.1, griff=dict(blick, sp=True))
    w.lauf(0.2, griff=blick)
    wp = [tuple(w.g.W[1].values())] if len(w.g.W) else []
    rueck.append(("Leertaste = Wegpunkt %s (500 m Ost, 287 m Nord der Kartenmitte)" % (wp,),
                  len(wp) == 1 and abs(wp[0][0] - m0[0] - 500) < 1 and abs(wp[0][1] - m0[1] - 287.5) < 1))
    w.lauf(5, griff=blick)
    rueck.append(("Karte steht, solange der Griff gehalten wird (Schiff fuhr %.0f m)" % (w.y - m0[1]),
                  (w.g.MX, w.g.MY) == m0 and w.y - m0[1] > 50))
    w.lauf(0.1, griff=dict(blick, sp=True))
    w.lauf(0.2, griff=blick)
    rueck.append(("Leertaste nochmal an derselben Stelle = Wegpunkt weg", len(w.g.W) == 0))
    w.lauf(0.1, griff=dict(blick, sp=True))
    w.lauf(0.1, griff={"lx": -gx / 4, "ly": -gy / 4})
    w.lauf(0.1, griff={"lx": -gx / 4, "ly": -gy / 4, "sp": True})
    w.lauf(0.1, griff={"lx": -gx / 4, "ly": -gy / 4})
    rueck.append(("zwei Wegpunkte", len(w.g.W) == 2))
    w.lauf(0.1)
    rueck.append(("Griff los: Karte wieder aufs Schiff", abs(w.g.MX - w.x) < 1 and abs(w.g.MY - w.y) < 1))
    # Zoom, Blick-Mitte, Rand schiebt, Hotkey 2
    z0 = w.g.zi
    w.lauf(0.1, griff={"ws": 1.0})
    w.lauf(0.1, griff={})
    z1 = w.g.zi
    w.lauf(0.1, griff={"pf": -1.0})
    w.lauf(0.1, griff={})
    w.lauf(0.1, griff={"pf": -1.0})
    w.lauf(0.1, griff={})
    z2 = w.g.zi
    w.lauf(1.0, griff={"ws": -1.0})
    rueck.append(("Zoom W / Pfeil runter / S gehalten: %d -> %d -> %d -> %d" % (z0, z1, z2, w.g.zi),
                  z1 == z0 - 1 and z2 == z0 + 1 and w.g.zi == min(7, z2 + 3)))
    # Tastatur-Achse steigt langsam: kurzer Tipp erreicht nur 0,3 (rauf und wieder runter) = ein Schritt
    w.lauf(0.1, griff={})
    za = w.g.zi
    for v_ in (0.1, 0.2, 0.3, 0.3, 0.2, 0.15, 0.1, 0.05, 0.0, 0.0):
        w.tick(griff={"ws": v_})
    zb = w.g.zi
    w.lauf(0.1, griff={"k3": True})
    w.lauf(0.1, griff={})
    zc = w.g.zi
    w.lauf(0.1, griff={"k4": True})
    w.lauf(0.1, griff={})
    rueck.append(("kurzer Tipp (Achse bis 0,3) = ein Schritt, Hotkey 3/4: %d -> %d -> %d -> %d" % (za, zb, zc, w.g.zi),
                  zb == za - 1 and zc == zb - 1 and w.g.zi == zc + 1))
    w.lauf(0.1, griff={"lx": 0.02, "ly": -0.01, "k1": True})
    w.lauf(0.1, griff={"lx": 0.02, "ly": -0.01})
    rueck.append(("Hotkey 1: jetziger Blick = Bildmitte (%d, %d)" % (w.g.CX, w.g.CY), (w.g.CX, w.g.CY) == (80, 48)))
    mx0 = w.g.MX
    w.lauf(1.0, griff={"lx": 0.02 + gx * 1.2, "ly": -0.01})
    mx1 = w.g.MX
    w.lauf(1.0, griff={"lx": 0.02 + gx * 2.0, "ly": -0.01})
    rueck.append(("Blick knapp ueber den rechten Rand schiebt die Karte nach Ost (%.0f m), weit weg nicht" % (mx1 - mx0),
                  mx1 - mx0 > 100 and w.g.MX == mx1))
    w.lauf(0.1, griff={"k2": True})
    rueck.append(("Hotkey 2: Karte aufs Schiff", abs(w.g.MX - w.x) < 1 and abs(w.g.MY - w.y) < 1))
    w.g.W[1] = w.rt.table(w.x + 500, w.y + 225)
    w.g.W[2] = w.rt.table(w.x + 1500, w.y + 2500)
    w.g.W[3] = w.rt.table(w.x + 3000, w.y + 2500)
    w.g.zi = 3
    w.tick(knopf=True)
    rueck.append(("an mit Wegpunkten: Route", w.g.md == 1))
    erreicht, nah = [], []
    n0 = len(w.g.W)
    for k in range(60 * 600):
        w.tick()
        if len(w.g.W) < n0:
            erreicht.append((round(w.x), round(w.y)))
            n0 = len(w.g.W)
        if n0 == 0 and w.v < 0.3:
            break
    rueck.append(("alle 3 Wegpunkte erreicht %s" % erreicht, len(erreicht) == 3))
    rueck.append(("am Ziel: Soll-Tempo 0, Schiff steht (%.2f kn), Modus Kurs" % w.km(), w.g.vz == 0 and w.v < 0.3
                  and w.g.md == 0))

    # A/D waehrend Route: Route verlassen, Kurs halten; Reset loescht
    w = anfahren()
    w.g.W[1] = w.rt.table(w.x + 5000, w.y + 5000)
    w.tick(knopf=True)
    w.lauf(1, ad=-1.0)
    rueck.append(("A/D waehrend Route: Modus Kurs", w.g.md == 0 and len(w.g.W) == 1))
    w.tick(reset=True)
    rueck.append(("Reset: Wegpunkte weg", len(w.g.W) == 0))

    # Hindernis: Insel 1,5 km voraus (Radius 300 m), Kurs direkt drauf
    w = anfahren(hd=0.0, insel=(0.0, 2400.0, 300.0), ws_s=4.0)
    rueck.append(("Anti-Kollision beim Laden aus: Laser aus, keine Treffer", not w.out(103) and w.g.ak is False
                  and all(w.g.H[k] is None for k in range(1, 10))))
    w.tick(knopf=True, ak=True)
    rueck.append(("Knopf Anti-Kollision: Laser an", w.out(103)))
    gesehen = gewarnt = 0
    for _ in range(60 * 300):
        w.tick()
        gesehen += any(w.g.H[k] is not None for k in range(1, 10))
        gewarnt += bool(w.g.BL)
    rueck.append(("Insel voraus: Laser sieht sie (%d Ticks), Hindernis (%d Ticks)" % (gesehen, gewarnt),
                  gesehen > 100 and gewarnt > 100))
    rueck.append(("weicht aus: kommt der Insel nie naeher als %.0f m" % w.min_insel, w.min_insel > 60))
    rueck.append(("danach wieder auf Kurs (%.1f Grad), Ausweichen aus" % w.hd, w.g.ao == 0 and abs(fehler(w.hd, 0)) < 5))
    w.insel = None

    # Laser-Treffer liegen auf der Insel
    w = Welt(insel=(0.0, 1000.0, 300.0))
    w.tick(ak=True)
    w.lauf(3)
    ok = True
    n = 0
    for k in range(1, 10):
        h = w.g.H[k]
        if h is not None:
            n += 1
            ok &= abs(math.hypot(h[1], h[2] - 1000.0) - 300) < 10
    rueck.append(("%d Laser-Treffer, alle auf dem Inselrand" % n, n >= 5 and ok))
    # Nickausgleich: Pivot Y
    rueck.append(("Pivot Y gleicht das Nicken aus (%.4f U)" % w.out(2), abs(w.out(2) - (0.3 / 360 - NICK) * PR["Laser Hoehe Richtung"]) < 1e-9))
    w.tick(ak=True)
    w.lauf(0.2)
    rueck.append(("Knopf nochmal: Anti-Kollision aus, Treffer weg", not w.out(103) and all(w.g.H[k] is None for k in range(1, 10))))

    # Zeichnen: Karte, keine Eingaenge
    w = anfahren()
    w.g.W[1] = w.rt.table(w.x + 500, w.y + 500)
    w.tick(knopf=True)
    d = w.draw()
    texte = [e[3] for e in d if e[0] == "t"]
    rueck.append(("onDraw: Karte in der Mitte des Schiffs, Texte %s" % texte, d[0][0] == "map" and abs(d[0][1] - w.x) < 1e-6
                  and "AP ROUTE" in texte and "AK AUS" in texte))
    w.tick(griff={"lx": 0.0, "ly": 0.0})
    d = w.draw()
    texte = [e[3] for e in d if e[0] == "t"]
    rueck.append(("onDraw mit Griff: Kreuz gelb in der Mitte, Entfernung %s" % texte[-2:], any(
        e[0] == "l" and e[1:5] == (75, 48, 79, 48) for e in d) and any(t.startswith("X0.0") for t in texte)))
    return pruefe(rueck)


if __name__ == "__main__":
    print("ALLES OK" if test_autopilot() else "FEHLER")
