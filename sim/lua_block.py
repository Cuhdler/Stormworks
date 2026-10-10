"""Lua-Baustein (Typ 56) fuer den Simulator: eigenes Lua 5.3 je Skript (lupa), Stormworks-Befehle nachgebaut.

- input.getNumber/getBool lesen das Eingangs-Composite, output.setNumber/setBool schreiben das Ausgangs-Composite.
- property.getNumber/getBool/getText lesen die Eigenschafts-Bausteine des Chips (34, 19, 20 / 33 / 58).
- screen.* zeichnet nur in onDraw: jeder Aufruf wird als (Name, Werte) mitgeschrieben.
- async.httpGet wird mitgeschrieben (kein Netz); die Antwort kommt nur, wenn das Szenario eine Antwort-Funktion hat.
- Fehlende Lua-Befehle wie im Spiel (wissen/microcontroller/lua.md): Aufruf = Absturz des Skripts.
- Ein Laufzeitfehler stoppt das Skript (wie im Spiel); der Fehler steht danach in .fehler.
"""
try:
    from lupa.lua53 import LuaRuntime
except ImportError as _e:
    raise ImportError("Der Simulator braucht lupa (Lua 5.3 fuer Python): pip install lupa") from _e

# wie tools/test_schiff.py (im Spiel gemessen 05.10., wissen/microcontroller/lua.md)
NICHT_IM_SPIEL = ("select", "unpack", "load", "loadstring", "dofile", "loadfile", "require", "rawget", "rawset",
                  "rawequal", "rawlen", "setmetatable", "getmetatable", "coroutine", "os", "io", "utf8", "package",
                  "print", "pcall", "xpcall", "error", "assert", "collectgarbage", "_G", "_VERSION")
MATH_FEHLT = ("atan2", "pow", "log10", "cosh", "sinh", "tanh", "frexp", "ldexp")
SCREEN = ("setColor", "drawClear", "drawText", "drawTextBox", "drawLine", "drawRect", "drawRectF", "drawCircle",
          "drawCircleF", "drawTriangle", "drawTriangleF", "drawMap", "setMapColorOcean", "setMapColorShallows",
          "setMapColorLand", "setMapColorGrass", "setMapColorSand", "setMapColorSnow", "setMapColorRock",
          "setMapColorGravel")


class Draw202(Exception):
    """Eingang in onDraw gelesen: im Spiel bricht das Bild mit 'draw error 202' ab [G]."""


def _kanal(i):
    try:
        k = int(i)
    except (TypeError, ValueError):
        return None
    return k if 1 <= k <= 32 and k == i else None


