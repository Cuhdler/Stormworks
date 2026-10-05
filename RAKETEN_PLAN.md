# Figet Marena – Raketensystem: wie es ursprünglich funktionieren sollte

**Stand:** 04.10.2026 (Andres Speicherstand 22:56)
**Spiel:** Stormworks: Build and Rescue, DLC *Search and Destroy*. Andre spielt allein, alles muss vom Steuersitz
(0,17,−10) aus bedienbar sein.
**Positionen** in Blöcken, Bug bei +z.

Diese Datei beschreibt nur Andres Plan und die gebaute Hardware. Logik für das Raketensystem gibt es noch nicht.

---

## 1. Zweck

- 24 Raketen gegen **Schiffe und Landziele**, nicht gegen Luftziele.
- Bedienung über einen **eigenen Bildschirm** und einen **eigenen Startknopf** auf der Brücke.
- Die übrigen Waffen (Battle Cannon, Autokanone, 2 Flaks) laufen unabhängig davon weiter.

## 2. Radar

- **Mast-Radar 6** (Radar Phalanx) bei (5,36,−51), gespiegelt eingebaut, ist für die Raketen reserviert.
- Es dreht sich rundum und bringt **alle Ziele außer Luftzielen** auf den Raketen-Bildschirm.

## 3. Raketen-Bildschirm (Monitor 3×3 bei (−3,20,−10), Touchscreen)

- **Ansicht:** 2D von oben, das eigene Schiff in der Mitte.
- **Farben:** Seeziele **blau**, Bodenziele **grün**.
- **Sweep-Strich:** Ein drehender Strich zeigt, wohin das Radar gerade schaut.
- **Helligkeit:** Ein Kontakt leuchtet hell, wenn der Strich ihn gerade gefunden hat, und wird dann langsam dunkler,
  bis der Strich wieder darübergeht.
- **Kontakte bleiben:** Ein Kontakt verschwindet nicht, nur weil das Radar ihn ein paar Sekunden nicht sieht. Erst
  nach **12 s** ohne Ortung wird er gelöscht.

## 4. Bedienablauf

1. **Ziel antippen** auf dem Raketen-Bildschirm → das Ziel bekommt ein **rotes Quadrat**.
2. Das Raketen-Radar **lockt dieses Ziel fest** (Hardlock).
3. **Startknopf** (Lockable Button bei (−1,19,−8)) drücken. Er ist nur entsperrt, wenn
   - **Master Arm an** ist (Schalter im Instrumentenblock (−2,19,−8), Bool 1) **und**
   - ein Ziel gelockt ist.

   **Jedes Umschalten = eine Rakete.**
4. Eine Rakete startet und fliegt ins markierte Ziel.

## 5. Dachkamera

- Die Dachkamera (Camera Stabilized bei (0,33,−15)) soll auch auf das gewählte Raketenziel zeigen.
- **Die letzte Auswahl gewinnt:**
  - Ziel auf dem Raketen-Bildschirm gewählt → Kamera schaut aufs Raketenziel.
  - Waffe auf dem Hauptbildschirm bzw. Monitor 2×3 gewählt (oder Hotkey 5) → Kamera schaut wieder auf das Ziel
    dieser Waffe.

## 6. Raketen (gebaute Hardware)

- **24 Raketen** in 4 Reihen × 6 im Heck, senkrecht stehend (Spitze oben):
  - Reihen x −11, −4, 4, 11; die Reihen x −4 und 11 sind gespiegelt eingebaut.
  - Plätze z −112, −117, −122, −127, −132, −137.
- **Halterung je Rakete:** connector_hardpoint_a am Schiff (x −14/−1/1/14, y 0), connector_hardpoint_b an der
  Rakete (x −12/−3/3/12).
- **Aufbau je Rakete**, Beispiel x −11, z −112, von unten nach oben:

  | Höhe y | Teil |
  |---|---|
  | −8 | Düse Medium |
  | −5 | Rocket Fins Medium |
  | −2 | Treibsatz Medium |
  | 0 | Hardpoint B, Physik-Sensor (−11,0,−111), kleine Batterie (−11,0,−112) |
  | 1 | Microcontroller 3×3 bei (−12,1,−113) |
  | 2 und 7 | 8 kleine Steuerflossen |
  | 5 | Warhead Body Medium |
  | 9 | Raketen-Radar (radar_advanced_missile), schaut nach oben |

  Dazu Pyramiden und Keile als Verkleidung.
- **Raketen-Radar** in jeder Rakete: Reichweite ca. 5 km, Sweep Mode statisch, FOV X 0,04 und FOV Y 0,04 (an der
  Rakete x −11, z −112 schon so eingestellt).
- **Vorhandene Kabel je Rakete:** Batterie → Hardpoint B, → Physik-Sensor, → Rocket Fins (jeweils Strom).

## 7. Luken

- Später sollen die Raketen **aus dem Boden kommen**, mit Klappen, die sich für sie öffnen.
- Zum Testen erst einmal **ohne Luken**.

## 8. Stand am Schiff

- **Nicht umgesetzt.** Am Schiff wurde für die Raketen nichts verdrahtet:
  - Radar 6 hängt weiter am Chip „Lage“. Platz 5 der Lagezentrale wird nie vergeben, Radar 6 sucht bis dahin mit
    (38° hoch).
  - Die 24 Microcontroller in den Raketen haben nur ein Beispiel-Skript.
  - Monitor 3×3 und Startknopf haben keine Kabel.
- **Hilfe von außen:** fertige Microcontroller im Steam Workshop, Tutorials, Stormworks-Discord, r/Stormworks.
