# Hinweise für Claude

- **Allgemeines Stormworks-Wissen** (Bauteile, Microcontroller, Lua, Fahrzeugdatei, Spielmechaniken) liegt in
  `wissen/`. Inhaltsverzeichnis: `wissen/README.md`. Neue allgemeine Erkenntnisse dort eintragen, mit Quelle.
- Projekt: Andres Stormworks-Schiff „Figet Marena“. Gesamtstand und alle Regeln: `SCHIFF_UEBERSICHT.md` (zuerst lesen).
- Spiel und Fahrzeugdatei liegen auf Andres PC. Dieses Repo ist der gemeinsame Speicher; `fahrzeug/` ist nur eine
  Kopie zum Lesen. Änderungen erreichen das Spiel erst, wenn Andre auf dem PC pullt und die `tools/` laufen lässt.
- Chips testen: neben den `tools/test_*.py` gibt es den Nachbau `sim/` (ganze Chip-Ketten aus der Fahrzeugdatei,
  auch Host + Mitspieler); Anleitung `sim/README.md`.
- Mitschriften (Übersicht, Checklisten, Pläne) nach jeder Arbeitssitzung aktualisieren und pushen.
- Antworten auf Deutsch, einfache Worte. Andre spielt allein, alles muss von einem Sitz aus bedienbar sein.
- Lua im Spiel (im Spiel gemessen, Liste in `wissen/microcontroller/lua.md`): höchstens 8192 Zeichen je Skript; es fehlen u. a.
  `select`, `print`, `pcall`, `error`, `setmetatable`, `unpack`, `load`, `os`; `table.unpack` geht. Eingänge nicht in
  `onDraw` lesen.
- Raketen und Raketen-Chip sind seit 07.10. entfernt; an ihre Stelle kommt der ferngesteuerte Jet (nur Flug, Kamera,
  Aufklärung). Teile ohne r-Attribut haben die Drehung 0,0,1,-1,0,0,0,-1,0 (nicht die Grunddrehung).
- Zweites Projekt: **KI-Landkreuzer** (autonomer Panzer) in `landkreuzer/`, Stand und Regeln in `landkreuzer/LANDKREUZER.md`.
  Er wird komplett per `landkreuzer/tools/bau_landkreuzer.py` erzeugt (Teile/Chips aus der Schiffsdatei kopiert).
