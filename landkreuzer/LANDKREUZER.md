# KI-Landkreuzer – ein Panzer, der selbst fährt und kämpft

**Stand:** 08.10.2026 (Nacht), Version v1.0, gebaut von Claude, **noch nie im Spiel gewesen**.
**Datei:** `landkreuzer/fahrzeug/KI Landkreuzer.xml` (fertig, nur die Räder fehlen, siehe Schritt 3).
**Bild:** `landkreuzer/bilder/ansicht.png` (von oben, von der Seite, von vorn).

Andres Wunsch (08.10.): „eine Art Landkreuzer, groß, mit allen möglichen Geschützen, und er soll komplett autonom
fahren – quasi ein KI-Panzer“.

---

## 1. Was er ist

| | |
|---|---|
| Größe | ca. 29 m lang (mit Rohr), 7,75 m Rumpf + Räder = ca. 8,5–9,5 m breit, ca. 10 m hoch (Mast) |
| Teile | ca. 16 000, 17 Körper, ca. 250 Kabel, 8 Chips |
| Waffen | vorn **Heavy-Autocannon-Turm** (AP), dahinter erhöht **Battle-Cannon-Turm mit 2 Rohren** (HE), hinten **2 Flak-Türme** mit je 2 Heavy Autocannons (Splitter, Zeitzünder) |
| Ortung | **6 Phalanx-Radare** am Mast (wie auf der Figet Marena), dazu ein Radar auf jedem Turm |
| Brücke | die Brücke der Figet Marena: Steuersitz, Hauptmonitor 9×5 (Radar, Kamera, Zielliste), Monitor 3×3 = **Karte der KI**, Instrumentenblock, Dachkamera |
| Antrieb | 14 Elektromotoren (Medium), je einer pro Rad, 8 große Batterien, Lenken wie ein Kettenfahrzeug (links/rechts verschieden schnell) |
| KI | fährt Wegpunkte ab oder patrouilliert im Revier, weicht Hindernissen aus (7 Laser), meidet Wasser und Abhänge, befreit sich, wenn sie feststeckt, bleibt im Gefecht stehen, fährt auf Wunsch nach Hause |

### Woher die Teile kommen
Alles, was im Schiff schon funktioniert, ist **genau kopiert** (gleiche Teile, gleiche Abstände, gleiche Kabel,
gleiche Chip-Logik):

- **Vorn (Bug):** AC-Turm + 10 Munitionstrommeln, genau wie am Bug der Figet Marena.
- **Dahinter:** BC-Turm mit Lade-Ablauf und Gurt-Magazin, genau wie auf dem Schiff.
- **Brücke** auf einem Sockel, dieselbe Höhe über dem BC-Turm wie auf dem Schiff (dieselbe Sicht nach vorn).
- **Radarmast** hinter der Brücke, die 6 Radare in derselben Anordnung wie am Schiffsmast.
- **Hinten:** beide Flak-Türme mit allen 48 Trommeln.
- **Chips:** Lage, Bildschirm, Flak L/R, Kanone BC/AC und Kamera sind die Schiffs-Chips, neu gebaut mit den Maßen
  des Panzers. Dazu kommt der neue **KI-Chip**.

Was es an Land anders macht, ist in die Chips eingebaut:
- Höhen zählen gegen die **eigene Höhe**, nicht gegen das Meer (an Land liegt der Boden nicht bei 0 m).
- Bodenziele sind Ziele für die Kanonen. Auf dem Schiff waren „Landziele“ gesperrt.
- Die Kanonen zielen auf die gemessene Zielhöhe. Auf dem Schiff war die Zielhöhe fest 1,5 m über dem Meer.
- Zielgröße für den Kamera-Zoom ist 10 m statt 40 m (Fahrzeuge statt Schiffe).
- Der Waffen-Schreiber ist aus (Port 0). Mit `--schreiber` beim Bauen ist er an (Port 8768).

---

## 2. Ins Spiel bringen

