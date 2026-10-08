"""Pruefstand fuer den KI Landkreuzer (landkreuzer/lua/ki_fahren.lua + ki_karte.lua), Lua 5.3 ueber lupa.

Aufruf (Python mit lupa):  python landkreuzer/tools/test_ki.py  [Testname ...]

Was nachgebildet wird:
- Lua wie im Stormworks-Microcontroller: nur die Namen, die es im Spiel gibt (LUA_STORMWORKS.md); input nur in onTick,
  screen/map nur in onDraw (sonst Fehler wie im Spiel); jeder Lua-Fehler = Test verloren.
- Welt (x Ost, z Nord, Hoehe ueber dem Meer): Hoehenfeld (Ebene 20 m, Huegel, See mit Strand, Klippe) und Hindernisse
  (Kreise/Kaesten = Felsen/Gebaeude, Hoehe ueber dem Boden).
- Panzer 27,5 x 9,5 m, Panzerlenkung: Vortrieb aus (L+R)/2 (leistungsbegrenzt, ca. 12 m/s Spitze, Hang bremst),
  Drehen aus (L-R)/2 (links schneller = Rechtsdrehung). Er liegt auf 7 Radpaaren (obere Huelle des Bodens laengs):
  ueber eine Kante kippt er erst, wenn die Mitte drueber ist. Hindernis = Stoss (Tempo 0, bleibt davor).
- Laser an denselben Stellen wie im gebauten Fahrzeug (Tabelle LASER, alles 90-Grad-Richtungen): drei Front-Laser
  2,4 m hoch (3,5 m auseinander), Seiten-Laser 3,1 m hoch auf Auslegern ueber den Raedern, Bug-Laser 1,6 m hoch in
  der Bugspitze senkrecht nach unten, Heck-Laser. Laser gehen durchs Wasser (treffen den Grund).
- Physik-Sensor in der Mitte, 2,1 m ueber dem Boden; Kompass gegen den Uhrzeigersinn ('Kompass Richtung' -1);
  Kanal 8 (Tempo vorwaerts) absichtlich mit falschem Vorzeichen - die KI rechnet ihr Tempo selbst.
60 Ticks je Sekunde. Jede Pruefung druckt eine Zeile (OK/FEHLER), am Ende 'ALLES OK'.
"""
import math
import os
import re
import sys
import time

from lupa import lua53

HIER = os.path.dirname(os.path.abspath(__file__))
LUA_DIR = os.path.join(os.path.dirname(HIER), "lua")
sys.path.insert(0, HIER)
from ki_props import PROPS_FAHREN, PROPS_KARTE  # noqa: E402

GRENZE = 8000          # Zeichen je Skript nach dem Verkleinern (im Spiel hart 8192)
DT = 1.0 / 60

# ---------------------------------------------------------------------------------------------------------------
# Verkleinern (einfach: Kommentare, Leerzeilen, Einrueckung, Leerzeichen neben Satzzeichen)
# ---------------------------------------------------------------------------------------------------------------


def _teile(zeile):
    """Zeile -> Liste von (ist_text, stueck); Kommentar ab '--' ausserhalb von Texten faellt weg."""
    teile, i, a, q = [], 0, 0, None
    while i < len(zeile):
        c = zeile[i]
        if q:
            if c == "\\":
                i += 2
                continue
            if c == q:
                teile.append((True, zeile[a:i + 1]))
                a, q = i + 1, None
        elif c in "'\"":
            teile.append((False, zeile[a:i]))
            a, q = i, c
        elif zeile.startswith("--", i):
            teile.append((False, zeile[a:i]))
            return teile
        i += 1
    teile.append((q is not None, zeile[a:]))
    return teile


def _id(c):
    return c.isalnum() or c == "_"


def _eng(code):
    code = re.sub(r"\s+", " ", code)
    aus = []
    for i, c in enumerate(code):
        if c == " ":
            p = aus[-1] if aus else ""
            n = code[i + 1] if i + 1 < len(code) else ""
            if not p or not n:
                continue
            behalten = (_id(p) and _id(n)) or (p == "-" and n == "-") or (p == "." and (n.isdigit() or n == ".")) \
                or (p.isdigit() and n == ".") or (p == "[" and n in "[=")
            if not behalten:
                continue
        aus.append(c)
    return "".join(aus)


def minify(src):
    zeilen = []
    for zeile in src.split("\n"):
        s = "".join(t if ist else _eng(t) for ist, t in _teile(zeile)).strip()
        if s:
            zeilen.append(s)
    return "\n".join(zeilen)


def quelle(name):
    with open(os.path.join(LUA_DIR, name), encoding="utf-8") as f:
        return f.read()


# ---------------------------------------------------------------------------------------------------------------
# Lua-Chip wie im Spiel
# ---------------------------------------------------------------------------------------------------------------
ERLAUBT = ("pairs", "ipairs", "next", "type", "tostring", "tonumber", "math", "string", "table", "input", "output",
           "property", "screen", "map", "async", "debug")
SPERREN = """
local keep={}
for _,k in ipairs({%s}) do keep[k]=1 end
local g=_G
local weg={}
for k in pairs(g) do if not keep[k] then weg[#weg+1]=k end end
for _,k in ipairs(weg) do g[k]=nil end
for _,k in ipairs({'atan2','pow','cosh','sinh','tanh','frexp','ldexp','log10'}) do math[k]=nil end
table.getn=nil table.maxn=nil
""" % ",".join("'%s'" % n for n in ERLAUBT)
SCREEN = ("setColor", "drawClear", "drawLine", "drawCircle", "drawCircleF", "drawRect", "drawRectF", "drawTriangle",
          "drawTriangleF", "drawText", "drawTextBox", "drawMap", "setMapColorOcean", "setMapColorShallows",
          "setMapColorLand", "setMapColorGrass", "setMapColorSand", "setMapColorSnow", "setMapColorRock",
          "setMapColorGravel")


def map_to_screen(cx, cy, zoom, sw, sh, wx, wy):
    s = sw / (zoom * 1000.0)
    return sw / 2 + (wx - cx) * s, sh / 2 - (wy - cy) * s


def screen_to_map(cx, cy, zoom, sw, sh, px, py):
    s = sw / (zoom * 1000.0)
    return cx + (px - sw / 2) / s, cy - (py - sh / 2) / s


