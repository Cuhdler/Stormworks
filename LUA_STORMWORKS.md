# Lua in Stormworks – was geht und was nicht

**Stand:** 05.10.2026, im Spiel gemessen. Das Prüf-Fahrzeug „Lua Pruefer“ (`lua/pruefer.lua`,
`tools/build_pruefer.py`, Empfang `tools/pruefer_empfang.py`) hat im Microcontroller jeden vorhandenen Namen
aufgelistet, über 200 bekannte Lua-Namen einzeln abgefragt und 25 Versuche ausgeführt. Rohdaten:
`logs/lua_pruefer_20261005_203729.txt`.

Die Liste ist **vollständig**: Was hier unter „geht“ steht, ist alles, was es im Microcontroller gibt. Weitere Namen
gibt es nicht.

---

## 1. Kurzfassung

**Es gibt nur:** `pairs`, `ipairs`, `next`, `type`, `tostring`, `tonumber` und die Tabellen `math`, `string`, `table`,
`input`, `output`, `property`, `screen`, `map`, `async`, `debug` (nur `debug.log`).

**Es gibt nicht** (Aufruf = Absturz des Skripts):
`select`, `print`, `pcall`, `xpcall`, `error`, `assert`, `setmetatable`, `getmetatable`, `rawget`, `rawset`,
`rawequal`, `rawlen`, `unpack` (aber `table.unpack` geht!), `load`, `loadstring`, `dofile`, `loadfile`, `require`,
`collectgarbage`, `_G`, `_VERSION`, sowie die Bibliotheken `os`, `io`, `coroutine`, `utf8`, `package`.

**Lua-Version:** 5.3 oder neuer (es gibt Ganzzahlen und Kommazahlen getrennt, `math.type`, `string.pack`,
`table.move`). `_VERSION` selbst fehlt.

---

## 2. Grundregeln

| Regel | Was das heißt | Quelle |
|---|---|---|
| **8192 Zeichen** je Lua-Block | Kommentare, Leerzeichen und `local` zählen mit; unsere Bau-Werkzeuge verkleinern vorher | im Spiel bestätigt |
| `onTick()` | jeden Tick (60 je Sekunde; im Gefecht lief das Spiel nur mit 21–37 Ticks/s) | bestätigt |
| `onDraw()` | nur, wenn am Video-Ausgang ein Bildschirm hängt; nur hier zeichnen | bestätigt |
| **Eingänge nur in `onTick` lesen** | in `onDraw` gelesen gab es „draw error 202“ → Werte in `onTick` merken | im Projekt beobachtet |
| Composite | je 32 Zahlen- und 32 Bool-Kanäle (1–32) | bestätigt |
| **Fehler stoppen das Skript** | ohne `pcall` gibt es kein Abfangen: jeder Laufzeitfehler (z. B. Aufruf einer fehlenden Funktion, `nil` indizieren) hält das Skript an | gemessen |
| Umgebung | die Skript-Umgebung ist `_ENV` (gibt es); `_G` gibt es nicht | gemessen |

---

## 3. Stormworks-Befehle (alle vorhanden)

### Ein- und Ausgänge, Eigenschaften
| Befehl | Hinweis |
|---|---|
| `input.getNumber(i)`, `input.getBool(i)` | Kanal 1–32 |
| `output.setNumber(i, wert)`, `output.setBool(i, wert)` | |
| `property.getNumber("Name")`, `property.getBool("Name")`, `property.getText("Name")` | Name muss genau stimmen |

### Internet (nur zum eigenen PC)
| Befehl | Hinweis |
|---|---|
| `async.httpGet(port, "/pfad?...")` | geht nur an `localhost` |
| `function httpReply(port, anfrage, antwort)` | eigene Funktion; das Spiel ruft sie, wenn die Antwort da ist |

Im Projekt bestätigt: höchstens **eine Anfrage je Tick** (Rest in einer Warteschlange für alle Chips); die Antwort
des PC-Programms braucht **Content-Length**; ein Port **ohne lauschendes Programm blockiert** die Warteschlange 2–4 s;
Pakete bis ca. 3000 Zeichen gingen durch.

