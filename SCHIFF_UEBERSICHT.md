# Figet Marena – Gesamtübersicht

**Stand:** 04.10.2026, Andres Speicherstand 22:56
**Fahrzeug:** `%APPDATA%\Stormworks\data\vehicles\Figet Marena.xml`
**Projektordner:** `Documents\Rok\Main Cloude\stormworks_schiff` (lua/, tools/, build/, backup/, logs/)
**Spiel:** Stormworks: Build and Rescue, nur DLC *Search and Destroy*, Andre spielt allein → alles von einem Sitz aus bedienbar.

Andre baut die Teile selbst (Rumpf, Türme, Radare, Kameras, Monitore). Die Microcontroller-Logik, die Skripte und
auf Wunsch die Kabel kamen von Claude (per Datei ins Fahrzeug geschrieben).

Weiterführende Dateien im Projekt:
- `CHECKLISTE.md` – Antrieb und Schiffsführung im Detail (Verlauf v0.8 bis v2.6, Flossen v1 bis v1.6)
- `WAFFEN_PLAN.md` – Waffensystem im Detail (Verlauf aller Versionen mit Log-Befunden)
- `KONZEPT.md` – ursprüngliches Konzept vom 26.09. (teilweise überholt, siehe Abschnitt 1)

---

## 1. Eckdaten

| | |
|---|---|
| Länge × Breite | ca. 56 m × 9,75 m (Rumpf x −19…19, z −155…69 Blöcke, Bug bei +z) |
| Höhe | y −21 (Kiel) bis 43 (Mastspitze) |
| Körper | 52 (Rumpf, Türme, Rohr-Gelenke, Kamera-Gelenke, 24 Raketen) |
| Teile im Rumpf | ca. 53 000 |
| Antrieb | 4 Diesel (je 18 Zylinder 3×3), 2 Schrauben, 8 Gänge |
| Höchsttempo | ca. 65–67 kn in Gang 7 (ruhiges Wasser, gemessen 02.10.), Gang 6 ca. 63 kn |
| Bewaffnung | Battle-Cannon-Turm (2 Rohre), Heavy-Autocannon-Turm vorn, 2 Flak-Türme (je 2 Heavy AC), 24 Raketen |
| Schutz | 2 × 60 Chaff-Werfer mit Auto-Chaff, Radarwarner, Lenzpumpen |

**Abweichungen vom Konzept (26.09.):** statt Jets jetzt 4 Diesel; statt Bertha jetzt 2 Battle Cannons; die
Autokanone hinten entfiel, dafür zwei Flak-Türme hinten; statt „Ziel markieren“ suchen sich alle Waffen ihre Ziele
selbst (Halbautomatik mit Master Arm).

---

## 2. Aufbau und wichtige Teile (Positionen in Blöcken)

| Bereich | Teile | Position |
|---|---|---|
| Brücke | Steuersitz (seat_compact) | (0,17,−10) |
| | Monitor 9×5 (Hauptbildschirm) | (0,22,−6) |
| | Monitor 2×3 (Waffenwahl, auf Gelenk, liegt flach) | (4,18,−8) |
| | Instrumentenblock (4 Schalter/Knöpfe) | (−2,19,−8) |
| | Monitor 3×3 (Raketen) | (−3,20,−10) |
| | Lockable Button (Raketen-Start) | (−1,19,−8) |
| Bruecken-Dach | Dachkamera (Camera Stabilized mit Laser) | (0,33,−15) |
| | Radar Detector (Radarwarner) | (0,32,−13) |
| Chip-Raum | alle Waffen-Chips; Wände x ±6, z −59…−48, y 2…13 | um (0,8,−55) |
| | Konstante (nicht anfassen) | (5,7,−59) |
| | Bool-Konstante (Monitor-Power) | (−5,6,−59) |
| Mittschiffs | Physik-Sensor (gemeinsam für alle Chips) | (0,27,−38) |
| Mast | 6 Radar (Phalanx), manueller Modus | siehe Abschnitt 5.1 |
| Unter Deck | Schiffsführungs-Chip (6×6), Flossen-Chip (3×4) | (0,−12,−41), (0,−5,−44) |
| Maschinenräume | 4 Diesel (L1/R1 unten y −16, L2/R2 oben y −8), getrennt links/rechts | x ±8, z −71…−89; Getriebe z −98…−101 |
| Heck | 2 Schrauben (giga_prop_small) | (±8,−16,−137) |
| | 2 Ruder (Bauteil `rudder`) + Ruder-Gelenke | (±9,−11,−148) |
| | Heck-Wasser-Messer (Liquid Meter, liegend) | (0,−16,−129) |
| Bug | Bugstrahlruder (Azimuth Thruster + Elektromotor) | (1,−16,41), Motor (0,−12,41) |
| | Sonar | (0,−19,16) |
| Strom | 2 Batterien Medium | (±8,−19,−65) |
| | 4 Batterien Large | (±4,−13,−39) und (±4,−13,−46) |
| | 2 Generatoren (an der Welle) | (±8,−15,−96) |
| Lenzen | 2 Large Fluid Pumps | (±15,−19,−56) |
| Chaff | 2 Ketten zu je 60 Flare Launchern, erster Werfer | (−8,17,−37) / (8,17,−37) |
| Raketen | 24 Plätze in 4 Reihen × 6 (Heck) | x −11/−4/4/11, z −112…−137 |

