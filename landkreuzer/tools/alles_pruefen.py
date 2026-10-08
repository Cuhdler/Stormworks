"""Baut beide Varianten des KI-Landkreuzers neu und laesst alle Pruefstaende laufen.

Aufruf (mit einem Python, das lupa hat): python landkreuzer/tools/alles_pruefen.py [--schnell]
--schnell: ohne die langen Simulationen (test_ki, test_land_lage, test_land_kanone)
"""
import os
import subprocess
import sys
import time

HIER = os.path.dirname(os.path.abspath(__file__))

SCHRITTE = [
    ("Fahrzeug bauen (Skid)", ["bau_landkreuzer.py"], False),
    ("Fahrzeug bauen (Lenkung)", ["bau_landkreuzer.py", "--lenkung"], False),
    ("Chip-Baukasten gegen Schiff", ["test_build_mc.py"], False),
    ("KI-Teile (Kleber, Lenkung, Status)", ["test_ki_teile.py"], False),
    ("Fahr-KI Simulation", ["test_ki.py"], True),
    ("Lage/Bildschirm an Land", ["test_land_lage.py"], True),
    ("Kanonen gegen Bodenziele", ["test_land_kanone.py"], True),
]


def main():
    schnell = "--schnell" in sys.argv
    ergebnis = []
    for name, args, lang in SCHRITTE:
        if lang and schnell:
            continue
        t0 = time.time()
        p = subprocess.run([sys.executable, os.path.join(HIER, args[0])] + args[1:], capture_output=True, text=True)
        aus = (p.stdout + p.stderr).strip().splitlines()
        ok = p.returncode == 0 and not any("FEHLER" in z for z in aus[-3:])
        ergebnis.append((name, ok, time.time() - t0, aus[-1] if aus else ""))
        print("%-40s %-6s %5.0f s  %s" % (name, "OK" if ok else "FEHLER", time.time() - t0, aus[-1][:80] if aus else ""))
    alle = all(e[1] for e in ergebnis)
    print("ALLES OK" if alle else "FEHLER")
    return alle


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
