"""Baut die Figet Marena auf Schiff v1.0 um (direkt in der Fahrzeug-Datei, reine Text-Chirurgie):

- beide ZE-Regler raus; ihre Kabel zu Air/Fuel Manifolds und Anlassern kommen jetzt vom Schiffs-Chip
- Schiffs-Chip im Fahrzeug durch build/Figet Marena Schiff v1.0.xml ersetzt (gleiche Anschluss-Lage)
- je Seite Getriebe 2-10 (z -100..-108) durch gerade Wellen ersetzt, Getriebe 1 (z -99): aus 1:1 / an -1:1
- Kabel zu entfernten Teilen geloescht

Aufruf: python umbau_v1.py [--schreiben]   (ohne --schreiben nur Probelauf)
Vorher sichern! Das Schiff darf im Spiel nicht gespawnt/offen sein.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VEH = os.path.join(os.environ["APPDATA"], "Stormworks", "data", "vehicles", "Figet Marena.xml")
CHIP = os.path.join(ROOT, "build", "Figet Marena Schiff v1.0.xml")  # nur fuer den einmaligen Umbau

# Schiffs-Chip bei (0,-12,-41): Knoten (x,z) -> Welt (0, -12-x, -41+z)
def chip(x, z):
    return (0, -12 - x, -41 + z)

# ZE-Regler bei (+-8,-18,-78): Knoten (x,z) -> Welt (vx, -18-z, -78+x)
def ze(vx, x, z):
    return (vx, -18 - z, -78 + x)

ZE_EIN = {(vx, x, z) for vx in (-8, 8) for (x, z) in [(0, 0), (2, 0), (0, 1), (1, 0), (3, 0)]}  # Cylinder, Throttle, RPS, On/Off, Dyn
ZE_EIN = {ze(*k) for k in ZE_EIN}
# ZE-Ausgang -> neuer Chip-Anschluss
UMLEITEN = {
    ze(-8, 3, 1): chip(2, 1),   # Air manifold L  -> Luft L
    ze(-8, 2, 1): chip(0, 5),   # Fuel manifold L -> Treibstoff L
    ze(-8, 1, 1): chip(1, 4),   # Starter L       -> Anlasser L
    ze(8, 3, 1): chip(0, 2),    # Air manifold R  -> Luft R
    ze(8, 2, 1): chip(1, 5),    # Fuel manifold R -> Treibstoff R
    ze(8, 1, 1): chip(3, 4),    # Starter R       -> Anlasser R
}
GETRIEBE_WEG = {(vx, -16, z) for vx in (-8, 8) for z in range(-108, -99)}


def xyz(attr):
    d = dict(re.findall(r'(\w)="(-?\d+)"', attr or ""))
    return tuple(int(d.get(k, 0)) for k in "xyz")


def vox(tag, p):
    a = "".join(' %s="%d"' % (k, v) for k, v in zip("xyz", p) if v)
    return "<%s%s/>" % (tag, a)


def chip_eingebettet():
    """MC-Datei -> Form, wie das Spiel sie im Fahrzeug speichert."""
    t = open(CHIP, encoding="utf-8").read()
    t = t[t.index("<microprocessor "):t.index("</microprocessor>")]
    scripts = []
    t = re.sub(r'script="[^"]*"', lambda m: (scripts.append(m.group(0)), 'script="\x00%d"' % (len(scripts) - 1))[1], t)
    t = re.sub(r">\s+<", "><", t).strip()
    for sec in ("component_states", "component_bridge_states"):
        t = re.sub(r"<%s>.*?</%s>" % (sec, sec), "", t, flags=re.S)
    t = t.replace("<group_states/>", "")
    t = t.replace(' mode="0"', "").replace(' type="0"', "")
    t = re.sub(r'<(position|pos)([^/>]*)/>', lambda m: "<%s%s/>" % (m.group(1), re.sub(r' [xyz]="0"', "", m.group(2))), t)
    t = t.replace("<position/>", "")
    t = re.sub(r'(<node [^>]*)></node>', r"\1/>", t)
    t = re.sub(r'<v text="0" value="0"/>', '<v text="0"/>', t)
    t = t.replace("<microprocessor ", "<microprocessor_definition ", 1) + "</microprocessor_definition>"
    t = re.sub(r'script="\x00(\d+)"', lambda m: scripts[int(m.group(1))], t)
    return t


def mc_bereich(s, name):
    """(Anfang, Ende) der Bauteil-Zeichenkette <c d="microprocessor"...>...</c> mit diesem Chip-Namen."""
    i = s.index('<microprocessor_definition name="%s"' % name)
    a = s.rindex('<c d="microprocessor"', 0, i)
    assert re.fullmatch(r'<c d="microprocessor"( t="\d+")?><o [^>]*>', s[a:i]), s[a:i]
    e = s.index("</o></c>", s.index("</microprocessor_definition>", i)) + len("</o></c>")
    return a, e


def main():
    s = open(VEH, encoding="utf-8", newline="").read()
    n0 = len(s)
    if "ZE Modular Engine Controller" not in s:
        sys.exit("Keine ZE-Regler mehr in der Datei - Umbau schon gemacht?")

    # 1. Schiffs-Chip ersetzen (Bauteil-Huelle mit Lage, Drehung, logic_slots bleibt)
    a, e = mc_bereich(s, "Figet Marena Schiffsfuehrung")
    teil = s[a:e]
    d0 = teil.index("<microprocessor_definition")
    d1 = teil.index("</microprocessor_definition>") + len("</microprocessor_definition>")
    alt_slots = teil.count("<slot/>")
    neu = chip_eingebettet()
    knoten = neu.count("<n id=")
    assert knoten == alt_slots == 28, (knoten, alt_slots)
    s = s[:a] + teil[:d0] + neu + teil[d1:] + s[e:]
    print("Schiffs-Chip ersetzt (%d Anschluesse)" % knoten)

    # 2. ZE-Regler entfernen
    for _ in range(2):
        a, e = mc_bereich(s, "ZE Modular Engine Controller")
        s = s[:a] + s[e:]
    assert "ZE Modular Engine Controller" not in s
    print("2 ZE-Regler entfernt")

    # 3. Getriebe: 1 bleibt (Rueckwaertsgang), 2-10 -> gerade Welle wie bei z=-109
    for vx in (-8, 8):
        m = re.search(r'<c d="trans_straight"( t="\d+")?><o [^>]*><vp x="%d" y="-16" z="-109"/></o></c>' % vx, s)
        vorlage = m.group(0)
        for z in range(-108, -99):
            pat = r'<c d="modular_engine_gearbox_1x1"( t="\d+")?><o [^>]*><vp x="%d" y="-16" z="%d"/><logic_slots>(<slot/>)*</logic_slots></o></c>' % (vx, z)
            ms = list(re.finditer(pat, s))
            assert len(ms) == 1, (vx, z, len(ms))
            s = s[:ms[0].start()] + vorlage.replace('z="-109"', 'z="%d"' % z) + s[ms[0].end():]
        pat = r'(<c d="modular_engine_gearbox_1x1"(?: t="\d+")?><o [^>]*?)gear_ratio_2="\d+"([^>]*><vp x="%d" y="-16" z="-99"/>)' % vx
        s, k = re.subn(pat, r'\1gear_ratio_2="1"\2', s)
        assert k == 1, (vx, k)
    assert s.count("modular_engine_gearbox_1x1") == 2
    print("18 Getriebe -> gerade Wellen, 2 Getriebe auf aus 1:1 / an -1:1")

    # 4. Kabel
    li = s.index("<logic_node_links>")
    le = s.index("</logic_node_links>", li)
    body = s[li + len("<logic_node_links>"):le]
    links = re.findall(r'<logic_node_link( type="\d+")?><voxel_pos_0([^/]*)/><voxel_pos_1([^/]*)/></logic_node_link>', body)
    assert "".join('<logic_node_link%s><voxel_pos_0%s/><voxel_pos_1%s/></logic_node_link>' % l for l in links) == body
    out, weg, um = [], 0, 0
    for typ, p0, p1 in links:
        a, b = xyz(p0), xyz(p1)
        if b in ZE_EIN or a in GETRIEBE_WEG or b in GETRIEBE_WEG:
            weg += 1
            continue
        if a in UMLEITEN:
            a = UMLEITEN[a]
            um += 1
        out.append("<logic_node_link%s>%s%s</logic_node_link>" % (typ, vox("voxel_pos_0", a), vox("voxel_pos_1", b)))
    left = [l for l in links if xyz(l[1]) in UMLEITEN]
    s = s[:li + len("<logic_node_links>")] + "".join(out) + s[le:]
    print("Kabel: %d vorher, %d geloescht, %d umgeleitet, %d nachher" % (len(links), weg, um, len(out)))
    # 8 ZE-Eingaenge, 18 Gear-Switch-Kabel, 20 Stromkabel zwischen den entfernten Getrieben (Getriebe 1 hat eigenes
    # Stromkabel zur Lichtmaschine)
    assert um == 24 and weg == 8 + 18 + 20, (um, weg)

    print("Dateigroesse %d -> %d" % (n0, len(s)))
    if "--schreiben" in sys.argv:
        with open(VEH, "w", encoding="utf-8", newline="") as f:
            f.write(s)
        print("geschrieben:", VEH)
    else:
        print("Probelauf - nichts geschrieben (mit --schreiben ausfuehren)")


if __name__ == "__main__":
    main()
