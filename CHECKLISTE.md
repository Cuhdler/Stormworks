# Figet Marena – Antrieb einbauen und Schiff-Chip verkabeln (aktuell Schiff v2.6, 4 Motoren, 8 Gänge, Fahrtenschreiber)

> **Ab v1.0 gibt es keine ZE-Regler mehr** (Abschnitt 6). Abschnitt 2 beschreibt den alten Stand mit ZE und bleibt
> nur zum Nachlesen.

## 1. Maschinenräume (zwei Diesel, je einer pro Welle)

Motor = dein **„Working ship engine“** (18 Zylinder 3×3, Schwungrad, Kupplung 3×3, ZE-Regler), zweimal.

- [ ] **Platz:** hinten zwischen Boden und Zwischendeck, direkt **vor den Wellenenden** (die Wellen enden 28 m vor
      dem Heck). Der Motor ist 13 × 8 × 26 Blöcke (ca. 3,25 × 2 × 6,5 m).
- [ ] **Höhe:** Motor direkt auf den Boden stellen → die Kurbelwelle liegt dann genau auf Wellenhöhe
      (1 m über dem Boden).
- [ ] **Links/rechts:** Kurbelwelle je auf die Linie ihrer Welle, die breitere Motorseite zur Bordwand.
      In der Mitte bleiben ca. 5 Blöcke für eine **Längswand** (ein Treffer legt nur eine Seite lahm).
- [ ] **Antriebsstrang:** Motor → Kupplung 3×3 → Welle → Giant Propeller. Erst mal ohne Getriebe; ob eins nötig ist,
      zeigt die Probefahrt (Drehzahl).
- [ ] **Jede Seite eigenständig:** eigener Tank, eigene Kühlung, Luftfilter oben an Deck, Abgas nach oben
      (Schornstein).
- [ ] **Strom:** je eine Lichtmaschine (Alternator) auf dem Riemen, dazu Batterien (später: Radare, Pumpen,
      Bugstrahlruder, Lader der Autokanonen).
- [ ] **Alte Bedienteile** der Motor-Kopien (Gashebel, Schalter) **nicht** mehr an die ZE-Regler anschließen – das
      macht jetzt der Chip.

## 2. Verkabelung – je Motor (hier links; rechts genauso mit „R“)

**A. Diese Kabel im Motor BLEIBEN (nicht anfassen):**

| von | nach |
|---|---|
| Zylinder 3×3: **Composite Data** | ZE-Chip: **Cylinder** |
| Kurbelwelle 3×3: **RPS** | ZE-Chip: **Crankshaft RPS** |
| ZE-Chip: **Air manifold** | beide Air Manifolds: **Throttle** |
| ZE-Chip: **Fuel manifold** | beide Fuel Manifolds: **Throttle** |
| ZE-Chip: **Starter** | alle 8 Anlasser: **Starter** |
| Batterie: **Electric** | Anlasser, Pumpen, Kühler (Strom) |

ZE-Eingang **Dynamic Stoich or AFR** bleibt leer. (v0.9: ZE `RPS at throttle 1` = 100; ab v1.0 ZE ausgebaut.)

**B. Die zwei Schalter BLEIBEN mit allen Kabeln – nur umstellen:**

- Schalter **„Engine on/off“** und Schalter **„Coolant Pumps“**: mit dem Auswahl-Werkzeug **External Input** von
  „on/off“ auf **„input“** stellen. Ihre Kabel zum ZE-Chip (On/Off) und zu allen Pumpen und Lüftern bleiben.

**C. Nur diese Teile samt Kabel LÖSCHEN:**

- **Gashebel** (Throttle Lever) – sein Kabel ging an ZE **Throttle value or Desired RPS value**
- das Kabel vom Chip **„1x2 switchbox“** zur Kupplung (**Clutch Pressure**). Threshold Gate und switchbox dürfen
  bleiben oder weg, sie werden nicht mehr gebraucht.
- (freiwillig) Anzeigeuhren und Chip „Quarter Panel NO“ dürfen bleiben.

**D. NEUE Kabel vom Schiffs-Chip (6 pro Motor):**

