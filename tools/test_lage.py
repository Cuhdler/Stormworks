"""Pruefstand fuer die Lagezentrale v2 der Figet Marena (lua/mastradar.lua x 6, lua/lage.lua, lua/bild.lua,
lua/waffenwahl.lua), Lua 5.3. Eingaenge nur in onTick (wie im Spiel: sonst 'draw error 202').
- Schiff faehrt (Tempo, Kurs), schaukelt (Nick/Roll); Physik-Sensor wie im Spiel (Kompass gegen den Uhrzeigersinn)
- 6 Radar (Phalanx) am Mast im manuellen Modus (Lage wie im Fahrzeug, Radar 6 gespiegelt): Schirm folgt dem Gimbal mit
  hoechstens 0,2865 U/s, Strahl 'fov' U breit/hoch; meldet jeden 2. Tick, was im Strahl ist (hoechstens 7 Plaetze, die
  naechsten; Winkel ab Sockel oder - strahl=True - ab Strahl, Hoehe gegen das Deck, mit Rauschen). behalten=True: ein
  gemeldetes Ziel bleibt danach in der Liste stehen (alte Werte, 'Zeit seit Meldung' waechst).
- Radar 2-6 bekommen ihre Lock-Richtung vom letzten Tick der Lagezentrale (wie im Chip, build_lage.py)
"""
import math
import os
import random
import sys

from lupa import LuaRuntime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_lage  # noqa: E402
from build_schiff import minify, LUA_DIR  # noqa: E402
from test_schiff import pruefe, sperren  # noqa: E402

PR = {n: v for n, v, _ in build_lage.PROPS}
PR.update({n: v for n, v, _ in build_lage.SCHREIBER_PROPS})
PR["Schreiber Port"] = 0            # Schreiber aus (nur test_schreiber schaltet ihn ein)


def lade(src, props, http=None):
    rt = LuaRuntime(unpack_returned_tuples=True)
    g = rt.globals()
    offen = []

    def get(p, b):
        offen.append((p, b))
        if http:
            http(p, b)
    g["async"] = rt.table(httpGet=get)
    io = {"n": {}, "b": {}, "on": {}, "draw": [], "tick": False}

    def nur_tick(f):
        def g2(i):
            if not io["tick"]:
                raise RuntimeError("202: attempting to use input function outside onTick")
            return f(i)
        return g2
    g.input = rt.table(getNumber=nur_tick(lambda i: float(io["n"].get(i, 0.0))),
                       getBool=nur_tick(lambda i: bool(io["b"].get(i, False))))
    g.output = rt.table(setNumber=lambda i, v: io["on"].__setitem__(i, v), setBool=lambda i, v: io["on"].__setitem__(100 + i, v))
    g.property = rt.table(getNumber=lambda s: props[s], getBool=lambda s: bool(props[s]))

    def zeichen(name):
        return lambda *a: io["draw"].append((name,) + tuple(a))
    g.screen = rt.table(setColor=zeichen("c"), drawText=zeichen("t"), drawLine=zeichen("l"), drawRect=zeichen("r"),
                        drawRectF=zeichen("rf"), drawTriangleF=zeichen("tf"), drawCircle=zeichen("ci"),
                        drawCircleF=zeichen("ci"), drawClear=zeichen("clr"), getWidth=lambda: io.get("w", (288, 160))[0],
                        getHeight=lambda: io.get("w", (288, 160))[1])
    sperren(rt)
    rt.execute(src)
    if g.onTick:
        ot = g.onTick

        def tick():
            while offen:
                p, b = offen.pop()
                if g.httpReply:
                    g.httpReply(p, b, "ok")
            io["tick"] = True
            try:
                ot()
            finally:
                io["tick"] = False
        g.onTick = tick
    return rt, g, io


def quelle(name):
    with open(os.path.join(LUA_DIR, name + ".lua"), encoding="utf-8") as f:
        return minify(f.read())