### Zeichnen (nur in `onDraw`)
`screen.setColor(r, g, b, [a])`, `screen.getWidth()`, `screen.getHeight()`, `screen.drawClear()`,
`screen.drawLine(x1, y1, x2, y2)`, `screen.drawCircle(x, y, r)`, `screen.drawCircleF(...)`,
`screen.drawRect(x, y, b, h)`, `screen.drawRectF(...)`, `screen.drawTriangle(x1, y1, x2, y2, x3, y3)`,
`screen.drawTriangleF(...)`, `screen.drawText(x, y, text)`, `screen.drawTextBox(x, y, b, h, text, [h_ausr], [v_ausr])`,
`screen.drawMap(x, y, zoom)`,
`screen.setMapColorOcean / Shallows / Land / Grass / Sand / Snow / Rock / Gravel(r, g, b, [a])`

### Karte
`map.screenToMap(...)`, `map.mapToScreen(...)`

### Sonstiges
| Befehl | Hinweis |
|---|---|
| `debug.log(text)` | geht (Ausgabe nur mit dem Windows-Programm DebugView sichtbar); sonst ist von `debug` nichts da |
| `print(...)` | **fehlt** – Aufruf stoppt das Skript |

---

## 4. Normales Lua

### Grundfunktionen
| geht | fehlt |
|---|---|
| `pairs`, `ipairs`, `next`, `type`, `tostring`, `tonumber` | `select`, `print`, `pcall`, `xpcall`, `error`, `assert`, `setmetatable`, `getmetatable`, `rawget`, `rawset`, `rawequal`, `rawlen`, `unpack`, `load`, `loadstring`, `dofile`, `loadfile`, `require`, `collectgarbage`, `_G`, `_VERSION` |

### math
| geht | fehlt |
|---|---|
| `abs`, `acos`, `asin`, `atan` (auch mit zwei Werten: `math.atan(y, x)`), `ceil`, `cos`, `deg`, `exp`, `floor`, `fmod`, `huge`, `log`, `max`, `maxinteger`, `min`, `mininteger`, `modf`, `pi`, `rad`, `random`, `randomseed`, `sin`, `sqrt`, `tan`, `tointeger`, `type`, `ult` | `atan2` (→ `math.atan(y, x)`), `pow` (→ `a^b`), `log10` (→ `math.log(x)/math.log(10)`), `cosh`, `sinh`, `tanh`, `frexp`, `ldexp` |

### string
| geht | fehlt |
|---|---|
| `byte`, `char`, `dump`, `find`, `format`, `gmatch`, `gsub`, `len`, `lower`, `match`, `pack`, `packsize`, `rep`, `reverse`, `sub`, `unpack`, `upper` | – |
| Schreibweise mit Doppelpunkt geht auch: `text:upper()`, `text:sub(1, 2)` | |

### table
| geht | fehlt |
|---|---|
| `concat`, `insert`, `move`, `pack`, `remove`, `sort`, `unpack` | `getn`, `maxn` |

### Bibliotheken, die es nicht gibt
`os` (Uhrzeit, Datum), `io` (Dateien), `coroutine`, `utf8`, `package`; von `debug` nur `debug.log`.
Für Zeit stattdessen Ticks in `onTick` zählen.

### Sprache
| Merkmal | Status |
|---|---|
| `local`, Funktionen, Tabellen, Schleifen, `if`, `..`, `#` | geht |
| Ganzzahlen / Kommazahlen getrennt (`math.type(3)` = integer, `math.type(3.0)` = float) | geht |
| `//` (Ganzzahl-Division), Bit-Operatoren `& | ~ << >>`, `goto` | gehören zu Lua 5.3, im Spiel nicht einzeln geprüft |

---

## 5. Was das für unsere Skripte heißt

- **Kein `select`, kein `unpack`:** Werte als Tabelle übergeben (wie unser Schreiber `LG(g, t, n)`) oder
  `table.unpack` nehmen.
- **Kein `print`:** zum Testen `debug.log` oder unseren Schreiber (HTTP an den PC) benutzen.
- **Kein `pcall`/`error`:** Fehler lassen sich nicht abfangen → vorher prüfen (`if t then ... end`, `t and t.x`).
- **Keine Metatabellen** (`setmetatable` fehlt): keine Klassen mit `__index`, stattdessen einfache Tabellen.
- Kurze Namen am Anfang sparen Zeichen: `N=input.getNumber B=input.getBool S=output.setNumber O=output.setBool
  P=property.getNumber`.
- Eigenschaften einmal beim ersten Tick lesen (`if not ini then ini=1 ... end`).
- Zu langes Skript: auf zwei Lua-Blöcke im selben Chip aufteilen (Daten über Composite weitergeben).
