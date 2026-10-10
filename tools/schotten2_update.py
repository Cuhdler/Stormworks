"""Schotten v2.0 ins Schiff (Andre 10.10.: "die Tuer-Knoepfe sind nur auf der linken Seite, und der Knopf oeffnet beide -
gedacht war pro Tuer ein Knopf"):
- 5 Kippschalter (2 Seiten) an Steuerbord: der Wandblock an der gespiegelten Stelle des Backbord-Schalters wird durch
  den Schalter ersetzt (Drehung an der Mittellinie gespiegelt; der zweite Block des Schalters liegt dahinter frei)
- Chip "Figet Marena Schotten" 4x3 -> v2.0 6x4 an derselben Stelle der Decke (vp (-2,13,-50), x -2..3, z -53..-50)
- Kabel: alle 17 Kabel des alten Chips weg; neu: Abteile 'Schotten auf' -> 'Alle auf'; je Schalter Toggled ->
  'Knopf BB/SB Wand k'; 'Tuer BB/SB Wand k' -> Open/Close genau dieser Tuer; 'Zustand' -> Abteile 'Tueren';
  Strom Batterie (-4,-13,-46) -> die 5 neuen Schalter (die Backbord-Schalter haben ihr Stromkabel schon)
Probe: ausser dem Chip, den 5 Bloecken -> Schaltern und den Kabeln aendert sich nichts.
Aufruf: python schotten2_update.py [--schreiben]   (vorher sichern; danach Schiff neu laden, NICHT vorher speichern)
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import umbau_v1 as u  # noqa: E402
import kabel_flak as kf  # noqa: E402
import sperrprofil  # noqa: E402
import build_schotten as bs  # noqa: E402
from build_schiff import BUILD  # noqa: E402
from feuer_rechts_update import chip_knoten  # noqa: E402
from autopilot_update import link, enden, chip_flaeche, flaeche, teil_bereich, BATT, LINKS  # noqa: E402

SCH, AB = "Figet Marena Schotten", "Figet Marena Abteile"
VP, R_ = (-2, 13, -50), "1,0,0,0,-1,0,0,0,-1"
KN = "button_toggle_2side"


def gespiegelt(r):
    """Drehung des Backbord-Schalters -> Steuerbord: lokal y und z an der Mittellinie gespiegelt, lokal x umgedreht
    (sonst waere es eine Spiegelung statt einer Drehung; beide Anschluesse liegen bei lokal x 0)."""
    q = [int(float(v)) for v in r.split(",")]
    return ",".join(str(v) for v in [q[0], -q[1], -q[2], -q[3], q[4], q[5], -q[6], q[7], q[8]])


def block_bereich(s, vp, a0, e0):
    """(Anfang, Ende) des einfachen Blocks (<c> ohne d) an vp im Bereich a0..e0."""
    for m in re.finditer(r'<c(?: t="\d+")?><o[ >][^>]*?>?', s[a0:e0]):
        a = a0 + m.start()
        e = s.index("</c>", a) + 4
        v = re.search(r"<vp([^/]*)/>", s[a:e])
        if v and u.xyz(v.group(1)) == vp:
            assert "<logic_slots>" not in s[a:e] and s[a:e].count("<c") == 1, s[a:e]
            return a, e
    raise ValueError(("Block fehlt", vp))


def main():
    s0 = open(u.VEH, encoding="utf-8", newline="").read()
    s = s0
    assert 'description="Schotten v1.0' in s, "Stand passt nicht (Schotten v1.0 erwartet)"
    i0 = s.index("<bodies>")
    ra, re_ = s.index("<body ", i0), s.index("</body>", s.index("<body ", i0))
    # 1. Steuerbord-Schalter statt Wandblock (von hinten nach vorn ersetzen, damit die Stellen davor gueltig bleiben)
    ersatz = []
    for wd in bs.WAENDE:
        a, e = teil_bereich(s, KN, wd[2])
        bb = s[a:e]
        assert '<c d="%s"><o r="' % KN in bb, bb[:80]
        r = re.search(r'<o r="([^"]*)"', bb).group(1)
        sb = bb.replace('r="%s"' % r, 'r="%s"' % gespiegelt(r), 1)
        sb = re.sub(r"<vp[^/]*/>", u.vox("vp", wd[3]), sb, count=1)
        ba_, be_ = block_bereich(s, wd[3], ra, re_)
        ersatz.append((ba_, be_, sb))
    for a, e, neu in sorted(ersatz, reverse=True):
        s = s[:a] + neu + s[e:]
    # 2. alten Chip raus, neuen an dieselbe Stelle
    kalt = chip_knoten(s, SCH)
    alt_flaeche = chip_flaeche(s, SCH)
    a, e = u.mc_bereich(s, SCH)
    u.CHIP = os.path.join(BUILD, "%s %s.xml" % (SCH, bs.VERSION))
    d = u.chip_eingebettet()
    w = int(re.search(r'<microprocessor_definition [^>]*width="(\d+)"', d).group(1))
    ln = int(re.search(r'<microprocessor_definition [^>]*length="(\d+)"', d).group(1))
    nk = len(re.findall(r"<n id=", d))
    R = [[int(v) for v in R_.split(",")][i * 3:i * 3 + 3] for i in range(3)]
    fl = flaeche(R, VP, w, ln)
    teile_vox = set(p for teile in sperrprofil.koerper() for dd, p in teile if dd != "microprocessor")
    chips_vox = set()
    for mm in re.finditer(r'<microprocessor_definition name="([^"]*)"', s):
        if mm.group(1) != SCH:
            chips_vox |= chip_flaeche(s, mm.group(1))
    belegt = teile_vox | chips_vox
    assert not (fl & belegt), ("Platz belegt", sorted(fl & belegt))
    vor = set((p[0] + R[1][0], p[1] + R[1][1], p[2] + R[1][2]) for p in fl)
    hinter = set((p[0] - R[1][0], p[1] - R[1][1], p[2] - R[1][2]) for p in fl)
    assert not (vor & belegt), ("unter dem Chip ist kein Raum", sorted(vor & belegt))
    # Decke: der alte Chip hing schon unter einem Loch bei (0,14,-52) - es reicht, wenn fast alle Felder anliegen
    luecken = sorted(hinter - teile_vox)
    assert len(luecken) <= 2, ("ueber dem Chip fehlt die Decke", luecken)
    if luecken:
        print("Hinweis: ueber dem Chip keine Decke bei", luecken, "(der alte Chip hing dort genauso)")
    teil = '<c d="microprocessor"><o r="%s" bc="70787D" sc="%d">%s%s<logic_slots>%s</logic_slots></o></c>' % (
        R_, 2 * w * ln + 2 * (w + ln), d, u.vox("vp", VP), "<slot/>" * nk)
    s = s[:a] + teil + s[e:]
    ks = chip_knoten(s, SCH)
    ka = chip_knoten(s, AB)
    print("Schotten %s %dx%d an der Decke %s: x %d..%d, z %d..%d (vorher %d Felder)" % (
        bs.VERSION, w, ln, VP, min(p[0] for p in fl), max(p[0] for p in fl), min(p[2] for p in fl), max(p[2] for p in fl),
        len(alt_flaeche)))
    # 3. Kabel
    tl = kf.teile(s)

    def an(d_, vp, lab, mo_soll, ty_soll):
        p, mo, ty = kf.anschluss(tl, d_, vp, lab)
        assert mo == mo_soll and ty == ty_soll, (d_, vp, lab, mo, ty)
        return p
    li, le = s.index("<logic_node_links>") + len("<logic_node_links>"), s.index("</logic_node_links>")
    alt_l = re.findall(LINKS, s[li:le])
    assert "".join(alt_l) == s[li:le]
    alte_knoten = set(kalt.values())
    weg = [x for x in alt_l if any(p in alte_knoten for p in enden(x))]
    assert len(weg) == 17, ("erwartet 17 Kabel am alten Chip", len(weg))
    bleibt = [x for x in alt_l if x not in weg]
    strom = an(BATT[0], BATT[1], "Electric Store", 1, 4)

    kp = ks.get
    neu = [(0, ka["Schotten auf"], kp("Alle auf"), "Abteile 'Schotten auf' -> Schotten 'Alle auf'"),
           (5, kp("Zustand"), ka["Tueren"], "Schotten 'Zustand' -> Abteile 'Tueren'")]
    for k, wd in enumerate(bs.WAENDE):
        for s_ in range(2):
            seite = bs.SEITE[s_]
            neu.append((0, kp("Tuer %s Wand %d" % (seite, k + 1)), an("door", wd[s_], "Open/Close", 1, 0),
                        "Tuer %s Wand %d -> Tuer %s" % (seite, k + 1, wd[s_])))
            neu.append((0, an(KN, wd[2 + s_], "Toggled", 0, 0), kp("Knopf %s Wand %d" % (seite, k + 1)),
                        "Kippschalter %s -> Knopf %s Wand %d" % (wd[2 + s_], seite, k + 1)))
        neu.append((4, strom, an(KN, wd[3], "Electric", 1, 4), "Strom -> Kippschalter %s" % (wd[3],)))
    belegte_eing = set((int(t or 0), p1) for t, p1 in re.findall(
        r'<logic_node_link(?: type="(\d+)")?><voxel_pos_0[^>]*/>(<voxel_pos_1[^>]*/>)', "".join(bleibt)))
    zu = []
    for typ, p0, p1, was in neu:
        assert (typ, u.vox("voxel_pos_1", p1)) not in belegte_eing, ("Eingang schon belegt", was, p1)
        zu.append(link(typ, p0, p1))
        print("  %-48s %s -> %s" % (was, p0, p1))
    s = s[:li] + "".join(bleibt + zu) + s[le:]

    # 4. Probe: ohne Chip, Kabel und die 5 Stellen muss alles gleich sein
    def ohne(x, bloecke_neu):
        a2, e2 = u.mc_bereich(x, SCH)
        x = x[:a2] + "<CHIP/>" + x[e2:]
        li2, le2 = x.index("<logic_node_links>"), x.index("</logic_node_links>")
        x = x[:li2] + x[le2:]
        i2 = x.index("<bodies>")
        ra2, re2 = x.index("<body ", i2), x.index("</body>", x.index("<body ", i2))
        st = []
        for wd in bs.WAENDE:
            st.append(teil_bereich(x, KN, wd[3]) if bloecke_neu else block_bereich(x, wd[3], ra2, re2))
        for a3, e3 in sorted(st, reverse=True):
            x = x[:a3] + "<STELLE/>" + x[e3:]
        return x
    assert ohne(s0, False) == ohne(s, True), "ausser Chip, Schaltern und Kabeln geaendert"
    print("Probe: Schotten %s neu, 5 Steuerbord-Schalter statt Wandbloecken, %d Kabel weg, %d neu, sonst nichts" % (
        bs.VERSION, len(weg), len(zu)))
    ziel = u.VEH if "--schreiben" in sys.argv else os.path.join(os.environ.get("TEMP", "."), "schiff_probe.xml")
    with open(ziel, "w", encoding="utf-8", newline="") as f:
        f.write(s)
    print("geschrieben:", ziel)


if __name__ == "__main__":
    main()
