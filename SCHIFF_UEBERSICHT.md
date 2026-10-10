# Figet Marena – Gesamtübersicht

**Stand:** 08.10.2026, 22:40 (Autopilot, Licht, Abteile/Sprit/Schotten/Pumpen, Jet-Steuerung)
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
| | 2 große E-Motoren (an der Welle vor den Getrieben, seit 10.10. statt der 2 kleinen Generatoren) | (±8,−13,−96) |
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
- **Kühlung/Pumpen:** 96 Wasserpumpen, 48 Kühler-Lüfter, 48 kleine Kühlwassertanks (schaltet „Motoren an“).
- **E-Motoren (10.10.):** 2 × Large Electric Motor (±8,−13,−96), je über ein T-Stück an der Welle vor den Getrieben
  (drehen also wie die Diesel, Gänge und Rückwärts gelten auch für sie); Strom von den großen Batterien (±4,−13,−46).
  Keine Generatoren mehr an Bord: die Batterien laden nur noch an der Werkbank.

### 3.2 Chip „Figet Marena Schiffsführung“ v3.5 (6×6, vp (0,−12,−41))
Skripte: `lua/schiff.lua` (v3.5), `lua/shud.lua` (Helm, v2.6), `lua/wellen.lua` (v2). Bau: `tools/build_schiff.py`.

- **Fahrhebel = Leistung** (Anteil der vollen Treibstoffmenge). Grenze ist die Temperatur, über `Motor heiss Grad`
  115 °C auskuppeln.
- **E-Motoren (v3.5, 10.10.):** bekommen den Teil des Fahrhebels, den die Temperatur-Grenze den Dieseln wegnimmt
  (`E-Motor Anteil` 1; nicht beim Gas-Abzug der Wellen-Schutzes). Batterie-Ladung kommt über den Flossen-Chip
  (Kanal 21 → 25); unter `E-Motor ab Batterie` 0,5 aus, erst ab 0,55 wieder an. Je Seite `E-Motor Richtung L/R` (±1).
  `E-Motor Test` 1: Diesel bleiben ausgekuppelt, E-Motoren fahren mit dem Hebel (Drehrichtung prüfen, danach 0).
  Helm: schmale Zeile „E45“ = E-Gas 45 %, Warnung „E-MOTOR: BATTERIE“, wenn er gebraucht würde, aber die Batterie zu
  leer ist; H4-Seite „E-MOTOR xx %“ (statt Bugstrahl). Anschlüsse: „Motoren an“ und „Rückwaerts“ gelten jetzt für beide
  Seiten (die Signale waren schon gleich), auf den frei gewordenen Plätzen „E-Motor L/R“. Schreiber: Spalten
  `e_motor_pct`, `e_motor_aus_batterie`. Prüfstand `test_schiff.py` test_emotor; Nachbau `sim/` mit der Probe-Datei.
- **Temperatur-Regler (v3.4, 09.10.):** eine Gas-Grenze für alle 4 Motoren (Schiff fährt gerade), nach dem Motor, der
  am stärksten über dem erlaubten Anstieg liegt. Erlaubter Anstieg = (`Temp Ziel` 70 − Temperatur) / `Temp Anflug s`
  60; `Temp Regel` 0,2. Kalt knapp 3 min volles Gas, dann weich auf Dauerleistung (Modell: ca. 22 % Gas bei 70 °C).
  Warum 70 statt 95: bis 75 °C volle Leistung, bei 80–85 °C nur noch etwa die Hälfte (Gang 7 Vollgas 60 → 48 kn,
  Fahrt 07.10.). v3.3 regelte jeden Motor allein auf 95 °C und schaukelte (Seiten abwechselnd 10 % / 55 % Gas,
  18–29 kn, Schiff zog hin und her). Prüfstand: `tools/test_schiff.py` test_temperatur (Wärmemodell nach 07.10.).
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

### 3.3 Chip „Figet Marena Flossen“ v1.8 (3×4, vp (0,−5,−44))
- v1.8 (10.10.): neuer Eingang „Batterie“ (Charge der Batterie (−4,−13,−46)), geht auf Kanal 21 von „Physik weiter“ an die Schiffsführung.
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
| A / D bei Autopilot an | Soll-Kurs verstellen (10 Grad/s), verlässt die Route |
| W / S bei Autopilot an | Soll-Tempo verstellen (5 kn/s) |
| Hotkey 2 bei Autopilot an | Stopp und Autopilot aus |
| Leertaste | gewählte Waffe schießt einmal (nur mit Master Arm) |
| Blick (Kopf) | Zielkorrektur, wenn der Knopf „Aim correction“ an ist (Abschnitt 5.6) |