---

## 3. Antrieb und Schiffsführung

### 3.1 Hardware
- **4 Diesel** („Working ship engine“, 18 Zylinder 3×3, Schwungrad, Kupplung 3×3), keine ZE-Regler mehr
  (seit v1.0 macht der Chip Gemisch, Anlasser, Leerlauf selbst). L1/R1 unten, L2/R2 oben, je Seite auf eine Welle.
- **Getriebe je Seite:** A 6:5 (z −98), B 3:2 (z −99), C 2:1 (z −100), Rückwärts 1:−1 (z −101). Zusammen 8 Gänge
  ×1,0 / 1,2 / 1,5 / 1,8 / 2,0 / 2,4 / 3,0 / 3,6.
- **Ruder:** 2 Ruder-Bauteile, Signal 1 = 45° am Ruder (90° am Robotic Pivot). E-Motoren an den Power-Pivots.
- **Bugstrahlruder** (Elektromotor Medium im Bug).
- **Kühlung/Pumpen:** 96 Wasserpumpen, 48 Kühler-Lüfter, 48 kleine Kühlwassertanks (schaltet „Motor L/R an“).

### 3.2 Chip „Figet Marena Schiffsführung“ v3.3 (6×6, vp (0,−12,−41))
Skripte: `lua/schiff.lua` (v3.2), `lua/shud.lua` (Helm, v2.5), `lua/wellen.lua` (v2). Bau: `tools/build_schiff.py`.

- **Fahrhebel = Leistung** (Anteil der vollen Treibstoffmenge). Grenze ist die Temperatur: bis `Temp Ziel` 95 °C
  volles Gas, darüber so viel weniger, dass sie dort bleibt; über `Motor heiss Grad` 115 °C auskuppeln.
- **Gemisch:** Treibstoff = Luft × Q / Luftverhältnis, Q fest 7,1 (Andre: „soll immer gleich bleiben“); mit
  `Gemisch Regler` > 0 würde Q wieder nachgeregelt.
- **Anlasser:** sofort nach Hotkey 1, bis der Motor 0,5 s läuft; höchstens 8 s am Stück, dann 2 s Pause; startet nach
  Abwürgen selbst neu.
- **Kupplung:** erst wenn der Motor läuft, sanft über 3 s; aus bei Überhitzung oder Ausfall (der andere treibt weiter).
- **Gänge:** Automatik hoch über `Hoch ab RPS` 18 (nur wenn der Motor danach noch über `Runter unter RPS` liegt),
  runter unter 13; `Schaltzeit s` 1. Hotkey 3 = Hand/Automatik, von Hand Pfeil hoch/runter.
- **Rückwärts:** S unter null; Gangwechsel erst, wenn beide Kupplungen der Seite offen sind.
- **Lenken:** A/D = Ruder (`Ruder max` 0,5), dazu Lenk-Schub 0,6 (kurveninnere Seite weniger Gas) und Bugstrahlruder
  (`Bugstrahl beim Lenken` 1). Pfeil links/rechts = Bugstrahl von Hand.
- **Wellen-Schutz (wellen.lua):** kommen die Schrauben aus dem Wasser (Heck-Wasser-Messer, ab 15 kn), sperrt es das
  Schalten (+2 s); Drehzahl-Dämpfung gegen Schaukeln in kleinen Gängen.
