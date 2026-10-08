"""Prueft eine Fahrzeugdatei, ohne das Spiel: laeuft nach jedem Bau des Landkreuzers (bau_landkreuzer.py) und laesst
sich auch einzeln aufrufen: python landkreuzer/tools/pruefen.py [Datei]

Prueft:
1. XML wohlgeformt (ein strenger XML-Leser liest die Datei)
2. nur Teil-Arten, die es in der Figet Marena gibt (deren Spiel-Definitionen sind also auf Andres PC vorhanden)
3. je Koerper keine zwei Teile auf demselben Platz (ausser Gelenk-Paaren)
4. Rumpf zusammenhaengend (Nachbar-Bloecke; Bauteile zaehlen mit 2 Bloecken Reichweite, weil sie groesser sind)
5. Kabel: kein Eingang doppelt belegt (ausser Strom), jedes Kabel verbindet zwei verschiedene Orte
6. Chips: Lua-Skripte hoechstens 8192 Zeichen, je Anschluss genau ein <slot/>
"""
import collections
import os
import re
import sys
import xml.etree.ElementTree as ET

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
import fz  # noqa: E402

LK = os.path.dirname(HIER)


def pruefe(txt, schiff=None, laut=True):
    fehler, hinweise = [], []
    root = ET.fromstring(txt.encode("utf-8"))
    F = fz.Fahrzeug(txt)
    # 2. Arten
    schiff = schiff or fz.Fahrzeug.lesen()
    bekannt = {t.d for _, ts in schiff.koerper for t in ts}
    arten = collections.Counter(t.d for _, ts in F.koerper for t in ts)
    neu = set(arten) - bekannt
    if neu:
        fehler.append("Teil-Arten, die es im Schiff nicht gibt: %s" % sorted(neu))
    # 3. doppelt
    for bi, (_, ts) in enumerate(F.koerper):
        pos = collections.Counter(t.vp for t in ts if not t.d.startswith("multibody"))
        dop = [p for p, n in pos.items() if n > 1]
        if dop:
            fehler.append("Koerper %d: %d Plaetze doppelt belegt, z. B. %s" % (bi, len(dop), dop[:3]))
    # 4. Rumpf zusammenhaengend
    rum = max(range(len(F.koerper)), key=lambda k: len(F.koerper[k][1]))
    ts = F.koerper[rum][1]
    vox = collections.defaultdict(list)
    for i, t in enumerate(ts):
        vox[t.vp].append(i)
    par = list(range(len(ts)))

    def f(a):
        while par[a] != a:
            par[a] = par[par[a]]
            a = par[a]
        return a
    for i, t in enumerate(ts):
        r = 1 if t.d in fz.STRUKTUR else 2
        for dx in range(-r, r + 1):
            for dy in range(-r, r + 1):
                for dz in range(-r, r + 1):
                    if abs(dx) + abs(dy) + abs(dz) > r:
                        continue
                    for j in vox.get((t.vp[0] + dx, t.vp[1] + dy, t.vp[2] + dz), ()):
                        a, b = f(i), f(j)
                        if a != b:
                            par[a] = b
    gruppen = collections.defaultdict(list)
    for i in range(len(ts)):
        gruppen[f(i)].append(i)
    gr = sorted(gruppen.values(), key=len, reverse=True)
    lose = [g for g in gr[1:] if len(g) > 1 or ts[g[0]].d in fz.STRUKTUR]
    if lose:
        fehler.append("Rumpf: %d lose Gruppen, z. B. %s" % (len(lose), [(len(g), ts[g[0]].d, ts[g[0]].vp) for g in lose[:4]]))
    einzeln = [ts[g[0]].d for g in gr[1:] if len(g) == 1 and ts[g[0]].d not in fz.STRUKTUR]
    if einzeln:
        hinweise.append("einzelne grosse Bauteile ohne Nachbarn in 2 Bloecken (meist ok, sie sind groesser): %s"
                        % dict(collections.Counter(einzeln)))
    # 5. Kabel
    ein = collections.Counter((typ, b) for typ, a, b in F.kabel if typ != 4)
    mehr = [k for k, n in ein.items() if n > 1]
    if mehr:
        fehler.append("Eingaenge mit mehreren Kabeln: %s" % mehr[:5])
    if any(a == b for _, a, b in F.kabel):
        fehler.append("Kabel mit gleichem Anfang und Ende")
    # 6. Chips
    for mp in root.iter("microprocessor_definition"):
        for c in mp.iter("c"):
            if c.get("type") == "56":
                n = len(c.find("object").get("script"))
                if n > 8192:
                    fehler.append("Chip %s: Lua-Skript %d Zeichen (> 8192)" % (mp.get("name"), n))
    for _, ts2 in F.koerper:
        for t in ts2:
            if t.d == "microprocessor":
                nodes = t.xml.count("<n id=")
                slots = t.xml[t.xml.rindex("<logic_slots>"):].count("<slot")
                if nodes != slots:
                    fehler.append("Chip bei %s: %d Anschluesse, %d Slots" % (t.vp, nodes, slots))
    if laut:
        print("Pruefung: %d Koerper, %d Teile, %d Arten, %d Kabel" % (len(F.koerper), sum(arten.values()), len(arten),
                                                                       len(F.kabel)))
        for x in fehler:
            print("  FEHLER:", x)
        for x in hinweise:
            print("  Hinweis:", x)
        print("  Pruefung OK" if not fehler else "  Pruefung mit Fehlern")
    return fehler, hinweise


if __name__ == "__main__":
    pfad = sys.argv[1] if len(sys.argv) > 1 else os.path.join(LK, "fahrzeug", "KI Landkreuzer.xml")
    f, _ = pruefe(open(pfad, encoding="utf-8", newline="").read())
    sys.exit(1 if f else 0)
