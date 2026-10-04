# Schnellkreuzer – Konzept (Stand 2026-09-26)

Ein-Mann-Kriegsschiff: schnell, schwer unterzukriegen, alles von einem Sitz. Nur Search-and-Destroy-DLC.
Nachfolger des Swifter (Hover-Flugpanzer, zu empfindlich: ein Treffer am Jet = Absturz).

## Eckdaten

- **Größe:** 55 m × 10 m (220 × 40 Blöcke)
- **Rumpf:** Gleitrumpf (flacher, leicht V-förmiger Boden, vorn angehoben), wasserdichte Abteilungen
- **Antrieb (geändert):** zwei Diesel („Working ship engine“, 18 Zylinder 3×3, ZE-Regler), je einer pro Welle,
  getrennte Maschinenräume, Kupplung 3×3 → Welle → Giant Propeller. Jets verworfen (Andre).
- **Schiff:** „Figet Marena“ (%APPDATA%/Stormworks/data/vehicles/Figet Marena.xml): 56 × 9,75 m, Brücke mit
  Steuersitz (Helm), Radarturm mit 4 Phalanx + drehbarem Mast, 2 Giant Propeller, 2 Ruder auf Robotic Pivots,
  Bugstrahlruder (Azimuth Thruster + Elektromotor). Suchradar im Turm, Feuerleit-Radare an den Türmen.
- **Lenzen:** in jeder Abteilung `Fluid Pump` + `Fluid Pressure Sensor`, Chip schaltet automatisch
- **Trimm:** Steuerflossen (`Control Fin`) am Heck, Chip stellt den günstigsten Gleitwinkel ein

## Bewaffnung

| Platz | Waffe | Steuerung |
|---|---|---|
| vorn | **Bertha Cannon** (1 Rohr, Spreng-Mörsergranaten, Zeitzünder) | **manuell** wie beim Swifter: Monitor-Zielen, Kamera + Laser, Zoom, Flugbahn-Rechnung, Autolader |
| vorn | Heavy Autocannon, HE | automatisch, **nur markierte Ziele** |
| hinten | Heavy Autocannon, HE | automatisch, **nur markierte Ziele** |
| links | Flak: 2 × Heavy Autocannon, Splitter | automatisch per Radar, Rohre **abwechselnd**, Zeitzünder = Flugzeit zum Vorhaltepunkt |
| rechts | Flak: 2 × Heavy Autocannon, Splitter | wie links |

**Ziel markieren:** Mit Kamera + Laser des Hauptgeschützes auf ein Ziel schauen und eine Taste drücken → der Chip
merkt sich die Position, nimmt die passende Radar-Spur (für Tempo/Vorhalt) und gibt sie an die Auto-Türme.

**Zeitzünder (neu gegenüber Swifter):** Heavy Autocannon, Battle/Artillery/Bertha haben den Eingang `Fuse Timer`
(Sekunden, für HE und Splitter). Die Flugzeit kennt der Chip aus der Flugbahn-Rechnung → Splittergranate platzt
direkt am Flugzeug, muss nicht direkt treffen.

## Microcontroller (Aufteilung)

1. **Schiffsführung:** Autopilot (Kurs/Tempo/Wegpunkt), Jets (Gas, Temperatur-Schutz), Propeller-Steigung
   (wie ein Getriebe), Ruder, Trimmklappen, Lenzpumpen, Helm-Anzeige
2. **Hauptgeschütz (Bertha):** Swifter-Waffen-Logik, Ziel markieren
3. **Auto-Türme (HE):** Spur des markierten Ziels, Vorhalt, Feuer
4. **Flak:** Radar-Spuren (AARADAR vom Swifter), 2 Türme, Tandem-Feuer, Zeitzünder

## Unbekannt, im Spiel zu messen

- Tempo, das ein Jet über Welle und Verstellpropeller bringt (Drehzahl, beste Steigung)
- Ob der Gleitrumpf in Stormworks wirklich aufgleitet und wie viel das spart
- Flugbahn von Bertha und Heavy Autocannon (Mündungsgeschwindigkeit, Luftwiderstand) → Einschießen
- Rückstoß der Bertha auf den Rumpf

## Bauphasen

1. **Testboot:** einfacher Gleitrumpf, 1 Jet mit Welle an 1 Verstellpropeller → Tempo, Drehzahl, Temperatur messen
2. **Rumpf 55 × 10** mit Abteilungen, kompletter Antrieb, Schiffsführungs-Chip (Autopilot, Lenzen, Trimm)
3. **Bertha** manuell (Swifter-Code, Einschießen)
4. **Flak** (2 Türme, Radar, Zeitzünder)
5. **Auto-HE-Türme** mit Zielmarkierung
