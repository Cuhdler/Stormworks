# Hinweise für Claude

- Projekt: Andres Stormworks-Schiff „Figet Marena“. Gesamtstand und alle Regeln: `SCHIFF_UEBERSICHT.md` (zuerst lesen).
- Spiel und Fahrzeugdatei liegen auf Andres PC. Dieses Repo ist der gemeinsame Speicher; `fahrzeug/` ist nur eine
  Kopie zum Lesen. Änderungen erreichen das Spiel erst, wenn Andre auf dem PC pullt und die `tools/` laufen lässt.
- Mitschriften (Übersicht, Checklisten, Pläne) nach jeder Arbeitssitzung aktualisieren und pushen.
- Antworten auf Deutsch, einfache Worte. Andre spielt allein, alles muss von einem Sitz aus bedienbar sein.
- Lua im Spiel: höchstens 8192 Zeichen je Skript, kein `select`, kein `table.unpack`, Eingänge nicht in `onDraw` lesen.
