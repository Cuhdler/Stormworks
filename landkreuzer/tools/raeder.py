"""Raeder an den KI-Landkreuzer: Andre setzt im Editor EIN Rad an den vorderen linken Wellen-Stummel (das Rad muss
an der Welle haengen, die aus der linken Seitenwand kommt, vorderste Achse) und speichert. Dieses Programm kopiert
das Rad an alle 14 Stummel (links gleich, rechts gespiegelt). Hat Andre auch rechts vorn ein Rad gesetzt, nimmt es
fuer rechts dieses als Vorlage (nur rechts gesetzt geht auch, dann wird links gespiegelt).

Aufruf auf dem PC (im Repo-Ordner):
    python landkreuzer/tools/raeder.py              Probelauf: zeigt, was es tun wuerde
    python landkreuzer/tools/raeder.py --schreiben  schreibt (vorher Sicherung "KI Landkreuzer vor Raeder.xml")
Danach im Spiel das Fahrzeug NEU LADEN, ohne vorher zu speichern.
Lenk-Variante: --lenkung (Datei "KI Landkreuzer Lenkung.xml"); eine andere Datei: --datei "C:/.../Name.xml"
Ein Rad aus mehreren Teilen (z. B. Rad + Kappe) wird als Ganzes kopiert. Stummel, die schon ein Rad haben, bleiben,
wie sie sind - zweimal laufen lassen schadet also nicht.
"""
import os
import re
import shutil
import sys

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
import fz  # noqa: E402
from bau_landkreuzer import RAD_Z, ACHSE_Y, X1  # noqa: E402

BEKANNT = ("multibody", "gun_", "radar", "camera", "laser", "microprocessor", "motor_", "trans_", "battery",
           "window", "seat", "monitor", "instrument", "button", "physics", "gate_", "door", "railing", "stair",
           "ladder", "flare", "rocket", "solid_", "warhead", "connector", "inventory", "sign", "control_fin",
           "small_light")


def stummel(F=None):
    """Wellen-Stummel (Seite, Position des aeussersten Wellen-Teils). Feste Achsen: Welle in der Seitenwand (x +-15);
    lenkbare Achsen (Variante mit Lenkung): Winkel-Welle aussen auf dem Gelenk-Koerper - gefunden ueber die
    Teile: aeusserstes trans_*-Teil je Achse und Seite auf Achs-Hoehe."""
    if F is None:
        return [("L", (-X1, ACHSE_Y, z)) for z in RAD_Z] + [("R", (X1, ACHSE_Y, z)) for z in RAD_Z]
    out = []
    for seite, sx in (("L", -1), ("R", 1)):
        for z in RAD_Z:
            kand = [t.vp for _, ts in F.koerper for t in ts
                    if t.d.startswith("trans_") and t.vp[1] == ACHSE_Y and t.vp[2] == z and t.vp[0] * sx >= X1]
            out.append((seite, max(kand, key=lambda p: p[0] * sx) if kand else (sx * X1, ACHSE_Y, z)))
    return out


def ist_neu(t):
    return t.d not in fz.STRUKTUR and not t.d.startswith(BEKANNT)


def gespiegelt(t, neu_vp):
    """Teil t an der Ebene x = 0 spiegeln: gleiche Drehung, Spiegel-Bit der lokalen Achse, die in Welt-x zeigt."""
    r = t.r
    achse = next(k for k in range(3) if r[3 * k] != 0)       # lokale Achse k zeigt in Welt-x (Spalte k: r[3k..3k+2])
    tneu = t.t ^ (1 << achse)
    x = t.xml
    m = re.match(r'<c( d="[^"]+")?( t="\d+")?><o', x)
    kopf = '<c%s%s><o' % (m.group(1) or "", ' t="%d"' % tneu if tneu else "")
    x = kopf + x[m.end():]
    return fz.Teil(x).verschoben(fz.sub(neu_vp, t.vp))