- **Helm (Headset Video):** normal eine Zeile unten (Gang, Hebel, Tempo, Kurs, Ruder) + HEISS/AUSFALL; Hotkey 4 =
  alle Werte je Motor (RPS, Temperatur, Gas, Gemisch, Zustand).

### 3.3 Chip „Figet Marena Flossen“ v1.7 (3×4, vp (0,−5,−44))
Skript `lua/flossen.lua`, Bau `tools/build_flossen.py`, Kabel `tools/kabel_flossen.py`.

- **12 Steuerflossen:** 8 Control Fin Medium (vorn (±1,−21,25/28), Mitte (±9,−21,−92), hinten (±10,−16,−120))
  und 4 Control Fin Large (hinterste (±10,−16,−134), vorn-Mitte (±9,−21,−2)).
- **+ = Vorderkante hoch** bei allen Flossen (Sichttest 02.10.), `Richtung links/rechts` 1.
- **Regel:** Nick/Roll gerade halten (PD + langsamer I-Anteil), Heck zuerst (Schrauben im Wasser halten): steigt das
  Heck, drücken hinten/Mitte es kräftig runter (0,3 s Vorhalt). Vordere nur Nick/Hub, Rollen machen Mitte und
  vorn-Mitte. Wirkung ∝ Tempo², darum Verstärkung (60 kn / Tempo)², höchstens 4; unter 6 kn gerade.
- **Heck-Wasser:** Messer meldet die Tiefe der Schrauben (+ unter Wasser, Fahrt 1,5–2,5 m). Flacher als
  `Schraube tief min m` 1,5 → Heck runter. Ausgang „Physik weiter“ gibt das an die Schiffsführung (Wellen-Schutz).

### 3.4 Tasten (Steuersitz)

| Taste | Wirkung |
|---|---|
| Hotkey 1 | Motoren an/aus |
| Hotkey 2 | Stopp (Hebel 0, auskuppeln) |
| Hotkey 3 | Gang-Automatik an/aus |
| Hotkey 4 | Helm: alle Werte an/aus |
| Hotkey 5 | nächste Waffe (Kamera-Wahl) |
| Hotkey 6 | kurz: Zielkorrektur der gewählten Waffe auf 0; 2 s halten: Blick-Mitte lernen |
| W / S | Fahrhebel hoch/runter (bleibt stehen; unter 0 = rückwärts) |
| A / D | Ruder (+ Lenk-Schub + Bugstrahl) |
| Pfeil links/rechts | Bugstrahlruder von Hand |
| Pfeil hoch/runter | Gang von Hand (nur ohne Automatik) |
| Leertaste | gewählte Waffe schießt einmal (nur mit Master Arm) |
| Blick (Kopf) | Zielkorrektur, wenn der Knopf „Aim correction“ an ist (Abschnitt 5.6) |

### 3.5 Instrumentenblock (−2,19,−8)

| Element | Kanal | geht an |
|---|---|---|
| Master Arm (Schalter) | Bool 1 | Waffenwahl-Chip → alle Waffen dürfen schießen |
| Aim correction (Knopf) | Bool 2 | Kamera-Chip: Blick-Korrektur an |
| Auto Chaff (Schalter) | Bool 3 | Schutz-Chip |
| Water Pumps (Schalter) | Bool 4 | Schutz-Chip → beide Lenzpumpen |

---

## 4. Chip-Übersicht