| von | nach |
|---|---|
| Schiffs-Chip: **Motor L Hebel** | ZE-Chip links: **Throttle value or Desired RPS value** (wo der Gashebel war) |
| Schiffs-Chip: **Kupplung L** | Kupplung 3×3 links: **Clutch Pressure** (wo die switchbox war) |
| Schiffs-Chip: **Motor L an** | Schalter „Engine on/off“ links: **External Input** |
| Schiffs-Chip: **Motor L an** | Schalter „Coolant Pumps“ links: **External Input** |
| Kurbelwelle 3×3 links: **RPS** (zusätzliches Kabel, das alte zum ZE bleibt) | Schiffs-Chip: **Motor L RPS** |
| Zylinder 3×3 links: **Composite Data** (zusätzliches Kabel) | Schiffs-Chip: **Motor L Zylinder** |

## 2b. Übrige Kabel am Schiffs-Chip (einmal)

| von | nach |
|---|---|
| Steuersitz (Helm): **Seat data** | Schiffs-Chip: **Sitz** |
| Physics Sensor (neu, Pfeil nach vorn): **Composite Output** | Schiffs-Chip: **Physik-Sensor** |
| Schiffs-Chip: **Ruder** | **beide** Ruder-Gelenke: **Rotation Target** |
| Schiffs-Chip: **Bugstrahlruder** | Elektromotor am Bug: **Throttle** |
| Schiffs-Chip: **Helm** | Steuersitz: **Headset Video** |
| Schiffs-Chip: **Schiffsdaten** | frei lassen |

**Strom:** Physics Sensor, Ruder-Gelenke, Bugstrahl-Motor und Chip brauchen Strom. Der alte Motor hatte keine
Lichtmaschine – mit 24 Pumpen und 12 Lüftern ist die Batterie schnell leer. Je Motor eine **Lichtmaschine
(Alternator)** an den Riemen (Drive Belt 3×3) und an die Batterie.

**Einstellungen am Schiffs-Chip** (Auswahl-Werkzeug): `Hebel als Soll-RPS` = 0 lassen (passt zu deinen ZE-Reglern).
Dreht das Schiff mit **D nach links**: `Ruder Richtung` = -1. Drückt **Pfeil rechts** den Bug nach links:
`Bugstrahl Richtung` = -1.

## 3. Bedienung

| Taste | Wirkung |
|---|---|
| **Hotkey 1** | Motoren an / aus (die ZE-Regler starten selbst) |
| **W / S** | Fahrhebel hoch / runter (bleibt stehen); unter null = rückwärts (bis −50 %) |
| **Hotkey 2** | Stopp: Fahrhebel 0, auskuppeln |
| **A / D** | Ruder |
| **Pfeil links / rechts** | Bugstrahlruder |

Der Chip kuppelt erst ein, wenn ein Motor läuft (3 RPS), und dann sanft über 3 s. Er kuppelt sofort aus, wenn der
Motor über 115 °C kommt (`Motor heiss Grad`) oder 5 s lang steht (Ausfall) – der andere Motor treibt weiter.

**Temperatur-Regler (ab v0.9):** bis `Temp Ziel` (95 °C) volles Gas. Wird ein Motor wärmer, nimmt der Chip bei diesem
Motor nur so viel Gas weg, dass er bei 95 °C bleibt, und gibt es beim Abkühlen wieder frei (`Temp Regel` = wie schnell).
Im Helm steht dann **GAS xx %** und gelb **TEMP**.

**Im Helm:** Motoren an/aus, Fahrhebel, Tempo (km/h und Knoten), Kurs, Ruder, Bugstrahl, je Motor Drehzahl,
Temperatur, Kupplung, Gas-Grenze und Zustand (OK / TEMP / HEISS / AUSFALL).

## 4. Probefahrt – bitte notieren

- Höchsttempo (TEMPO im Helm) bei Fahrhebel 100 %
- Drehzahl (RPS) und Temperatur beider Motoren bei Volllast
- Liegt das Schiff gerade im Wasser (vorn/hinten)? Hebt sich der Bug bei Fahrt?
- Dreht es sauber mit A/D?

