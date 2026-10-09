# Spielmechaniken

Was wir über das Spiel selbst wissen, unabhängig vom Fahrzeug. Wie sich einzelne Bauteile verhalten, steht in
`wissen/bauteile/README.md`. Kennzeichen wie in `wissen/README.md`.

Weitere Dateien in diesem Ordner:
- `physik.md`: Schwerkraft, Luftwiderstand, Auftrieb, Dichtigkeit und Lecks, Flüssigkeiten und Gase, Flügel, Treibstoff
- `strom.md`: Batterien, Generatoren, Verbrauch, Stromausfall
- `funk.md`: Funk, Video, Reichweiten, Fernsteuerung

## Maße und Koordinaten

- 1 Block = 0,25 m. Positionen in der Fahrzeugdatei sind ganze Blöcke [S].
- Achsen im Fahrzeug: x links − / rechts +, y oben +, z vorn + / hinten −. Alle Körper (auch Türme, Gelenke) und
  alle Kabel benutzen dasselbe System [G] (siehe `wissen/fahrzeugdatei.md` Abschnitt 2).
- Welt: x = Ost, z = Nord, y = Höhe über dem Meer (= Karten-/GPS-Koordinaten) [G].
- Teile **ohne** `r`-Attribut haben die Drehung `0,0,1,-1,0,0,0,-1,0`, nicht die Grunddrehung. Aus den Kabeln aller
  Fahrzeuge bestimmt: erklärt 122 Teile, die Grunddrehung nur 4 [G 08.10.].
- Spiegel-Flag `t` wirkt lokal, **vor** der Drehung [G, 38 Kabel].

## Spiegeln

- Gespiegelte Teile (`t`-Attribut) können ihre Wirkrichtung umdrehen: Radare zählen gespiegelt, Drehkränze drehen
  andersherum [G, Figet Marena].
- Steuerflossen: Signal + heißt bei **allen** Vorderkante hoch, auch gespiegelt (Fahrtenschreiber 02.10.) [G].

## Zeit und Ticks

- Ein Tick ist ein Spiel-Schritt. Ohne Gefecht gemessen: 61 Ticks/s (Fahrtenschreiber 02.10.) [G].
- Im Gefecht fiel das Spiel auf ca. 21–37 Ticks/s. Zeiten in Skripten darum in Ticks zählen (= Spielzeit), nicht in
  echten Sekunden [G].

## Microcontroller und Lua

- Höchstens 8192 Zeichen je Lua-Skript [G].
- Eingänge in `onDraw` lesen gibt „draw error 202“. Eingänge nur in `onTick` lesen [G].
- Vollständige Liste der Lua-Befehle: `wissen/microcontroller/lua.md`.

## HTTP (Chip ↔ eigener PC)

- Höchstens eine Anfrage je Tick [G].
- Die Antwort braucht `Content-Length` [G].
- Eine Anfrage an einen Port, an dem niemand lauscht, blockiert die HTTP-Warteschlange des Spiels unter Windows
  2 s (127.0.0.1) bzw. 4,1 s (localhost). Darum nur an Ports senden, an denen ein Programm wartet [G 04.10.].

## Fahrzeuge laden und speichern

- Das Spiel löscht beim Laden **stumm** Kabel, die auf keinen passenden Anschluss zeigen [G].
- Beim Speichern schreibt der Editor die ganze Datei neu (z. B. fällt `offset="0"` weg) – Vergleiche daher inhaltlich [G].
- Speichert man im Editor auf einem älteren geladenen Stand, sind Datei-Änderungen dazwischen weg → nach jeder
  Änderung per Datei im Spiel **neu laden, nicht speichern** [G].

## Mehrspieler (Host und Mitspieler)

- **Lua-Skripte laufen auf jedem PC selbst, ihr innerer Zustand (Variablen) wird nicht abgeglichen.** Entwickler auf
  Geometa #22188 (Jan. 2024): die Engine synchronisiert selbst geschriebene Lua-Skripte nicht, „nicht praktikabel“;
  außerdem laden Mitspieler nicht alle Fahrzeuge (Bandbreite) – ihre Radare sehen ferne Ziele also gar nicht [W].
- Logik-Werte außerhalb von Lua (Anschlüsse, Composite) werden laut Wiki abgeglichen, das Bild auf Monitoren kann
  trotzdem verschieden sein [W]. Offener Wunsch an die Entwickler (Geometa #28174): Zustand von Fahrzeug-Lua speichern
  und im Mehrspieler abgleichen; bis dahin wichtigen Zustand in Logik außerhalb von Lua halten [W].
- Physik rechnet der Host und schickt sie an alle (Türme drehen sich bei Mitspielern richtig) [W/G].
- Figet Marena, 09.10. (Andre Host, Freund Mitspieler) [G]: Türme drehen richtig; Zielliste leer, Radar-Pings und
  Kamera-Zoom nur ab und zu; Schüsse und Explosionen sieht er nur ca. 10 %; Autopilot- und Abteile-Monitor richtig.
  Beim Host feuerten die Waffen (gleichzeitig im Schreiber: BC 182, AC 562, Flak 192/100 Schuss). Erklärung: Lage,
  Bildschirm und Geschütz-Chips rechnen beim Mitspieler selbst, ohne die Radar-Ziele des Hosts; was er ab und zu sieht,
  sind vermutlich abgeglichene Zwischenstände vom Host. Treffer zählen vermutlich nur beim Host [V].
- Folge für eigene Chips: alles, was Mitspieler sehen sollen, nur aus Werten berechnen, die jeder PC gleich hat
  (Sensoren am eigenen Fahrzeug, Sitz, Physik) – Radar-Ziele gehören nicht dazu.

## Ziele und Welt

- Zielhöhen (Radar/Laser): fahrende Schiffe ca. −2 m (Ausreißer bis +6), stehende Dinge im Wasser 3–6 m,
  Bodenziele 14–16 m; fahrende Schiffe 6–13 m/s [G].
- Weit entfernte Fahrzeuge werden evtl. nicht mehr simuliert → „Keep Active Block“ (`no_sleep`) [W], siehe `funk.md`.

## Offene Fragen

Hier sammeln, was wir noch nicht wissen und im Spiel prüfen wollen:

- Physik: wie viel Gewicht ein Block Rumpf trägt, Wasserwiderstand je Rumpfform (Grundlagen in `physik.md`, [W]).
- Antrieb: Motor-Kennlinien, Getriebe, Kupplung, Treibstoffverbrauch.
- Strom: Verbrauch der eigenen Fahrzeuge messen (Wiki-Werte in `strom.md`, [W]).
- Wetter, Wellen, Tageszeit und wie sie Sensoren beeinflussen.
- Schaden, Feuer, Wassereinbruch.
- Video- und Daten-Funk auf derselben Frequenz-Zahl: stören sie sich? (`funk.md`)