def main():
    pfad = None
    if "--datei" in sys.argv:
        pfad = sys.argv[sys.argv.index("--datei") + 1]
    else:
        pfad = os.path.join(os.environ.get("APPDATA", ""), "Stormworks", "data", "vehicles",
                            "KI Landkreuzer Lenkung.xml" if "--lenkung" in sys.argv else "KI Landkreuzer.xml")
    txt = open(pfad, encoding="utf-8", newline="").read()
    F = fz.Fahrzeug(txt)
    rumpf = max(range(len(F.koerper)), key=lambda k: len(F.koerper[k][1]))
    st = stummel(F)
    # Koerper je Stummel (bei lenkbaren Achsen sitzt der Stummel auf dem Gelenk-Koerper - das Rad muss dorthin)
    koerper_von = {}
    for bi, (_, ts) in enumerate(F.koerper):
        for t in ts:
            koerper_von.setdefault(t.vp, bi)
    gruppen = {}           # Stummel -> neue Teile daneben (ein Rad kann auch aus mehreren Teilen bestehen)
    for bi, (_, ts) in enumerate(F.koerper):
        for t in ts:
            if not ist_neu(t):
                continue
            seite, s = min(st, key=lambda q: max(abs(q[1][i] - t.vp[i]) for i in range(3)))
            d = max(abs(s[i] - t.vp[i]) for i in range(3))
            if d <= 10:
                print("gefunden: %s bei %s (Koerper %d), %d Bloecke vom Stummel %s %s" % (t.d, t.vp, bi, d, seite, s))
                gruppen.setdefault((seite, s), []).append(t)
    vorlagen = {}          # je Seite das Rad an der vordersten Achse
    for (seite, s), ts in gruppen.items():
        if seite not in vorlagen or s[2] > vorlagen[seite][1][2]:
            vorlagen[seite] = (ts, s)
    if not vorlagen:
        sys.exit("Kein Rad an einem Stummel gefunden. Bitte ein Rad an die vorderste linke Welle setzen und speichern.")
    besetzt = {s for _, s in gruppen}
    neue, gesetzt = [], []
    for seite, s in st:
        if s in besetzt:   # hat schon ein Rad (Vorlage, oder raeder.py lief schon einmal)
            continue
        ziel_k = koerper_von.get(s, rumpf)
        gesetzt.append(s)
        if seite in vorlagen:
            ts, s0 = vorlagen[seite]
            neue += [(ziel_k, t.verschoben(fz.sub(s, s0))) for t in ts]
        else:
            ts, s0 = vorlagen["R" if seite == "L" else "L"]     # die andere Seite, gespiegelt
            for t in ts:
                off = fz.sub(t.vp, s0)
                neue.append((ziel_k, gespiegelt(t, (s[0] - off[0], s[1] + off[1], s[2] + off[2]))))
    for bi, t in neue:
        if t.vp in {u.vp for u in F.koerper[bi][1]}:
            print("ACHTUNG: dort sitzt schon ein Teil:", t.vp)
    if not neue:
        print("Alle %d Stummel haben schon ein Rad - nichts zu tun." % len(st))
        return
    print("%d Raeder kommen dazu (%d Teile), an die Stummel %s." % (len(gesetzt), len(neue),
                                                                   ", ".join(str(s) for s in gesetzt)))
    if "--schreiben" not in sys.argv:
        print("Probelauf - mit --schreiben wird die Datei geaendert.")
        return
    koerper = [(k, list(ts)) for k, ts in F.koerper]
    for bi, t in neue:
        koerper[bi][1].append(t)
    neu_txt = fz.schreiben(F.kopf, koerper, F.kabel, F.fuss)
    sich = os.path.splitext(pfad)[0] + " vor Raeder.xml"
    shutil.copyfile(pfad, sich)
    open(pfad, "w", encoding="utf-8", newline="").write(neu_txt)
    print("geschrieben:", pfad, "(Sicherung:", sich + ")")
    print("Jetzt im Spiel das Fahrzeug neu laden, OHNE vorher zu speichern.")


if __name__ == "__main__":
    main()
