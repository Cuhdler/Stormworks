# KI-Landkreuzer – ein Panzer, der selbst fährt und kämpft

**Stand:** 09.10.2026 früh, Version v1.0, gebaut von Claude in der Nacht, **noch nie im Spiel gewesen**.
**Dateien:** `landkreuzer/fahrzeug/KI Landkreuzer.xml` und `KI Landkreuzer Lenkung.xml` (zwei Varianten, siehe
Abschnitt 2). Beide sind fertig, nur die Räder fehlen.
**Bilder:** `landkreuzer/bilder/beschriftet.png` (was wo ist), `schraeg.png` und `schraeg_links.png` (schräg von
vorn), `schraeg_lenkung.png` (Lenk-Variante), `ansicht.png` (oben, rechts, vorn), `rad_stummel.png` (wo das Rad hin
muss), `vorschau_raeder.png` und `vorschau_raeder_lenkung.png` (so etwa sieht er mit Rädern aus – die Räder
sind dort nur gemalt). Alle Bilder zeigen ihn so, wie man ihn im Spiel sieht (nicht gespiegelt).

Andres Wunsch (08.10.): „eine Art Landkreuzer, groß, mit allen möglichen Geschützen, und er soll komplett autonom
fahren – quasi ein KI-Panzer“.

---

## Schnellstart (die ersten 15 Minuten)