## 5. Getriebe (ab Chip v0.9): nur noch Rückwärtsgang, sonst direkter Antrieb

Messung 27.09.: ZE auf 100, direkt (1:1) = **151 km/h** bei 51 RPS und 33 °C. Der Motor bringt mit mehr Drehzahl viel mehr
Kraft; die Übersetzung ins Schnelle hat die Drehzahl nur gedrückt, und jedes Getriebe kostet 5 % (10 in Reihe ≈ 40 %).

**Je Seite (seit 27.09. so in der Datei):** nur das **Getriebe am Motor** (z = −99) bleibt: Ratio Off **1:1**, Ratio On
**−1:1** (rückwärts). Die anderen 9 Getriebe je Seite sind **gerade Wellen**.

| Chip-Anschluss | Getriebe |
|---|---|
| **Rueckwaerts L** (früher „L 6:5 1er“) | links Getriebe 1 (am Motor): Gear Switch |
| **Rueckwaerts R** (früher „R 6:5 1er“) | rechts Getriebe 1 (am Motor): Gear Switch |
| **frei 5 … frei 10** | nichts |

**Rückwärts:** S zieht den Fahrhebel unter null. Beim Nulldurchgang kuppelt der Chip aus, legt den Rückwärtsgang ein und
kuppelt sanft wieder ein. Im Helm: `HEBEL 30% RUECK`.

**Später ausprobieren:** Ratio Off am Getriebe 1 auf 6:5 stellen und Höchsttempo mit 1:1 vergleichen.

## 6. Motorsteuerung ohne ZE-Regler (ab v1.0, am 27.09. von Claude in der Datei umgebaut)

Beide ZE-Regler sind ausgebaut; der Schiffs-Chip macht Gemisch, Anlasser und Leerlauf selbst. Sicherung vorher:
`backup/Figet Marena vor ZE-Ausbau.xml`. Umbau-Skript: `tools/umbau_v1.py`.

| Chip-Anschluss | geht an (je Motor) |
|---|---|
| **Luft L / R** (früher „Motor L/R Hebel“) | beide Air Manifolds: Throttle |
| **Treibstoff L / R** | beide Fuel Manifolds: Throttle |
| **Anlasser L / R** | alle 8 Anlasser: Starter |
| **Motor L / R Zylinder** | liest jetzt Luft, Treibstoff und Temperatur |

- **Fahrhebel = Leistung** (Anteil der vollen Treibstoffmenge), keine Drehzahl-Grenze im Betrieb.
- **Grenze ist die Temperatur:** bis `Temp Ziel` (95 °C) volles Gas, darüber nimmt der Chip so viel weg, dass sie dort
  bleibt. Über `Motor heiss Grad` (115 °C) kuppelt er aus. Schaden laut Community ab ca. 120 °C.
- Ausgekuppelt hält er `Leerlauf RPS` (4). `RPS Notgrenze` (120) greift nur, wenn die Schraube aus dem Wasser kommt.
- `Gemisch` = Stöchiometrie wie am Zylinder angezeigt: 0.5 kräftig (wie vorher beim ZE), 0.2 sparsam.
- Anlasser (ab v1.1): dreht sofort nach Hotkey 1, bis der Motor 0.5 s über 3 RPS läuft; höchstens 8 s, dann 2 s
  Pause und neu. Nach Abwürgen startet er selbst neu. Treibstoff gibt es schon beim Anlassen (v1.0 erst ab 2 RPS -
  der Anlasser schafft nur 1.5–2.3 RPS, deshalb sprang v1.0 nicht an).
- Gemisch (ab v1.1): Treibstoff = Luft × Q / Luftverhältnis, Q startet mit 6.88 (Community-Formel) und wird langsam aus
  den Zylinder-Werten gelernt. v1.0 rechnete jeden Tick neu aus den Messwerten und war beim Anlassen viel zu mager.
- Chip neu einsetzen ohne Umbau: `tools/build_schiff.py --install`, dann `tools/chip_einsetzen.py --schreiben`.
- Im Helm je Motor: `RPS`, `T`, `K` (Kupplung), `GAS` (Anteil von voll), `MIX` (gemessene Stöchiometrie), Zustand.

