# Microcontroller – Signale, Bausteine, Aufbau in der Datei

Lua im Chip steht extra in `wissen/microcontroller/lua.md`. Wie ein Chip in der Fahrzeugdatei steht (Anschlüsse,
Eigenschaften, Weltposition der Anschlüsse), steht ausführlich in `wissen/fahrzeugdatei.md` Abschnitt 3.3. Den
Baukasten zum Erzeugen von Chips per Python gibt es in `landkreuzer/tools/build_mc.py` (Beispiele: `tools/build_*.py`).

Quellen: *Datei* = aus Andres Fahrzeugdateien oder Werkzeugen, die damit im Spiel funktionieren; *vermutet* = noch
nicht im Spiel oder in einer Datei bestätigt.

## 1. Signal-Arten (`type` an Anschlüssen und Kabeln)

| type | Signal | Quelle |
|---|---|---|
| 0 (oder fehlt) | An/Aus | Datei |
| 1 | Zahl | Datei |
| 2 | Drehmoment (Antriebswelle) | vermutet |
| 3 | Wasser / Flüssigkeit | vermutet |
| 4 | Strom | Datei |
| 5 | Composite (32 Zahlen + 32 An/Aus auf einem Kabel) | Datei |
| 6 | Video | Datei |
| 7 | Ton | vermutet |
| 8 | Seil / Gurt | vermutet |

Anschluss-Richtung: `mode="1"` = Eingang, `mode` fehlt oder `0` = Ausgang. Prüfen lassen sich die vermuteten Zeilen,
sobald `wissen/bauteile/bauteile.json` da ist (Anschlüsse von Pumpen, Motoren, Lautsprechern, Winden ansehen).

## 2. Bausteine im Chip (`<c type="N">` in `<components>`)

| type | Baustein | Wichtige Angaben in `<object>` | Quelle |
|---|---|---|---|
| 10 | Funktion mit 3 Eingängen f(x,y,z) | `e="Formel"` (z. B. `max(x,y)`), Eingänge `in1`…`in3` | Datei (`tools/build_abteile.py`) |
| 29 | Composite lesen, An/Aus | `i` = Kanal ab 0 (fehlt = Kanal 1), Eingang `in1` = Composite | Datei |
| 31 | Composite lesen, Zahl | wie 29 | Datei |
| 34 | Eigenschaft Zahl (Wert im Editor einstellbar) | `n="Name"`, darin `<v text=".." value=".."/>` | Datei |
| 40 | Composite schreiben, Zahl | `count`, `offset` (Startkanal ab 0), `inc` = Composite rein, `in1`… = Werte | Datei |
| 41 | Composite schreiben, An/Aus | wie 40 | Datei |
| 53 | Composite-Umschalter | 3 Eingänge: A, B, Schalter (An/Aus) | vermutet (`tools/build_autopilot.py`) |
| 56 | Lua-Skript | `script="..."` (höchstens 8192 Zeichen) | Datei |
| 57 | Video-Umschalter | | Datei |

Jeder Baustein hat `id` (eindeutig im Chip) und `<pos x y/>` (Platz im Logik-Editor, fehlend = 0). Ein Eingang
zeigt mit `<inN component_id=".." node_index=".."/>` auf den Ausgang eines anderen Bausteins (`node_index` fehlt =
erster Ausgang).

**Noch unbekannt:** die Nummern aller anderen Bausteine (UND, ODER, NICHT, Rechnen, Vergleich, PID, Speicher,
Zähler, Verzögerung, Taster-Logik …). Am einfachsten zu holen: Andre baut im Spiel einen Test-Chip, in dem jeder
Baustein einmal vorkommt, und speichert ihn. Ein Werkzeug liest dann Nummer, Name und Angaben jedes Bausteins aus
und schreibt diese Tabelle voll.

## 3. Brücken zwischen Chip-Anschluss und Logik (`<components_bridge>`)

Jeder Anschluss des Chips hat innen einen Brücken-Baustein. Seine Nummer hängt von Signal-Art und Richtung ab
(Quelle: Datei, `landkreuzer/tools/build_mc.py`, `BRUECKE`):

| Signal | Eingang | Ausgang |
|---|---|---|
| An/Aus | 0 | 1 |
| Zahl | 2 | 3 |
| Composite | 4 | 5 |
| Video | 6 | 7 |

## 4. Merksätze

- Anschlüsse eines Chips beim Tauschen **nie umsortieren**, neue nur hinten anhängen, sonst passen die Kabel nicht.
- Je Anschluss genau ein `<slot/>` in `<logic_slots>`.
- Andre stellt Chip-Eigenschaften nicht im Editor um; neue Werte kommen als neue Chip-Version.
