# Hinweise für Claude

- Projekt: Andres Stormworks-Schiff „Figet Marena“. Gesamtstand und alle Regeln: `SCHIFF_UEBERSICHT.md` (zuerst lesen).
- Spiel und Fahrzeugdatei liegen auf Andres PC. Dieses Repo ist der gemeinsame Speicher; `fahrzeug/` ist nur eine
  Kopie zum Lesen. Änderungen erreichen das Spiel erst, wenn Andre auf dem PC pullt und die `tools/` laufen lässt.
- Mitschriften (Übersicht, Checklisten, Pläne) nach jeder Arbeitssitzung aktualisieren und pushen.
- Antworten auf Deutsch, einfache Worte. Andre spielt allein, alles muss von einem Sitz aus bedienbar sein.
- Lua im Spiel (im Spiel gemessen, Liste in `LUA_STORMWORKS.md`): höchstens 8192 Zeichen je Skript; es fehlen u. a.
  `select`, `print`, `pcall`, `error`, `setmetatable`, `unpack`, `load`, `os`; `table.unpack` geht. Eingänge nicht in
  `onDraw` lesen.
- Raketensystem ist fertig (Andre): Raketen-Chip, seine Kabel und Teile bei eigenen Änderungen unverändert lassen.
- Zweites Projekt: **KI-Landkreuzer** (autonomer Panzer) in `landkreuzer/`, Stand und Regeln in `landkreuzer/LANDKREUZER.md`.
  Er wird komplett per `landkreuzer/tools/bau_landkreuzer.py` erzeugt (Teile/Chips aus der Schiffsdatei kopiert).