class Chip:
    def __init__(self, src, props, seed=1):
        self.rt = lua53.LuaRuntime(unpack_returned_tuples=True)
        g = self.rt.globals()
        self.n, self.b = [0.0] * 33, [False] * 33
        self.on, self.ob = [0.0] * 33, [False] * 33
        self.modus = None
        self.draw = []
        self.groesse = (96, 96)
        self.props = props
        chip = self

        def nur(m, f):
            def g2(*a):
                if chip.modus != m:
                    raise RuntimeError("%s ausserhalb von %s (im Spiel: Fehler)" % (f.__name__, m))
                return f(*a)
            return g2

        def get_n(i):
            i = int(i)
            return float(chip.n[i]) if 1 <= i <= 32 else 0.0

        def get_b(i):
            i = int(i)
            return bool(chip.b[i]) if 1 <= i <= 32 else False

        def set_n(i, v):
            if v is None or not isinstance(v, (int, float)) or v != v or abs(v) == float("inf"):
                raise RuntimeError("Ausgang Zahl %s = %r (nil/NaN/unendlich)" % (i, v))
            if 1 <= int(i) <= 32:
                chip.on[int(i)] = float(v)

        def set_b(i, v):
            if 1 <= int(i) <= 32:
                chip.ob[int(i)] = bool(v)

        def prop(name):
            if name not in chip.props:
                raise KeyError("Property fehlt: %s" % name)
            return float(chip.props[name])

        def zeichen(name):
            def f(*a):
                for v in a:
                    if isinstance(v, float) and (v != v):
                        raise RuntimeError("screen.%s mit NaN" % name)
                chip.draw.append((name,) + tuple(a))
            f.__name__ = "screen." + name
            return f

        g.input = self.rt.table(getNumber=nur("tick", get_n), getBool=nur("tick", get_b))
        g.output = self.rt.table(setNumber=set_n, setBool=set_b)
        g.property = self.rt.table(getNumber=prop, getBool=lambda s: bool(prop(s)), getText=lambda s: "")
        scr = {k: nur("draw", zeichen(k)) for k in SCREEN}
        scr["getWidth"] = nur("draw", lambda: chip.groesse[0])
        scr["getHeight"] = nur("draw", lambda: chip.groesse[1])
        g.screen = self.rt.table(**scr)
        map_to_screen.__name__, screen_to_map.__name__ = "map.mapToScreen", "map.screenToMap"
        g.map = self.rt.table(mapToScreen=nur("draw", map_to_screen), screenToMap=nur("draw", screen_to_map))
        g["async"] = self.rt.table(httpGet=lambda *a: None)
        g.debug = self.rt.table(log=lambda *a: None)
        self.rt.execute("math.randomseed(%d)" % seed)
        self.rt.execute(SPERREN)
        self.rt.execute(src)
        self.g = g

    def tick(self):
        self.modus = "tick"
        try:
            self.g.onTick()
        finally:
            self.modus = None

    def zeichne(self):
        self.draw = []
        self.modus = "draw"
        try:
            self.g.onDraw()
        finally:
            self.modus = None


PR_FAHREN = {n: v for n, v, _ in PROPS_FAHREN}
PR_KARTE = {n: v for n, v, _ in PROPS_KARTE}

# ---------------------------------------------------------------------------------------------------------------
# Welt
# ---------------------------------------------------------------------------------------------------------------


class Hind:
    """Hindernis: ('k', Ost, Nord, Radius, Hoehe) Kreis oder ('b', Ost0, Nord0, Ost1, Nord1, Hoehe) Kasten."""

    def __init__(self, art, *w):
        self.art = art
        if art == "k":
            self.cx, self.cz, self.r, self.hoch = w
        else:
            self.x0, self.z0, self.x1, self.z1, self.hoch = w

    def spanne(self, ox, oz, dx, dz):
        """Eintritt/Austritt des waagerechten Anteils (Parameter t entlang des Strahls) oder None."""
        if self.art == "k":
            px, pz = ox - self.cx, oz - self.cz
            a = dx * dx + dz * dz
            c = px * px + pz * pz - self.r * self.r
            if a < 1e-12:
                return (0.0, 1e9) if c <= 0 else None
            b = 2 * (px * dx + pz * dz)
            disk = b * b - 4 * a * c
            if disk < 0:
                return None
            w = math.sqrt(disk)
            t1, t2 = (-b - w) / (2 * a), (-b + w) / (2 * a)
            return (t1, t2) if t2 >= 0 else None
        t1, t2 = -1e9, 1e9
        for o, d, lo, hi in ((ox, dx, self.x0, self.x1), (oz, dz, self.z0, self.z1)):
            if abs(d) < 1e-12:
                if not lo <= o <= hi:
                    return None
            else:
                a, b = (lo - o) / d, (hi - o) / d
                if a > b:
                    a, b = b, a
                t1, t2 = max(t1, a), min(t2, b)
        return (t1, t2) if t1 <= t2 and t2 >= 0 else None


class Welt:
    def __init__(self, hoehe=None, hmax=20.0, hind=(), name=""):
        self.h = hoehe or (lambda x, z: 20.0)
        self.hmax = hmax
        self.hind = [Hind(*o) for o in hind]
        self.name = name

    def strahl(self, o, d, tmax=60.0):
        best = None
        for ob in self.hind:
            sp = ob.spanne(o[0], o[2], d[0], d[2])
            if not sp:
                continue
            t1, t2 = max(sp[0], 0.0), sp[1]
            if best is not None and t1 >= best:
                continue
            top = self.h(o[0] + d[0] * t1, o[2] + d[2] * t1) + ob.hoch
            y = o[1] + d[1] * t1
            if y <= top:
                t = t1
            elif d[1] < 0:
                t = (o[1] - top) / -d[1]
                if not t1 <= t <= t2:
                    continue
            else:
                continue
            if t <= tmax and (best is None or t < best):
                best = t
        g = self.gelaende(o, d, best if best is not None else tmax)
        if g is not None:
            best = g
        return best if best is not None else 4000.0

    def gelaende(self, o, d, tmax):
        if d[1] >= 0 and o[1] > self.hmax + 0.01:
            return None
        t = prev = 0.0
        h = self.h
        while t < tmax:
            t = min(t + (0.25 if t < 4 else 1.0 if t < 30 else 3.0), tmax)
            y = o[1] + d[1] * t
            if y < h(o[0] + d[0] * t, o[2] + d[2] * t):
                lo, hi = prev, t
                for _ in range(10):
                    mid = (lo + hi) / 2
                    if o[1] + d[1] * mid < h(o[0] + d[0] * mid, o[2] + d[2] * mid):
                        hi = mid
                    else:
                        lo = mid
                return hi
            if d[1] >= 0 and y > self.hmax:
                return None
            prev = t
        return None


def eben():
    return Welt(name="Ebene")


# ---------------------------------------------------------------------------------------------------------------
# Panzer
# ---------------------------------------------------------------------------------------------------------------
# Masse wie im gebauten Fahrzeug (bau_landkreuzer.py, Bloecke 0,25 m, Physik-Sensor bei z -12, y 2; Raeder 7x7, Boden
# bei y -6,5): Rumpf z -66,5 .. 42,5 (+ Leiter), Front-Laser z 41 / y 3 / x 0, +-14, Seiten-Laser z -8 / y 6 / x +-19,
# Bug-Laser in der Bugspitze z 42 / y 0, Heck-Laser z -67 / y 3
LANG, BREIT = 27.5, 9.5
HL = LANG / 2
SENSOR_H = 2.1
BUG_H = 1.6
LASER = {  # Kanal: (vor, rechts, hoch, Richtung)
    9: (13.25, -3.5, 2.4, "f"), 10: (13.25, 0.0, 2.4, "f"), 11: (13.25, 3.5, 2.4, "f"),
    12: (1.0, -4.75, 3.1, "l"), 13: (1.0, 4.75, 3.1, "r"), 14: (13.5, 0.0, BUG_H, "u"), 15: (-13.75, 0.0, 2.4, "h"),
}


