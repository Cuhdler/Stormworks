# KI-Landkreuzer – ein Panzer, der selbst fährt und kämpft

**Stand:** 08.10.2026 (Nacht), Version v1.0, gebaut von Claude, **noch nie im Spiel gewesen**.
**Dateien:** `landkreuzer/fahrzeug/KI Landkreuzer.xml` und `KI Landkreuzer Lenkung.xml` (zwei Varianten, siehe
Abschnitt 2). Beide sind fertig, nur die Räder fehlen.
**Bilder:** `landkreuzer/bilder/schraeg.png` und `schraeg_links.png` (schräg von vorn), `schraeg_lenkung.png`
(Lenk-Variante), `ansicht.png` (oben, Seite, vorn).

Andres Wunsch (08.10.): „eine Art Landkreuzer, groß, mit allen möglichen Geschützen, und er soll komplett autonom
fahren – quasi ein KI-Panzer“.

---

## 1. Was er ist

| | |
|---|---|
| Größe | Rumpf 28 m lang (mit Bug-Schräge), mit AC-Rohr 29 m; 7,75 m breit + Räder ≈ 9–10 m; Mast ≈ 9 m über dem Boden des Rumpfs |
| Teile | ca. 17 000, 25 Körper, ca. 390 Kabel, 9 Chips |
| Waffen | vorn **Heavy-Autocannon-Turm** (AP), dahinter erhöht **Battle-Cannon-Turm mit 2 Rohren** (HE), hinten **2 Flak-Türme** mit je 2 Heavy Autocannons (Splitter, Zeitzünder) |
| Schutz | **Auto-Chaff**: 8 Werfer-Ketten mit je 15 Werfern (wie auf dem Schiff), Radarwarner auf dem Brückendach |
| Ortung | **6 Phalanx-Radare** am Mast (wie auf der Figet Marena), dazu ein Radar auf jedem Turm, Dachkamera |
| Brücke | die Brücke der Figet Marena: Steuersitz, Hauptmonitor 9×5 (Radar, Kamera, Zielliste), Monitor 3×3 = **Karte der KI**, Monitor 2×3 = **KI-Status**, Instrumentenblock; Aufstieg über Leitern hinten und hinter der Brücke |
| Antrieb | 14 Elektromotoren (Medium), je einer pro Rad, 24 große Batterien im Fahrwerksraum; gelenkt wird wie bei einem Kettenfahrzeug (links und rechts verschieden schnell) |
| KI | fährt Wegpunkte ab oder patrouilliert im Revier, weicht Hindernissen aus (7 Laser), meidet Wasser und Abhänge, befreit sich, wenn sie feststeckt, bleibt im Gefecht stehen, fährt auf Wunsch nach Hause |
| Aussehen | Tarnanstrich (Wald: Oliv, Dunkelgrün, Braun, Schwarz) auf allen Blöcken, 45°-Bug-Schräge, Kennung „KL-1“ weiß an beiden Seiten |

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
- Auto-Chaff ist an, solange die Waffen frei sind. Es gibt keinen eigenen Schalter mehr.
- Der Waffen-Schreiber ist aus (Port 0). Baut man mit `--schreiber`, ist er an (Port 8768).

**Geprüft am Rechner, mit den Prüfständen deines Schiffs:**

| Prüfstand | Ergebnis |
|---|---|
| `tools/test_land_lage.py` | Panzer auf 100 m Höhe, 2 Bodenfahrzeuge, Hubschrauber, Jet, Gebäude. Kanonen auf Bodenfahrzeugen 329/360 Zeitschritte, nie auf Gebäude oder Luftziel. Flaks nur auf Luftzielen. Ohne die Land-Änderung: 0/360. |
| `tools/test_land_kanone.py` | BC und AC gegen fahrende Bodenziele am Hang (+45 m bis −25 m, 0,8–3 km): 47–55 % Treffer. Mit der festen Schiffs-Zielhöhe: 0 Treffer. |
| `tools/test_ki.py` | Fahr-KI in einer Simulation (siehe Abschnitt 3) |
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

**Empfehlung:** Erst `KI Landkreuzer.xml` ausprobieren. Dreht er schlecht, die Lenk-Variante nehmen. Beide
haben denselben KI-Chip; die Lenk-Ausgänge sind in der einfachen Variante nur nicht verkabelt.

