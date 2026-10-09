# Funk, Video, Fernsteuerung

## Bauteile [S]

- **Radio RX Huge** (`rx_huge_v2`): Data Send / Data Recv (Composite), Audio Send/Recv, Frequency (Zahl),
  Transmit Mode (an = senden, aus = empfangen), Signal Strength (Zahl), Strom.
- **Radio Video Xmit** (`rx_video_x`): Video Send (Kamerabild rein), Frequency Send, Strom.
- **Radio Video Recv** (`rx_video_r`): Video Recv (Bild raus), Frequency Recv, Signal Strength, Strom.

## Reichweiten [W] (Wiki/Forum, ungeprüft)

- Antenne klein ~100 m, mittel ~1 km, groß ~4 km, riesig ~20 km; Video ~10–20 km.
- Reichweite = Sender + Empfänger, mal Batterie-Ladung (riesig + riesig ~40 km).
- Zahlen/an-aus gehen bis zur Grenze sauber, Ton und Bild werden vorher schlechter.

## Fernsteuerung (Figet Marena + small Jet, 08.10.) [G/V]

- Aufbau: Sitz → Chip → Funk senden (Frequenz A) → Funk empfangen im Fahrzeug → Chip; Rückkanal auf Frequenz B.
- Lebenszeichen: Schiff schickt einen Zähler, Fahrzeug schickt ihn zurück → beide Seiten erkennen Funkverlust;
  Fahrzeug fliegt bei Verlust ein Notprogramm.
- Video- und Daten-Funk mit derselben Frequenz-Zahl: wir nehmen an, dass sie sich nicht stören [V – im Spiel prüfen].
- Weit entfernte Fahrzeuge werden evtl. nicht mehr simuliert: **„Keep Active Block“** (`no_sleep`) ins Fahrzeug [W].
  Zusammen gespawnte Fahrzeuge trennen sich angeblich ab 1,5–3 km → Flugzeug getrennt spawnen [W].
