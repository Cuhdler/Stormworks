# Figet Marena – Stormworks-Projekt

Mitschriften, Skripte und Werkzeuge für Andres Schiff „Figet Marena“ (Stormworks: Build and Rescue, DLC Search and
Destroy). Spiel und Fahrzeugdatei liegen auf Andres PC. Dieses Repo ist der gemeinsame Speicher, damit jede
Claude-Sitzung (auf dem PC oder in der Cloud) den aktuellen Stand kennt.

## Inhalt

| Datei / Ordner | Was | Status |
|---|---|---|
| `SCHIFF_UEBERSICHT.md` | Gesamtübersicht (Stand 04.10.2026, 22:56) | da |
| `CHECKLISTE.md`, `WAFFEN_PLAN.md`, `KONZEPT.md` | Details Antrieb, Waffen, Konzept | da |
| `LUA_STORMWORKS.md` | welche Lua-Funktionen es im Microcontroller gibt (im Spiel gemessen) | da |
| `lua/` | alle Chip-Skripte | da |
| `tools/` | Bau-, Einbau-, Prüfstand- und Logger-Programme | da |
| `fahrzeug/Figet Marena.xml` | Kopie der Fahrzeugdatei (Stand 05.10. 19:08, mit Raketen-Chip), nur zum Lesen; ohne Steam-Autorangaben | da |

`logs/`, `build/` und `backup/` werden nicht hochgeladen (groß bzw. erzeugt, siehe `.gitignore`). Einzelne Logs,
die Claude auswerten soll, mit `git add -f logs/...` dazunehmen.

## Arbeitsweise

1. **PC → GitHub:** Projektordner einmal hochladen (siehe unten), danach Änderungen vom PC immer pushen.
2. **Claude (Cloud)** liest das Repo, ändert Skripte, Werkzeuge und Mitschriften und pusht.
3. **GitHub → PC:** auf dem PC holen (pull), dann wie gewohnt bauen und einbauen
   (`tools/build_*.py --install`, `tools/*_update.py --schreiben`). Danach das Schiff **neu laden, ohne vorher zu
   speichern**.

Die Cloud-Sitzung kann das Spiel nicht starten, die Fahrzeugdatei auf dem PC nicht direkt ändern und keine Logs
über Port 8768 empfangen. Das läuft weiter auf dem PC.

## Projektordner hochladen (einmalig)

**Weg A – mit Claude Code auf dem PC:** dort sagen: „Lade den Ordner `stormworks_schiff` in das GitHub-Repo
`Cuhdler/Stormworks` hoch (ohne logs, build, backup) und lege eine Kopie von `Figet Marena.xml` unter `fahrzeug/` ab.“

**Weg B – mit GitHub Desktop:**
1. GitHub Desktop installieren und mit dem GitHub-Konto anmelden.
2. *File → Clone repository → Cuhdler/Stormworks*, z. B. nach `Documents\Rok\Main Cloude\stormworks_repo`.
3. Aus `stormworks_schiff` die Ordner `lua`, `tools` und alle `.md`-Dateien in den geklonten Ordner kopieren.
4. Ordner `fahrzeug` anlegen und eine Kopie von `%APPDATA%\Stormworks\data\vehicles\Figet Marena.xml` hineinlegen
   (GitHub nimmt Dateien bis 100 MB).
5. In GitHub Desktop eine kurze Beschreibung eintragen, *Commit*, dann *Push origin*.
