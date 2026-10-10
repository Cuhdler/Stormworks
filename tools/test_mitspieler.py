"""Prueft MITSPIELER (lua/mitspieler.lua, Bildschirm-Chip v3.7) im Rechner:
- Host: alle echten Lage-Logs seit 04.10. (logs/waffen_*/la.csv, jede Zeile als EIN Tick - viermal enger als im Spiel,
  also strenger) - der Mitspieler-Modus darf nie anspringen, jeder Wert muss unveraendert durchgehen.
- Host mit Stoerungen: Takt der Lage fehlt alle 30 s einmal, Lage haengt 5 s - nichts darf sich aendern.
- Mitspieler (Modell, im Spiel noch unbestaetigt): vom Host kommt nur alle N Ticks ein Zwischenstand (mit seinem Takt),
  dazwischen meldet der eigene Chip leere Plaetze (oder ein eigenes Ziel) - Modus muss anspringen, Host-Ziele halten.
- 'Mehrspieler-Hilfe' 0: immer nur durchreichen. Anzeige 'MP' nur im Mitspieler-Modus.
Aufruf: python tools/test_mitspieler.py   (braucht lupa wie die anderen Pruefstaende)
"""
import csv
import glob
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from test_schiff import load, pruefe  # noqa: E402
from build_lage import MP_PROPS  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PR = {n: v for n, v, _ in MP_PROPS}


