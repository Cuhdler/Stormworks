"""Wertet einen Fahrtenschreiber-Log der KI aus (logs/waffen_<Datum>_<Zeit>/ki.csv, siehe LANDKREUZER.md, Schnellstart):
Zusammenfassung als Text und ein Bild (Fahrspur nach Zustand gefaerbt, Tempo, Laser, Batterie, Neigung).

Aufruf: python landkreuzer/tools/ki_log.py <Ordner oder ki.csv> [Bild.png]
        ohne Bild-Name: <Ordner>/ki_auswertung.png (braucht matplotlib)
"""
import math
import os
import sys

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HIER)), "tools"))
from schreiber_spalten import lade  # noqa: E402

ZUSTAENDE = ["AUS", "HAND", "WEGPUNKT", "REVIER", "AUSWEICHEN", "ZURUECK", "KAMPF", "BATTERIE", "GEFAHR", "WARTET",
             "LASER?"]
FARBEN = ["#999999", "#1f77b4", "#2ca02c", "#17becf", "#ff7f0e", "#9467bd", "#d62728", "#8c564b", "#e377c2",
          "#bcbd22", "#000000"]
LASER = [("laser_vl", "vorn links"), ("laser_vm", "vorn Mitte"), ("laser_vr", "vorn rechts"), ("laser_li", "links"),
         ("laser_re", "rechts"), ("laser_un", "unten"), ("laser_hi", "hinten")]


def zusammenfassung(z):
    """z: Zeilen (dicts) -> Liste von Textzeilen"""
    out = []
    t0, t1 = z[0]["tick"], z[-1]["tick"]
    dauer = (t1 - t0) / 60
    weg = sum(math.hypot(b["x"] - a["x"], b["z"] - a["z"]) for a, b in zip(z, z[1:])
              if math.hypot(b["x"] - a["x"], b["z"] - a["z"]) < 5)
    out.append("Dauer %.0f s (%d Zeilen), gefahren %.0f m, Ort von (%.0f, %.0f) bis (%.0f, %.0f)" % (
        dauer, len(z), weg, z[0]["x"], z[0]["z"], z[-1]["x"], z[-1]["z"]))
    zaehl = {}
    for d in z:
        k = int(round(d["zustand"]))
        zaehl[k] = zaehl.get(k, 0) + 1
    out.append("Zustaende: " + ", ".join("%s %.0f %%" % (ZUSTAENDE[k] if 0 <= k < len(ZUSTAENDE) else k,
                                                         100 * n / len(z)) for k, n in sorted(zaehl.items())))
    wechsel = [(d["tick"], int(round(d["zustand"]))) for a, d in zip(z, z[1:]) if round(a["zustand"]) != round(d["zustand"])]
    out.append("Zustandswechsel: %d (erste: %s)" % (len(wechsel), ", ".join(
        "%.0fs %s" % ((t - t0) / 60, ZUSTAENDE[k] if 0 <= k < len(ZUSTAENDE) else k) for t, k in wechsel[:8])))
    vs = [d["v"] for d in z]
    out.append("Tempo: hoechstens %.1f m/s, im Mittel %.1f m/s (Soll im Mittel %.1f)" % (
        max(vs), sum(vs) / len(vs), sum(d["v_soll"] for d in z) / len(z)))
    for k, name in LASER:
        w = [d[k] for d in z]
        null = sum(1 for v in w if v == 0)
        nah = [v for v in w if 0 < v < 1000]
        out.append("Laser %-11s: %s%s" % (name, "nie eine Messung (0) - Kabel/Strom/Einschalten pruefen!" if null == len(w)
                                         else "kleinste %.1f m" % min(nah) if nah else "immer frei (>1 km)",
                                         "" if null in (0, len(w)) else ", %d mal 0" % null))
    b = [(d["tick"], d["batterie"]) for d in z if d["batterie"] > 0]
    if len(b) > 1 and b[-1][0] > b[0][0]:
        je_min = (b[0][1] - b[-1][1]) / ((b[-1][0] - b[0][0]) / 3600)
        out.append("Batterie: %.0f %% -> %.0f %%, Verbrauch %.2f %% je Minute%s" % (
            100 * b[0][1], 100 * b[-1][1], 100 * je_min,
            ", voll reicht also etwa %.0f Minuten" % (1 / je_min) if je_min > 0 else ""))
    else:
        out.append("Batterie: kein Wert (Eingang nicht angeschlossen?)")
    out.append("Nick %.0f..%.0f Grad, Roll %.0f..%.0f Grad (+ = Bug hoch / rechts tief)" % (
        min(d["nick"] for d in z), max(d["nick"] for d in z), min(d["roll"] for d in z), max(d["roll"] for d in z)))
    if any(d["umgelernt_l"] or d["umgelernt_r"] for d in z):
        out.append("ACHTUNG: Rad-Richtung umgelernt (links %s, rechts %s) - im KI-Chip 'Rad Richtung' umstellen" % (
            any(d["umgelernt_l"] for d in z), any(d["umgelernt_r"] for d in z)))
    out.append("Waffen frei %.0f %% der Zeit, Schutzzone sperrte %.0f %%, jemand im Sitz %.0f %%" % (
        100 * sum(d["waffen_frei"] for d in z) / len(z), 100 * sum(d["schutzzone"] for d in z) / len(z),
        100 * sum(d["sitz"] for d in z) / len(z)))
    return out


