# Wissen über Stormworks – Inhaltsverzeichnis

Hier liegt alles **allgemeine** Wissen über Stormworks, das für jedes Fahrzeug gilt: Bauteile, Microcontroller,
Lua, Fahrzeugdatei und Spielmechaniken. Was nur ein bestimmtes Fahrzeug betrifft, steht beim Fahrzeug
(`SCHIFF_UEBERSICHT.md` für die Figet Marena, `landkreuzer/` für den KI-Landkreuzer).

**Für Claude:** Bei jeder Frage zu Stormworks zuerst hier in der Tabelle nachsehen, dann die passende Datei lesen.
Alle Pfade gelten ab dem Repo-Ordner.

## Wo steht was?

| Frage | Datei |
|---|---|
| Welche Bauteile gibt es? Datei-Name, Gewicht, Größe, Anschlüsse eines Bauteils | `wissen/bauteile/README.md` (Erklärung) und `wissen/bauteile/bauteile.json` (Daten aus dem Spiel) |
| Ein Bauteil schnell finden | `python tools/bauteil_suchen.py <Wort>` |
| Wie verhält sich ein Bauteil im Spiel (Laser, Pivot, Kamera, Radar …)? | `wissen/bauteile/README.md`, Abschnitt „Im Spiel gelernt“ |
| Welche Bausteine gibt es im Microcontroller und wie stehen sie in der Datei? | `wissen/microcontroller/README.md` |
| Welche Signal-Arten gibt es (An/Aus, Zahl, Composite, Video …)? | `wissen/microcontroller/README.md`, Abschnitt 1 |
| Welche Lua-Befehle gibt es im Chip, was fehlt? | `wissen/microcontroller/lua.md` |
| Wie ist eine Fahrzeugdatei (`.xml`) aufgebaut, wie ändert man sie sicher? | `wissen/fahrzeugdatei.md` |
| Koordinaten, Drehung, Spiegeln von Teilen | `wissen/fahrzeugdatei.md` Abschnitt 2–3 und `wissen/mechaniken/README.md` |
| Spielmechaniken: Ticks, HTTP, Spiegeln, Wasser, Munition … | `wissen/mechaniken/README.md` |

## Ordner

```
wissen/
  README.md              dieses Inhaltsverzeichnis
  fahrzeugdatei.md       Aufbau der Fahrzeug-XML, sicher bearbeiten
  bauteile/
    README.md            Aufbau von bauteile.json, Suchen, Erfahrungen mit einzelnen Bauteilen
    bauteile.json        alle Bauteile des Spiels (erzeugt von tools/bauteile_holen.py, nicht von Hand ändern)
  microcontroller/
    README.md            Signal-Arten, Bausteine (Nummer -> Name), Aufbau eines Chips in der Datei
    lua.md               Lua im Chip: was es gibt und was nicht (im Spiel gemessen)
  mechaniken/
    README.md            Spielmechaniken, die wir kennen (mit Quelle)
```

## Regeln für diese Ablage

1. **Quelle angeben.** Jede Aussage sagt, woher sie kommt: *Spiel-Datei* (aus `rom/data/definitions` oder einer
   Fahrzeugdatei gelesen), *gemessen* (im Spiel getestet, mit Datum) oder *vermutet* (noch nicht geprüft).
   Vermutetes wird zu *gemessen*, sobald es im Spiel bestätigt ist.
2. **Allgemeines hierher, Fahrzeug-Eigenes zum Fahrzeug.** Lernt Claude bei einem Fahrzeug etwas, das für alle gilt
   (z. B. wie ein Bauteil reagiert), kommt es hierher, und beim Fahrzeug steht nur ein Verweis.
3. **Erzeugte Daten nicht von Hand ändern.** `bauteile.json` kommt nur aus `tools/bauteile_holen.py`. Neu holen,
   wenn das Spiel ein Update hatte.
4. **Neue Themen** bekommen eine eigene Datei im passenden Ordner und eine Zeile in der Tabelle oben.
5. **Nach jeder Arbeitssitzung** neue Erkenntnisse eintragen und pushen.
