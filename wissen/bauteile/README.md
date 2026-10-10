# Bauteile

## 1. Die Daten (aus dem Spiel erzeugt)

`python tools/bauteile_holen.py` liest auf dem PC `Stormworks\rom\data\definitions` (findet Stormworks über Steam,
sonst `-d <...>\Stormworks\rom\data\definitions`) und schreibt:

| Datei | Inhalt |
|---|---|
| `INDEX.md` | alle 759 Bauteile (Stand 09.10.2026) in einer Tabelle je Kategorie: Name, Datei-Name, Größe, Masse, Preis, Anschlüsse kurz |
| `<Kategorie>.md` | je Bauteil: Beschreibung aus dem Spiel, Größe, Werte, die vom Üblichen abweichen (Motorkraft, Auftrieb, Pumpendruck …), alle Anschlüsse mit Art, Richtung, Lage und Beschreibung |
| `bauteile.json` | dasselbe maschinenlesbar |

Nach jedem Spiel-Update neu erzeugen, committen und pushen. Die Dateien nie von Hand ändern.

Aufbau von `bauteile.json`: ein Eintrag je Bauteil. Der Schlüssel ist der Datei-Name ohne `.xml`, genau so steht
das Teil auch in der Fahrzeugdatei (`<c d="...">`).

| Feld | Bedeutung |
|---|---|
| `name` | Name im Spiel (englisch) |
| `kategorie` | Kategorie-Nummer im Spiel-Menü (0 Blöcke, 1 Fahrzeugsteuerung, 2 Bedienelemente, 3 Antrieb, 4 Spezialausrüstung, 5 Logik, 6 Anzeigen, 7 Sensoren, 8 Deko, 9 Flüssigkeiten, 10 Elektrik, 11 Strahltriebwerke, 12 Waffen, 13 Modulare Motoren, 14 Industrie, 15 Fenster) |
| `masse`, `preis` | Gewicht (1 = 10 kg), Preis in $ |
| `kurz`, `beschreibung` | Beschreibung aus dem Spiel (englisch) |
| `groesse`, `voxel_min`, `voxel_max` | Ausdehnung in Blöcken, lokal (vom Bezugsblock `vp` aus) |
| `bloecke` | alle belegten Blöcke `[x, y, z]`, relativ zum Teil |
| `anschluesse` | Liste `{label, ein, typ, pos, beschreibung}`: `ein` 1 = Eingang, 0 = Ausgang; `typ` = Signal-Art (Tabelle in `wissen/microcontroller/README.md`); `pos` = Block relativ zum Teil |
| `kind` | Versatz des zweiten Körpers bei Gelenken (Pivot, Drehkranz …) |
| `flags`, `tags`, `sonst` | Merkmale und alle weiteren Attribute der Spiel-Datei (ohne Grafik und Ton) |

Wo ein Anschluss im Fahrzeug liegt (spiegeln, drehen, verschieben): `wissen/fahrzeugdatei.md` Abschnitt 3.4.
**Ein Teil belegt mehr als seinen `vp`:** bei der Platzsuche die ganze Ausdehnung rechnen (am Jet waren „freie“
Stellen in Wahrheit Funkgerät und Video-Sender) [G 08.10.].

## 2. Suchen

```
python tools/bauteil_suchen.py laser            alle Bauteile mit "laser" im Datei-Namen oder Namen
python tools/bauteil_suchen.py laser_distance_sensor --voll    ein Bauteil mit allen Angaben
```

Oder in `INDEX.md` nach dem englischen Namen suchen (z. B. „Liquid Meter“ heißt in der Datei `water_measure`).

## 3. Im Spiel gelernt

Wie sich einzelne Bauteile verhalten. Neue Erfahrungen hier eintragen (mit Datum und Kennzeichen), allgemeine
Spielregeln in `wissen/mechaniken/README.md`.

### Sitze und Griffe

- Seat data (Composite) bei Sitz und Control Handle: Zahl 1 A/D, 2 W/S, 3 Pfeil links/rechts, 4 Pfeil hoch/runter,
  **9/10 Blick X/Y (Umdrehungen)**; An/Aus 1–6 Hotkeys, **31 Leertaste (Trigger), 32 besetzt** [S].