## 7. Vier Motoren – Schiff v2.1 (am 27.09. abends von Claude verkabelt)

Die zweiten Motoren sitzen 8 Blöcke über den ersten: **L1/R1 unten** (y −16), **L2/R2 oben** (y −8). Ein Schiffs-Chip
(6×6, gleiche Stelle, eine Spalte mehr nach unten) steuert alle vier; Motor-Chips pro Motor (v2.0-Idee) sind
verworfen. Sicherung vorher: `backup/Figet Marena vor Kabel v2.1.xml`, Skript `tools/kabel_v21.py`.

**Von Claude gelegt (198 Kabel, Kopie der L1/R1-Kabel, 8 Blöcke höher):**
- Chip → L2/R2: Luft (2 Air Manifolds), Treibstoff (2 Fuel Manifolds), Anlasser (8), Kupplung; Kurbelwelle RPS und
  Zylinder-Composite → Chip
- „Motor L/R an“ → alle 24 Pumpen und 12 Kühler-Lüfter je oberem Motor
- Strom von den beiden Batterien → Anlasser, Pumpen, Kühler, Transponder der oberen Motoren

**Macht Andre selbst:** Welle der oberen Motoren zur Schraubenwelle (hinter deren Kupplungen), Treibstoff- und
Kühlwasser-Leitungen der oberen Motoren, Getriebe am Motor „Ratio On“ = 1:-1.

**Achtung Strom:** 2 mittlere Batterien versorgen jetzt 32 Anlasser, 96 Pumpen, 48 Kühler. Die zwei kleinen
Lichtmaschinen sitzen auf der Schraubenwelle – sie laden nur, wenn die Schraube dreht (nicht im Leerlauf mit offener
Kupplung). Werden Anlassen oder Pumpen schwach: mehr/größere Batterien oder Lichtmaschinen an die Motoren.

**Helm:** je Motor `L1/L2/R1/R2 RPS … T … GAS …% MIX … ` + Zustand OK / LEER / KUPPELT / TEMP / HEISS / AUSFALL / ---.
Lenk-Schub, Ruder-Tempo, Rückwärtsgang je Seite wie in v2.0 (Rückwärts schaltet erst, wenn beide Kupplungen der
Seite offen sind).

**Getriebe ins Schnelle (Pfeil zum Motor) – messen statt raten:** gleiches Tempo fahren, GAS % und Temperatur notieren –
einmal 1:1, einmal mit Übersetzung (6:5, dann 3:2).

## 8. Schiff v2.2 – Gemisch-Regelung (28.09.)

Mit 4 Motoren stand MIX weit daneben (L1 2.24 fett, L2/R1/R2 um −1 mager) → nur 54 km/h. Ursache im Chip: er lernte das
Luft/Treibstoff-Verhältnis nur im Bereich 3–15 und verwarf alles andere. v2.2 regelt direkt auf den gemessenen MIX
(zu fett → weniger Treibstoff je Luft, zu mager → mehr), Bereich 1–60, höchstens 2 % je Tick. Im Rechner geprüft für
Verhältnisse 2 bis 20: alle regeln auf MIX 0.50.

**Einbau:** Schiffs-Chip im Spiel mit „Figet Marena Schiff v2.2“ überschreiben – Anschlüsse identisch mit v2.1, alle
Kabel bleiben (Eigenschaften danach auf Standard).

**Hotkey 4 – Diagnose-Seite im Helm:** je Motor `Q` (Treibstoff je Luft, nachgeregelt; normal um 6.9), `LUFT %`,
`TREIB %`, `MIX`. Steht TREIB bei 100 % und LUFT deutlich darunter, bekommt der Motor zu wenig Treibstoff; steht LUFT
bei 100 % und TREIB niedrig, zu wenig Luft. Nochmal Hotkey 4 = zurück.

## 9. Schiff v2.3 – 8 Gänge aus 3 Getrieben (in der Bibliothek seit 01.10., getestet im Schiffsmodell)