| Chip | Version | Größe | Lage (vp) | Aufgabe | Skripte |
|---|---|---|---|---|---|
| Figet Marena Schiffsführung | v3.3 | 6×6 | (0,−12,−41) | Motoren, Gänge, Ruder, Bugstrahl, Helm | schiff, shud, wellen |
| Figet Marena Flossen | v1.7 | 3×4 | (0,−5,−44) | 12 Steuerflossen, Heck-Wasser | flossen |
| Figet Marena Lage | v3.3 | 4×4 | (−4,9,−59) | 6 Mast-Radare → 5 Ziele in der Welt | 6× mastradar, lage |
| Figet Marena Bildschirm | v3.3 | 4×3 | (1,9,−59) | Monitor 9×5, Zielverteilung, Master Arm | bild |
| Figet Marena Waffenwahl | v1.2 | 3×2 | (−4,5,−59) | Monitor 2×3: Waffe wählen | waffenwahl |
| Figet Marena Flak L | v2.8 | 4×5 | (−5,9,−58) | linker Flak-Turm | flakradar, flak |
| Figet Marena Flak R | v2.8 | 4×5 | (5,6,−58) | rechter Flak-Turm | flakradar, flak |
| Figet Marena Kanone BC | v1.6 | 4×7 | (−5,13,−58) | Battle-Cannon-Turm (2 Rohre, Lader) | flakradar, flak |
| Figet Marena Kanone AC | v1.6 | 4×5 | (5,10,−58) | Heavy-Autocannon-Turm vorn | flakradar, flak |
| Figet Marena Kamera | v2.2 | 4×5 | (5,10,−53) | Dachkamera, Zoom, Blick-Korrektur | kamera |
| Figet Marena Schutz | v1.0 | 2×3 | (−5,13,−51) | Auto-Chaff, Lenzpumpen | schutz |
| Quarter Panel NO (3×) | – | 1×2 | Maschinenräume | Andres Anzeigen (alt) | – |
| „Microcontroller“ (24×) | – | 3×3 | je Rakete | Raketen (Andre) | – |

Alle Waffen-Chips nutzen denselben Physik-Sensor (0,27,−38). Lua-Grenze im Spiel: 8192 Zeichen je Skript
(Lage-Skript 8119 – fast voll).

---

## 5. Waffensystem

### 5.1 Lagezentrale (Chip „Lage“ v3.3)
**Mast-Radare** (Radar Phalanx, manueller Modus per Gimbal, Strahl FOV 0,1):

| Radar | Position | Aufgabe |
|---|---|---|
| 1 | (0,42,−56) | sucht immer (kreist flach, 8°) |
| 2 | (0,42,−46) | hält Luftziel Platz 1 (frei: sucht 38° hoch) |
| 3 | (0,36,−44) | hält Luftziel Platz 2 (frei: sucht 20°) |
| 4 | (0,36,−58) | hält Seeziel Platz 3 (frei: sucht flach) |
| 5 | (−5,36,−51) | hält Seeziel Platz 4 (frei: sucht flach) |
| 6 | (5,36,−51), gespiegelt | **für Raketen reserviert**; Platz 5 wird nie vergeben, Radar 6 sucht bis dahin hoch (38°) mit |

- Kreisen 0,25 U/s. Winkel kommen **ab Sockel** (der Chip erkennt das selbst per Mehrheit; Log bestätigt).
  Gespiegelte Radare zählen gespiegelt (Radar 6 mit Vorzeichen −1).
- **5 Plätze:** 1–2 Luft, 3–4 See, 5 frei (Raketen). Neue Ortungen kommen erst in einen „Topf“ (bis 6 Kandidaten),
  bis ihre Art feststeht; ein näheres Ziel verdrängt das fernste seiner Art.
- **Filter:** Ziel vergessen nach 4 s; Reichweite 10 km; Mindestabstand 30 m; jedes Ziel hat eine feste Kennung.
- **Arten:** Luft (hoch genug/schnell genug, einmal Luft bleibt Luft solange schnell); **Land** = Nicht-Luftziel
  (geglättet) höher als 7 m über dem Meer → nie Kanonenziel; See-Ziel schneller als 28 m/s → kein Schiff
  (Tiefflieger); „bewegt“ = hat sich nachweislich bewegt (stehende Hafen-Dinge sind keine Ziele, Luftziele über 60 m
  auch stehend); nachweislich stehende Dinge kommen auf eine Merkliste (24 Orte) und werden ignoriert.
- **Bedrohung:** Luftziel näher als 1,5 km, kommt mit mehr als 5 m/s näher.

### 5.2 Hauptbildschirm (Chip „Bildschirm“ v3.3, Monitor 9×5)
- **Links:** 3D-Radar (Bug oben, Luftziele auf Strichen je nach Höhe, zoomt selbst, ferne Ziele als Pfeil am Rand,
  rotes Quadrat = wird beschossen, graue = stehend, dunkelorange = Luftziel, das keine Flak erreicht).