### 3.5 Instrumentenblock (−2,19,−8)

| Element | Kanal | geht an |
|---|---|---|
| Master Arm (Schalter) | Bool 1 | Waffenwahl-Chip → alle Waffen dürfen schießen |
| Aim correction (Knopf) | Bool 2 | Kamera-Chip: Blick-Korrektur an |
| Auto Chaff (Schalter) | Bool 3 | Schutz-Chip |
| Auto water pumps (Schalter) | Bool 4 | Abteil-Chip: Lenzpumpen automatisch, sobald Wasser in einem Abteil steht (seit 08.10.; vorher Schutz-Chip, Pumpen dauernd an) |

### 3.6 Autopilot (Chip „Figet Marena Autopilot“ v1.2, 4×3, vp (−4,12,−59), seit 08.10.)

- **Lage:** Chip zwischen Fahrersitz und Schiffsführung. Ein Composite-Umschalter im Chip (nicht das Skript) lässt das
  Sitz-Signal unverändert durch, solange der Autopilot aus ist. Ist er an, kommen Achse 1 (Ruder) und Achse 2
  (Fahrhebel) vom Skript `lua/autopilot.lua`; alle anderen Tasten gehen weiter direkt durch.
- **Knöpfe** (an der Karte): „Activate Autopilot“ (−4,19,−22) an/aus, „Reset“ (−5,19,−22) löscht die Route,
  „Automatic anti kollision“ (−8,19,−22) schaltet Bug-Laser und Ausweichen an/aus (beim Laden aus).
  Beim Einschalten des Autopiloten: Soll-Kurs = jetziger Kurs, Soll-Tempo = jetziges Tempo.
- **Karte** auf Monitor 5×3 (−6,21,−22), aufrecht gedreht (`screen.drawMap` lässt sich nicht drehen), Nord oben.
  Niemand am Griff: Schiff in der Mitte. Weißes Dreieck = Schiff, grüne Linie = Soll-Kurs, gelb = Route, rot =
  Laser-Treffer. Text: AP AUS/KURS/ROUTE, S = Soll-Kurs/-Tempo, I = Ist, WP = Wegpunkte, AK AN/AUS, Maßstab.
- **Control Handle** (−6,19,−21) für die Karte (seit v1.1, Touch ist raus): der Blick bewegt ein gelbes Kreuz
  (±0,09 U links/rechts, ±0,055 U oben/unten = Bildrand); solange man den Griff hält, bleibt die Karte stehen.
  Leertaste = Wegpunkt am Kreuz, nochmal an derselben Stelle = weg (höchstens 20). W/S oder Pfeil hoch/runter = Zoom
  (ab Achse 0,2, gehalten alle 0,4 s; v1.1 brauchte 0,5 und reagierte im Spiel nicht), ersatzweise Hotkey 3 näher /
  Hotkey 4 weiter. Blick knapp über den Bildrand schiebt die Karte. Hotkey 1 = jetziger Blick ist die Bildmitte,
  Hotkey 2 = Karte zurück aufs Schiff. Unten links: Entfernung Schiff–Kreuz.
- **Route:** mit Wegpunkten fährt er sie der Reihe nach ab (erreicht = näher als 150 m). Nach dem letzten: Kurs halten,
  mit „Am Ziel stoppen“ 1 Soll-Tempo 0.
- **Regler:** Kurs = (Fehler − 3 s × Drehrate) / 25 Grad + kleiner I-Anteil; Tempo = PI auf den Soll-Hebel, W/S-Pulse
  schieben den Fahrhebel der Schiffsführung dorthin. Den Hebel rechnet der Chip wie die Schiffsführung mit („Hebel
  Tempo“ 0,25, „Rückwärts max“ 0,5 müssen in beiden Chips gleich sein).
- **Anti-Kollision, Laser am Bug** (0,2,64): schwenkt in 9 Schritten über ±0,06 U, Nicken über Pivot Y ausgeglichen
  (0,3 Grad über waagerecht). Treffer in der Gasse (±30 m) näher als 400 m bzw. Tempo × 40 s = Hindernis: 35 Grad zur
  freieren Seite, 15 s halten, langsamer; ab 150 m Hebel 0 (nur bei Autopilot an; aus = nur Anzeige). Der Laser sitzt
  ~0,2 m über der Wasserlinie (im Hafen knapp darunter; er sieht durchs Wasser, das stört nicht).