- Pfeil hoch/runter am Control Handle: Zoom mit Schwelle 0,5 sprach nicht an, mit 0,2 schon (08.10.) – Tastatur-
  Achsen steigen vermutlich erst an [G/V].
- Control Handle: Blick am Monitor als „Zeiger“ brauchbar (±0,09 U links/rechts, ±0,055 U oben/unten ≈ 5×3-Monitor
  aus Griff-Abstand), Hotkey zum Mitte-Lernen hilft [G 08.10.].

### Physik-Sensor

- Composite: 1 x, 2 Höhe, 3 z, 4–6 Euler-Winkel, 7–9 Tempo lokal, 10–12 Drehrate lokal, 13 Tempo gesamt (m/s),
  14 Drehrate gesamt, **15 Kippung lokal z, 16 Kippung lokal x (Umdrehungen), 17 Kompass (−0,5..0,5)** [S].
- Kompass zählt gegen den Uhrzeigersinn → Kurs im Uhrzeigersinn = −Kompass [G].
- Kippung = Neigung der jeweiligen Sensor-Achse gegen den Horizont; hängt nur an der Achsrichtung → bei verdreht
  eingebautem Sensor Achse zuordnen und Vorzeichen anpassen (Jet: Nick = −Kippung z, Querlage = −Kippung x) [G/V].
- Nase hoch = Kippung z positiv bei normal eingebautem Sensor [G].
- x = Ost, z = Nord (= Karten-/GPS-Koordinaten) [G].

### Laser Distance Sensor

- Bis 4000 m; ohne Treffer 4000 [G].
- **Sieht durch das Wasser bis zum Meeresboden** (Wellen und Wasseroberfläche zählen nicht). Log 08.10.: Strahl
  7,6° nach unten traf den Hafengrund in 270–430 m (36–57 m tief); der Autopilot hielt das mit falschem Vorzeichen
  für ein „Hindernis“ [G].
- Pivot (Composite 1 = X, 2 = Y) in **Umdrehungen**, höchstens ±0,125 [S]. Richtung hängt am Einbau: beim Bug-Laser
  der Figet Marena kippt Pivot Y plus den Strahl nach unten [G 08.10.].

### Kameras

- Camera Stabilized: Pivot/Pitch-Eingang = Drehtempo mit Totzone 0,1; 0,106 U/s je 1 darüber; ~8 Ticks Verzug;
  Composite 4/5 = Kopf-Neigung/-Drehung relativ zum Spawnen [G].

### Monitore

- Touch Output (Composite): Zahl 1/2 Breite/Höhe in Pixeln, 3/4 Druckpunkt x/y; An/Aus 1 gedrückt [G].
- Auflösung 32 px je Block (3×3 = 96×96, 5×3 = 160×96, 9×5 = 288×160) [G].
- Bild-Ausrichtung und Teile ohne `r`: `wissen/fahrzeugdatei.md` Abschnitt 3.1.

### Liquid Meter (`water_measure`)

- Liquid Level (Liter) + Fluid Capacity (Liter des geschlossenen Raums); Composite je Flüssigkeit (1 Wasser,
  2 Diesel, 3 Kerosin, 6 Öl, 7 Salzwasser, 9/10 Schlamm) [S].
- **Nicht in geschlossenem Raum: Capacity 0, Level = Höhe zum Wasser** (negativ = unter der Wasserlinie = Leck)
  [S/G – C4-Test 08.10.].
- Sensoren im selben Raum melden dasselbe; offene Türen verbinden Räume (Wert springt auf das gemeinsame Volumen) [G].
- Fluid Spawner (`water_spawner`) markiert einen geschlossenen Raum, der beim Spawnen mit Flüssigkeit gefüllt wird
  (Treibstofftanks im Doppelboden der Figet Marena) [S/G].

### Türen, Knöpfe, Licht, Uhr

- Sliding Door (Electric): Open/Close an = auf [S]. **Ohne Strom gehen elektrische Türen auf** [W – Wiki Electricity].
- Toggle Button (2 Sided): „Toggled“ hält den Zustand, von beiden Seiten der Wand bedienbar [S].
- Push Button: „Pressed“ nur solange gedrückt [S].
- Small Light RGB: Color Data Composite 1–3 = Rot/Grün/Blau **0..1** (Heli + Schiff) [G].
- Clock: Time 0 = Mitternacht, 0,5 = Mittag [S].
- Instrumentenblock: jedes Element ist `<display_N channel="K">`, `channel` zählt ab 0; Elemente **ohne** `channel`
  schreiben alle auf An/Aus 1 [G].

