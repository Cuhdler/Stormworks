"""Raeder an den KI-Landkreuzer: Andre setzt im Editor EIN Rad an den vorderen linken Wellen-Stummel (das Rad muss
an der Welle haengen, die aus der linken Seitenwand kommt, vorderste Achse) und speichert. Dieses Programm kopiert
das Rad an alle 14 Stummel (links gleich, rechts gespiegelt). Hat Andre auch rechts vorn ein Rad gesetzt, nimmt es
fuer rechts dieses als Vorlage.

Aufruf auf dem PC (im Repo-Ordner):
    python landkreuzer/tools/raeder.py              Probelauf: zeigt, was es tun wuerde
    python landkreuzer/tools/raeder.py --schreiben  schreibt (vorher Sicherung "KI Landkreuzer vor Raeder.xml")
Danach im Spiel das Fahrzeug NEU LADEN, ohne vorher zu speichern.
Eine andere Datei: --datei "C:/.../KI Landkreuzer.xml"
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
           "ladder", "flare", "rocket", "solid_", "warhead", "connector", "inventory", "sign", "control_fin")


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
        pfad = os.path.join(os.environ.get("APPDATA", ""), "Stormworks", "data", "vehicles", "KI Landkreuzer.xml")
    txt = open(pfad, encoding="utf-8", newline="").read()
    F = fz.Fahrzeug(txt)
    rumpf = max(range(len(F.koerper)), key=lambda k: len(F.koerper[k][1]))
    st = stummel(F)
    # Koerper je Stummel (bei lenkbaren Achsen sitzt der Stummel auf dem Gelenk-Koerper - das Rad muss dorthin)
    koerper_von = {}
    for bi, (_, ts) in enumerate(F.koerper):
        for t in ts:
            koerper_von.setdefault(t.vp, bi)
    vorlagen = {}
    for bi, (_, ts) in enumerate(F.koerper):
        for t in ts:
            if not ist_neu(t):
                continue
            seite, s = min(st, key=lambda q: max(abs(q[1][i] - t.vp[i]) for i in range(3)))
            d = max(abs(s[i] - t.vp[i]) for i in range(3))
            if d <= 10:
                print("gefunden: %s bei %s (Koerper %d), %d Bloecke vom Stummel %s %s" % (t.d, t.vp, bi, d, seite, s))
                vorlagen.setdefault(seite, (t, s, bi))
    if "L" not in vorlagen:
        sys.exit("Kein Rad am linken Stummel gefunden. Bitte ein Rad an die vorderste linke Welle setzen und speichern.")
    neue = []
    for seite, s in st:
        ziel_k = koerper_von.get(s, rumpf)
        if seite in vorlagen:
            t, s0, bi = vorlagen[seite]
            if s == s0:
                continue
            neue.append((ziel_k, t.verschoben(fz.sub(s, s0))))
        else:
            t, s0, bi = vorlagen["L"]
            off = fz.sub(t.vp, s0)
            ziel = (s[0] - off[0], s[1] + off[1], s[2] + off[2])
            neue.append((ziel_k, gespiegelt(t, ziel)))
    belegt = {t.vp for t in F.koerper[rumpf][1]}
    for bi, t in neue:
        if bi == rumpf and t.vp in belegt:
            print("ACHTUNG: dort sitzt schon ein Teil:", t.vp)
    print("%d Raeder kommen dazu (%s)." % (len(neue), ", ".join(str(t.vp) for _, t in neue)))
    if "--schreiben" not in sys.argv:
        print("Probelauf - mit --schreiben wird die Datei geaendert.")
        return
    koerper = [(k, list(ts)) for k, ts in F.koerper]
    for bi, t in neue:
        koerper[bi][1].append(t)
    neu_txt = fz.schreiben(F.kopf, koerper, F.kabel, F.fuss)
    sich = os.path.join(os.path.dirname(pfad), "KI Landkreuzer vor Raeder.xml")
    shutil.copyfile(pfad, sich)
    open(pfad, "w", encoding="utf-8", newline="").write(neu_txt)
    print("geschrieben:", pfad, "(Sicherung:", sich + ")")
    print("Jetzt im Spiel das Fahrzeug neu laden, OHNE vorher zu speichern.")


if __name__ == "__main__":
    main()