1. Auf dem PC pullen. `landkreuzer/fahrzeug/KI Landkreuzer.xml` nach `%APPDATA%\Stormworks\data\vehicles\` kopieren.
   Spawnen nur an einer großen **Land**-Werkbank (z. B. großer Hangar der Kreativ-Insel), nicht am Schiffs-Dock.
2. Im Editor laden, **ein** Rad an den pinken Stummel links vorn setzen (Bild `bilder/rad_stummel.png`), speichern.
   Große Räder nehmen (bis 12 Blöcke), dann hat er mehr Bodenfreiheit.
3. `python landkreuzer/tools/raeder.py --schreiben` (kopiert das Rad an alle 14 Wellen), im Spiel neu laden
   **ohne** zu speichern.
4. Die Schalter stehen beim Spawnen immer auf „aus“ (= die KI darf). Für den ersten Test darum vorher im Editor
   den KI-Chip anklicken und bei den Eigenschaften **„Start Verzoegerung s“ = 600** und **„Waffen Verzoegerung s“
   = 600** eintragen (10 Minuten Ruhe), speichern, spawnen. Dann in der Brücke im Instrumentenblock **„Waffen
   sperren“ an** und **„KI Pause“ an**. (Ohne diese Änderung fährt er nach 30 s los, schießt nach 60 s.)
5. Hinsetzen, W/A/S/D: fährt und lenkt er? Status-Monitor rechts vom Sitz: stehen bei allen 7 Lasern Zahlen
   (nicht „--“)?
6. „KI Pause“ aus: Er fährt allein (Revier 400 m um den Startpunkt). Auf die Karte links vom Sitz tippen = Wegpunkt.
7. Erst wenn das klappt: „Waffen sperren“ aus. Achtung: Er schießt auf alles außerhalb der Schutzzone (300 m um
   den Startpunkt).

Was nicht klappt, bitte aufschreiben (am besten mit der Anzeige des Status-Monitors). Abschnitt 4 sagt, welche
Eigenschaft man im KI-Chip umstellt, wenn z. B. eine Seite falsch herum dreht.

**Fahrtenschreiber (sehr hilfreich für mich):** Im KI-Chip die Eigenschaft „Schreiber Port“ auf **8768** stellen
(oder den Panzer mit `python landkreuzer/tools/bau_landkreuzer.py --schreiber` bauen, dann schreiben auch die
Waffen-Chips mit). Auf dem PC `python tools/waffen_logger.py` starten (wie beim Schiff). **Nur mit laufendem
Logger einschalten**: Anfragen an einen Port ohne Lauscher blockieren die HTTP-Warteschlange des Spiels (siehe
Schiffs-Übersicht). Dann landet jede Fahrt in `logs/waffen_<Datum>_<Zeit>/ki.csv`: je Tick Zustand, Ort, Kurs,
Tempo, Befehle, alle Laser, Batterie, Nick/Roll.
Mit `git add -f logs/...` hochladen – dann sehe ich genau, was die KI gesehen und entschieden hat. Selbst
anschauen: `python landkreuzer/tools/ki_log.py logs/waffen_<Datum>_<Zeit>` (Zusammenfassung und Bild der Fahrspur).
Das Werkzeug prüft dabei auch selbst die **Vorzeichen**: Passt der Kompass zur Fahrspur? Hebt sich der Bug beim
Bergauffahren (Nick)? Dreht er bei „rechts“ wirklich rechtsherum (sonst sind die Motor-Kabel links/rechts vertauscht)?
Es sagt dann, welche Eigenschaft im KI-Chip umzustellen ist.

---

## Was in der Nacht noch dazukam (nachdem du ins Bett bist)

Gefundene **Fehler**, die im Spiel Ärger gemacht hätten (alle behoben und mit Prüfungen abgesichert):
- **Laser einschalten:** Die Turm-Kamera des Schiffs braucht für ihren Laser ein „Laser an“-Signal. Die Laser des
  Panzers bekommen jetzt so ein Kabel vom KI-Chip. Und: Meldet ein wichtiger Laser 0, fährt die KI nicht los
  (Zustand LASER?) – vorher hätte sie das als „frei“ gelesen und wäre blind gefahren.
- **KI-Status-Monitor** wäre dunkel geblieben: Auf dem Schiff schaltete ihn der Waffenwahl-Chip ein. Jetzt der KI-Chip.
- **Roll-Vorzeichen** war in der Fahr-KI andersherum als bei den Flossen deines Schiffs (die im Spiel funktionieren).
- **Composite-Kanal 33** (gibt es nicht, nur 1–32) – hätte den KI-Chip im Spiel kaputt machen können.
- **Status zeigte immer Tempo 0**, der rechte Motor-Balken war beim Vorwärtsfahren rot.
- **Wegrollen am Hang:** Elektromotoren ohne Gas bremsen nicht. Im Kampf rollte er am 10°-Hang in 30 s 16 m zurück;
  jetzt hält er die Stelle.
- **Bug:** Die Spitze lag unten am Boden, 3 m vor den Vorderrädern – an Hängen ab ~10° hätte er aufgesetzt. Jetzt Keil
  (oben und unten 45°), Heck unten abgeschrägt.
- Bilder von rechts waren spiegelverkehrt.

**Neu:**
- **Schutzzone** 300 m um den Startpunkt und **Freund-Punkte** auf der Karte (Finger 1,5 s halten): Ziele dort
  beschießt er nicht.
- Auto-Chaff nur, wenn die Radare auch einen Gegner sehen.
- Laser- und Sensor-Höhe stellt die KI selbst auf die Radgröße ein.
- Nach Hause schon bei 40 % Batterie; der Status zeigt die **Restzeit** der Batterie.
- **Fahrtenschreiber** im KI-Chip (wie in den Waffen-Chips, Standard aus), siehe Schnellstart.
- Er fährt erst 30 s nach dem Spawnen los (vorher 10 s – zu kurz, um in die Brücke zu kommen).
- Ladestand kommt von einer zusätzlichen kleinen Batterie (sichere Anschluss-Lage), siehe Technik.
- Karte: „H“ am Heimatpunkt; Werkzeug `ki_log.py` wertet Fahrtenschreiber-Logs aus.
- Status zeigt Nick/Roll/Kurs in Grad (Vorzeichen prüfen) und rot L!/R!, wenn eine Radseite falsch herum dreht.
- Prüfstände: Wald, Damm durch einen See, enges Tal, holpriger Boden, größere Räder, Stehen am Hang, Lenk-Variante;
  Kabel-Vergleich Schiff ↔ Panzer.
- **Zuverlässigkeit im Simulator (Endstand):** 12 zufällige Welten mit Hügel, See, Klippe, Felsen, Häusern, je
  10 Minuten Patrouille: 12 von 12 fehlerfrei – zusammen 2 Stunden, rund 39 km, nie im Wasser, nie abgestürzt,
  2 leichte Stöße. Nach den Korrekturen aus der Durchsicht nochmal gerechnet: wieder 12 von 12, 39,6 km, 4 leichte
  Stöße.
- **Lenk-Variante:** Beim Rückwärtsfahren schlugen die Achsen falsch herum ein (Lenkung und Kettenlenkung arbeiteten
  gegeneinander). Behoben; im Simulator jetzt geprüft.
- **Durchsicht der KI-Skripte** (ein Helfer las alles gegen, jeder Fund im Simulator nachgestellt, jetzt mit Prüfung):
  - Die **Heimat** sprang bei jedem „KI Pause aus“ an die aktuelle Stelle. Die Schutzzone blieb aber am Spawn-Ort –
    die Karte zeigte den roten Kreis also an der falschen Stelle, und „Nach Hause“ fuhr nicht zum Spawn-Ort. Jetzt ist
    die Heimat überall der Spawn-Ort.
  - Letzter Wegpunkt unerreichbar (z. B. im See) und Revier aus: Er fing wieder bei Wegpunkt 1 an und fuhr endlos hin
    und her. Jetzt bleibt er stehen.
  - Nach Handbetrieb mitten im Zurücksetzen machte die KI das alte Manöver weiter und merkte sich eine „Sackgasse“
    mit 150 m Radius. Jetzt bricht W/S/A/D das Manöver ab.
  - Der Bug-Laser lernte bei jedem Stehen mit KI Pause weiter (über einer Mulde falsch). Jetzt nur in den ersten 10 s.
  - Lenk-Variante: Beim Drehen auf der Stelle schlugen die Achsen meist falsch herum ein (kleiner negativer Fahrbefehl
    des Halte-Reglers galt als „rückwärts“). Jetzt zählt das Soll-Tempo; im Simulator so auch schneller um die Wand
    (74 statt 79 s).
- **Fahrtenschreiber-Auswertung** (`ki_log.py`) prüft aus der Fahrspur die Vorzeichen von Kompass, Nick und
  Drehrichtung und sagt, was umzustellen ist (im Prüfstand mit absichtlich falschen Vorzeichen geprüft).
- **Karte:** zeigt jetzt die **Fahrspur** (blasse Punkte alle 10 m, die letzten 600 m) – man sieht, wo er war.
- **Räder-Werkzeug:** Zweimal `raeder.py --schreiben` hätte jedes Rad doppelt gesetzt (zwei Räder im selben Platz)
  und die Sicherung überschrieben. Jetzt bleiben Wellen mit Rad unberührt; Räder aus mehreren Teilen gehen auch;
  eigene Sicherung je Datei; `--lenkung` für die Lenk-Variante. Neuer Prüfstand `test_raeder.py`.
- Bilder `vorschau_raeder.png` / `vorschau_raeder_lenkung.png`: so etwa sieht er mit 11er-Rädern aus.
- Aussehen: Schlamm unten, Lüftungsgitter, Abzeichen; Bild `beschriftet.png` (was wo ist), `anzeigen.png` (Monitore).

Ausprobiert und **verworfen**: zwei zusätzliche Eck-Laser für dichten Wald (im Simulator schlechter). Ein
Diesel-Generator aus Schiffsteilen geht nicht sicher (im Schiff fehlen Kraftstoff-Teile, Kühlung mit Seewasser).

---

## 1. Was er ist

| | |
|---|---|
| Größe | Rumpf 27 m lang, mit AC-Rohr 29 m; 7,75 m breit + Räder ≈ 9–10 m; Mast ≈ 9 m über dem Boden des Rumpfs |
| Teile | ca. 17 000 (ein Drittel der Figet Marena mit ≈ 56 000), 25 Körper, ca. 420 Kabel, 9 Chips |
| Waffen | vorn **Heavy-Autocannon-Turm** (AP), dahinter erhöht **Battle-Cannon-Turm mit 2 Rohren** (HE), hinten **2 Flak-Türme** mit je 2 Heavy Autocannons (Splitter, Zeitzünder) |
| Schutz | **Auto-Chaff**: 8 Werfer-Ketten mit je 15 Werfern (wie auf dem Schiff), Radarwarner auf dem Brückendach |
| Ortung | **6 Phalanx-Radare** am Mast (wie auf der Figet Marena), dazu ein Radar auf jedem Turm, Dachkamera |
| Brücke | die Brücke der Figet Marena: Steuersitz, Hauptmonitor 9×5 (Radar, Kamera, Zielliste), Monitor 3×3 = **Karte der KI**, Monitor 2×3 = **KI-Status**, Instrumentenblock; Aufstieg über Leitern hinten und hinter der Brücke |
| Antrieb | 14 Elektromotoren (Medium), je einer pro Rad, 24 große Batterien im Fahrwerksraum; gelenkt wird wie bei einem Kettenfahrzeug (links und rechts verschieden schnell) |
| KI | fährt Wegpunkte ab oder patrouilliert im Revier, weicht Hindernissen aus (7 Laser), meidet Wasser und Abhänge, befreit sich, wenn sie feststeckt, bleibt im Gefecht stehen (hält auch am Hang die Stelle), fährt auf Wunsch oder bei 40 % Batterie nach Hause, schießt nicht in die Schutzzone um ihre Basis |
| Aussehen | Tarnanstrich (Wald: Oliv, Dunkelgrün, Braun, Schwarz) auf allen Blöcken, unten Schlamm-Spritzer, Bug als Keil (oben und unten 45°), Heck unten abgeschrägt, Kennung „KL-1“ weiß und ein Abzeichen (gelber Blitz) an beiden Seiten, Lüftungsgitter auf dem Heckdeck |

### Woher die Teile kommen
Alles, was im Schiff schon funktioniert, ist **genau kopiert**: gleiche Teile, gleiche Abstände, gleiche Kabel,
gleiche Chip-Logik. Es gibt **keine einzige Teil-Art, die nicht auch im Schiff steckt**, also kennt dein Spiel alle
Teile.

- **Vorn (Bug):** AC-Turm + 10 Munitionstrommeln, genau wie am Bug der Figet Marena.
- **Dahinter:** BC-Turm mit Lade-Ablauf und Gurt-Magazin, genau wie auf dem Schiff.
- **Brücke** auf einem Sockel, in derselben Höhe über dem BC-Turm wie auf dem Schiff (dieselbe Sicht nach vorn).
- **Radarmast** hinter der Brücke, die 6 Radare in derselben Anordnung wie am Schiffsmast.
- **Chaff-Werfer** links und rechts auf dem Mitteldeck, wie an Deck des Schiffs.
- **Hinten:** beide Flak-Türme mit allen 48 Trommeln.
- **Chips:** Lage, Bildschirm, Flak L/R, Kanone BC/AC, Kamera und Schutz sind die Schiffs-Chips, neu gebaut mit den
  Maßen des Panzers. Dazu kommt der neue **KI-Chip**.

Was an Land anders sein muss, ist in die Chips eingebaut:
- Höhen zählen gegen die **eigene Höhe**, nicht gegen das Meer. An Land liegt der Boden nicht bei 0 m.
  Das betrifft die Lagezentrale (Luft oder Boden?) und das Turm-Radar (Mindesthöhe der Flak).
- Bodenziele sind Ziele für die Kanonen. Auf dem Schiff waren „Landziele“ gesperrt.
- Die Kanonen zielen auf die gemessene Zielhöhe. Auf dem Schiff war sie fest 1,5 m über dem Meer.
- Zielgröße für den Kamera-Zoom ist 10 m statt 40 m (Fahrzeuge statt Schiffe).
- Auto-Chaff ist an, solange die Waffen frei sind **und** eine Waffe ein Ziel hat. Es gibt keinen eigenen Schalter mehr.
- Der Waffen-Schreiber ist aus (Port 0). Baut man mit `--schreiber`, ist er an (Port 8768).

**Geprüft am Rechner, mit den Prüfständen deines Schiffs:**

| Prüfstand | Ergebnis |
|---|---|
| `tools/test_land_lage.py` | Panzer auf 100 m Höhe, 2 Bodenfahrzeuge, Hubschrauber, Jet, Gebäude. Kanonen auf Bodenfahrzeugen 329/360 Zeitschritte, nie auf Gebäude oder Luftziel. Flaks nur auf Luftzielen. Ohne die Land-Änderung: 0/360. |
| `tools/test_land_kanone.py` | BC und AC gegen fahrende Bodenziele am Hang (+45 m bis −25 m, 0,8–3 km): 47–55 % Treffer. Mit der festen Schiffs-Zielhöhe: 0 Treffer. |
| `tools/test_ki.py` | Fahr-KI in einer Simulation mit Hügeln, See, Klippe, Häusern, Wänden, Sackgasse, Wald, Damm, Tal: 61 Prüfungen, auch 10-Minuten-Dauerläufe ohne Unfall, mit größeren Rädern und Stehen am Hang (Einzelheiten `KI_FAHREN.md`) |
| `tools/pruefen.py` | Datei: XML, Teil-Arten, keine doppelten Plätze, Rumpf hängt zusammen, Kabel, Chips |
| `tools/test_build_mc.py` | Chip-Baukasten baut alle Schiffs-Chips byte-gleich nach |

---

## 2. Ins Spiel bringen

### Zwei Varianten
Der Panzer ist lang und schmal (Radstand 22 m, Spur ≈ 9 m). Solche Fahrzeuge drehen nur über
„links schneller als rechts“ (Skid-Lenkung) oft schlecht, weil alle Räder quer rutschen müssen. Darum gibt es zwei
Dateien:

| Datei | Lenkung |
|---|---|
| `KI Landkreuzer.xml` | nur Skid-Lenkung (wie ein Kettenfahrzeug): 14 feste Räder. Einfacher, weniger Teile. |
| `KI Landkreuzer Lenkung.xml` | dazu **Allrad-Lenkung**: Die vorderen 2 und die hinteren 2 Achsen sitzen auf senkrechten Gelenken (gebaut wie die Ruder der Figet Marena, mit kleinem Gelenk-Motor). Vorn und hinten lenken gegenläufig, die mittleren 3 Achsen bleiben fest. |

**Empfehlung:** Erst `KI Landkreuzer.xml` ausprobieren. Dreht er schlecht, die Lenk-Variante nehmen. Im Simulator
fährt die Lenk-Variante genauso sauber (Wegpunkte, Wand, Sackgasse, Dauerläufe) und streift im Wald weniger. Beide
haben denselben KI-Chip; die Lenk-Ausgänge sind in der einfachen Variante nur nicht verkabelt.

1. Auf dem PC das Repo holen (pull).
2. Die gewünschte Datei aus `landkreuzer/fahrzeug/` nach `%APPDATA%\Stormworks\data\vehicles\` kopieren.
3. **Räder:** Die Spiel-Dateien der Räder liegen nur auf deinem PC, darum fehlen sie noch.
   - Im Editor den Landkreuzer laden.
   - **Ein** Rad an die **vorderste linke Welle** setzen. Das ist der Stummel, der links unten vorn aus der
     Seitenwand kommt; das Bild `landkreuzer/bilder/rad_stummel.png` zeigt ihn pink. Das Rad muss an der Welle
     hängen. Speichern.
     - Tipp aus dem Netz für schwere Fahrzeuge: große Räder, Federung (Steifigkeit, Dämpfung) hoch, sonst schlägt
       sie durch. Je größer das Rad, desto mehr Bodenfreiheit (bei 7er-Rädern nur 0,5 m). Die KI stellt sich selbst
       auf die Radgröße ein (sie misst im Stand, wie hoch sie steht).
     - Platz: bis ca. 12 Blöcke Durchmesser passen zwischen die Achsen (Abstand 15 Blöcke).
   - Im Repo-Ordner: `python landkreuzer/tools/raeder.py`. Das ist ein Probelauf: Er zeigt, welche 13 Räder
     dazukommen. Für die Lenk-Variante `--lenkung` anhängen. Dort sitzt der vorderste linke Stummel außen am
     Gelenk, und die gelenkten Räder kommen auf ihre Gelenk-Körper. (Eine andere Datei: `--datei "<Pfad>"`.)
   - Dann `python landkreuzer/tools/raeder.py --schreiben`. Es kopiert das Rad an alle Wellen (rechts
     gespiegelt) und legt vorher eine Sicherung an.
   - Im Spiel das Fahrzeug **neu laden, ohne vorher zu speichern**.
   - Wenn du rechts ein anderes Rad willst: auch rechts vorn eines setzen, dann nimmt das Programm dieses für rechts.
   - Zweimal laufen lassen schadet nicht: Wellen, die schon ein Rad haben, bleiben, wie sie sind. Ein Rad aus
     mehreren Teilen (z. B. mit Kappe) wird als Ganzes kopiert. Nur rechts gesetzt geht auch (links wird gespiegelt).
4. Spawnen. Er ist groß (≈ 27 × 10 × 9 m) und braucht eine große **Land**-Werkbank, z. B. den großen Hangar auf der
   Kreativ-Insel (laut Forum gibt es die große Werkbank auch an anderen Orten; welche Insel was hat, steht bei der
   Insel-Auswahl). **Nicht** am Schiffs-Dock spawnen – dort steht er im Wasser. Zum Bearbeiten im Editor (Rad setzen)
   ist jede Werkbank recht, in die er passt.
5. **Einsteigen:** Leiter hinten (links der Mitte) aufs Deck. Die unterste Sprosse hängt je nach Rad etwa 1 m über
   dem Boden (das Heck ist unten abgeschrägt): hinlaufen und hochspringen. Nach vorn zur Plattform hinter der Brücke,
   dort die Leiter hoch, dann durch die Tür in der Rückwand der Brücke.

---

## 3. Bedienung

**Ganz ohne Bedienung:** 30 s nach dem Spawnen fährt er los (Zeit, um von Bord zu kommen oder in die Brücke zu
steigen), nach 60 s sind die Waffen frei. Dann schießt er selbst
und wirft Chaff, wenn ihn ein Radar erfasst (und seine Radare einen Gegner sehen). Er patrouilliert in 400 m um den Spawn-Punkt.

> **Achtung, kein Freund-Feind:** Die KI kennt keine Freunde (nur die Schutzzone, siehe unten). Mit freien Waffen
> beschießt sie **alles, was sich bewegt** und in Reichweite ist (BC bis 6 km). Das gilt auch für dich in Auto, Hubschrauber oder auf dem Schiff.
> Das Schiff macht es mit Master Arm genauso. Darum gilt:
> - Zum Testen vorher **„Waffen sperren“ an**.
> - Nach dem Spawnen hast du 60 s, um wegzukommen.
> - Willst du zu ihm hin, nähere dich zu Fuß. Ob Radare Menschen sehen, ist ungeprüft.
> - **Schutzzone:** Ist ein Ziel irgendeiner Waffe näher als **300 m** am Startpunkt (dort, wo du ihn gespawnt hast,
>   also an deiner Werkbank), schweigen **alle** Waffen, solange es aufgeschaltet ist; die KI fährt so ein Ziel auch
>   nicht an. Der KI-Status zeigt dann „SCHUTZZONE“. Deine Fahrzeuge an der Basis sind so sicher – unterwegs nicht.
>   Eigenschaft „Schutzzone m“ im KI-Chip (0 = aus). Auf der Karte: rot gestrichelter Kreis.
> - **Freund-Punkte:** Weitere Schutzzonen setzt du auf der Karte: **Finger 1,5 s auf eine Stelle halten** (ein blauer
>   Kreis wächst), z. B. auf deinen Hafen. Blau gestrichelt mit „F“. Nochmal dort halten = wieder weg. Höchstens 4;
>   nach einem Neuspawn sind sie weg.
> - Idee für später: Freund-Kennung per Funk. Deine Fahrzeuge senden ihren Ort, der Panzer schießt dort nicht hin.

### Schalter im Instrumentenblock (Brücke, links vom Sitz)
Die Schalter sind andersherum als auf dem Schiff. **Aus heißt: Die KI darf.**

| Schalter | Wirkung |
|---|---|
| **Waffen sperren** | an = kein Schuss, kein Chaff (Master Arm aus); aus = alle Waffen schießen selbst (außer auf Ziele in der Schutzzone) |
| **Aim correction** | Knopf, wie auf dem Schiff (Zielkorrektur per Blick) |
| **KI Pause** | an = KI fährt nicht (steht); aus = KI fährt |
| **Nach Hause** | an = fährt zum Spawn-Punkt zurück und bleibt dort stehen |

### Karte (Monitor 3×3 links vom Sitz)
- Auf die Karte **kurz** tippen: Dort kommt ein **Wegpunkt** hin. Bis zu 8 Wegpunkte, die KI fährt sie der Reihe nach
  im Kreis ab.
- Finger **1,5 s halten**: **Freund-Punkt** (Schutzzone, siehe oben), nochmal halten = weg.
- Knopf **Loeschen** zweimal binnen 3 s tippen: alle Wegpunkte weg (einmal wäre zu leicht aus Versehen). Ohne
  Wegpunkte patrouilliert die KI im Revier (Zufallspunkte bis 400 m um den Startpunkt, an jedem 45 s Pause).
- **+ / −**: Zoom. **Revier** (grün = an): nach dem letzten Wegpunkt wieder von vorn; aus = am letzten stehen bleiben.
- Oben steht der Zustand der KI (siehe unten). Auf der Karte: der Panzer als weißer Pfeil, **H** = Heimat
  (Spawn-Ort), blasse Punkte = seine **Fahrspur** (letzte 600 m), gelber Strich = wohin er gerade will.

### KI-Status (Monitor 2×3 rechts vom Sitz und im Helm)
Auf dem Schiff schaltete der Waffenwahl-Chip diesen Monitor ein. Im Panzer macht das der KI-Chip (Ausgang
„Immer an“). Bleibt er dunkel, im Editor nachsehen, ob der Monitor einen Ein-Schalter-Eingang hat und das Kabel dort
ankommt. Der Monitor zeigt:
- den Zustand der KI:

  | Zustand | heißt |
  |---|---|
  | AUS / PAUSE | KI aus (Schalter „KI Pause“ oder Startverzögerung) |
  | HAND | du fährst (W/S/A/D), oder 2 s Pause danach |
  | WEGPUNKT | fährt zum Wegpunkt oder nach Hause |
  | REVIER | fährt zum nächsten Revier-Punkt |
  | AUSWEICHEN | Hindernis vorn: kriecht und lenkt zur freien Seite |
  | ZURUECK | setzt zurück (Wand, Sackgasse, festgefahren) |
  | KAMPF | Ziel näher als 1,5 km: steht, Bug zum Ziel |
  | BATTERIE | Batterie fast leer: steht |
  | GEFAHR | Wasser, Kante oder zu schräg: zurück, die Stelle wird gemieden |
  | WARTET | am Ziel, zu Hause oder Pause im Revier |
  | LASER? | Laser vorn Mitte oder Bug-Laser meldet 0 (kein Strom, kein Kabel, nicht eingeschaltet): die KI ist blind und fährt nicht |

- das Tempo (ist/soll), den Wegpunkt, die Batterie, ob die Waffen frei sind
- hinter der Batterie die **Restzeit**: „BAT 83% 45M“ = bei diesem Verbrauch noch etwa 45 Minuten bis leer (gemessen
  alle 10 s; nach Hause fährt er schon bei 40 %). So siehst du beim ersten Test, wie lange er durchhält – bitte
  aufschreiben, dann kann ich Tempo und Pausen anpassen.
- die **7 Laser-Entfernungen**: VL, VM, VR = vorn links/Mitte/rechts, LI, RE = Seiten, UN = unten, HI = hinten.
  „--“ heißt: der Laser meldet 0 (kein Kabel oder kein Strom), „>1K“ heißt: frei (nichts in 1 km).
- **N** Nick (+ = Bug hoch), **R** Roll (+ = rechte Seite tief), **K** Kurs in Grad (0 Nord, 90 Ost) – so, wie die
  KI es sieht. Damit prüfst du die Vorzeichen: auf einen Hang stellen, rechte Seite tief → muss R+ zeigen; Bug bergauf
  → N+; nach Norden fahren → K um 0. Stimmt eins nicht, im KI-Chip „Roll Richtung“, „Nick Richtung“ bzw.
  „Kompass Richtung“ umdrehen (1 ↔ −1).
- rot **L!** / **R!** hinter dem Kurs: Die KI hat gemerkt, dass die linke/rechte Radseite falsch herum dreht, und es
  selbst umgedreht. Das gilt nur bis zum nächsten Spawn – stell dann im KI-Chip „Rad Richtung links“ bzw. „rechts“
  dauerhaft um (1 ↔ −1).
- zwei Balken für die Motoren links und rechts (grün = vorwärts, rot = rückwärts, wie die KI es meint).

Vorschau beider Monitore: `bilder/anzeigen.png` (gezeichnet mit `tools/anzeige_bild.py`).

Im Helm steht dasselbe kurz in einer Zeile unten.

### Selbst fahren
Hinsetzen und **W/S/A/D** drücken: Du fährst. 2 s nach dem Loslassen übernimmt die KI wieder, wenn sie nicht auf
Pause steht. Die Waffen bedienst du wie auf dem Schiff: **H5** wählt die Waffe für die Kamera, die **Leertaste**
gibt einen Schuss der gewählten Waffe ab.

---

## 4. Was im Spiel zuerst geprüft werden muss (ehrlich: nichts davon ist im Spiel getestet)

In dieser Reihenfolge. Anfangen jeweils mit **KI Pause an** und **Waffen sperren an**:

1. **Lädt die Datei?** Der Editor zeigt den Panzer. Wenn nicht, bitte die Fehlermeldung aufschreiben.
2. **Räder an den Wellen?** Nach `raeder.py` sitzen 14 Räder an den Wellen.
3. **Antrieb:** Hinsetzen, W drücken.
   - Drehen alle Räder? Wenn nicht, sitzt ein Motor falsch herum.
     Annahme: Die Kraft kommt **unten** aus dem Motor, so wie am Bugstrahlruder und an den Ruder-Motoren des Schiffs.
   - Fährt er bei W vorwärts? Die Richtung je Seite stellen die Eigenschaften „Rad Richtung links/rechts“ im
     KI-Chip ein. Die KI lernt das auch selbst, solange „Richtung lernen“ 1 ist.
4. **Laser:** Auf dem KI-Status-Monitor stehen alle 7 Entfernungen. Bei „--“ hängt ein Laser nicht richtig.
   Annahme: Strom, Ausgang und Einschalten sitzen am Laser-Block selbst, der Strahl zeigt wie bei der Turm-Kamera.
   Die Turm-Kamera hat für ihren Laser einen Eingang „Laser an“; darum bekommt jeder Laser vom KI-Chip
   (Ausgang „Immer an“) ein Einschalt-Kabel. Zeigen trotzdem alle „--“: im Editor an einem Laser nachsehen,
   welche Anschlüsse er hat, und mir sagen. Solange der mittlere Front-Laser oder der Bug-Laser 0 meldet, fährt die
   KI nicht (Zustand LASER?) – sie fährt also nie blind los.
5. **Türme:** wie auf dem Schiff (Test Rohre usw.). Die Richtungs-Eigenschaften sind die vom Schiff, weil die Türme
   genauso eingebaut sind.
6. **Lenk-Variante:** Hinsetzen, D drücken. Lenken die vorderen Räder nach rechts und die hinteren nach links?
   Wenn es andersherum ist: Eigenschaft „Lenk Richtung“ im KI-Chip auf −1. Drehen sich die Gelenke gar nicht:
   Bekommen die kleinen Gelenk-Motoren Strom und Gas (Konstante 1)? Beides ist wie beim Schiffs-Ruder verkabelt.
   Anders als beim Ruder trägt hier jedes Gelenk das Gewicht seines Rades. Knickt ein Rad weg oder wackelt es stark,
   ist das Gelenk zu schwach; dann bleibt nur die einfache Variante.
7. **KI:** Erst die Vorzeichen auf dem Status-Monitor prüfen (N, R, K – siehe „KI-Status“). Dann KI Pause aus, auf
   freiem Gelände. Fährt er los, weicht er aus, hält er vor Wasser? Die genaue Prüfliste (Kompass, Rad-Richtung,
   Nick/Roll, Bug-Laser, Bremsweg, Karte) steht in `KI_FAHREN.md`, Abschnitt 6.
8. **Waffen:** Waffen sperren aus, mit Gegnern.
9. **Chaff:** Auf dem Schiff war offen, ob der Radarwarner die **eigenen** Radare meldet. Damit das nicht alle Werfer
   leert, wirft der Panzer Chaff nur, wenn seine Radare auch einen Gegner sehen. Wirft er trotzdem ständig (sobald
   irgendein Ziel da ist), bitte melden.

### Fehlersuche: wenn du das siehst …

Alle Eigenschaften stehen im **KI-Chip** (im Editor anklicken). Nach dem Ändern speichern und neu spawnen.

| Du siehst | Dann |
|---|---|
| Status zeigt **LASER?**, fährt nicht | ein Laser meldet 0: Status-Zeilen VM/UN prüfen; Laser-Kabel/Strom im Editor ansehen |
| Status-Monitor bleibt **dunkel** | hat der Monitor 2×3 einen Ein-Schalter-Eingang? Kabel vom KI-Chip „Immer an“ dorthin |
| Bei W fährt er **rückwärts** | „Rad Richtung links“ und „Rad Richtung rechts“ umdrehen (1 ↔ −1) |
| Er **dreht statt zu fahren**, rot **L!** oder **R!** | diese Seite in „Rad Richtung links/rechts“ umdrehen |
| Fährt zum Wegpunkt in **falscher Richtung**/Spirale | Status K beim Fahren nach Norden ≈ 0? Sonst „Kompass Richtung“ umdrehen |
| Am Hang **GEFAHR**, obwohl flach, oder dreht falsch | Status N/R prüfen (Bug hoch = N+, rechts tief = R+), sonst „Nick/Roll Richtung“ umdrehen |
| Bleibt vor jedem **sanften Hügel** stehen | „Steigung max Grad“ höher (30 → 35) |
| **Fährt zu schnell** an Hindernisse | „Tempo m/s“ kleiner (8 → 6) |
| **Dreht zu träge** | „Lenk Staerke“ höher; Lenk-Variante: „Lenk Faktor“ höher |
| **Schaukelt/pendelt** beim Geradeausfahren | „Lenk Staerke“ kleiner (4 → 2) |
| Lenk-Variante lenkt **falsch herum** | „Lenk Richtung“ = −1 |
| **Batterie** schnell leer (Restzeit im Status) | „Tempo m/s“ kleiner, „Patrouille Pause s“ länger, „Heim Batterie“ höher |
| Schießt **nicht** | Status: WAFFEN FREI? SCHUTZZONE? Schalter „Waffen sperren“ aus? 60 s nach dem Spawnen? |
| Schießt auf **eigene Fahrzeuge** | dort einen Freund-Punkt setzen (Karte, Finger 1,5 s halten) oder „Schutzzone m“ größer |
| Wirft **dauernd Chaff** | melden (Radarwarner sieht vermutlich die eigenen Radare) |
| Steckt im **Wald** fest | Wegpunkte um den Wald setzen; Lenk-Variante streift weniger |
| Nach **Spielstand laden** Wegpunkte weg, „H“ woanders | normal: die Skripte starten neu, Heimat = Ort beim Laden (siehe Schwachstellen) |

### Bekannte Schwachstellen
- **Strom:** Es gibt nur Batterien (24 große), keinen Generator. Den Schiffs-Diesel kann man nicht einfach übernehmen,
  weil er mit Seewasser kühlt. 14 Medium-Motoren ziehen viel Strom (laut Forum etwa so viel
  wie ein großer Motor leistet). Wie lange die Batterien reichen, ist offen. Für lange Einsätze braucht es einen
  Diesel-Generator; Platz dafür ist im Fahrwerksraum. Die KI fährt sparsam: Im Revier wartet sie an jedem Punkt,
  bei wenig Batterie fährt sie langsamer.
  Laut Forum werden Elektromotoren mit sinkender Ladung schwächer (schon ab etwa 80 % merkbar). Darum fährt die KI
  schon bei **40 %** Ladung nach Hause (Eigenschaft „Heim Batterie“ im KI-Chip), damit sie es noch den Hang hoch
  schafft. Ab 50 % fährt sie wieder normal.
- **Größe:** Der Panzer ist sehr groß (≈ 27 × 10 m). Eine kleinere Werkbank reicht nicht.
- **Spielstand laden:** Beim Laden startet jedes Lua-Skript neu (bekannt aus dem Forum, z. B. bei Autopilot-Karten
  aus dem Workshop). Für den Panzer heißt das: Wegpunkte und Freund-Punkte sind weg, die **Heimat** (und damit
  Revier und Schutzzone) ist dann der Ort, an dem er beim Laden steht, und die Wartezeiten (30 s Fahren, 60 s Waffen)
  laufen neu. Nach dem Laden also kurz prüfen, wo das „H“ auf der Karte steht.
- **Dichter Wald:** Im Simulator kommt er durch einen lichten Wald, in dichtem Wald (Bäume im Mittel 30 m
  auseinander) bleibt er aber in 3 von 8 Fällen hängen und streift viele Bäume. Grund: Er ist 27 m lang und 9,5 m
  breit, und dünne Stämme genau vor einer Bugecke sieht kein Laser. Zwei zusätzliche Eck-Laser habe ich ausprobiert –
  damit wurde es schlechter, darum sind sie nicht drin. **Wegpunkte um Wälder herum setzen** und das Revier nicht in
  ein Waldgebiet legen.
- **Wackeln/Zittern:** Laut Forum hilft bei großen Fahrzeugen mit Gelenken eine höhere Physik-Stufe in den
  Einstellungen (Allgemein). Räder berühren den Boden nur an einem Punkt (dem untersten beim Bauen); darum sind die
  Lenk-Gelenke senkrecht, so bleibt dieser Punkt beim Lenken unten.
- **Räder:** Welches Rad am besten passt, musst du ausprobieren (siehe oben).
- **Licht:** Er hat keine Scheinwerfer, weil es im Schiff keine Licht-Teile gibt (siehe „Woher die Teile kommen“).
  Die KI fährt nachts trotzdem, denn die Laser sehen im Dunkeln. Willst du ihn nachts sehen: im Editor 2–4
  Scheinwerfer vorn an die Bug-Schräge setzen, Strom von einer Batterie, an einen Knopf in der Brücke. Laut Forum
  machen viele Lichter große Fahrzeuge langsamer, also lieber wenige.

---

## 5. Technik (für spätere Arbeit)

| Datei | Was |
|---|---|
| `tools/bau_landkreuzer.py` | baut die ganze Fahrzeugdatei neu und prüft sie (`python landkreuzer/tools/bau_landkreuzer.py`, Lenk-Variante mit `--lenkung`) |
| `tools/fz.py` | Fahrzeugdatei lesen/schreiben (Teile, Körper, Kabel); Lesen und Schreiben ergibt byte-gleich dieselbe Datei |
| `tools/build_mc.py` | Chip-Baukasten (Nachbau des fehlenden Originals; baut alle Schiffs-Chips byte-gleich nach, siehe `tools/test_build_mc.py`) |
| `tools/build_ki.py` | KI-Chip (5×5) |
| `tools/raeder.py` | Räder kopieren (`--lenkung` für die Lenk-Variante; Prüfstand `tools/test_raeder.py`) |
| `tools/pruefen.py` | Prüfungen der Datei (läuft nach jedem Bau) |
| `tools/ki_log.py` | wertet einen Fahrtenschreiber-Log aus (`python landkreuzer/tools/ki_log.py logs/waffen_...`): Zusammenfassung und Bild der Fahrt |
| `tools/kabel_vergleich.py` | jedes Kabel des Schiffs, dessen Quelle im Panzer fehlt (fand den dunklen Monitor 2×3) |
| `tools/alles_pruefen.py` | baut beide Varianten und lässt alle Prüfstände laufen (`--schnell` ohne die langen) |
| `tools/ansicht.py` | Bilder zeichnen (braucht matplotlib) |
| `tools/anzeige_bild.py` | Vorschau der Monitore Karte und KI-Status (braucht lupa und pillow) |
| `tools/test_ki.py` | Prüfstand der Fahr-KI (Simulation, braucht lupa) |
| `KI_FAHREN.md` | **alles zur Fahr-KI**: Verhalten, Kanäle, alle Eigenschaften mit Erklärung, Grenzen, Prüfliste im Spiel |
| `tools/ki_props.py` | Eigenschaften der Fahr-KI und Karte (Standardwerte) |
| `tools/test_ki_teile.py` | Prüfstand Kleber, Lenkung, Status-Anzeige |
| `tools/test_land_lage.py`, `tools/test_land_kanone.py` | Prüfstände Waffen an Land (mit den Schiffs-Prüfständen, braucht lupa) |
| `lua/ki_kleber.lua`, `lua/ki_fahren.lua`, `lua/ki_karte.lua`, `lua/ki_status.lua`, `lua/ki_lenkung.lua` | die fünf Skripte im KI-Chip |

**Koordinaten** (Blöcke à 0,25 m): x rechts, y oben, z vorn. Das ist ein **Linkssystem** (wie die Welt im Spiel:
x Ost, y oben, z Nord). Wer Bilder zeichnet, muss darauf achten, sonst ist alles spiegelverkehrt (so war es bei den
ersten Bildern von rechts).
- Höhen: Boden des Fahrwerksraums y −4, Hauptboden y 1, Deck vorn y 6, Mitte y 10, hinten y 9.
- Bug-Keil z 37 … 42: oben 45° vom Deck (y 6) herab, unten 45° vom Boden herauf, Spitze bei y 0,5 (1,25 m über der
  Rumpf-Unterkante). Vorher lag die Spitze unten am Boden, 3 m vor den Vorderrädern; mit kleinen Rädern hätte er
  schon an Hängen ab etwa 10° aufgesetzt. Jetzt begrenzt die untere Schräge (45°).
- Heck: die letzten 3 Reihen (z −64 … −66) unten 45° hochgezogen. Mit großen Rädern (12 Blöcke) setzt das Heck erst
  an Hängen über etwa 34° auf (vorher 24°).
- Bodenfreiheit = Rad-Radius − 1,5 Blöcke (Achse bei y −3, Unterkante y −4,5). Bei 7er-Rädern nur 0,5 m, darum
  lieber große Räder.
- Brücken-Boden y 15.
- Wellen-Stummel bei x ±15, y −3, z 35 / 20 / 5 / −10 / −25 / −40 / −55 (Mitte = geschätzter Schwerpunkt).
- **Schwerpunkt** (geschätzt, jedes Teil gleich schwer): y ≈ 5, also gut 2,5 m über dem Boden bei ≈ 8,5 m Spur.
  Er kippt erst bei sehr steilen Seitenhängen (über 45°); Ballast ist nicht nötig. Die KI meidet steile Hänge ohnehin.
- **Chips** liegen auf dem Hauptboden in der Mitte (y 2, z −29 … −17), der Physik-Sensor bei (0, 2, −12).
  Die Batterien sitzen im Fahrwerksraum. Den Ladestand liest die KI von einer **kleinen Batterie** bei (0, −3, −14)
  im selben Stromnetz: Bei ihr sitzen alle Anschlüsse in ihrem einen Block, bei der großen ist offen, wo der
  Ladestand herauskommt. Zeigt der Status „BAT ?“, kommt kein Wert an (dann fährt die KI ohne Batterie-Regeln).

---

## 6. Ideen für später

- **Freund-Kennung per Funk:** Deine Fahrzeuge (Schiff, Heli) senden ihren GPS-Ort auf einer Frequenz. Der Panzer
  schießt dort nicht hin und zeigt sie auf der Karte. Dafür braucht es Funk-Teile (Antenne, Radio). Die gibt es im
  Schiff noch nicht, darum kann Claude sie nicht per Datei einbauen. Setzt du sie einmal ein, kann ich die Logik bauen.
- **Raketen-Abwehr (APS):** Die Flaks schießen schnelle Objekte ab, die auf den Panzer zufliegen. Das ist dieselbe
  Idee wie die geplante Raketenabwehr des Schiffs (`SCHIFF_UEBERSICHT.md`, Abschnitt 11). Das Lage-Skript ist dafür
  zu voll und muss erst aufgeteilt werden.
- **Diesel-Generator** für lange Einsätze: Der Schiffs-Diesel kühlt mit Seewasser. An Land braucht es einen
  geschlossenen Kühlkreis mit Kühlern.
- **Befehle vom Schiff:** Wegpunkte für den Panzer auf der Schiffskarte setzen (Funk).
- **Keep Active Block** (siehe Schiffs-Übersicht): Ohne ihn wird der Panzer nicht simuliert, wenn du weit weg bist.
  Er bleibt dann stehen.
- **Weitere Geschütz-Arten** (Rotary/Light Autocannon, Artillerie, Bertha): Deren Spiel-Definitionen sind nicht in
  der Schiffsdatei. Setzt du je eins auf ein Testfahrzeug und lädst es hoch, kann der Generator sie einbauen.