- **Laser Höhe Richtung −1** (08.10. umgestellt): mit 1 zeigte der Strahl 7,6 Grad nach unten und traf durchs Wasser
  den Meeresboden (rote Punkte auf dem Wasser, „HINDERNIS“ im Hafen).
- **Ungeprüft im Spiel:** Vorzeichen von Pivot X („Laser Seite“), Blickrichtung am Griff („Blick X/Y Richtung“,
  „Blick X/Y U“), Zoom-Richtung von `drawMap`, Regler-Werte. Log „ap“ (Port 8768) zeigt alles.

### 3.7 Licht (Chip „Figet Marena Licht“ v1.0, 2×2, vp (1,12,−59), seit 08.10.)

- 55 kleine RGB-Lampen (Andre), immer an. Helligkeit nach der Uhr (Bauteil „Clock“ an der Chip-Wand (4,12,−59)):
  Tag 1,0 ab 6:30, Nacht 0,35 ab 19:30, je 1 h Übergang; Farbe warmweiß (1 / 0,92 / 0,8). Alles über Eigenschaften
  einstellbar („Hell Tag“, „Hell Nacht“, „Tag ab Uhr“, „Nacht ab Uhr“, „Farbe R/G/B“).
- Steuerungsraum = die 4 Deckenlampen (±4,25,−25) und (±4,25,−11): bei Bedrohung (Lage-Chip Bool 25, wie
  „BEDROHUNG“ am großen Bildschirm) rot, bleibt 5 s nach der letzten Meldung.
- Strom aller Lampen und der Uhr von der Batterie (−4,−13,−46). Skript `lua/licht.lua`, Prüfstand `tools/test_licht.py`.

### 3.8 Abteile, Sprit, Batterie, Schotten, Lenzpumpen (Chips „Figet Marena Abteile“ v1.6 4×8 (−5,5,−59) + „Abteile Sammler“ v1.1 4×5 (5,2,−58), seit 08.10.)

- 18 Liquid Meter: 10 in den Abteilen (Andre 08.10.) und 8 im Doppelboden (y −19) = **Treibstofftanks** (Fluid
  Spawner füllen sie beim Spawnen). (0,−16,−129) gehört dem Flossen-Chip (Heck-Wasser). Je Sensor Füllstand +
  Kapazität; Sensor 10–18 schickt der Sammler abwechselnd gepackt (Kapazität/200 L × 1000 + Promille, Zahl 32 = 0) und
  als Liter (Zahl 32 = 1). Abteil-Sensoren mit gleicher Kapazität und Füllung = ein Abteil (offene Schotten verbinden
  Abteile), nummeriert vom Bug.
- 8 Tanks, je Sensor einer (Andre; Abschnitte z 15/−1/−19/−42, je Backbord + Steuerbord). Anzeige SPRIT gesamt %
  und L, Tabelle mit 8 Balken (Spalten Heck links → Bug rechts, oben SB, unten BB), VERBR (L/s über 2 min), Restzeit;
  BATTERIE (Charge der großen (−4,−13,−46) und mittleren (−8,−19,−65), alle 6 in einem Netz). Tanks zählen nicht als
  Wasser.
- Monitor 9×5 (8,21,−23) steht senkrecht an Steuerbord, Bild nach Backbord (r 0,0,−1,−1,0,0,0,1,0; vorher ohne
  Drehangabe = kopfüber). Oben Grundriss waagerecht (Bug rechts, Steuerbord oben; Sensoren grün/gelb ab 1 %/rot ab
  20 %/grau = nicht dicht, Schotten grün auf/rot zu), darunter Liste Abteil – Prozent – Liter (3 Spalten), unten
  Pumpen (AN/AUS, L/s, „RAUS“ = gepumpt seit dem Laden, AUTO AN/AUS) und Schotten-Feld; „WASSER!“ blinkt.
- Lenzpumpen: Andres Lenzleitung (Einlässe in den Abteilen bei y −13, Rohr auf x 0, Pumpe (0,−4,−5), Rückschlagventil,
  Auslass an Deck (0,14,−47)) + die zwei alten (±15,−19,−56). Schalter „Auto water pumps“ an und ein Abteil ab 0,3 %
  Wasser → alle drei an, 20 s Nachlauf. Fluss = Summe der Flow Rates.
