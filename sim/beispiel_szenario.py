"""Beispiel-Szenario fuer den Simulator: Wassereinbruch in der Figet Marena (nur Chips ohne Waffen).

Aufruf: python sim/beispiel_szenario.py

Laeuft mit vier Chips aus der echten Fahrzeugdatei: Abteile Sammler, Abteile, Schotten, Licht. Die Liquid Meter sind
die Fuehler (das Szenario setzt sie), die Schiebetueren und Lampen sind Stellglieder (das Szenario liest sie).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import swsim  # noqa: E402

CHIPS = ["Figet Marena Abteile Sammler", "Figet Marena Abteile", "Figet Marena Schotten", "Figet Marena Licht"]


def szenario(fz, tick):
    """Wird vor jedem Tick gerufen. Fuehler-Werte bleiben stehen, bis sie neu gesetzt werden."""
    if tick == 0:
        for teil in fz.daten.nach_art()["water_measure"]:      # alle Liquid Meter: dichter Raum, 1000 L, leer
            g = swsim.TeilGriff(fz, teil)
            g.setze("Fluid Capacity", 1000.0)
            g.setze("Liquid Level", 0.0)
        fz.teil(d="clock").setze("Time", 0.9)                   # Uhr: 21:36 Uhr (Nacht)
    if tick == 120:                                             # nach 2 s: 50 L Wasser im Abteil SEITE BB
        fz.teil(d="water_measure", pos=(-18, -15, -40)).setze("Liquid Level", 50.0)


def main():
    fz = swsim.Fahrzeug("Figet Marena", chips=CHIPS)
    tuer = fz.teil(d="door", pos=(-4, -12, 3))                  # eine Schiebetuer der vordersten Schottwand
    lampe = fz.teil(d="small_light_rgb", pos=(-17, 1, 0))
    for sek in range(5):
        fz.tick(60, szenario)
        print("nach %d s: Tuer vorn %s, Lampe R/G/B %s" % (
            sek + 1, "auf" if tuer.lese("Open/Close") else "zu", ["%.2f" % v for v in lampe.lese("Color Data").n[:3]]))
    print("Abteil-Monitor (Texte aus onDraw):")
    for z in fz.teil(d="monitor_9", pos=(8, 21, -23)).texte("Video Signal", 288, 160):
        print("   ", z)
    for z in fz.bericht():
        print(z)

    # Mehrspieler: Gast bekommt dieselben Fuehler; Chip-Anschluesse vom Host nur alle 120 Ticks (Modell vermutet)
    mp = swsim.Mehrspieler("Figet Marena", chips=CHIPS, abgleich_ticks=120)
    mp.tick(300, szenario)
    gleich = mp.host.teil(d="door", pos=(-4, -12, 3)).lese("Open/Close") == mp.gast.teil(d="door", pos=(-4, -12, 3)).lese("Open/Close")
    print("Mehrspieler nach 5 s: Tuer beim Gast wie beim Host:", "ja" if gleich else "nein")


if __name__ == "__main__":
    main()
