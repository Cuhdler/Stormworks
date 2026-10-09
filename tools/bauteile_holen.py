"""Holt die Bauteil-Daten aus dem Spiel (Stormworks/rom/data/definitions, eine XML-Datei je Bauteil) und schreibt das
Bauteil-Verzeichnis nach wissen/bauteile/ - damit Claude jedes Bauteil kennt (Name, Datei-Name fuer die
Fahrzeugdatei, Gewicht, Groesse, Bloecke, Anschluesse mit Position, Art und Beschreibung) und Teile wie Raeder oder
Ketten selbst richtig einbauen und verkabeln kann.

Aufruf auf dem PC (im Repo-Ordner, nur Python, keine Zusatzpakete):
    python tools/bauteile_holen.py                    findet Stormworks ueber Steam
    python tools/bauteile_holen.py -d "D:/SteamLibrary/steamapps/common/Stormworks/rom/data/definitions"
Nach jedem Spiel-Update neu laufen lassen, dann wissen/bauteile/ committen und pushen.

Ausgabe (wissen/bauteile/):
  bauteile.json   alles maschinenlesbar. Schluessel = Datei-Name ohne .xml (so heisst das Teil auch im Fahrzeug:
                  <c d="...">). Je Bauteil: name, kategorie, masse, preis, flags, tags, kurz, beschreibung,
                  groesse [x,y,z], voxel_min, voxel_max, bloecke [[x,y,z],...], anschluesse [{label, ein (1 = Eingang,
                  0 = Ausgang), typ (0 An/Aus, 1 Zahl, 2 Drehmoment, 3 Fluessigkeit/Gas, 4 Strom, 5 Composite,
                  6 Video, 7 Ton, 8 Seil/Munition), pos, beschreibung}], kind (Bloecke-Versatz des zweiten Koerpers bei
                  Gelenken), sonst (alle weiteren Attribute ausser Grafik und Ton).
  INDEX.md        eine Zeile je Bauteil, nach Kategorien
  <Kategorie>.md  je Bauteil: Beschreibung, Groesse, Masse, Preis, Werte, die vom Ueblichen abweichen (Motorkraft,
                  Auftrieb, Pumpendruck ...), alle Anschluesse
Die Spiel-Dateien sind nicht immer gueltiges XML (ungueltige Attribut-Namen) - darum liest das Programm sie
fehlertolerant mit regulaeren Ausdruecken statt mit einem strengen XML-Leser.
"""
import collections
import html
import json
import os
import re
import sys

HIER = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HIER)
ZIEL = os.path.join(ROOT, "wissen", "bauteile")
AUS = os.path.join(ZIEL, "bauteile.json")

ATTR = re.compile(r'([^\s=<>/"\']+)\s*=\s*("([^"]*)"|\'([^\']*)\')')
KATEGORIEN = {0: "Bloecke", 1: "Fahrzeugsteuerung", 2: "Bedienelemente", 3: "Antrieb", 4: "Spezialausruestung",
              5: "Logik", 6: "Anzeigen", 7: "Sensoren", 8: "Deko", 9: "Fluessigkeiten", 10: "Elektrik",
              11: "Strahltriebwerke", 12: "Waffen", 13: "Modulare-Motoren", 14: "Industrie", 15: "Fenster",
              -1: "Ohne-Kategorie"}
ARTEN = {0: "An/Aus", 1: "Zahl", 2: "Drehmoment", 3: "Fluessigkeit/Gas", 4: "Strom", 5: "Composite", 6: "Video",
         7: "Ton", 8: "Seil/Munition"}
# Attribute, die nur Grafik oder Ton betreffen - nicht ins Verzeichnis
GRAFIK = re.compile(r"mesh|audio|ies_map|particle")


def attrs(kopf):
    return {m.group(1): m.group(3) if m.group(3) is not None else m.group(4) for m in ATTR.finditer(kopf)}


def pos(text):
    """<position x=".." y=".." z=".."/> im Text -> [x, y, z] (fehlend = 0)."""
    m = re.search(r"<position\b([^>]*)/?>", text)
    a = attrs(m.group(1)) if m else {}
    return [int(float(a.get(k, 0) or 0)) for k in "xyz"]


def zahl(v, standard=0.0):
    try:
        return float(v)
    except (TypeError, ValueError):
        return standard


def vektor(text, tag):
    m = re.search(r"<%s\b([^>]*)/?>" % tag, text)
    a = attrs(m.group(1)) if m else {}
    return [int(zahl(a.get(k), 0)) for k in "xyz"]