- **Mitte:** Bild der Dachkamera (nur das mittlere Drittel des Monitors zeigt Video) mit Fadenkreuz/Korrektur-Kreis.
- **Rechts:** Zielliste (Platz 1–5, L/S, km, Richtung, Höhe), gewählte Waffe, Master Arm, BEDROHUNG.
- **Zielverteilung (Halbautomatik):** jede Waffe nimmt das nächste passende Ziel und bleibt dabei; Wechsel nur bei
  weniger als halb so weit. Flaks nie auf dasselbe Ziel (bei nur einem: die Flak seiner Seite), Kanonen auf
  verschiedene, wenn möglich. Sperrprofile der Flaks bekannt (nur erreichbare Ziele); Kanonen nur in ihrem Bereich
  (BC bis ~105°, AC bis ~145° ab Bug). Reichweiten: BC 6 km, AC 2 km, Flak 3 km. Kanonen erst ab 150 m.
- **Master Arm an:** alle Waffen schießen selbst. Die Wahl (H5 oder Monitor 2×3) bestimmt nur die Kamera;
  Leertaste = gewählte Waffe einmal.

### 5.3 Waffenwahl (Chip „Waffenwahl“ v1.2, Monitor 2×3)
Schiff von oben (Umriss aus der Fahrzeugdatei), 4 Waffen als Kreise (BC orange, AC lila, Flak L hellblau, Flak R
weiß; hell = hat Ziel, Strich = Zielrichtung). Antippen = wählen, nochmal = keine. Quadrat in der Ecke = Master Arm.
Keine Schrift (stünde quer).

### 5.4 Türme

| Turm | Teile | Munition | Chip |
|---|---|---|---|
| Battle Cannon (vorn) | Turret Large (0,10,5), 2 × gun_l auf Pivots (±4,14,9), 2 Belt Feeder L (±1,14,7), Weiche (0,14,7), Radar Basic (0,17,11), Camera Medium + Laser (4,19,11) | HE | Kanone BC |
| Autokanone vorn | Turret Medium (0,6,31), Heavy AC gun_m (0,9,34) auf Pivots (±2,9,34), Radar Basic (0,12,35), Camera + Laser (−4,9,35) | Heavy AP | Kanone AC |
| Flak L / R (hinten) | Turret Medium (∓10, z −105), je 2 Heavy AC auf eigenen Pivots, Radar Basic (±10,21,−104), Camera (±15,20,−99) | Heavy Fragmentation | Flak L / Flak R |

**Gemeinsame Turm-Logik** (`flakradar.lua` + `flak.lua`, gleiche Skripte, nur Eigenschaften anders):
- Ziel kommt vom Bildschirm-Chip; das Turm-Radar (manueller Modus) wird aufs Ziel gehalten → dichte Meldungen.
- Spuren in Weltkoordinaten (Alpha-Beta-Filter), Vorhalt mit Ballistik (Mündungstempo, Luftwiderstand, Schwerkraft,
  eigene Fahrt), Nick/Roll des Schiffs eingerechnet, Sperrprofil (nie in eigene Aufbauten).
- Ohne Spur dreht der Turm schon zur Vorgabe.
- **Flak:** Zeitzünder = Flugzeit auf den nächsten Tick aufgerundet (Zerlegung knapp hinter dem Ziel), Rohre
  abwechselnd (alle 19 Ticks ein Schuss).
- **Battle Cannon:** Ladeablauf v2.5 – beide Rohre laden parallel (Melder „Contains Ammo“ der Zuführungen),
  Weichen-Polung lernt der Chip, Feuer abwechselnd; gemessen ca. alle 1,6 s ein Schuss. Ballistik 800 m/s,
  Drag 0,002 (Community-Werte), Zielhöhe fest 1,5 m über dem Meer.
- Ausgang „Kamera Zoom“ steuert noch die Turm-Kameras (deren Bild geht aber nicht mehr auf den Monitor).
- Eingang „Korrektur“ vom Kamera-Chip verschiebt den Zielpunkt.

### 5.5 Dachkamera (Chip „Kamera“ v2.2)
- Camera Stabilized auf dem Brücken-Dach. Pivot/Pitch sind **Tempo-Eingänge** (Totzone 0,1; 0,106 U/s je 1
  darüber; 8 Ticks Verzug), Composite 4/5 = Kopf-Neigung/-Drehung relativ zum Spawnen.
- **Messfahrt beim Spawnen** (~6 s): misst Drehtempo, Kipp-Seite (−1, sonst steht das Bild auf dem Kopf) und wohin
  Drehung 0 zeigt (über Laser-Treffer auf dem Meer).