- Schotten = 10 Schiebetüren (Sliding Door (Electric), an = auf) in 5 Schottwänden (vom Bug: z 3, Oberdeck −13, −15,
  −29, −53, je Backbord + Steuerbord). Chip „Figet Marena Schotten“ v2.0 (6×4, Decke des Chip-Raums (−2,13,−50),
  x −2..3, z −53..−50): „alle zu/auf“ vom Abteil-Chip (Feld unten rechts antippen, Eingang „Knopf Schotten“ noch frei;
  Wasser ab 0,5 % in einem Abteil = alle zu, nur beim Auftreten); **neben jeder Tür ein Kippschalter (2 Seiten, in der
  Wand) für genau diese Tür** (v2.0, 10.10.: die 5 Steuerbord-Schalter an der gespiegelten Stelle der Backbord-Schalter
  statt eines Wandblocks; bis v1.0 schaltete der Backbord-Schalter beide Türen der Wand). Beim Laden alle auf. Strom
  Monitor, Türen, Schalter von Batterie (−4,−13,−46). Über dem Chip-Feld (0,13,−52) ist ein Loch in der Decke.
- Monitor-Bild v1.5: links Abteile als Liste (Name nach Sensor-Lage: BUG, VORSCHIFF, MITTE, SEITE BB/SB, MASCHINE;
  „+“ = mit weiteren verbunden) mit Balken und Prozent, darunter TÜREN je Wand (1AUF/1ZU, vom Bug); rechts SPRIT,
  Tank-Balken, VERBR, BATTERIE, PUMPEN; unten rechts Feld „ALLE ZU/AUF“.
- v1.6: Sensor nicht in einem geschlossenen Raum (Loch, offene Luke) misst die Höhe zum Wasser: darunter = **LECK**
  (rot, zählt als voll: Alarm „LECK!“, Schotten zu, Pumpen), darüber = OFFEN (grau). Getrennte Räume einer Seite
  heißen „… BB“/„… SB“. Bestätigt mit Andres C4-Loch im Vorschiff (08.10.).

### 3.9 Ferngesteuerter Jet („small Jet“, Chips „Jet Flug“ v1.0 im Jet + „Figet Marena Jet Steuerung“ v1.0 im Schiff, seit 08.10.)

- **Jet** (`%APPDATA%\Stormworks\data\vehicles\small Jet.xml`, Workshop-Drohne von Ciampi141, alte Chips raus): steht
  senkrecht (Nase +y), 6 Booster für den Start, Strahltriebwerk, 2 Elevons (±6,−6,−21) + Seitenruder, Kamera vorn
  (klein, oben am Heck) und unten (mittel, Zoom), 4 Magnete. Physik-Sensor (0,3,−18) rückwärts und kopfüber: Nick =
  −Kippung lokal z, Querlage = −Kippung lokal x. Chip „Jet Flug“ 4×4 an Andres Platzhalter (−3,−3,−21): Querlage-
  und Nick-Regler (Band/Dämpfung, Ruder × (60 m/s / Tempo)², 0,3–2,5), Elevon-Mischung, Notprogramm nach 1 s ohne
  Lebenszeichen (Flügel gerade, 5° Nick, Gas 0,6), Start-Nick 45° für 3 s nach dem Zünden, Flugdaten zurück.
- **Schiff**: zweiter Sitz (−5,16,−26), Monitor 3×3 (−5,20,−24) mit Kamerabild + Anzeige; Chip an der Decke des
  Chip-Raums (−2,13,−54). Funk Senden (−7,24,−50) auf 7301 (Befehle), Empfang (7,24,−50) auf 7302 (Flugdaten), Video-
  Empfänger (0,24,−44) auf 7301 (Kamera vorn) bzw. 7302 (unten).
- **Bedienung:** Maus (Blick) = Knüppel (rechts/links Querlage, hoch/runter Nick; Totzone 0,1; Hotkey 6 = Blick-Mitte),
  W/S Gas, A/D Seitenruder, Pfeil hoch/runter Zoom, Leertaste Booster (nur mit Triebwerk an), Hotkey 1 Triebwerk,
  2 Licht, 3 Magnete (beim Laden an), 4 Kamera vorn/unten. Anzeige: Horizont, Knüppel-Kreis, kn, m, Kurs, Gas, Sprit,
  Entfernung, KEIN SIGNAL / NOTPROGRAMM / TRIEBWERK AUS. Log „js“ (Port 8768).
