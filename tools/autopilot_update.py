"""Autopilot v1.0 ins Schiff (Andre 08.10.: "du kannst den Autopilot schonmal machen, der Bildschirm mit den Knoepfen
'Activate Autopilot' und 'Reset' ist der richtige, baue ihn gleich ein"):
- Monitor 5x3 (-6,21,-22): gedreht auf r -1,0,0,0,0,1,0,1,0 (gleiche Stelle, gleiche Flaeche, Bild-Oben jetzt oben -
  die Karte von screen.drawMap laesst sich im Skript nicht drehen)
- Chip "Figet Marena Autopilot" 4x3 neu an der Chip-Wand (vp (-4,12,-59), x -4..-1, y 10..12; frei), Eigenschaften
  'Laser vor/ueber Physik m' aus der Lage von Laser und Physik-Sensor
- Kabel: Fahrersitz Seat data -> Autopilot 'Sitz', Autopilot 'Sitz aus' -> Schiffsfuehrung 'Sitz' (statt direkt);
  Physik-Sensor -> 'Physik'; Monitor 5x3 Touch -> 'Touch', 'Monitor' -> Video, 'Monitor an' -> Power Switch;
  Knopf 'Activate Autopilot' / 'Reset' Pressed -> 'Knopf Autopilot' / 'Knopf Reset'; Laser am Bug (0,2,64) Distance ->
  'Laser Entfernung', 'Laser an' -> Active, 'Laser Pivot' -> Pivot
- Strom: Batterie (-4,-13,-46) -> Monitor 5x3, beide Knoepfe, Laser am Bug (wie die anderen Monitore dort)
Probe: ausser diesen Teilen und Kabeln aendert sich nichts.
Aufruf: python autopilot_update.py [--schreiben]   (vorher sichern; danach Schiff neu laden, NICHT vorher speichern)
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import umbau_v1 as u  # noqa: E402
import kabel_flak as kf  # noqa: E402
import sperrprofil  # noqa: E402
import build_autopilot  # noqa: E402
from build_schiff import BUILD  # noqa: E402
from flak_tauschen import werte, setze  # noqa: E402
from feuer_rechts_update import chip_knoten  # noqa: E402

AP = "Figet Marena Autopilot"
VP, R_ = (-4, 12, -59), "1,0,0,0,0,1,0,-1,0"
MON = ("monitor_5", (-6, 21, -22))
MON_R_ALT, MON_R_NEU = "1,0,0,0,0,1,0,-1,0", "-1,0,0,0,0,1,0,1,0"
KN_AP = ("button_push", (-4, 19, -22))
KN_RS = ("button_push", (-5, 19, -22))
LASER = ("laser_distance_sensor", (0, 2, 64))
SITZ = ("seat_compact", (0, 17, -10))
PHYS = ("physics_sensor", (0, 27, -38))
BATT = ("battery_large", (-4, -13, -46))
LINKS = r"<logic_node_link[ >].*?</logic_node_link>"


def link(typ, p0, p1):
    return "<logic_node_link%s>%s%s</logic_node_link>" % (' type="%d"' % typ if typ else "", u.vox("voxel_pos_0", p0),
                                                          u.vox("voxel_pos_1", p1))


def enden(x):
    return [u.xyz(v) for v in re.findall(r"<voxel_pos_\d([^/]*)/>", x)]


def chip_flaeche(s, name):
    """Felder eines eingebauten Chips (auch mit Anstrich-Attributen nach r)."""
    i = s.index('<microprocessor_definition name="%s"' % name)
    a = s.rindex('<c d="microprocessor"><o ', 0, i)
    r = re.match(r'<c d="microprocessor"><o r="([^"]*)"', s[a:]).group(1)
    R = [[int(float(v)) for v in r.split(",")][k * 3:k * 3 + 3] for k in range(3)]
    w, ln = map(int, re.match(r'<microprocessor_definition [^>]*width="(\d+)" length="(\d+)"', s[i:]).groups())
    e = s.index("</microprocessor_definition>", i)
    vp = u.xyz(re.match(r"<vp([^/]*)/>", s[e + len("</microprocessor_definition>"):]).group(1))
    return flaeche(R, vp, w, ln)


def flaeche(R, vp, w, ln):
    return set(tuple(vp[k] + R[0][k] * x + R[2][k] * z for k in range(3)) for x in range(w) for z in range(ln))


def teil_bereich(s, d, vp):
    """(Anfang, Ende) des Bauteils <c d=..>...</c> an vp."""
    for m in re.finditer(r'<c d="%s"(?: t="\d+")?><o [^>]*>' % d, s):
        e = s.index("</c>", m.end()) + 4
        v = re.search(r"<vp([^/]*)/>", s[m.end():e])
        if u.xyz(v.group(1)) == vp:
            return m.start(), e
    raise ValueError(("Teil fehlt", d, vp))


def main():
    s0 = open(u.VEH, encoding="utf-8", newline="").read()
    s = s0
    assert '<microprocessor_definition name="%s"' % AP not in s, "Autopilot ist schon eingebaut"
    # Teile pruefen
    tl = kf.teile(s)
    for d, vp in (MON, KN_AP, KN_RS, LASER, SITZ, PHYS, BATT):
        assert len(tl.get((d, vp), [])) == 1, ("Teil fehlt", d, vp)
    for (d, vp), name in ((KN_AP, "Activate Autopilot"), (KN_RS, "Reset")):
        a, e = teil_bereich(s, d, vp)
        assert 'custom_name="%s"' % name in s[a:e], ("Knopf", vp, name)
    # Monitor drehen
    a, e = teil_bereich(s, *MON)
    alt = s[a:e]
    assert alt.startswith('<c d="monitor_5"><o r="%s"' % MON_R_ALT), alt[:80]
    s = s[:a] + alt.replace('r="%s"' % MON_R_ALT, 'r="%s"' % MON_R_NEU, 1) + s[e:]
    print("Monitor 5x3 %s gedreht: r %s -> %s" % (MON[1], MON_R_ALT, MON_R_NEU))
    # Chip bauen und einsetzen (direkt hinter dem Seeradar, gleicher Koerper)
    u.CHIP = os.path.join(BUILD, "%s %s.xml" % (AP, build_autopilot.VERSION))
    d = u.chip_eingebettet()
    lz = (LASER[1][2] - PHYS[1][2]) * 0.25
    ly = (LASER[1][1] - PHYS[1][1]) * 0.25
    d = setze(d, "Laser vor Physik m", lz)
    d = setze(d, "Laser ueber Physik m", ly)
    wv = werte(d)
    assert float(wv["Laser vor Physik m"]) == lz and float(wv["Laser ueber Physik m"]) == ly, wv
    w = int(re.search(r'<microprocessor_definition [^>]*width="(\d+)"', d).group(1))
    ln = int(re.search(r'<microprocessor_definition [^>]*length="(\d+)"', d).group(1))
    nk = len(re.findall(r"<n id=", d))
    R = [[int(v) for v in R_.split(",")][i * 3:i * 3 + 3] for i in range(3)]
    fl = flaeche(R, VP, w, ln)
    belegt = set(p for teile in sperrprofil.koerper() for dd, p in teile if dd != "microprocessor")
    for mm in re.finditer(r'<microprocessor_definition name="([^"]*)"', s):
        belegt |= chip_flaeche(s, mm.group(1))
    voll = sorted(p for p in fl if p in belegt)
    assert not voll, ("Platz fuer den Autopiloten belegt", voll)
    teil = '<c d="microprocessor"><o r="%s" bc="70787D" sc="%d">%s%s<logic_slots>%s</logic_slots></o></c>' % (
        R_, 2 * w * ln + 2 * (w + ln), d, u.vox("vp", VP), "<slot/>" * nk)
    _, e = u.mc_bereich(s, "Figet Marena Seeradar")
    s = s[:e] + teil + s[e:]
    ak = chip_knoten(s, AP)
    print("Autopilot %d x %d eingesetzt: vp %s, Flaeche %s frei; Laser vor/ueber Physik %.2f / %.2f m"
          % (w, ln, VP, sorted(fl), lz, ly))
    # Kabel
    tl = kf.teile(s)

    def an(teil_, lab, mo_soll, ty_soll):
        p, mo, ty = kf.anschluss(tl, teil_[0], teil_[1], lab)
        assert mo == mo_soll and ty == ty_soll, (teil_, lab, mo, ty)
        return p
    sitz = an(SITZ, "Seat data", 0, 5)
    sf = chip_knoten(s, "Figet Marena Schiffsfuehrung")["Sitz"]
    li, le = s.index("<logic_node_links>") + len("<logic_node_links>"), s.index("</logic_node_links>")
    alt_l = re.findall(LINKS, s[li:le])
    assert "".join(alt_l) == s[li:le], "Kabelliste nicht vollstaendig erfasst"
    weg = [x for x in alt_l if enden(x) == [sitz, sf]]
    assert len(weg) == 1, ("Kabel Sitz -> Schiffsfuehrung", weg)
    bleibt = [x for x in alt_l if x not in weg]
    strom = an(BATT, "Electric Store", 1, 4)   # Strom: beide Richtungen, Batterie vorn wie bei den anderen Monitoren
    neu = [(5, sitz, ak["Sitz"], "Fahrersitz -> Autopilot 'Sitz'"),
           (5, ak["Sitz aus"], sf, "Autopilot 'Sitz aus' -> Schiffsfuehrung 'Sitz'"),
           (5, an(PHYS, "Composite Output", 0, 5), ak["Physik"], "Physik-Sensor -> Autopilot"),
           (5, an(MON, "Touch Output", 0, 5), ak["Touch"], "Monitor 5x3 Touch -> Autopilot"),
           (6, ak["Monitor"], an(MON, "Video Signal", 1, 6), "Autopilot -> Monitor 5x3 Video"),
           (0, ak["Monitor an"], an(MON, "Power Switch", 1, 0), "Autopilot -> Monitor 5x3 Power Switch"),
           (0, an(KN_AP, "Pressed", 0, 0), ak["Knopf Autopilot"], "Knopf 'Activate Autopilot' -> Autopilot"),
           (0, an(KN_RS, "Pressed", 0, 0), ak["Knopf Reset"], "Knopf 'Reset' -> Autopilot"),
           (1, an(LASER, "Distance", 0, 1), ak["Laser Entfernung"], "Laser Distance -> Autopilot"),
           (0, ak["Laser an"], an(LASER, "Active", 1, 0), "Autopilot -> Laser Active"),
           (5, ak["Laser Pivot"], an(LASER, "Pivot", 1, 5), "Autopilot -> Laser Pivot"),
           (4, strom, an(MON, "Electric", 1, 4), "Strom -> Monitor 5x3"),
           (4, strom, an(KN_AP, "Electric", 1, 4), "Strom -> Knopf 'Activate Autopilot'"),
           (4, strom, an(KN_RS, "Electric", 1, 4), "Strom -> Knopf 'Reset'"),
           (4, strom, an(LASER, "Electric", 1, 4), "Strom -> Laser")]
    belegte_eing = set((int(t or 0), p1) for t, p1 in re.findall(
        r'<logic_node_link(?: type="(\d+)")?><voxel_pos_0[^>]*/>(<voxel_pos_1[^>]*/>)', "".join(bleibt)))
    zu = []
    for typ, p0, p1, was in neu:
        assert (typ, u.vox("voxel_pos_1", p1)) not in belegte_eing, ("Eingang schon belegt", was, p1)
        zu.append(link(typ, p0, p1))
        print("  %-48s %s -> %s" % (was, p0, p1))
    for x in weg:
        print("  Kabel weg: %s" % x)
    s = s[:li] + "".join(bleibt + zu) + s[le:]
    # Probe
    def ohne(x, mit_chip):
        if mit_chip:
            a2, e2 = u.mc_bereich(x, AP)
            x = x[:a2] + x[e2:]
        a2, e2 = teil_bereich(x, *MON)
        x = x[:a2] + x[a2:e2].replace('r="%s"' % MON_R_NEU, 'r="%s"' % MON_R_ALT, 1) + x[e2:]
        li2, le2 = x.index("<logic_node_links>"), x.index("</logic_node_links>")
        return x[:li2] + x[le2:]
    assert ohne(s0, False) == ohne(s, True), "ausser Monitor-Drehung, Chip und Kabeln geaendert"
    assert re.findall(LINKS, s[s.index("<logic_node_links>"):s.index("</logic_node_links>")]) == bleibt + zu
    assert s.count("<microprocessor_definition ") == s0.count("<microprocessor_definition ") + 1
    print("Probe: Monitor gedreht, Autopilot neu, %d Kabel weg, %d neu, sonst nichts" % (len(weg), len(zu)))
    ziel = u.VEH if "--schreiben" in sys.argv else os.path.join(os.environ.get("TEMP", "."), "schiff_probe.xml")
    with open(ziel, "w", encoding="utf-8", newline="") as f:
        f.write(s)
    print("geschrieben:", ziel)


if __name__ == "__main__":
    main()
