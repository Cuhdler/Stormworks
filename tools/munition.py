"""Munition der Figet Marena einstellen (Andre 03.10.).
property_ammo_damage = Art, IM SPIEL GEPRUEFT (Andre 03.10.): 1 High Explosive, 2 Fragmentation, 3 Armor Piercing,
  4 Incendiary; neue Teile stehen auf 5 (vermutlich Kinetic). Die Liste aus dem Netz (1 Kinetic, 2 HE, 3 Frag, 4 AP,
  5 Incendiary) war FALSCH - damit stand die Flak auf AP, die Battle Cannon auf Frag, die Autokanone vorn auf Incendiary.
property_ammo_type   = Kaliber in Autokanonen-Trommeln/-Gurten: 7 Light, 8 Rotary, 9 Heavy Autocannon

- Battle Cannon (alle *_l-Gurtteile, Zufuehrungen, die Kanonen): HE
- Autokanone vorn (Trommeln/Gurte/Zufuehrung/Kanone vor z -50): Heavy + Armor Piercing
- Flak hinten (Trommeln/Gurte/Zufuehrungen/Kanonen hinter z -50): Heavy + Fragmentation
Probe: ausser diesen Attributen aendert sich nichts.
Aufruf: python munition.py [--schreiben]   (ohne: Probe nach %TEMP%\\schiff_probe.xml)
"""
import os
import re
import sys
from collections import Counter

VEH = os.path.join(os.environ["APPDATA"], "Stormworks", "data", "vehicles", "Figet Marena.xml")
ART = {"HE": 1, "Frag": 2, "AP": 3, "Incendiary": 4}
HEAVY = 9
AC_TEILE = ("gun_drum_", "gun_belt_flex", "gun_belt_loader", "gun_belt_straight", "gun_belt_corner", "gun_belt_junction",
            "gun_belt_receiver")


def gruppe(d, z):
    """-> (Kaliber oder None, Art) oder None (nicht anfassen)."""
    if d == "gun_l" or (d.startswith("gun_belt_") and d.endswith("_l")):
        return None, ART["HE"]
    if d == "gun_m":       # die Kanone selbst: nur die Art (sie hatte nie ein Kaliber-Attribut)
        return None, ART["AP"] if z > -50 else ART["Frag"]
    if d.startswith(AC_TEILE) and not d.endswith(("_l", "_xl", "_xxl")):
        return HEAVY, ART["AP"] if z > -50 else ART["Frag"]
    return None


def main():
    s0 = open(VEH, encoding="utf-8", newline="").read()
    zaehl = Counter()

    def tausch(m):
        d, t, o, rest = m.group(1), m.group(2) or "", m.group(3), m.group(4)
        vp = re.search(r"<vp([^/]*)/>", rest)
        z = int(dict(re.findall(r'(\w)="(-?\d+)"', vp.group(1))).get("z", 0)) if vp else 0
        g = gruppe(d, z)
        if g is None:
            return m.group(0)
        kal, art = g
        o2 = re.sub(r' property_ammo_(type|damage)="\d+"', "", o)
        o2 += (' property_ammo_type="%d"' % kal if kal else "") + ' property_ammo_damage="%d"' % art
        zaehl[(d.replace("gun_", ""), "vorn" if z > -50 else "hinten", kal or "-", art)] += 1
        return '<c d="%s"%s><o %s>%s' % (d, t, o2, rest)

    s = re.sub(r'<c d="(gun_[a-z0-9_]+)"( t="\d+")?><o ([^>]*)>((?:(?!</c>).)*?<vp[^/]*/>)', tausch, s0, flags=re.S)
    for (d, wo, kal, art), n in sorted(zaehl.items()):
        print("  %-28s %-6s Kaliber %-2s Art %d (%s)  x%d" % (d, wo, kal, art, [k for k, v in ART.items() if v == art][0], n))
    # Probe: ohne die Munitions-Attribute muessen beide Fassungen gleich sein
    ohne = lambda x: re.sub(r' property_ammo_(type|damage)="\d+"', "", x)
    assert ohne(s0) == ohne(s), "ausser Munition geaendert"
    print("Probe: ausser property_ammo_type/_damage nichts geaendert; %d Teile umgestellt" % sum(zaehl.values()))
    ziel = VEH if "--schreiben" in sys.argv else os.path.join(os.environ.get("TEMP", "."), "schiff_probe.xml")
    with open(ziel, "w", encoding="utf-8", newline="") as f:
        f.write(s)
    print("geschrieben:", ziel)


if __name__ == "__main__":
    main()