- **Ungeprüft:** Ruder-Richtungen („Höhe/Quer/Seite Richtung“), Regler-Werte, ob Video- und Daten-Funk dieselbe
  Frequenz-Zahl teilen dürfen, Bildwinkel-Wert der Kamera.

---

## 4. Chip-Übersicht

| Chip | Version | Größe | Lage (vp) | Aufgabe | Skripte |
|---|---|---|---|---|---|
| Figet Marena Schiffsführung | v3.5 | 6×6 | (0,−12,−41) | Motoren, Gänge, Ruder, Bugstrahl, Helm, Temperatur-Regler, E-Motoren | schiff, shud, wellen |
| Figet Marena Flossen | v1.8 | 3×4 | (0,−5,−44) | 12 Steuerflossen, Heck-Wasser, Batterie weiter | flossen |
| Figet Marena Lage | v3.4 | 4×4 | (−4,9,−59) | 6 Mast-Radare → 5 Ziele in der Welt | 6× mastradar, lage |
| Figet Marena Bildschirm | v3.7 | 4×3 | (1,9,−59) | Monitor 9×5, Zielverteilung, Master Arm, Mehrspieler-Hilfe | mitspieler, bild |
| Figet Marena Waffenwahl | v1.2 | 3×2 | (−4,5,−59) | Monitor 2×3: Waffe wählen | waffenwahl |
| Figet Marena Flak L | v2.8 | 4×5 | (−5,9,−58) | linker Flak-Turm | flakradar, flak |
| Figet Marena Flak R | v2.8 | 4×5 | (5,6,−58) | rechter Flak-Turm | flakradar, flak |
| Figet Marena Kanone BC | v1.6 | 4×7 | (−5,13,−58) | Battle-Cannon-Turm (2 Rohre, Lader) | flakradar, flak |
| Figet Marena Kanone AC | v1.6 | 4×5 | (5,10,−58) | Heavy-Autocannon-Turm vorn | flakradar, flak |
| Figet Marena Kamera | v2.2 | 4×5 | (5,10,−53) | Dachkamera, Zoom, Blick-Korrektur | kamera |
| Figet Marena Schutz | v1.0 | 2×3 | (−5,13,−51) | Auto-Chaff, Lenzpumpen | schutz |
| Figet Marena Jet Steuerung | v1.0 | 4×3 | (−2,13,−54) Decke | Jet fernsteuern: Maus-Knüppel, Funk, Kamerabild Monitor 3×3 | jet_steuerung |
| Figet Marena Schotten | v2.0 | 6×4 | (−2,13,−50) Decke | 5 Schottwände, 10 Türen: alle zu/auf, Kippschalter je Tür | schotten |
| Figet Marena Abteile | v1.6 | 4×8 | (−5,5,−59) | Monitor 9×5: Abteile, Sprit, Batterie, Pumpen; Schotten zu/auf, Lenzpumpen automatisch | abteile |
| Figet Marena Abteile Sammler | v1.1 | 4×5 | (5,2,−58) | Liquid Meter 10–18 gepackt | abteile_sammler |
| Figet Marena Licht | v1.0 | 2×2 | (1,12,−59) | 55 RGB-Lampen, Tag/Nacht, Steuerungsraum rot bei Bedrohung | licht |
| Figet Marena Autopilot | v1.2 | 4×3 | (−4,12,−59) | Kurs/Tempo halten, Karte mit Wegpunkten (Control Handle), Anti-Kollision | autopilot |
| Quarter Panel NO (3×) | – | 1×2 | Maschinenräume | Andres Anzeigen (alt) | – |
| „Microcontroller“ (24×) | – | 3×3 | je Rakete | Raketen (Andre) | – |

Alle Waffen-Chips nutzen denselben Physik-Sensor (0,27,−38). Lua-Grenze im Spiel: 8192 Zeichen je Skript
(Lage-Skript 8119 – fast voll).

---

## 5. Waffensystem

### 5.1 Lagezentrale (Chip „Lage“ v3.4)
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

### 5.2 Hauptbildschirm (Chip „Bildschirm“ v3.7, Monitor 9×5)
- **Mehrspieler-Hilfe (v3.7, 10.10.):** `lua/mitspieler.lua` vor BILD. Beim Host reicht es alles durch. Beim Mitspieler
  (erkannt am springenden Takt der Lage, Bool 21–24) hält es die 5 Ziele aus dem letzten Stand des Hosts bis
  `MP halten s` (10) fest; oben auf dem Radar steht dann „MP <Alter>S“. `Mehrspieler-Hilfe` 0 = aus.
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
  kBr/kBf und kAr/kAf Kanonen, ka Kamera, sc Schutz, sr/srK Seeradar, ap Autopilot (alle 4 Ticks); **ki** = Fahr-KI
  des Landkreuzers (Status-Skript, Spalten in `schreiber_spalten.py`, Auswertung `landkreuzer/tools/ki_log.py`).
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