def lies(text):
    """Text einer Definitions-Datei -> dict (oder None, wenn keine <definition> drin ist)."""
    m = re.search(r"<definition\b([^>]*)>", text)
    if not m:
        return None
    a = attrs(m.group(1))
    rest = text[m.end():]
    knoten = []
    ln = re.search(r"<logic_nodes\b[^>]*>(.*?)</logic_nodes>", rest, re.S)
    if ln:
        for k in re.finditer(r"<logic_node\b([^>]*?)(/>|>(.*?)</logic_node>)", ln.group(1), re.S):
            ka = attrs(k.group(1))
            knoten.append({"label": ka.get("label", ""), "ein": int(zahl(ka.get("mode"), 0)),
                           "typ": int(zahl(ka.get("type"), 0)), "pos": pos(k.group(3) or ""),
                           "beschreibung": html.unescape(ka.get("description", ""))})
    bloecke = []
    vx = re.search(r"<voxels\b[^>]*>(.*?)</voxels>", rest, re.S)
    if vx:
        for v in re.finditer(r"<voxel\b[^>]*?(/>|>(.*?)</voxel>)", vx.group(1), re.S):
            bloecke.append(pos(v.group(2) or ""))
    kind = re.search(r"<voxel_location_child\b([^>]*)/?>", rest)
    kind = [int(zahl(attrs(kind.group(1)).get(k), 0)) for k in "xyz"] if kind else None
    tip = re.search(r"<tooltip_properties\b([^>]*)/?>", rest)
    tip = attrs(tip.group(1)) if tip else {}
    vmin, vmax = vektor(rest, "voxel_min"), vektor(rest, "voxel_max")
    bekannt = {"name", "category", "mass", "value", "flags", "tags"}
    return {"name": a.get("name", ""), "kategorie": int(zahl(a.get("category"), -1)), "masse": zahl(a.get("mass")),
            "preis": zahl(a.get("value")), "flags": int(zahl(a.get("flags"), 0)), "tags": a.get("tags", ""),
            "kurz": html.unescape(tip.get("short_description", "")),
            "beschreibung": html.unescape(tip.get("description", "")),
            "groesse": [vmax[i] - vmin[i] + 1 for i in range(3)], "voxel_min": vmin, "voxel_max": vmax,
            "bloecke": bloecke, "anschluesse": knoten, "kind": kind,
            "sonst": {k: v for k, v in a.items() if k not in bekannt and len(v) < 200 and not GRAFIK.search(k)}}