Idee (Andre, 28.09.): Drehmoment ist genug da, die Drehzahl begrenzt die Hitze → mit Getrieben ins Schnelle
übersetzen; möglichst wenige Getriebe, die in Kombination viele Gänge ergeben.

- [ ] **Je Seite 3 Getriebe 1x1** auf die Welle (Reihenfolge egal, jedes mit Strom), Pfeil zum Motor, *Ratio Off* 1:1:

| Getriebe | Ratio On | Chip-Anschluss (an beide Seiten) |
|---|---|---|
| A | 6:5 | **Getriebe A** |
| B | 3:2 | **Getriebe B** |
| C | 2:1 | **Getriebe C** |

  Zusammen 8 Gänge: ×1.0, 1.2, 1.5, 1.8, 2.0, 2.4, 3.0, 3.6.
- [ ] **Rückwärts-Getriebe z = −99 (beide Seiten): *Ratio On* auf 1:−1 stellen.** Im gespeicherten Stand (28.09.)
      stehen beide auf „On“ 1:1 (`gear_ratio_2="0"`) – damit fährt der Rückwärtsgang vorwärts.
- **Stand 01.10. abends:** Andre baute je Seite 4 Getriebe (z −98 = 6:5 A, −99 = 3:2 B, −100 = C (Ratio nie umgestellt –
      im Editor auf 2:1 prüfen!), −101 = 1:−1 Rückwärts), Chip v2.3 liegt im Schiff. Claude legte die 8 Gear-Switch-Kabel
      (tools/kabel_v23.py, Sicherung `backup/Figet Marena vor Getriebekabeln v2.3.xml`). gear_ratio_2-Index:
      0 = 1:−1, 1 = 1:1, 2 = 6:5, 3 = 3:2.
- [x] **Chip tauschen:** v2.3 über den eingebauten Schiffs-Chip legen – alle Kabel bleiben (gleiche Anschluss-Lage).
      Neu sind nur die 3 Ausgänge Getriebe A/B/C (A auf dem früheren Platz „Schiffsdaten“, der nie verbunden war).
      Die 6 Gear-Switch-Kabel kann Claude per Datei legen, wenn die Getriebe stehen.
- **Bedienung:** Automatik (Standard): über `Hoch ab RPS` (22) hoch, aber nur, wenn der Motor danach noch über
  `Runter unter RPS` × 1.1 liegt; unter `Runter unter RPS` (15) runter; `Schaltzeit s` (1) warten, nach dem Schalten
  doppelt so lange. Rückwärts und Hebel 0 = Gang 1. **Hotkey 3** = Hand/Automatik, von Hand **Pfeil hoch/runter**.
  Helm oben: `MOTOREN AN  GANG 3 X1.5 AUTO`.
- **Einstellen:** von Hand Gang für Gang Vollgas fahren, Tempo (kn) und Temperatur notieren → die zwei RPS-Grenzen so
  setzen, dass die Automatik im schnellsten Gang landet.
- Modell-Test (tools/test_schiff.py, test_gaenge): Hand 1–8 in der richtigen Reihenfolge, Automatik schaltet bei
  Vollgas Gang für Gang hoch ohne Pendeln, bei 30 % Hebel runter und bleibt ruhig, rückwärts sofort Gang 1.

## 10. Schiff v2.4 – Fahrtenschreiber (01.10. abends, von Claude ins Schiff gesetzt)

Wie der Flugschreiber im Heli: die Helm-Anzeige (shud.lua) schickt jeden Tick eine Zeile (alle 32 Ausgänge des
Schiffs-Skripts + 11 Schalter, roh) per HTTP an **tools/logger.py** auf dem PC (Port 8766, Chip-Eigenschaft `Log Port`,
0 = aus). Das Programm entpackt sie und schreibt `logs/fahrt_<Datum>_<Zeit>.csv`: Tempo (kn, km/h), Kurs, Hebel, Gang,
Übersetzung, Automatik, Ruder, Bug, Motoren an, Rückwärts L/R, Getriebe A/B/C, je Motor RPS, Temperatur, Zustand,
Gas %, MIX, Q, Luft %, Treibstoff-Drossel, Kupplung, Anlasser.
- Starten: `python tools/logger.py` (Claude startet es meist selbst im Hintergrund). Helm unten: `LOG OK n` = läuft;
  `LOG: PC-PROGRAMM AUS?` = keine Antwort.
