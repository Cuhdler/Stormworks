"""Baut die Feuerleit-Chips der Anti-Schiffs-Kanonen vorn der Figet Marena (Andre 04.10.: "lass uns jetzt die Anti-
Schiffs-Kanonen machen"): "Figet Marena Kanone BC" (Battle Cannon, grosser Turm) und "Figet Marena Kanone AC" (Heavy
Autocannon, mittlerer Turm vorn). Die Tuerme sind gebaut wie die Flak-Tuerme (Drehkranz, Rohr auf zwei Robotic Pivots,
Turm-Radar, Kamera auf Compact Pivot) - darum dieselbe Schaltung und dieselben Skripte FLAKRADAR + FLAK
(build_flak.build), mit eigenen Eigenschaften: Ziele auf dem Wasser, flache Bahn, Reichweite, Aufschlagzuender, Battle
Cannon mit Lade-Ablauf (Verschluss).

Richtungen aus den Teilen abgeleitet (gleiche Regel wie an allen vier Flak-Pivots, die im Spiel stimmen): Drehkranz -1
(nicht gespiegelt wie Flak L), Radar +1, Kamera-Pivot -1; Hoehen-Pivots BC +1/+1 (Achse +x), AC -1/-1 (Achse -x).
Ballistik: AC wie die Flak (Heavy Autocannon 900 m/s, Drag 0,005); BC nach Community-Werten 800 m/s, Drag 0,002 -
ungeprueft, beim Einschiessen ggf. 'AA v0' / 'AA Drag' anpassen.
- mit --install zusaetzlich nach %APPDATA%/Stormworks/data/microprocessors kopieren
"""
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_schiff import minify, fmt, LUA_LIMIT, LUA_DIR, BUILD  # noqa: E402
from build_lage import kopf  # noqa: E402
import build_flak  # noqa: E402
import sperrprofil  # noqa: E402

VERSION = "v1.6"
# Kuerzel (Schreiber kB / kA), Name, Waffe im Bildschirm (1 BC, 2 AC), Drehmitte (x, z), Hoehe der Rohr-Drehachse (y),
# Geschuetz, Turm-Name in den Anschluss-Beschreibungen, Verschluss
KANONEN = [("B", "BC", 1, 0, 5, 14, "Battle Cannon", "BC-Turm", True),
           ("A", "AC", 2, 0, 31, 9, "Heavy Autocannon", "AC-Turm vorn", False)]
# Abweichungen von den Flak-Eigenschaften (build_flak.PROPS)
GEMEINSAM = {"AA Turm Richtung": -1, "AA Radar Richtung": 1, "AA Radar Hoehe Richtung": 1, "Kamera Hoehe Richtung": -1,
             "AA Mindesthoehe m": -30, "AA Suchhoehe Grad": 0, "AA Suchstufen": 1, "AA tiefster Winkel Grad": -5,
             "AA Zuender": 0, "AA Takt Ticks": 1, "Ziel Tempo max m/s": 20, "Kamera Zielgroesse m": 40}
EIGEN = {
    "B": dict(GEMEINSAM, **{"AA Hoehe Richtung links": 1, "AA Hoehe Richtung rechts": 1, "AA Reichweite m": 6000,
                            "AA v0": 800, "AA Drag": 0.002, "AA Toleranz Grad": 0.1, "AA Toleranz m": 6,
                            "AA Streuung m": 0, "Lader Zeit s": 3.6, "AA Turm Bremsen": 0.2, "Rohre": 2}),
    "A": dict(GEMEINSAM, **{"AA Hoehe Richtung links": -1, "AA Hoehe Richtung rechts": -1, "AA Reichweite m": 2000,
                            "AA Toleranz Grad": 0.3, "AA Toleranz m": 3, "AA Streuung m": 1}),
}
# Lage der Turm-Radare zum Physik-Sensor (0, 27, -38): BC-Radar (0, 17, 11), AC-Radar (0, 12, 35) - Bloecke * 0,25 m
# Spur-Glaettung (Pruefstand 04.10.: BC 4,5 km 10 von 13 Treffern statt 0 mit 0,1/0,005; AC am besten 0,05/0,001)
EIGEN["B"].update({"Spur Alpha": 0.03, "Spur Beta": 0.0003})
EIGEN["A"].update({"Spur Alpha": 0.05, "Spur Beta": 0.001})
EIGEN["B"].update({"Ziel Hoehe fest m": 1.5, "Radar ueber Physik m": (17 - 27) * .25, "Radar vor Physik m": (11 + 38) * .25})
EIGEN["A"].update({"Ziel Hoehe fest m": 1.5, "Radar ueber Physik m": (12 - 27) * .25, "Radar vor Physik m": (35 + 38) * .25})
TEXT = {"AA Mindesthoehe m": "Nur Ziele hoeher als das ueber dem Meer (-30: auch Schiffe)",
        "AA Reichweite m": "Bis zu dieser Entfernung schiesst die Kanone",
        "AA Zuender": "0 = Aufschlagzuender (gegen Schiffe), 1 = Zeitzuender auf die Flugzeit",
        "Lader Zeit s": "Battle Cannon: so lange bleibt der Verschluss je Ladeversuch offen (KI-Panzer: 3,6); 0 = Autocannon"}


def props(k):
    out = []
    for name, val, desc in build_flak.PROPS:
        if name in EIGEN[k]:
            val, desc = EIGEN[k][name], TEXT.get(name, desc)
        out.append((name, val, desc))
    return out


def main():
    os.makedirs(BUILD, exist_ok=True)
    src = {}
    for name in ("flakradar", "flak"):
        with open(os.path.join(LUA_DIR, name + ".lua"), encoding="utf-8") as f:
            src[name] = minify(f.read())
    kp = sperrprofil.koerper()
    for k, name, waffe, cx, cz, gy, gname, turm, verschluss in KANONEN:
        prf = sperrprofil.profil(cx, cz, gy, kp)
        fl = src["flak"].replace("PRF='0'", "PRF='%s'" % ",".join(fmt(float(v)) for v in prf))
        assert fl != src["flak"], "PRF nicht gefunden"
        fl = kopf(fl, "k%sf" % k)
        fr = kopf(src["flakradar"], "k%sr" % k)
        for nm, s in (("radar " + name, fr), ("kanone " + name, fl)):
            print("%-10s %5d Zeichen %s" % (nm, len(s), "OK" if len(s) <= LUA_LIMIT else "ZU LANG"))
            if len(s) > LUA_LIMIT:
                sys.exit("Skript zu lang")
        mc = build_flak.build(fr, fl, k, src, titel="Figet Marena Kanone %s" % name,
                              beschr="Kanone %s %s: Schiffsziel und Feuer frei vom Bildschirm, Turm-Radar, Vorhalt, Schreiber"
                              % (name, VERSION), waffe=waffe, props=props(k), turm=turm, gname=gname,
                              rechts=verschluss, verschluss=verschluss, zwilling=verschluss)
        assert len(mc.desc) <= 128, len(mc.desc)
        fname = "Figet Marena Kanone %s %s.xml" % (name, VERSION)
        out = os.path.join(BUILD, fname)
        with open(out, "w", encoding="utf-8", newline="\n") as f:
            f.write(mc.xml())
        print("geschrieben:", out)
        if "--install" in sys.argv:
            dst = os.path.join(os.environ["APPDATA"], "Stormworks", "data", "microprocessors", fname)
            shutil.copyfile(out, dst)
            print("installiert:", dst)


if __name__ == "__main__":
    main()