class Lage:
    """6 Mast-Radare + LAGE + BILD + WAFFENWAHL wie im Chip; ziele = [[Ort Welt (Ost, Nord, Hoch) m, Tempo m/s], ...]"""

    def __init__(self, ziele, own=(0.0, 12.0, 0.0), hdg=30.0, roll=4.0, nick=2.0, fov=float(build_lage.FOV), behalten=False,
                 props=None, seed=1, rauschen=1.0, strahl=False, weit=8000, hrausch=1.0, blind=None, frisch=False):
        self.rnd = random.Random(seed)
        pr = dict(PR)
        pr.update(props or {})
        src = quelle("mastradar")
        self.http = []                      # Schreiber-Pakete (Tick, Anfrage)
        hp = lambda p, b: self.http.append((self.t, b))
        self.ms = [lade(build_lage.mastradar(src, k), pr, hp) for k in range(6)]
        _, self.g, self.io = lade(build_lage.kopf(quelle("lage"), "la"), pr, hp)
        _, self.bg, self.bio = lade(build_lage.kopf(build_lage.bild_flak(quelle("bild")), "ba"), pr, hp)
        ww = quelle("waffenwahl").replace("UM='0'", "UM='%s'" % ",".join(str(v) for v in [0, 0] + [18] * 78 + [12, 8, 4] + [0] * 13))
        _, self.wg, self.wio = lade(ww, pr)
        self.wio["w"] = (96, 64)
        self.ziele = [[list(p), list(v)] for p, v in ziele]
        self.own, self.hdg, self.roll, self.nick, self.fov = own, hdg, roll, nick, fov
        self.S = [0.0, 0.0, 2.0]
        self.dish = [[0.0, 0.0] for _ in range(6)]
        self.liste = [dict() for _ in range(6)]
        self.behalten, self.rauschen, self.strahl = behalten, rauschen, strahl
        self.weit, self.hrausch = weit, hrausch
        self.blind = blind or {}           # Radar-Index -> (Richtung ab Bug U, halbe Breite U): sieht dort nichts (Mast)
        # frisch=True: die Liste zeigt die frischesten 7 statt der naechsten (Andres Hafen-Log 04.10.: das Such-Radar
        # meldete das Boot in 780 m bei jeder Runde, obwohl ueber 10 Dinge naeher waren)
        self.frisch = frisch
        self.t = 0
        self.h5 = False
        self.btouch = False                 # Bildschirm v3.5: Monitor 9x5 beruehrt
        self.wtouch = None                  # Touch auf dem Waffenwahl-Monitor 2x3
        self.wout = {}
        self.ma = True                      # Master Arm (Flip Switch am Instrument Panel)
        self.leer = False                   # Leertaste
        self.sitz = True                    # jemand im Sitz
        self.flakz = {21: 2e5 + 1200, 22: 2e5 + 900}   # Flak L/R gepackt (Zustand*100000+Entfernung): beide 'Ziel'
        self.bed = {}
        self.aus = {}

    def schritt(self):
        t = self.t
        self.t += 1
        rl = self.roll * math.sin(2 * math.pi * t / 420) / 360
        nk = self.nick * math.sin(2 * math.pi * t / 300) / 360
        h = self.hdg / 360
        self.S = [self.S[i] + self.own[i] / 60 for i in range(3)]
        for z in self.ziele:
            z[0] = [z[0][i] + z[1][i] / 60 for i in range(3)]
        ln, lb = {}, {}
        for k in range(6):
            pos, _, _, rs = build_lage.RADARE[k]
            _, g, io = self.ms[k]
            ox, oy, oz = pos[0] * .25, (pos[1] - 27) * .25, (pos[2] + 38) * .25
            ch, sh = math.cos(h * 2 * math.pi), math.sin(h * 2 * math.pi)
            rp = [self.S[0] + ox * ch + oz * sh, self.S[1] - ox * sh + oz * ch, self.S[2] + oy]
            gy, gp = io["on"].get(1, 0.0), io["on"].get(2, 0.0)
            d = self.dish[k]
            smax = 0.2865 / 60
            dd = ((gy - d[0] + 0.5) % 1) - 0.5
            d[0] = ((d[0] + max(-smax, min(smax, dd)) + 0.5) % 1) - 0.5
            d[1] += max(-smax, min(smax, max(-0.125, min(0.125, gp)) - d[1]))
            n, b, neu = {}, {}, {}
            for i, (o, _) in enumerate(self.ziele):
                rel = [o[j] - rp[j] for j in range(3)]
                R = math.sqrt(sum(c * c for c in rel))
                yaw = math.atan2(rel[0], rel[1]) / (2 * math.pi)
                elw = math.asin(rel[2] / R) / (2 * math.pi)
                az = ((yaw - h + 0.5) % 1) - 0.5
                th = az * 2 * math.pi
                el = elw - (nk * math.cos(th) - rl * math.sin(th))
                azr = az * rs
                bl = self.blind.get(k)
                if bl and abs(((az - bl[0] + 0.5) % 1) - 0.5) < bl[1]:
                    continue
                if (t % 2 == 0 and abs(((azr - d[0] + 0.5) % 1) - 0.5) < self.fov / 2
                        and abs(el - d[1]) < self.fov / 2 and R < self.weit):
                    q = self.rauschen
                    if self.strahl:
                        azr, el = ((azr - d[0] + 0.5) % 1) - 0.5, el - d[1]
                    neu[i] = (R * (1 + self.rnd.uniform(-1, 1) * 0.002 * q),
                              azr + self.rnd.uniform(-1, 1) * 0.0003 * q, el + self.rnd.uniform(-1, 1) * 0.0003 * q * self.hrausch)
            L = self.liste[k]
            for i in list(L):
                L[i][3] += 1
                if L[i][3] > 120 or not self.behalten:
                    del L[i]
            for i, v in neu.items():
                L[i] = list(v) + [0]
            wahl = (lambda q: (q[1][3], q[1][0])) if self.frisch else (lambda q: q[1][0])
            for slot, (i, v) in enumerate(sorted(sorted(L.items(), key=wahl)[:7])):
                s = slot + 1
                n[4 * s - 3], n[4 * s - 2], n[4 * s - 1], n[4 * s] = v
                b[s] = True
            # Lagezentrale vom letzten Tick: 'ab Strahl'/'ab Sockel', Lock-Richtung fuer Radar 2-6
            b[9], b[10] = bool(self.aus.get(128)), bool(self.aus.get(129))
            if k > 0:
                n[29], n[30] = self.aus.get(19 + 2 * k, 0.0), self.aus.get(20 + 2 * k, 0.0)
                b[11] = bool(self.aus.get(110 + k))
            io["n"], io["b"] = n, b
            io["on"].clear()
            g.onTick()
            o = io["on"]
            ln[3 * k + 1], ln[3 * k + 2], ln[3 * k + 3] = o.get(3, 0.0), o.get(4, 0.0), o.get(5, 0.0)
            lb[k + 1] = bool(o.get(101, False))
            lb[8 + k], lb[14 + k] = bool(o.get(102, False)), bool(o.get(103, False))
        ln.update({19: self.S[0], 20: self.S[1], 21: self.S[2], 22: -h, 23: nk, 24: -rl})
        self.io["n"], self.io["b"] = ln, lb
        self.io["on"].clear()
        self.g.onTick()
        self.aus = dict(self.io["on"])
        # Bildschirm v2: Lage-Ausgang, ueberschrieben 21/22 Flak gepackt, 23 Waffenwahl; Bool 26 Master Arm (ueber die
        # Waffenwahl, vom letzten Tick), 28 H5, 30 Leertaste, 31 Sitz besetzt
        bn = {i: self.aus.get(i, 0.0) for i in range(1, 33)}
        bb = {i: bool(self.aus.get(100 + i, False)) for i in range(1, 33)}
        bn.update({21: self.flakz[21], 22: self.flakz[22], 23: self.wout.get(1, 0)})
        bb[26], bb[28], bb[30], bb[31] = bool(self.wout.get(101)), self.h5, self.leer, self.sitz
        bb[32] = self.btouch
        self.bio["n"], self.bio["b"] = bn, bb
        self.bio["on"].clear()
        self.bg.onTick()
        self.bed = dict(self.bio["on"])
        if t % 10 == 0:
            self.bio["draw"].clear()
            self.bg.onDraw()
        # Waffenwahl: Bedienung + Touch 2x3 + Master Arm (Instrument Panel, Schalter 1)
        wn = {i: self.bed.get(i, 0.0) for i in range(1, 33)}
        wb = {i: bool(self.bed.get(100 + i, False)) for i in range(1, 33)}
        wn.update({26: self.wtouch[0] if self.wtouch else 0, 27: self.wtouch[1] if self.wtouch else 0})
        wb[13], wb[14] = self.wtouch is not None, self.ma
        self.wio["n"], self.wio["b"] = wn, wb
        self.wio["on"].clear()
        self.wg.onTick()
        self.wout = dict(self.wio["on"])
        if t % 10 == 5:
            self.wio["draw"].clear()
            self.wg.onDraw()

    def laufe(self, sek):
        for _ in range(int(sek * 60)):
            self.schritt()

    def ziele_aus(self):
        """Lage-Ausgang -> {Platz k: (E, N, U, Tempo, Luft, Kennung, Radar haelt)}"""
        o, out = self.aus, {}
        for k in range(1, 6):
            if o.get(100 + k):
                pk = o[3 * k]
                out[k] = (o[3 * k - 2], o[3 * k - 1], pk % 20000 - 100, (pk // 20000) * 2, bool(o.get(105 + k)),
                          o.get(15 + k), bool(o.get(110 + k)))
        return out

    def zuordnung(self, tol=150):
        """echtes Ziel i -> Liste der Plaetze, die naeher als tol dran sind"""
        tr = self.ziele_aus()
        z = {}
        for i, (p, _) in enumerate(self.ziele):
            rel = [p[0] - self.S[0], p[1] - self.S[1], p[2]]
            z[i] = [k for k, v in tr.items() if math.dist(rel, v[:3]) < tol]
        return z, tr


def drueck(L, was, ticks=2):
    setattr(L, was, True)
    for _ in range(ticks):
        L.schritt()
    setattr(L, was, False)
    L.laufe(0.2)


def waehle(L, w):
    """Waffe w ueber H5 waehlen (0 = keine)."""
    while L.bed.get(2, 0) != w:
        drueck(L, "h5")


def test_verfolgen(behalten, strahl=False):
    ziele = [((-2500, 1500, 300), (150, 0, 0)),        # Flugzeug quer
             ((1200, 900, 60), (0, 0, 0)),             # Hubschrauber schwebt
             ((3000, -2500, 2), (-6, 8, 0)),           # Schiff
             ((-1800, -2600, 3), (4, 3, 0))]           # Schiff 2
    L = Lage(ziele, behalten=behalten, strahl=strahl)
    L.laufe(25)
    z, tr = L.zuordnung()
    ids = {i: [tr[k][5] for k in v] for i, v in z.items()}
    fehler = []
    for _ in range(4):
        L.laufe(5)
        z2, tr2 = L.zuordnung()
        for i in z2:
            if [tr2[k][5] for k in z2[i]] != ids[i]:
                fehler.append((i, ids[i], z2[i]))
    z, tr = L.zuordnung(tol=60)
    print("  Plaetze:", {k: tuple(round(c) for c in v[:4]) + v[4:5] + (v[6],) for k, v in tr.items()})
    print("  Zuordnung (60 m):", z, " Kennung gewechselt:", fehler)
    tempo = {i: tr[z[i][0]][3] for i in z if z[i]}
    echt = {i: math.dist(v, (0, 0, 0)) for i, (_, v) in enumerate(L.ziele)}
    print("  Tempo Platz / echt:", {i: (tempo.get(i), round(echt[i])) for i in echt})
    return [
        ("jedes Ziel genau ein Platz, naeher als 60 m (behalten=%s, ab Strahl=%s)" % (behalten, strahl),
         all(len(v) == 1 for v in z.values())),
        ("keine weiteren Plaetze, jeder von seinem Radar gehalten", len(tr) == len(ziele) and all(v[6] for v in tr.values())),
        ("Luftziele auf Platz 1-2, Schiffe auf 3-4", all(z[i] and z[i][0] in (1, 2) for i in (0, 1))
         and all(z[i] and z[i][0] in (3, 4) for i in (2, 3))),
        ("Kennungen bleiben 20 s gleich", not fehler),
        ("Flugzeug, Hubschrauber = Luft, Schiffe = See",
         [tr[z[i][0]][4] for i in range(4)] == [True, True, False, False] if all(z.values()) else False),
        ("Tempo Flugzeug 150 +- 20 m/s", abs(tempo.get(0, 0) - 150) < 20),
        ("Tempo Schiff 10 +- 6 m/s", abs(tempo.get(2, 0) - 10) < 6),
    ]


def test_plaetze():
    """Andres Fall: viele Schiffe nah, Hubschrauber daneben - die Hubschrauber muessen trotzdem gehalten werden
    (Platz 1-2 Luft, 3-4 See, 5 bleibt frei). Ein naeherer Heli verdraengt den ferneren; ein tiefer schneller Flieger
    (sieht zuerst wie ein Schiff aus) landet auf einem Luft-Platz und die zwei naechsten Schiffe bleiben."""
    ziele = [((r * math.sin(b), r * math.cos(b), 2), (0, 0, 0)) for r, b in
             ((700, 0.3), (900, 1.6), (1100, 2.9), (1300, 4.2), (1500, 5.4))]
    ziele += [((2000 * math.sin(1.0), 2000 * math.cos(1.0), 80), (0, 0, 0)),
              ((2500 * math.sin(3.6), 2500 * math.cos(3.6), 120), (0, 0, 0))]
    L = Lage(ziele, own=(0, 0, 0), behalten=True)
    L.laufe(30)
    z, tr = L.zuordnung(tol=80)
    platz = {i: (v[0] if v else None) for i, v in z.items()}
    print("  5 Schiffe + 2 Helis: Platz je Ziel", platz)
    ok1 = platz[5] in (1, 2) and platz[6] in (1, 2) and {platz[0], platz[1]} == {3, 4} and 5 not in tr
    # naeherer Heli (1 km) -> verdraengt den in 2,5 km
    L.ziele.append([[1000 * math.sin(5.0), 1000 * math.cos(5.0), 100], [0, 0, 0]])
    L.laufe(15)
    z2, _ = L.zuordnung(tol=80)
    gehalten2 = sorted(i for i, v in z2.items() if v)
    # tiefer schneller Flieger (20 m hoch, 70 m/s) in 1,3 km
    L.ziele.append([[1300 * math.sin(2.2), 1300 * math.cos(2.2), 20], [70 * math.cos(2.2), -70 * math.sin(2.2), 0]])
    L.laufe(20)
    z3, tr3 = L.zuordnung(tol=120)
    gehalten3 = sorted(i for i, v in z3.items() if v)
    print("  + Heli in 1 km:", gehalten2, " + tiefer schneller Flieger:", gehalten3,
          " Plaetze:", {k: (round(math.hypot(v[0], v[1])), round(v[2]), v[4]) for k, v in tr3.items()})
    return [("Helis werden gehalten, obwohl 5 Schiffe naeher sind (Platz 1-2), die 2 naechsten Schiffe auf 3-4, 5 frei", ok1),
            ("naeherer Heli verdraengt den ferneren", gehalten2 == [0, 1, 5, 7]),
            ("tiefer schneller Flieger: Luft-Platz, die 2 naechsten Schiffe bleiben", gehalten3 == [0, 1, 7, 8]
             and z3[8] and z3[8][0] in (1, 2))]


def test_springen():
    """Andres Fall: Ziel 2 sprang herum und wechselte die Art. Das haltende Radar sieht sein Ziel nicht (Mast davor),
    aber ein anderes Luftziel im breiten Strahl - das darf nicht an sein Ziel gehaengt werden."""
    # Kurs 0: Heli A hinten (1,5 km, 180 Grad, 120 m hoch), fuer die haltenden Radare 2-6 vom Mast verdeckt; knapp
    # daneben ein Schiff C (1,55 km, 182 Grad) im breiten Strahl des haltenden Radars - ohne eigenen Platz, weil 4 Schiffe
    # naeher sind (wie bei Andre: Plaetze voll, das fremde Objekt hing sich an Ziel 2)
    ziele = [((1500 * math.sin(math.pi), 1500 * math.cos(math.pi), 120), (0, 0, 0)),
             ((1550 * math.sin(math.pi + 0.035), 1550 * math.cos(math.pi + 0.035), 2), (0, 0, 0))]
    ziele += [((r * math.sin(bb), r * math.cos(bb), 2), (0, 0, 0)) for r, bb in ((900, 0.5), (1000, 1.5), (1100, 4.3), (1200, 5.5))]
    L = Lage(ziele, own=(0, 0, 0), hdg=0, behalten=True, blind={k: (0.5, 0.004) for k in range(1, 6)})
    L.laufe(10)
    spruenge, art, vorher = 0, 0, {}
    for _ in range(60 * 30):
        L.schritt()
        jetzt = L.ziele_aus()
        for k, v in jetzt.items():
            if k in vorher and vorher[k][5] == v[5]:
                if math.dist(vorher[k][:2], v[:2]) > 60:
                    spruenge += 1
                if vorher[k][4] != v[4]:
                    art += 1
        vorher = jetzt
    z, tr = L.zuordnung(tol=40)
    print("  Spruenge:", spruenge, " Art-Wechsel:", art, " Plaetze:", {k: (round(math.hypot(v[0], v[1])), v[4], v[5]) for k, v in tr.items()})
    return [("kein Ziel springt (gleiche Kennung, ueber 60 m pro Tick)", spruenge == 0),
            ("kein Ziel wechselt die Art", art == 0),
            ("Heli A wird gehalten", len(z[0]) == 1)]


def test_ruhend():
    """Andres Log 03.10. im Hafen: zwei stehende Dinge (190 m / 15 m hoch, 226 m / 37 m hoch) hielten beide Luft-Plaetze,
    die fliegenden Helis (1,1 km / 120 m, naeher kommend) blieben draussen; dazu etwas 40 m neben dem Schiff. Jetzt:
    bewegte Helis verdraengen die stehenden, die Flaks nehmen nur die bewegten; ein Heli, der heranfliegt und in 70 m
    in der Luft stehen bleibt, bleibt Ziel (Andre: Helis bewegen sich langsam, stehen, kommen naeher als 100 m)."""
    # Kurs 127 wie im Log; Richtungen ab Bug -> Welt
    b = lambda brg: math.radians(brg + 127)
    ziele = [((190 * math.sin(b(174)), 190 * math.cos(b(174)), 15), (0, 0, 0)),          # 0 steht, 15 m hoch
             ((226 * math.sin(b(196)), 226 * math.cos(b(196)), 37), (0, 0, 0)),          # 1 steht, 37 m hoch
             ((40 * math.sin(b(296)), 40 * math.cos(b(296)), 3), (0, 0, 0)),             # 2 Pier/Boot daneben
             ((1150 * math.sin(b(200)), 1150 * math.cos(b(200)), 120),
              (-13 * math.sin(b(200)), -13 * math.cos(b(200)), 0)),                      # 3 Heli, kommt naeher
             ((800 * math.sin(b(60)), 800 * math.cos(b(60)), 90),
              (20 * math.cos(b(60)), -20 * math.sin(b(60)), 0))]                         # 4 Heli rechts, quer
    L = Lage(ziele, own=(0, 0, 0), hdg=127, behalten=True)
    L.laufe(40)
    z0, tr0 = L.zuordnung(tol=60)
    fl0 = (L.bed.get(15), L.bed.get(19))
    # Heli 4 kommt auf 70 m heran und bleibt dann in der Luft stehen
    h4 = L.ziele[4]
    rel = [70 * math.sin(b(60)) - h4[0][0], 70 * math.cos(b(60)) - h4[0][1]]
    h4[1] = [rel[0] / 10, rel[1] / 10, -4]
    L.laufe(10)
    h4[1] = [0, 0, 0]
    L.laufe(15)
    z5, tr5 = L.zuordnung(tol=40)
    k4 = tr5[z5[4][0]][5] if z5[4] else None
    fl5 = (L.bed.get(15), L.bed.get(19))
    print("  Heli 4 jetzt %.0f m weg, steht: Platz %s, Flak L/R %s" % (math.hypot(*h4[0][:2]), z5[4], fl5))
    stehend = z5[4] and k4 in fl5
    z, tr, fl = z0, tr0, fl0
    kid = lambda i: tr[z[i][0]][5] if z[i] else None
    print("  Plaetze:", {k: (round(math.hypot(v[0], v[1])), round(v[2]), "L" if v[4] else "S") for k, v in tr.items()},
          " Ziel->Platz:", z, " Flak L/R:", fl, " Helis:", kid(3), kid(4))
    return [("beide fliegenden Helis auf den Luft-Plaetzen", z[3] and z[3][0] in (1, 2) and z[4] and z[4][0] in (1, 2)),
            ("Flaks auf den fliegenden Helis (je einer)", set(fl) == {kid(3), kid(4)}),
            ("das Ding 40 m neben dem Schiff steht: keine Kanone darauf (und nie naeher als 150 m)",
             not (z[2] and tr[z[2][0]][5] in (L.bed.get(7), L.bed.get(11)))),
            ("keine Waffe auf stehenden Dingen", not ({L.bed.get(7), L.bed.get(11)} & {kid(0), kid(1)} - {None})),
            ("Heli kommt auf 70 m heran und bleibt in der Luft stehen: weiter Ziel einer Flak", stehend)]


def test_paar():
    """Andres Log 03.10. 22:30: ein Luft-Platz sprang mit '175 m/s' zwischen einem stehenden Ding (250 m, 46 m hoch) und
    einem Heli dahinter (550 m, 138 m hoch, gleiche Richtung) hin und her. Jetzt: beide sauber getrennt, kein
    Fantasie-Tempo, Kennungen bleiben."""
    b = lambda brg: math.radians(brg + 127)
    ziele = [((250 * math.sin(b(204)), 250 * math.cos(b(204)), 46), (0, 0, 0)),
             ((550 * math.sin(b(229)), 550 * math.cos(b(229)), 138),
              (12 * math.cos(b(229)), -12 * math.sin(b(229)), 0))]
    L = Lage(ziele, own=(0, 0, 0), hdg=127, behalten=True)
    L.laufe(15)
    schnell, wechsel, vorher = 0, 0, None
    for _ in range(60 * 25):
        L.schritt()
        jetzt = L.ziele_aus()
        schnell += sum(1 for v in jetzt.values() if v[3] > 60)
        ids = {k: v[5] for k, v in jetzt.items()}
        if vorher is not None and ids != vorher:
            wechsel += 1
        vorher = ids
    z, tr = L.zuordnung(tol=50)
    print("  Plaetze:", {k: (round(math.hypot(v[0], v[1])), round(v[2]), v[3], "L" if v[4] else "S") for k, v in tr.items()},
          " Ziel->Platz:", z, " Ticks mit Tempo > 60:", schnell, " Wechsel:", wechsel)
    return [("stehendes Ding und Heli je genau ein Platz", len(z[0]) == 1 and len(z[1]) == 1),
            ("kein Fantasie-Tempo (ueber 60 m/s)", schnell == 0),
            ("Kennungen wechseln in 25 s nicht", wechsel == 0)]


def test_verlust():
    """Ein gehaltenes Schiff ist weg (abgeschossen): nach 'Ziel vergessen s' ist der Platz frei, das naechste wartende
    Schiff kommt hinein."""
    ziele = [((1000, 800, 2), (0, 0, 0)), ((-1400, 600, 2), (0, 0, 0)), ((2500, -2000, 2), (0, 0, 0))]
    L = Lage(ziele, own=(0, 0, 0), behalten=True)
    L.laufe(30)
    z, _ = L.zuordnung()
    vorher = sorted(i for i, v in z.items() if v)
    L.ziele[0][0] = [60000.0, 0.0, 2.0]
    L.laufe(PR["Ziel vergessen s"] + 8)
    z2, _ = L.zuordnung()
    nachher = sorted(i for i, v in z2.items() if v)
    print("  gehalten vorher:", vorher, " nach Abschuss von 0:", nachher)
    return [("2 Schiffe gehalten, das 3. wartet", vorher == [0, 1]),
            ("Schiff weg: Platz frei, das wartende kommt hinein", nachher == [1, 2])]


def test_hafen():
    """Im Hafen: viele stehende Dinge, die meisten weiter als 'Radar Reichweite m' - die Plaetze wechseln nicht."""
    rnd = random.Random(5)
    weit = [((r * math.sin(b), r * math.cos(b), rnd.uniform(0, 60)), (0, 0, 0))
            for r, b in ((rnd.uniform(12000, 25000), rnd.uniform(0, 2 * math.pi)) for _ in range(14))]
    nah = [((r * math.sin(b), r * math.cos(b), hh), (0, 0, 0)) for r, b, hh in ((300, 0.3, 5), (450, 1.9, 8), (2000, 3.0, 8))]
    L = Lage(nah + [((-2000, 500, 300), (0, 80, 0))] + weit, own=(0, 0, 0), behalten=True, weit=30000, hrausch=2.5)
    L.laufe(15)
    wechsel, vorher = 0, None
    for _ in range(60 * 20):
        L.schritt()
        jetzt = {k: v[5] for k, v in L.ziele_aus().items()}
        if vorher is not None and jetzt != vorher:
            wechsel += 1
        vorher = jetzt
    z, tr = L.zuordnung()
    print("  Plaetze:", {k: (round(math.hypot(v[0], v[1])), round(v[2]), v[4]) for k, v in tr.items()}, " Wechsel:", wechsel)
    return [("Hafen: die 2 naechsten Dinge (See) und der Flieger gehalten, nichts von weiter als 10 km",
             len(z[0]) == 1 and len(z[1]) == 1 and len(z[3]) == 1 and len(tr) == 3),
            ("Plaetze wechseln in 20 s nicht", wechsel == 0)]


def test_zuweisung():
    """Waffen: naechstes Ziel zuerst; Kanonen verteilen sich auf zwei Schiffe; ein naeheres Schiff verdraengt das fernere
    (die Kanone darauf nimmt das neue); Flaks nie dasselbe, ein Luftziel nur die Flak seiner Seite."""
    # Kurs 30: A Luft links voraus (1,7 km), B Luft rechts (1,8 km), S1 Schiff (1,9 km - Bild v3.2: AC reicht 2 km)
    ziele = [((-1500, 900, 200), (8, 6, 0)), ((1700, -300, 250), (-6, 8, 0)), ((500, 1830, 2), (6, -3, 0))]
    L = Lage(ziele, own=(0, 0, 0), behalten=True)
    L.laufe(15)
    z, tr = L.zuordnung()
    ka, kb, ks1 = z[0][0], z[1][0], z[2][0]
    kid = lambda k, t=None: (t or tr)[k][5]
    flak, kan = (L.bed.get(15), L.bed.get(19)), (L.bed.get(7), L.bed.get(11))
    print("  Plaetze A/B/S1:", ka, kb, ks1, " Flak L/R Kennung:", flak, " BC/AC:", kan)
    ok1 = flak == (kid(ka), kid(kb))
    ok2 = kan == (kid(ks1), kid(ks1))
    # S2 kommt dazu (1,5 km) -> die Kanonen verteilen sich
    L.ziele.append([[-1500 * math.sin(0.2), 1500 * math.cos(0.2), 2], [5, 4, 0]])
    L.laufe(12)
    z2, tr2 = L.zuordnung()
    kan2 = (L.bed.get(7), L.bed.get(11))
    ks2 = z2[3][0] if z2[3] else None
    # S3 (800 m) -> verdraengt das fernere S1; die Kanone darauf nimmt S3
    L.ziele.append([[800 * math.sin(1.2), 800 * math.cos(1.2), 2], [-4, 6, 0]])
    L.laufe(25)                         # Lage v3.0: See-Ziel 'bewegt' erst nach 40 m + 1 % dichter Verfolgung (~10 s)
    z3, tr3 = L.zuordnung()
    kan3 = (L.bed.get(7), L.bed.get(11))
    ks3 = z3[4][0] if z3[4] else None
    print("  + S2: BC/AC", kan2, "(S2 =", ks2 and kid(ks2, tr2), ")  + S3: BC/AC", kan3, "(S3 =", ks3 and kid(ks3, tr3), ")")
    L2 = Lage([((1700, -300, 250), (5, 5, 0))], own=(0, 0, 0), behalten=True)
    L2.laufe(12)
    flak4 = (L2.bed.get(15), L2.bed.get(19))
    print("  nur ein Luftziel rechts: Flak L/R", flak4)
    return [
        ("Flak L nimmt das linke, Flak R das rechte Luftziel", ok1),
        ("ein Schiff: beide Kanonen darauf", ok2),
        ("zweites Schiff: die Kanonen verteilen sich (BC auf das naehere)", ks2 is not None
         and kan2 == (kid(ks2, tr2), kid(ks1, tr2))),
        ("naeheres drittes Schiff verdraengt S1, eine Kanone nimmt es, die andere bleibt auf S2",
         ks3 is not None and set(kan3) == {kid(ks3, tr3), kid(ks2, tr2)} and not z3[2]),
        ("nur ein Luftziel rechts: nur Flak R", flak4[0] == 0 and flak4[1] > 0),
    ]


def test_abgeben():
    """Andres Test 03.10.: Heli rechts, die rechte Flak fand ihn nicht und wartete ewig, die linke blieb in Ruhe.
    Jetzt: meldet die Flak 4 s lang 'sucht', gibt sie das Ziel 20 s lang ab und die andere nimmt es."""
    L = Lage([((500, -870, 150), (5, 5, 0))], own=(0, 0, 0), hdg=0, behalten=True)
    L.laufe(15)
    z, tr = L.zuordnung()
    kid = tr[z[0][0]][5] if z[0] else None
    fl = lambda: (L.bed.get(15), L.bed.get(19))
    f0 = fl()
    L.flakz[22] = 1e5                   # Flak R meldet 'sucht'
    L.laufe(3)
    f3 = fl()
    L.laufe(2)
    f5 = fl()
    L.flakz[22] = 0                     # Flak R ohne Ziel: wartet
    L.laufe(25)
    f30 = fl()
    print("  Ziel %s; Flak L/R: anfangs %s, 3 s 'sucht' %s, 5 s %s, 30 s %s" % (kid, f0, f3, f5, f30))
    return [("anfangs nur die rechte Flak (Ziel rechts)", kid and f0 == (0, kid)),
            ("3 s 'sucht': sie bleibt dabei", f3 == f0),
            ("nach 4 s: die linke nimmt es, die rechte keins", f5 == (kid, 0)),
            ("nach 30 s: die linke bleibt dabei (nie beide)", f30 == (kid, 0))]


def test_flach():
    """Ein Heli je Seite; die rechte Flak meldet 'zu flach' (Sperrprofil): sie gibt ihren ab (die linke bleibt bei ihrem,
    nie beide auf einem) und versucht es nach 20 s wieder."""
    L = Lage([((-800, 400, 150), (-5, 5, 0)), ((800, 400, 150), (5, 5, 0))], own=(0, 0, 0), hdg=0, behalten=True)
    L.laufe(15)
    z, tr = L.zuordnung()
    kl, kr = (tr[z[i][0]][5] if z[i] else None for i in (0, 1))
    fl = lambda: (L.bed.get(15), L.bed.get(19))
    f0 = fl()
    L.flakz[22] = 4e5 + 900             # Flak R: zu flach
    L.laufe(5)
    f5 = fl()
    L.flakz[22] = 2e5 + 900
    L.laufe(10)
    f15 = fl()
    L.laufe(10)
    f25 = fl()
    print("  Ziele L/R %s %s; Flak L/R: anfangs %s, 5 s 'zu flach' %s, 15 s %s, 25 s %s" % (kl, kr, f0, f5, f15, f25))
    return [("anfangs jede Flak der Heli auf ihrer Seite", kl and kr and f0 == (kl, kr)),
            ("nach 4 s 'zu flach': rechte gibt ab, linke bleibt", f5 == (kl, 0)),
            ("waehrend der Sperre nimmt die rechte ihn nicht", f15 == (kl, 0)),
            ("nach 20 s versucht sie es wieder", f25 == (kl, kr))]


def test_wasser():
    """Andres Log 03.10.: ein Luft-Platz blieb 'Luft', obwohl sein Ziel auf dem Wasser fuhr (3-7 m) - die Flak wartete
    ewig. Jetzt: unter 10 m ist es nicht mehr Luft und zieht auf einen See-Platz."""
    L = Lage([((600, 900, 80), (10, 0, 0))], own=(0, 0, 0), hdg=0, behalten=True)
    L.laufe(12)
    z, tr = L.zuordnung()
    p0 = z[0][0] if z[0] else None
    a0 = tr[p0][4] if p0 else None
    kid = tr[p0][5] if p0 else None
    L.ziele[0][1] = [10, 0, -10]        # sinkt auf 4 m
    L.laufe(7.6)
    L.ziele[0][1] = [10, 0, 0]
    L.laufe(10)
    z, tr = L.zuordnung()
    p1 = z[0][0] if z[0] else None
    a1 = tr[p1][4] if p1 else None
    k1 = tr[p1][5] if p1 else None
    fl, ka = (L.bed.get(15), L.bed.get(19)), (L.bed.get(7), L.bed.get(11))
    print("  vorher Platz %s Luft %s Kennung %s; auf dem Wasser Platz %s Luft %s Kennung %s; Flaks %s Kanonen %s" % (
        p0, a0, kid, p1, a1, k1, fl, ka))
    return [("in 80 m Hoehe: Luft-Platz", p0 in (1, 2) and a0),
            ("auf dem Wasser: See-Platz, nicht mehr Luft", p1 in (3, 4) and a1 is False),
            ("dieselbe Kennung", k1 == kid),
            ("keine Flak darauf, eine Kanone schon", kid not in fl and kid in ka)]


def test_voraus():
    """Andres Log 04.10.: Heli A genau voraus (~360 Grad, 120 m hoch) - die hinteren Flaks kommen nach vorn erst ab ~30
    Grad ueber den Aufbau; Heli B rechts (108 Grad, 1,3 km). Flak R schoss auf B und liess ihn fallen, als A unter die
    halbe Entfernung kam (50-%-Regel) - danach schoss keine. Jetzt: A bekommt keine Flak, R bleibt auf B; ein Heli hoch
    voraus (ueber dem Sperrprofil) bekommt eine."""
    b = math.radians(108)
    L = Lage([((-60, 900, 120), (0, -2, 0)), ((1300 * math.sin(b), 1300 * math.cos(b), 190), (-4, 2, 0))],
             own=(0, 0, 0), hdg=0, behalten=True)
    L.laufe(15)
    z, tr = L.zuordnung()
    ka, kb = (tr[z[i][0]][5] if z[i] else None for i in (0, 1))
    fl = lambda: (L.bed.get(15), L.bed.get(19))
    f0 = fl()
    L.ziele[0][0] = [-30, 450, 110]     # A springt unter die halbe Entfernung von B (neue Spur, neue Kennung)
    L.laufe(6)
    f1 = fl()
    z, tr = L.zuordnung()
    ka1 = tr[z[0][0]][5] if z[0] else None
    L.ziele.append([[20, 230, 220], [6, 0, 0]])     # C hoch voraus: 42 Grad vom Flak-Turm
    L.laufe(12)
    z, tr = L.zuordnung()
    kc = tr[z[2][0]][5] if z[2] else None
    f2 = fl()
    print("  A %s B %s C %s; Flak L/R: anfangs %s, A naeher %s, mit C %s" % (ka, kb, kc, f0, f1, f2))
    return [("A voraus tief: keine Flak; B rechts: Flak R, Flak L nicht (quer uebers Schiff zu flach)",
             ka and kb and f0 == (0, kb)),
            ("A unter der halben Entfernung (Sprung: neue Kennung): R bleibt auf B, A bekommt keine",
             ka1 and f1 == (0, kb)),
            ("Heli hoch voraus: eine Flak darauf, A weiter keine", kc and kc in f2 and ka not in f2)]


def schreiber_pruefen(http, maxz):
    """Schreiber-Pakete [(Tick, Anfrage)] auswerten -> (Text, je Messstelle: Pakete, groesstes, verworfen, Zeilen je
    Datenstrom, Fehler)"""
    import re
    import urllib.parse
    from schreiber_spalten import spalten
    je, ticks, fehler = {}, {}, []
    proTick = {}
    for t, b in http:
        proTick[t] = proTick.get(t, 0) + 1
        a = urllib.parse.parse_qs(urllib.parse.urlparse(b).query, keep_blank_values=True)
        q, x = a["q"][0], int(a["x"][0])
        e = je.setdefault(q, {"pakete": 0, "max": 0, "x": 0})
        e["pakete"] += 1
        e["max"] = max(e["max"], len(b))
        e["x"] += x
        for z in a["d"][0].split(";"):
            m = re.match(r"([A-Za-z]*)(\d+),(.*)$", z)
            if not m:
                fehler.append(("Zeile", q, z[:40]))
                continue
            st = q + m.group(1)
            n = len(m.group(3).split(","))
            sp = spalten(st)
            if not sp or len(sp) != n:
                fehler.append(("Spalten", st, n, len(sp) if sp else None))
            ticks.setdefault(st, []).append(int(m.group(2)))
    doppelt = sum(1 for v in proTick.values() if v > 1)
    luecken = {}
    for st, tl in ticks.items():
        tl = sorted(tl)
        schritt = min(b - a for a, b in zip(tl, tl[1:])) if len(tl) > 1 else 1
        luecken[st] = sum(1 for a, b in zip(tl, tl[1:]) if b - a != schritt)
    return je, doppelt, luecken, fehler, {st: len(v) for st, v in ticks.items()}


def test_schreiber():
    """Schreiber v2 (Andre: "der Log muss ALLES sagen"): im Hafen mit vielen Dingen und Helis - jedes Skript sendet
    in seinem Takt (nie zwei Anfragen im selben Tick), Pakete unter 'Schreiber Zeichen', nichts verworfen, keine
    Luecken, jede Zeile passt zu ihrer Spaltenliste."""
    rnd = random.Random(7)
    dinge = [((r * math.sin(b), r * math.cos(b), rnd.uniform(1, 40)), (0, 0, 0))
             for r, b in ((rnd.uniform(150, 3000), rnd.uniform(0, 2 * math.pi)) for _ in range(14))]
    helis = [((900, 600, 150), (-5, 3, 0)), ((-700, 800, 120), (4, -2, 0)), ((300, -1200, 200), (0, 8, 0))]
    L = Lage(helis + dinge, own=(0, 0, 0), behalten=True, props={"Schreiber Port": 8768})
    L.laufe(20)
    je, doppelt, luecken, fehler, zeilen = schreiber_pruefen(L.http, PR["Schreiber Zeichen"])
    print("  Pakete je Messstelle (Anzahl, groesstes Zeichen, verworfen):",
          {q: (e["pakete"], e["max"], e["x"]) for q, e in sorted(je.items())})
    print("  Zeilen je Datenstrom:", dict(sorted(zeilen.items())), " Luecken:", {k: v for k, v in luecken.items() if v},
          " Ticks mit 2 Anfragen:", doppelt, " Fehler:", fehler[:5])
    erw = {"la", "ba"} | {"r%d" % k for k in range(1, 7)}
    return [("alle 8 Messstellen senden (Lage, Bildschirm, 6 Mast-Radare)", set(je) == erw),
            ("nie zwei Anfragen im selben Tick", doppelt == 0),
            ("nichts verworfen, Pakete unter 'Schreiber Zeichen'",
             all(e["x"] == 0 and e["max"] <= PR["Schreiber Zeichen"] + 200 for e in je.values())),
            ("keine Luecken (jeder Tick / jeder 4. bei der Lage)", not any(luecken.values())),
            ("jede Zeile passt zu ihrer Spaltenliste", not fehler)]


def test_tempo_falsch():
    """Andres Log 04.10. 08:43 (Hafen, kein Heli): zwei stehende Dinge 190 m / 300 m hinten, 15 m hoch, kamen mit
    falschem Tempo (51 / 64 m/s - im Topf zwei Dinge einer Spur zugeordnet) auf die Plaetze, wurden 'Luft, bewegt' und
    hielten beide Luft-Plaetze; das haltende Radar zielte dem Tempo nach. Nachgestellt: falsches Tempo auf ein stehendes
    Ding setzen - es bleibt See, nicht bewegt, dieselbe Kennung; ein echter Heli bekommt einen Luft-Platz und eine Flak."""
    b = lambda brg, r, h: (r * math.sin(math.radians(brg)), r * math.cos(math.radians(brg)), h)
    ziele = [(b(166, 300, 15), (0, 0, 0)), (b(175, 190, 15), (0, 0, 0)),
             (b(40, 1000, 80), (12 * math.cos(math.radians(40)), -12 * math.sin(math.radians(40)), 0))]
    L = Lage(ziele, own=(0, 0, 0), hdg=0, behalten=True)
    L.laufe(12)
    z, tr = L.zuordnung(tol=60)
    ka = z[0][0] if z[0] else None
    id0 = tr[ka][5] if ka else None
    t = L.g.T[ka] if ka else None
    if t is not None:
        # Tempo wie im Log: aus zwei falsch zugeordneten Ortungen (passt nicht zum vorigen: k 0), noch nicht dicht gemessen
        t.v[1], t.v[2], t.v[3], t.c, t.q, t.k = 45.0, -30.0, 3.0, 0, None, 0
    luft = bew = False
    alt_max = 0
    for _ in range(60 * 12):
        L.schritt()
        z2, tr2 = L.zuordnung(tol=60)
        if z2[0]:
            k = z2[0][0]
            tt = L.g.T[k]
            luft = luft or bool(tt.air)
            bew = bew or bool(tt.bw)
            alt_max = max(alt_max, tt.a)
    z, tr = L.zuordnung(tol=60)
    ka1 = z[0][0] if z[0] else None
    kh = z[2][0] if z[2] else None
    idh = tr[kh][5] if kh else None
    fl = (L.bed.get(15), L.bed.get(19))
    th = L.g.T[kh] if kh else None
    print("  Ding A Platz %s Kennung %s -> Platz %s Kennung %s, je Luft %s, je bewegt %s, Ticks ohne Ortung max %d;"
          " Heli Platz %s bewegt %s, Flaks %s" % (ka, id0, ka1, tr[ka1][5] if ka1 else None, luft, bew, alt_max, kh,
                                                  bool(th.bw) if th is not None else None, fl))
    return [("stehendes Ding mit falschem Tempo: bleibt auf seinem Platz (gleiche Kennung)",
             ka and ka1 == ka and tr[ka1][5] == id0),
            ("wird nie 'Luft' und nie 'bewegt'", not luft and not bew),
            ("haltendes Radar verliert es nicht (hoechstens 0,5 s ohne Ortung)", alt_max <= 30),
            ("echter Heli: Luft-Platz, bewegt, eine Flak darauf", kh in (1, 2) and th is not None and bool(th.bw)
             and idh in fl)]


def test_schwebt():
    """Andres Test 04.10. 09:01: ein Heli schwebte 435 m links in 150 m Hoehe und bekam keine Flak (nie 'bewegt').
    Jetzt: Luftziele ueber 'Stehend Ziel ab m' sind auch stehend Ziel; ein stehender Kran (40 m hoch) und dicht
    liegende Boote im Hafen (auf Meereshoehe, 20-30 m auseinander) werden kein Ziel."""
    b = lambda brg, r, h: (r * math.sin(math.radians(brg)), r * math.cos(math.radians(brg)), h)
    ziele = [(b(278, 435, 150), (0, 0, 0)),                                           # 0 Heli schwebt
             (b(150, 220, 40), (0, 0, 0)),                                            # 1 Kran
             (b(238, 137, 3), (0, 0, 0)), (b(232, 150, 3), (0, 0, 0)),                # 2, 3 Boote dicht
             (b(213, 170, 3), (0, 0, 0)), (b(220, 175, 2), (0, 0, 0))]                # 4, 5 Boote dicht
    L = Lage(ziele, own=(0, 0, 0), hdg=0, behalten=True)
    ziel_je = {i: False for i in range(len(ziele))}
    for _ in range(40 * 4):
        L.laufe(0.25)
        z, tr = L.zuordnung(tol=40)
        for i, ks in z.items():
            for k in ks:
                if L.aus.get(115 + k):
                    ziel_je[i] = True
    z, tr = L.zuordnung(tol=40)
    kh = z[0][0] if z[0] else None
    idh = tr[kh][5] if kh else None
    fl = (L.bed.get(15), L.bed.get(19))
    print("  Plaetze:", {k: (round(math.hypot(v[0], v[1])), round(v[2]), "L" if v[4] else "S") for k, v in tr.items()},
          " je Ziel fuer die Waffen:", ziel_je, " Flaks:", fl)
    return [("schwebender Heli (150 m): Ziel, eine Flak darauf", ziel_je[0] and idh in fl),
            ("stehender Kran (40 m) nie Ziel", not ziel_je[1]),
            ("dicht liegende Boote im Hafen nie Ziel", not any(ziel_je[i] for i in (2, 3, 4, 5)))]


def test_einzel():
    """Leertaste (Bild v3.1, Andre 04.10.): mit gewaehlter Waffe und Master Arm je Druck einen Tick 'Einzelschuss' fuer
    diese Waffe (gedrueckt halten wiederholt nicht); ohne Master Arm nichts; die Automatik (Feuer frei) bleibt."""
    ziele = [((-1400, 900, 200), (8, 6, 0)), ((1700, -300, 250), (-6, 8, 0))]
    L = Lage(ziele, own=(0, 0, 0), behalten=True)
    L.laufe(12)
    waehle(L, 4)                        # Flak R

    def zaehle(ticks, leer, ma=True):
        L.ma = ma
        n = {w: 0 for w in range(1, 5)}
        frei = []
        for i in range(ticks):
            L.leer = leer(i)
            L.schritt()
            for w in range(1, 5):
                if L.bed.get(112 + w):
                    n[w] += 1
            frei.append(bool(L.bed.get(108)))
        L.leer = False
        L.ma = True
        return n, all(frei)
    n1, f1 = zaehle(120, lambda i: 10 <= i < 70)            # einmal lang gedrueckt
    n2, f2 = zaehle(120, lambda i: i % 30 in (5, 6))         # viermal kurz
    n3, _ = zaehle(60, lambda i: 10 <= i < 12, ma=False)     # ohne Master Arm
    print("  Einzelschuss-Ticks je Waffe: lang gedrueckt %s, 4x kurz %s, ohne Master Arm %s; Flak R Automatik frei: %s %s"
          % (n1, n2, n3, f1, f2))
    return [("lang gedrueckt: genau ein Einzelschuss, nur fuer die gewaehlte Flak R", n1 == {1: 0, 2: 0, 3: 0, 4: 1}),
            ("viermal kurz: vier Einzelschuesse", n2 == {1: 0, 2: 0, 3: 0, 4: 4}),
            ("ohne Master Arm: keiner", n3 == {1: 0, 2: 0, 3: 0, 4: 0}),
            ("die Automatik der Flak bleibt frei", f1 and f2)]


def test_feindhafen():
    """Andres Test 04.10. 12:54 am feindlichen Hafen (Kurs 127): stehende Dinge achtern und seitlich (Lage aus dem Log),
    ein Patrouillenboot rechts voraus (700 m, 24 Grad), faehrt weg. Die See-Plaetze hielten zwei stehende Dinge achtern
    (ihre Spuren sprangen auf Nachbar-Dinge und galten als 'bewegt'). Jetzt: das Boot bekommt einen See-Platz und die
    Kanonen, kein stehendes Ding wird 'bewegt'."""
    b = lambda brg, r, h: (r * math.sin(math.radians(brg + 127)), r * math.cos(math.radians(brg + 127)), h)
    dinge = [(85, 245, 2), (174, 226, 3), (137, 237, 1), (38, 297, 4), (166, 191, 3), (170, 213, 1), (186, 175, 13),
             (301, 166, 15), (449, 336, 14), (129, 238, 1), (84, 250, 2), (175, 230, 1)]
    ziele = [(b(brg, r, h), (0, 0, 0)) for r, brg, h in dinge]
    w = math.radians(24 + 127)
    ziele.append((b(24, 700, 1), (7 * math.sin(w), 7 * math.cos(w), 0)))          # Patrouillenboot, faehrt weg
    L = Lage(ziele, own=(0, 0, 0), hdg=127, behalten=True, frisch=True)
    bewegt_steht = set()
    boot_platz = 0
    for _ in range(45 * 4):
        L.laufe(0.25)
        z, tr = L.zuordnung(tol=40)
        for i in range(len(dinge)):
            for k in z[i]:
                if L.aus.get(115 + k):
                    bewegt_steht.add(i)
        if z[len(dinge)] and z[len(dinge)][0] in (3, 4):
            boot_platz += 1
    z, tr = L.zuordnung(tol=40)
    kb = z[len(dinge)][0] if z[len(dinge)] else None
    idb = tr[kb][5] if kb else None
    kan = (L.bed.get(7), L.bed.get(11))
    print("  Plaetze:", {k: (round(math.hypot(v[0], v[1])), round((math.degrees(math.atan2(v[0], v[1])) - 127) % 360),
                             "L" if v[4] else "S") for k, v in tr.items()},
          " Boot auf See-Platz in %d von 180 Viertelsekunden, am Ende Platz %s, Kanonen BC/AC %s, stehend als Ziel: %s"
          % (boot_platz, kb, kan, sorted(bewegt_steht)))
    return [("Patrouillenboot voraus auf einem See-Platz (am Ende und meistens)", kb in (3, 4) and boot_platz > 120),
            ("beide Kanonen auf dem Boot", idb and kan == (idb, idb)),
            ("kein stehendes Ding im Hafen wird Ziel fuer die Waffen", not bewegt_steht)]


def test_land():
    """Andres zwei Tests 04.10. ~14:05: BC und AC schossen auf Bodenziele (#11 308 m/94 Grad, 15 m hoch, fast stehend;
    #10 1-1,6 km/249 Grad, 15 m hoch, faehrt ~10 m/s) - dazu Bauten an Land 14 m hoch und ein Schiff 1,4 km/40 Grad,
    -2 m, 10 m/s. Lage v3.2: Land (geglaettet hoeher als 7 m) ist nie Kanonen-Ziel; das Schiff bekommt beide Kanonen."""
    hd = 30
    b = lambda brg, r, h: (r * math.sin(math.radians(brg + hd)), r * math.cos(math.radians(brg + hd)), h)
    w = lambda brg, v: (v * math.sin(math.radians(brg + hd)), v * math.cos(math.radians(brg + hd)), 0.0)
    ziele = [(b(94, 308, 15), w(180, 0.8)), (b(249, 1058, 15), w(160, 10)), (b(150, 404, 14), (0, 0, 0)),
             (b(200, 1100, 14), (0, 0, 0)), (b(40, 1388, -2), w(100, 10))]
    L = Lage(ziele, own=(0, 0, 0), hdg=hd, behalten=True, frisch=True, hrausch=3.0)
    land_ziel, schiff_ziel = 0, 0
    for q in range(60 * 4):
        L.laufe(0.25)
        z, tr = L.zuordnung(tol=60)
        ids = {i: tr[z[i][0]][5] for i in range(len(ziele)) if z[i]}
        kan = (L.bed.get(7), L.bed.get(11))
        if any(k and k in [ids.get(i) for i in range(4)] for k in kan):
            land_ziel += 1
        if ids.get(4) and kan == (ids[4], ids[4]):
            schiff_ziel += 1
    print("  Viertelsekunden mit einer Kanone auf Land: %d, beide Kanonen auf dem Schiff: %d von 240" % (land_ziel, schiff_ziel))
    return [("keine Kanone auf einem Bodenziel", land_ziel == 0),
            ("beide Kanonen auf dem Schiff (meistens)", schiff_ziel >= 120)]


def test_tief():
    """Andres Test 04.10. ~14:25: ein sehr tief fliegender Eurofighter und Hubschrauber wurden als Schiff von BC und AC
    beschossen (Log: kreisten 2-5 m ueber dem Meer in ~2 km, Kreis ~100 m, gemessenes Tempo sprang 0..80 m/s; ein Heli
    7-9 m hoch mit 30 m/s). Nachgestellt: Heli kreist 4 m hoch (45 m/s, Radius 100 m), Heli 5 m hoch mit 30 m/s geradeaus,
    Jet 5 m hoch mit 150 m/s, dazu ein Schiff 1,5 km mit 10 m/s. Lage v3.3: Strecken-Tempo ueber 28 m/s ist kein Schiff."""
    hd = 0
    b = lambda brg, r, h: (r * math.sin(math.radians(brg + hd)), r * math.cos(math.radians(brg + hd)), h)
    w = lambda brg, v: (v * math.sin(math.radians(brg + hd)), v * math.cos(math.radians(brg + hd)), 0.0)
    ziele = [(b(345, 2000, 4), (45.0, 0.0, 0.0)), (b(320, 2300, 5), w(70, 30)), (b(20, 2600, 5), w(250, 150)),
             (b(40, 1500, -2), w(110, 10))]
    L = Lage(ziele, own=(0, 0, 0), hdg=hd, behalten=True, frisch=True, hrausch=3.0)
    falsch, schiff_ziel = 0, 0
    om = 45.0 / 100.0                         # Kreis: Winkelgeschwindigkeit rad/s
    for q in range(60 * 4):
        for _ in range(15):
            v = L.ziele[0][1]
            c, s_ = math.cos(om / 60), math.sin(om / 60)
            L.ziele[0][1] = [v[0] * c - v[1] * s_, v[0] * s_ + v[1] * c, 0.0]
            L.schritt()
        z, tr = L.zuordnung(tol=80)
        ids = {i: tr[z[i][0]][5] for i in range(len(ziele)) if z[i]}
        kan = (L.bed.get(7), L.bed.get(11))
        if any(k and k in [ids.get(i) for i in range(3)] for k in kan):
            falsch += 1
        if ids.get(3) and kan == (ids[3], ids[3]):
            schiff_ziel += 1
    print("  Viertelsekunden mit einer Kanone auf Heli/Jet: %d, beide Kanonen auf dem Schiff: %d von 240" % (falsch, schiff_ziel))
    return [("keine Kanone auf tief fliegendem Heli oder Jet", falsch == 0),
            ("beide Kanonen auf dem Schiff (meistens)", schiff_ziel >= 100)]


def test_feuer():
    """Feuer frei: nur mit Master Arm - dann alle Waffen selbst, auch die gewaehlte (Bild v3.0, Andre 04.10.: keine
    Leertaste mehr); Leertaste und Sitz aendern nichts."""
    ziele = [((-1400, 900, 200), (8, 6, 0)), ((1700, -300, 250), (-6, 8, 0)), ((500, 1500, 2), (6, -3, 0))]
    L = Lage(ziele, own=(0, 0, 0), behalten=True)
    L.laufe(22)                         # Lage v3.0: das Schiff ist erst nach ~10 s dichter Verfolgung 'bewegt'
    frei = lambda: tuple(bool(L.bed.get(104 + w)) for w in range(1, 5))
    L.ma = False
    L.laufe(0.2)
    aus = frei()
    L.ma = True
    waehle(L, 3)
    sitz = frei()
    L.leer = True
    L.laufe(0.1)
    leer = frei()
    L.leer = False
    L.sitz = False
    L.laufe(0.1)
    leer_sitz = frei()
    print("  Feuer frei BC/AC/FlakL/FlakR: Master Arm aus", aus, " Flak L gewaehlt", sitz, " +Leertaste", leer,
          " niemand im Sitz", leer_sitz)
    return [("Master Arm aus: keine Waffe frei", aus == (False,) * 4),
            ("Master Arm an, Flak L gewaehlt: alle frei (auch sie, ohne Leertaste)", sitz == (True,) * 4),
            ("Leertaste aendert nichts", leer == (True,) * 4),
            ("niemand im Sitz: alle frei", leer_sitz == (True,) * 4)]


def test_waffenwahl():
    """Monitor 2x3: Flak R antippen = gewaehlt (Finger liegen lassen schaltet nicht zurueck), nochmal = keine Waffe;
    Master Arm kommt vom Schalter am Instrument Panel."""
    L = Lage([((-900, 1300, 150), (0, 0, 0))], own=(0, 0, 0))
    L.laufe(2)
    px = lambda zz: 2 + (zz + 155) * 92 / 224
    L.wtouch = (px(-105), 32 + 10 * 0.85)
    L.laufe(1)
    w1 = L.bed.get(2)
    L.wtouch = None
    L.laufe(0.3)
    L.wtouch = (px(-105) + 1, 32 + 10 * 0.85)
    L.laufe(0.3)
    L.wtouch = None
    L.laufe(0.3)
    w2 = L.bed.get(2)
    L.wtouch = (px(5), 32)
    L.laufe(0.3)
    L.wtouch = None
    L.laufe(0.3)
    w3 = L.bed.get(2)
    ma_an = L.bed.get(101)
    L.ma = False
    L.laufe(0.3)
    ma_aus = L.bed.get(101)
    zeichen = [d[0] for d in L.wio["draw"]]
    print("  Flak R antippen ->", w1, " nochmal ->", w2, " BC ->", w3, " Master Arm an/aus:", ma_an, ma_aus)
    return [("2x3: Flak R antippen = Waffe 4 (auch mit liegendem Finger)", w1 == 4),
            ("2x3: nochmal = keine Waffe", w2 == 0),
            ("2x3: BC antippen = Waffe 1", w3 == 1),
            ("Master Arm vom Instrument Panel kommt im Bildschirm an", ma_an is True and ma_aus is False),
            ("2x3: zeichnet Umriss und Waffen", zeichen.count("ci") >= 4 and zeichen.count("rf") > 50)]


def test_zeichnen():
    """Bildschirm zeichnet (ohne Eingaenge in onDraw) mit jeder Waffe; rotes Quadrat um beschossene Ziele; Zoom."""
    L = Lage([((150, 120, 2), (4, 4, 0)), ((-120, 200, 2), (-4, 4, 0)), ((-1400, 900, 200), (20, 0, 0)),
              ((5000, 3000, 2), (0, 0, 0))], own=(0, 0, 0), behalten=True)
    L.laufe(25)
    ok = True
    rot = 0
    for wfw in range(5):
        waehle(L, wfw)
        try:
            L.bio["draw"].clear()
            L.bg.onDraw()
            d = L.bio["draw"]
            rot = max(rot, sum(1 for i in range(len(d) - 1) if d[i][0] == "c" and d[i][1:4] == (255, 30, 20) and d[i + 1][0] == "r"))
        except Exception as e:  # noqa: BLE001
            print("  Fehler", wfw, e)
            ok = False
    texte = [x[3] for x in L.bio["draw"] if x[0] == "t"]

    print("  Zoom %g m, rote Quadrate/Rahmen %d, Texte %s" % (L.bg.rr, rot, texte[:5]))
    L0 = Lage([], own=(0, 0, 0))
    L0.laufe(1)
    # Bild v3.4 (Andres Test 06.10. im Hafen: Zoom 200 m): zwei stehende Bodenziele in 130/145 m halten den Zoom nicht fest
    LH = Lage([((100, 83, 15), (0, 0, 0)), ((-60, 132, 15), (0, 0, 0))], own=(0, 0, 0), behalten=True)
    LH.laufe(20)
    return [("Bildschirm zeichnet mit jeder Waffe", ok),
            ("rote Quadrate um die beschossenen Ziele (Radar und Liste)", rot >= 4),
            ("Zoom (Stufen 1/2,5/5/10 km): zwei Schiffe ~400 m auseinander -> 1 km (%g)" % L.bg.rr, L.bg.rr == 1000),
            ("ohne Ziele: 10 km", L0.bg.rr == 10000),
            ("Hafen: zwei Bodenziele 130/145 m (15 m hoch) loesen keinen Zoom aus (%g m)" % LH.bg.rr, LH.bg.rr == 10000),
            ("Master Arm an steht da", "MASTER ARM AN" in texte)]


def main():
    ok = True
    for name, f in (("Verfolgen, Radar meldet nur im Strahl", lambda: test_verfolgen(False)),
                    ("Verfolgen, Radar behaelt Ziele", lambda: test_verfolgen(True)),
                    ("Verfolgen, Winkel ab Strahl", lambda: test_verfolgen(True, strahl=True)),
                    ("Plaetze nach Art", test_plaetze), ("Springen (Mast verdeckt)", test_springen), ("Hafen: stehende Dinge", test_ruhend), ("Ding und Heli hintereinander", test_paar), ("Verlust", test_verlust), ("Hafen", test_hafen),
                    ("Zuweisung", test_zuweisung), ("Flak gibt ab", test_abgeben), ("Flak zu flach", test_flach),
                    ("Luftziel geht aufs Wasser", test_wasser),
                    ("Sperrprofil: Heli voraus", test_voraus), ("Schreiber v2", test_schreiber), ("Falsches Tempo im Hafen", test_tempo_falsch), ("Heli schwebt, Hafen-Dinge", test_schwebt), ("Einzelschuss Leertaste", test_einzel), ("Feindlicher Hafen: Boot voraus", test_feindhafen), ("Land: Bodenziele nie Kanonen-Ziel", test_land), ("Tiefflieger nie Kanonen-Ziel", test_tief), ("Feuer: Master Arm, Leertaste", test_feuer),
                    ("Waffenwahl 2x3", test_waffenwahl), ("Zeichnen", test_zeichnen)):
        print("---", name)
        ok &= pruefe(f())
    print("ALLES OK" if ok else "FEHLER")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