- Anschlüsse unverändert (nur die Chip-Definition getauscht, Sicherung `backup/Figet Marena vor Chip v2.4.xml`).
- Test: tools/test_schiff.py test_schreiber (2400 Zeilen in 40 s lückenlos, Werte = Chip-Ausgang, ohne PC alle 2 s
  neuer Versuch).

## 11. Schiff v2.5 – Ruder 4× weiter, ruhigerer Gemisch-Regler (02.10., von Claude ins Schiff gesetzt)

Auswertung Fahrtenschreiber 01.10. 21:49 und 02.10. 12:37:
- **Ruder:** Signal 1 = 90° am Robotic Pivot, 45° am Ruder-Bauteil (`rudder`). `Ruder max` 0.125 hieß nur 11° bzw.
  5.6° (meine alte Beschreibung „45°“ war falsch) → jetzt **0.5** (45° bzw. 22.5°), `Ruder Tempo` 1 (0.5 s bis voll).
  Andre baute je Seite ein zweites Ruder (Bauteil `rudder` z −148) + kleine E-Motoren an die Power-Pivots.
- **Gang 4:** Tempo pendelt 32–53 kn, Gemisch −1.3 … 3.3, Q schwankt ±22 % im Takt → Regler zu schnell (1 %/Tick).
  Jetzt höchstens 0.2 %/Tick. Bleibt das Pendeln, zeigt der Schreiber ein festes Q → dann liegt es am Motor.
- **Gang 6:** 70–72 kn, 18–20 RPS, Gemisch ruhig (außer L1, pendelt −0.4 … 1.5). Temperatur steigt stetig
  (R1 41 → 82 °C in 150 s) → bei langer Fahrt greift der Temperatur-Regler (95 °C).
- **Gang 7/8** liefen nur, als das Schiff bei 72 kn auf eine Insel fuhr (Schrauben frei, 31–35 RPS) – keine
  gültigen Werte. Danach drehte es sich um ~60° und stand. Die 95.6 kn waren Aufprall-Werte.
- Nächster Test: auf ruhigem Wasser von Hand Gang 6, 7, 8 je ~30 s Vollgas (Tempo, RPS, Temperatur).

## 12. Schiff v2.6 – Manövrieren (02.10. nachmittags, von Claude ins Schiff gesetzt)

Fahrt 02.10. 16:14 (Wellen-Test): Gang 4 jetzt ruhig 46–50 kn (Regler v2.5 wirkt). Kurve bei 50–60 kn mit bis 98 % Ruder:
nur ~1 Grad/s; 29 % weniger Gas rechts änderte die Drehzahl nicht (17.7 zu 17.9 RPS). Wellen: Schrauben frei bis 40 RPS →
Automatik schaltete 6 → 7 → 8, danach Motoren 7–12 RPS, Tempo bis 12 kn eingebrochen. Bugstrahl lief nie (nur Pfeiltasten).
- **Bugstrahlruder lenkt mit A/D mit** (`Bugstrahl beim Lenken` 1; 0 = nur Pfeile). Motor_medium im Bug (0,−12,41).
- **Lenk-Schub 0.6** (kurveninnere Seite 40 % Gas).
- **Automatik:** hoch nur, wenn das Tempo während der Wartezeit nicht fällt (frei drehende Schrauben in Wellen). Modell:
  v2.5 schaltete in Wellen 6 → 8, v2.6 bleibt in 6.
- schiff.lua jetzt mit drop_local gekürzt (4036/4096). Sicherung vorher: `backup/Figet Marena vor Chip v2.6.xml`.
- Nächster Test Manövrieren: je ~10 s volles Ruder bei ~10, ~30 und ~60 kn, dazu Wenden aus dem Stand.

## 13. Steuerflossen – Chip „Figet Marena Flossen v1“ (02.10. abends, von Claude eingesetzt und verkabelt)