class LuaBlock:
    """Ein Lua-Skript in einem Chip. ort = Text fuer Meldungen (Chip-Name und Baustein-Nummer)."""

    def __init__(self, skript, eigenschaften, ort, f32=None, halten=True, http=None):
        self.ort, self.f32, self.halten = ort, f32 or (lambda v: v), halten
        self.eig = eigenschaften          # {"zahl": {...}, "an": {...}, "text": {...}}
        self.http = http                  # Liste fuer Anfragen (gemeinsam fuer das ganze Fahrzeug) oder None
        self.ein_n, self.ein_b = [0.0] * 32, [False] * 32
        self.aus_n, self.aus_b = [0.0] * 32, [False] * 32
        self.fehler, self.hinweise, self.log = None, [], []
        self.im_draw, self.zeichnung, self.groesse = False, [], (96, 96)
        self.rt = LuaRuntime(unpack_returned_tuples=True)
        self._umgebung()
        try:
            self.rt.execute(skript)
        except Exception as e:                # noqa: BLE001
            self._absturz("beim Laden", e)
        g = self.rt.globals()
        self.on_tick, self.on_draw, self.http_reply = g.onTick, g.onDraw, g.httpReply

    # ---- Stormworks-Befehle ----------------------------------------------------------------------------------------

    def _hinweis(self, text):
        if text not in self.hinweise:
            self.hinweise.append(text)

    def _umgebung(self):
        rt, g = self.rt, self.rt.globals()
        for n in NICHT_IM_SPIEL:
            g[n] = None
        for n in MATH_FEHLT:
            g.math[n] = None

        def get_n(i):
            if self.im_draw:
                self._hinweis("Eingang in onDraw gelesen (im Spiel 'draw error 202')")
                raise Draw202("draw error 202: input.getNumber in onDraw")
            k = _kanal(i)
            if k is None:
                self._hinweis("input.getNumber(%r): Kanal gibt es nicht (1-32)" % (i,))
                return 0.0
            return float(self.ein_n[k - 1])

        def get_b(i):
            if self.im_draw:
                self._hinweis("Eingang in onDraw gelesen (im Spiel 'draw error 202')")
                raise Draw202("draw error 202: input.getBool in onDraw")
            k = _kanal(i)
            if k is None:
                self._hinweis("input.getBool(%r): Kanal gibt es nicht (1-32)" % (i,))
                return False
            return bool(self.ein_b[k - 1])

        def set_n(i, v):
            k = _kanal(i)
            if k is None:
                self._hinweis("output.setNumber(%r): Kanal gibt es nicht (1-32)" % (i,))
                return
            if isinstance(v, bool) or not isinstance(v, (int, float)):
                self._hinweis("output.setNumber(%d, %r): keine Zahl -> 0" % (k, v))
                v = 0.0
            self.aus_n[k - 1] = self.f32(float(v))

        def set_b(i, v):
            k = _kanal(i)
            if k is None:
                self._hinweis("output.setBool(%r): Kanal gibt es nicht (1-32)" % (i,))
                return
            if v is not None and not isinstance(v, bool):
                self._hinweis("output.setBool(%d, %r): kein true/false (in Lua ist auch 0 wahr)" % (k, v))
            self.aus_b[k - 1] = bool(v)

        def eig(art, standard):
            def f(name):
                tab = self.eig[art]
                if name not in tab:
                    self._hinweis("property-Abfrage %r: keine solche Eigenschaft im Chip" % (name,))
                    return standard
                return tab[name]
            return f

        g.input = rt.table(getNumber=get_n, getBool=get_b)
        g.output = rt.table(setNumber=set_n, setBool=set_b)
        g.property = rt.table(getNumber=eig("zahl", 0.0), getBool=eig("an", False), getText=eig("text", ""))

        def malen(name):
            def f(*a):
                if not self.im_draw:
                    self._hinweis("screen.%s ausserhalb von onDraw (zeichnet im Spiel nichts)" % name)
                    return
                self.zeichnung.append((name,) + tuple(a))
            return f
        sc = rt.table()
        for n in SCREEN:
            sc[n] = malen(n)
        sc.getWidth = lambda: self.groesse[0]
        sc.getHeight = lambda: self.groesse[1]
        g.screen = sc

        # Karte: zoom = km ueber die Bildbreite (wie landkreuzer/tools/chip_sim.py)
        def s2m(mx, my, zoom, w, h, px, py):
            k = zoom * 1000 / w
            return mx + (px - w / 2) * k, my - (py - h / 2) * k

        def m2s(mx, my, zoom, w, h, wx, wy):
            k = zoom * 1000 / w
            return w / 2 + (wx - mx) / k, h / 2 - (wy - my) / k
        g.map = rt.table(screenToMap=s2m, mapToScreen=m2s)

        def http_get(port, text):
            if self.http is None:
                self._hinweis("async.httpGet ohne Netz (Simulator schickt nichts)")
                return
            self.http.append((self, int(port), str(text)))
        g["async"] = rt.table(httpGet=http_get)
        g.debug = rt.table(log=lambda t: self.log.append(str(t)))

    # ---- Ablauf ----------------------------------------------------------------------------------------------------

    def _absturz(self, wo, e):
        text = str(e).strip().splitlines()[0] if str(e).strip() else type(e).__name__
        self.fehler = "Lua-Fehler %s in %s: %s" % (wo, self.ort, text)

    def tick(self, comp):
        """Ein Tick: Eingangs-Composite -> onTick -> (Zahlen, An/Aus) des Ausgangs."""
        self.ein_n, self.ein_b = comp.n, comp.b
        if not self.halten:
            self.aus_n, self.aus_b = [0.0] * 32, [False] * 32
        else:
            self.aus_n, self.aus_b = list(self.aus_n), list(self.aus_b)
        if self.fehler is None and self.on_tick is not None:
            try:
                self.on_tick()
            except Exception as e:            # noqa: BLE001 - Lua-Fehler oder falscher Aufruf eines Befehls
                self._absturz("in onTick", e)
        return self.aus_n, self.aus_b

    def antwort(self, port, anfrage, text):
        """httpReply(port, anfrage, antwort) aufrufen, falls das Skript es hat."""
        if self.fehler is None and self.http_reply is not None:
            try:
                self.http_reply(port, anfrage, text)
            except Exception as e:            # noqa: BLE001
                self._absturz("in httpReply", e)

    def zeichne(self, breite=96, hoehe=96):
        """onDraw einmal aufrufen; Rueckgabe: Liste der screen-Aufrufe [(Name, Werte...), ...]."""
        self.zeichnung, self.groesse = [], (breite, hoehe)
        if self.fehler is None and self.on_draw is not None:
            self.im_draw = True
            try:
                self.on_draw()
            except Draw202:
                pass                      # nur dieses Bild bricht ab (im Spiel steht 'draw error 202' auf dem Monitor)
            except Exception as e:            # noqa: BLE001
                if "draw error 202" not in str(e):
                    self._absturz("in onDraw", e)
            finally:
                self.im_draw = False
        return list(self.zeichnung)

    def texte(self, breite=96, hoehe=96):
        """Nur die Texte aus onDraw (drawText / drawTextBox), praktisch fuer Pruefungen."""
        out = []
        for z in self.zeichne(breite, hoehe):
            if z[0] == "drawText" and len(z) >= 4:
                out.append(str(z[3]))
            elif z[0] == "drawTextBox" and len(z) >= 6:
                out.append(str(z[5]))
        return out
