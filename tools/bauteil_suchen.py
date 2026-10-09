"""Sucht in wissen/bauteile/bauteile.json (erzeugt von tools/bauteile_holen.py).

    python tools/bauteil_suchen.py laser                 Liste: Datei-Name, Name, Gewicht, Bloecke, Anschluesse
    python tools/bauteil_suchen.py laser_distance_sensor --voll   alle Angaben (JSON)
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATEI = os.path.join(ROOT, "wissen", "bauteile", "bauteile.json")
TYP = {0: "An/Aus", 1: "Zahl", 2: "Drehmoment", 3: "Wasser", 4: "Strom", 5: "Composite", 6: "Video", 7: "Ton",
       8: "Seil"}


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        sys.exit(__doc__)
    if not os.path.exists(DATEI):
        sys.exit("%s fehlt noch - erst auf dem PC tools/bauteile_holen.py laufen lassen." % DATEI)
    daten = json.load(open(DATEI, encoding="utf-8"))
    wort = args[0].lower()
    treffer = {k: d for k, d in daten.items() if wort in k.lower() or wort in d["name"].lower()}
    if "--voll" in sys.argv:
        print(json.dumps(treffer, ensure_ascii=False, indent=1))
        return
    for k, d in sorted(treffer.items()):
        ans = ", ".join("%s %s %s" % ("rein" if a["ein"] else "raus", TYP.get(a["typ"], a["typ"]), a["label"])
                        for a in d["anschluesse"])
        print("%s | %s | Masse %s | %d Bloecke | %s" % (k, d["name"], d["masse"], len(d["bloecke"]), ans or "-"))
    print("%d Treffer" % len(treffer))


if __name__ == "__main__":
    main()