Andre setzte 10 Control Fin Medium (waagerecht seitlich, Profil längs): vorn (±1,−21,25/28) am Kiel, hinten
(±10,−16,−120/−134), Mitte hinten (±9,−21,−92); dazu einen leeren Microcontroller bei (0,−5,−44) als Platz.
- Der Microcontroller ist jetzt der Flossen-Chip (3×3, sc 30): Physik-Sensor (0,27,−38) als zweites Kabel; Ausgänge
  vorn L/R, hinten L/R, Mitte L/R → je Flosse „Rotation“ (Anschluss Flossenmitte + 1 in z); Strom je Flosse von der
  Batterie ihrer Seite (±8,−18,−64). Linkes Ruder-Bauteil (neu gesetzt) wieder am Chip-Ausgang „Ruder“.
- Regel: Nase zu hoch → vorn ab, hinten auf; Seite zu tief → dort auf, gegenüber ab; Steigen (Welle) → alle ab; dazu
  Dämpfung der Drehraten. Kraft ~ Tempo², daher Verstärkung (60 kn / Tempo)², höchstens 4; unter 6 kn gerade.
- **Wichtig beim ersten Test:** Annahme „+ = Vorderkante hoch = Auftrieb nach oben“. Nickt/rollt das Schiff mit
  Flossen stärker statt ruhiger → Chip-Eigenschaft **Flossen Richtung = −1**. Aus: **Flossen an = 0**.
- Modell (tools/test_flossen.py, geschätzte Rumpfwerte): ab 25 kn Nicken in Wellen −55…−80 %, Rollen −40…−60 %;
  falsch gepolt deutlich schlimmer; 10 kn kaum Wirkung (zu wenig Strömung).
- Flossen-Schreiber: Port 8767 → logs/flossen_*.csv (Tempo, Nick, Roll, Raten, Steigen, Verstärkung, 6 Ausschläge).
- Sicherung vorher: `backup/Figet Marena vor Flossen v1.xml`. Werkzeuge: build_flossen.py, kabel_flossen.py.
- **v1.1 (02.10.):** Andre: die 3 hinteren linken Flossen drückten das Heck hoch statt runter. Daten bestätigen es
  (bei 50 kn blieb 1.5–2° Schräglage links, obwohl links „hoch“ befohlen war). Ursache: links normal gesetzt, rechts
  gespiegelt – das Spiel dreht dabei die Wirkrichtung um. Neue Eigenschaften **Richtung links −1** (alle linken, auch
  die vorderen, gleiche Einbaulage) und **Richtung rechts 1**. Sicherung: `backup/Figet Marena vor Flossen v1.1.xml`.
- **v1.2 (02.10.):** v1.1 war schlimmer (bis 26° Schlagseite links, Nicken −11…+6°, 65–68 % am Anschlag, obwohl der Chip
  richtig befahl) → in v1.1 arbeiteten ALLE Flossen verkehrt. Beide Fahrten passen nur zu: **links (normal) + = Vorderkante
  hoch, rechts (gespiegelt) umgekehrt** (Modell bildet v1 und v1.1 so nach). Jetzt **Richtung links 1, rechts −1**.
  Andres Beobachtung „hintere linke drücken das Heck hoch“ war vermutlich der Roll-Ausgleich (links tief → links hoch).
  Neu: **Flossen Test** = 1 → im Stand alle Flossen auf Vorderkante hoch (nachsehen, ob alle 10 gleich stehen; dann 0);
  **Roll vorn Anteil 0** (vordere nur Nick/Hub, Andre); **Nick I / Roll I** 0.03 gegen dauernde Schlagseite/Trimm
  (bei 25–40 kn reicht die Flossenkraft nur teilweise). Sicherung: `backup/Figet Marena vor Flossen v1.2.xml`.
