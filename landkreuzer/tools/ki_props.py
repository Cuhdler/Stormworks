"""Eigenschaften (Property-Bauteile) der KI-Chips des KI Landkreuzers.

Je Eintrag: (Name, Standardwert, Erklaerung). Der Name muss genau so im Lua stehen (property.getNumber('Name')).
Der Chip-Bauer legt fuer jeden Eintrag ein Zahlen-Property an; Andre kann die Werte spaeter im Spiel aendern.
PROPS_FAHREN gehoert zu lua/ki_fahren.lua, PROPS_KARTE zu lua/ki_karte.lua.
"""

PROPS_FAHREN = [
    # Tempo
    ("Tempo m/s", 8, "Reisetempo der KI auf freier Strecke (8 m/s = knapp 29 km/h)"),
    ("Vollgas m/s", 12, "So schnell faehrt der Panzer auf ebenem Boden mit Vollgas (hilft dem Tempo-Regler)"),
    ("Kriech m/s", 1.5, "Schleich-Tempo nah an Hindernissen, am Wasser und in Schraeglage"),
    ("Rampe s", 1, "So lange braucht der Fahrbefehl von 0 auf voll (schont den Antrieb; Bremsen geht dreimal so schnell)"),
    ("Lenk Staerke", 4, "Wie kraeftig die KI auf den Kurs lenkt (hoeher = schneller, aber unruhiger)"),
    ("Dreh Gas", 0.6, "Lenkbefehl beim Drehen auf der Stelle (0 bis 1)"),
    ("Rad Richtung links", 1, "1 oder -1: Vorzeichen fuer den linken Antrieb (dreht die linke Seite falsch herum: -1)"),
    ("Rad Richtung rechts", -1, "1 oder -1: Vorzeichen fuer den rechten Antrieb (rechts ist gespiegelt eingebaut: meist -1)"),
    ("Richtung lernen", 1, "1 = die KI merkt selbst, wenn eine Seite falsch herum dreht, und dreht sie um (0 = aus)"),
    # Ziele
    ("Ziel Radius m", 20, "So nah muss der Panzer an einen Wegpunkt, dann gilt er als erreicht"),
    ("Revier m", 400, "Ohne Wegpunkte faehrt die KI zu Zufallspunkten hoechstens so weit vom Startpunkt"),
    ("Patrouille Pause s", 45, "Am Revier-Punkt so lange stehen bleiben (Strom sparen, Tuerme arbeiten weiter); 0 = gleich weiter"),
    # Hindernisse und Gelaende
    ("Hindernis m", 25, "Meldet ein Front-Laser weniger, wird langsamer gefahren und zur freien Seite gelenkt"),
    ("Notstopp m", 8, "Unter diesem Abstand nur noch Schleich-Tempo, bis klar ist: Hang oder Hindernis"),
    ("Steigung max Grad", 30, "Steiler darf ein Hang nicht sein; steiler = Hindernis (ausweichen)"),
    ("Kipp max Grad", 25, "Mehr Schraeglage = Gefahr, Stelle meiden: bei Nick zurueck, bei Roll langsam vor und zur hohen Seite drehen"),
    ("Wasser Hoehe m", 3, "Eigene Hoehe ueber dem Meer (Physik-Sensor) darunter: nur Schleich-Tempo; Boden unter dem Bug: ab 10 m darueber stufenlos langsamer"),
    ("Wasser Stopp m", 1.5, "Eigene Hoehe ueber dem Meer darunter: sofort zurueck und die Stelle meiden"),
    ("Absturz m", 2.5, "Misst der Bug-Laser so viel mehr als normal und kam das ploetzlich (steiler als 'Steigung max'), ist vorn eine Kante: zurueck"),
    # Fahrzeug-Masse und Laser
    ("Breite m", 9.5, "Breite des Panzers mit Raedern (fuer Sicherheitsabstand und enge Gassen)"),
    ("Laenge m", 27.5, "Laenge des Panzers (der Physik-Sensor sitzt etwa in der Mitte, der Bug-Laser ganz vorn)"),
    ("Laser Hoehe m", 2.4, "Hoehe der drei Front-Laser ueber dem Boden"),
    ("Boden Laser Hoehe m", 0, "Normale Messung des Bug-Lasers (senkrecht nach unten) auf ebenem Boden; 0 = Automatik: lernt sie, solange der Panzer vor dem KI-Start still steht"),
    ("Sensor Hoehe m", 2.1, "Hoehe des Physik-Sensors ueber dem Boden"),
    # Kampf
    ("Kampf Abstand m", 1500, "Ziel naeher als das: anhalten (stabile Plattform fuer die Tuerme)"),
    ("Kampf Tempo m/s", 0, "Tempo im Kampf (0 = stehen bleiben)"),
    ("Kampf Winkel Grad", 30, "Im Kampf den Bug so drehen, dass das Ziel hoechstens so weit seitlich liegt (0 = nicht drehen)"),
    ("Mindestabstand m", 150, "Ziel naeher als das: rueckwaerts Abstand gewinnen (Bug bleibt zum Ziel)"),
    # Sonstiges
    ("Batterie min", 0.1, "Batterie darunter (0 bis 1): KI haelt an (0 = Pruefung aus; Eingang 0 = nicht angeschlossen)"),
    ("Kompass Richtung", -1, "-1: der Kompass des Physik-Sensors zaehlt gegen den Uhrzeigersinn (wie beim Schiff)"),
    ("Nick Richtung", 1, "1: Physik-Sensor meldet Bug hoch positiv; sonst -1"),
    # -1: der Physik-Sensor meldet 'rechte Seite tief' NEGATIV - so arbeiten die Flossen der Figet Marena (lua/flossen.lua:
    # Roll = -Kanal 16), und die halten das Schiff im Spiel nachweislich gerade (v1.3, CHECKLISTE.md)
    ("Roll Richtung", -1, "-1: Physik-Sensor meldet rechte Seite tief negativ (wie bei den Flossen des Schiffs); sonst 1"),
]

PROPS_KARTE = [
    ("Zoom Start", 1, "Karten-Zoom beim Einschalten (kleiner = naeher dran; die Knoepfe +/- halbieren bzw. verdoppeln)"),
]

PROPS = PROPS_FAHREN + PROPS_KARTE
