"""Prueft den Nachbau build_mc.py gegen die Chips, die in der Figet Marena stecken (fahrzeug/Figet Marena.xml):
die Schiffs-Bauskripte (tools/build_*.py) bauen mit diesem build_mc alle Waffen-Chips neu (Sperrprofile aus der
Fahrzeugkopie im Repo); Aufbau (Anschluesse, Bausteine, Kabel im Chip) muss genau gleich sein. Abweichende
Eigenschafts-Werte und Skripte werden nur gemeldet (Andre/Claude haben einzelne Werte nach dem Bau geaendert).

Aufruf: python landkreuzer/tools/test_build_mc.py
"""
import html
import os
import re
import sys

HIER = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HIER))
sys.path.insert(0, HIER)
import build_mc  # noqa: E402

sys.modules["build_mc"] = build_mc
sys.path.insert(1, os.path.join(ROOT, "tools"))
os.environ.setdefault("APPDATA", "/tmp/kein_appdata")
SCHIFF_PFAD = os.path.join(ROOT, "fahrzeug", "Figet Marena.xml")
SCHIFF = open(SCHIFF_PFAD, encoding="utf-8", newline="").read()


def eingebaut(name):
    i = SCHIFF.index('<microprocessor_definition name="%s"' % name)
    e = SCHIFF.index("</microprocessor_definition>", i) + len("</microprocessor_definition>")
    return SCHIFF[i:e]


def ohne(t):
    t = re.sub(r'script=("[^"]*"|\'[^\']*\')', 'script=""', t)
    return re.sub(r'<v text="[^"]*"( value="[^"]*")?/>', "<v/>", t)


def skripte(t):
    return [html.unescape(a or b) for a, b in re.findall(r'script=(?:"([^"]*)"|\'([^\']*)\')', t)]


def props(t):
    return re.findall(r'n="([^"]*)"><pos[^>]*/><v text="([^"]*)"', t)


def vergleich(name, neu):
    alt = eingebaut(name)
    a, b = ohne(alt), ohne(neu)
    if a != b:
        al, bl = a.replace("><", ">\n<").split("\n"), b.replace("><", ">\n<").split("\n")
        for k, (x, y) in enumerate(zip(al, bl)):
            if x != y:
                print("  %s: Aufbau verschieden ab Zeile %d:\n    eingebaut: %s\n    neu:       %s" % (name, k, x[:160], y[:160]))
                return False
        print("  %s: Aufbau verschieden (Laenge)" % name)
        return False
    pa, pb = props(alt), props(neu)
    dp = [(n, v, w) for (n, v), (_, w) in zip(pa, pb) if v != w]
    sa, sb = skripte(alt), skripte(neu)
    gleich = [x == y for x, y in zip(sa, sb)]
    print("  %-30s Aufbau gleich; Skripte gleich %s; Eigenschaften anders (Name, eingebaut, Bau): %s"
          % (name, gleich, dp or "keine"))
    return True


def main():
    import sperrprofil
    import umbau_v1
    sperrprofil.koerper.__defaults__ = (SCHIFF_PFAD,)
    # die 24 Raketen (mit eigenem Physik-Sensor) kamen nach dem Bau der Waffen-Chips dazu - fuer den Vergleich weglassen
    _k = sperrprofil.koerper
    sperrprofil.koerper = lambda pfad=SCHIFF_PFAD: [t for t in _k(pfad) if not any(d == "solid_rocket_medium" for d, _ in t)]
    umbau_v1.VEH = SCHIFF_PFAD
    import build_schutz
    import build_lage
    import build_flak
    import build_kanone
    import build_kamera
    from build_schiff import LUA_DIR
    mini = lambda n: build_mc.minify(open(os.path.join(LUA_DIR, n + ".lua"), encoding="utf-8").read())
    ok = True
    print("Nachbau build_mc gegen die eingebauten Chips der Figet Marena:")
    ok &= vergleich("Figet Marena Schutz", build_schutz.build(build_lage.kopf(mini("schutz"), "sc")).embedded())
    kp = sperrprofil.koerper()
    src = {n: mini(n) for n in ("flakradar", "flak")}
    for seite, cx, cz, gy in build_flak.TUERME:
        prf = sperrprofil.profil(cx, cz, gy, kp)
        fl = build_lage.kopf(src["flak"].replace("PRF='0'", "PRF='%s'" % ",".join(build_mc.fmt(float(v)) for v in prf)),
                             "f%sf" % seite)
        fr = build_lage.kopf(src["flakradar"], "f%sr" % seite)
        ok &= vergleich("Figet Marena Flak %s" % seite, build_flak.build(fr, fl, seite, src).embedded())
    for k, name, waffe, cx, cz, gy, gname, turm, verschluss in build_kanone.KANONEN:
        prf = sperrprofil.profil(cx, cz, gy, kp)
        fl = build_lage.kopf(src["flak"].replace("PRF='0'", "PRF='%s'" % ",".join(build_mc.fmt(float(v)) for v in prf)),
                             "k%sf" % k)
        fr = build_lage.kopf(src["flakradar"], "k%sr" % k)
        mc = build_flak.build(fr, fl, k, src, titel="Figet Marena Kanone %s" % name,
                              beschr="Kanone %s %s: Schiffsziel und Feuer frei vom Bildschirm, Turm-Radar, Vorhalt, Schreiber"
                              % (name, build_kanone.VERSION), waffe=waffe, props=build_kanone.props(k), turm=turm,
                              gname=gname, rechts=verschluss, verschluss=verschluss, zwilling=verschluss)
        ok &= vergleich("Figet Marena Kanone %s" % name, mc.embedded())
    ok &= vergleich("Figet Marena Kamera", build_kamera.build(build_lage.kopf(mini("kamera"), "ka")).embedded())
    ls = {n: mini(n) for n in ("mastradar", "lage", "bild", "waffenwahl")}
    hw = build_lage.umriss()
    ls["waffenwahl"] = ls["waffenwahl"].replace("UM='0'", "UM='%s'" % ",".join(str(v) for v in hw))
    ls["bild"] = build_lage.kopf(build_lage.bild_flak(ls["bild"]), "ba")
    ls["lage"] = build_lage.kopf(ls["lage"], "la")
    ok &= vergleich("Figet Marena Lage", build_lage.build_lage(ls).embedded())
    ok &= vergleich("Figet Marena Bildschirm", build_lage.build_bild(ls).embedded())
    ok &= vergleich("Figet Marena Waffenwahl", build_lage.build_wahl(ls).embedded())
    print("ALLES OK" if ok else "FEHLER")
    return ok


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