- **v1.3 (02.10.):** Test-Chip (alle 6 Ausgänge +0.7, `kabel_flossen.py --test`): bei **allen** Flossen zeigt die
  Vorderkante nach oben, auch rechts (gespiegelt). Also **+ = Vorderkante hoch überall → Richtung links 1, rechts 1**
  (wie v1). Meine Deutung der Fahrtdaten für v1.1/v1.2 war falsch: die Daten passten zu beiden Erklärungen, erst der
  Sichttest war eindeutig. Was in v1 blieb (Schlagseite ~−1.3°, Nase +0.5°), war der fehlende I-Anteil – jetzt drin.
  v1.3 = v1.2 mit beiden Richtungen 1. Sicherung: `backup/Figet Marena vor Flossen v1.3.xml`.
- **v1.4 (02.10. abends):** Fahrt 17:18 mit v1.3: gerade Strecke ±2.5° Roll; lange Linkskurve (Ruder −100 %, ~4.5 °/s – das
  Lenken geht jetzt!) mit 13–20° Krängung, der I-Anteil lud sich auf und übersteuerte danach; am Ende Wellen-Springen.
  Modell mit Wellenschlag (Bug hochgeworfen, Flossen 0.25 s verzögert): v1.3 hebelte das Heck bis 1.4 m hoch (schlimmer
  als ohne Flossen 0.8 m), weil die vorderen den Bug runterdrückten. v1.4: Heck zuerst (Andre: Schrauben im Wasser) –
  Heck-Steigen aus Steigen und Nicken (22 m hinter dem Sensor), 0.3 s Vorhalt, „Heck runter“ 0.5 / „Heck hoch“ 0.1,
  vordere nur „Vorn Nick Anteil“ 0.5, I-Anteil ruht über 3° → Heck im Wellenschlag höchstens 0.25 m. Die zwei hintersten
  Flossen sind jetzt Control Fin Large (Andre), 4 Kabel neu. Sicherung: `backup/Figet Marena vor Flossen v1.4.xml`.
- **v1.5 (02.10. abends):** Fahrt 17:40: 21× Schrauben frei, meist während das Heck sogar sank und das Schiff gerade lag
  → das Wasser zieht unter dem Heck weg (Andre); der Chip sah das nicht. Die hinteren Flossen arbeiteten 38 % der Zeit
  gegen das Rollen und hoben dabei eine Schraube an. Andre setzte 2 Control Fin Large vorn-Mitte (±9,−21,−2).
  v1.5: Chip 3×4 (sc 38): neue Ausgänge **vorn-Mitte L/R** (übernehmen das Rollen, „Roll vorn-Mitte Anteil“ 1,
  „Nick vorn-Mitte Anteil“ 0.3), hinten nur noch „Roll hinten Anteil“ 0.5; neuer Eingang **Heck-Wasser** (Feld 0,3):
  Liquid Meter am Heck → Tiefe der Schraube, normale Tiefe gelernt; läuft sie (mit Vorhalt) flacher als normal
  („Wasser Spiel m“ 0) oder als 1 m → hinten/Mitte drücken das Heck runter („Wasser Druck“ 1.5 je m). Modell: Wasser
  zieht 1.6 m weg, 45 kn: flachste Schraube 0.40 → 0.86 m. Ohne Messer liest der Eingang 0 und wird nicht genutzt.
  **Noch zu bauen (Andre):** 1 Liquid Meter außen am Heck auf Höhe der Schraubenwellen, **nicht kopfüber** (beim Heli
  meldete ein kopfüber gesetzter Messer knapp über dem Wasser das falsche Vorzeichen); kabel_flossen.py verbindet ihn.
  Flossen-Schreiber jetzt 17 Werte (vorn-Mitte, heck_wasser). Sicherung: `backup/Figet Marena vor Flossen v1.5.xml`.
- Heck-Wasser verbunden (02.10. 18:05): Andres Liquid Meter (0,−16,−129) (Schraubenwellen-Höhe, 2 m vor den Schrauben,
  liegend eingebaut – nicht kopfüber) → Flossen-Chip „Heck-Wasser“ (0,−5,−41). Sicherung `backup/Figet Marena vor
  Heck-Wasser-Kabel.xml`. Prüfen im Flossen-Schreiber: heck_wasser in Fahrt negativ (ca. −2 m = Tiefe); positive große
  Zahlen hieße „misst Liter in einem Raum“ → Messer muss außen am Rumpf sitzen.