### Antrieb und Bewegung

- Robotic Pivot: Signal 1 = 90° [G]. Ruder-Bauteil: Signal 1 = 45° [G].
- Steuerflossen: Signal ±1 = ±0,25 rad; Signal + = Vorderkante hoch bei **allen**, auch gespiegelt eingebauten
  (Fahrtenschreiber 02.10.) [G].
- Drehkranz: dreht gespiegelt eingebaut andersherum [G].
- Jet Exhaust Rotating: Bereich ±0,5 Umdrehungen [G].
- Modular-Diesel, Temperatur: **volle Leistung bis ~75 °C, darüber bricht sie ein** – Figet Marena Gang 7 Vollgas
  (gleiche Drosseln): 25–75 °C 59–60 kn, 75–80 °C 54 kn, 80–85 °C 48 kn, 85–90 °C 45 kn; dabei wird das Gemisch im
  Zylinder magerer (Luftverhältnis 12,6 → 15,5) [G 07.10.]. Wärme entsteht aus dem verbrannten Treibstoff, nicht aus
  der Drehzahl [W – Wiki „Modular engine“]. Darum Temperatur-Regler auf ~70 °C, nicht höher.
- Modular-Diesel, Kühlung: 18-Zylinder-3×3-Motor mit 12 Electric Radiator 3×3, 24 Pumpen: Vollgas ab kalt ~15 °C/min;
  Gas weg → Temperatur fällt erst 10–15 s später [G 07.10.]. Getrennte Regler je Motor schaukeln sich gegenseitig auf
  (Seiten abwechselnd gedrosselt, Schiff zieht) → eine gemeinsame Grenze für alle Motoren [G].
- Feststoff-Booster (`solid_rocket_nozzle_*`): einziger Eingang „Trigger“ (zünden); brennt dann ohne Unterbrechung, bis
  der Treibstoff leer ist. Die Brenngeschwindigkeit ist eine Editor-Einstellung (langsamer = weniger Schub, länger) [S].
  Treibstoff-Blöcke (`solid_rocket_*`) auf den Booster stapeln = längere Brenndauer [S]. Im Flug nicht regelbar [W].
  Groß ab Medium mit Ausgang „Fuel Remaining“; der kleine Booster ist 1×1×1 [S].
- Elektromotoren (`motor_small/medium/large`): liefern Kraft ab 0 RPS, brauchen keine Kupplung; verbrauchen viel Strom,
  laut Wiki reichen auch mehrere nicht als Hauptantrieb großer Schiffe [W]. Bei leerer Batterie werden sie langsamer [W].
  Verbrauch noch nicht gemessen.
- Getriebe (`modular_engine_gearbox_1x1`): `gear_ratio_2` = Index „Ratio On“: 0 = 1:−1, 1 = 1:1, 2 = 6:5, 3 = 3:2 [G].
  Pfeil zum Motor = Übersetzung ins Langsame; Kupplung 0..1; Motoren laufen ab ~2 RPS (Anlasser) [G].

### Radar, Waffen, Munition

- Radar: zählt gespiegelt eingebaut gespiegelt; `m_sweep_mode="4"` = manueller Modus, `m_fov_x`/`m_fov_y` =
  Öffnungswinkel [G].
- Phalanx-Radar: Winkel ab Sockel; meldet nur, solange der Strahl über dem Ziel ist; behält alte Ziele in der Liste [G].
- Radar Detector springt evtl. auf eigene Radare an [V].
- Sprengköpfe (`warhead_*`): Eingang „Arm“; explodieren beim Aufprall oder bei Beschädigung [S] – laut Andre beim
  Aufprall auch ohne „Arm“ (10.10.). Darum geschützt aufstellen.
- Battle Cannon: Verschluss öffnet nach 79 Ticks, „Loaded“ ca. 98 Ticks nach dem Schließen [G].
- Munitions-Kennung `property_ammo_damage`: 1 HE, 2 Fragmentation, 3 AP, 4 Incendiary [G].
