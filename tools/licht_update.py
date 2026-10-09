"""Licht ins Schiff (Andre 08.10.: "jede Menge Lichter hinzugefuegt, sie sollen immer an sein, nur Tag und Nachts
unterschiedlich hell, die im Steuerungsraum sollen bei Bedrohung rot werden"):
- Chip "Figet Marena Licht" 2x2 neu an der Chip-Wand vp (1,12,-59) (x 1..2, y 11..12, frei)
- Uhr (Bauteil 'Clock') neu an der Chip-Wand (4,12,-59), Zifferblatt zum Raum (+z) - liefert die Tageszeit
- Kabel: Uhr Time -> Licht 'Uhr'; Lage-Chip 'Lage' -> Licht 'Lage'; Licht 'Licht' -> Color Data der 51 Lampen ausser
  Steuerungsraum; 'Licht Steuerraum' -> die 4 Deckenlampen im Steuerungsraum (y 25, ueber Fahrersitz und Autopilot)
- Strom: Batterie (-4,-13,-46) -> alle 55 Lampen und die Uhr
Probe: ausser diesen zwei Teilen und Kabeln aendert sich nichts.
Aufruf: python licht_update.py [--schreiben]   (vorher sichern; danach Schiff neu laden, NICHT vorher speichern)
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import umbau_v1 as u  # noqa: E402
import kabel_flak as kf  # noqa: E402
import sperrprofil  # noqa: E402
import build_licht  # noqa: E402
from build_schiff import BUILD  # noqa: E402
from feuer_rechts_update import chip_knoten  # noqa: E402
from autopilot_update import link, chip_flaeche, flaeche, BATT, LINKS, AP  # noqa: E402

LI = "Figet Marena Licht"
VP, R_ = (1, 12, -59), "1,0,0,0,0,1,0,-1,0"
UHR_VP = (4, 12, -59)
UHR = ('<c d="clock"><o r="%s" bc="70787D" sc="5" timer_scalar_1="0.183" timer_scalar_2="0.183">%s<logic_slots>%s'
       '</logic_slots><property_output_float_val text="0"/><min_threshold text="0"/><max_threshold text="0"/>'
       '<pid_controller_ki text="1" value="1"/><pid_controller_kp text="1" value="1"/><pid_controller_kd text="1" '
       'value="1"/><pid_controller_max_error text="0"/><exp text="2" value="2"/><min_lever_value text="-1" value="-1"/>'
       '<max_lever_value text="1" value="1"/><starting_lever_value text="0"/></o></c>') % (R_, u.vox("vp", UHR_VP),
                                                                                         "<slot/>" * 15)
STEUERRAUM = [(-4, 25, -25), (4, 25, -25), (-4, 25, -11), (4, 25, -11)]


def main():
    s0 = open(u.VEH, encoding="utf-8", newline="").read()
    s = s0
    assert '<microprocessor_definition name="%s"' % LI not in s, "Licht-Chip ist schon eingebaut"
    assert '<c d="clock"' not in s, "Uhr ist schon eingebaut"
    tl = kf.teile(s)
    lampen = sorted(vp for (d, vp) in tl if d == "small_light_rgb")
    assert len(lampen) == 55 and all(p in lampen for p in STEUERRAUM), len(lampen)
    # Platz: Chip 2x2 und Uhr (2 Felder: Gehaeuse + Zifferblatt davor)
    R = [[int(v) for v in R_.split(",")][i * 3:i * 3 + 3] for i in range(3)]
    u.CHIP = os.path.join(BUILD, "%s %s.xml" % (LI, build_licht.VERSION))
    d = u.chip_eingebettet()
    w = int(re.search(r'<microprocessor_definition [^>]*width="(\d+)"', d).group(1))
    ln = int(re.search(r'<microprocessor_definition [^>]*length="(\d+)"', d).group(1))
    nk = len(re.findall(r"<n id=", d))
    fl = flaeche(R, VP, w, ln)
    uhr_fl = {UHR_VP, (UHR_VP[0], UHR_VP[1], UHR_VP[2] + 1)}
    belegt = set(p for teile in sperrprofil.koerper() for dd, p in teile if dd != "microprocessor")
    for mm in re.finditer(r'<microprocessor_definition name="([^"]*)"', s):
        belegt |= chip_flaeche(s, mm.group(1))
    voll = sorted(p for p in fl | uhr_fl if p in belegt)
    assert not voll and not (fl & uhr_fl), ("Platz belegt", voll)
    teil = '<c d="microprocessor"><o r="%s" bc="70787D" sc="%d">%s%s<logic_slots>%s</logic_slots></o></c>' % (
        R_, 2 * w * ln + 2 * (w + ln), d, u.vox("vp", VP), "<slot/>" * nk)
    _, e = u.mc_bereich(s, AP)
    s = s[:e] + teil + UHR + s[e:]
    lk = chip_knoten(s, LI)
    print("Licht-Chip %dx%d bei %s, Uhr bei %s" % (w, ln, VP, UHR_VP))
    tl = kf.teile(s)

    def an(d_, vp, lab, mo_soll, ty_soll):
        p, mo, ty = kf.anschluss(tl, d_, vp, lab)
        assert mo == mo_soll and ty == ty_soll, (d_, vp, lab, mo, ty)
        return p
    strom = an(BATT[0], BATT[1], "Electric Store", 1, 4)
    neu = [(1, an("clock", UHR_VP, "Time", 0, 1), lk["Uhr"], "Uhr Time -> Licht 'Uhr'"),
           (5, chip_knoten(s, "Figet Marena Lage")["Lage"], lk["Lage"], "Lage 'Lage' -> Licht 'Lage'"),
           (4, strom, an("clock", UHR_VP, "Electric", 1, 4), "Strom -> Uhr")]
    for vp in lampen:
        quelle = lk["Licht Steuerraum"] if vp in STEUERRAUM else lk["Licht"]
        neu.append((5, quelle, an("small_light_rgb", vp, "Color Data", 1, 5), "Farbe -> Lampe %s" % (vp,)))
        neu.append((4, strom, an("small_light_rgb", vp, "Electric", 1, 4), "Strom -> Lampe %s" % (vp,)))
    li, le = s.index("<logic_node_links>") + len("<logic_node_links>"), s.index("</logic_node_links>")
    alt_l = re.findall(LINKS, s[li:le])
    assert "".join(alt_l) == s[li:le], "Kabelliste nicht vollstaendig erfasst"
    belegte_eing = set((int(t or 0), p1) for t, p1 in re.findall(
        r'<logic_node_link(?: type="(\d+)")?><voxel_pos_0[^>]*/>(<voxel_pos_1[^>]*/>)', "".join(alt_l)))
    zu = []
    for typ, p0, p1, was in neu:
        assert (typ, u.vox("voxel_pos_1", p1)) not in belegte_eing, ("Eingang schon belegt", was, p1)
        zu.append(link(typ, p0, p1))
    for typ, p0, p1, was in neu[:3]:
        print("  %-40s %s -> %s" % (was, p0, p1))
    print("  Farbe: %d Lampen an 'Licht', %d an 'Licht Steuerraum' %s; Strom an %d Lampen" % (
        len(lampen) - len(STEUERRAUM), len(STEUERRAUM), STEUERRAUM, len(lampen)))
    s = s[:li] + "".join(alt_l + zu) + s[le:]

    # Probe
    def ohne(x, neu_teile):
        if neu_teile:
            a2, e2 = u.mc_bereich(x, LI)
            assert x[e2:e2 + len(UHR)] == UHR
            x = x[:a2] + x[e2 + len(UHR):]
        li2, le2 = x.index("<logic_node_links>"), x.index("</logic_node_links>")
        return x[:li2] + x[le2:]
    assert ohne(s0, False) == ohne(s, True), "ausser Licht-Chip, Uhr und Kabeln geaendert"
    assert re.findall(LINKS, s[s.index("<logic_node_links>"):s.index("</logic_node_links>")]) == alt_l + zu
    print("Probe: Licht-Chip und Uhr neu, %d Kabel neu, sonst nichts" % len(zu))
    ziel = u.VEH if "--schreiben" in sys.argv else os.path.join(os.environ.get("TEMP", "."), "schiff_probe.xml")
    with open(ziel, "w", encoding="utf-8", newline="") as f:
        f.write(s)
    print("geschrieben:", ziel)


if __name__ == "__main__":
    main()
