"""Pruefstand fuer raeder.py: setzt (wie Andre im Editor) ein Rad an den vorderen linken Stummel einer frisch gebauten
Datei, laesst raeder.py --schreiben laufen und prueft: 14 Raeder, je eins vor jedem Stummel, rechts gespiegelt, im
richtigen Koerper (Lenk-Variante: Gelenk-Koerper), nichts sonst veraendert, Sicherung angelegt.
Dazu: Vorlage auch rechts gesetzt (dann nimmt er die), kein Rad gesetzt (Fehlermeldung), zweiter Lauf.
Aufruf: python landkreuzer/tools/test_raeder.py
"""
import contextlib
import io
import os
import shutil
import sys
import tempfile

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
import fz  # noqa: E402
import raeder  # noqa: E402

DATEIEN = {"Skid": "KI Landkreuzer.xml", "Lenkung": "KI Landkreuzer Lenkung.xml"}
# ein Rad wie aus dem Editor: lokale z-Achse (Anschluss) zeigt zum Rumpf (Welt -x), Mitte 2 Bloecke neben der Welle
RAD_R = "0,0,1,0,1,0,-1,0,0"


def rad(d, vp, t=0):
    return fz.Teil('<c d="%s"%s><o r="%s" sc="6">%s</o></c>' % (d, ' t="%d"' % t if t else "", RAD_R, fz.vox("vp", vp)))


def koerper_von(F):
    k = {}
    for bi, (_, ts) in enumerate(F.koerper):
        for t in ts:
            k.setdefault(t.vp, bi)
    return k


def lauf(pfad, args):
    alt = sys.argv
    sys.argv = ["raeder.py", "--datei", pfad] + args
    out = io.StringIO()
    try:
        with contextlib.redirect_stdout(out):
            raeder.main()
        return True, out.getvalue()
    except SystemExit as e:
        return False, str(e)
    finally:
        sys.argv = alt


def vorbereiten(ordner, name, rechts_auch=False, kappe=False, nur_rechts=False):
    txt = open(os.path.join(os.path.dirname(HIER), "fahrzeug", name), encoding="utf-8").read()
    F = fz.Fahrzeug(txt)
    st = raeder.stummel(F)
    kv = koerper_von(F)
    koerper = [(k, list(ts)) for k, ts in F.koerper]
    _, sl = max((q for q in st if q[0] == "L"), key=lambda q: q[1][2])
    if not nur_rechts:
        koerper[kv[sl]][1].append(rad("wheel_test", fz.add(sl, (-2, 0, 0))))
    if kappe:
        koerper[kv[sl]][1].append(rad("wheel_test_kappe", fz.add(sl, (-4, 0, 0))))
    if rechts_auch or nur_rechts:
        _, sr = max((q for q in st if q[0] == "R"), key=lambda q: q[1][2])
        koerper[kv[sr]][1].append(rad("wheel_test_r", fz.add(sr, (3, 0, 0)), t=4))
    pfad = os.path.join(ordner, name)
    open(pfad, "w", encoding="utf-8", newline="").write(fz.schreiben(F.kopf, koerper, F.kabel, F.fuss))
    return pfad, F, st, kv


