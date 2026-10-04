"""Lage v3.1 (Andres Test 04.10. am feindlichen Hafen: die See-Plaetze hielten stehende Dinge, das Patrouillenboot
rechts voraus verlor seinen Platz und kam nie wieder): Chips tauschen wie kanone_update (Lage neu, die anderen in ihrer
aktuellen Fassung; Kabel, Lage, Eigenschaften bleiben, neue Eigenschaft 'See Ziel bis Grad' mit Vorgabe 145).
Probe: ausser den Chip-Definitionen aendert sich nichts.
Aufruf: python lage31_update.py [--schreiben]   (vorher sichern; danach Schiff neu laden, NICHT vorher speichern)
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kanone_update  # noqa: E402

if __name__ == "__main__":
    kanone_update.main()
