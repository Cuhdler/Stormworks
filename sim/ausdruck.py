"""Formeln der Microcontroller-Bausteine in Python uebersetzen (Teil des Simulators sim/swsim.py).

Zahlen-Formeln (Baustein 10 f(x,y,z), 36 mit 8 Eingaengen, 45 mit 1 Eingang):
  Variablen x y z w a b c d, Zahlen (auch .5), + - * / % ^, Klammern, Funktionen wie im Spiel:
  abs sqrt floor ceil round sin cos tan asin acos atan atan2 exp log pow min max clamp lerp len sgn, Konstanten pi pi2.
  Diese Liste ist aus den Formeln in Andres Chip-Dateien abgelesen (10.10.); weitere Namen geben einen klaren Fehler.
An/Aus-Formeln (Baustein 46 mit 4, 47 mit 8 Eingaengen): ! & | ^ (= entweder-oder) und Klammern.

Vermutet [V] (nicht im Spiel geprueft): % rechnet wie fmod (Vorzeichen vom linken Wert), round rundet .5 von null weg,
sgn(0) = 0, x/0 = unendlich (bzw. nan bei 0/0), ^ bindet staerker als ein Minus davor (-x^2 = -(x^2)).
"""
import math

VARIABLEN = "xyzwabcd"


def _div(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        if a == 0 or a != a:
            return math.nan
        return math.copysign(math.inf, a) * math.copysign(1.0, b)


def _mod(a, b):
    try:
        return math.fmod(a, b)
    except (ValueError, ZeroDivisionError):
        return math.nan


def _pow(a, b):
    try:
        r = math.pow(a, b)
    except (ValueError, OverflowError, ZeroDivisionError):
        return math.nan if a < 0 else math.inf
    return r


def _sicher(f):
    def g(*a):
        try:
            return f(*a)
        except (ValueError, OverflowError, ZeroDivisionError):
            return math.nan
    return g


def _runde(x):
    return math.floor(x + 0.5) if x >= 0 else -math.floor(-x + 0.5)


def _sgn(x):
    return 1.0 if x > 0 else (-1.0 if x < 0 else 0.0)


FUNKTIONEN = {
    "abs": abs, "sqrt": _sicher(math.sqrt), "floor": _sicher(math.floor), "ceil": _sicher(math.ceil),
    "round": _sicher(_runde), "sin": _sicher(math.sin), "cos": _sicher(math.cos), "tan": _sicher(math.tan),
    "asin": _sicher(math.asin), "acos": _sicher(math.acos), "atan": _sicher(math.atan),
    "atan2": _sicher(math.atan2), "exp": _sicher(math.exp), "log": _sicher(math.log), "pow": _pow,
    "min": lambda *a: min(a), "max": lambda *a: max(a), "clamp": lambda x, a, b: min(max(x, a), b), "lerp": lambda a, b, t: a + (b - a) * t,
    "len": lambda *v: math.sqrt(sum(q * q for q in v)), "sgn": _sgn,
}
KONSTANTEN = {"pi": math.pi, "pi2": 2 * math.pi}


class AusdruckFehler(Exception):
    pass


def _woerter(text):
    """Zerlegt die Formel in Teile: Zahlen, Namen, Zeichen."""
    out, i = [], 0
    while i < len(text):
        ch = text[i]
        if ch.isspace():
            i += 1
        elif ch.isdigit() or (ch == "." and i + 1 < len(text) and text[i + 1].isdigit()):
            j = i
            while j < len(text) and (text[j].isdigit() or text[j] == "."):
                j += 1
            if j < len(text) and text[j] in "eE" and j + 1 < len(text) and (text[j + 1].isdigit() or text[j + 1] in "+-"):
                j += 2
                while j < len(text) and text[j].isdigit():
                    j += 1
            out.append(("zahl", text[i:j]))
            i = j
        elif ch.isalpha() or ch == "_":
            j = i
            while j < len(text) and (text[j].isalnum() or text[j] == "_"):
                j += 1
            out.append(("name", text[i:j].lower()))
            i = j
        elif ch in "+-*/%^(),&|!":
            out.append(("zeichen", ch))
            i += 1
        else:
            raise AusdruckFehler("Zeichen %r in der Formel %r unbekannt" % (ch, text))
    return out


class _Leser:
    def __init__(self, text, variablen):
        self.text, self.w, self.i, self.var = text, _woerter(text), 0, variablen

    def sieh(self):
        return self.w[self.i] if self.i < len(self.w) else (None, None)

    def nimm(self, zeichen=None):
        t = self.sieh()
        if zeichen is not None and t != ("zeichen", zeichen):
            raise AusdruckFehler("in der Formel %r fehlt %r (Stelle %d)" % (self.text, zeichen, self.i))
        self.i += 1
        return t

    def fertig(self):
        if self.i != len(self.w):
            raise AusdruckFehler("Formel %r: unerwartetes %r" % (self.text, self.sieh()[1]))


# ---- Zahlen-Formeln -----------------------------------------------------------------------------------------------

def _summe(p):
    a = _produkt(p)
    while p.sieh() in (("zeichen", "+"), ("zeichen", "-")):
        op = p.nimm()[1]
        a = "(%s %s %s)" % (a, op, _produkt(p))
    return a


def _produkt(p):
    a = _vorzeichen(p)
    while p.sieh() in (("zeichen", "*"), ("zeichen", "/"), ("zeichen", "%")):
        op = p.nimm()[1]
        b = _vorzeichen(p)
        a = "(%s * %s)" % (a, b) if op == "*" else ("_div(%s, %s)" % (a, b) if op == "/" else "_mod(%s, %s)" % (a, b))
    return a


def _vorzeichen(p):
    if p.sieh() == ("zeichen", "-"):
        p.nimm()
        return "(-%s)" % _vorzeichen(p)
    if p.sieh() == ("zeichen", "+"):
        p.nimm()
        return _vorzeichen(p)
    return _hoch(p)


def _hoch(p):
    a = _grund(p)
    if p.sieh() == ("zeichen", "^"):
        p.nimm()
        return "_pow(%s, %s)" % (a, _vorzeichen(p))
    return a


def _grund(p):
    art, w = p.nimm()
    if art == "zahl":
        try:
            return repr(float(w))
        except ValueError:
            raise AusdruckFehler("Zahl %r in der Formel %r unlesbar" % (w, p.text))
    if art == "zeichen" and w == "(":
        a = _summe(p)
        p.nimm(")")
        return a
    if art == "name":
        if p.sieh() == ("zeichen", "("):
            if w not in FUNKTIONEN:
                raise AusdruckFehler("Funktion %r in der Formel %r kennt der Simulator nicht" % (w, p.text))
            p.nimm()
            args = []
            if p.sieh() != ("zeichen", ")"):
                args.append(_summe(p))
                while p.sieh() == ("zeichen", ","):
                    p.nimm()
                    args.append(_summe(p))
            p.nimm(")")
            return "_f_%s(%s)" % (w, ", ".join(args))
        if w in p.var:
            return w
        if w in KONSTANTEN:
            return repr(KONSTANTEN[w])
        raise AusdruckFehler("Name %r in der Formel %r unbekannt (Variablen: %s)" % (w, p.text, " ".join(p.var)))
    raise AusdruckFehler("Formel %r: unerwartetes %r" % (p.text, w))


def zahl_formel(text, anzahl):
    """Formel -> Python-Funktion f(x, y, ...) mit 'anzahl' Eingaengen (1, 3 oder 8)."""
    var = VARIABLEN[:anzahl]
    p = _Leser(text, var)
    if not p.w:
        return lambda *a: 0.0
    code = _summe(p)
    p.fertig()
    umg = {"_div": _div, "_mod": _mod, "_pow": _pow, "math": math}
    umg.update({"_f_" + k: f for k, f in FUNKTIONEN.items()})
    f = eval("lambda %s: float(%s)" % (", ".join(var), code), umg)

    def sicher(*a):
        try:
            return f(*a)
        except (OverflowError, ValueError, ZeroDivisionError):
            return math.nan
        except TypeError as e:
            raise AusdruckFehler("Formel %r: %s" % (text, e))
    return sicher


# ---- An/Aus-Formeln -----------------------------------------------------------------------------------------------

def _oder(p):
    a = _entweder(p)
    while p.sieh() == ("zeichen", "|"):
        p.nimm()
        a = "(%s or %s)" % (a, _entweder(p))
    return a


def _entweder(p):
    a = _und(p)
    while p.sieh() == ("zeichen", "^"):
        p.nimm()
        a = "(%s != %s)" % (a, _und(p))
    return a


def _und(p):
    a = _nicht(p)
    while p.sieh() == ("zeichen", "&"):
        p.nimm()
        a = "(%s and %s)" % (a, _nicht(p))
    return a


def _nicht(p):
    if p.sieh() == ("zeichen", "!"):
        p.nimm()
        return "(not %s)" % _nicht(p)
    art, w = p.nimm()
    if art == "zeichen" and w == "(":
        a = _oder(p)
        p.nimm(")")
        return a
    if art == "name" and w in p.var:
        return w
    if art == "zahl" and w in ("0", "1"):
        return "True" if w == "1" else "False"
    raise AusdruckFehler("An/Aus-Formel %r: unerwartetes %r" % (p.text, w))


def logik_formel(text, anzahl):
    """An/Aus-Formel -> Python-Funktion f(x, y, ...) -> bool."""
    var = VARIABLEN[:anzahl]
    p = _Leser(text, var)
    if not p.w:
        return lambda *a: False
    code = _oder(p)
    p.fertig()
    return eval("lambda %s: bool(%s)" % (", ".join(var), code), {})