def _kreuz(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


class Panzer:
    def __init__(self, welt, x=0.0, z=0.0, kurs=0.0):
        self.w = welt
        self.x, self.z, self.psi = x, z, math.radians(kurs)
        self.v = self.om = 0.0
        self.stoesse = 0            # Stoesse an Hindernissen, die die Laser sehen koennen (2 m und hoeher)
        self.flach = 0              # an flachen (unsichtbaren) Hindernissen - dafuer ist die Festfahr-Erkennung da
        self.frei = 999             # Ticks seit dem letzten Stoss (entprellt: neuer Stoss erst nach 1 s frei)
        self.blockiert = False
        self.abgestuerzt = False
        self.lage()

    def auflage(self, x, z, psi):
        """Hoehe der Unterkante in der Mitte, Nick, Roll aus der oberen Huelle der 7 Radpaare."""
        f = (math.sin(psi), math.cos(psi))
        r = (math.cos(psi), -math.sin(psi))
        pk = []
        for k in range(7):
            s = -HL + k * LANG / 6
            pk.append((s, max(self.w.h(x + f[0] * s + r[0] * q, z + f[1] * s + r[1] * q) for q in (-4.0, 4.0))))
        huelle = []
        for p in pk:
            while len(huelle) >= 2:
                o, a = huelle[-2], huelle[-1]
                if (a[0] - o[0]) * (p[1] - o[1]) - (a[1] - o[1]) * (p[0] - o[0]) >= 0:
                    huelle.pop()
                else:
                    break
            huelle.append(p)
        a, b = huelle[0], huelle[-1]
        for i in range(len(huelle) - 1):
            if huelle[i][0] < 0 <= huelle[i + 1][0]:
                a, b = huelle[i], huelle[i + 1]
                break
        nick = math.atan2(b[1] - a[1], b[0] - a[0])
        y0 = a[1] + (0 - a[0]) * (b[1] - a[1]) / (b[0] - a[0])
        # quer: je Seite die hoechste Auflage (starrer Rumpf auf Raedern - eine Ecke ueber einer Kante kippt ihn nicht)
        hl = max(self.w.h(x + f[0] * s - r[0] * 4.0, z + f[1] * s - r[1] * 4.0) for s in (-8, 0, 8))
        hr = max(self.w.h(x + f[0] * s + r[0] * 4.0, z + f[1] * s + r[1] * 4.0) for s in (-8, 0, 8))
        return y0, nick, math.atan2(hl - hr, 8.0)

    def lage(self):
        self.y0, self.nick, self.roll = self.auflage(self.x, self.z, self.psi)

    def stoss(self, x, z, psi):
        """Welches Hindernis der Rumpf an dieser Stelle beruehrt (oder None)."""
        f = (math.sin(psi), math.cos(psi))
        r = (math.cos(psi), -math.sin(psi))
        for ob in self.w.hind:
            if ob.hoch < 0.5:
                continue
            if ob.art == "k":
                rx, rz = ob.cx - x, ob.cz - z
                lf, lr = rx * f[0] + rz * f[1], rx * r[0] + rz * r[1]
                cf, cr = max(-HL, min(HL, lf)), max(-4.75, min(4.75, lr))
                if (lf - cf) ** 2 + (lr - cr) ** 2 < ob.r ** 2:
                    return ob
            else:
                ecken = [(x + f[0] * a + r[0] * b, z + f[1] * a + r[1] * b) for a in (-HL, HL) for b in (-4.75, 4.75)]
                box = [(ob.x0, ob.z0), (ob.x0, ob.z1), (ob.x1, ob.z0), (ob.x1, ob.z1)]
                trennt = False
                for ax in ((1.0, 0.0), (0.0, 1.0), f, r):
                    p1 = [e[0] * ax[0] + e[1] * ax[1] for e in ecken]
                    p2 = [e[0] * ax[0] + e[1] * ax[1] for e in box]
                    if max(p1) < min(p2) or max(p2) < min(p1):
                        trennt = True
                        break
                if not trennt:
                    return ob
        return None

    def schritt(self, links, rechts, dt=DT):
        links, rechts = max(-1.0, min(1.0, links)), max(-1.0, min(1.0, rechts))
        thr, dif = (links + rechts) / 2, (links - rechts) / 2
        v = self.v
        kraft = min(4.0, 24.0 / max(abs(v), 1.0)) * thr - 9.81 * math.sin(self.nick)
        if abs(v) > 0.05:
            a = kraft - 0.14 * v - 0.3 * math.copysign(1, v)
            nv = v + a * dt
            if nv * v < 0 and abs(kraft) < 0.3:
                nv = 0.0
        else:
            nv = 0.0 if abs(kraft) < 0.3 else v + (kraft - 0.3 * math.copysign(1, kraft)) * dt
        self.om += (0.4 * dif - self.om) * dt / 0.4
        npsi = self.psi + self.om * dt
        nx = self.x + nv * math.sin(npsi) * dt
        nz = self.z + nv * math.cos(npsi) * dt
        ob = self.stoss(nx, nz, npsi)
        frei = ob is None
        if frei:
            y0, nick, roll = self.auflage(nx, nz, npsi)
            if nick > 0.66 and nick > self.nick + 0.005:      # zu steil / Wand im Gelaende: geht nicht hinauf
                frei = False
        self.frei += 1
        if frei:
            self.x, self.z, self.psi, self.v = nx, nz, npsi, nv
            self.y0, self.nick, self.roll = y0, nick, roll
            self.blockiert = False
            if nick < -0.6:
                self.abgestuerzt = True
        else:
            if self.frei > 60:
                if ob is None or ob.hoch >= 2:
                    self.stoesse += 1
                else:
                    self.flach += 1
            self.frei = 0
            self.blockiert = True
            self.v = 0.0
            if not self.stoss(self.x, self.z, npsi):
                self.psi = npsi
                self.lage()
            else:
                self.om = 0.0

    def basis(self):
        p, r, s = self.nick, self.roll, self.psi
        f = (math.sin(s) * math.cos(p), math.sin(p), math.cos(s) * math.cos(p))
        rt = (math.cos(s) * math.cos(r), -math.sin(r), -math.sin(s) * math.cos(r))
        return f, rt, _kreuz(f, rt)

    def laser(self):
        f, rt, up = self.basis()
        o0 = (self.x, self.y0, self.z)
        aus = {}
        for k, (vo, re_, ho, ri) in LASER.items():
            o = tuple(o0[i] + f[i] * vo + rt[i] * re_ + up[i] * ho for i in range(3))
            d = {"f": f, "h": tuple(-c for c in f), "r": rt, "l": tuple(-c for c in rt), "u": tuple(-c for c in up)}[ri]
            aus[k] = self.w.strahl(o, d)
        return aus

    def physik(self):
        hd = self.psi / (2 * math.pi)
        kompass = ((-hd) + 0.5) % 1 - 0.5
        # Kanal 8 absichtlich mit falschem Vorzeichen: die KI rechnet ihr Tempo selbst aus der Ortsaenderung
        # Roll wie im Spiel: rechte Seite tief = negativ (Flossen des Schiffs), daher 'Roll Richtung' -1
        return {1: self.x, 2: self.y0 + SENSOR_H, 3: self.z, 4: kompass, 5: self.nick / (2 * math.pi),
                6: -self.roll / (2 * math.pi), 7: abs(self.v), 8: -self.v}

    def boden(self, s):
        """Boden in s m vor der Mitte (Wasser, wenn < 0)."""
        return self.w.h(self.x + math.sin(self.psi) * s, self.z + math.cos(self.psi) * s)


# ---------------------------------------------------------------------------------------------------------------
# Simulation: KI-Chip + Panzer
# ---------------------------------------------------------------------------------------------------------------
class Sim:
    def __init__(self, welt, x=0.0, z=0.0, kurs=0.0, props=None, ki=True, rad=(1, -1), seed=1):
        """rad: wie die Antriebe eingebaut sind (Ausgang mal rad = Vortrieb der Seite); rechts gespiegelt = -1."""
        pr = dict(PR_FAHREN)
        pr.update(props or {})
        self.pr = pr
        self.chip = Chip(minify(quelle("ki_fahren.lua")), pr, seed)
        self.pz = Panzer(welt, x, z, kurs)
        self.welt = welt
        self.ki, self.sitz, self.ws, self.ad, self.heim = ki, False, 0.0, 0.0, False
        self.rad = rad
        self.batterie = 1.0
        self.ziel = None
        self.ereignisse = []
        self.t = 0
        self.log = []
        self.weg = 0.0
        self.erreicht = []          # (Zeit s, Ziel Ost, Ziel Nord)
        self.zustaende = set()

    def tippe(self, x, z):
        self.ereignisse.append(("t", x, z))

    def befehl(self, c):
        self.ereignisse.append(("b", c))

    def tick(self):
        ch, pz = self.chip, self.pz
        n, b = ch.n, ch.b
        b[3] = b[5] = False
        if self.ereignisse and self.t % 2 == 0:
            e = self.ereignisse.pop(0)
            if e[0] == "t":
                n[23], n[24], b[3] = e[1], e[2], True
            else:
                n[25], b[5] = e[1], True
        for k, v in pz.physik().items():
            n[k] = v
        for k, v in pz.laser().items():
            n[k] = v
        n[16], n[17], n[18] = self.batterie, self.ad, self.ws
        b[1], b[2], b[6] = self.ki, self.sitz, self.heim
        if self.ziel:
            n[20], n[21], n[22], b[4] = self.ziel[0], self.ziel[1], 20.0, True
        else:
            b[4] = False
        ch.tick()
        if self.rad == (1, -1) and (ch.ob[5] or ch.ob[6]):
            FALSCH_GELERNT.add(self.welt.name or "?")
        x0, z0 = pz.x, pz.z
        pz.schritt(*self.seiten())
        self.weg += math.hypot(pz.x - x0, pz.z - z0)
        zs = int(round(ch.on[3]))
        self.zustaende.add(zs)
        if ch.ob[4]:
            self.erreicht.append((self.t / 60, ch.on[4], ch.on[5]))
        self.log.append((self.t, pz.x, pz.z, zs, int(round(ch.on[11])), pz.v, ch.on[1], ch.on[2], pz.boden(0),
                         pz.boden(HL), round(ch.on[4]), round(ch.on[5])))
        self.t += 1

    def lauf(self, sek, bis=None):
        for _ in range(int(sek * 60)):
            self.tick()
            if bis and bis(self):
                return True
        return False

    def seiten(self):
        """Vortrieb links/rechts, wie er an den Raedern ankommt."""
        return self.chip.on[1] * self.rad[0], self.chip.on[2] * self.rad[1]

    @property
    def zs(self):
        return int(round(self.chip.on[3]))

    def kursfehler(self, x, z):
        """Winkel (Grad) zwischen eigenem Kurs und der Richtung zu (x, z)."""
        soll = math.degrees(math.atan2(x - self.pz.x, z - self.pz.z))
        return (soll - math.degrees(self.pz.psi) + 180) % 360 - 180


# ---------------------------------------------------------------------------------------------------------------
# Pruefungen
# ---------------------------------------------------------------------------------------------------------------
ERGEBNIS = []
FALSCH_GELERNT = set()      # Szenarien, in denen ein richtig eingebauter Panzer umgelernt wurde


def pruefe(text, ok):
    ERGEBNIS.append(ok)
    print("%s %s" % ("OK    " if ok else "FEHLER", text))
    return ok


def still(log, fenster, weniger):
    """Wie oft (Fenster alle 10 s) die gefahrene Strecke in 'fenster' Ticks kleiner als 'weniger' m war."""
    weg = [0.0]
    for a, b in zip(log, log[1:]):
        weg.append(weg[-1] + math.hypot(b[1] - a[1], b[2] - a[2]))
    return sum(1 for i in range(0, len(log) - fenster, 600) if weg[i + fenster] - weg[i] < weniger)


def nah(e, x, z, r):
    return math.hypot(e[1] - x, e[2] - z) < r


def test_wegpunkte():
    s = Sim(eben())
    wp = [(0, 200), (150, 300), (-100, 350)]
    for p in wp:
        s.tippe(*p)
    s.lauf(240, bis=lambda s: len(s.erreicht) >= 3)
    rr = s.pr["Ziel Radius m"] + 2
    reihe = [next((k + 1 for k, p in enumerate(wp) if nah(e, p[0], p[1], 1)), 0) for e in s.erreicht[:3]]
    ok = reihe == [1, 2, 3] and all(math.hypot(s.log[int(e[0] * 60)][1] - e[1], s.log[int(e[0] * 60)][2] - e[2]) < rr
                                    for e in s.erreicht[:3]) and s.pz.stoesse == 0
    pruefe("3 Wegpunkte auf freier Flaeche der Reihe nach: erreicht %s nach %s s, Stoesse %d" % (
        reihe, [round(e[0]) for e in s.erreicht[:3]], s.pz.stoesse), ok)


def test_wand():
    s = Sim(Welt(hind=[("b", -50, 100, 50, 103, 10)], name="Wand"))
    s.tippe(0, 230)
    s.lauf(240, bis=lambda s: len(s.erreicht) >= 1)
    ok = len(s.erreicht) >= 1 and s.pz.stoesse == 0 and (4 in s.zustaende or 5 in s.zustaende)
    pruefe("Wand (100 m breit) zwischen Start und Wegpunkt: erreicht nach %s s, Stoesse %d, Zustaende %s" % (
        round(s.erreicht[0][0]) if s.erreicht else "-", s.pz.stoesse, sorted(s.zustaende)), ok)


def test_sackgasse():
    # U offen nach Sueden, innen 22 m breit (zu eng zum Drehen auf der Stelle), 45 m tief
    u = [("b", -14, 140, 14, 143, 10), ("b", -14, 95, -11, 143, 10), ("b", 11, 95, 14, 143, 10)]
    s = Sim(Welt(hind=u, name="Sackgasse"))
    s.tippe(0, 270)
    s.lauf(420, bis=lambda s: len(s.erreicht) >= 1)
    drin = max(z for _, x, z, *_ in s.log if abs(x) < 11 and z < 140) + HL
    ok = len(s.erreicht) >= 1 and 5 in s.zustaende
    pruefe("Sackgasse (U, 22 m breit, Boden bei Nord 140): Bug hinein bis Nord %.0f, rueckwaerts heraus (Zustand 5: %s), Wegpunkt dahinter "
           "erreicht nach %s s, Stoesse %d" % (drin, 5 in s.zustaende,
                                               round(s.erreicht[0][0]) if s.erreicht else "-", s.pz.stoesse), ok)


def see():
    # runder See um (0, 330): Grund -5 m innen (r < 110), Strand bis r = 230 (dort 20 m); Wasserlinie bei r = 134
    def h(x, z):
        r = math.hypot(x, z - 330)
        return 20.0 if r >= 230 else -5.0 if r <= 110 else -5.0 + 25.0 * (r - 110) / 120
    return Welt(h, 20.0, name="See")


def test_see():
    s = Sim(see())
    s.tippe(0, 330)          # mitten im See
    s.tippe(-150, 80)        # an Land
    nass = []

    def bis(s):
        if s.pz.boden(0) < 0 or s.pz.boden(HL) < -1.5:
            nass.append(s.t)
        return any(nah(e, -150, 80, 1) for e in s.erreicht)
    s.lauf(400, bis)
    see1 = any(nah(e, 0, 330, 1) for e in s.erreicht)
    nahe = min(math.hypot(x, z - 330) for _, x, z, *_ in s.log)
    ok = not nass and not see1 and any(nah(e, -150, 80, 1) for e in s.erreicht)
    pruefe("Wegpunkt im See: nie ins Wasser (Mitte min. %.0f m vom Seemittelpunkt, Wasserlinie 134 m), "
           "Seepunkt uebersprungen, Landpunkt erreicht nach %s s, Zustaende %s" % (
               nahe, next((round(e[0]) for e in s.erreicht if nah(e, -150, 80, 1)), "-"), sorted(s.zustaende)), ok)


def test_klippe():
    # Hochebene 20 m bis Nord 150, dann senkrecht 15 m hinunter
    s = Sim(Welt(lambda x, z: 20.0 if z < 150 else 5.0, 20.0, name="Klippe"))
    s.tippe(0, 260)          # unter der Klippe
    s.tippe(120, 40)         # oben
    s.lauf(400, bis=lambda s: any(nah(e, 120, 40, 1) for e in s.erreicht) or s.pz.abgestuerzt)
    vorn = max(z for _, x, z, *_ in s.log) + HL
    ok = not s.pz.abgestuerzt and any(nah(e, 120, 40, 1) for e in s.erreicht)
    pruefe("Klippe (15 m senkrecht): nicht abgestuerzt (%s), Bug hoechstens bis Nord %.0f (Kante 150), "
           "oberer Punkt erreicht, Zustaende %s" % (not s.pz.abgestuerzt, vorn, sorted(s.zustaende)), ok)


def test_huegel():
    # Huegel bei (0, 160), 22 m hoch, steilste Stelle ca. 15 Grad: drueber, nicht aussen herum
    def h(x, z):
        return 20.0 + 22.0 * math.exp(-(x * x + (z - 160) ** 2) / 70.0 ** 2)
    s = Sim(Welt(h, 42.0, name="Huegel"))
    s.tippe(0, 320)
    s.lauf(240, bis=lambda s: len(s.erreicht) >= 1)
    hoch = max(s.pz.w.h(x, z) for _, x, z, *_ in s.log)
    seit = max(abs(x) for _, x, z, *_ in s.log)
    ok = len(s.erreicht) >= 1 and hoch > 35 and s.pz.stoesse == 0
    pruefe("sanfter Huegel (15 Grad) im Weg: drueber gefahren (hoechster Boden %.0f m, seitlich max %.0f m), "
           "erreicht nach %s s" % (hoch, seit, round(s.erreicht[0][0]) if s.erreicht else "-"), ok)


def test_revier():
    fels = [("k", 60, 80, 8, 6), ("b", -90, -40, -60, -20, 10), ("k", -40, 120, 6, 6)]
    s = Sim(Welt(hind=fels, name="Revier"), props={"Revier m": 200, "Patrouille Pause s": 0})
    s.lauf(300)
    weit = max(math.hypot(x, z) for _, x, z, *_ in s.log)
    steh = still(s.log, 1800, 5)
    ok = weit <= 200 + 30 and s.weg > 600 and len(s.erreicht) >= 2 and s.pz.stoesse == 0 and steh == 0 \
        and 3 in s.zustaende
    pruefe("Revier 200 m ohne Wegpunkte, 5 min: hoechstens %.0f m von der Heimat, %.0f m gefahren, %d Revier-Punkte "
           "erreicht, %d mal 30 s fast still, Stoesse %d" % (weit, s.weg, len(s.erreicht), steh, s.pz.stoesse), ok)


def test_bodenlaser():
    s = Sim(eben(), ki=False)
    s.lauf(3)
    s.ki = True
    s.tippe(0, 300)
    s.lauf(5)
    auto = s.chip.g.BH
    s2 = Sim(eben(), props={"Boden Laser Hoehe m": 1.2})
    s2.lauf(1)
    pruefe("Bug-Laser-Grundwert: Automatik lernt im Stand %.2f m (Laser %.2f m ueber dem Boden), Property 1.2 gilt (%.2f)"
           % (auto, BUG_H, s2.chip.g.BH), abs(auto - BUG_H) < 0.02 and abs(s2.chip.g.BH - 1.2) < 1e-9)


def test_hand():
    s = Sim(eben())
    s.tippe(0, 800)
    s.lauf(10)
    vorher = s.zs
    s.sitz, s.ws, s.ad = True, 1.0, 0.5
    s.lauf(1.5)
    hand = (s.zs,) + tuple(round(v, 2) for v in s.seiten())
    roh = (round(s.chip.on[29], 2), round(s.chip.on[30], 2))
    s.lauf(1.5)
    s.ws, s.ad = 0.0, 0.0
    s.lauf(1.5)
    pause = (s.zs,) + tuple(round(v, 2) for v in s.seiten()) + (s.chip.ob[2],)
    s.lauf(1.5)
    weiter = s.zs
    s.lauf(3)
    ok = vorher == 2 and hand == (1, 1.0, 0.5) and roh == (0.5, 1.0) and pause[0] == 1 and abs(pause[1]) < .01 and abs(pause[2]) < .01 \
        and not pause[3] and weiter == 2 and s.pz.v > 2
    pruefe("Hand-Uebernahme: KI faehrt (Zustand %d), W+D: Zustand/links/rechts %s, Roh Lenken/Fahren %s, losgelassen "
           "(1,5 s): %s, nach 3 s Zustand %d, Tempo %.1f m/s" % (vorher, hand, roh, pause[:3], weiter, s.pz.v), ok)


def test_aus():
    s = Sim(eben(), ki=False)
    s.tippe(0, 300)
    s.lauf(20)
    still = math.hypot(s.pz.x, s.pz.z) < 0.5 and s.chip.on[1] == 0 and s.chip.on[2] == 0 and s.zs == 0
    s.sitz, s.ws = True, 1.0
    s.lauf(5)
    hand = s.zs == 1 and s.pz.v > 1
    pruefe("KI aus: 20 s keine Bewegung (Ort %.2f m, Zustand 0); mit W am Sitz faehrt er doch (Tempo %.1f m/s)" % (
        math.hypot(s.log[1199][1], s.log[1199][2]), s.pz.v), still and hand)


def test_kampf():
    s = Sim(eben())
    s.tippe(0, 1500)
    s.lauf(10)
    fahrt = s.pz.v
    s.ziel = (s.pz.x + 600, s.pz.z + 500)        # ca. 780 m rechts voraus (50 Grad)
    s.lauf(15)
    halt = (s.zs, abs(s.pz.v), s.kursfehler(*s.ziel))
    s.ziel = None
    s.lauf(4)
    noch = s.zs
    s.lauf(8)
    weiter = (s.zs, s.pz.v)
    ok1 = fahrt > 3 and halt[0] == 6 and halt[1] < 0.3 and abs(halt[2]) <= 31 and noch == 6 and weiter[0] == 2 \
        and weiter[1] > 2
    pruefe("Kampf: Ziel in 780 m -> Zustand %d, Tempo %.2f, Ziel %.0f Grad neben dem Bug; Ziel weg: nach 4 s "
           "Zustand %d, nach 12 s Zustand %d mit %.1f m/s" % (halt + (noch,) + weiter), ok1)
    # zu nah: rueckwaerts, Bug zum Ziel
    s = Sim(eben())
    s.tippe(0, 1500)
    s.lauf(8)
    s.ziel = (s.pz.x + 20, s.pz.z + 100)
    d0 = math.hypot(s.ziel[0] - s.pz.x, s.ziel[1] - s.pz.z)
    s.lauf(15)
    d1 = math.hypot(s.ziel[0] - s.pz.x, s.ziel[1] - s.pz.z)
    ok2 = d1 > d0 + 10 and s.zs == 6 and abs(s.kursfehler(*s.ziel)) < 20
    pruefe("Kampf: Ziel 100 m voraus (unter Mindestabstand 150): rueckwaerts von %.0f auf %.0f m, Bug %.0f Grad "
           "neben dem Ziel" % (d0, d1, s.kursfehler(*s.ziel)), ok2)


def test_fest():
    # flacher Fels (0,8 m) - die Laser in 2 m Hoehe sehen ihn nicht, der Panzer bleibt daran haengen
    s = Sim(Welt(hind=[("k", 0, 80, 6, 0.8)], name="Fels"))
    s.tippe(0, 220)
    t_stoss = []
    s.lauf(240, bis=lambda s: (s.pz.blockiert and not t_stoss and t_stoss.append(s.t)) or len(s.erreicht) >= 1)
    t5 = next((t for t, *_r, in s.log if _r[2] == 5 and t_stoss and t >= t_stoss[0]), None)
    zurueck = any(r[5] < -0.3 for r in s.log)
    ok = bool(t_stoss) and t5 is not None and (t5 - t_stoss[0]) / 60 < 5 and zurueck and len(s.erreicht) >= 1
    pruefe("Festgefahren an flachem Fels: Stoss bei %s s, Zustand 5 nach %s s, rueckwaerts: %s, Wegpunkt dahinter "
           "erreicht nach %s s" % (round(t_stoss[0] / 60) if t_stoss else "-",
                                   round((t5 - t_stoss[0]) / 60, 1) if t5 and t_stoss else "-", zurueck,
                                   round(s.erreicht[0][0]) if s.erreicht else "-"), ok)


def test_batterie():
    s = Sim(eben())
    s.tippe(0, 1500)
    s.lauf(10)
    s.batterie = 0.05
    s.lauf(8)
    leer = (s.zs, abs(s.pz.v), s.chip.on[1], s.chip.on[2])
    s.batterie = 0.5
    s.lauf(10)
    ok = leer[0] == 7 and leer[1] < 0.3 and abs(leer[2]) < 0.15 and abs(leer[3]) < 0.15 and s.zs == 2 and s.pz.v > 2
    pruefe("Batterie 5 %%: Zustand %d, Tempo %.2f nach 8 s; wieder voll: Zustand %d, %.1f m/s" % (
        leer[0], leer[1], s.zs, s.pz.v), ok)
    s = Sim(eben())
    s.batterie = 0.25
    s.tippe(0, 1500)
    s.lauf(20)
    pruefe("Batterie 25 %%: Soll-Tempo 60 %% (%.1f m/s, gefahren %.1f m/s)" % (s.chip.on[28], s.pz.v),
           abs(s.chip.on[28] - 0.6 * s.pr["Tempo m/s"]) < 0.2 and abs(s.pz.v - 0.6 * s.pr["Tempo m/s"]) < 0.5)
    s = Sim(eben())
    s.batterie = 0.0
    s.tippe(0, 1500)
    s.lauf(15)
    pruefe("Batterie-Eingang 0 (nicht angeschlossen) = unbekannt: KI faehrt (Zustand %d, %.1f m/s)" % (s.zs, s.pz.v),
           s.zs == 2 and s.pz.v > 3)


def test_pause():
    s = Sim(eben(), props={"Revier m": 200})
    s.lauf(120, bis=lambda s: len(s.erreicht) >= 1)
    t0 = s.t
    halt = []
    s.lauf(60, bis=lambda s: halt.append((s.zs, s.chip.on[1], s.chip.on[2], abs(s.pz.v))) or s.zs != 9)
    dauer = (s.t - t0) / 60
    ruhig = all(z == 9 and l == 0 and r == 0 for z, l, r, _ in halt[240:-1]) and max(v for *_, v in halt[240:]) < 0.1
    s.lauf(30)
    pruefe("Patrouille: am Revier-Punkt %.1f s Pause (soll 45), bremst, dann Zustand 9, Ausgaenge 0, steht: %s; danach "
           "weiter "
           "(Zustand %d, %.1f m/s)" % (dauer, ruhig, s.zs, s.pz.v), 44 < dauer < 47 and ruhig and s.zs == 3 and s.pz.v > 2)


def test_heim():
    s = Sim(eben(), x=0, z=0)
    s.tippe(200, 300)
    s.lauf(40)
    weg = math.hypot(s.pz.x, s.pz.z)
    s.heim = True
    s.lauf(120, bis=lambda s: s.zs == 9 and abs(s.pz.v) < 0.2)
    heim = (s.zs, math.hypot(s.pz.x, s.pz.z), s.pz.v)
    s.lauf(10)
    bleibt = s.zs == 9 and math.hypot(s.pz.x, s.pz.z) < s.pr["Ziel Radius m"] + 5
    s.heim = False
    s.lauf(25)
    ok = weg > 150 and heim[0] == 9 and heim[1] < s.pr["Ziel Radius m"] + 5 and bleibt and s.zs == 2 and s.pz.v > 2
    pruefe("Nach Hause: %.0f m weg -> Schalter an: zurueck, Zustand %d in %.0f m von der Heimat, bleibt dort; "
           "Schalter aus: weiter zum Wegpunkt (Zustand %d, %.1f m/s)" % (weg, heim[0], heim[1], s.zs, s.pz.v), ok)


def test_lernen():
    for rad, was, wp in (((1, 1), "rechte Seite falsch", (0, 250)), ((-1, 1), "beide falsch", (0, 250)),
                         ((-1, -1), "linke Seite falsch", (0, 250)),
                         ((1, 1), "rechte Seite falsch, Ziel hinten (erst drehen)", (30, -250))):
        s = Sim(eben(), rad=rad)
        s.tippe(*wp)
        s.lauf(120, bis=lambda s: len(s.erreicht) >= 1)
        gel = s.chip.ob[5], s.chip.ob[6]
        pruefe("Richtung lernen, %s: gelernt links/rechts %s, Wegpunkt erreicht nach %s s, Stoesse %d" % (
            was, gel, round(s.erreicht[0][0]) if s.erreicht else "-", s.pz.stoesse), len(s.erreicht) >= 1)
    s = Sim(eben(), rad=(1, 1), props={"Richtung lernen": 0})
    s.tippe(0, 250)
    s.lauf(60, bis=lambda s: len(s.erreicht) >= 1)
    s2 = Sim(eben())
    s2.tippe(0, 250)
    s2.lauf(60, bis=lambda s: len(s.erreicht) >= 1)
    pruefe("Richtung lernen aus: mit falscher Seite kein Erreichen (%s), richtig eingebaut nichts umgelernt (%s)" % (
        bool(s.erreicht), (s2.chip.ob[5], s2.chip.ob[6])), not s.erreicht and not s2.chip.ob[5] and not s2.chip.ob[6]
        and bool(s2.erreicht))


def test_karte():
    pr = dict(PR_KARTE)
    k = Chip(minify(quelle("ki_karte.lua")), pr)
    fehler = []
    try:
        k.zeichne()                                   # Bild vor dem ersten Tick
    except Exception as e:  # noqa: BLE001
        fehler.append("onDraw vor onTick: %s" % e)

    def daten(zs=2, nw=3, x=100.0, z=200.0, pm=True):
        n = k.n
        for i in range(1, 33):
            n[i] = 0.0
        n[3], n[4], n[5], n[6], n[7], n[8], n[9], n[10], n[11] = zs, 300, 400, 0.1, 50, 60, 400, nw, 2
        for i in range(8):
            n[12 + 2 * i], n[13 + 2 * i] = 100 + 50 * i, 250 + 30 * i
        n[28], n[29], n[30], n[31], n[32] = 8, x, z, 0.25, 7.5
        k.b[3] = pm

    def bild(tx=0, ty=0, an=False, ticks=1):
        tipps, befehle, zoom = [], [], None
        for _ in range(ticks):
            k.n[1], k.n[2], k.b[32] = tx, ty, an
            k.tick()
            if k.ob[3]:
                tipps.append((k.on[23], k.on[24]))
            if k.ob[5]:
                befehle.append(int(k.on[25]))
            k.zeichne()
            zoom = next((d[3] for d in k.draw if d[0] == "drawMap"), None)
        return tipps, befehle, zoom

    try:
        for gr in ((96, 96), (160, 96), (32, 32), (288, 160)):
            k.groesse = gr
            for zs, nw in ((0, 0), (2, 3), (3, 0), (6, 8), (9, 20), (8, 1), (4, -3)):
                daten(zs, nw)
                bild(ticks=2)
        k.groesse = (96, 96)
        daten()
        _, _, z0 = bild(ticks=3)
        # Tipp auf die Karte, 30 Ticks gehalten -> genau ein Wegpunkt-Puls
        t1, b1, _ = bild(40, 40, True, 30)
        t1b, _, _ = bild(ticks=5)
        t1 += t1b
        soll = screen_to_map(100.0, 200.0, z0, 96, 96, 40, 40)
        tipp_ok = len(t1) == 1 and abs(t1[0][0] - soll[0]) < 0.01 and abs(t1[0][1] - soll[1]) < 0.01 and not b1
        # Zoom: '+' (60 % Breite) halbiert, '-' (40 %) verdoppelt
        bild(ticks=2)
        bild(58, 90, True, 3)
        _, _, zp = bild(ticks=2)
        bild(38, 90, True, 3)
        bild(ticks=2)
        bild(38, 90, True, 3)
        _, _, zm = bild(ticks=2)
        zoom_ok = zp == z0 / 2 and zm == z0 * 2
        # Revier: ein Befehl 2
        _, b2, _ = bild(85, 90, True, 20)
        _, b2b, _ = bild(ticks=3)
        revier_ok = b2 + b2b == [2]
        # Loeschen: einmal = nichts, zweimal binnen 3 s = Befehl 1; nach 4 s Pause wieder nur scharf
        _, b3, _ = bild(10, 90, True, 3)
        _, b3b, _ = bild(ticks=30)
        _, b3c, _ = bild(10, 90, True, 3)
        _, b3d, _ = bild(ticks=3)
        _, b4, _ = bild(10, 90, True, 3)
        _, b4b, _ = bild(ticks=250)
        _, b4c, _ = bild(10, 90, True, 3)
        loesch_ok = b3 + b3b == [] and b3c + b3d == [1] and b4 + b4b + b4c == []
        # Knopfleiste ist kein Kartentipp
        t5, _, _ = bild(85, 90, True, 3)
    except Exception as e:  # noqa: BLE001
        fehler.append(str(e))
        tipp_ok = zoom_ok = revier_ok = loesch_ok = False
        t5 = []
    pruefe("Karte: keine Lua-Fehler (4 Bildgroessen, viele Zustaende) %s" % (fehler or ""), not fehler)
    pruefe("Karte: Tipp 30 Ticks gehalten = genau 1 Wegpunkt-Puls an der richtigen Stelle", tipp_ok)
    pruefe("Karte: Zoom +/- halbiert/verdoppelt", zoom_ok)
    pruefe("Karte: Revier-Knopf = genau 1 Befehl 2; Knoepfe setzen keinen Wegpunkt", revier_ok and not t5)
    pruefe("Karte: Loeschen erst beim 2. Tippen binnen 3 s (Befehl 1), sonst nichts", loesch_ok)

    # Karte und Fahren zusammen wie im Chip: Tipp auf der Karte -> Wegpunkt in ki_fahren
    s = Sim(eben(), ki=False)
    k.groesse = (160, 96)
    weiter = []
    for t in range(40):
        k.n[1], k.n[2], k.b[32] = (120.0, 30.0, True) if 5 <= t < 15 else (0.0, 0.0, False)
        for i in range(3, 33):
            k.n[i] = s.chip.on[i]
        k.n[29], k.n[30] = s.pz.x, s.pz.z          # wie im Chip: eigener Ort vom Physik-Sensor
        for i in range(1, 5):
            k.b[i] = s.chip.ob[i]
        k.tick()
        k.zeichne()
        s.chip.n[23], s.chip.n[24], s.chip.n[25] = k.on[23], k.on[24], k.on[25]
        s.chip.b[3], s.chip.b[5] = k.ob[3], k.ob[5]
        weiter.append(k.ob[3])
        s.ereignisse = []
        s.tick_ohne_karte = True
        _tick_verbunden(s)
    soll = screen_to_map(s.pz.x, s.pz.z, k.g.zm, 160, 96, 120, 30)
    ok = int(s.chip.on[10]) == 1 and abs(s.chip.on[12] - soll[0]) < 1 and abs(s.chip.on[13] - soll[1]) < 1
    pruefe("Karte + Fahren verbunden: Tipp -> 1 Wegpunkt in ki_fahren (%.0f/%.0f, soll %.0f/%.0f)" % (
        s.chip.on[12], s.chip.on[13], soll[0], soll[1]), ok)


def _tick_verbunden(s):
    """Wie Sim.tick, aber Karten-Eingaenge (23-25, Bool 3/5) kommen schon gesetzt von der Karte."""
    ch, pz = s.chip, s.pz
    for k, v in pz.physik().items():
        ch.n[k] = v
    for k, v in pz.laser().items():
        ch.n[k] = v
    ch.n[16] = s.batterie
    ch.b[1], ch.b[2] = s.ki, s.sitz
    ch.tick()
    pz.schritt(*s.seiten())


VERBOTEN = ("select", "print", "pcall", "xpcall", "error", "assert", "setmetatable", "getmetatable", "rawget",
            "rawset", "rawequal", "rawlen", "unpack", "load", "loadstring", "dofile", "loadfile", "require",
            "collectgarbage", "_G", "_VERSION", "os", "io", "coroutine", "utf8", "package", "atan2", "pow")


def test_groesse():
    bm = None
    if os.path.exists(os.path.join(HIER, "build_mc.py")):
        try:
            import build_mc  # noqa: E402
            bm = getattr(build_mc, "minify", None)
        except Exception as e:  # noqa: BLE001
            print("Hinweis: build_mc.py laesst sich nicht laden (%s)" % e)
    for name, props in (("ki_fahren.lua", PROPS_FAHREN), ("ki_karte.lua", PROPS_KARTE)):
        src = quelle(name)
        mini = minify(src)
        text = "%s: %d Zeichen (Quelle %d)" % (name, len(mini), len(src))
        ok = len(mini) <= GRENZE
        if bm:
            try:
                m2 = bm(src)
                text += ", build_mc.minify %d" % len(m2)
                ok = ok and len(m2) <= GRENZE
            except Exception as e:  # noqa: BLE001
                text += ", build_mc.minify Fehler: %s" % e
                ok = False
        pruefe("Groesse %s <= %d" % (text, GRENZE), ok)
        code = "".join(t for ist, t in (p for z in src.split("\n") for p in _teile(z)) if not ist)
        verb = sorted({v for v in VERBOTEN if re.search(r"(?<![\w.])%s\b|\.%s\b" % (v, v), code)
                       and not (v in ("unpack",) and "table.unpack" in code and not re.search(r"(?<![\w.])unpack", code))})
        namen = set(re.findall(r"(?:getNumber|\bP)\('([^']+)'\)", src))
        liste = {n for n, _, _ in props}
        pruefe("%s: keine Doppel-Anfuehrungszeichen, keine verbotenen Namen %s, Properties = ki_props (%d)%s" % (
            name, verb or "", len(liste), "" if namen == liste else " FEHLT: %s ZUVIEL: %s" % (namen - liste, liste - namen)),
            '"' not in mini and not verb and namen == liste)


def gemischt():
    """Ebene 20 m mit Huegel (Ost), See (West), Klippe (Sueden: unter Nord -200 nur 5 m hoch), Felsen, Haeusern."""
    def h(x, z):
        if z < -200:
            return 5.0
        r2 = (x - 250) ** 2 + (z - 150) ** 2
        g = 20.0 + 18.0 * math.exp(-r2 / 6400.0) if r2 < 90000 else 20.0
        r = math.hypot(x + 250, z - 200)
        if r < 190:
            g = min(g, -5.0 if r <= 90 else -5.0 + 25.0 * (r - 90) / 100)
        return g
    hind = [("k", 60, 80, 8, 6), ("b", -90, -60, -60, -30, 10), ("k", -40, 140, 6, 6), ("b", 100, -120, 160, -100, 12),
            ("k", 0, -60, 4, 0.8), ("k", 150, 300, 10, 8), ("b", -20, 250, 40, 254, 10)]
    return Welt(h, 38.0, hind, name="gemischt")


def test_dauerlauf():
    for seed in (1, 2, 3, 4):
        dauerlauf(seed)


def dauerlauf(seed):
    s = Sim(gemischt(), props={"Revier m": 400, "Patrouille Pause s": 0}, seed=seed)
    nass, tief = [], []

    def bis(s):
        if s.pz.boden(0) < 0 or s.pz.boden(HL) < -1.5:
            nass.append(s.t)
        return s.pz.abgestuerzt
    s.lauf(600, bis)
    steh = still(s.log, 3600, 10)
    weit = max(math.hypot(x, z) for _, x, z, *_ in s.log)
    ziele = sum(1 for a, b in zip(s.log, s.log[1:]) if a[10:] != b[10:])
    ok = not nass and not s.pz.abgestuerzt and s.pz.stoesse <= 2 and s.weg > 2000 and len(s.erreicht) >= 3 \
        and ziele >= 6 and steh == 0
    pruefe("Dauerlauf %d: 10 min Revier 400 m (Huegel, See, Klippe, Felsen, Haeuser, flacher Fels): %.0f m gefahren, "
           "%d Punkte erreicht, %d Zielwechsel (unerreichbare uebersprungen), flacher Fels %d mal, "
           "nass %d Ticks, abgestuerzt %s, Stoesse %d, max %.0f m von der Heimat, %d mal 60 s fast still, "
           "Zustaende %s" % (seed, s.weg, len(s.erreicht), ziele, s.pz.flach, len(nass), s.pz.abgestuerzt, s.pz.stoesse, weit, steh,
                             sorted(s.zustaende)), ok)


def test_nie_falsch_gelernt():
    pruefe("Richtung lernen: in keinem Szenario mit richtig eingebautem Panzer umgelernt %s" % (
        sorted(FALSCH_GELERNT) or ""), not FALSCH_GELERNT)


def test_grosse_raeder():
    """Andre waehlt die Raeder erst im Spiel: mit 12er-Raedern steht der Panzer 0,6 m hoeher. Mit den Standard-
    Eigenschaften (Hoehen 0 = Automatik aus dem Bug-Laser) muss die KI genauso Wand, Huegel, Klippe und See schaffen."""
    global LASER, SENSOR_H, BUG_H
    alt = (LASER, SENSOR_H, BUG_H)
    hub = 0.6
    LASER = {k: (v, r, h + hub, ri) for k, (v, r, h, ri) in LASER.items()}
    SENSOR_H, BUG_H = SENSOR_H + hub, BUG_H + hub
    try:
        s = Sim(eben())
        s.tippe(0, 300)
        s.lauf(15)
        g = s.chip.g
        pruefe("grosse Raeder (+0,6 m): Automatik lernt Bug %.2f, Front-Laser %.2f (echt %.2f), Sensor %.2f (echt %.2f)"
               % (g.BH, g.LH, LASER[10][2], g.SH, SENSOR_H),
               abs(g.LH - LASER[10][2]) < 0.1 and abs(g.SH - SENSOR_H) < 0.1)
        for t in (test_wand, test_huegel, test_klippe, test_see):
            t()
    finally:
        LASER, SENSOR_H, BUG_H = alt


TESTS = [test_groesse, test_karte, test_aus, test_bodenlaser, test_hand, test_batterie, test_pause, test_heim, test_lernen, test_kampf,
         test_wegpunkte, test_wand,
         test_huegel, test_fest, test_sackgasse, test_see, test_klippe, test_revier, test_dauerlauf,
         test_nie_falsch_gelernt, test_grosse_raeder]

if __name__ == "__main__":
    wahl = sys.argv[1:]
    for t in TESTS:
        if wahl and not any(w in t.__name__ for w in wahl):
            continue
        t0 = time.time()
        try:
            t()
        except Exception as e:  # noqa: BLE001
            pruefe("%s: Abbruch %s: %s" % (t.__name__, type(e).__name__, e), False)
        if os.environ.get("ZEIT"):
            print("   (%.1f s)" % (time.time() - t0))
    print("ALLES OK" if ERGEBNIS and all(ERGEBNIS) else "FEHLER: %d von %d" % (ERGEBNIS.count(False), len(ERGEBNIS)))
