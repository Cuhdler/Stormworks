"""Zeichnet ein Stormworks-Fahrzeug von oben, von der Seite und von vorn (PNG), zum Ansehen ohne Spiel.

Aufruf (mit matplotlib): python landkreuzer/tools/ansicht.py              alle Bilder in landkreuzer/bilder neu
                         python landkreuzer/tools/ansicht.py Fahrzeug.xml [Ausgabe.png]   nur die drei Ansichten
Blickrichtungen wie im Spiel (nicht gespiegelt): die Kennung KL-1 ist auf beiden Seiten von aussen lesbar.
Jedes Teil ist ein Kaestchen an seiner Position (0,25 m); Bloecke in ihrer Farbe, Bauteile nach Art eingefaerbt.
"""
import os
import sys

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
import fz  # noqa: E402

LK = os.path.dirname(HIER)
ARTEN = [  # (Anfang des Namens, Farbe, Legende)
    (("gun_", "multibody_robotic_pivot_01"), "#d62728", "Geschuetze"),
    (("multibody_turret",), "#ff7f0e", "Drehkranz"),
    (("radar", "camera", "laser_distance"), "#1f77b4", "Radar/Kamera/Laser"),
    (("microprocessor", "gate_"), "#9467bd", "Chips"),
    (("motor_", "trans_"), "#7f7f7f", "Antrieb/Wellen"),
    (("battery",), "#e6c200", "Batterien"),
    (("window",), "#17becf", "Fenster"),
    (("seat", "monitor", "instrument", "button"), "#2ca02c", "Bruecke"),
]


def farbe(t):
    for anf, f, _ in ARTEN:
        if t.d.startswith(anf):
            return f
    import re
    m = re.search(r'\bbc="([0-9A-Fa-f]{6})"', t.xml)
    return "#" + m.group(1) if m else "#a0a0a0"


def zeichnen(pfad, aus):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Patch
    F = fz.Fahrzeug.lesen(pfad)
    teile = [t for _, ts in F.koerper for t in ts]
    fig, ax = plt.subplots(3, 1, figsize=(14, 15), gridspec_kw={"height_ratios": [1.1, 1, 0.9]})
    # Blickrichtungen wie im Spiel (x rechts, y oben, z vorn; Linkssystem): von oben mit Bug rechts liegt die linke
    # Seite oben, von rechts mit Bug rechts, von vorn liegt die rechte Seite links im Bild
    sichten = (("von oben (Bug rechts, linke Seite oben)", lambda v: (v[2], -v[0]), lambda t: t.vp[1], "z (vorn)", "-x (links)"),
               ("von rechts (Bug rechts)", lambda v: (v[2], v[1]), lambda t: t.vp[0], "z (vorn)", "y (oben)"),
               ("von vorn (rechte Seite links im Bild)", lambda v: (-v[0], v[1]), lambda t: t.vp[2], "-x (links)",
                "y (oben)"))
    for a, (titel, proj, tiefe, xl, yl) in zip(ax, sichten):
        a.set_xlabel(xl)
        a.set_ylabel(yl)
        # nach Tiefe sortieren, damit das Naeherliegende oben liegt
        ts = sorted(teile, key=tiefe)
        pts = [proj(t.vp) for t in ts]
        a.scatter([q[0] for q in pts], [q[1] for q in pts], c=[farbe(t) for t in ts], marker="s", s=16, linewidths=0)
        a.set_aspect("equal")
        a.set_title(titel)
        a.grid(alpha=.2)
    ax[0].legend(handles=[Patch(color=f, label=l) for _, f, l in ARTEN], loc="upper left", fontsize=8, ncol=4)
    fig.suptitle("%s - %d Teile, %d Koerper, %d Kabel (1 Kaestchen = 0,25 m)" % (
        os.path.basename(pfad), len(teile), len(F.koerper), len(F.kabel)))
    fig.tight_layout()
    os.makedirs(os.path.dirname(aus), exist_ok=True)
    fig.savefig(aus, dpi=80)
    print("gezeichnet:", aus)


