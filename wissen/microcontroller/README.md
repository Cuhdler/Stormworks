# Microcontroller – Signale, Bausteine, Aufbau in der Datei

Lua im Chip: volle Liste in `wissen/microcontroller/lua.md`, Kurzfassung unten in Abschnitt 5. Wie ein Chip in der
Fahrzeugdatei steht (Anschlüsse, Eigenschaften, Weltposition der Anschlüsse), steht ausführlich in
`wissen/fahrzeugdatei.md` Abschnitt 3.3. Den Baukasten zum Erzeugen von Chips per Python gibt es in
`tools/build_mc.py` und `landkreuzer/tools/build_mc.py` (Beispiele: `tools/build_*.py`).

Die Bausteine im Chip stehen **nicht** in den Spieldaten. Die Typnummern stammen aus Andres und unseren Chips und
allen Chip-Dateien auf dem PC (Auswertung 08.10.). Kennzeichen wie in `wissen/README.md`.

## 1. Signal-Arten (`type` an Anschlüssen und Kabeln)

| type | Signal | Quelle |
|---|---|---|
| 0 (oder fehlt) | An/Aus | [S] |
| 1 | Zahl | [S] |
| 2 | Drehmoment / Welle (RPS) – keine Kabel, verbindet durch Berührung | [S] |
| 3 | Flüssigkeit / Gas (Rohre) – keine Kabel, verbindet durch Berührung | [S] |
| 4 | Strom | [S] |
| 5 | Composite (32 Zahlen + 32 An/Aus auf einem Kabel) | [S] |
| 6 | Video | [S] |
| 7 | Ton (Mikrofon, Lautsprecher, Funk) | [S] |
| 8 | Munitionsgurt / Seil | [S] |

Quelle [S] = in `wissen/bauteile/bauteile.json` an den Anschlüssen der Bauteile abgelesen (09.10.).
Anschluss-Richtung: `mode="1"` = Eingang, `mode` fehlt oder `0` = Ausgang.

## 2. Bausteine im Chip (`<c type="N"><object id=".." ...>` in `<components>`)

| type | Baustein | Eingänge / Werte | Quelle |
|---|---|---|---|
| 10 | Formel f(x,y,z) (Zahl) | `e="Formel"` (z. B. `max(x,y)`); in1 = x, in2 = y, in3 = z | [G] (`tools/build_abteile.py`) |
| 22 | Zahlen-Umschalter | in1 = Wert bei an, in2 = Wert bei aus, in3 = Schalter | [V] (aus Kabel-Auswertung) |
| 29 | Composite lesen, An/Aus | `i` = Kanal **ab 0** (fehlt = Kanal 1); in1 = Composite | [G] |
| 31 | Composite lesen, Zahl | wie 29 | [G] |
| 34 | Eigenschaft Zahl (Wert im Editor einstellbar) | `n="Name"`, darin `<v text=".." value=".."/>` | [G] |
| 40 | Composite schreiben, Zahl | `count`, `offset` (erster Kanal ab 0); `inc` = Grund-Composite, in1..inN = Werte | [G] |
| 41 | Composite schreiben, An/Aus | wie 40 | [G] |
| 53 | Composite-Umschalter | in1 = Composite bei an, in2 = bei aus, in3 = Schalter | [G] (Autopilot: Sitz durchreichen) |
| 56 | Lua-Skript | `script="..."` (höchstens 8192 Zeichen); in1 = Composite, in2 = Video; Ausgang 0 = Composite, 1 = Video | [G] |
| 57 | Video-Umschalter | in1 = Bild bei an, in2 = bei aus, in3 = Schalter | [G] |

Vermutet aus der Auswertung (Attribute passen, nicht geprüft) [V]: 15 Konstante Zahl (`n`), 19 Eigenschaft Schieber
(`min/max/int/v`), 20 Eigenschaft Auswahl (`items`), 23 PID (`kp/ki/kd`), 26 Zeitglied (`ct/dt`), 33 Eigenschaft
Schalter (`n/on/off`), 36 Formel mit 8 Eingängen (`e`), 37 Zähler (`min/max/r/i/m`), 45 Formel mit 1 Eingang (`e`),
46/47 Logik-Formel mit 4/8 Eingängen (`e`), 58 Eigenschaft Text (`n/v`).

