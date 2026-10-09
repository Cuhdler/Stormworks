# Bauteile

## 1. Die Daten: `bauteile.json`

**Stand:** noch leer. Andre lässt einmal auf dem PC `python tools/bauteile_holen.py` laufen (findet Stormworks
über Steam, sonst `-d <...>\Stormworks\rom\data\definitions`), dann `wissen/bauteile/bauteile.json` committen und
pushen. Nach jedem Spiel-Update neu holen. Die Datei nie von Hand ändern.

Aufbau: ein Eintrag je Bauteil. Der Schlüssel ist der Datei-Name ohne `.xml`, genau so steht das Teil auch in der
Fahrzeugdatei (`<c d="...">`).

| Feld | Bedeutung |
|---|---|
| `name` | Name im Spiel (englisch) |
| `kategorie` | Kategorie-Nummer im Spiel-Menü |
| `masse` | Gewicht |
| `preis` | Preis |
| `flags`, `tags` | Merkmale aus der Spiel-Datei |
| `bloecke` | belegte Blöcke `[x, y, z]`, relativ zum Teil |
| `anschluesse` | Liste `{label, ein, typ, pos}`: `ein` 1 = Eingang, 0 = Ausgang; `typ` = Signal-Art (Tabelle in `wissen/microcontroller/README.md`); `pos` = Block relativ zum Teil |
| `kind` | Versatz des zweiten Körpers bei Gelenken (Pivot, Drehkranz …), sonst `null` |
| `sonst` | alle weiteren Attribute der Spiel-Datei |

Wo ein Anschluss im Fahrzeug liegt (spiegeln, drehen, verschieben): `wissen/fahrzeugdatei.md` Abschnitt 3.4.

## 2. Suchen

```
python tools/bauteil_suchen.py laser            alle Bauteile mit "laser" im Datei-Namen oder Namen
python tools/bauteil_suchen.py laser_distance_sensor --voll    ein Bauteil mit allen Angaben
```

## 3. Im Spiel gelernt

Wie sich einzelne Bauteile verhalten. Neue Erfahrungen hier eintragen (mit Datum), allgemeine Spielregeln in
`wissen/mechaniken/README.md`.

| Bauteil | Was wir wissen | Quelle |
|---|---|---|
| Laser Distance Sensor | Sieht **durch das Wasser bis zum Meeresboden** (Wellen und Wasseroberfläche zählen nicht). Ohne Treffer = 4000. | gemessen 08.10. |
| Laser-Pivot | Pivot in Umdrehungen (höchstens 0,125). Beim Bug-Laser der Figet Marena kippt „Pivot Y plus“ den Strahl nach unten. Mit falschem Vorzeichen sah der Autopilot im Hafen den Boden 36–57 m tief als „Hindernis“. | gemessen 08.10. |
| Camera Stabilized | Pivot/Pitch-Eingang = Drehtempo mit Totzone 0,1. | gemessen |
| Robotic Pivot | Signal 1 = 90°. | gemessen |
| Ruder | Signal 1 = 45°. | gemessen |
| Steuerflosse | Signal + = Vorderkante hoch, auch wenn gespiegelt eingebaut. | gemessen 02.10. |
| Drehkranz | Dreht gespiegelt eingebaut andersherum. | gemessen |
| Radar | Zählt gespiegelt eingebaut gespiegelt. | gemessen |
| Phalanx-Radar | Winkel ab Sockel; meldet nur, solange der Strahl über dem Ziel ist. | gemessen |
| Instrumentenblock | Elemente ohne `channel` schreiben alle auf Bool 1. | Datei/gemessen |
| Battle Cannon | Verschluss öffnet 79 Ticks; „Loaded“ ca. 98 Ticks nach dem Schließen. | gemessen |
| Munition | `property_ammo_damage`: 1 HE, 2 Fragmentation, 3 AP, 4 Incendiary. | Datei |