def steam_bibliotheken():
    orte = []
    try:
        import winreg
        for wurzel, schluessel in ((winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Valve\Steam"),
                                   (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Valve\Steam"),
                                   (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Valve\Steam")):
            try:
                with winreg.OpenKey(wurzel, schluessel) as k:
                    for name in ("InstallPath", "SteamPath"):
                        try:
                            orte.append(winreg.QueryValueEx(k, name)[0])
                        except OSError:
                            pass
            except OSError:
                pass
    except ImportError:
        pass
    orte += [r"C:\Program Files (x86)\Steam", r"C:\Program Files\Steam", os.path.expanduser("~/.steam/steam"),
             os.path.expanduser("~/.local/share/Steam")]
    alle = []
    for s in orte:
        vdf = os.path.join(s, "steamapps", "libraryfolders.vdf")
        alle.append(s)
        if os.path.exists(vdf):
            alle += [p.replace("\\\\", "\\") for p in re.findall(r'"path"\s+"([^"]+)"', open(vdf, encoding="utf-8",
                                                                                          errors="replace").read())]
    return alle


def finde_definitionen():
    for b in steam_bibliotheken():
        d = os.path.join(b, "steamapps", "common", "Stormworks", "rom", "data", "definitions")
        if os.path.isdir(d):
            return d
    return None


def holen(ordner):
    daten, kaputt = {}, []
    for datei in sorted(os.listdir(ordner)):
        if not datei.lower().endswith(".xml"):
            continue
        text = open(os.path.join(ordner, datei), encoding="utf-8", errors="replace").read()
        d = lies(text)
        if d is None:
            kaputt.append(datei)
        else:
            daten[datei[:-4]] = d
    return daten, kaputt


def zelle(text):
    return text.replace("|", "/").replace("\n", " ").strip()


def markdown(daten):
    """INDEX.md und je Kategorie eine .md-Datei schreiben."""
    zaehler = collections.defaultdict(collections.Counter)
    for d in daten.values():
        for k, v in d["sonst"].items():
            zaehler[k][v] += 1
    ueblich = {k: c.most_common(1)[0][0] for k, c in zaehler.items()}

    def kurz(d):
        a = collections.Counter("%s %s" % ("E" if k["ein"] else "A", ARTEN.get(k["typ"], k["typ"]))
                                for k in d["anschluesse"])
        return ", ".join("%dx %s" % (n, s) if n > 1 else s for s, n in sorted(a.items()))

    nach_kat = collections.defaultdict(list)
    for key, d in daten.items():
        nach_kat[d["kategorie"] if d["kategorie"] in KATEGORIEN else -1].append((key, d))
    index = ["# Bauteil-Verzeichnis", "",
             "Aus den Spieldaten erzeugt von `tools/bauteile_holen.py` (%d Bauteile) - **nicht von Hand ändern**, "
             "nach einem Spiel-Update neu erzeugen. Erklärung und Erfahrungen aus dem Spiel: [README.md](README.md)."
             % len(daten),
             "", "Größe in Blöcken (x y z, lokal). Masse in Spiel-Einheiten (1 = 10 kg), Preis in $. "
             "Anschlüsse: E = Eingang, A = Ausgang (bei Welle, Flüssigkeit und Strom ist die Richtung egal).", ""]
    for kat in sorted(nach_kat, key=lambda k: k if k >= 0 else 99):
        kn = KATEGORIEN[kat]
        teile = sorted(nach_kat[kat], key=lambda kd: (kd[1]["name"].lower(), kd[0]))
        index += ["## %s (Kategorie %d) - Einzelheiten: [%s.md](%s.md)" % (kn, kat, kn, kn), "",
                  "| Name | Datei-Name | Größe | Masse | Preis | Anschlüsse |", "|---|---|---|---|---|---|"]
        seite = ["# %s (Kategorie %d)" % (kn, kat), "",
                 "Aus den Spieldaten erzeugt von `tools/bauteile_holen.py` - nicht von Hand ändern.", ""]
        for key, d in teile:
            index.append("| %s | `%s` | %s | %g | %g | %s |" % (zelle(d["name"]), key, "x".join(map(str, d["groesse"])),
                                                              d["masse"], d["preis"], kurz(d)))
            seite += ["## %s (`%s`)" % (d["name"], key), ""]
            if d["kurz"]:
                seite.append("*%s*" % d["kurz"].strip())
            if d["beschreibung"] and d["beschreibung"] != d["kurz"]:
                seite.append(d["beschreibung"].strip())
            seite += ["", "- Größe %s Blöcke (voxel %s .. %s), Masse %g, Preis %g%s" % (
                "x".join(map(str, d["groesse"])), d["voxel_min"], d["voxel_max"], d["masse"], d["preis"],
                ", Tags: " + d["tags"] if d["tags"] else "")]
            besonders = {k: v for k, v in d["sonst"].items() if v != ueblich[k]}
            if besonders:
                seite.append("- Werte: " + ", ".join("%s=%s" % kv for kv in sorted(besonders.items())))
            if d["kind"] and any(d["kind"]):
                seite.append("- Zweiter Körper (Gelenk) bei %s" % d["kind"])
            if d["anschluesse"]:
                seite += ["", "| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |", "|---|---|---|---|---|"]
                for n in d["anschluesse"]:
                    seite.append("| %s | %s | %s | %s | %s |" % (zelle(n["label"]), ARTEN.get(n["typ"], n["typ"]),
                                                               "Eingang" if n["ein"] else "Ausgang", tuple(n["pos"]),
                                                               zelle(n["beschreibung"])))
            seite.append("")
        index.append("")
        with open(os.path.join(ZIEL, kn + ".md"), "w", encoding="utf-8", newline="\n") as f:
            f.write("\n".join(seite))
    with open(os.path.join(ZIEL, "INDEX.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(index))
    return len(nach_kat)


def main():
    ordner = sys.argv[sys.argv.index("-d") + 1] if "-d" in sys.argv else finde_definitionen()
    if not ordner or not os.path.isdir(ordner):
        sys.exit("Stormworks-Ordner nicht gefunden. Bitte mit -d den Ordner ...\\Stormworks\\rom\\data\\definitions angeben.")
    daten, kaputt = holen(ordner)
    os.makedirs(ZIEL, exist_ok=True)
    with open(AUS, "w", encoding="utf-8", newline="\n") as f:
        json.dump(daten, f, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        f.write("\n")
    kategorien = markdown(daten)
    mit = sum(1 for d in daten.values() if d["anschluesse"])
    print("gelesen: %s" % ordner)
    print("%d Bauteile (%d mit Anschluessen) in %d Kategorien -> %s (%d KB)" % (
        len(daten), mit, kategorien, ZIEL, os.path.getsize(AUS) // 1024))
    if kaputt:
        print("nicht lesbar (%d): %s" % (len(kaputt), ", ".join(kaputt[:10])))
    for probe in ("wheel_tank_drive_7", "wheel_advanced_7_sus", "laser_distance_sensor"):
        d = daten.get(probe)
        if d:
            print("  %s: %s, %d Bloecke, Anschluesse %s" % (probe, d["name"], len(d["bloecke"]),
                                                          [(k["label"], k["pos"]) for k in d["anschluesse"]]))
    print("Jetzt: git add wissen/bauteile, committen und pushen.")


if __name__ == "__main__":
    main()
