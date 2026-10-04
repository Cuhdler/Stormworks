"""Sperrprofil fuer einen Geschuetzturm der Figet Marena aus der Fahrzeug-Datei: je 5 Grad Richtung (ab Bug, im
Uhrzeigersinn, 72 Werte) der tiefste Rohrwinkel in Grad, mit dem ein Geschoss vom Drehpunkt der Rohre aus ueber alle
Teile des Schiffs hinweg geht.

- Rumpf (Koerper mit den meisten Teilen): jedes Teil als Wuerfel (0,25 m); Teile innerhalb 'frei_r' Bloecke um die
  eigene Turmmitte unterhalb der Rohre gehoeren zum eigenen Drehkranz und zaehlen nicht
- andere Tuerme: ihr Drehkranz-Oberteil als Kreis (Radius ihres weitesten Teils um die Drehmitte, hoechste Hoehe);
  ihre Rohre zaehlen nicht (mit dem ganzen Schwenkbereich der Rohre waere z. B. fuer Flak L die halbe rechte Seite
  unter 43 Grad gesperrt - die Rohre zeigen aber fast immer nach oben)
- eigener Turm und seine Rohre: zaehlen nicht (drehen mit)
Rand: Nachbar-Richtungen mit (der Strahl ist nicht genau), dazu 'zugabe' Grad.
Aufruf zum Ansehen: python sperrprofil.py
"""
import math
import os
import re

VEH = os.path.join(os.environ["APPDATA"], "Stormworks", "data", "vehicles", "Figet Marena.xml")


def koerper(pfad=VEH):
    """Liste der Koerper: je Liste von (Teil, (x, y, z))."""
    s = open(pfad, encoding="utf-8").read()
    s = re.sub(r"<microprocessor_definition.*?</microprocessor_definition>", "", s, flags=re.S)
    i, e = s.index("<bodies>"), s.index("</bodies>")
    out = []
    for txt in re.findall(r"<body [^>]*>(.*?)</body>", s[i:e], re.S):
        teile = []
        for m in re.finditer(r'<c(?: d="([^"]+)")?(?: t="\d+")?><o [^>]*>(?:(?!</c>).)*?<vp([^/]*)/>', txt, re.S):
            p = dict(re.findall(r'(\w)="(-?\d+)"', m.group(2)))
            teile.append((m.group(1) or "block", tuple(int(p.get(k, 0)) for k in "xyz")))
        out.append(teile)
    return out


def tuerme(kp):
    """Tuerme: (Drehmitte x, z, Koerper-Indizes) - ein Turm = Koerper mit Turret-Ring-Oberteil (_b) plus die Koerper
    seiner Rohre (Koerper mit Geschuetz innerhalb von 16 Bloecken um die Mitte)."""
    rum = max(range(len(kp)), key=lambda k: len(kp[k]))
    out = []
    for k, teile in enumerate(kp):
        ringe = [p for d, p in teile if d.startswith("multibody_turret_") and d.endswith("_b")]
        if ringe and k != rum:
            cx, cz = ringe[0][0], ringe[0][2]
            gl = [k] + [j for j, t in enumerate(kp) if j not in (k, rum) and any(d.startswith("gun_") for d, _ in t)
                         and not any(dd.startswith("multibody_turret_") for dd, _ in t)
                         and all(math.hypot(p[0] - cx, p[2] - cz) < 16 for _, p in t)]
            out.append((cx, cz, gl))
    return rum, out


def profil(cx, cz, gy, kp=None, frei_r=4.5, zugabe=2.0, schritt=5):
    kp = kp or koerper()
    rum, tu = tuerme(kp)
    eigen = [g for g in tu if g[0] == cx and g[1] == cz]
    assert eigen, ("kein Turm bei", cx, cz)
    n = 360 // schritt
    roh = [0.0] * n

    def punkt(x, y, z, halb=0.5):
        dx, dz, dy = x - cx, z - cz, y - gy
        h = math.hypot(dx, dz)
        if h < 1:
            return
        el = math.degrees(math.atan2(dy + halb, max(h - halb, 0.5)))
        b = math.degrees(math.atan2(dx, dz))
        k = int(round(b / schritt)) % n
        roh[k] = max(roh[k], el)

    for d, (x, y, z) in kp[rum]:
        if math.hypot(x - cx, z - cz) < frei_r and y <= gy:
            continue
        punkt(x, y, z)
    for (ox, oz, gl) in tu:
        if (ox, oz) == (cx, cz):
            continue
        pts = [p for _, p in kp[gl[0]]]
        r = max(math.hypot(p[0] - ox, p[2] - oz) for p in pts) + 0.5
        top = max(p[1] for p in pts)
        for w in range(0, 360, 2):
            a = math.radians(w)
            for f in (0.0, 0.5, 1.0):
                punkt(ox + f * r * math.sin(a), top, oz + f * r * math.cos(a))
    fertig = [round(min(85.0, max(roh[(k - 1) % n], roh[k], roh[(k + 1) % n]) + zugabe), 1) if
              max(roh[(k - 1) % n], roh[k], roh[(k + 1) % n]) > 0 else 0.0 for k in range(n)]
    return fertig


if __name__ == "__main__":
    kp = koerper()
    rum, tu = tuerme(kp)
    print("Rumpf-Koerper %d, Tuerme: %s" % (rum, [(x, z, g) for x, z, g in tu]))
    for name, cx, cz in (("Flak L", -10, -105), ("Flak R", 10, -105)):
        pr = profil(cx, cz, 18, kp)
        print("%s (Mitte %d,%d, Rohre y 18):" % (name, cx, cz))
        for k in range(0, 72, 12):
            print("   " + "  ".join("%4d:%4.0f" % (((k + j) * 5 + 180) % 360 - 180, pr[k + j]) for j in range(12)))