def pruefen(variante, name, ordner):
    rueck = []
    pfad, F0, st, kv = vorbereiten(ordner, name)
    ok, aus = lauf(pfad, [])
    rueck.append(("%s: Probelauf aendert nichts" % variante,
                  ok and "13 Raeder kommen dazu (13 Teile)" in aus and open(pfad, encoding="utf-8").read().count("wheel_test") == 1))
    ok, aus = lauf(pfad, ["--schreiben"])
    F = fz.Fahrzeug(open(pfad, encoding="utf-8").read())
    raeder_neu = [(bi, t) for bi, (_, ts) in enumerate(F.koerper) for t in ts if t.d.startswith("wheel_")]
    rueck.append(("%s: 14 Raeder in der Datei" % variante, ok and len(raeder_neu) == 14))
    fehl = []
    for seite, s in st:
        soll = fz.add(s, (-2, 0, 0) if seite == "L" else (2, 0, 0))
        da = [(bi, t) for bi, t in raeder_neu if t.vp == soll]
        if len(da) != 1:
            fehl.append("%s %s: kein Rad bei %s" % (seite, s, soll))
            continue
        bi, t = da[0]
        if bi != kv[s]:
            fehl.append("%s %s: Rad in Koerper %d statt %d" % (seite, s, bi, kv[s]))
        if t.t != (4 if seite == "R" else 0) or t.r != tuple(int(v) for v in RAD_R.split(",")):
            fehl.append("%s %s: Spiegelung t=%d" % (seite, s, t.t))
        # das gespiegelte Rad muss mit seinem Anschluss (lokal z) zum Rumpf zeigen: Welt +x links, -x rechts
        a = fz.sub(t.lokal_zu_welt((0, 0, 1)), t.vp)
        if a[0] * (1 if seite == "L" else -1) >= 0:
            fehl.append("%s %s: Anschluss zeigt nach aussen %s" % (seite, s, a))
    rueck.append(("%s: je Stummel ein Rad, Koerper und Spiegelung richtig%s" % (
        variante, "" if not fehl else " - " + "; ".join(fehl[:3])), not fehl))
    rest0 = sorted((t.d, t.vp) for _, ts in F0.koerper for t in ts)
    rest1 = sorted((t.d, t.vp) for _, ts in F.koerper for t in ts if not t.d.startswith("wheel_"))
    rueck.append(("%s: sonst nichts veraendert (%d Teile, %d Kabel, %d Koerper)" % (
        variante, len(rest1), len(F.kabel), len(F.koerper)),
        rest0 == rest1 and len(F.kabel) == len(F0.kabel) and len(F.koerper) == len(F0.koerper)))
    sich = os.path.splitext(pfad)[0] + " vor Raeder.xml"
    rueck.append(("%s: Sicherung angelegt (mit nur 1 Rad)" % variante,
                  os.path.exists(sich) and open(sich, encoding="utf-8").read().count("wheel_test") == 1))
    ok, aus = lauf(pfad, ["--schreiben"])
    F2 = fz.Fahrzeug(open(pfad, encoding="utf-8").read())
    n2 = sum(1 for _, ts in F2.koerper for t in ts if t.d.startswith("wheel_"))
    rueck.append(("%s: zweiter Lauf setzt keine doppelten Raeder (%d)" % (variante, n2),
                  ok and n2 == 14 and "nichts zu tun" in aus))
    os.remove(pfad)
    os.remove(sich)
    # Vorlage auch rechts: dann nimmt er die (andere Art, 3 Bloecke Abstand)
    pfad, F0, st, kv = vorbereiten(ordner, name, rechts_auch=True)
    ok, aus = lauf(pfad, ["--schreiben"])
    F = fz.Fahrzeug(open(pfad, encoding="utf-8").read())
    r = [t for _, ts in F.koerper for t in ts if t.d == "wheel_test_r"]
    rueck.append(("%s: rechte Vorlage wird rechts benutzt (%d Raeder)" % (variante, len(r)),
                  ok and len(r) == 7 and all(t.vp in {fz.add(s, (3, 0, 0)) for q, s in st if q == "R"} for t in r)))
    os.remove(pfad)
    # Rad aus zwei Teilen (Rad + Kappe): beide werden kopiert, rechts gespiegelt
    pfad, F0, st, kv = vorbereiten(ordner, name, kappe=True)
    ok, aus = lauf(pfad, ["--schreiben"])
    F = fz.Fahrzeug(open(pfad, encoding="utf-8").read())
    k = {t.vp for _, ts in F.koerper for t in ts if t.d == "wheel_test_kappe"}
    rueck.append(("%s: Rad aus zwei Teilen ganz kopiert (%d Kappen)" % (variante, len(k)),
                  ok and k == {fz.add(s, (-4, 0, 0) if q == "L" else (4, 0, 0)) for q, s in st}))
    os.remove(pfad)
    # nur rechts gesetzt: links wird gespiegelt
    pfad, F0, st, kv = vorbereiten(ordner, name, nur_rechts=True)
    ok, aus = lauf(pfad, ["--schreiben"])
    F = fz.Fahrzeug(open(pfad, encoding="utf-8").read())
    lk = {(t.vp, t.t) for _, ts in F.koerper for t in ts if t.d == "wheel_test_r" and t.vp[0] < 0}
    rueck.append(("%s: nur rechts gesetzt - links gespiegelt (%d)" % (variante, len(lk)),
                  ok and lk == {(fz.add(s, (-3, 0, 0)), 0) for q, s in st if q == "L"}))
    os.remove(pfad)
    # kein Rad gesetzt
    shutil.copyfile(os.path.join(os.path.dirname(HIER), "fahrzeug", name), pfad)
    ok, aus = lauf(pfad, ["--schreiben"])
    rueck.append(("%s: ohne Rad klare Meldung, Datei unveraendert" % variante,
                  not ok and "Kein Rad" in aus and "wheel_" not in open(pfad, encoding="utf-8").read()))
    return rueck


def main():
    ordner = tempfile.mkdtemp(prefix="raeder_")
    rueck = []
    for variante, name in DATEIEN.items():
        rueck += pruefen(variante, name, ordner)
    shutil.rmtree(ordner, ignore_errors=True)
    ok = True
    for t, g in rueck:
        print("%-100s %s" % (t, "ok" if g else "FEHLER"))
        ok &= bool(g)
    print("ALLES OK" if ok else "FEHLER")
    return ok


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