- Schaut auf das Ziel der gewählten Waffe, **Zoom nach Entfernung**: Schiff (40 m) / Flugziel (20 m) füllt die
  halbe sichtbare Bildbreite. Ohne Ziel weit (1,2 rad).
- Video: Dachkamera → Kamera-Chip (zeichnet Kreis und Marke) → alle 4 Kamera-Eingänge des Bildschirm-Chips.

### 5.6 Zielkorrektur per Blick (Kamera v2.2 + Turm-Chips)
- Nur mit Knopf **Aim correction** an. Ist die Blick-Mitte innerhalb von 8° um das Fadenkreuz, wandert der
  Zielpunkt der gewählten Waffe in Blickrichtung (Joystick-Prinzip, bleibt stehen): am Kreisrand 2 mrad/s, Totzone
  0,8°. Hauptkreuz bleibt fest; die Waffe zielt aufs orange Korrektur-Kreuz.
- Hotkey 6 kurz = Korrektur 0; 2 s halten = Blick-Mitte neu lernen (Standard X 0°, Y 15°, im Log bestätigt).

### 5.7 Schutz (Chip „Schutz“ v1.0)
- **Auto-Chaff** (Schalter Auto Chaff): meldet der Radar Detector eine Ortung, feuern beide Ketten gleichzeitig eine
  Salve, danach alle 1,5 s, höchstens 8 je Ortung; neue Ortung erst nach 3 s Ruhe; insgesamt 60 Salven.
- **Lenzpumpen** folgen dem Schalter Water Pumps (Strom: Batterie L/R).
- Offen: ob der Radar Detector auch die eigenen Radare meldet (dann Dauer-Chaff; Log „sc“ Spalte ortung prüfen).

---

## 6. Schreiber (Logs)

- **Waffen-Schreiber:** steckt in allen Waffen-Skripten (Kopf LG/LF). Jeden Tick eine Zeile mit allem, was das
  Skript sieht und entscheidet; Pakete versetzt per HTTP an Port **8768**.
- **PC-Programm:** `python -u tools/waffen_logger.py` (im Ordner stormworks_schiff) → `logs/waffen_<Zeit>/<Kennung>.csv`
  (Spaltennamen aus `tools/schreiber_spalten.py`; `empfang.csv` = Ankunft/Paketnummern).
- **Kennungen:** r1–r6 Mast-Radare, la/laD Lage, ba Bildschirm, fLr/fLf und fRr/fRf Flak-Radar/-Feuerleitung L/R,
  kBr/kBf und kAr/kAf Kanonen, ka Kamera, sc Schutz.
- **Fahrtenschreiber** (Schiffsführung Port 8766) und **Flossen-Schreiber** (8767): `Log Port` steht auf 0 (aus).
  Anfragen an Ports ohne Lauscher blockieren die HTTP-Warteschlange des Spiels für Sekunden. Wieder an: Port setzen
  und `tools/logger.py` starten.
- Ein von Claude im Hintergrund gestarteter Logger läuft höchstens 2 h.

---

## 7. Werkzeuge und Arbeitsweise

- **Bauen:** `tools/build_*.py` erzeugt die Chip-XML aus `lua/*.lua` (verkleinert, Schreiber-Kopf, Eigenschaften)
  → `build/`; mit `--install` in die Spiel-Bibliothek.
- **Einbauen:** `tools/*_update.py` (z. B. `schutz_update.py`, `korrektur_update.py`): tauschen Chip-Definitionen,
  setzen Chips/Kabel, **Probe** (prüft, dass sich sonst nichts ändert) → ohne `--schreiben` nur Testdatei.
- **Prüfstände:** `tools/test_*.py` (Lage, Flak, Kanone, Kamera, Schutz, Schiff, Flossen) mit Lua 5.3 über `lupa`
  in einer Scratchpad-venv (System-Python hat kein lupa; venv wird gelegentlich gelöscht → neu anlegen).
- **Sicherungen:** `backup/Figet Marena vor <Schritt>.xml` vor jedem Schreiben; letzte: „vor Raketen (Andres Stand
  22-56)“.
- **Regeln:**
  - Nach jedem Schreiben durch Claude: Schiff **neu laden, ohne vorher zu speichern** (sonst speichert der Editor den
    alten Stand drüber).
  - Vor jedem Schreiben Datei-Zeit prüfen und gegen den letzten eigenen Stand vergleichen (Andre baut parallel).
  - Neue Chip-Anschlüsse immer **hinten anhängen**, damit alte Kabel bleiben.
  - Teile nur auf oberster Körper-Ebene einfügen (nie in einen anderen Microcontroller).
  - Andre darf/will Chips nicht per Editor-Eigenschaften umstellen → Einstellungen per Chip-Version.