1. Auf dem PC das Repo holen (pull).
2. `landkreuzer/fahrzeug/KI Landkreuzer.xml` nach `%APPDATA%\Stormworks\data\vehicles\` kopieren.
3. **Räder:** Die Spiel-Dateien der Räder liegen nur auf deinem PC, darum fehlen sie noch.
   - Im Editor den Landkreuzer laden.
   - **Ein** Rad (das größte, das du hast) an die **vorderste linke Welle** setzen. Das ist der Stummel, der links
     unten vorn aus der Seitenwand kommt. Das Rad muss an der Welle hängen. Speichern.
   - Im Repo-Ordner: `python landkreuzer/tools/raeder.py`. Das ist ein Probelauf: Er zeigt, welche 13 Räder
     dazukommen.
   - Dann `python landkreuzer/tools/raeder.py --schreiben`. Es kopiert das Rad an alle Wellen (rechts
     gespiegelt) und legt vorher eine Sicherung an.
   - Im Spiel das Fahrzeug **neu laden, ohne vorher zu speichern**.
   - Wenn du rechts ein anderes Rad willst: auch rechts vorn eines setzen, dann nimmt das Programm dieses für
     rechts.
4. Spawnen. Er ist groß, er braucht eine große Werkbank bzw. einen großen Platz.

---

## 3. Bedienung

**Ganz ohne Bedienung:** 10 s nach dem Spawnen fährt er los und schießt selbst. Er patrouilliert dann in 400 m um den
Spawn-Punkt.

### Schalter im Instrumentenblock (Brücke, links vom Sitz)
Die Schalter sind andersherum als auf dem Schiff. **Aus heißt: Die KI darf.**

| Schalter | Wirkung |
|---|---|
| **Waffen sperren** | an = kein Schuss (Master Arm aus); aus = alle Waffen schießen selbst |
| **Aim correction** | Knopf, wie auf dem Schiff (Zielkorrektur per Blick) |
| **KI Pause** | an = KI fährt nicht (steht); aus = KI fährt |
| **Nach Hause** | an = fährt zum Spawn-Punkt zurück und bleibt dort stehen |

### Karte (Monitor 3×3 links vom Sitz)
- Auf die Karte tippen: Dort kommt ein **Wegpunkt** hin. Bis zu 8 Wegpunkte, die KI fährt sie der Reihe nach im Kreis ab.
- Knopf **Löschen**: alle Wegpunkte weg. Ohne Wegpunkte patrouilliert die KI im Revier.
- **+ / −**: Zoom. **Revier**: Patrouille an/aus.

### Selbst fahren
Hinsetzen und **W/S/A/D** drücken: Du fährst. 2 s nach dem Loslassen übernimmt die KI wieder (wenn sie nicht auf
Pause steht). Waffen wie auf dem Schiff: **H5** wählt die Waffe für die Kamera, **Leertaste** = ein Schuss der
gewählten Waffe.

---

## 4. Was im Spiel zuerst geprüft werden muss (ehrlich: nichts davon ist getestet)

In dieser Reihenfolge, jeweils mit **KI Pause an** und **Waffen sperren an** anfangen:

1. **Lädt die Datei?** Der Editor zeigt den Panzer. Wenn nicht, bitte die Fehlermeldung aufschreiben.
2. **Räder an den Wellen?** Nach `raeder.py` sitzen 14 Räder an den Wellen.
3. **Antrieb:** Hinsetzen, W drücken.
   - Fahren alle Räder? Falls nicht, sitzt ein Motor falsch herum.
     Annahme: Die Kraft kommt unten aus dem Motor, so wie am Bugstrahlruder des Schiffs.
   - Fährt er bei W vorwärts? Die Richtung je Seite stellen die Eigenschaften „Rad Richtung links/rechts“
     im KI-Chip ein. Die KI lernt das auch selbst, wenn „Richtung lernen“ 1 ist.
4. **Laser:** Die Karte bzw. die KI zeigt Laser-Entfernungen. Bei 0 hängt ein Laser nicht richtig. Annahme: Strom und
   Ausgang sitzen am Laser-Block selbst.
5. **Türme:** wie auf dem Schiff (Test Rohre usw.). Die Richtungs-Eigenschaften sind die vom Schiff, weil die Türme
   genauso eingebaut sind.
6. **KI:** KI Pause aus, auf freiem Gelände. Fährt er los, weicht er aus, hält er vor Wasser?
7. **Waffen:** Waffen sperren aus, mit Gegnern.

---

## 5. Technik (für spätere Arbeit)

| Datei | Was |
|---|---|
| `tools/bau_landkreuzer.py` | baut die ganze Fahrzeugdatei neu (`python landkreuzer/tools/bau_landkreuzer.py`) |
| `tools/fz.py` | Fahrzeugdatei lesen/schreiben (Teile, Körper, Kabel) |
| `tools/build_mc.py` | Chip-Baukasten (Nachbau des fehlenden Originals; baut alle Schiffs-Chips byte-gleich nach, siehe `tools/test_build_mc.py`) |
| `tools/build_ki.py` | KI-Chip |
| `tools/raeder.py` | Räder kopieren |
| `tools/ansicht.py` | Bilder zeichnen (braucht matplotlib) |
| `tools/test_ki.py` | Prüfstand der Fahr-KI (Simulation, braucht lupa) |
| `lua/ki_fahren.lua`, `lua/ki_karte.lua`, `lua/ki_kleber.lua` | die drei Skripte im KI-Chip |

**Koordinaten** (Blöcke à 0,25 m): x rechts, y oben, z vorn. Boden des Fahrwerksraums y −4, Hauptboden y 1, Deck vorn
y 6, Mitte y 10, hinten y 9. Wellen-Stummel bei x ±15, y −3, z 35 / 20 / 5 / −10 / −25 / −40 / −55 (Mitte = geschätzter Schwerpunkt).

**Chips** liegen auf dem Hauptboden in der Mitte (y 2, z −29 … −17), Physik-Sensor bei (0, 2, −12), Batterien im
Fahrwerksraum.