def zahl(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return 0.0


def lage_zeilen(pfad):
    """la.csv -> Liste von (Zahlen, Bools) wie im Composite der Lage (leer im Log = 0)."""
    out = []
    for r in csv.DictReader(open(pfad, encoding="utf-8")):
        n, b = {}, {}
        for k in range(1, 6):
            i = zahl(r.get("p%d_id" % k))
            art = int(zahl(r.get("p%d_art" % k)))
            n[3 * k - 2], n[3 * k - 1], n[3 * k] = zahl(r.get("p%d_ost" % k)), zahl(r.get("p%d_nord" % k)), zahl(r.get("p%d_hoehe" % k))
            n[15 + k] = i
            b[k], b[5 + k], b[15 + k] = i > 0, art & 1 == 1, art & 2 == 2
        n[31], n[32] = zahl(r.get("kurs")), zahl(r.get("hoehe"))
        b[25] = zahl(r.get("bedrohung")) > 0
        out.append((n, b))
    return out


class Filter:
    def __init__(self, props=PR):
        _, self.g, self.io = load("mitspieler.lua", props)
        self.g.screen.drawRectF = lambda *a: None

    def tick(self, n, b):
        self.io["n"], self.io["b"] = n, b
        self.io["on"].clear()
        self.g.onTick()
        o = self.io["on"]
        return {i: o.get(i, 0.0) for i in range(1, 33)}, {i: bool(o.get(100 + i, False)) for i in range(1, 33)}

    def malt(self):
        self.io["draw"].clear()
        self.g.onDraw()
        return list(self.io["draw"])


def takt(b, c):
    """Takt der Lagezentrale (v3.4) auf Bool 21-24."""
    b = dict(b)
    for i in range(4):
        b[21 + i] = (c >> i) & 1 == 1
    return b


def test_host():
    logs = sorted(glob.glob(os.path.join(ROOT, "logs", "waffen_*", "la.csv")))
    zeilen, an, falsch, fahrten = 0, 0, 0, 0
    for p in logs:
        try:
            Z = lage_zeilen(p)
        except Exception:
            continue
        if not Z or 16 not in Z[0][0]:
            continue
        fahrten += 1
        f = Filter()
        for t, (n, b) in enumerate(Z):
            b = takt(b, t % 16)
            on, ob = f.tick(n, b)
            zeilen += 1
            an += bool(f.g.cm)
            if any(on[i] != n.get(i, 0.0) for i in range(1, 33)) or any(ob[i] != b.get(i, False) for i in range(1, 33)):
                falsch += 1
        malt = f.malt()
    # Stoerungen beim Host: alle 30 s fehlt ein Takt; Lagezentrale haengt 5 s (alles steht)
    Z = lage_zeilen(os.path.join(ROOT, "logs", "waffen_20261009_183744", "la.csv"))[15000:20000]
    f, an2, falsch2, c = Filter(), 0, 0, 0
    for t, (n, b) in enumerate(Z):
        c = (c + (2 if t % 1800 == 0 else 1)) % 16
        if 3000 <= t < 3300:
            n, b = Z[3000]
            c = 5
        b = takt(b, c)
        on, ob = f.tick(n, b)
        an2 += bool(f.g.cm)
        if any(on[i] != n.get(i, 0.0) for i in range(1, 33)) or any(ob[i] != b.get(i, False) for i in range(1, 33)):
            falsch2 += 1
    return pruefe([
        ("Host: %d Log-Zeilen aus %d Fahrten, Mitspieler-Modus %d mal" % (zeilen, fahrten, an), zeilen > 100000 and an == 0),
        ("Host: jeder Wert unveraendert durchgereicht (%d Abweichungen)" % falsch, falsch == 0),
        ("Host: keine Anzeige 'MP'", malt == []),
        ("Host mit Stoerungen (Takt fehlt alle 30 s, Lage haengt 5 s): Modus %d mal, %d Abweichungen" % (an2, falsch2),
         falsch2 == 0),
    ])


def mitspieler(Z, alle, dauer=1, eigenes=False, props=PR, versatz=7):
    """Mitspieler-Modell (im Spiel unbestaetigt): Zeile = 4 Ticks wie im Spiel; alle 'alle' Ticks kommt fuer 'dauer'
    Ticks der Stand des Hosts (mit seinem Takt), sonst meldet die eigene Lage leere Plaetze (eigenes=True: ein eigenes
    Ziel auf Platz 3, Kennung 9000) mit dem eigenen Takt."""
    f = Filter(props)
    erkannt, gesamt, gezeigt, richtig = None, 0, 0, True
    letzter = {}
    t = 0
    for n, b in Z:
        for _ in range(4):
            t += 1
            if t % alle < dauer:
                ni, bi = dict(n), takt(b, (t + versatz) % 16)
                for k in range(1, 6):
                    letzter[k] = (n[3 * k - 2], n[15 + k], b[k])
            else:
                ni = {i: (n.get(i, 0.0) if i > 20 else 0.0) for i in range(1, 33)}
                bi = takt({i: (b.get(i, False) if i > 25 else False) for i in range(1, 33)}, t % 16)
                if eigenes:
                    ni[7], ni[8], ni[9], ni[18], bi[3] = 100.0, 200.0, 5.0, 9000.0, True
            on, ob = f.tick(ni, bi)
            if f.g.cm and erkannt is None:
                erkannt = t
            if erkannt is not None:
                for k in range(1, 6):
                    if b[k]:
                        gesamt += 1
                        gezeigt += ob[k] and on[15 + k] == n[15 + k]
                    if k in letzter and ob[k] and on[15 + k] == letzter[k][1] and on[3 * k - 2] != letzter[k][0]                             and on[15 + k] != 9000:
                        richtig = False
    return erkannt, gezeigt / max(gesamt, 1), richtig, f


def test_mitspieler():
    p = os.path.join(ROOT, "logs", "waffen_20261009_183744", "la.csv")
    Z = lage_zeilen(p)[15000:22500]          # 7500 Zeilen * 4 Ticks = ca. 8 min Fahrt vom 09.10. mit 2-4 Zielen
    ok = True
    for alle, dauer in ((30, 1), (120, 1), (300, 1), (600, 1), (120, 3)):
        erkannt, anteil, richtig, f = mitspieler(Z, alle, dauer)
        malt = f.malt()
        ok &= pruefe([
            ("Mitspieler, Stand alle %3d Ticks (%d Tick lang): erkannt nach %s s, Host-Ziele zu %3.0f %% sichtbar" % (
                alle, dauer, "%.1f" % (erkannt / 60) if erkannt else "-", anteil * 100),
             erkannt is not None and erkannt <= 2 * alle + 10 and anteil >= (0.85 if alle <= 300 else 0.75)),
            ("  gehaltene Werte = letzter Stand des Hosts", richtig),
            ("  Anzeige %s" % malt, any(str(x).startswith("MP ") for x in malt)),
        ])
    erkannt, anteil, richtig, _ = mitspieler(Z, 120, eigenes=True)
    ok &= pruefe([("Mitspieler mit eigenem Ziel auf Platz 3: erkannt nach %s s, Host-Ziele zu %3.0f %%" % (
        "%.1f" % (erkannt / 60) if erkannt else "-", anteil * 100), erkannt is not None and anteil >= 0.85 and richtig)])
    aus = dict(PR, **{"Mehrspieler-Hilfe": 0})
    erkannt, anteil, _, f = mitspieler(Z, 120, props=aus)
    ok &= pruefe([("'Mehrspieler-Hilfe' 0: nie aktiv, keine Anzeige", erkannt is None and f.malt() == [])])
    return ok


if __name__ == "__main__":
    ok = test_host()
    ok &= test_mitspieler()
    print("ALLES OK" if ok else "FEHLER")
    sys.exit(0 if ok else 1)