1. Auf dem PC das Repo holen (pull).
2. Die gewünschte Datei aus `landkreuzer/fahrzeug/` nach `%APPDATA%\Stormworks\data\vehicles\` kopieren.
3. **Räder:** Die Spiel-Dateien der Räder liegen nur auf deinem PC, darum fehlen sie noch.
   - Im Editor den Landkreuzer laden.
   - **Ein** Rad an die **vorderste linke Welle** setzen. Das ist der Stummel, der links unten vorn aus der
     Seitenwand kommt. Das Rad muss an der Welle hängen. Speichern.
     - Tipp aus dem Netz für schwere Fahrzeuge: große Räder (7×7). Federung (Steifigkeit, Dämpfung) hoch, sonst schlägt
       sie durch. Mehr und größere Räder sind besser als wenige.
     - Platz: bis ca. 12 Blöcke Durchmesser passen zwischen die Achsen (Abstand 15 Blöcke).
   - Im Repo-Ordner: `python landkreuzer/tools/raeder.py`. Das ist ein Probelauf: Er zeigt, welche 13 Räder
     dazukommen. Für die Lenk-Variante: `--datei "%APPDATA%\Stormworks\data\vehicles\KI Landkreuzer Lenkung.xml"`
     anhängen. Dort sitzt der vorderste linke Stummel außen am Gelenk, und die gelenkten Räder kommen auf ihre
     Gelenk-Körper.
   - Dann `python landkreuzer/tools/raeder.py --schreiben`. Es kopiert das Rad an alle Wellen (rechts
     gespiegelt) und legt vorher eine Sicherung an.
   - Im Spiel das Fahrzeug **neu laden, ohne vorher zu speichern**.
   - Wenn du rechts ein anderes Rad willst: auch rechts vorn eines setzen, dann nimmt das Programm dieses für rechts.
4. Spawnen. Er ist groß und braucht eine große Werkbank bzw. einen großen Platz.
5. **Einsteigen:** Leiter hinten (links der Mitte) aufs Deck. Nach vorn zur Plattform hinter der Brücke, dort die
   Leiter hoch, dann durch die Tür in der Rückwand der Brücke.

---

## 3. Bedienung

**Ganz ohne Bedienung:** 10 s nach dem Spawnen fährt er los, nach 60 s sind die Waffen frei. Dann schießt er selbst
und wirft Chaff, wenn ihn ein Radar erfasst. Er patrouilliert in 400 m um den Spawn-Punkt.

> **Achtung, kein Freund-Feind:** Die KI kennt keine Freunde. Mit freien Waffen beschießt sie **alles, was sich
> bewegt** und in Reichweite ist (BC bis 6 km). Das gilt auch für dich in Auto, Hubschrauber oder auf dem Schiff.
> Das Schiff macht es mit Master Arm genauso. Darum gilt:
> - Zum Testen vorher **„Waffen sperren“ an**.
> - Nach dem Spawnen hast du 60 s, um wegzukommen.
> - Willst du zu ihm hin, nähere dich zu Fuß. Ob Radare Menschen sehen, ist ungeprüft.
> - Idee für später: Freund-Kennung per Funk. Deine Fahrzeuge senden ihren Ort, der Panzer schießt dort nicht hin.

### Schalter im Instrumentenblock (Brücke, links vom Sitz)
Die Schalter sind andersherum als auf dem Schiff. **Aus heißt: Die KI darf.**

| Schalter | Wirkung |
|---|---|
| **Waffen sperren** | an = kein Schuss, kein Chaff (Master Arm aus); aus = alle Waffen schießen selbst |
| **Aim correction** | Knopf, wie auf dem Schiff (Zielkorrektur per Blick) |
| **KI Pause** | an = KI fährt nicht (steht); aus = KI fährt |
| **Nach Hause** | an = fährt zum Spawn-Punkt zurück und bleibt dort stehen |

### Karte (Monitor 3×3 links vom Sitz)
- Auf die Karte tippen: Dort kommt ein **Wegpunkt** hin. Bis zu 8 Wegpunkte, die KI fährt sie der Reihe nach im Kreis ab.
- Knopf **Löschen**: alle Wegpunkte weg. Ohne Wegpunkte patrouilliert die KI im Revier.
- **+ / −**: Zoom. **Revier**: Patrouille an/aus.

### KI-Status (Monitor 2×3 rechts vom Sitz und im Helm)
Der Monitor zeigt:
- den Zustand der KI (z. B. WEGPUNKT, REVIER, AUSWEICHEN, ZURUECK, GEFECHT, GEFAHR, ANGEKOMMEN)
- das Tempo (ist/soll), den Wegpunkt, die Batterie, ob die Waffen frei sind
- die **7 Laser-Entfernungen**: VL, VM, VR = vorn links/Mitte/rechts, LI, RE = Seiten, UN = unten, HI = hinten.
  „--“ heißt: der Laser meldet nichts.
- zwei Balken für die Motoren links und rechts.

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
   Annahme: Strom und Ausgang sitzen am Laser-Block selbst, der Strahl zeigt wie bei der Turm-Kamera.
5. **Türme:** wie auf dem Schiff (Test Rohre usw.). Die Richtungs-Eigenschaften sind die vom Schiff, weil die Türme
   genauso eingebaut sind.
6. **Lenk-Variante:** Hinsetzen, D drücken. Lenken die vorderen Räder nach rechts und die hinteren nach links?
   Wenn es andersherum ist: Eigenschaft „Lenk Richtung“ im KI-Chip auf −1. Drehen sich die Gelenke gar nicht:
   Bekommen die kleinen Gelenk-Motoren Strom und Gas (Konstante 1)? Beides ist wie beim Schiffs-Ruder verkabelt.
7. **KI:** KI Pause aus, auf freiem Gelände. Fährt er los, weicht er aus, hält er vor Wasser?
8. **Waffen:** Waffen sperren aus, mit Gegnern.
9. **Chaff:** Auf dem Schiff war offen, ob der Radarwarner die **eigenen** Radare meldet. Wenn ja, wirft der Panzer
   dauernd Chaff, bis die 60 Salven leer sind. Dann bitte melden; ich baue dann eine Sperre ein.

### Bekannte Schwachstellen
- **Strom:** Es gibt nur Batterien (24 große), keinen Generator. Den Schiffs-Diesel kann man nicht einfach übernehmen,
  weil er mit Seewasser kühlt. 14 Medium-Motoren ziehen viel Strom (laut Forum etwa so viel
  wie ein großer Motor leistet). Wie lange die Batterien reichen, ist offen. Für lange Einsätze braucht es einen
  Diesel-Generator; Platz dafür ist im Fahrwerksraum. Die KI fährt sparsam: Im Revier wartet sie an jedem Punkt,
  bei wenig Batterie fährt sie langsamer.
- **Größe:** Der Panzer ist sehr groß (≈ 28 × 10 m). Eine kleinere Werkbank reicht nicht.
- **Räder:** Welches Rad am besten passt, musst du ausprobieren (siehe oben).

---

## 5. Technik (für spätere Arbeit)

| Datei | Was |
|---|---|
| `tools/bau_landkreuzer.py` | baut die ganze Fahrzeugdatei neu und prüft sie (`python landkreuzer/tools/bau_landkreuzer.py`, Lenk-Variante mit `--lenkung`) |
| `tools/fz.py` | Fahrzeugdatei lesen/schreiben (Teile, Körper, Kabel); Lesen und Schreiben ergibt byte-gleich dieselbe Datei |
| `tools/build_mc.py` | Chip-Baukasten (Nachbau des fehlenden Originals; baut alle Schiffs-Chips byte-gleich nach, siehe `tools/test_build_mc.py`) |
| `tools/build_ki.py` | KI-Chip (5×5) |
| `tools/raeder.py` | Räder kopieren |
| `tools/pruefen.py` | Prüfungen der Datei (läuft nach jedem Bau) |
| `tools/ansicht.py` | Bilder zeichnen (braucht matplotlib) |
| `tools/test_ki.py` | Prüfstand der Fahr-KI (Simulation, braucht lupa) |
| `tools/test_ki_teile.py` | Prüfstand Kleber, Lenkung, Status-Anzeige |
| `tools/test_land_lage.py`, `tools/test_land_kanone.py` | Prüfstände Waffen an Land (mit den Schiffs-Prüfständen, braucht lupa) |
| `lua/ki_kleber.lua`, `lua/ki_fahren.lua`, `lua/ki_karte.lua`, `lua/ki_status.lua`, `lua/ki_lenkung.lua` | die fünf Skripte im KI-Chip |

**Koordinaten** (Blöcke à 0,25 m): x rechts, y oben, z vorn.
- Höhen: Boden des Fahrwerksraums y −4, Hauptboden y 1, Deck vorn y 6, Mitte y 10, hinten y 9.
- Bug-Schräge z 37 … 47. Brücken-Boden y 15.
- Wellen-Stummel bei x ±15, y −3, z 35 / 20 / 5 / −10 / −25 / −40 / −55 (Mitte = geschätzter Schwerpunkt).
- **Chips** liegen auf dem Hauptboden in der Mitte (y 2, z −29 … −17), der Physik-Sensor bei (0, 2, −12).
  Die Batterien sitzen im Fahrwerksraum.

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

