"""Holt die Bauteil-Daten aus dem Spiel (Stormworks/rom/data/definitions, eine XML-Datei je Bauteil) und schreibt sie
kompakt nach daten/bauteile.json - damit Claude jedes Bauteil kennt (Name, Datei-Name fuer die Fahrzeugdatei,
Gewicht, Bloecke, Anschluesse mit Position und Art) und Teile wie Raeder oder Ketten selbst richtig einbauen und
verkabeln kann.

Aufruf auf dem PC (im Repo-Ordner, nur Python, keine Zusatzpakete):
    python tools/bauteile_holen.py                    findet Stormworks ueber Steam
    python tools/bauteile_holen.py -d "D:/SteamLibrary/steamapps/common/Stormworks/rom/data/definitions"
Danach: git add daten/bauteile.json, committen, pushen.

Inhalt je Bauteil (Schluessel = Datei-Name ohne .xml, so heisst es auch im Fahrzeug: <c d="...">):
  name, kategorie, masse, preis, flags, tags, bloecke [[x,y,z],...], anschluesse [{label, ein (1 = Eingang,
  0 = Ausgang), typ (0 An/Aus, 1 Zahl, 2 Drehmoment, 3 Wasser, 4 Strom, 5 Composite, 6 Video, 7 Ton, 8 Seil), pos}],
  kind (Bloecke-Versatz des zweiten Koerpers bei Gelenken), sonst (alle weiteren Attribute des Bauteils).
Die Spiel-Dateien sind nicht immer gueltiges XML (ungueltige Attribut-Namen) - darum liest das Programm sie
fehlertolerant mit regulaeren Ausdruecken statt mit einem strengen XML-Leser.
"""
import json
import os
import re
import sys

HIER = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HIER)
AUS = os.path.join(ROOT, "daten", "bauteile.json")

ATTR = re.compile(r'([^\s=<>/"\']+)\s*=\s*("([^"]*)"|\'([^\']*)\')')


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
                           "typ": int(zahl(ka.get("type"), 0)), "pos": pos(k.group(3) or "")})
    bloecke = []
    vx = re.search(r"<voxels\b[^>]*>(.*?)</voxels>", rest, re.S)
    if vx:
        for v in re.finditer(r"<voxel\b[^>]*?(/>|>(.*?)</voxel>)", vx.group(1), re.S):
            bloecke.append(pos(v.group(2) or ""))
    kind = re.search(r"<voxel_location_child\b([^>]*)/?>", rest)
    kind = [int(zahl(attrs(kind.group(1)).get(k), 0)) for k in "xyz"] if kind else None
    bekannt = {"name", "category", "mass", "value", "flags", "tags"}
    return {"name": a.get("name", ""), "kategorie": int(zahl(a.get("category"), -1)), "masse": zahl(a.get("mass")),
            "preis": zahl(a.get("value")), "flags": int(zahl(a.get("flags"), 0)), "tags": a.get("tags", ""),
            "bloecke": bloecke, "anschluesse": knoten, "kind": kind,
            "sonst": {k: v for k, v in a.items() if k not in bekannt and len(v) < 200}}


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


def main():
    ordner = sys.argv[sys.argv.index("-d") + 1] if "-d" in sys.argv else finde_definitionen()
    if not ordner or not os.path.isdir(ordner):
        sys.exit("Stormworks-Ordner nicht gefunden. Bitte mit -d den Ordner ...\\Stormworks\\rom\\data\\definitions angeben.")
    daten, kaputt = holen(ordner)
    os.makedirs(os.path.dirname(AUS), exist_ok=True)
    with open(AUS, "w", encoding="utf-8", newline="\n") as f:
        json.dump(daten, f, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        f.write("\n")
    mit = sum(1 for d in daten.values() if d["anschluesse"])
    print("gelesen: %s" % ordner)
    print("%d Bauteile (%d mit Anschluessen) -> %s (%d KB)" % (len(daten), mit, AUS, os.path.getsize(AUS) // 1024))
    if kaputt:
        print("nicht lesbar (%d): %s" % (len(kaputt), ", ".join(kaputt[:10])))
    for probe in ("wheel_tank_drive_7", "wheel_advanced_7_sus", "laser_distance_sensor"):
        d = daten.get(probe)
        if d:
            print("  %s: %s, %d Bloecke, Anschluesse %s" % (probe, d["name"], len(d["bloecke"]),
                                                          [(k["label"], k["pos"]) for k in d["anschluesse"]]))
    print("Jetzt: git add daten/bauteile.json, committen und pushen.")


if __name__ == "__main__":
    main()
