"""Zeichnet ein Stormworks-Fahrzeug von oben, von der Seite und von vorn (PNG), zum Ansehen ohne Spiel.

Aufruf (mit matplotlib): python landkreuzer/tools/ansicht.py [Fahrzeug.xml] [Ausgabe.png]
Standard: landkreuzer/fahrzeug/KI Landkreuzer.xml -> landkreuzer/bilder/ansicht.png
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
    for a, (i, j, titel) in zip(ax, ((2, 0, "von oben (vorn rechts)"), (2, 1, "von links (vorn rechts)"),
                                     (0, 1, "von vorn"))):
        # nach Tiefe sortieren, damit das Naeherliegende oben liegt
        k = ({0: 1, 1: 0, 2: 1}[i] if titel != "von vorn" else 2)
        tiefe = (lambda t: t.vp[1]) if titel.startswith("von oben") else (
            (lambda t: -t.vp[0]) if titel.startswith("von links") else (lambda t: t.vp[2]))
        ts = sorted(teile, key=tiefe)
        a.scatter([t.vp[i] for t in ts], [t.vp[j] for t in ts], c=[farbe(t) for t in ts], marker="s", s=16, linewidths=0)
        a.set_aspect("equal")
        a.set_title(titel)
        a.grid(alpha=.2)
        _ = k
    ax[0].legend(handles=[Patch(color=f, label=l) for _, f, l in ARTEN], loc="upper left", fontsize=8, ncol=4)
    fig.suptitle("%s - %d Teile, %d Koerper, %d Kabel (1 Kaestchen = 0,25 m)" % (
        os.path.basename(pfad), len(teile), len(F.koerper), len(F.kabel)))
    fig.tight_layout()
    os.makedirs(os.path.dirname(aus), exist_ok=True)
    fig.savefig(aus, dpi=80)
    print("gezeichnet:", aus)


if __name__ == "__main__":
    pf = sys.argv[1] if len(sys.argv) > 1 else os.path.join(LK, "fahrzeug", "KI Landkreuzer.xml")
    au = sys.argv[2] if len(sys.argv) > 2 else os.path.join(LK, "bilder", "ansicht.png")
    zeichnen(pf, au)