def bild(z, aus):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=(14, 11))
    ax = fig.add_subplot(2, 2, 1)
    for k in sorted({int(round(d["zustand"])) for d in z}):
        p = [d for d in z if int(round(d["zustand"])) == k]
        ax.scatter([d["x"] for d in p], [d["z"] for d in p], s=3, c=FARBEN[k % len(FARBEN)],
                   label=ZUSTAENDE[k] if 0 <= k < len(ZUSTAENDE) else str(k))
    ax.plot([z[0]["x"]], [z[0]["z"]], "k^", ms=10, label="Start")
    ax.set_aspect("equal")
    ax.set_title("Fahrspur (Ost/Nord, m) nach Zustand")
    ax.legend(fontsize=7, markerscale=3)
    t = [(d["tick"] - z[0]["tick"]) / 60 for d in z]
    ax = fig.add_subplot(2, 2, 2)
    ax.plot(t, [d["v"] for d in z], label="Tempo")
    ax.plot(t, [d["v_soll"] for d in z], label="Soll")
    ax.plot(t, [d["fahr"] * 5 for d in z], label="Fahrbefehl x5", alpha=.5)
    ax.plot(t, [d["lenk"] * 5 for d in z], label="Lenkbefehl x5", alpha=.5)
    ax.set_title("Tempo m/s und Befehle")
    ax.legend(fontsize=7)
    ax = fig.add_subplot(2, 2, 3)
    for k, name in LASER:
        ax.plot(t, [min(d[k], 60) for d in z], label=name, lw=.8)
    ax.set_ylim(0, 62)
    ax.set_title("Laser m (ab 60 abgeschnitten, 0 = keine Messung)")
    ax.legend(fontsize=7)
    ax = fig.add_subplot(2, 2, 4)
    ax.plot(t, [d["nick"] for d in z], label="Nick Grad")
    ax.plot(t, [d["roll"] for d in z], label="Roll Grad")
    ax.plot(t, [d["batterie"] * 100 for d in z], label="Batterie %")
    ax.set_title("Neigung und Batterie")
    ax.legend(fontsize=7)
    for a in fig.axes:
        a.grid(alpha=.3)
    fig.tight_layout()
    fig.savefig(aus, dpi=80)
    return aus


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    p = sys.argv[1]
    ordner = os.path.dirname(p) if p.endswith(".csv") else p
    z = lade(ordner, "ki")
    if len(z) < 2:
        sys.exit("zu wenige Zeilen in %s" % os.path.join(ordner, "ki.csv"))
    for zeile in zusammenfassung(z):
        print(zeile)
    try:
        print("Bild:", bild(z, sys.argv[2] if len(sys.argv) > 2 else os.path.join(ordner, "ki_auswertung.png")))
    except ImportError:
        print("(kein Bild: matplotlib fehlt)")


if __name__ == "__main__":
    main()
