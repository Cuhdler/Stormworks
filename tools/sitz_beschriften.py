"""Beschriftet den Steuersitz der Figet Marena (seat_compact (0,17,-10); Andre 10.10.: "den Fahrersitz beschriften fuer
alle Steuerungen"). Stormworks speichert die Texte im Sitz-Teil als hotkey_0_label..hotkey_5_label (Hotkey 1-6),
trigger_label (Leertaste) und control_mode_0_label..control_mode_3_label (A/D, W/S, Pfeil links/rechts, Pfeil hoch/
runter) - so in mehreren Workshop-Fahrzeugen auf Andres PC. Umlaute als ae/oe/ue (Spielschrift).
Probe: ausser dem einen Sitz aendert sich nichts.
Aufruf: python sitz_beschriften.py [--schreiben]   (vorher sichern; danach Schiff neu laden, NICHT vorher speichern)
"""
import os
import re
import sys
from xml.sax.saxutils import quoteattr

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import umbau_v1 as u  # noqa: E402
from autopilot_update import teil_bereich  # noqa: E402

SITZ = ("seat_compact", (0, 17, -10))
TEXTE = [
    ("custom_name", "Steuersitz"),
    ("control_mode_0_label", "Ruder (Autopilot: Kurs)"),
    ("control_mode_1_label", "Fahrhebel (Autopilot: Tempo)"),
    ("control_mode_2_label", "Bugstrahlruder"),
    ("control_mode_3_label", "Gang hoch/runter (bei HAND)"),
    ("hotkey_0_label", "Motoren an/aus"),
    ("hotkey_1_label", "Stopp: Hebel 0, auskuppeln, Autopilot aus"),
    ("hotkey_2_label", "Gaenge: Automatik/Hand"),
    ("hotkey_3_label", "Helm: alle Werte"),
    ("hotkey_4_label", "Naechste Waffe (Kamera)"),
    ("hotkey_5_label", "Zielkorrektur 0 (2 s: Blickmitte lernen)"),
    ("trigger_label", "Gewaehlte Waffe einmal feuern"),
]


def main():
    s0 = open(u.VEH, encoding="utf-8", newline="").read()
    a, e = teil_bereich(s0, *SITZ)
    teil = s0[a:e]
    m = re.match(r'(<c d="%s"(?: t="\d+")?><o )([^>]*)>' % SITZ[0], teil)
    attrs = m.group(2)
    for name, _ in TEXTE:
        attrs = re.sub(r'\s%s="[^"]*"' % name, "", attrs)
    neu_attrs = attrs + "".join(" %s=%s" % (n, quoteattr(t)) for n, t in TEXTE)
    neu = m.group(1) + neu_attrs + ">" + teil[m.end():]
    s = s0[:a] + neu + s0[e:]
    assert s0[:a] == s[:a] and s0[e:] == s[a + len(neu):], "ausser dem Sitz geaendert"
    print("Sitz %s %s:" % SITZ)
    for n, t in TEXTE:
        print("  %-22s %s" % (n, t))
    ziel = u.VEH if "--schreiben" in sys.argv else os.path.join(os.environ.get("TEMP", "."), "schiff_probe.xml")
    with open(ziel, "w", encoding="utf-8", newline="") as f:
        f.write(s)
    print("Probe: nur der Sitz geaendert; geschrieben:", ziel)


if __name__ == "__main__":
    main()
