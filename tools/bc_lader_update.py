"""BC-Lader v2.5 ins Schiff (Andre 04.10.: "auch die BC sollte mit beiden Rohren abwechselnd schiessen, optimiere das
alles bitte"; Log 13:28: ein Rohr lud 295 Ticks, beide nacheinander, 11 Schuss in 51 s):
- Chips tauschen wie kanone_update (Flak L/R v2.5, Kanone BC/AC v1.3: Lader mit Meldern, abwechselnd feuern; BC hat
  zwei neue Eingaenge 'Munition links/rechts' am Ende, die alten Anschluesse behalten ihre Kabel)
- zwei Kabel: Battle Cannon Belt (Feeder) links/rechts 'Contains Ammo' -> BC-Chip 'Munition links/rechts'
Probe: ausser den Chip-Definitionen, Steckplaetzen und diesen zwei Kabeln aendert sich nichts.
Aufruf: python bc_lader_update.py [--schreiben]   (vorher sichern; danach Schiff neu laden, NICHT vorher speichern)
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import umbau_v1 as u  # noqa: E402
import kabel_flak as kf  # noqa: E402
from kabel_kanone import TURM  # noqa: E402
from kanone_update import TAUSCH  # noqa: E402
from waffen_update import tausche  # noqa: E402
from feuer_rechts_update import chip_knoten  # noqa: E402

NEU = [("lad", "Munition links"), ("lad_r", "Munition rechts")]


def main():
    s0 = open(u.VEH, encoding="utf-8", newline="").read()
    s = s0
    for name, datei, vorgabe in TAUSCH:
        s = tausche(s, name, datei, vorgabe)
    tl = kf.teile(s)
    kn = chip_knoten(s, "Figet Marena Kanone BC")
    li, le = s.index("<logic_node_links>"), s.index("</logic_node_links>")
    alt = s[li:le]
    zu = []
    for teil, label in NEU:
        d, vp = TURM["BC"][teil]
        p0, mo, ty = kf.anschluss(tl, d, vp, "Contains Ammo")
        assert mo == 0 and ty == 0, ("Contains Ammo", teil, mo, ty)
        p1 = kn[label]
        assert u.vox("voxel_pos_1", p1) not in alt, ("Chip-Eingang schon belegt", label, p1)
        k = "<logic_node_link>%s%s</logic_node_link>" % (u.vox("voxel_pos_0", p0), u.vox("voxel_pos_1", p1))
        assert k not in alt
        zu.append(k)
        print("Kabel: %s %s 'Contains Ammo' %s -> BC-Chip '%s' %s" % (d, vp, p0, label, p1))
    s = s[:le] + "".join(zu) + s[le:]
    namen = "|".join(re.escape(n) for n, _, _ in TAUSCH)

    def ohne(x):
        x = re.sub(r'<microprocessor_definition name="(%s)".*?</microprocessor_definition>' % namen, "", x, flags=re.S)
        x = re.sub(r"<logic_slots>(<slot(?: editor_connected=\"1\")?/>)*</logic_slots>", "<logic_slots/>", x)
        for k in zu:
            x = x.replace(k, "")
        return x
    assert ohne(s0) == ohne(s), "ausser Chip-Definitionen, Steckplaetzen und den zwei Kabeln geaendert"
    print("Probe: nur %d Chip-Definitionen, Steckplaetze und %d neue Kabel" % (len(TAUSCH), len(zu)))
    ziel = u.VEH if "--schreiben" in sys.argv else os.path.join(os.environ.get("TEMP", "."), "schiff_probe.xml")
    with open(ziel, "w", encoding="utf-8", newline="") as f:
        f.write(s)
    print("geschrieben:", ziel)


if __name__ == "__main__":
    main()