Seit 09.10. in der allgemeinen Wissensablage, weil sie für jedes Fahrzeug gelten:
Spielregeln (Lua, HTTP, Ticks, Drehung, Spiegeln, Zielhöhen) in `wissen/mechaniken/README.md`, Verhalten einzelner
Bauteile (Laser, Pivot, Kamera, Radar, Battle Cannon, Munition) in `wissen/bauteile/README.md` Abschnitt 3.

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
- **07.10. entfernt:** die 24 Raketen und der Raketen-Chip (funktionierten nicht). Radar 6 und der Monitor 3×3 dienen
  jetzt dem Seeradar; statt Raketen kommt der ferngesteuerte Jet (Abschnitt 3.9). Bis 07.10. galt: Raketen-Chip „Figet Marena Raketen“, seine Kabel, Radar 6, Monitor 3×3,
  Startknopf und die 24 Raketen bei anderen Änderungen unverändert lassen.
- Die Kopie in `fahrzeug/` ist der Stand vom 08.10. 22:40 (ohne Raketen, mit allen Chips; ohne Steam-Autorangaben).

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
- **Werkzeuge:** `build_mc.py` liegt seit 08.10. als Kopie in `tools/` (die Bau-Skripte nehmen bevorzugt die aus
  `stormworks_flugpanzer\tools`, sonst diese). Außerdem gibt es den Nachbau `landkreuzer/tools/build_mc.py` (08.10.):
  Mit ihm bauen die Schiffs-Bauskripte alle Waffen-Chips byte-gleich nach (Prüfung:
  `python landkreuzer/tools/test_build_mc.py`); der Landkreuzer-Bau benutzt ihn.

## 11. Ideen für später

- **Raketenabwehr** (Andre will am 06.10. abends anfangen): nur Rohrwaffen und Täuschung, keine Abfangraketen.
  1. Lage erkennt schnelle kleine Luftziele als „Rakete“, höchster Vorrang für die Flaks (Lage-Skript vorher aufteilen).
  2. evtl. eigener Abwehrturm (z. B. Rotary Autocannon + Radar), Logik aus Flak abgeleitet.
  3. Auto-Chaff auch bei erkannter Rakete. 4. Warnung „RAKETE“ + Richtung auf Hauptbildschirm und Helm.
  Offen: welche Gegner/Raketen, Flaks oder eigener Turm (wo, welche Kanone), Log einer anfliegenden Rakete (Tempo, Höhe).
- **Ferngesteuerte Fahrzeuge** (Drohne/Boot vom Schiff): Sitz → Chip → Radio (Frequenz) → Radio → Chip im Fahrzeug,
  Rückkanal auf zweiter Frequenz. Allein bedienbar nur, wenn das Schiff solange selbst Kurs hält oder stoppt. Grenzen:
  Ferne Fahrzeuge werden nicht simuliert (s. u.). Funk (Wiki/Forum, ungeprüft): Antenne klein ~100 m, mittel ~1 km,
  groß ~4 km, Video ~10–20 km, riesig ~20 km; Reichweite = Sender + Empfänger, mal Batteriestand (riesig+riesig ~40 km).
  Zahlen/An-Aus bis zur Grenze sicher, Ton/Video werden vorher schlechter. Video per Funk geht (Video-Antenne).
  Gegen Anhalten/Verschwinden in der Ferne: Bauteil **„Keep Active Block“** (seit v0.7.1; Karriere: über Blaupause
  „Radio RX“) ins Flugzeug, evtl. auch ins Schiff. Laut Forum: zusammen gespawnte Teile trennen sich ab ca. 1,5–3 km →
  Flugzeug besser getrennt spawnen und an Deck stellen. Kostet Leistung. Ungeprüft – im Spiel 3–5 km wegfliegen und testen.
  Idee Flugzeug (08.10.): Start mit Fahrtwind (60 kn ≈ 30 m/s) oder Senkrechtstarter; Landung als Wasserflugzeug + Kran;
  Schiff braucht Autopilot (Kurs/Tempo halten), Flugzeug Selbststabilisierung + „Zurück zum Schiff“. Nur Aufklärung/Spaß.
