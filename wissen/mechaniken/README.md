# Spielmechaniken

Was wir über das Spiel selbst wissen, unabhängig vom Fahrzeug. Wie sich einzelne Bauteile verhalten, steht in
`wissen/bauteile/README.md`. Jede Zeile nennt ihre Quelle; *gemessen* heißt im Spiel bestätigt.

## Maße und Koordinaten

- 1 Block = 0,25 m. Positionen in der Fahrzeugdatei sind ganze Blöcke. *(Datei)*
- Achsen im Fahrzeug: x links − / rechts +, y oben +, z vorn + / hinten −. Alle Körper (auch Türme, Gelenke) und
  alle Kabel benutzen dasselbe System. *(Datei, siehe `wissen/fahrzeugdatei.md` Abschnitt 2)*
- Teile **ohne** `r`-Attribut haben die Drehung `0,0,1,-1,0,0,0,-1,0`, nicht die Grunddrehung. Aus den Kabeln aller
  Fahrzeuge bestimmt: erklärt 122 Teile, die Grunddrehung nur 4. *(Datei)*
- Spiegel-Flag `t` wirkt lokal, **vor** der Drehung. *(Datei)*

## Spiegeln

- Gespiegelte Teile (`t`-Attribut) können ihre Wirkrichtung umdrehen: Radare zählen gespiegelt, Drehkränze drehen
  andersherum. *(gemessen, Figet Marena)*
- Steuerflossen: Signal + heißt bei **allen** Vorderkante hoch, auch gespiegelt (Fahrtenschreiber 02.10.).
  *(gemessen)*

## Zeit und Ticks

- Ein Tick ist ein Spiel-Schritt. Ohne Gefecht gemessen: 61 Ticks/s (Fahrtenschreiber 02.10.). *(gemessen)*
- Im Gefecht fiel das Spiel auf ca. 21–37 Ticks/s. Zeiten in Skripten darum in Ticks zählen (= Spielzeit), nicht in
  echten Sekunden. *(gemessen)*

## Microcontroller und Lua

- Höchstens 8192 Zeichen je Lua-Skript. *(gemessen)*
- Eingänge in `onDraw` lesen gibt „draw error 202“. Eingänge nur in `onTick` lesen. *(gemessen)*
- Vollständige Liste der Lua-Befehle: `wissen/microcontroller/lua.md`.

## HTTP (Chip ↔ eigener PC)

- Höchstens eine Anfrage je Tick. *(gemessen)*
- Die Antwort braucht `Content-Length`. *(gemessen)*
- Eine Anfrage an einen Port, an dem niemand lauscht, blockiert die HTTP-Warteschlange des Spiels unter Windows
  2 s (127.0.0.1) bzw. 4,1 s (localhost). Darum nur an Ports senden, an denen ein Programm wartet. *(gemessen 04.10.)*

## Ziele und Welt

- Zielhöhen (Radar/Laser): fahrende Schiffe ca. −2 m (Ausreißer bis +6), stehende Dinge im Wasser 3–6 m,
  Bodenziele 14–16 m; fahrende Schiffe 6–13 m/s. *(gemessen)*

## Offene Fragen

Hier sammeln, was wir noch nicht wissen und im Spiel prüfen wollen:

- Physik: Auftrieb, Wasserwiderstand, wie viel Gewicht ein Block Rumpf trägt.
- Antrieb: Motor-Kennlinien, Getriebe, Kupplung, Treibstoffverbrauch.
- Strom: Verbrauch und Erzeugung der wichtigsten Teile.
- Wetter, Wellen, Tageszeit und wie sie Sensoren beeinflussen.
- Schaden, Feuer, Wassereinbruch.