---

## 8. Erkenntnisse aus dem Spiel (bestätigt)

- Lua: 8192 Zeichen je Skript; **kein `select`**, kein `table.unpack`; Eingänge in `onDraw` lesen = „draw error 202“.
- HTTP: höchstens eine Anfrage je Tick; Antwort braucht Content-Length; Ports ohne Lauscher blockieren 2–4 s.
- Spiel lief im Gefecht mit ca. 21–37 Ticks/s.
- Gespiegelte Teile (t-Attribut): Radare zählen gespiegelt; Drehkränze drehen andersherum; Steuerflossen: + =
  Vorderkante hoch bei allen.
- Phalanx-Radar: Winkel ab Sockel; meldet nur, solange der Strahl drüber ist.
- Instrumentenblock: Elemente ohne `channel` schreiben alle auf Bool 1.
- Camera Stabilized: Pivot/Pitch = Tempo mit Totzone 0,1; Laser ohne Treffer = 4000.
- Robotic Pivot: Signal 1 = 90°; Ruder-Bauteil: 1 = 45°.
- Munitions-Kennung im Spiel: `property_ammo_damage` 1 HE, 2 Fragmentation, 3 AP, 4 Incendiary.
- Gemessene Zielhöhen: fahrende Schiffe ca. −2 m (Ausreißer bis +6), stehende Dinge im Wasser 3–6 m,
  Bodenziele 14–16 m; fahrende Schiffe 6–13 m/s.
- Battle Cannon: Verschluss öffnet 79 Ticks, „Loaded“ ca. 98 Ticks nach dem Schließen.

---

## 9. Raketensystem – ursprünglicher Plan (fertig gebaut von Andre)

### 9.1 Andres Plan, wie es funktionieren sollte
- **Eigener Bildschirm** (Monitor 3×3 bei (−3,20,−10)): zeigt die Ziele des reservierten Raketen-Radars.
- **Radar:** Mast-Radar 6 ist für die Raketen reserviert. Weil die Raketen nur gegen **Schiffe und Landziele** gedacht
  sind, dreht sich das Radar rundum und bringt alle Ziele außer Luftzielen auf den Schirm.
- **Anzeige:** 2D von oben. **Seeziele blau, Bodenziele grün.** Ein drehender Strich zeigt, wohin das Radar gerade
  schaut. Ein Kontakt ist hell, wenn der Strich ihn gerade gefunden hat, und wird dunkler, bis der Strich wieder
  drübergeht.
- **Kontakte bleiben:** ein Ping verschwindet nicht, nur weil das Radar ihn ein paar Sekunden nicht sieht; erst nach
  **12 s** ohne Ortung wird er gelöscht.
- **Bedienung:**
  1. Ziel auf dem Touchscreen antippen → Ziel wird mit **rotem Quadrat** markiert.
  2. Das Raketen-Radar lockt dieses Ziel fest (Hardlock).
  3. Raketen-Startknopf (Lockable Button bei (−1,19,−8)) drücken. Er ist nur entsperrt, wenn **Master Arm an** ist
     **und** ein Ziel gelockt ist. Jedes Umschalten = eine Rakete.
  4. Eine Rakete startet und fliegt ins markierte Ziel.
- **Dachkamera:** soll auf das gewählte Raketenziel zeigen. **„Die letzte Auswahl gewinnt“:** Auswahl auf dem
  Raketen-Bildschirm → Kamera aufs Raketenziel; Waffe auf dem Hauptbildschirm gewählt → zurück auf deren Ziel.
- **Raketen-Radar** in jeder Rakete: Reichweite ca. 5 km, Sweep Mode statisch, FOV X 0,04 und FOV Y 0,04 (an der
  Rakete x −11, z −112 schon so eingestellt).
- **Luken:** Die Raketen sollen später aus dem Boden kommen, mit Klappen, die sich für sie öffnen. Zum Testen erst
  einmal ohne Luken.