def vorschau_raeder(F, durchmesser=11, breite=3):
    """Nur fuers Bild: Raeder (Reifen schwarz, Felge grau) an allen Wellen-Stummeln, wie nach raeder.py."""
    import raeder
    r2 = (durchmesser / 2) ** 2
    out = []
    for seite, s in raeder.stummel(F):
        sx = -1 if seite == "L" else 1
        n = int(durchmesser // 2) + 1
        for dx in range(1, breite + 1):
            for dy in range(-n, n + 1):
                for dz in range(-n, n + 1):
                    q = dy * dy + dz * dz
                    if q <= r2:
                        f = "6B6B6B" if q <= r2 * .2 or (dx == breite and q <= r2 * .45) else "1E1E1E"
                        out.append(fz.Teil('<c><o bc="%s" ac="%s" sc="6">%s</o></c>' % (
                            f, f, fz.vox("vp", (s[0] + sx * dx, s[1] + dy, s[2] + dz)))))
    return out


def schraeg(pfad, aus, rechts=True, markiert=(), titel=None, ausschnitt=None, beschriftung=(), raeder=False):
    """Schraegbild (isometrisch, von vorn rechts oben): jedes Teil als Wuerfel, hinten zuerst gezeichnet.
    beschriftung: [(Text, (x, y, z), (dx, dy) Versatz des Textes in Bildpunkten)] - Pfeil vom Text zum Ort.
    raeder: Vorschau-Raeder (11 Bloecke) an die Wellen malen (nur im Bild)."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.collections import PolyCollection
    import matplotlib.colors as mc
    F = fz.Fahrzeug.lesen(pfad)
    teile = [t for _, ts in F.koerper for t in ts]
    if raeder:
        teile += vorschau_raeder(F)
    sx = 1 if rechts else -1
    # Projektion: x nach rechts-unten, z nach rechts-oben, y nach oben
    cx, cz = 0.866, 0.5

    def p(x, y, z):
        # Blick aus Richtung (sx, +1, +1), wie eine Kamera im Spiel (Linkssystem: x rechts, y oben, z vorn).
        # Von vorn rechts liegt der Bug rechts im Bild, von vorn links links. Naeher = groesseres sx*x+z -> weiter unten
        return ((sx * z - x) * cx, y - (sx * x + z) * cz)
    belegt = {t.vp for t in teile}
    polys, farben = [], []
    if ausschnitt:
        lo, hi = ausschnitt
        teile = [t for t in teile if all(lo[i] <= t.vp[i] <= hi[i] for i in range(3))]
        belegt = {t.vp for t in teile}
    for t in sorted(teile, key=lambda t: t.vp[2] + sx * t.vp[0] + t.vp[1]):
        x, y, z = t.vp
        f = mc.to_rgb("#ff00ff" if t.vp in markiert else farbe(t))
        flaechen = []
        if (x, y + 1, z) not in belegt:     # oben
            flaechen.append(([p(x - .5, y + .5, z - .5), p(x + .5, y + .5, z - .5), p(x + .5, y + .5, z + .5),
                              p(x - .5, y + .5, z + .5)], 1.0))
        if (x + sx, y, z) not in belegt:    # Seite (rechts)
            xs = x + .5 * sx
            flaechen.append(([p(xs, y - .5, z - .5), p(xs, y + .5, z - .5), p(xs, y + .5, z + .5), p(xs, y - .5, z + .5)], .7))
        if (x, y, z + 1) not in belegt:     # vorn
            flaechen.append(([p(x - .5, y - .5, z + .5), p(x + .5, y - .5, z + .5), p(x + .5, y + .5, z + .5),
                              p(x - .5, y + .5, z + .5)], .85))
        for poly, hell in flaechen:
            polys.append(poly)
            farben.append(tuple(min(1, c * hell) for c in f))
    # Malreihenfolge: wie die Teile sortiert sind (hinten-links-unten zuerst)
    reihen = range(len(polys))
    fig, ax = plt.subplots(figsize=(16, 10))
    ax.add_collection(PolyCollection([polys[i] for i in reihen], facecolors=[farben[i] for i in reihen], edgecolors="none"))
    for txt, ort, (dx, dy) in beschriftung:
        ax.annotate(txt, xy=p(*ort), xytext=(dx, dy), textcoords="offset points", fontsize=11, ha="center",
                    bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="0.3", alpha=0.9),
                    arrowprops=dict(arrowstyle="->", color="0.1", lw=1.2))
    ax.autoscale()
    ax.set_aspect("equal")
    ax.axis("off")
    fig.suptitle(titel or "KI Landkreuzer - Schraegbild von vorn %s oben (Raeder fehlen noch: setzt Andre, siehe LANDKREUZER.md)"
                 % ("rechts" if rechts else "links"))
    fig.tight_layout()
    fig.savefig(aus, dpi=90)
    print("gezeichnet:", aus)


# Was wo ist (Blick von vorn links): Text, Ort, Versatz des Textes
BESCHRIFTUNG = [
    ("AC-Turm (vorn, Panzerbrechend)", (0, 9, 34), (-60, 90)),
    ("BC-Turm (2 Rohre, Sprenggranaten)", (0, 14, 9), (-150, 110)),
    ("Bruecke: Sitz, Monitore, Instrumente", (-6, 22, -6), (-90, 150)),
    ("Radarmast (6 Phalanx-Radare)", (-5, 26, -24), (60, 150)),
    ("Dachkamera + Radarwarner", (0, 33, -15), (-40, 110)),
    ("Chaff-Werfer (links und rechts)", (-10, 12, -30), (200, 120)),
    ("Flak L und Flak R (je 2 Rohre)", (-10, 13, -57), (90, 110)),
    ("Laser vorn (3 Stueck, + unten)", (-14, 3, 41), (-120, -60)),
    ("Laser Seite (je einer, auf Ausleger)", (-19, 6, -8), (-100, -90)),
    ("Wellen fuer die Raeder (7 je Seite)", (-15, -3, 5), (60, -100)),
    ("Kennung KL-1", (-15, 5, -16), (160, -90)),
]


def alle_bilder():
    """Alle Bilder in landkreuzer/bilder neu zeichnen (nach bau_landkreuzer.py und bau_landkreuzer.py --lenkung)."""
    sys.path.insert(0, HIER)
    import bau_landkreuzer as B
    fzg = os.path.join(LK, "fahrzeug")
    bi = os.path.join(LK, "bilder")
    einfach, lenk = os.path.join(fzg, "KI Landkreuzer.xml"), os.path.join(fzg, "KI Landkreuzer Lenkung.xml")
    zeichnen(einfach, os.path.join(bi, "ansicht.png"))
    schraeg(einfach, os.path.join(bi, "schraeg.png"))
    schraeg(einfach, os.path.join(bi, "schraeg_links.png"), rechts=False)
    if os.path.exists(lenk):
        schraeg(lenk, os.path.join(bi, "schraeg_lenkung.png"),
                titel="KI Landkreuzer Lenkung - vordere und hintere Achsen auf Gelenken (Raeder setzt Andre)")
    schraeg(einfach, os.path.join(bi, "beschriftet.png"), rechts=False, beschriftung=BESCHRIFTUNG,
            titel="KI Landkreuzer - was wo ist (von vorn links)")
    schraeg(einfach, os.path.join(bi, "rad_stummel.png"), rechts=False, markiert={(-B.X1, B.ACHSE_Y, B.RAD_Z[0])},
            ausschnitt=((-16, -5, 10), (0, 12, 48)),
            titel="Hier das EINE Rad ansetzen: pinker Wellen-Stummel links vorn (x -15, y -3, z 35), Blick von vorn links")
    schraeg(einfach, os.path.join(bi, "vorschau_raeder.png"), rechts=False, raeder=True,
            titel="KI Landkreuzer - so etwa sieht er mit Raedern aus (Vorschau: 11er-Raeder nur gemalt, setzt Andre)")
    if os.path.exists(lenk):
        schraeg(lenk, os.path.join(bi, "vorschau_raeder_lenkung.png"), raeder=True,
                titel="KI Landkreuzer Lenkung mit Raedern (Vorschau, von vorn rechts; vordere/hintere Achsen lenken)")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        pf = sys.argv[1]
        au = sys.argv[2] if len(sys.argv) > 2 else os.path.join(LK, "bilder", "ansicht.png")
        zeichnen(pf, au)
    else:
        alle_bilder()
