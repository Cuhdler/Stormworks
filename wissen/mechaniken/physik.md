# Physik und Mechaniken

Zusammengefasst aus dem Wiki (Stand der Seiten 2022–2025) und eigenen Beobachtungen. Wiki-Inhalte [W] in eigenen
Worten; bei Abweichungen im Spiel hier korrigieren und auf [G] setzen.

## Grundwerte [W]

- Schwerkraft 10 m/s² (statt 9,81). Spiel-Kraft-Einheit 1 = 1 kg · 10 m/s².
- Physik-Engine: Bullet.
- **Luftwiderstand viel höher als in echt** („Luft wie Suppe“): Propeller und Düsen wirken stark, Gleiten ist schwer,
  Flügel-Auftrieb ist kaum spürbar – Flugzeuge halten sich vor allem durch Tempo/Schub.
- Schnell drehende Gelenke (Pivots, Scharniere, Ketten) erzeugen viel Drehimpuls und können das ganze Fahrzeug drehen.

## Schwimmen und Dichtigkeit [W]

- Schwimmt, wenn die Gesamtdichte unter der des Wassers (1 kg/L) liegt.
- Normaler Block: Masse „1“ = 10 kg, 0,25 m Kante = 15,625 L → 640 kg/m³, schwimmt. Gewichtsblock: Masse 10 = 100 kg,
  6400 kg/m³, sinkt. Motoren, Generatoren, Batterien, Waffen sind dicht/schwer → viel eingeschlossene Luft nötig.
- Luft hat keine Masse. **Nicht geschlossene Räume unter der Wasserlinie gelten sofort als voll Wasser.**
- Geschlossene Räume mit offener Tür/Luke unter Wasser laufen langsamer voll (Pumpen können mithalten).
- Undichte Stellen: jede Lücke; **nicht verschmolzene Teile** (außer passende Tür-Ränder); **Ecken von Flüssigkeits-
  tanks**; **Batterien** (nur die Unterseite dichtet). Normale Rohre lassen Wasser durch (geschlossene Rohr-Varianten
  nehmen).
- Lecksuche: Liquid Meter in den Raum, Capacity anzeigen; 0 = nicht dicht. Raum mit Zwischenwand teilen, je Teil ein
  Meter, so lange halbieren, bis das Loch gefunden ist. (Der Abteil-Chip der Figet Marena zeigt dann OFFEN/LECK.)

## Flüssigkeiten und Gase [W] (Wiki-Stand v1.15.1)

- Fließen vom höheren zum niedrigeren Druck; Flüssigkeiten sind nicht zusammendrückbar.
- **Höhe beeinflusst den Druck nicht mehr** (seit Space-DLC): zwei halbvolle Tanks auf verschiedener Höhe tauschen
  nichts aus; Abpumpen von oben oder unten ist gleich schnell.
- Verbundene Tanks gleichen sich in der Zusammensetzung an, außer durch Einweg-Teile (Rückschlagventil, Pumpe);
  Überdruckventile für Flüssigkeit lassen nur Flüssigkeit, für Gas nur Gas durch.
- Rohre speichern nichts; jedes Fluid-Teil hat nur einen kleinen Puffer je Anschluss.
- Selbstgebaute Tanks aus Blöcken: Keile, Chips, Fenster vergrößern das Volumen (nehmen weniger als einen Block ein).
  Ein Block Volumen = 15,625 L. Tanks: klein 1×1×2 = 31,25 L, mittel 2×2×3 = 187,5 L, groß 3×3×5 = 703,125 L.
- Fertige Tanks haben Gasdruck zum Auspressen, **selbstgebaute nicht** → beim Leerpumpen entsteht Unterdruck; abhelfen
  mit einem Gas-Überdruckventil von innen nach außen (Flüssigkeit geht da nicht durch).
- Diesel + Kerosin im selben Tank werden bei Kälte zu Öl; Öl lässt sich heiß zu beiden verarbeiten.
- Luftdruck sinkt mit der Höhe (500 m ≈ 0,94 atm), Wasserdruck steigt mit der Tiefe.
- Gase: Luft (~20 % O₂, ~79 % N₂, ~1 % CO₂), Sauerstoff, Stickstoff, Wasserstoff spawnbar; CO₂ und Dampf entstehen.
  Spieler ersticken unter 15 % Sauerstoff oder über 10 % CO₂ (ohne Anzug); Druck ohne Anzug 0,12–4 atm.
- Pumpen: je Tank ein eigener Anschluss – zwei Pumpen über ein T-Stück an einem Tank pumpen eher langsamer.

## Flügel [W]

- Flügel erzeugen Kraft in ihre Richtung; verkehrt herum = Abtrieb.
- **Fehler im Spiel:** Flügel/Ruder auf Körpern hinter Gelenken liefern keine Kraft, wenn der Schub (z. B. Düse) auf
  einem anderen Körper sitzt.
- Selbstgebaute Flügel liefern weniger Auftrieb als die fertigen.

## Motorkühlung

- Modulare Motoren brauchen einen Kühlkreis über die Coolant Manifolds (Pumpen, Kühler oder Wärmetauscher) [W].
- Wiki-Tipp: statt Luft-Kühlern ein Liquid-Liquid Heat Exchanger, dessen zweite Seite über Fluid Ports Meerwasser
  durchpumpt (bei Fluid Ports saugt der Motor nicht selbst → Pumpen in richtiger Richtung) [W].
  **Meerwasser im Kühlkreis verschleißt Teile, wenn auch wenig** (Andre, 09.10.) – darum auf der Figet Marena nicht genutzt.
- Wie stark Luft-Kühler sind und wovon die Motorleistung bei Hitze abhängt: `wissen/bauteile/README.md` (Modular-Diesel).

## Treibstoff [W]

- Diesel (Dieselmotoren), Kerosin (Strahltriebwerke – brauchen für gleiche Kraft weniger als Diesel), Kohle
  (Dampfkessel), Brennstäbe.
- Karriere: Fahrzeuge spawnen mit dem Treibstoff der Spawn-Stelle, die man selbst auffüllen muss. Diesel kaufen 2 $/L,
  verkaufen 3 $/L.

## Wellen (Drehung) [G]

- Getriebe: Pfeil zum Motor = Übersetzung ins Langsame; Kupplung 0..1; Motoren laufen ab ~2 RPS (Anlasser).
- Generatorleistung ~ Drehzahl² (siehe `strom.md`).