### 9.2 Gebaute Hardware (Andre, Stand 22:56)
- **24 Raketen** in 4 Reihen × 6, senkrecht stehend (Spitze oben): x −11, −4, 4, 11; z −112, −117, −122, −127,
  −132, −137. Die Reihen x −4 und 11 sind gespiegelt eingebaut.
- **Halterung je Rakete:** connector_hardpoint_a am Schiff (x −14/−1/1/14, y 0) und connector_hardpoint_b an der
  Rakete (x −12/−3/3/12).
- **Je Rakete (Beispiel x −11, z −112, von unten nach oben):** Düse Medium (y −8), Rocket Fins Medium (y −5),
  Treibsatz Medium (y −2), auf Höhe y 0: Hardpoint B, Physik-Sensor (−11,0,−111), kleine Batterie (−11,0,−112);
  Microcontroller 3×3 bei (−12,1,−113); Warhead Body Medium (y 5); Raketen-Radar (radar_advanced_missile, y 9,
  schaut nach oben); 8 kleine Steuerflossen (y 7 und y 2) und Pyramiden/Keile als Verkleidung.
- **Vorhandene Kabel je Rakete:** Batterie → Hardpoint B (Strom), → Physik-Sensor (Strom), → Rocket Fins (Strom).
- **Bedienteile:** Monitor 3×3 (−3,20,−10), Lockable Button (−1,19,−8).

### 9.3 Stand
- **Fertig gebaut (Andre, 05.10.2026).** Raketen-Chip „Figet Marena Raketen“, seine Kabel, Radar 6, Monitor 3×3,
  Startknopf und die 24 Raketen bei anderen Änderungen unverändert lassen.
- Die Kopie in `fahrzeug/` ist noch der Stand vom 04.10. (ohne Raketen-Chip).

---

## 10. Offene Punkte (ohne Raketen)

- **Schutz:** im Log „sc“ prüfen, ob der Radar Detector auf die eigenen Radare anspringt.
- **Knopf „Aim correction“:** rastet er ein (mode 1)? Falls nicht, im Skript auf Umschalten je Druck ändern.
- **Luken** für die Raketenschächte: reine Mechanik per Knopf (Sliding Hatch o. ä.), noch nicht gebaut.
- **Wasser im Motor nach Tanktreffer:** einfache Lösungen ohne Filter/Zentrifuge noch offen (z. B. getrennte Tanks je
  Motor, Tanks weiter innen/geschützt).
- **Turm-Kameras:** ihr Bild wird nicht mehr gebraucht (Dachkamera); Zoom-Ausgänge könnten später entfallen.
- **Lage-Skript:** 8119 von 8192 Zeichen; für neue Funktionen müsste es aufgeteilt werden.
- **Höchsttempo:** seit dem Umbau am 02.10. ca. 25 % mehr Widerstand (Ballast, Türme); Gang 8 ungetestet.
- **Links/rechts-Unterschied** im Tempo der Seiten (seit 02.10.) – Ursache offen.
- **Getriebe C** (z −100, beide Seiten): kein Wert in der Datei (Standard) – im Editor prüfen, ob 2:1.
- **Werkzeuge:** `build_mc.py` (aus `stormworks_flugpanzer\tools`) fehlt im Repo – ohne kann Claude keine Chips bauen.

## 11. Ideen für später

- **Raketenabwehr** (Andre will am 06.10. abends anfangen): nur Rohrwaffen und Täuschung, keine Abfangraketen.
  1. Lage erkennt schnelle kleine Luftziele als „Rakete“, höchster Vorrang für die Flaks (Lage-Skript vorher aufteilen).
  2. evtl. eigener Abwehrturm (z. B. Rotary Autocannon + Radar), Logik aus Flak abgeleitet.
  3. Auto-Chaff auch bei erkannter Rakete. 4. Warnung „RAKETE“ + Richtung auf Hauptbildschirm und Helm.
  Offen: welche Gegner/Raketen, Flaks oder eigener Turm (wo, welche Kanone), Log einer anfliegenden Rakete (Tempo, Höhe).
- **Ferngesteuerte Fahrzeuge** (Drohne/Boot vom Schiff): Sitz → Chip → Radio (Frequenz) → Radio → Chip im Fahrzeug,
  Rückkanal auf zweiter Frequenz. Allein bedienbar nur, wenn das Schiff solange selbst Kurs hält oder stoppt. Grenzen:
  Funkreichweite, ferne Fahrzeuge werden nicht simuliert, Video per Funk unklar.
