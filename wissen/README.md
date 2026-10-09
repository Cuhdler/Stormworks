# Wissen über Stormworks – Inhaltsverzeichnis

Hier liegt alles **allgemeine** Wissen über Stormworks, das für jedes Fahrzeug gilt: Bauteile, Microcontroller,
Lua, Fahrzeugdatei, Physik, Strom, Funk und Spielmechaniken. Was nur ein bestimmtes Fahrzeug betrifft, steht beim
Fahrzeug (`SCHIFF_UEBERSICHT.md` für die Figet Marena, `landkreuzer/` für den KI-Landkreuzer).

Seit 09.10.2026 die **eine gemeinsame Wissensdatenbank** für alle Chats (PC und Cloud). Auf Andres PC liegt sie
unter `Dokumente\Rok\Main Cloude\stormworks_schiff\wissen\` (der frühere Ordner
`Main Cloude\stormworks_wissen` verweist nur noch hierher).

**Für Claude:** Bei jeder Frage zu Stormworks zuerst hier in der Tabelle nachsehen, dann die passende Datei lesen.
Alle Pfade gelten ab dem Repo-Ordner.

## Wo steht was?

| Frage | Datei |
|---|---|
| Welche Bauteile gibt es? Name, Datei-Name, Größe, Masse, Preis, Anschlüsse | `wissen/bauteile/INDEX.md` (Liste aller 759 Teile), Einzelheiten je Kategorie in `wissen/bauteile/<Kategorie>.md` |
| Ein Bauteil schnell finden | `python tools/bauteil_suchen.py <Wort>` (sucht in `wissen/bauteile/bauteile.json`) |
| Wie verhält sich ein Bauteil im Spiel (Sitz-Kanäle, Physik-Sensor, Laser, Liquid Meter, Türen …)? | `wissen/bauteile/README.md`, Abschnitt 3 „Im Spiel gelernt“ |
| Welche Bausteine gibt es im Microcontroller und wie stehen sie in der Datei? | `wissen/microcontroller/README.md` |
| Welche Signal-Arten gibt es (An/Aus, Zahl, Composite, Video …)? | `wissen/microcontroller/README.md`, Abschnitt 1 |
| Welche Lua-Befehle gibt es im Chip, was fehlt? Bildschirm, HTTP | `wissen/microcontroller/lua.md` (Liste) und `wissen/microcontroller/README.md` Abschnitt 5 (Kurzfassung) |
| Wie ist eine Fahrzeugdatei (`.xml`) aufgebaut, wie ändert man sie sicher? | `wissen/fahrzeugdatei.md` |
| Koordinaten, Drehung `r`, Spiegeln `t`, Monitore richtig herum | `wissen/fahrzeugdatei.md` Abschnitt 2–3 |
| Schwerkraft, Auftrieb, Dichtigkeit, Lecks, Flüssigkeiten, Flügel, Treibstoff | `wissen/mechaniken/physik.md` |
| Batterien, Generatoren, Verbrauch, Stromausfall | `wissen/mechaniken/strom.md` |
| Funk, Video, Reichweiten, Fernsteuerung | `wissen/mechaniken/funk.md` |
| Spielregeln: Ticks, HTTP, Spiegeln, Mehrspieler, Zielhöhen, offene Fragen | `wissen/mechaniken/README.md` |

## Ordner

```
wissen/
  README.md              dieses Inhaltsverzeichnis
  fahrzeugdatei.md       Aufbau der Fahrzeug-XML, sicher bearbeiten
  bauteile/
    README.md            Aufbau von bauteile.json, Suchen, Erfahrungen mit einzelnen Bauteilen
    INDEX.md             alle Bauteile in einer Tabelle (erzeugt)
    <Kategorie>.md       je Bauteil alle Anschlüsse und besonderen Werte (erzeugt)
    bauteile.json        dasselbe maschinenlesbar (erzeugt)
  microcontroller/
    README.md            Signal-Arten, Bausteine (Nummer -> Name), Composite, Lua-Kurzfassung
    lua.md               Lua im Chip: was es gibt und was nicht (im Spiel gemessen)
  mechaniken/
    README.md            Spielregeln (Ticks, HTTP, Spiegeln …), offene Fragen
    physik.md            Schwerkraft, Auftrieb, Dichtigkeit, Flüssigkeiten, Flügel, Treibstoff
    strom.md             Batterien, Generatoren, Verbrauch, Stromausfall
    funk.md              Funk, Video, Fernsteuerung
```

Die erzeugten Dateien kommen nur aus `tools/bauteile_holen.py`. Nach einem Spiel-Update auf dem PC neu laufen lassen.

## Quellen-Kennzeichen

Jede Aussage sagt, woher sie kommt:

| Zeichen | Bedeutung | Verlässlichkeit |
|---|---|---|
| **[S]** | aus den Spieldaten (`rom/data/definitions`) | genau (für diese Spielversion) |
| **[G]** | im Spiel gemessen, aus Logs oder an funktionierenden Fahrzeug-/Chip-Dateien belegt (mit Datum) | sicher |
| **[W]** | aus dem Wiki oder Forum, nicht selbst geprüft | wahrscheinlich, kann veraltet sein |
| **[V]** | Vermutung, Annahme | erst prüfen |

Vermutetes wird zu [G], sobald es im Spiel bestätigt ist.

## Einheiten (Kurzfassung)

- 1 Block = 0,25 m; 1 m = 4 Blöcke [S]. 1 Block Volumen = 15,625 L [W].
- Spiel-Masse „1“ = 10 kg (ein normaler Block) [W]. Schwerkraft 10 m/s² [W].
- 60 Ticks = 1 s (Lua `onTick`), im Gefecht fällt das Spiel auf 21–37 Ticks/s [G].
- Winkel in Chips meist in Umdrehungen (1 = 360°) [G].

## Weitere Quellen auf Andres PC

- Spieldaten: `E:\SteamLibrary\steamapps\common\Stormworks\rom\data\definitions`
- Fahrzeuge / Chips: `%APPDATA%\Stormworks\data\vehicles` bzw. `...\data\microprocessors`
- ältere Tipps: `Main Cloude\stormworks_ki_tipps.md` (neben dem Repo-Ordner, nur auf dem PC)
- Wiki: https://stormworks.fandom.com/wiki/Gameplay/Mechanics (Unterseiten Buoyancy, Electricity, Fluids, Fuel, Lift,
  Logic, Lua, Ropes, Trim, Wheels …). Blockt direkte Abrufe (HTTP 402), mit dem Browser lesen. Noch nicht
  ausgewertet: Logic, Lua, Ropes, Trim, Wheels, Center of Mass.

## Regeln für diese Ablage

1. **Quelle angeben** (Kennzeichen oben), bei Messungen mit Datum.
2. **Allgemeines hierher, Fahrzeug-Eigenes zum Fahrzeug.** Lernt Claude bei einem Fahrzeug etwas, das für alle gilt
   (z. B. wie ein Bauteil reagiert), kommt es hierher, und beim Fahrzeug steht nur ein Verweis.
3. **Erzeugte Daten nicht von Hand ändern.** `bauteile.json`, `INDEX.md` und die Kategorie-Dateien kommen nur aus
   `tools/bauteile_holen.py`.
4. **Neue Themen** bekommen eine eigene Datei im passenden Ordner und eine Zeile in der Tabelle oben.
5. **Nach jeder Arbeitssitzung** neue Erkenntnisse eintragen und pushen. Auf dem PC vorher `git pull`, damit
   Einträge aus Cloud-Chats nicht verloren gehen.