Jeder Baustein hat `id` (eindeutig im Chip) und `<pos x y/>` (Platz im Logik-Editor, fehlend = 0). Ein Eingang
zeigt mit `<inN component_id=".." node_index=".."/>` auf den Ausgang eines anderen Bausteins (`node_index` fehlt =
erster Ausgang).

**Noch unbekannt:** die sicheren Nummern aller anderen Bausteine (UND, ODER, NICHT, Rechnen, Vergleich, PID,
Speicher, Zähler, Verzögerung, Taster-Logik …). Am einfachsten zu holen: Andre baut im Spiel einen Test-Chip, in dem
jeder Baustein einmal vorkommt, und speichert ihn. Ein Werkzeug liest dann Nummer, Name und Angaben jedes Bausteins
aus und schreibt diese Tabelle voll.

## 3. Brücken zwischen Chip-Anschluss und Logik (`<components_bridge>`)

Jeder Anschluss des Chips hat innen einen Brücken-Baustein. Seine Nummer hängt von Signal-Art und Richtung ab [G]
(`landkreuzer/tools/build_mc.py`, `BRUECKE`):

| Signal | Eingang | Ausgang |
|---|---|---|
| An/Aus | 0 | 1 |
| Zahl | 2 | 3 |
| Composite | 4 | 5 |
| Video | 6 | 7 |

## 4. Composite [G]

- 32 Zahlen + 32 An/Aus je Composite. Kanäle im Spiel ab 1, in der Datei (`i`, `offset`) ab 0.
- Über Funk (Radio RX Huge) geht das ganze Composite.
- Composite-Werte sind 32-Bit-Kommazahlen: ganze Zahlen bis 16 777 216 exakt (gepackte Werte daran ausrichten).

## 5. Lua im Chip – Kurzfassung [G]

Volle Liste (im Spiel gemessen 07.10.): `wissen/microcontroller/lua.md`. Das Wichtigste:

- **8192 Zeichen je Skript** (nicht 4096). Kommentare und Einrückung zählen mit → vor dem Einbau verkleinern.
- Es fehlen u. a. `select`, `print`, `pcall`, `error`, `setmetatable`, `unpack` (aber `table.unpack` geht), `load`,
  `os`, `io`, `coroutine`, `utf8`, `math.atan2` (→ `math.atan(y, x)`), `math.pow`, `math.log10`.
- Lua 5.3: Ganzzahlen und Kommazahlen getrennt, `//` ganzzahlig teilen.
- `onTick` 60× je Sekunde; **in `onDraw` keine Eingänge lesen** („draw error 202“) – Werte in `onTick` merken.
- `screen.*` zeichnet nur in `onDraw`; Schrift 4×5 Pixel + 1 Abstand (5 px je Zeichen), `drawText` kann nicht drehen.
- `screen.drawMap(x, y, zoom)` lässt sich nicht drehen (Nord oben); `map.screenToMap` / `map.mapToScreen` zum Umrechnen.
- `async.httpGet(port, text)`: höchstens eine Anfrage je Tick für das ganze Spiel; Antwort braucht Content-Length;
  **Ports ohne Lauscher blockieren die Warteschlange 2–4 s**.
- Lua-Block mit Video-Eingang: Ausgabe = Eingangsbild + Gezeichnetes darüber (Kamerabild mit Anzeige).

## 6. Merksätze

- Anschlüsse eines Chips beim Tauschen **nie umsortieren**, neue nur hinten anhängen, sonst passen die Kabel nicht.
- Je Anschluss genau ein `<slot/>` in `<logic_slots>`.
- Chip-Beschreibung höchstens 128 Zeichen.
- Andre stellt Chip-Eigenschaften nicht im Editor um; neue Werte kommen als neue Chip-Version.
- Arbeitsweise im Schiffs-Projekt: Chips aus Python bauen (`tools/build_*.py`, Klasse `MC`), mit lupa im Prüfstand
  testen (`tools/test_*.py`) und per Skript in die Fahrzeugdatei einsetzen (Sicherung, Probe, dann schreiben).
