"""Kleiner Simulator fuer Microcontroller aus build_mc.MC (wie das Spiel sie je Tick ausrechnet), zum Pruefen der
Verdrahtung im Chip: Composite lesen (29 An/Aus, 31 Zahl), Composite schreiben (40 Zahl, 41 An/Aus), Eigenschaften
(34) und Lua-Skripte (56, mit lupa). Video wird nicht nachgebildet (onDraw laeuft nicht).
Kreise im Chip (z. B. KI_KARTE -> KI_FAHREN) bekommen den Wert vom letzten Tick, wie im Spiel.

    sim = ChipSim(mc)
    aus = sim.tick({"Physik-Sensor": ({1: x, ...}, {}), "Laser vorn Mitte": 25.0, ...})
    aus["Links"], aus["Wahl"] -> Zahl bzw. (Zahlen, An/Aus)
"""
from lupa import lua53

LEER = ({}, {})


class ChipSim:
    def __init__(self, mc):
        self.mc = mc
        self.comps = {c[1]: c for c in mc.comps}
        self.bridges = {b[1]: b for b in mc.bridges}
        self.props = {}
        for typ, cid, pos, ins, attrs, extra in mc.comps:
            if typ == 34:
                import re
                v = re.search(r'value="([^"]*)"', extra) or re.search(r'text="([^"]*)"', extra)
                self.props[attrs["n"]] = float(v.group(1)) if v else 0.0
        self.lua = {}
        for typ, cid, pos, ins, attrs, extra in mc.comps:
            if typ == 56:
                self.lua[cid] = self._lade(attrs["script"])
        self.alt = {}
        self.neu = {}
        self.knoten = {e[1]: e for e in mc.nodes + mc.late}          # Label -> Eintrag

    def _lade(self, src):
        rt = lua53.LuaRuntime(unpack_returned_tuples=True)
        g = rt.globals()
        io = {"n": {}, "b": {}, "on": {}, "ob": {}}
        rt.execute("input={} output={} property={} screen={} map={} async={} debug={}")
        g.input.getNumber = lambda i: float(io["n"].get(i, 0.0))
        g.input.getBool = lambda i: bool(io["b"].get(i, False))
        g.output.setNumber = lambda i, v: io["on"].__setitem__(i, float(v))
        g.output.setBool = lambda i, v: io["ob"].__setitem__(i, bool(v))
        g.property.getNumber = lambda s: self.props[s]
        g.property.getBool = lambda s: bool(self.props[s])
        g.debug.log = lambda s: None
        # Bildschirm und Karte fuer onDraw (Monitor 96 x 96; Zoom = km ueber die Bildbreite, wie im Spiel)
        for f in ("setColor", "drawClear", "drawText", "drawTextBox", "drawLine", "drawRect", "drawRectF", "drawCircle",
                  "drawCircleF", "drawTriangle", "drawTriangleF", "drawMap", "setMapColorOcean", "setMapColorShallows",
                  "setMapColorLand", "setMapColorGrass", "setMapColorSand", "setMapColorSnow", "setMapColorRock",
                  "setMapColorGravel"):
            setattr(g.screen, f, lambda *a: None)
        g.screen.getWidth = lambda: 96
        g.screen.getHeight = lambda: 96

        def s2m(mx, my, zoom, w, h, px, py):
            k = zoom * 1000 / w
            return mx + (px - w / 2) * k, my - (py - h / 2) * k

        def m2s(mx, my, zoom, w, h, wx, wy):
            k = zoom * 1000 / w
            return w / 2 + (wx - mx) / k, h / 2 - (wy - my) / k
        g.map.screenToMap = s2m
        g.map.mapToScreen = m2s
        g["async"].httpGet = lambda p, s: None
        rt.execute(src)
        return g, io

    def _wert(self, cid, nr=0):
        key = (cid, nr)
        if key in self.neu:
            return self.neu[key]
        if key in self.rechnet:                                        # Kreis: Wert vom letzten Tick
            if key in self.alt:
                return self.alt[key]
            typ = self.comps[cid][0] if cid in self.comps else self.bridges[cid][0]
            return LEER if typ in (40, 41, 56, 4, 5) else (False if typ in (29, 0, 1) else 0.0)
        self.rechnet.add(key)
        if cid in self.bridges:
            btyp, _, pos, ins = self.bridges[cid]
            if btyp % 2 == 0:                                          # Eingang
                v = self.eingang.get(self.bruecke_label[cid], LEER if btyp == 4 else 0.0 if btyp == 2 else False)
            else:
                v = self._quelle(ins[0]) if ins else None
        else:
            v = self._comp(cid, nr)
        self.neu[key] = v
        return v

    def _quelle(self, e):
        q, nr = e
        return self._wert(q, nr)

    def _comp(self, cid, nr):
        typ, _, pos, ins, attrs, extra = self.comps[cid]
        normal = [e for e in ins if e[0] != "inc"]
        inc = [e[1] for e in ins if e[0] == "inc"]
        if typ in (29, 31):
            c = self._quelle(normal[0]) if normal else LEER
            i = int(attrs.get("i", 0)) + 1
            return (c[0].get(i, 0.0) if typ == 31 else c[1].get(i, False))
        if typ in (40, 41):
            c = self._quelle(inc[0]) if inc else LEER
            nums, bools = dict(c[0]), dict(c[1])
            off = int(attrs.get("offset", 0))
            for k, e in enumerate(normal[:int(attrs.get("count", 1))]):
                v = self._quelle(e)
                if typ == 40:
                    nums[off + k + 1] = float(v or 0.0)
                else:
                    bools[off + k + 1] = bool(v)
            return (nums, bools)
        if typ == 56:
            c = self._quelle(normal[0]) if normal else LEER
            g, io = self.lua[cid]
            if cid not in self.lauf:
                self.lauf.add(cid)
                io["n"], io["b"], io["on"], io["ob"] = c[0], c[1], {}, {}
                if g.onTick:
                    g.onTick()
                self.lua_aus[cid] = (dict(io["on"]), dict(io["ob"]))
            return self.lua_aus[cid] if nr == 0 else None
        if typ == 34:
            return self.props[attrs["n"]]
        return None

    def tick(self, eingang):
        self.eingang = eingang
        self.bruecke_label = {e[7]: e[1] for e in self.mc.nodes + self.mc.late}
        self.neu, self.rechnet, self.lauf, self.lua_aus = {}, set(), set(), {}
        # alle Lua-Bloecke einmal je Tick rechnen (auch ohne Ausgang), dann alle Ausgaenge
        for cid in self.lua:
            self._wert(cid, 0)
        out = {}
        for e in self.mc.nodes + self.mc.late:
            label, mode, cid = e[1], e[2], e[7]
            if not mode:
                out[label] = self._wert(cid)
        self.alt = dict(self.neu)
        # onDraw aller Skripte (im Spiel nur mit angeschlossenem Bildschirm - hier immer)
        for cid, (g, io) in self.lua.items():
            if g.onDraw:
                g.onDraw()
        return out
