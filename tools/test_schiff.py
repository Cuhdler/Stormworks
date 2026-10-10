"""Prueft den Schiffs-Chip v3.3 der Figet Marena (schiff.lua + shud.lua) im Rechner, 4 Motoren mit Motormodell:
- test_motor: ein Motor im Detail - Anlassen (schwacher Anlasser), Leerlauf, Gemisch, Gas = Leistung, Temperatur-Regler,
  Notgrenze, Aus
- test_system: 4 Motoren (einer fehlt, einer mit schwachem Anlasser) - Start, Fahrhebel, Lenk-Schub, Rueckwaertsgang
  je Seite, Ruder, Bugstrahl, Stopp, Ausfall, Helm-Anzeige (gepackte Werte)
- test_gemisch: andere Luft/Treibstoff-Verhaeltnisse, Diagnose-Seite
- test_gaenge: 8 Gaenge im Schiffsmodell (Hand, Automatik hoch/runter, rueckwaerts)
- test_schreiber: Fahrtenschreiber (shud.lua -> HTTP -> logger.entpacke) lueckenlos und richtig entpackt
- test_temperatur (v3.4): Waermemodell nach der Fahrt 07.10. - gemeinsame Gas-Grenze, sanft auf 'Temp Ziel', ohne
  Schaukeln, auch mit traeger Kuehlung
- test_emotor (v3.5): E-Motoren bekommen den Rest des Hebels, Batterie-Schutz, Test-Schalter (Diesel ausgekuppelt)
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_schiff import LUA_DIR, PROPS, minify  # noqa: E402
from lupa.lua53 import LuaRuntime  # noqa: E402

PR = {n: v for n, v, _ in PROPS}


# Lua-Funktionen, die es in Stormworks nicht gibt (04.10.: 'select' lief im Pruefstand und stuerzte im Spiel ab;
# 05.10. im Spiel gemessen, wissen/microcontroller/lua.md - table.unpack gibt es, debug nur mit debug.log)
NICHT_IM_SPIEL = ("select", "unpack", "load", "loadstring", "dofile", "loadfile", "require", "rawget", "rawset",
                  "rawequal", "rawlen", "setmetatable", "getmetatable", "coroutine", "os", "io", "utf8", "package",
                  "print", "pcall", "xpcall", "error", "assert", "collectgarbage", "_G", "_VERSION")


def sperren(rt):
    g = rt.globals()
    for n in NICHT_IM_SPIEL:
        g[n] = None
    g.debug = rt.table(log=lambda *a: None)
    for n in ("atan2", "pow", "log10", "cosh", "sinh", "tanh", "frexp", "ldexp"):
        g.math[n] = None


def load(name, props):
    rt = LuaRuntime(unpack_returned_tuples=True)
    g = rt.globals()
    io = {"n": {}, "b": {}, "on": {}, "draw": [], "http": []}
    g["async"] = rt.table(httpGet=lambda port, body: io["http"].append((port, body)))
    g.input = rt.table(getNumber=lambda i: float(io["n"].get(i, 0.0)), getBool=lambda i: bool(io["b"].get(i, False)))
    g.output = rt.table(setNumber=lambda i, v: io["on"].__setitem__(i, v), setBool=lambda i, v: io["on"].__setitem__(100 + i, v))
    g.property = rt.table(getNumber=lambda s: props[s], getBool=lambda s: bool(props[s]))
    g.screen = rt.table(setColor=lambda *a: None, drawText=lambda x, y, s: io["draw"].append(s),
                        getWidth=lambda: 288, getHeight=lambda: 160)
    with open(os.path.join(LUA_DIR, name), encoding="utf-8") as f:
        src = minify(f.read(), drop_local=(name == "schiff.lua"))   # wie build_schiff
    sperren(rt)
    rt.execute(src)
    if g.onTick and name in ("flakradar.lua", "flak.lua"):
        # Antwort auf httpGet kommt im naechsten Tick (wie im Spiel bei leerer Warteschlange)
        ot, n0 = g.onTick, [0]

        def tick():
            if len(io["http"]) > n0[0] and g.httpReply:
                g.httpReply(io["http"][-1][0], io["http"][-1][1], "ok")
            n0[0] = len(io["http"])
            ot()
        g.onTick = tick
    return rt, g, io


class Motor:
    """Motormodell: der Zylinder sieht die Drosseln 5 Ticks spaeter (Luft ka*A, Treibstoff ka*F/6.88), Drehmoment aus
    dem Treibstoff, Anlasser, Reibung, Schraube ueber die Kupplung. fehlt: nichts angeschlossen (alles 0)."""

    def __init__(self, anlasser=1.5, ka=0.1, fehlt=False, zuendet=True, kreal=6.88, traeg=0, luftgrenze=0.0, waerme=None):
        self.rps, self.hist, self.anl, self.ka, self.fehlt, self.zuendet = 0.0, [(0.0, 0.0)] * 5, anlasser, ka, fehlt, zuendet
        self.tmp, self.kreal, self.sto = 60.0, kreal, 0.0
        # waerme = (Anstieg Grad/s bei Vollgas, Kuehlung je Grad ueber 20, Verzoegerung s): Waerme aus dem Treibstoff.
        # Fahrt 07.10. Gang 7 Vollgas: 15 Grad/min ab kalt, bei 95 Grad hielten im Mittel ca. 35 % Gas -> (0.27, 0.00124)
        self.wm, self.hq = waerme, 0.0
        if waerme:
            self.tmp = 20.0
        # traeg > 0: Zylinder-Inhalt folgt den Drosseln traege (Ticks, wie die 3x3-Motoren im Spiel: Fahrt 01.10.), die
        # Kraft faellt mit dem Gemisch weich ab statt hart (das Spiel lief auch bei MIX 3 und -1.3 noch, schwaecher)
        self.traeg, self.zl = traeg, (0.0, 0.0)
        # luftgrenze > 0: ueber so vielen RPS saugt der Motor je Takt weniger Luft an (Luftmenge pro Sekunde begrenzt) -
        # das Gemisch wird beim Hochdrehen fett, beim Abfallen mager (Fahrt 01.10. Gang 4)
        self.lg = luftgrenze

    def schritt(self, luft, treib, kup, anl, last=1.0):
        """Rueckgabe: RPS, Temperatur, Luft, Treibstoff im Zylinder (fuer den naechsten Tick)."""
        if self.fehlt:
            return 0.0, 0.0, 0.0, 0.0
        ad, fd = self.hist[-5]
        if self.traeg:
            ad, fd = self.zl
        # Zuendung nur bei brauchbarem Gemisch (Stoechiometrie -1..1.3); Kraft aus der verbrannten Treibstoffmenge
        T = min(max(self.tmp, 0), 100)
        self.sto = (T + 1400 - 100 * self.kreal * ad / fd) / (3 * T + 200) if fd > 1e-9 else -9
        if self.traeg:
            brennt = self.zuendet and self.rps > 0.5 and -3 < self.sto < 5
            wg = max(0.0, 1 - ((self.sto - 0.5) / 3) ** 2)
        else:
            brennt, wg = self.zuendet and self.rps > 0.5 and -1 < self.sto < 1.3, 1.0
        tq = (90 * wg * min(fd * 6.88 / self.kreal, ad * 6.88 / 12.9) if brennt else 0.0) + (self.anl * 0.4 if anl else 0.0)
        self.rps = max(0.0, self.rps + (tq - 0.4 * self.rps - last * kup * 0.03 * self.rps ** 2) / 60)
        self.hist = self.hist[1:] + [(luft, treib)]
        if self.wm:
            a, b, lag = self.wm
            self.hq += (min(treib / 0.55, 1.0) * (self.rps > 1) - self.hq) / (lag * 60)
            self.tmp += (a * self.hq - b * (self.tmp - 20)) / 60
        ad, fd = self.hist[-5]
        if self.lg:
            ad *= min(1.0, self.lg / max(self.rps, 1e-3))
        if self.traeg:
            za, zf = self.zl
            self.zl = (za + (ad - za) / self.traeg, zf + (fd - zf) / self.traeg)
            ad, fd = self.zl
        return self.rps, self.tmp, self.ka * ad, self.ka * fd / self.kreal


class Schiff:
    def __init__(self, motoren):
        _, self.g, self.io = load("schiff.lua", PR)
        _, self.hg, self.hio = load("shud.lua", PR)
        _, self.wg, self.wio = load("wellen.lua", PR)
        self.mo = motoren
        self.mess = [(0.0, 0.0, 0.0, 0.0)] * 4
        self.out = {}
        self.batt = 0.0          # v3.5: Batterie-Ladung auf Kanal 25 (ueber den Flossen-Chip); 0 = keine -> E-Motoren aus

    def wellen(self, n, b):
        """Wellen-Skript wie im Chip: liest dasselbe Composite, Gas-Abzug -> Kanal 24, Schaltsperre -> Bool 9."""
        self.wio["n"] = n
        self.wio["on"].clear()
        self.wg.onTick()
        n[24] = self.wio["on"].get(1, 0.0)
        b[9] = bool(self.wio["on"].get(101, False))

    def tick(self, ad=0.0, ws=0.0, bug=0.0, h1=False, h2=False, last=1.0, h4=False):
        n = {1: ad, 2: ws, 3: bug, 5: 8.0, 6: 0.25, 25: self.batt}
        for i, m in enumerate(self.mess):
            for j in range(4):
                n[7 + 4 * i + j] = m[j]
        b = {1: h1, 2: h2, 4: h4, 8: True}
        self.wellen(n, b)
        self.io["n"], self.io["b"] = n, b
        self.io["on"].clear()
        self.g.onTick()
        o = dict(self.io["on"])
        self.mess = [mo.schritt(o[3 * i + 1], o[3 * i + 2], o[3 * i + 3], o[102 + i], last) for i, mo in enumerate(self.mo)]
        o["rps"] = [mo.rps for mo in self.mo]
        self.out = o
        self.hio["n"] = o
        self.hio["b"] = {k - 100: v for k, v in o.items() if isinstance(k, int) and k > 100}
        self.hg.onTick()
        return o

    def helm(self):
        self.hio["draw"].clear()
        self.hg.onDraw()
        return list(self.hio["draw"])


def pruefe(checks):
    ok = True
    for name, res in checks:
        print("%-60s %s" % (name, "ok" if res else "FEHLER"))
        ok &= bool(res)
    return ok


def entpacke(o, i):
    a, b = round(o[19 + 2 * i]), round(o[20 + 2 * i])
    return {"rps": (a // 1000) / 10, "tmp": a % 1000, "z": b // 1000000, "gas": (b % 1000000) // 1000, "mix": (b % 1000) / 100 - 2}


def test_motor():
    """Ein Motor (L1) im Detail, die anderen fehlen."""
    mo = Motor()
    sch = Schiff([mo, Motor(fehlt=True), Motor(fehlt=True), Motor(fehlt=True)])
    log, rmax_frei = {}, 0.0
    for k in range(60 * 95):
        sek = k / 60
        mo.tmp = 105.0 if 45 <= sek < 60 else 60.0
        ws = 1.0 if 20 <= sek < 24 else (-1.0 if 35 <= sek < 37 else (1.0 if 62 <= sek < 64 else 0.0))
        last = 0.0 if 62 <= sek < 75 else 1.0
        o = sch.tick(ws=ws, h1=(1 <= sek < 1.05) or (85 <= sek < 85.05), last=last)
        if 62 <= sek < 75: rmax_frei = max(rmax_frei, mo.rps)
        log[round(sek, 2)] = o
    at = lambda s: log[round(s, 2)]
    fx = 7.1 / (14 + 0.6 - 2 * 0.5 - 0.03 * 60 * 0.5)    # v3.2: Q fest 7.1
    return pruefe([
        ("aus: Drosseln zu, kein Anlasser, Pumpen aus", at(0.5)[1] < 1e-6 and at(0.5)[2] < 1e-6 and at(0.5)[102] is False and at(0.5)[101] is False),
        ("an: Anlasser dreht sofort, Pumpen an", at(1.1)[102] is True and at(1.1)[101] is True),
        ("schwacher Anlasser (1.5 RPS): springt an, Anlasser aus", at(8)[102] is False and at(8)["rps"][0] > 3),
        ("Leerlauf haelt 4 RPS, ausgekuppelt", abs(at(18)["rps"][0] - 4) < 1 and at(18)[3] == 0),
        # v3.2 festes Verhaeltnis Q 7.1 (Modell-Motor 6.88): Gemisch nahe am Ziel, nicht genau
        ("Gemisch im Zylinder nahe Ziel 0.5 (Anzeige %.2f, Q fest)" % entpacke(at(18), 1)["mix"], abs(entpacke(at(18), 1)["mix"] - 0.5) < 0.15),
        ("Vollgas eingekuppelt: Treibstoff am Luft-Limit, Gas 100 %", abs(at(34)[2] - fx) < 0.01 and at(34)[1] > 0.98 and entpacke(at(34), 1)["gas"] == 100),
        ("Hebel 50 %: halbe Leistung", abs(entpacke(at(44), 1)["gas"] - 50) <= 2 and abs(at(44)[1] - 0.5) < 0.03),
        ("heiss (105): Gas unter 50 %, Anzeige TEMP", entpacke(at(59.9), 1)["gas"] < 45 and entpacke(at(59.9), 1)["z"] == 3),
        ("Schraube aus dem Wasser: hoechstens Notgrenze", rmax_frei < PR["RPS Notgrenze"] * 1.08),
        ("aus: Drosseln zu, Anlasser und Pumpen aus", at(87)[1] < 1e-6 and at(87)[2] < 1e-6 and at(87)[102] is False and at(87)[101] is False),
    ])


def test_system():
    mo = [Motor(), Motor(fehlt=True), Motor(anlasser=2.2), Motor()]     # L2 ohne Kabel, R1 staerkerer Anlasser
    sch = Schiff(mo)
    log = {}
    for k in range(60 * 70):
        sek = k / 60
        ad = -1.0 if 30 <= sek < 32 else 0.0                         # A: Linkskurve
        ws = 1.0 if 10 <= sek < 14 else (-1.0 if 40 <= sek < 46 else 0.0)
        o = sch.tick(ad=ad, ws=ws, bug=1.0 if 33 <= sek < 34 else 0.0, h1=1 <= sek < 1.05, h2=60 <= sek < 60.05)
        log[round(sek, 2)] = o
    at = lambda s: log[round(s, 2)]
    K = lambda s, i: at(s)[3 * i + 3]
    ok = pruefe([
        ("vor Hotkey 1: aus", at(0.5)[101] is False and at(0.5)[15] == 0),
        ("Hotkey 1: alle 3 Motoren laufen", all(at(8)["rps"][i] > 3 for i in (0, 2, 3))),
        ("fehlender Motor L2: Anzeige ---", entpacke(at(8), 2)["z"] == 6),
        ("laufende Motoren ausgekuppelt: Anzeige LEER", entpacke(at(8), 1)["z"] == 4 and entpacke(at(8), 4)["z"] == 4),
        ("Anzeige RPS/Temperatur entpackt richtig", abs(entpacke(at(8), 1)["rps"] - round(at(8)["rps"][0], 1)) < 0.11 and entpacke(at(8), 1)["tmp"] == 60),
        ("W 4 s: Hebel 100 %", abs(at(20)[16] - 1) < 1e-6),
        ("eingekuppelt: L1, R1, R2 ganz ein, Anzeige OK", K(25, 0) == 1 and K(25, 2) == 1 and K(25, 3) == 1 and entpacke(at(25), 1)["z"] == 0),
        ("A (links): Ruder voll (%.2f), linke Motoren %.0f %% weniger Gas, Bugstrahl %+.1f" % (at(31.9)[13], PR["Lenk-Schub"] * 100, at(31.9)[14]),
         abs(at(31.9)[13] + PR["Ruder max"]) < 1e-6 and abs(entpacke(at(31.9), 1)["gas"] - 100 * (1 - PR["Lenk-Schub"])) <= 2 and entpacke(at(31.9), 3)["gas"] >= 98
         and abs(at(31.9)[14] + PR["Bugstrahl beim Lenken"] * PR["Bugstrahl Richtung"]) < 1e-6),
        ("Ruder zurueck in %.2f s" % (PR["Ruder max"] / PR["Ruder Tempo"]), abs(at(32.05 + PR["Ruder max"] / PR["Ruder Tempo"])[13]) < 1e-6),
        ("Bugstrahlruder", at(33.5)[14] == 1),
        ("S durch null: erst auskuppeln, Gang noch vorwaerts", at(44.05)[106] is False and K(44.05, 0) == 0 and K(44.05, 3) == 0),
        ("dann Rueckwaertsgang beide Seiten", at(45)[106] is True and at(45)[107] is True),
        ("rueckwaerts wieder eingekuppelt, Hebel -50 %", K(52, 0) == 1 and K(52, 2) == 1 and abs(at(52)[16] + 0.5) < 1e-6),
        ("Hotkey 2 Stopp: Hebel 0, ausgekuppelt", at(61)[16] == 0 and K(61, 0) == 0 and K(61, 3) == 0),
    ])
    kurz = sch.helm()
    sch.tick(h4=True)
    sch.tick()
    h = sch.helm()
    print("Helm-Anzeige schmal:", kurz)
    print("Helm-Anzeige mit Hotkey 4:")
    for z in h:
        print("   ", z)
    ok &= pruefe([("Helm schmal (v2.5): eine Zeile mit Gang, Hebel, Tempo, Kurs", len(kurz) == 1 and kurz[0].startswith("G") and "KN" in kurz[0]),
                  ("Helm mit H4: 5 Zeilen + 4 Motorzeilen + Schreiber (hier ohne PC)", len(h) == 10 and h[6].startswith("L2") and h[6].endswith("---") and h[9].startswith("LOG"))])
    # Ausfall: ein Motor zuendet nie -> AUSFALL, die anderen fahren weiter
    mo = [Motor(), Motor(zuendet=False), Motor(), Motor()]
    sch = Schiff(mo)
    for k in range(60 * 30):
        sek = k / 60
        o = sch.tick(ws=1.0 if 2 <= sek < 6 else 0.0, h1=1 <= sek < 1.05)
    ok &= pruefe([("L2 zuendet nie: AUSFALL, ausgekuppelt; L1 faehrt", entpacke(o, 2)["z"] == 2 and o[6] == 0 and o[3] == 1)])
    return ok


def test_gemisch():
    """Andere Versorgung je Motor (Luft/Treibstoff-Verhaeltnis 2 bis 20 statt 6.88): springt an, regelt auf MIX 0.5,
    Q folgt dem wahren Verhaeltnis; Hotkey 4 schaltet die Helm-Anzeige auf die Gemisch-Diagnose.
    Seit v3.1 regelt das Gemisch 5-mal langsamer (gegen das Mitschaukeln): Andres Motoren (7.1) in 30 s, die extremen
    Verhaeltnisse brauchen bis 2.5 min."""
    ok = True
    # v3.2: das feste Verhaeltnis (Standard) passt zu Andres Motoren (7.1); die anderen nur mit 'Gemisch Regler'
    for kr, sek_max, gq in ((7.1, 30, 0), (7.1, 30, 2e-4), (2.0, 160, 2e-4), (4.0, 160, 2e-4), (12.0, 160, 2e-4), (20.0, 160, 2e-4)):
        mo = [Motor(kreal=kr), Motor(), Motor(fehlt=True), Motor(fehlt=True)]
        alt = PR["Gemisch Regler"]
        PR["Gemisch Regler"] = gq
        sch = Schiff(mo)
        sch.tick()
        PR["Gemisch Regler"] = alt
        for k in range(60 * sek_max):
            sek = k / 60
            o = sch.tick(ws=1.0 if 5 <= sek < 9 else 0.0, h1=1 <= sek < 1.05)
        e, q = entpacke(o, 1), round(o[29])
        ok &= pruefe([("Verhaeltnis %4.1f nach %d s (%s): laeuft, MIX %.2f, Q %.1f" % (kr, sek_max, "Regler" if gq else "fest", e["mix"], (q // 1000) / 10),
                       mo[0].rps > 10 and abs(e["mix"] - 0.5) < 0.05 and abs((q // 1000) / 10 - kr) / kr < 0.1)])
    seite1 = sch.helm()
    sch.tick(h4=True)
    sch.tick()
    seite2 = sch.helm()
    print("   Helm:", seite1)
    print("   mit Hotkey 4:", seite2[5])
    ok &= pruefe([("Hotkey 4: alle Werte (Motorzeile mit RPS und MIX)", len(seite1) <= 2 and seite2[5].startswith("L1 RPS") and "MIX" in seite2[5])])
    sch.tick(h4=True)
    sch.tick()
    ok &= pruefe([("Hotkey 4 nochmal: wieder schmal", len(sch.helm()) <= 2)])
    return ok


class SchiffG(Schiff):
    """Schiff mit 3 Getrieben je Seite: Schraube p = RPS * Uebersetzung (Bits Ausgang 9-11), Last am Motor
    ~ Uebersetzung^2 * RPS^2 * Schlupf, Schub ~ p^2 * Schlupf, Tempo aus Schub minus Wasserwiderstand."""
    KV, KF, CD, MASSE = 0.8, 0.012, 0.25, 40.0

    def __init__(self, motoren, messer=False, tempo_bricht=False):
        """messer: Heck-Messer (Tiefe, + unter Wasser) auf Kanal 23 wie ueber den Flossen-Chip; tempo_bricht: der
        Tempo-Wert faellt bei Schrauben in der Luft scheinbar auf 20 % und springt beim Eintauchen zurueck (Spiel 02.10.)."""
        super().__init__(motoren)
        self.v, self.ueb = 0.0, 1.0
        self.messer, self.tempo_bricht, self.vf = messer, tempo_bricht, 1.0

    def tick(self, ad=0.0, ws=0.0, bug=0.0, h1=False, h2=False, h3=False, a4=0.0, h4=False, frei=False):
        """frei: Schrauben aus dem Wasser (Welle) - kaum Last, kein Schub."""
        self.vf = max(0.2, self.vf - 0.8 / 120) if (frei and self.tempo_bricht) else 1.0
        n = {1: ad, 2: ws, 3: bug, 4: a4, 5: self.v * self.vf, 6: 0.25}
        if self.messer:
            n[23] = -0.5 if frei else 2.0
        for i, m in enumerate(self.mess):
            for j in range(4):
                n[7 + 4 * i + j] = m[j]
        b = {1: h1, 2: h2, 3: h3, 4: h4, 8: True}
        self.wellen(n, b)
        self.io["n"], self.io["b"] = n, b
        self.io["on"].clear()
        self.g.onTick()
        o = dict(self.io["on"])
        ga = [PR["Getriebe A"], PR["Getriebe B"], PR["Getriebe C"]]
        self.ueb = 1.0
        for k in range(3):
            if o[109 + k]:
                self.ueb *= ga[k]
        schub, mess = 0.0, []
        for i, mo in enumerate(self.mo):
            rv = o[106 + (0 if i < 2 else 1)]
            p = mo.rps * self.ueb
            sl = max(1 - (-self.v if rv else self.v) / (self.KV * p), 0.05) if p > 0.1 else 1.0
            if frei:
                sl = 0.02
            mess.append(mo.schritt(o[3 * i + 1], o[3 * i + 2], o[3 * i + 3], o[102 + i], self.ueb ** 2 * sl))
            schub += 0.0 if frei else (-1 if rv else 1) * o[3 * i + 3] * self.KF * p * p * sl
        self.mess = mess
        self.v += (schub - self.CD * self.v * abs(self.v)) / self.MASSE / 60
        o["rps"] = [mo.rps for mo in self.mo]
        o["v"], o["ueb"] = self.v, self.ueb
        self.out = o
        self.hio["n"] = o
        self.hio["b"] = {k - 100: v for k, v in o.items() if isinstance(k, int) and k > 100}
        self.hg.onTick()
        return o


def gang(o):
    return (round(o[15]) // 100) % 100 if o[15] else 0


def test_gaenge():
    """8 Gaenge (Getriebe A/B/C je an/aus) im Schiffsmodell: Reihenfolge der Uebersetzungen und Hand-Schaltung,
    Automatik bei Vollgas (schaltet hoch, ohne zu pendeln, schneller als Gang 1), weniger Gas (schaltet runter, bleibt
    ruhig), Rueckwaerts = Gang 1."""
    def anfahren(s, hand=False):
        for k in range(60 * 10):
            s.tick(ws=1.0 if 5 <= k / 60 < 9 else 0.0, h1=k == 60, h3=hand and k == 120)
    ok = True
    # Hand: Hotkey 3 schaltet die Automatik aus, Pfeil hoch 7x, Pfeil runter 1x
    s = SchiffG([Motor() for _ in range(4)])
    anfahren(s, hand=True)
    hand = "HAND" in s.helm()[0]
    uebs = [(gang(s.out), s.ueb)]
    for _ in range(7):
        for k in range(12):
            s.tick(a4=1.0 if k < 6 else 0.0)
        uebs.append((gang(s.out), s.ueb))
    for k in range(12):
        s.tick(a4=-1.0 if k < 6 else 0.0)
    runter = gang(s.out)
    soll = sorted(a * b * c for a in (1, PR["Getriebe A"]) for b in (1, PR["Getriebe B"]) for c in (1, PR["Getriebe C"]))
    ok &= pruefe([
        ("Hotkey 3: Handschaltung (Helm zeigt HAND)", hand),
        ("Pfeil hoch: Gang 1-8, Uebersetzung %s" % " ".join("%.1f" % u for _, u in uebs),
         [g for g, _ in uebs] == list(range(1, 9)) and all(abs(u - w) < 1e-9 for (_, u), w in zip(uebs, soll))),
        ("Pfeil runter: ein Gang zurueck (%d)" % runter, runter == 7),
    ])
    # Gang 1 fest, Vollgas: Vergleichs-Tempo
    s1 = SchiffG([Motor() for _ in range(4)])
    anfahren(s1, hand=True)
    for _ in range(60 * 140):
        s1.tick()
    v1 = s1.v
    # Automatik: Vollgas 140 s, dann Hebel auf 30 %, dann rueckwaerts
    s = SchiffG([Motor() for _ in range(4)])
    anfahren(s)
    gl, rl = [], []
    for _ in range(60 * 140):
        o = s.tick()
        gl.append(gang(o))
        rl.append(o["rps"][0])
    voll, v_auto = gl[-1], s.v
    schalt = [i for i in range(1, len(gl)) if gl[i] != gl[i - 1]]
    for k in range(int(60 * 2.8)):
        s.tick(ws=-1.0)
    g2 = []
    for _ in range(60 * 90):
        o = s.tick()
        g2.append(gang(o))
    s2 = [i for i in range(1, len(g2)) if g2[i] != g2[i - 1]]
    hebel = s.out[16]
    rw = None
    for k in range(60 * 3):
        o = s.tick(ws=-1.0)
        if rw is None and o[16] < 0:
            rw = gang(o)
    ok &= pruefe([
        ("Automatik Vollgas: schaltet je einen Gang hoch, Gang %d -> %d (x%.1f), nie zurueck" % (gl[0], voll, soll[voll - 1]),
         voll >= 3 and all(0 <= b - a <= 1 for a, b in zip(gl, gl[1:])) and len(schalt) == voll - gl[0]),
        ("  danach ruhig (letzte Schaltung nach %.0f s), Motor %.1f RPS (zwischen 'Runter unter' und 'Hoch ab')" % (schalt[-1] / 60 if schalt else 0, rl[-1]),
         schalt and schalt[-1] < 60 * 100 and PR["Runter unter RPS"] <= rl[-1] <= PR["Hoch ab RPS"] + 0.5),
        ("  schneller als fest in Gang 1 (%.1f statt %.1f kn)" % (v_auto * 1.944, v1 * 1.944), v_auto > v1 * 1.02),
        ("Hebel %.0f %%: schaltet runter auf Gang %d, danach ruhig (%d Schaltungen in den letzten 40 s)" % (hebel * 100, g2[-1], sum(1 for i in s2 if i > 60 * 50)),
         g2[-1] < voll and sum(1 for i in s2 if i > 60 * 50) == 0),
        ("rueckwaerts: sofort Gang 1", rw == 1),
    ])
    # Wellen: nach dem Hochlaufen alle 5 s fuer 1.5 s Schrauben aus dem Wasser (drehen frei hoch, Tempo faellt) -
    # die Automatik darf deshalb nicht hochschalten
    # (v3.2: ohne die alte Bedingung 'Tempo faellt nicht' sperrt das nur noch das Wellen-Skript mit dem Heck-Messer)
    s = SchiffG([Motor() for _ in range(4)], messer=True)
    anfahren(s)
    for _ in range(60 * 120):
        s.tick()
    g0, rmax, gw = gang(s.out), 0.0, []
    for k in range(60 * 40):
        o = s.tick(frei=(k % 300) < 90)
        rmax = max(rmax, o["rps"][0])
        gw.append(gang(o))
    ok &= pruefe([("Wellen (Schrauben frei bis %.0f RPS): kein Hochschalten (Gang %d, hoechstens %d)" % (rmax, g0, max(gw)),
                   rmax > PR["Hoch ab RPS"] + 3 and max(gw) <= g0)])
    # v2.7 Wellen-Schutz: wie im Spiel bricht dabei der Tempo-Wert ein und springt beim Eintauchen zurueck. Ohne Messer
    # (= v2.6) schaltet die Automatik dann hin und her; mit Messer: Schaltsperre und Drehzahl halten
    erg = {}
    for name, mess, fx in (("ohne Messer", False, 0), ("mit Messer", True, 0), ("Grenze 1.5", True, 1.5)):
        # liest das Skript beim ersten Tick; 'wie v2.6' auch ohne Drehzahl-Daempfung (v3.0)
        alt = dict(PR)
        PR["Frei max RPS Faktor"] = fx
        if not mess:
            PR["Drehzahl Daempfung"] = 0
        s = SchiffG([Motor() for _ in range(4)], messer=mess, tempo_bricht=True)
        anfahren(s)
        PR.update(alt)
        for _ in range(60 * 120):
            s.tick()
        g0, r0, gw, rf = gang(s.out), max(s.out["rps"]), [], []
        for k in range(60 * 60):
            o = s.tick(frei=(k % 420) < 90)
            gw.append(gang(o))
            if (k % 420) < 90:
                rf.append(max(o["rps"]))
        erg[name] = (sum(1 for a, b in zip(gw, gw[1:]) if a != b), max(rf), r0, g0, gw[-1], s.v * 1.944)
    oh, mi, gr = erg["ohne Messer"], erg["mit Messer"], erg["Grenze 1.5"]
    ok &= pruefe([
        ("Wellen mit Tempo-Einbruch, ohne Messer (wie v2.6): %d Schaltungen in 60 s, Motor frei bis %.0f RPS, %.1f kn" % (oh[0], oh[1], oh[5]), oh[0] >= 1),
        ("  mit Messer (v2.7): %d Schaltungen, bleibt in Gang %d (%d), %.1f kn" % (mi[0], mi[3], mi[4], mi[5]),
         mi[0] == 0 and mi[4] == mi[3] and mi[5] > oh[5] * 0.95),
        ("  'Frei max RPS Faktor' 1.5: frei hoechstens %.0f RPS (vorher %.0f, %.2f-fach), %d Schaltungen" % (gr[1], gr[2], gr[1] / gr[2], gr[0]),
         gr[1] < gr[2] * 1.8 and gr[0] == 0),
    ])
    return ok


def test_schreiber():
    """Fahrtenschreiber: shud.lua schickt je 4 Ticks ein Paket an 'Log Port', erst nach Antwort das naechste; logger.py
    entpackt jede Zeile - lueckenlos, Werte gleich den Chip-Ausgaengen; ohne PC (keine Antwort) nach 2 s erneut."""
    import urllib.parse
    import logger
    s = SchiffG([Motor() for _ in range(4)])
    zeilen, chip, pakete = [], {}, 0
    for k in range(60 * 40):
        o = s.tick(ws=1.0 if 5 <= k / 60 < 9 else 0.0, h1=k == 60)
        chip[k + 1] = o
        while s.hio["http"]:
            port, body = s.hio["http"].pop(0)
            pakete += 1
            assert port == PR["Log Port"]
            for roh in urllib.parse.parse_qs(urllib.parse.urlparse(body).query)["d"][0].split(";"):
                zeilen.append(logger.entpacke(roh))
            s.hg.httpReply(port, body, "ok")
    ok_form = all(z is not None and len(z) == len(logger.SPALTEN) for z in zeilen)
    ticks = [int(z[0]) for z in zeilen if z]
    luecken = ticks == list(range(1, len(ticks) + 1))
    z = dict(zip(logger.SPALTEN, zeilen[-1]))
    o = chip[int(z["tick"])]
    rps = o["rps"][0]
    gleich = (int(z["gang"]) == gang(o) and abs(float(z["tempo_kmh"]) - o[17] * 3.6) < 0.06 and abs(float(z["L1_rps"]) - rps) < 0.06
              and z["L1_zustand"] == "OK" and z["motoren_an"] == "1" and abs(float(z["hebel_pct"]) - 100) < 0.6)
    s.hg.p2 = True          # Helm mit Hotkey 4 (alle Werte, mit Schreiber-Zeile), ohne einen Tick zu verbrauchen
    helm = s.helm()
    s.hg.p2 = False
    # PC-Programm aus: keine Antwort -> nach 2 s darf er wieder senden
    s.hio["http"].clear()
    n = 0
    for k in range(60 * 5):
        s.tick(ws=0.0)
        n += len(s.hio["http"])
        s.hio["http"].clear()
    print("   letzte Zeile:", ", ".join("%s=%s" % kv for kv in list(z.items())[:16]))
    print("   ", ", ".join("%s=%s" % kv for kv in list(z.items())[16:26]))
    return pruefe([
        ("Schreiber: %d Pakete, %d Zeilen in 40 s, je %d Spalten" % (pakete, len(zeilen), len(logger.SPALTEN)), ok_form and len(zeilen) >= 60 * 40 - 8),
        ("  lueckenlos (Tick 1..%d)" % (ticks[-1] if ticks else 0), luecken),
        ("  entpackt = Chip-Ausgang (Gang %s, %s km/h, L1 %s RPS)" % (z["gang"], z["tempo_kmh"], z["L1_rps"]), gleich),
        ("  Helm unten: %s" % helm[-1], helm[-1].startswith("LOG OK")),
        ("  ohne Antwort: alle 2 s ein neuer Versuch (%d in 5 s)" % n, 2 <= n <= 3),
    ])


def test_temperatur():
    """v3.4: 4 Motoren mit Waermemodell (L2 wird 4 % waermer), kalt los, 12 min Vollgas, dann 2 min Hebel 30 %, dann
    wieder Vollgas. Gemeinsame Grenze: alle gleich viel Gas; sanft auf 'Temp Ziel', kaum Ueberschwingen, kein Schaukeln.
    Fahrt 07.10.: Gas weg -> Temperatur faellt erst 10-15 s spaeter. Falls das Spiel nur ganze Grad meldet, schwankt das
    Gas mehr (alle Motoren gleich, Temperatur bleibt beim Ziel)."""
    tz, ok = PR["Temp Ziel"], True
    for lag, name, schw, ganz in ((15, "Kuehlung 15 s traege", 5, False), (25, "Kuehlung 25 s traege", 12, False),
                                  (15, "nur ganze Grad", 30, True)):
        mo = [Motor(waerme=(0.27 * f, 0.00124, lag)) for f in (1.0, 1.04, 1.0, 0.98)]
        if ganz:
            for m in mo:
                m.schritt = (lambda alt: lambda *x: (lambda r: (r[0], float(round(r[1])), r[2], r[3]))(alt(*x)))(m.schritt)
        sch = Schiff(mo)
        T, gas, gleich, zust, voll = [], [], True, set(), 0.0
        for k in range(60 * 17 * 60):
            sek = k / 60
            ws = 1.0 if 2 <= sek < 6 or 14 * 60 + 2 <= sek < 14 * 60 + 5 else (-1.0 if 12 * 60 <= sek < 12 * 60 + 2.8 else 0.0)
            o = sch.tick(ws=ws, h1=1 <= sek < 1.05)
            if k % 30:
                continue
            g = [entpacke(o, i)["gas"] for i in (1, 2, 3, 4)]
            T.append((sek, max(m.tmp for m in mo)))
            gas.append((sek, g[0]))
            if sek > 20:
                gleich &= max(g) - min(g) <= 1
                zust |= {entpacke(o, i)["z"] for i in (1, 2, 3, 4)}
            if g[0] >= 95:
                voll = sek
        im = lambda a, b, L: [v for t, v in L if a <= t < b]
        tmax = max(im(0, 12 * 60, T))
        ruhig = im(8 * 60, 12 * 60, gas)
        tr = im(8 * 60, 12 * 60, T)
        nach = max(im(14 * 60, 17 * 60, T))
        print("   %s: Vollgas bis %.0f s, hoechstens %.1f Grad, ab 8 min %.1f-%.1f Grad bei %d-%d %% Gas, wieder Vollgas: hoechstens %.1f"
              % (name, voll if voll < 600 else 0, tmax, min(tr), max(tr), min(ruhig), max(ruhig), nach))
        voll_kalt = max(t for t, v in gas if v >= 95 and t < 600)
        ok &= pruefe([
            ("%s: ab kalt %.0f s volles Gas" % (name, voll_kalt), voll_kalt >= 150),
            ("  ueberschiesst hoechstens 2 Grad (%.1f)" % tmax, tmax <= tz + 2),
            ("  haelt %d +-1.5 Grad (%.1f..%.1f)" % (tz, min(tr), max(tr)), tz - 1.5 <= min(tr) and max(tr) <= tz + 1.5),
            ("  Gas schwankt hoechstens %d %% (%d..%d)" % (schw, min(ruhig), max(ruhig)), max(ruhig) - min(ruhig) <= schw),
            ("  alle 4 Motoren gleich viel Gas", gleich),
            ("  Anzeige TEMP, nie HEISS", 3 in zust and 1 not in zust),
            ("  Hebel 30 %% und wieder voll: hoechstens %.1f Grad" % nach, nach <= tz + 2),
        ])
    return ok


def test_emotor():
    """v3.5: 4 Motoren mit Waermemodell, Vollgas. E-Gas (Zahl 20) = Hebel minus Temperatur-Grenze; Batterie unter 50 %:
    aus (erst ab 55 % wieder an), Bool 13; 'E-Motor Test' 1: Diesel ausgekuppelt, E-Gas = Hebel."""
    ok = True
    mo = [Motor(waerme=(0.27 * f, 0.00124, 15)) for f in (1.0, 1.04, 1.0, 0.98)]
    sch = Schiff(mo)
    sch.batt = 0.9
    log = {}
    for k in range(60 * 12 * 60):
        sek = k / 60
        if sek >= 600:
            sch.batt = 0.4 if sek < 630 else (0.52 if sek < 660 else 0.6)
        o = sch.tick(ws=1.0 if 2 <= sek < 6 else 0.0, h1=1 <= sek < 1.05)
        if k % 30 == 0:
            log[round(sek, 1)] = (o[20], entpacke(o, 1)["gas"], bool(o.get(113)), o[3])
    at = lambda t: log[round(t, 1)]
    kalt = at(100)
    heiss = at(540)
    ok &= pruefe([
        ("kalt (100 s): Diesel %d %% Gas, E-Motor %.0f %%" % (kalt[1], kalt[0] * 100), kalt[1] >= 95 and kalt[0] < 0.05),
        ("heiss (540 s): Diesel %d %%, E-Motor %.0f %% = der Rest bis 100 %%" % (heiss[1], heiss[0] * 100),
         heiss[1] < 40 and abs(heiss[0] * 100 + heiss[1] - 100) <= 3),
        ("Batterie 40 %%: E-Motor aus (%.0f %%), Warnung (Bool 13) an" % (at(620)[0] * 100), at(620)[0] < 0.01 and at(620)[2]),
        ("Batterie 52 %: bleibt aus (erst ab 55 %)", at(650)[0] < 0.01 and at(650)[2]),
        ("Batterie 60 %%: wieder an (%.0f %%), Bool 13 aus" % (at(700)[0] * 100), at(700)[0] > 0.4 and not at(700)[2]),
    ])
    PR["E-Motor Test"] = 1
    try:
        sch = Schiff([Motor() for _ in range(4)])
        sch.batt = 0.9
        for k in range(60 * 20):
            sek = k / 60
            o = sch.tick(ws=1.0 if 2 <= sek < 4 else 0.0, h1=1 <= sek < 1.05)
    finally:
        PR["E-Motor Test"] = 0
    ok &= pruefe([("'E-Motor Test': Diesel ausgekuppelt, E-Gas = Hebel (%.0f %% / %.0f %%)" % (o[20] * 100, o[16] * 100),
                   all(o[3 * i + 3] == 0 for i in range(4)) and abs(o[20] - o[16]) < 0.01 and o[16] > 0.4)])
    sch = Schiff([Motor() for _ in range(4)])
    for k in range(60 * 30):
        o = sch.tick(ws=1.0 if 2 <= k / 60 < 6 else 0.0, h1=60 <= k < 63)
    ok &= pruefe([("ohne Batterie (Kanal 25 = 0), kalt: E-Motoren aus, keine Warnung (nicht gebraucht)",
                   o[20] == 0 and not o.get(113))])
    return ok


if __name__ == "__main__":
    ok = test_motor()
    ok &= test_system()
    ok &= test_gemisch()
    ok &= test_gaenge()
    ok &= test_schreiber()
    ok &= test_temperatur()
    ok &= test_emotor()
    print("ALLES OK" if ok else "FEHLER")
    sys.exit(0 if ok else 1)
