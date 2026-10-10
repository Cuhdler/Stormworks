# Figet Marena – Stormworks-Projekt

Mitschriften, Skripte und Werkzeuge für Andres Schiff „Figet Marena“ (Stormworks: Build and Rescue, DLC Search and
Destroy). Spiel und Fahrzeugdatei liegen auf Andres PC. Dieses Repo ist der gemeinsame Speicher, damit jede
Claude-Sitzung (auf dem PC oder in der Cloud) den aktuellen Stand kennt.

## Inhalt

| Datei / Ordner | Was | Status |
|---|---|---|
| `SCHIFF_UEBERSICHT.md` | Gesamtübersicht (Stand 04.10.2026, 22:56) | da |
| `CHECKLISTE.md`, `WAFFEN_PLAN.md`, `KONZEPT.md` | Details Antrieb, Waffen, Konzept | da |
| `wissen/` | **Gemeinsame Stormworks-Wissensdatenbank** für alle Fahrzeuge und alle Chats: alle Bauteile, Microcontroller, Lua, Fahrzeugdatei, Physik, Strom, Funk, Spielmechaniken. Inhaltsverzeichnis `wissen/README.md` | da |
| `lua/` | alle Chip-Skripte | da |
| `sim/` | **Nachbau von Stormworks** (10.10.): lädt die echte Fahrzeugdatei und führt alle Chips Tick für Tick aus (Logik-Bausteine, Lua, Kabel zwischen Chips, Host + Mitspieler). Keine Physik. Anleitung `sim/README.md`, Prüfstand `python sim/test_sim.py` | da |
| `tools/` | Bau-, Einbau-, Prüfstand- und Logger-Programme | da |
| `fahrzeug/Figet Marena.xml` | Kopie der Fahrzeugdatei (Stand 10.10. 14:40, Schiff v3.4, Lage v3.4, Bildschirm v3.7), nur zum Lesen; ohne Steam-Autorangaben | da |
| `tools/bauteile_holen.py` → `wissen/bauteile/` | Alle 759 Bauteile des Spiels (Datei-Name, Gewicht, Größe, Blöcke, Anschlüsse mit Position und Beschreibung) als `INDEX.md`, Seiten je Kategorie und `bauteile.json`, aus `Stormworks\rom\data\definitions` auf Andres PC geholt; suchen mit `tools/bauteil_suchen.py` | da (Stand 09.10.2026) |
| `landkreuzer/` | **KI-Landkreuzer** (08./09.10.): autonomer Panzer aus Schiffsteilen, Fahr-KI (`KI_FAHREN.md`), Anleitung mit Schnellstart `landkreuzer/LANDKREUZER.md` | fertig gebaut, im Simulator geprüft, im Spiel noch ungetestet |

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
