# Figet Marena - Waffensystem: Plan (Stand 02.10.2026)

Andres Wunsch: jede Waffe arbeitet automatisch; man kann durch die Waffen durchschalten (oder keine bedienen).
Anti-Schiff-Waffe gewaehlt -> Zielen am Bildschirm (wie Swifter: Blick vom Mittelpunkt weg = Turm faehrt hin).
Flugabwehr -> zielt und verfolgt automatisch, man waehlt aus, welches Ziel gelockt wird, und kann am Bildschirm
leicht korrigieren. Ein-Mann-Bedienung vom Steuersitz.

Waffen (Andre, vorlaeufig):
- vorn: Turm mit 2 Battle Cannons (SCHON GEBAUT: Turret Ring Large, 2x gun_l mit Zufuehrung, 2 Robotic Pivots)
- vorn: 1 "Large Autocannon" gegen Schiffe (im Spiel: Heavy Autocannon? - offen)
- oben hinten Mitte: 1-2 Flak je Seite, Heavy Autocannon doppelt
- hinten: 1 "Large Autocannon" gegen Schiffe
- spaeter vielleicht Raketen / Marschflugkoerper

## Vorlage "Radar boat" (vehicles/Radar boat.xml)

Ein Chip (5x2), Phalanx-Radar, Kompass, Monitor 5x3 mit Touch:
- Tracker-Skript (8153 Zeichen!) macht aus den 8 Radar-Meldungen (Entfernung, Seite, Hoehe, Zeit seit Meldung)
  8 feste Zielzeilen ("Tracks"), die ihr Ziel behalten, bis es verloren ist; rechnet Annaeherungs-Tempo, Bedrohung
  (naeher als 1500 m und kommt mit mehr als 5 m/s), zeichnet einen schraeg gestellten Radarschirm.
- Touch: Ziel auf dem Schirm antippen = auswaehlen/locken, Knoepfe fuer Reichweite und Schraeglage, Seite "TGT" mit
  Zieltabelle (antippen = waehlen). Zweites Skript zeichnet die Tabelle (Entfernung, Peilung, Hoehe, CPA-Zeit).
- Ausgang: gewaehltes Ziel (Peilung, Entfernung, Hoehe, Annaeherung), Bedrohung.
- Lua-Grenze: 8192 Zeichen je Skript (Andre: war schon immer so; bis 02.10. faelschlich mit 4096 gerechnet).

Uebernehmen: Tracks mit fester Nummer, Antippen zum Locken, Zieltabelle, Bedrohungs-Erkennung.

## Aufbau: drei Schichten

1. Lagezentrale (ein Chip): alle Radare -> eine Zielliste
   - Such-Radare oben (2-4, z. B. Phalanx/Basic, drehend): 360 Grad, weit
   - Feuerleit-Radar je Geschuetz (Phalanx auf dem Turm, manueller Modus per Gimbal, wie Swifter-Flak): haelt das
     zugewiesene Ziel dauerhaft im Strahl -> genaue, lueckenlose Daten
   - jede Meldung mit Lage und Drehung ihres Radars + Physik-Sensor (Kurs, Nick, Roll) in Welt-Koordinaten
     umrechnen -> gleiche Ziele aus verschiedenen Radaren zusammenlegen
   - je Track: Position, Geschwindigkeit, Luft/See (Hoehe), Bedrohung, markiert ja/nein, welcher Waffe zugewiesen
   - Zuweisung: markiertes Ziel -> passende Waffe (See-Ziel -> Kanonen, Luft-Ziel -> Flak), sonst gefaehrlichstes
2. Bedienung (Touch-Monitor am Steuersitz + Tasten)
   - Radarschirm wie Radar boat, Ziel antippen = markieren / locken; Zieltabelle
   - Waffenauswahl durchschalten: AUS -> Battle Cannons -> AC vorn -> AC hinten -> Flak -> (Raketen)
   - Tasten (Steuersitz, frei sind H5, H6, Abzug): Abzug = Feuer gewaehlte Waffe, H5 = naechste Waffe,
     H6 = Ziel im Blick markieren (das Radar-Ziel, das der Blickrichtung am naechsten ist); W/S, A/D, Pfeile bleiben Fahren
   - Monitor fuer die Zielkamera der gewaehlten Waffe (Bildschirm-Zielen wie Swifter)
3. Geschuetz-Chips (einer je Turm, alle gleich gebaut, nur Eigenschaften anders: Waffe, Lage, Grenzen)
   - bekommen ihr Ziel von der Lagezentrale (Composite-Kabel), rechnen Vorhalt und Flugbahn (Swifter-Code:
     Mündungsgeschwindigkeit, Luftwiderstand, Schwerkraft, eigene Fahrt), richten Turm und Rohr, feuern
   - gegen Schlingern: Nick/Roll des Schiffs in die Rohr-Richtung einrechnen (der Turm steht auf einem schaukelnden Schiff)
   - Modi: AUTO (feuert selbst: Flak auf Luftziele im Sektor, Kanonen NUR auf markierte Ziele), GEFUEHRT (gewaehlte
     Waffe: Kanonen per Blick, Flak automatisch mit Blick-Korrektur), AUS
   - Sperr-Sektoren: nie in eigene Aufbauten/Tuerme schiessen (wie Swifter-Flak vorne)

Freund/Feind: das Radar unterscheidet nicht. Darum Kanonen nur auf markierte Ziele; Flak "nur markierte" oder
"frei" (alles in der Luft, was naeher kommt) - sonst trifft sie z. B. den eigenen Rescue Heli.

## Reihenfolge

1. Lagezentrale + Touch-Radarschirm mit 1-2 Such-Radaren: Ziele sehen, markieren (noch ohne Waffen)
2. Battle-Cannon-Turm vorn (steht schon): Bildschirm-Zielen + "folgt markiertem Ziel", Schlinger-Ausgleich
3. Flak hinten (Heavy AC doppelt) mit Radar auf dem Turm: automatisch + Blick-Korrektur (Swifter-Flak als Grundlage)
4. Anti-Schiff-Autokanonen vorn/hinten: gleicher Geschuetz-Chip wie 2/3
5. Durchschalten, Tastenbelegung, Munitionsanzeige, alles zusammen
6. Raketen / Marschflugkoerper (eigenes Vorhaben: Rakete mit eigenem Chip und Suchkopf)

Andre baut die Teile selbst (Tuerme, Radare, Kameras, Monitor), Claude schreibt die Chips und legt auf Wunsch die Kabel.

## Stand 03.10.2026

Gebaut von Andre (noch nicht verkabelt): vorn Turm Large mit 2 Battle Cannons + Radar (Basic) auf dem Turm; davor
Turm Medium mit 1 Heavy Autocannon + Radar (Basic); hinten Mitte 2 Tuerme Medium (x -10 / +10, z -105) mit je
2 Heavy Autocannons auf eigenen Robotic Pivots + Radar (Basic); am Mast 6 Radar (Phalanx); 10 Trommeln vorn, 48 hinten.
Munition gesetzt (tools/munition.py, Sicherung 'vor Munition'): Battle Cannon HE, Autokanone vorn Heavy+AP,
Flak Heavy+Fragmentation (property_ammo_damage im Spiel geprueft: 1 HE, 2 Frag, 3 AP, 4 Incendiary; property_ammo_type 7/8/9
Light/Rotary/Heavy).

Fertig (Bibliothek): "Figet Marena Flak L v1" und "... R v1" (4x4, je Flak-Turm): lua/flakradar.lua + lua/flak.lua
(Umbau der Swifter-Flak), Zeitzuender auf Flugzeit, Sperrprofil aus dem Fahrzeug (tools/sperrprofil.py: vorn ueber
den Mast 28-35 Grad, ueber den Nachbarturm 15-19 Grad), H6 Flak an/aus, 'Test Rohre'. Pruefstand tools/test_flak.py.
Offen fuer die Flak: Andre setzt 2 leere Microcontroller (4x4), dann Chips einsetzen + Kabel (inkl. Strom);
Turm-Radare in den manuellen Modus (m_sweep_mode 4 wie Swifter); Richtungen (Turm, Rohre) mit 'Test Rohre' pruefen.

## Stand 03.10.2026 abends: Lagezentrale eingebaut (Schritt 1)

Chips an der Rueckwand des Chip-Raums (z -59), eingebaut mit tools/kabel_lage.py (Sicherung 'vor Lagezentrale'):
- "Figet Marena Lage v1" (4x4, x -4..-1, y 9..6): 6 x lua/mastradar.lua (je ein Radar (Phalanx) am Mast, manueller
  Modus, kreist mit 0,25 U/s; Strahl-Hoehen 0/0/12/24/36/45 Grad, die zwei tiefen eine halbe Runde versetzt;
  Strahl m_fov 0,04 statt 0,02) + lua/lage.lua (8 Ziele T1-T8 mit festen Nummern in der Welt, Luft/See,
  Markierung, AUTO markiert Luftziele unter 3 km, Bedrohung unter 1,5 km und naeher kommend).
- "Figet Marena Bildschirm v1" (4x3, x 1..4, y 9..7): lua/bild.lua + 3 Video Switchboxes. Monitor 9x5 in drei
  Teilen: links 3D-Radar (Bug oben, Luftziele auf Strichen je nach Hoehe; Kopfzeile antippen = 1/2/4/8 km),
  Mitte Kamera der gewaehlten Waffe mit Fadenkreuz und Zustand (Flak: AUS/SUCHT/ZIEL/FEUER + km), rechts
  Zielliste. Ziel antippen = waehlen + markieren, nochmal = weg. Unten: Waffe < >, AUTO, BEDROHUNG.
  H5 = naechste Waffe (keine, Battle Cannon, AC vorn, Flak L, Flak R).
- Winkel ab Strahl oder ab Sockel erkennt MASTRADAR selbst (Meldung wandert beim Ueberstreichen mit oder nicht);
  was ein Radar herausfand, gibt die Lage an alle 6 zurueck. Pruefstand tools/test_lage.py (beide Arten, Radar
  behaelt alte Ziele oder nicht, gespiegeltes Radar 6, Bedienung).
- Strom: linke Batterie -> 6 Mast-Radare + Monitor, rechte -> Kameras BC und AC vorn.
Noch nicht: Waffen folgen der Auswahl (Flak 'Lage'-Eingang -> Flak v1.3), Geschuetz-Chips BC/AC vorn, Kamera-Zoom.

### 03.10. 19:4x: Lage v1.1, Schiff v3.3 (tools/lage_update.py, Sicherung 'vor Lage v1.1')
Andres erster Test: Bild gespiegelt, Helm verdeckt den Monitor, Ziele flackern, Ziele bis 22 km gesehen (Strahl 0,04).
- Monitor 9x5: r 1,0,0,0,0,-1,0,1,0 ohne t (wie die meisten Monitore im Spiel). Andre hatte ihn auf dem Kopf eingebaut
  und mit t 4 gespiegelt - Hoehe richtig, links/rechts vertauscht. Seine Konstante an 'Power Switch' (-5,6,-59) bleibt:
  der Monitor braucht das An-Signal.
- Helm (SHUD v2.5): nur eine Zeile ganz unten + HEISS/AUSFALL; H4 = alle Werte.
- Mast-Radare: Strahl 0,1, zwei Baender je 3 Radare (8 Grad: Radar 1-3, 38 Grad: Radar 4-6), Drittelrunde versetzt.
- LAGE v1.1: 'Radar Reichweite m' 10000; volle Liste: nur Ersatz fuer >3 s nicht gesehene oder fuer das entfernteste,
  wenn das neue deutlich naeher ist (vorher staendiger Platzwechsel = Flackern); Fangbereich/Zusammenlegen mit der
  Entfernung groesser, Hoehe zaehlt halb; Luftziel-Grenzen mit Entfernungs-Zugabe (weit weg ist die Hoehe ungenau).
- MASTRADAR v1.1: Strahl/Sockel-Erkennung per Mehrheit der Beobachtungen. BILD v1.1: See-Hoehe '-', Ziele hinter der
  Reichweite nur grauer Randpunkt.

### 03.10. ~20:30: Zuweisung, AUTO, Blick-Markieren, Waffenwahl 2x3, Flak folgt (tools/waffen_update.py, Sicherung 'vor Waffenwahl')
Andres Test: Bild richtig; im Hafen lagen viele Ziele uebereinander (nicht einzeln antippbar); Kamera auf dem Kopf;
Waffenwahl soll auf den 2x3-Monitor neben dem Sitz; Frage: Markieren per Blick, wie arbeitet AUTO (2 Schiffe -> je ein
Geschuetz eines; mehrere Flieger -> die Flaks nicht beide auf eines).
- BILD v1.2: Ziel antippen/H6-Blick = Ziel der gewaehlten Waffe (ohne Waffe: nur markieren). Im Radar uebereinander:
  an derselben Stelle nochmal tippen = naechstes. Reichweite 0,5-8 km. Zuweisung je Waffe (Hand-Ziel gilt immer;
  AUTO: markierte passende Ziele in Reichweite, zwei gleiche Waffen verschiedene Ziele, Flaks bevorzugen ihre Seite,
  Ziel bleibt solange es passt). Ausgang 'Bedienung': je Waffe Ziel + Ort, Feuer frei, Vorgabe da (Layout im Kopf).
- WAFFENWAHL v1 (neuer Chip 3x2, x -4..-2, y 5..4 an der Rueckwand): Monitor 2x3 zeigt Schiff von oben (Umriss aus
  dem Fahrzeug), Waffen als Kreise, Strich zum Ziel, antippen = waehlen, Ecke = AUTO. Keine Schrift (stuende quer).
- FLAK v1.3: schiesst nur auf die Vorgabe (eigene Luft-Spur am naechsten daran) mit 'Feuer frei'; H6 macht das nicht
  mehr (ist jetzt Ziel im Blick). Bildschirm-Anzeige: Flak-Kanal 18 gepackt.
- LAGE v1.2: 'Ziel vergessen s' 6 (abgeschossenes Ziel haelt die Waffe nicht 12 s fest).
- Kameras um die Blickachse gedreht (r -1,0,0,0,0,1,0,1,0), Flak-R-Kamera nicht mehr gespiegelt.
Offen: Geschuetz-Chips BC und AC vorn (bekommen ihr Ziel schon ueber 'Bedienung' Waffe 1/2), Freund-Kennung ausser
"von Hand entmarkiert", Kamera-Zoom.

### 03.10. ~21:xx: Halbautomatik nach Andres Vorschlag (tools/halbauto_update.py, Sicherung 'vor Halbautomatik')
Fehler davor: beide Bildschirm-Skripte lasen in onDraw Eingaenge -> 'draw error 202' (Pruefstand prueft das jetzt).
Andres System:
- Master Arm (Schalter am Armaturenbrett -> Waffenwahl-Chip 'Master Arm', NOCH NICHT GEBAUT): aus = keine Waffe schiesst.
- Alle Waffen suchen ihr Ziel selbst (jedes passende lebende Ziel in Reichweite ausser Freunden) und behalten es,
  solange es passt (Hardlock auch im Flak-Radar per Zielnummer, bis ein anderes Ziel zugewiesen wird).
- Flaks NIE auf dasselbe Ziel; nur ein Luftziel -> nur die Flak auf seiner Seite. Kanonen: verschiedene, wenn moeglich.
- Niemand im Sitz / keine Waffe gewaehlt: alle schiessen selbst (mit Master Arm). Waffe gewaehlt: die zielt und
  verfolgt selbst, schiesst nur mit Leertaste; die anderen selbst.
- Antippen/H6 mit gewaehlter Waffe = deren Ziel (dasselbe nochmal = sucht wieder selbst); ohne Waffe = Freund an/aus.
- 3D-Radar zoomt selbst (groesste Stufe 200 m..10 km, bei der alle Ziele >= 10 px auseinander), ferne Ziele als Pfeil
  am Rand (antippbar, uebereinander: nochmal tippen = naechstes).
Offen: Blick-Korrektur der gewaehlten Waffe (Abstand Blick - Fadenkreuz), bewegliche Ziel-Kamera fuer H6 (Andre baut?),
Geschuetz-Chips BC/AC vorn mit Turm-Radar-Hardlock.

### 03.10. ~22h: Lagezentrale v2, "simpler" (tools/lage2_update.py, Sicherung 'vor Lage v2')
Andres Vorgabe: ein Mast-Radar sucht, die anderen 5 halten je ein Ziel; neues Ziel nur, wenn naeher als das
entfernteste gehaltene (das Radar mit dem fernsten wechselt) -> hoechstens 5 Ziele. Waffen: naechstes zuerst, Wechsel
nur bei weniger als halb so weit (seltenes Wechseln). Geschuetz-Radar lockt das zugewiesene Ziel. Bildschirm: nichts
mehr antippen, rotes Quadrat = wird beschossen. Master Arm: Flip Switch 1 am Instrument Panel (-2,19,-8) -> Waffenwahl.
- MASTRADAR v2: Radar 1 sucht (Runden abwechselnd 8/38 Grad), Radar 2-6 Lock (Richtung + 'haelt' von LAGE auf
  Kanal 29/30 + Bool 11), meldet im Lock nur die Ortung an der Strahlmitte; frei: sucht mit.
- LAGE v2: 5 Plaetze = Radar 2-6, Kennung je Ziel (wechselt beim Verdraengen), Filter wie FLAKRADAR, 'Ziel
  vergessen s' 4. Ausgang: 1-15 Ziele, 16-20 Kennungen, 21-30 Lock-Richtungen, 31 Kurs, 32 Hoehe.
- BILD v2: nur Anzeige; Zuweisung wie oben, Flaks nie dasselbe (ein Ziel: Flak seiner Seite), Kanonen verschiedene
  wenn moeglich (eines: beide); Master Arm, Leertaste fuer die gewaehlte Waffe (H5 / Monitor 2x3).
- Weg: Antippen, Freund, H6-Blick, Touch des grossen Monitors (Kabel bleibt, unbenutzt).

### 03.10. ~22:30: Vorzeichen gespiegelter Radare (tools/vorzeichen_update.py, Sicherung 'vor Vorzeichen')
Andres Test: Flak L traf einen Heli mehrmals punktgenau; Flak R schoss auf 'Geister' und weit vorbei. Einziger
ungeprüfter Unterschied: Flak R 'AA Radar Richtung' -1 (von mir geraten, Radar gespiegelt t 1). Pruefstand mit falsch
zaehlendem Radar: wenige Schuss, alle 300-400 m daneben - passt. -> Flak R +1, Mast-Radar 6 (auch t 1) RS +1:
gespiegelte Radare zaehlen offenbar NICHT gespiegelt (anders als der gespiegelte Drehkranz, der dreht andersherum).
FLAK v1.5: Sicherung - eigene Spur 2 s weiter als 300 m + 15 % neben der Vorgabe -> loslassen, neu an der Vorgabe.
Andre hat die Turm-Radare der Geschuetze (BC, AC, Flak L/R) selbst auf m_fov 0.05 gestellt - Pruefstand ok damit.

### 03.10. ~23h: Lage v2.2 - Plaetze nach Art (tools/lage22_update.py, Sicherung 'vor Lage v2.2')
Andre: 5 Schiffe gelockt, Helis daneben ignoriert -> Vorschlag 2 Locks Luft, 2 See, 1 spaeter Raketen. Dazu: "Ziel 2
teleportierte und wechselte den Status".
- LAGE v2.2: Platz 1-2 Luft (Radar 2/3), 3-4 See (Radar 4/5), 5 frei (Radar 6 sucht bis zu den Raketen hoch mit,
  Radar 1 flach). Topf (bis 6 Kandidaten, unsichtbar) bis die Art feststeht (See erst nach gemessenem Tempo; einmal
  Luft bleibt Luft); naeher als 90 % des ferneren -> verdraengt es (das kommt in den Topf). Haltendes Radar fuehrt nur
  sein eigenes Ziel nach, enger Fangbereich mit voller Hoehe (vorher hing sich ein fremdes Objekt im breiten Strahl an).
- BILD v2.2: Ziele ueber die Kennung behalten; Kanonen verteilen sich, wenn beide auf einem sind und es ein zweites
  gibt; leere Listenplaetze zeigen ihre Art (L/L/S/S/R).
- Pruefstand: test_plaetze (5 Schiffe + Helis, tiefer schneller Flieger), test_springen (Mast verdeckt den Heli, Schiff
  ohne Platz darunter; alte v2.1 verliert dort den Heli an das Schiff = Andres Bild).

### 03.10. ~23:15: Waffen-Schreiber (Lage v2.3, Bild v2.3, Flak v1.6; tools/lage22_update.py, Sicherung 'vor Schreiber')
Andre: Heli rechts, linke Flak schwenkte nach links und zurueck, rechte rührte sich nicht -> Verdacht: Lage sieht die
Seite spiegelverkehrt (Phalanx-Zaehlrichtung nie geprueft). Statt raten: lua/schreiber.lua in allen Chips (15
Messstellen, 'Schreiber Port' 8768, 'Schreiber Takt' 3) -> tools/waffen_logger.py -> logs/waffen_<Zeit>/<q>.csv.
Messstellen: r1..r6 Mast-Radar roh (+ Gimbal-Befehl 31/32, Bool 12-14), le/la Lage ein/aus, ba Bedienung,
fLe/fRe Flak-Radar ein (roh + Turm + Physik + Vorgabe), fLr/fRr Flak-Radar aus, fLf/fRf Feuerleitung aus.
Ende-zu-Ende geprueft (Skript -> HTTP -> CSV). Naechstes: Andres Log auswerten (Seite des Helis in r*/le/la).

### 03.10. ~23:30: erster Log ausgewertet -> Lage v2.4 (Sicherung 'vor Lage v2.4')
Log logs/waffen_20261003_221836: Kette funktioniert (Flak L fand die Vorgabe genau, Turm drehte richtig). Fehler:
zwei STEHENDE Dinge im Hafen (190 m / 15 m hoch, 226 m / 37 m) hielten beide Luft-Plaetze, die Helis dahinter (Flak R
sah einen in 1,1 km / ~120 m, naeher kommend) blieben draussen; ein Ding 40 m neben dem Schiff auf einem See-Platz.
Phalanx-Seitenwinkel stimmt (keine Spiegelung).
- LAGE v2.4: 'bewegt' = seit der ersten Ortung > 25 m + 1 % der Entfernung weg (verrauschtes Tempo reicht nicht);
  stehende zaehlen beim Platz-Vergleich 5-fach so weit; Luft erst nach zweiter Ortung (sofort nur ueber 'Luft immer ab
  m' 120); > 45 m/s = Luft; 'Mindestabstand m' 100. Ausgang Bool 15+k bewegt.
- BILD v2.4: Waffen nehmen nur bewegte Ziele; stehende grau.
- Schreiber: PC-Antwort ohne Content-Length -> Spiel wartete vergeblich, nur alle 2 s ein Paket. Behoben.
- 03.10. ~23:40 LAGE/BILD v2.5 (Andre: Helis langsam, stehen in der Luft, kommen naeher als 100 m): 'bewegt' ab 15 m +
  0,5 % (bleibt - heranfliegen und dann stehen = weiter Ziel), 'Mindestabstand m' 30, Kanonen erst ab 150 m, Flaks ohne.

### 03.10. ~23:55: Lage v2.6, Vorzeichen zurueck (Sicherung 'vor Lage v2.6')
Andres Bild: beide Flak-Tuerme zielten aufeinander. Log logs/waffen_20261003_222924: Flak R meldete ein Objekt bei
106 Grad (82 m), das die Lage bei 255 Grad sieht; Mast-Radar 2 und 6 sahen dasselbe Objekt (250 m, 33 Grad) bei +150 /
-150 Grad -> gespiegelte Radare ZAEHLEN gespiegelt, meine Umstellung auf +1 (vorzeichen_update) war FALSCH. Mit +1
erzeugte Radar 6 Geister (Heli rechts bei 142 Grad auch links bei 220 = id18), Flak R bekam den Geist -> zielte ueber
das Deck. Zurueck: Mast-Radar 6 RS -1, Flak R 'AA Radar Richtung' -1. Flak L fand ihre Vorgaben (1,3 km / 450 m) genau.
- LAGE v2.6: Fangbereich bei unbekanntem Tempo 120 m/s (max 250 m), sonst max 200 m; Hoehe voll bei Luft/ueber 20 m;
  seltene Ortung, die das Tempo um > 50 m/s aendern wuerde, gehoert nicht dazu (gegen Platz-Springen).
- Offen: Turm-Radare (Gimbal max 45 Grad, Strahl 0,05) sehen Helis ueber ~54 Grad nicht (Heli in 85-170 m, 150 m hoch).

### 04.10. ~01:25: Flaks geben ab (Lage v2.7, Bild v2.7, Flak v1.7; tools/lage22_update.py, Sicherung 'vor Waffen v2.7')
Andre: Flaks stehen in Ruhestellung, Radar dreht nicht, nichts passiert, obwohl ein Heli da ist. Log
logs/waffen_20261003_222924 (nach Neustart): drei Ursachen.
1. Flak L bekam Lage-Ziel #8 (300 m), fing aber ein STEHENDES Ding 133 m daneben (Fangbereich war 150 m + 5 %) und
   liess es per Hardlock nicht los, auch als ihr Heli #17 (190 m) zugewiesen wurde (Sicherung erst ab 300 m + 15 %).
2. Flak R bekam #6 - ein Ding auf dem Wasser (3-7 m), das 'Luft' blieb (Luft war fuer immer, nach Sprung von einem
   37 m hohen Ding). Die Flak nimmt nur Spuren ueber 'AA Mindesthoehe m' -> fand nie etwas, Strahl starrte auf die
   Vorgabe (deshalb "dreht nicht mehr"), Turm in Ruhestellung (dreht nur mit Spur).
3. Keine Waffe gab ein Ziel je ab, das sie nicht fand/nicht beschiessen durfte.
- FLAK v1.7: Fangbereich 40 m + 10 %, Hoehe voll; loslassen bei > 60 m + 20 % fuer 1 s; Zustand 4 'zu flach' (Ziel
  unter dem Sperrprofil). Test 11 (Hafen: Vorgabe Heli 250 m, Ding 130 m daneben) ok.
- LAGE v2.7: 'Luft' bleibt nur ueber 10 m; jeder Platz mit falscher Art zieht um (nicht nur See->Luft).
- BILD v2.7: Flak meldet 4 s 'sucht'/'zu flach' fuer dasselbe Ziel -> 20 s fuer sie gesperrt, die andere Flak darf es
  (bei nur einem Luftziel), sie selbst nimmt ein anderes oder keins. Anzeige 'ZU FLACH'.
- Tests: test_lage + 'Flak gibt ab', 'Flak zu flach', 'Luftziel geht aufs Wasser' ok; test_flak alles ok.
- Andre hatte vorher die Flak-Radar-FOV geaendert (L 0.25 x 0.04, R 0.24 x 0.04) - bleibt.
- Tests laufen im Scratchpad-venv (lupa, numpy); System-Python hat kein lupa.

### 04.10. ~08:05: Bild v2.8 - Sperrprofile im Bildschirm (Sicherung 'vor Bild v2.8')
Andre: "Flak R schoss rechts, gab auf, ignorierte den Heli, wechselte nach links und starrte 10 s". Log
logs/waffen_20261004_074902 (ganzer Test, 46 s Spielzeit): Heli #2 rechts (108 Grad, 1,3 km, 190 m) - Flak R schoss
darauf (70 Schuss); Heli #1 genau voraus (356 Grad, 1000 -> 480 m, 110 m hoch). Flak L meldete fuer #1 'zu flach'
(gab nach 4 s ab, richtig). Bei Tick ~2600 kam #1 unter die halbe Entfernung von #2 -> 50-%-Regel: Flak R wechselte
auf #1, Flak L bekam #2 - beide unerreichbar (hintere Tuerme: nach vorn erst ab ~30 Grad, quer uebers Schiff ab ~19).
- BILD v2.8: kennt beide Sperrprofile (build_lage.bild_flak setzt sie wie bei den Flak-Chips ein, dazu Turm-Lage zum
  Physik-Sensor (0,27,-38): rechts 2,5 m, vorn -16,75 m, hoch -2,25 m, tiefster Winkel 3 Grad); passt() gibt einer Flak
  nur Ziele mit Hoehenwinkel +1 Grad ueber dem Profil. Unerreichbare Luftziele dunkelorange.
- Test 'Sperrprofil: Heli voraus' (Log nachgestellt) ok; alle Tests ok.
- Beobachtung: Spiel lief im Log mit ~21 Ticks/s; Schreiber-Pakete je Quelle nur alle ~120 Ticks (httpReply kommt nicht).

### 04.10. ~08:20: Schreiber v2 (Lage v2.8, Bild v2.9, Flak v1.8; Sicherung 'vor Schreiber v2')
Andre: "der Log muss dir ALLES sagen, was im Code passiert und was das Schiff macht, sonst ist es ein Ratespiel".
Befund alter Schreiber: 15 Abgreif-Skripte am selben Port warteten je auf eine Antwort, die kaum kam (Fahrtenschreiber
allein auf 8766 lief am 01.10. tadellos) -> je Quelle nur 1 Paket / 120 Ticks, ~12 % der Zeit; nur Kabelwerte.
Stormworks-Wiki: 1 HTTP-Anfrage je Tick, weitere in eine Warteschlange.
- Schreiber steckt jetzt IN den Skripten (Kopf LG/LF, in allen 5 Waffen-Skripten gleich): je Tick eine Zeile mit
  inneren Werten (Spuren, Fangabstaende, Loslass-Zaehler, Sperren, erreichbar je Flak, Ortungs-Ergebnis je Radar ...).
- Fester Sende-Takt ohne Warten auf Antwort, versetzt (build_lage.TAKT): la 0, ba 1, fLr 2+10, fLf 3, fRr 4+12, fRf 5,
  r1-r6 6,7,8,9,11,13 von 16 Ticks -> nie zwei Anfragen in einem Tick. Paketnummer + verworfene Zeilen gehen mit.
- 'Schreiber Zeichen' 3000 (laengeres Paket: aelteste Zeilen weg, gezaehlt). Pruefstand: Mast-Radar bis 2600 Zeichen.
- PC: tools/waffen_logger.py v2 (CSV je Datenstrom mit Spaltennamen aus tools/schreiber_spalten.py, empfang.csv mit
  Ankunftszeit/Paketnummer/Laenge). Lesen: schreiber_spalten.lade(ordner, "fLr").
- Alte Abgreif-Skripte (lua/schreiber.lua) aus allen Chips entfernt.
- Offen: ob URLs ueber ~1000 Zeichen im Spiel durchgehen (Fahrtenschreiber hatte ~1000) - empfang.csv zeigt es.
- 04.10. ~08:26 FIX: Andre bekam "73: attempt to call a nil value (global 'select')" - Stormworks-Lua hat kein
  select (und vermutlich kein table.unpack). LG(g,t,n) nimmt jetzt eine Tabelle; Bild nutzt string.byte statt :byte.
  Pruefstaende (test_schiff.sperren, auch test_lage) entfernen select/unpack/load/require/os/io/... vor dem Laden.
  Sicherung 'vor select-Fix'.

### 04.10. ~08:42: Schreiber v2 - Stau behoben (Sicherung 'vor Schreiber-Antwort', tools/schreiber2_update.py)
Test 08:26-08:31: alle Pakete kamen an (keine Nummer fehlte), aber in Schueben von 40 (1 je Tick) mit ~8,2 s Pausen,
im Mittel 3 Pakete/s - der Log hinkte nach; beim Beenden waren erst 1218 Ticks (~20 s) da, Andres Moment fehlte.
Gemessen: Verbindung zu einem Port ohne Lauscher dauert unter Windows 2 s (127.0.0.1) bzw. 4,1 s (localhost).
Schiffsfuehrung und Flossen schickten ihren Fahrtenschreiber an 8766/8767 (niemand lauschte) -> je Anfrage ~4 s
Blockade der HTTP-Warteschlange des Spiels (2 x 4,1 = die 8,2-s-Pausen). PC-Empfaenger antwortet in 1-2 ms.
Fahrtenschreiber allein (02.10.): 15,4 Anfragen/s bei 61 Ticks/s, 100 % der Ticks.
- Schiffsfuehrung/Flossen: Eigenschaft 'Log Port' -> 0 (zurueck: 8766/8767 + tools/logger.py).
- Waffen-Skripte: senden erst nach der Antwort aufs letzte Paket (max 300 Ticks warten), fruehestens LT Ticks danach,
  erstes Paket bei LO+1; Antwortzeit in Ticks geht als w mit (empfang.csv: antwort_ticks).
- waffen_logger: request_queue_size 64 (Python-Standard 5).
- Im Log 08:26 (erste 20 s): Flak R hatte Heli #1 (1 km), verlor ihn, als ein 'Luft, bewegt'-Ding 303 m / 15 m hoch
  hinten (#7) den Luft-Platz nahm (erreicht keine Flak: zu flach); Flak L verfolgte #5 (440 m hoch).

### 04.10. ~09:00: Lage v2.9 - falsches Tempo im Hafen (Sicherung 'vor Lage v2.9')
Log logs/waffen_20261004_084207 (kein Heli, Hafen, Master Arm aus; Uebertragung einwandfrei: Antwort 2 Ticks, kein
Paket fehlt; Spiel lief ~31 Ticks/s; Mast-Radar-Pakete am 3000-Zeichen-Rand, r2-r5 verwarfen 13-25 % der Zeilen):
beide Luft-Plaetze den ganzen Test von stehenden Dingen belegt (#9 190 m/175 Grad/15 m, #5 300 m/166 Grad/15 m, 'Luft,
bewegt'); die Flaks wurden abwechselnd darauf gesetzt (zu flach -> gesperrt -> neu). Ursache: im Topf ordnete das
Such-Radar zwei Dinge einer Spur zu -> Tempo 51/64 m/s -> 'U>5 und >45 m/s' = Luft, Verschiebung = bewegt (beides
klebt); das haltende Radar zielte dem Tempo nach (Lock-Richtung = Ort + Tempo * Zeit) und fand #4/#5 nie wieder
(alter bis 240). Auch die "ignorierten" Helis der Tests davor passen dazu (Luft-Plaetze von solchen Dingen belegt).
- LAGE v2.9: Tempo zaehlt fuer 'Luft' erst nach 60 dichten Ortungen des haltenden Radars (c) oder - solange noch nicht
  dicht gemessen - nach 3 seltenen Ortungen mit auf 15 m/s passendem Tempo (k); 'bewegt' = seit der 30. dichten Ortung
  > 15 m + 0,5 % gekommen; haltendes Radar: Ortung nah am letzten Ort, weit von der Vorhersage -> Tempo 0 (laD 30+k);
  0,5 s ohne Ortung -> Tempo 0; Platz-Vergleich: dicht gemessen stehende Luftziele x20, Kandidat mit bestaetigtem Tempo
  und im Schnitt > 4 m/s seit der ersten Ortung zaehlt wie bewegt (x1), sonst nicht bewegte x5.
- Test 'Falsches Tempo im Hafen' (Log nachgestellt) + alle anderen ok. Schreiber: Art +4 = dicht bestaetigt.
- Offen: Mast-Radar-Pakete groesser als 3000 Zeichen (Grenze im Spiel unbekannt, 2999 gingen).

### 04.10. ~09:20: Lage v3.0 / Bild v3.0 (Sicherung 'vor v3.0')
Test 09:00-09:03 (Log waffen_20261004_090004, 163 s, ~37 Ticks/s, nichts verloren): Flak R verfolgte Flieger #3
(450 m hoch, weg fliegend) ab Tick 600, Andre hatte sie gewaehlt -> wartete ~47 s auf die Leertaste, dann 98 Schuss.
Heli #1 schwebte 435 m links in 150 m Hoehe - nie 'bewegt' -> keine Flak. Stehende Hafen-Dinge auf Meereshoehe wurden
'bewegt': Platzwechsel auf ein anderes Radar (Radar-Lage am Mast: 10-14 m Versatz) bzw. haltendes Radar fing nach
2 s ohne Ortung ein Ding 36 m daneben (Fangbereich wuchs 15 m/s * Zeit).
- BILD v3.0 (Andre: Leertaste weg, Master Arm reicht): mit Master Arm schiessen alle Waffen selbst; Wahl = nur Kamera.
- LAGE v3.0: Bool 15+k = Ziel fuer die Waffen = bewegt ODER Luftziel hoeher als 'Stehend Ziel ab m' (60); neuer Platz
  -> c/q neu (bewegt neu messen); See bewegt erst ab 40 m + 1 % (Luft 15 m + 0,5 %); Fangbereich haltendes Radar
  waechst mit (Tempo + 5) * Zeit.
- Tests: 'Heli schwebt, Hafen-Dinge' neu; Zuweisung/Feuer warten laenger (See-Ziel ~10 s bis bewegt).

### 04.10. ~09:35: Einzelschuss per Leertaste (Bild v3.1, Flak v1.9; Sicherung 'vor Einzelschuss')
Andre: "Leertaste mit gewaehlter Waffe = diese schiesst 1 mal (je Druck), soll die Automatik nicht stoppen/behindern".
- BILD v3.1: Leertaste-Flanke + Master Arm + Waffe gewaehlt -> Bool 12+w einen Tick (halten wiederholt nicht).
- FLAKRADAR: Bool 12 (vom Bildschirm) -> O(4) an FLAK. build_flak: Bedienung Bool 12+w -> Flak-Radar Bool 12.
- FLAK v1.9: Bool 4 -> feuern bis zum naechsten Schuss (max 30 Ticks), auch ohne Ziel/Toleranz, nie unter dem
  Sperrprofil; Schreiber-Spalte 'einzel'. Automatik unveraendert.
- Festgelegt (Andre gefragt im Text): Einzelschuss nur mit Master Arm an.
- Tests: Bild 'Einzelschuss Leertaste', Flak Test 13 (3 Druecke ohne Ziel = 3 Schuss; mit Ziel Automatik normal).

### 04.10. ~10:10: Flak v2.0 - Rohre abwechselnd, Zuender knapp hinter dem Ziel (Sicherung 'vor Flak v2.0')
- Gemessen (Log 090004): eine Salve alle 38 Ticks (beide Rohre gleichzeitig) -> ein Rohr laedt 38 Ticks.
- FLAK v2.0: 'AA Takt Ticks' 38, erste Haelfte linkes Rohr (Bool 1 'Feuer'), zweite rechtes (Bool 5 'Feuer rechts',
  neuer Anschluss am Ende) -> alle 19 Ticks ein Schuss. tools/feuer_rechts_update.py legte je Turm das Kabel zum
  Trigger des rechten Rohrs auf 'Feuer rechts' um. Einzelschuss nur links.
- Andre: Heavy-Autocannon-Fragmentation wirkt nur auf ~0,5 m; der Zeitzuender soll an bleiben, aber eine Granate, die
  vorbeifliegt, knapp HINTER dem Ziel zerlegen. Zuender = Flugzeit auf den naechsten ganzen Tick aufgerundet (der Zuender
  zaehlt ganze Ticks, ein Tick = 12-15 m Flugweg) -> Zerlegung 0..1 Tick hinter dem Zielpunkt; 'AA Zuender Zugabe s'
  zum Nachstellen. Spiel-Doku: Fuse Timer = "optional time-delay fuse" (0 = kein Zeitzuender).
- Test 09:55-10:00 (Stand v3.0): stehende Hafen-Dinge jetzt 'See, nicht bewegt' (v2.9-Fix wirkt im Spiel), kein Luftziel.
- Naechstes: Anti-Schiffs-Chips fuer BC (Koerper 4/5: turret_large (0,11,5), gun_l auf Pivots (+-4,14,9), Radar (0,17,11),
  Kamera+Laser (3..4,18..19,10..12)) und AC vorn (Koerper 6/7: turret_medium (0,7,31), gun_m auf Pivots (+-2,9,34),
  Radar (0,12,35), Kamera+Laser (-5..-3,8..9,34..36)) - Aufbau wie die Flaks.

### 04.10. ~10:35: Anti-Schiffs-Kanonen eingebaut (Kanone BC/AC v1.0, Flak v2.2, Bild v3.2; Sicherung 'vor Kanonen')
Werkzeuge: tools/build_kanone.py (nutzt build_flak.build mit Optionen), tools/test_kanone.py, tools/kabel_kanone.py.
- Tuerme wie die Flaks: BC turret_large_a (0,10,5), gun_l (-2,14,9) auf Pivots (+-4,14,9), Belt Feeder L (-1,14,7),
  Radar (0,17,11), Kamera-Pivot (4,18,12); AC turret_medium_a (0,6,31), gun_m (0,9,34) auf Pivots (+-2,9,34), Feeder
  (0,8,34), Radar (0,12,35), Kamera-Pivot (-3,8,36). Chips: BC links ueber Flak L vp (-5,13,-58), AC rechts vp (5,10,-58).
  44 Kabel (inkl. Strom BC links, AC rechts; Kamera hatte schon), Turm-Radare manueller Modus (FOV 0,05 x 0,05 belassen).
- Richtungen aus den Teilen (Regel an allen 4 Flak-Pivots bestaetigt): Drehkranz -1, Radar +1, Kamera -1, Hoehe BC +1/+1,
  AC -1/-1 -> im Spiel pruefen (dreht der Turm zum Ziel? Rohr hoch/runter?).
- FLAK v2.1/v2.2 (gemeinsam): Battle-Cannon-Lade-Ablauf ('Lader Zeit s' 3,6: Verschluss Bool 6, Feed ab 1 s, 2 s warten);
  'Ziel Hoehe fest m' (Schiff 1,5 m ueber dem Meer statt Radar-Hoehe; eigene Hoehe = Physik + Radar-Versatz
  ('Radar ueber/vor Physik m') mit Nick) - bei flacher Bahn kosten 0,5 m Hoehenfehler 15 m Weite; Bahnrechnung: von der
  Sichtlinie in 0,02 rad anheben bis erreicht, dann eingrenzen; ohne Bahnloesung kein Feuer.
- FLAKRADAR v2.0: 'Spur Alpha/Beta' (Flak 0,1/0,005; BC 0,03/0,0003, AC 0,05/0,001 - Tempo-Rauschen x Flugzeit).
- Kanonen: Mindesthoehe -30, tiefster Winkel -5 Grad, Aufschlagzuender, Takt 1 (ein Rohr), BC 800 m/s Drag 0,002
  (Community-Werte, ungeprueft; damit ~5 km Reichweite), Reichweite BC 6000 / AC 2000, Toleranz BC 0,1 Grad / AC 0,3.
- BILD v3.2: Reichweite je Waffe {6000, 2000, 3000, 3000}; Kamera-Text "NOCH OHNE CHIP" weg.
- Pruefstand (Rumpf-Treffer, Schiff 2 m hoch, Seegang): BC 1,5 km 10/11, 3 km 8/11, 4,5 km 10/13; AC 0,4-1,9 km 55-60 %;
  kein Schuss achteraus/ueber Reichweite; Einzelschuss 1. Pruefstand-Konvention: alle Richtungen +1.
- Schreiber: kBr/kBf, kAr/kAf (Takt 14/15, Feuerleitungen teilen 1/3).

### 04.10. ~12:40: Kanonen v1.1 - BC zwei Rohre, Weiche, Vordrehen, tote Winkel (Sicherung 'vor Kanonen v1.1')
Andres Test 10:35 (Log waffen_20261004_100947, 2. Spawn): Flak gut; Kanonen bewegten sich nicht - Bildschirm gab beiden
Ziel #7 (174 m, 227 Grad = achtern links, Hafen-Ding); die Turm-Radare drehten hin (-133 Grad), sahen durch die Bruecke
aber nichts -> nie eine Spur -> Turm blieb in Ruhe. Andre: BC hat ZWEI Rohre (gun_l (-2,14,9) und (2,14,9)), zwei Belt
Feeder L ((+-1,14,7)), eine Weiche gun_belt_junction_l (0,14,7) am gemeinsamen Magazin (er legte selbst das
Munitionskabel Typ 8 flex (0,12,7) -> (0,9,8)).
- FLAK v2.3: ohne Spur dreht der Turm zur Vorgabe (FLAKRADAR v2.1 gibt sie dann auf 3-5) - auch fuer die Flaks;
  Battle Cannon 'Rohre' 2: leeres Rohr laedt (angefangener Ladevorgang laeuft zu Ende), Weiche Bool 7 auf seine Seite,
  Verschluss L Bool 6 / R Bool 8, Loaded R auf Bool 5, abwechselnd schiessen; Weichen-Polung lernt der Chip (2
  Ladezyklen ohne Loaded -> umgekehrt). Schreiber-Spalten laedt/geladen/weiche_umgekehrt.
- BILD v3.3: Kanonen nur Ziele innerhalb GS (aus ihren Sperrprofilen beim Bauen: BC 105 Grad, AC 145 Grad ab Bug).
- KANONE BC v1.1: Chip 4 x 6 (Feuer rechts, Verschluss rechts, Weiche, Geladen rechts); kabel_kanone.py baut alte
  Kanonen-Chips samt Kabeln aus und neu ein (31 alte Kabel weg, 38 neu, Strom schon da bis auf Feeder rechts).
- Pruefstand: BC 2 Rohre links 5 / rechts 6, Treffer 9/11; Weiche verkehrt -> gelernt, beide schiessen; Turm dreht ohne
  Radarkontakt zur Vorgabe (93 statt 90 Grad); alle Flak-/Lage-Tests ok.

### 04.10. ~12:55: Kanonen v1.2 / Flak v2.4 - gehaltene Spur fror ein (Sicherung 'vor Kanonen v1.2', tools/kanone_update.py)
Andres Test 12:43 (Log waffen_20261004_124305): Turm-Drehrichtung RICHTIG (beide Tuerme 27,2 Grad auf Schiff bei 27 Grad),
BC lud beide Rohre (Weiche stimmte auf Anhieb), Radar hielt das Ziel - aber kein Schuss: die gehaltene Spur war
eingefroren (Ort 335/-672, Alter 4, Messdauer 0,15 s ueber 1000+ Ticks). Turm-Radar meldete im Hafen oft 6 Dinge (Ziel
650-750 m, andere 900 m und 6,3 km) -> 16 Spuren voll -> die gehaltene Spur als 'aelteste' verdraengt, der Hardlock hielt
den Verweis fest; Feuern verlangt Messdauer >= 0,4 s -> nie.
- FLAKRADAR v2.2 (Flak v2.4, Kanone v1.2): gehaltene Spur nie verdraengen; nicht mehr in der Liste -> verloren.
  'Ziel Tempo max m/s' (Kanonen 20, Flak 400). BC 'AA Toleranz m' 6.
- Pruefstand-Fehler gefunden: Ortungen lagen auf Kanal = Objekt-Nummer -> ab 7 Objekten ueberschrieben sie Vorgabe/
  Feuer frei/Einzelschuss. Jetzt hoechstens 6 Ortungen je Tick (bei mehr zufaellige Auswahl wie im Spiel).
- Neuer Test 'im Hafen (32 Dinge im Strahl)': altes Skript AC 0 Schuss, neues AC 30 Schuss/17 Treffer, BC 8/6.

### 04.10. ~13:26: Lage v3.1 - Patrouillenboot statt Hafen-Dinge (Sicherung 'vor Lage v3.1', tools/lage31_update.py)
Andres Test 12:54 am feindlichen Hafen (Log waffen_20261004_125349, Kurs 127): Boot rechts voraus (660-760 m, 24 Grad,
~6,5 m/s) hielt Platz 3 von Tick 48 bis 1128 (ab 468 'bewegt'), dann verdraengt von einem ungeklaerten Ding in 137 m
(stehende See-Ziele zaehlten 5-mal: 5 x 137 < 760). Im Topf (6, voll mit Hafen-Dingen) flog es als fernstes sofort raus;
Radar 1 und 3 meldeten es danach noch ~900-mal (Schuebe alle 3-4 s) - jede Ortung Code 99, abgewiesen. Platz 4 hielt
ein Ding 36 m/297 Grad; zwei Hafen-Dinge (173 m/226, 83 m/244) galten zeitweise als 'bewegt' (Spur sprang auf
Nachbar-Dinge 12-50 m daneben).
- LAGE v3.1: fremde Radare fuehren eine Platz-Spur nur im engen Fangbereich nach; stehende See-Ziele zaehlen 50-mal so
  weit, ausserhalb 'See Ziel bis Grad' (145, neu) nochmal 20-mal; ein noch unklares See-Ziel auf einem Platz verdraengt
  nur ein bewegtes; Topf tauscht nach demselben Vergleich (nachweislich stehende - 300 dichte oder 3 passende seltene
  Ortungen ohne Fortschritt - 100-mal), vergisst erst nach 8 s; wer aus dem vollen Topf fliegt und nachweislich steht,
  kommt auf die Merkliste (24 Orte, Ortungen dort Code -8); seltene Ortungen: Tempo passt nur bis (5 m + 2 % R)/s + 3
  m/s (vorher 15), 'bewegt' braucht 10 m + 1 % R mehr Fortschritt, und bei See-Zielen setzt eine seltene Ortung die
  dichte Zaehlung zurueck. Schreiber: Art +8 = nachweislich stehend, neue Spalte la.stehend_gemerkt.
- Pruefstand: neuer Test 'Feindlicher Hafen' (Dinge aus dem Log, Radar meldet die frischesten statt der naechsten -
  wie im Log): Boot 179/180 auf See-Platz, beide Kanonen darauf, kein Hafen-Ding Ziel; Boot erst nach 30/45 s dazu:
  nach 10-11 s auf dem Platz; auch mit 4-fachem Rauschen. Alle Lage-Tests ok. Offen: Boot unter ~5 m/s, das spaeter
  kommt, beweist seine Fahrt im Topf nicht (bekommt einen Platz erst, wenn einer frei oder es naeher ist).
- Im Spiel 13:28 (Log waffen_20261004_132614): 2 Schiffe versenkt. Boot #1 (700 m) ab Tick 522 'bewegt' -> beide Kanonen,
  weg bei 1764; Schiff #9 (1,7 km, 42 Grad) ab 2430 -> beide Kanonen, weg bei 4534. Hafen-Ding 36 m/298 hielt Platz 4,
  Art 12 (nachweislich stehend), nie Ziel; Merkliste 2. BC nur 11 Schuss in ~51 s Gefecht (laedt 86 % der Zeit, ~4,6 s
  je Schuss) - AC 128. Offen: BC-Ladeablauf schneller (Wartezeiten 1 s / 2 s im Spiel ausmessen).

### 04.10. ~14:02: BC-Lader v2.5 - beide Rohre laden gleichzeitig, abwechselnd feuern (Sicherung 'vor BC-Lader', tools/bc_lader_update.py)
Andre: "auch die BC sollte mit beiden Rohren abwechselnd schiessen, optimiere das alles". Log 13:28 ausgemessen: ein Rohr
lud immer 295 Ticks (Verschluss 216 offen, 'Loaded' 79 Ticks nach dem Schliessen), beide nacheinander, dann zwei
Schuesse 6 Ticks auseinander -> ~4,9 s je Schuss, 86 % der Gefechtszeit wurde geladen.
- FLAK v2.5 (Kanone v1.3, Flak L/R v2.5 - Flak-Ablauf unveraendert): Zufuehrung immer an; je Rohr Zustand (zu / offen /
  wartet auf 'Loaded' bis 150 Ticks). Melder 'Contains Ammo' beider Zufuehrungen (neue BC-Eingaenge 'Munition links/
  rechts' auf Bool 6/7): Verschluss auf, sobald die eigene Zufuehrung eine Granate hat; zu 'Lader Nachlauf Ticks' (10)
  nachdem sie sie abgab (hoechstens 'Lader Zeit'); kein 'Loaded' -> nochmal, Nachlauf +5. Weiche bleibt auf einer Seite,
  bis deren Zufuehrung voll ist, dann auf eine leere; Polung lernt sie an den Meldern (Granate kommt auf der anderen
  Seite an, oder 10 s keine). Ohne Melder (nie eine Meldung): alter Ablauf v2.3. Feuer: das Rohr, das nicht zuletzt
  schoss, Abstand halbe gemessene Ladezeit (Schuss bis 'Loaded'); Abzug bleibt am gewaehlten Rohr, bis es geschossen hat;
  Schusserkennung vor der Rohrwahl (Einzelschuss schoss sonst zweimal).
- Kabel: Feeder links (-1,14,7) / rechts (1,14,7) 'Contains Ammo' -> BC-Chip (-5,11,-53) / (-5,10,-53).
- Schreiber 'ff': Spalten lader (Zustand L + 3 x R), geladen (+4/8 Zufuehrung L/R voll, +16 Melder da), nachlauf,
  ladezeit, weiche_auf.
- Pruefstand: Lade-Modell nach dem Log (Verschluss zu 79 Ticks; unbekannt: auf, Zufuehrung->Rohr, Weiche, Magazin);
  Gegenprobe altes Skript = 295/591/887 wie im Log. Neu in 40 s: Standard 32 Schuss (16/16, alle 70 Ticks) statt 8;
  langsamer Nachschub 15; Weiche verkehrt 15; Granate braucht 25 Ticks zum Sitzen -> Nachlauf gelernt, 23; ohne Melder 8.
  Alle Flak- und Kanonen-Tests ok. Offen im Spiel: echte Zeiten (Log Spalten lader/geladen/nachlauf/ladezeit).
- Im Spiel 14:05 (Log waffen_20261004_140308, 2 Laeufe): Lader v2.5 laeuft - Melder kommen, Weichen-Polung stimmte.
  Granate verlaesst die Zufuehrung 79 Ticks nach dem Oeffnen (so lange oeffnet der Verschluss), Zufuehrung 4 Ticks
  spaeter wieder voll, 'Loaded' ~98 Ticks nach dem Schliessen -> Ladezeit 185 Ticks je Rohr (vorher 295), beide parallel,
  Schuss alle ~95 Ticks (1,6 s) statt im Mittel 4,9 s.

### 04.10. ~14:21: Lage v3.2 (Bodenziele) + Auto-Zoom (Flak v2.6, Kanone v1.4; Sicherung 'vor Zoom', tools/zoom_update.py)
Andre: "2 Testlaeufe, bei beiden wurden auch Bodenziele beschossen, fixe und optimiere; neues Feature: Automatik-Zoom,
der mit der bekannten Entfernung so an das Ziel zoomt, dass man es gut erkennt (und spaeter leichter korrigieren kann)".
Log 14:05: Lauf 1 AC 72 Schuss auf #10 (1-1,6 km/249 Grad, 15-22 m hoch, fuhr), Lauf 2 BC+AC 95 Schuss auf #11 (308 m/94
Grad, 15 m hoch, fast stehend, 'bewegt'). Hoehen im Log: fahrende Schiffe Median -2 m (bis +6), stehende Dinge im Wasser
3-6 m, Bodenziele Median 14-16 m (nie unter 6). Flaks schossen nur auf Flugziele (68-382 m hoch).
- LAGE v3.2: geglaettete Hoehe h (3 % je Ortung); Nicht-Luftziel hoeher als 'See Hoehe max m' (7) = Land: nie Ziel fuer
  die Kanonen (Ausgang 'bewegt' aus), beim Platz-Vergleich wie stehend (50-mal); Schreiber-Art +16 = Land.
  Test 'Land' nach dem Log: alte Lage 169 Viertelsekunden Kanone auf Land / 9 auf dem Schiff, neue 0 / 178.
- FLAK v2.6 / Kanone v1.4: Ausgang 'Kamera Zoom' (Zahl 19) an 'Field of View' der Turm-Kamera (Camera Medium 2,2 ..
  0,025 rad, gleichmaessig angenommen). Bildwinkel: Ziel ('Kamera Zielgroesse m' Flak 20 / Kanonen 40) fuellt 'Kamera
  Bildanteil' (0,4) der Breite, aber mindestens so weit, dass das Ziel trotz Vorhalt drin bleibt (Kamera schaut mit dem
  Turm); ohne Ziel 'Kamera FOV ohne Ziel rad' (1,0); weich (6 % je Tick im Verhaeltnis). BC-Chip dafuer 4 x 7 (neue
  Reihe (-5,10..13,-52) war frei). Kabel: Kanone BC (-5,13,-52) -> Kamera (4,19,12); AC (5,12,-54) -> (-4,9,36);
  Flak L (-5,7,-54) -> (-15,20,-98); Flak R (5,8,-54) -> (15,20,-98). Schreiber 'ff' + kamera_fov.
- Pruefstand: Schiff 1,5 km im Bild 100 %, fuellt 40 %; 4,5 km 25 % (Vorhalt-Rand); Flugzeug 1,2 km im Bild 100 %,
  Bildwinkel 0,3 rad (Vorhalt ~0,1 rad), fuellt 6 %. Alle Lage-, Flak-, Kanonen-Tests ok.
- Offen: FOV-Kennlinie der Kamera im Spiel pruefen (Zoom-Eingang linear?); Flak-Kamera zoomt wegen des Vorhalts nur
  maessig - mit dem Pivot-Eingang der Kamera (X/Y, bis 0,125 U) koennte sie aufs Ziel schwenken und enger zoomen;
  Luft-Schwellen ('Luft sicher ab m' 30) koennten Bauten auf Klippen > 30 m als Luftziel nehmen (nicht beobachtet).

### 04.10. ~15:00: Dachkamera, Tiefflieger, schnelle Fahrt (Sicherung 'vor Dachkamera (Andres Stand 14-39)', tools/kamera_update.py)
Andre (Test 14:25, Log waffen_20261004_142203): "ein sehr tief fliegender Eurofighter wurde als Schiff gesehen und von
AC und BC beschossen, dasselbe mit einem Hubschrauber; bei schneller Eigenfahrt haben BC und AC leicht verzogen; die
Kamera hat nicht gut funktioniert, da die Kanonen vorzielen - eine bewegliche Kamera auf dem Dach fuer alle Waffen".
Er baute selbst: Camera Stabilized (camera_gimbal_laser) auf dem Bruecken-Dach (0,33,-15) auf 3x3 Bloecken (y 32) statt
der Pyramiden-Haube; Raketen-Saeule oben am Mast (z -51, y 42-52) entfernt. Keine Kabel.
- Log: #26 (2 km, 5 m hoch, 64 m/s) lag erst auf einem Luft-Platz, verlor 'Luft' unter 10 m -> See-Platz, BC 13 Schuss;
  #53/#34 (2 km, 2-5 m hoch) kreisten (Entfernung +-100 m, Tempo-Schaetzung 0..80 m/s); #35 Heli 7-9 m hoch, 30 m/s.
  Fahrende Schiffe in allen Logs 6-13 m/s.
- LAGE v3.3: Strecken-Tempo vx je Platz (waagerechte Strecke in 2,5 s, abklingendes Maximum); See-Ziel schneller als
  'See Tempo max m/s' (28) ist nie Kanonen-Ziel; Luft bleibt Luft unter 10 m, solange vx > 28. (Die Grenze gilt nur fuer
  See-Ziele - erst falsch auch fuer Luftziele gesetzt, Test 'Heli schwebt in 70 m' fand es.) Test 'Tiefflieger':
  alte Lage 217 Viertelsekunden Kanone auf Heli/Jet, neue 0; Schiff 194/240. Lage jetzt 8119 von 8192 Zeichen.
- FLAKRADAR v2.3 (Flak v2.7, Kanone v1.5): Spuren in der Welt (Ortung + Physik-Ort); vorher relativ - 'Ziel Tempo max'
  (Kanonen 20) deckelte bei 36 m/s eigener Fahrt das Relativ-Tempo, Glaettung hinkte. Pruefstand 36 m/s: alt BC/AC 0
  Treffer, neu BC 18-21 / AC 17-23 von ~20/40 Schuss.
- Monitor: das Kamerabild ist nur im mittleren Drittel des 9x5-Monitors sichtbar (links Radar, rechts Liste) - der
  Turm-Kamera-Zoom (v2.6) hielt das Ziel nur im ganzen Bild, darum lag es mit Vorhalt oft ausserhalb.
- KAMERA v1.0 (neuer Chip 'Figet Marena Kamera' 4x5, vp (5,10,-53) rechte Wand neben AC): schaut auf das Ziel der
  gewaehlten Waffe (Bedienung Zahl 2/4-6, ohne Vorhalt), Zoom: Ziel ('Ziel See m' 40 / 'Ziel Luft m' 20) fuellt
  'Bildanteil' 0,5 der sichtbaren Breite (Drittel). Ob Pivot/Pitch Winkel oder Tempo sind, ist nicht dokumentiert ->
  Messfahrt beim Spawnen (~5 s): Neigung ueber Composite 4, Drehung ueber Laser-Treffer auf dem Meer (Composite 1-3);
  Tempo-Eingang -> Regler auf die Rueckmeldung (Gier am Laser geeicht) mit Vorsteuerung. Pruefstand: drei Kamera-
  Modelle (Winkel U, Winkel rad verdreht/Null achtern, Tempo) - Fehler < 0,0002 U, Schiff 2 km fuellt 52 % des Drittels.
  Kabel: Bedienung, Physik, Composite, Laser Distance -> Chip; Drehung/Neigung/Zoom/Laser an -> Kamera; Strom (linke
  Batterie); Video: Turm-Kameras raus, Dachkamera an alle 4 Kamera-Eingaenge des Bildschirm-Chips. Schreiber 'ka'.
- Offen: Messfahrt im Spiel pruefen (Log 'ka': phase, neigung_je/_0, drehung_je/_0, tempo_*); scheitert sie (kein
  Laser-Treffer, z. B. Mast im Weg), gelten die Eigenschaften (Winkel in U, 0 = oben/Bug).

### 04.10. ~17:43: Kamera v1.1 - Tempo-Eingaenge mit Totzone (Sicherung 'vor Kamera v1.1 (Andres Stand 17-24)', tools/kamera11_update.py)
Andres Test 15:01 (Log waffen_20261004_150020): "die Kamera hat sich nicht mal bewegt". Log 'ka': Composite 4/5 sind
Neigung/Drehung des Kopfs in U relativ zum Spawnen (beide 0 am Anfang, keine Welt-Winkel); Laser ohne Treffer = 4000;
Pivot/Pitch sind TEMPO-Eingaenge mit Totzone 0,1: Modell Drehtempo = 0,106 U/s x (|Befehl| - 0,1), 8 Ticks Verzug -
passt auf 2548 Ticks bis 1e-6 U. Alle Neigungs-Befehle v1.0 lagen <= 0,1 -> sie blieb senkrecht oben; gedreht hat sie
sich ~40 Grad (Blick in den Himmel - unsichtbar). Waffenwahl im Log: 2 AC, 3 Flak L, 4 Flak R; Ziel-Platz kam an.
- KAMERA v1.1: Regler auf die Kopf-Winkel (2,5/s) mit Totzonen-Ausgleich und Vorsteuerung; Messfahrt: mit 1 bis 5 Grad
  unter waagerecht kippen (Tempo und Kipp-Seite messen), Laser-Treffer auf dem Meer abwarten (sonst weiterdrehen),
  etwas drehen, zweiter Treffer -> wohin Drehung 0 zeigt und Drehrichtung. Eigenschaften Totzone 0,1, Tempo je Befehl
  0,106, ohne Treffer Drehung 0 ab Bug 0 / Vorzeichen 1. Pruefstand mit dem gemessenen Modell, 5 Einbau-Varianten
  (auch Laser relativ gemeldet, erster Blick nach achtern auf den Mast): Messfahrt 5,6 s, danach Fehler < 0,0001 U.
- Andre hatte um 17:24 gespeichert (Rumpf: Treppen/Bloecke y 2-7 um z -17..-28 beidseitig, Bloecke y 15 entfernt; keine
  Kabel/Chips) - Update tauscht nur die Kamera-Chip-Definition.
- 17:46: Andre hatte mit Innenausbau ueber den 17:43-Stand gespeichert (Kamera v1.0 zurueck, alles andere v3.3/v2.7/v1.5 noch drin) -> kamera11_update erneut angewendet (Sicherung 'vor Kamera v1.1 (Andres Stand 17-46)').
- 17:50 Kamera v1.2 (Andre: Bild hoch-unten invertiert): die Messfahrt kippte mit +1 nach vorn - ueber die 'Stirn'
  der Kamera (Log 17:47 sonst gut: Tempo 0,1061, Laser-Treffer 92-108 m voraus, Drehung 0 = Bug, Vorzeichen +1,
  danach waagerecht voraus). Jetzt 'Kipp Befehl' -1 (andere Seite, dann halbe Drehung nach vorn); Ersatzwert ohne
  Laser-Treffer 'Drehung 0 ab Bug U' 0,5. Sicherung 'vor Kamera v1.2'.

### 04.10. ~18:40: Korrektur per Blick (Kamera v2.0, Flak v2.8, Kanone v1.6; Sicherung 'vor Korrektur (Andres Stand 17-55)', tools/korrektur_update.py)
Andre: "Korrektur bei ausgewaehlter Waffe - je weiter die Sicht vom Fadenkreuz weg, desto weiter korrigiert er in die
Richtung; wie beim Swifter, aber nur, wenn der Mittelpunkt meines Sichtfelds in einem kleinen Kreis um das Fadenkreuz
ist"; Verhalten wie ein Joystick, Korrektur bleibt. (Kamera v1.2 war 'perfekt' - Bild steht richtig.) Andre hatte um
17:55 gespeichert: nur 'ir_laser' an der Dachkamera eingeschaltet - bleibt.
- KAMERA v2.0: Blick X/Y vom Sitz (Seat data Zahl 9/10, U) gegen 'Blick Mitte X/Y Grad' (geschaetzt 0/15); im Kreis
  'Kreis Grad' 4 (Totzone 0,4) wandert der Zielpunkt der gewaehlten Waffe in Blickrichtung, am Kreisrand 'Korrektur
  Tempo' 0,3 der sichtbaren Bildbreite je s; bleibt je Waffe (Ausgang 'Korrektur' Zahl 2+2w / 3+2w, U). Hotkey 6 kurz =
  Korrektur 0, 2 s halten = Blick-Mitte lernen (bis zum naechsten Spawnen; Log 'blick_mitte_x/y' -> Eigenschaft).
  Zeichnet ins Kamerabild (Video Dachkamera -> Kamera-Chip -> Bildschirm): Kreis (gelb = korrigiert), orange Marke =
  Zielpunkt der Waffe gegenueber dem Ziel.
- FLAK v2.8 / Kanone v1.6: Eingang 'Korrektur' -> Zahl 27/28, Zielpunkt (samt Vorhalt) seitlich/Hoehe verschoben.
  Pruefstand: 0,002 U rechts -> Einschlaege +17,8 m quer bei 1,5 km.
- Kabel: Kamera-Chip Korrektur -> 4 Turm-Chips; Sitz Seat data (0,17,-9) -> Kamera-Chip; Dachkamera Video -> Kamera-Chip;
  Kamera-Chip Video aus -> 4 Kamera-Eingaenge des Bildschirm-Chips (statt Dachkamera direkt).
- Offen: Blick-Mitte im Spiel lernen/eintragen; Richtung Blick X/Y pruefen (wie beim Swifter angenommen: + rechts/hoch).
- ~19:00 Kamera v2.1 (Andre: "Kreis doppelt so gross, Kreuz wesentlich langsamer; Hauptkreuz bleibt, der Vorhalt zieht
  aufs Korrektur-Kreuz?" - ja, so gedacht). Log 18:40: AC ohne Ziel (Kamera weit 1,2 rad) - Tempo hing an der sichtbaren
  Bildbreite, Korrektur nach 2 s am Anschlag 0,1 rad; Blick aufs Fadenkreuz = X ~0 / Y 15,0 Grad (Schaetzung stimmt);
  Hotkey 6 nur kurz (Reset). Jetzt Tempo fest 'Korrektur mrad/s' 2 am Kreisrand (zoom-unabhaengig, ~15x langsamer
  als vorher bei herangezoomtem Schiff), Kreis 8 Grad / 16 Pixel, Totzone 0,8 Grad. Sicherung 'vor Kamera v2.1'.

### 04.10. ~21:23: Auto-Chaff, Lenzpumpen, Knopf Zielkorrektur (Sicherung 'vor Schutz (Andres Stand 21-16)', tools/schutz_update.py)
Andre baute (Stand 21:16): 120 Flare Launcher in zwei Ketten zu 60 (Launch Passthrough -> Launch, erste ohne Eingang:
(-8,17,-37) / (8,17,-37)), Radar Detector (0,32,-13) unter der Dachkamera, 2 Large Fluid Pumps (+-15,-19,-56) mit
Einlaessen/Ueberdruckventilen, 4 grosse Batterien, Tueren, Ausruestung; Instrumentenblock (-2,19,-8) mit 4 Elementen:
'Master arm' (Schalter), 'Aim correction' (Knopf, mode 1), 'Auto Chaff' (Schalter), 'Water Pumps' (Schalter) - alle
ohne 'channel', also alle auf Bool 1 (fehlende Angabe = Kanal 0, wie in den Beispiel-Schiffen ersichtlich).
- Instrumentenblock: Aim correction -> Bool 2, Auto Chaff -> Bool 3, Water Pumps -> Bool 4 (channel 1/2/3).
- KAMERA v2.2: Korrektur nur mit Knopf an (Eingang 'Instrumente', Bool 2 -> Skript Bool 3); aus: kein Kreis, Ausgang 0,
  gemerkte Werte bleiben.
- SCHUTZ v1.0 (neuer Chip 2x3 vp (-5,13,-51)): Auto-Chaff an + Radar Detector -> beide Ketten gleichzeitig (1-Tick-Puls),
  dann alle 'Chaff Abstand s' 1,5, hoechstens 'Chaff je Ortung' 8, neue Ortung nach 'Chaff Pause s' 3; 60 Salven max.
  Pumpen folgen dem Schalter. Strom Pumpen: Batterie L/R. Schreiber 'sc'. Pruefstand test_schutz.py ok.
- Offen: meldet der Radar Detector auch die eigenen Radare? (Log 'sc' Spalte ortung) - sonst feuert Auto-Chaff dauernd
  (bis 8 je Ortung). Knopf 'Aim correction' rastet ein (mode 1)? Wenn nicht: im Skript auf Umschalten bei Druck aendern.
- Andres Frage Treibstoff (Tank getroffen -> Wasser im Motor): Fluid Filter (laesst nur gewaehlte Fluessigkeiten durch)
  auf Diesel vor jedem Motor ist die einfache Loesung; Centrifugal Separator (RPS-Antrieb, Dense Fluid Out = Wasser)
  kann Wasser aktiv abtrennen, braucht aber Drehmoment und Leitung ueber Bord.

### 05.-07.10.: Seeradar, Raketen-Rueckbau, Anstrich, Lua-Liste (Stand 07.10.)
- Raketen: die 24 alten Raketen und der alte Feuerleit-Chip sind raus (Andre baut sein Raketensystem selbst, mit
  Workshop-Chips - Claude baut keine Raketen-Lenk-/Zielerfassungslogik).
- SEERADAR v2.1 (Chip 4x3 an der Rueckwand vp (0,6,-59)): Radar 6 kreist flach, Monitor 3x3 links neben dem Sitz zeigt
  2D-Radar (See blau, Land gruen, Strich, Verblassen, 12 s), Bild 180 Grad gedreht, Zoom 1/2,5/5/10 km selbst (keine
  zwei Punkte naeher als 5 px), Antippen: mit BC/AC gewaehlt -> diese Kanone 20 s auf das Ziel (UEBERGABE im Chip setzt
  es in deren Bedienung), sonst Koordinaten X/Y an 'Ziel X/Y' und Monitor 1x2. Kanonen und Dachkamera bekommen ihre
  Bedienung jetzt ueber den Seeradar-Chip.
- Bildschirm v3.6: 3D-Radar-Zoom 1/2,5/5/10 km selbst, nur Seeziele loesen aus. Flak/Kanone v2.9/v1.7: Bodenziel
  (Vorgabe hoeher als 'Land ab m' 7) -> Radar-Hoehe statt 'Ziel Hoehe fest m'.
- Anstrich (tools/anstrich.py v2.2, Vorschau tools/anstrich_vorschau.py): Marine-Schema mit Platten-Schraffur, innen
  und aussen, auch Bauteile (sc + bc/bc2/bc3).
- wissen/microcontroller/lua.md: im Spiel gemessene Lua-Liste (kein select/print/pcall/setmetatable, table.unpack geht).
- Folgeschalter 54 (2 Chips, nur Bibliothek).

### Offen (Andre 07.10.)
- Flak-Zuender: Splitter reichen weiter als 0,5 m, bester Zerlegepunkt ~0,75 m hinter dem Ziel. Grenze: Zuender zaehlt
  ganze Ticks (~13-17 m Flugweg je Tick). Idee: bevorzugt feuern, wenn ein Tick-Ende ~0,75 m hinter dem Ziel liegt
  (Pruefstand: Treffer gegen Feuerrate abwaegen).
- Antrieb: nach langer Fahrt nur noch 35 kn, eine Schraube zeitweise schneller als die andere (Schiff lenkt komisch).
  Verdacht: Temperatur-Regler je Motor (95 C) drosselt einseitig. Fahrtenschreiber an (Log Port 8766), Auswertung steht
  aus; Abhilfe dann: beide Seiten gleich drosseln und/oder Kuehlung der heissen Seite.
- Autopilot (Andre 07.10.): noch einzubauen - Umfang klaeren (Kurs halten, Tempo halten, Wegpunkt per Seeradar-Antippen,
  Land-Warnung).

### 08.10. ~19:31: Autopilot v1.0 eingebaut (Sicherung 'vor Autopilot (08.10. 19-31)', tools/autopilot_update.py)
- Chip "Figet Marena Autopilot" 4x3 an der Chip-Wand vp (-4,12,-59); Skript lua/autopilot.lua (6018 Zeichen),
  Pruefstand tools/test_autopilot.py (26 Pruefungen ok: Kurs gegen Stroemung, D/W verstellen, Route mit 3 Wegpunkten,
  Antippen/Loeschen, Zoom, Reset, Hotkey 2, Insel-Ausweichen, Laser-Treffer, Nickausgleich, onDraw).
- Kabel: Sitz -> Autopilot 'Sitz', 'Sitz aus' -> Schiffsfuehrung 'Sitz' (statt direkt; Composite-Umschalter Typ 53 im
  Chip: aus = Sitz unveraendert); Physik, Touch, Knoepfe, Laser (Distance/Active/Pivot), Monitor (Video/Power).
  Strom von der Batterie (-4,-13,-46) an Monitor 5x3, beide Knoepfe, Laser. Monitor 5x3 aufrecht gedreht.
- Im Spiel zu pruefen: Zoom-Richtung von drawMap (+ = naeher?), rote Laser-Punkte auf der Kueste (sonst 'Laser Seite'
  -1), Laser-Hoehe (keine Punkte: 'Laser Hoehe Richtung' -1), Regler (Log ap).

### 08.10. ~19:38: Laser schaute aufs Wasser (Sicherung 'vor Laser-Richtung', tools/chip_eigenschaft.py)
- Andres Bild: rote Punkte 300-650 m voraus auf dem Wasser, HINDERNIS im Hafen. Log ap: Nick -3,7 Grad, Felder 1-5
  treffen in 274..430 m (gleichmaessig steigend), Felder 6-9 nichts (4000). Passt zu: Pivot Y plus kippt diesen Laser
  nach UNTEN -> Strahl -7,6 statt +0,3 Grad, Treffer = Meeresboden 36-57 m tief (der Laser sieht durchs Wasser).
- 'Laser Hoehe Richtung' im Schiff auf -1 (nur diese Eigenschaft), Vorgabe in build_autopilot.py ebenso.

### 08.10. ~19:55: Autopilot v1.1 - Control Handle statt Touch, Anti-Kollision per Knopf (Sicherung 'vor Autopilot v1.1 (Andres Stand 19-48)', tools/autopilot11_update.py)
- Andre: Blick bewegt ein Kreuz auf der Karte (nicht schiffzentriert), Leertaste = Wegpunkt dazu/weg, Zoom hoch/runter,
  Touch raus; Bug-Laser beim Laden aus, Knopf 'Automatic anti kollision' schaltet ihn an.
- Chip-Definition getauscht ('Touch' -> 'Griff' gleiche Stelle, neu 'Knopf Anti-Kollision' (2,2)); Kabel: Touch weg,
  Control Handle (-6,19,-21) Seat data -> Griff (Blick = Kanal 9/10, Leertaste Bool 31, besetzt 32), Knopf -> Chip,
  Strom an den Knopf. Pruefstand 36 Pruefungen ok. Skript 7019 Zeichen.
- Griff ist im Editor um 180 Grad (um x) gekippt eingebaut (r 1,0,0,0,-1,0,0,0,-1) - falls Blick/Kreuz verkehrt:
  'Blick X/Y Richtung' -1.

### 08.10. ~20:02: Autopilot v1.2 - Zoom (Sicherung 'vor Autopilot v1.2 (Andres Stand 19-56)', tools/autopilot12_update.py)
- Andre: Zoom per hoch/runter geht nicht. Log: 33 s am Griff, Zoom-Stufe blieb 3 (Schwelle war 0,5). Verdacht:
  Tastatur-Achsen steigen erst an. Jetzt ab 0,2 (scharf erst wieder unter 0,1), dazu Hotkey 3/4 am Griff; Log hat
  alle 4 Griff-Achsen roh (griff_ad, griff_ws, griff_pfeil_lr, griff_pfeil_hr) - zeigt beim naechsten Test, was ankommt.

### 08.10. ~20:20: Licht v1.0 (Sicherung 'vor Licht (Andres Stand 20-14)', tools/licht_update.py)
- Andre: 55 small_light_rgb verteilt (Kabel keine). Chip "Figet Marena Licht" 2x2 (1,12,-59) + Uhr (Clock) (4,12,-59)
  an der Chip-Wand; Tag 1,0 / Nacht 0,35 nach Uhrzeit, Steuerungsraum (4 Deckenlampen y 25) bei Lage-Bedrohung rot
  (5 s halten). 113 Kabel (Farbe, Strom, Uhr, Lage). RGB-Werte 0-1 wie beim Rescue Heli.

### 08.10. ~20:40: Abteile + Schotten v1.0 (Sicherung 'vor Abteile (Andres Stand 20-28)', tools/abteile_update.py)
- Andre: Liquid Meter + 10 Schiebetueren (Schotten) eingebaut, Monitor 9x5 (8,21,-23) fuer die Anzeige. 18 Sensoren
  (8 alte bei y -19 + 10 neue), Abteile erkennt der Chip im Spiel (gleiche Kapazitaet+Fuellung). Zwei Chips (36 Werte),
  61 Kabel. Pruefstand tools/test_abteile.py. kabel_flak.teile: r-Regex las 'fluid_filter="..."' als Drehung - behoben.
  Spiegel-Flags (t) an Anschluessen lokal (vor der Drehung) - per 38 vorhandenen Kabeln bestaetigt.

### 08.10. ~21:10: Abteile v1.2 + Lenzpumpen automatisch (Sicherung 'vor Abteile v1.2 + Pumpen (Andres Stand 21-00)', tools/abteile12_update.py)
- Andre baute die Lenzleitung (eine Pumpe fuer alle Abteile); Schalter 'Auto water pumps' (Instrumentenblock Bool 4) =
  Automatik; Anzeige: pumpt?, L/s, insgesamt raus. Alte Pumpen jetzt auch vom Abteil-Chip (Schutz-Kabel weg).
- Befund: Teile ohne r-Attribut = Drehung 0,0,1,-1,0,0,0,-1,0. Darum stand der Monitor 9x5 senkrecht kopfueber (meine
  Drehung um 20:43 haette ihn flach gelegt - Andres Speichern 21:00 auf altem Stand hat sie ueberschrieben) und die
  Kapazitaets-Kabel der Sensoren 17/18 zeigten daneben (vom Spiel verworfen). kabel_flak/kabel_flossen/teil_drehen
  korrigiert. Abteil-Chip 4x8 an derselben Wand (Ecke an Waffenwahl).
- Andre speichert manchmal auf einem Stand vor meinem letzten Einbau (21:00 basierte auf 20:39) - vor jedem Einbau den
  Stand pruefen, Aenderungen ggf. erneut einbauen.

### 08.10. ~21:22: Abteile v1.3 - Sprit und Batterie (Sicherung 'vor Abteile v1.3', tools/abteile13_update.py)
- Andres Bild: "WASSER!" im Hafen - die 8 alten Sensoren bei y -19 sind die Treibstofftanks (Doppelboden mit Fluid
  Spawner, 98 % voll). Jetzt: Tanks fest (7 Stueck aus den Wand-Querschnitten), kein Wasser-Alarm/Pumpen/Schotten
  durch Sprit; SPRIT/VERBR/Restzeit/BATTERIE auf dem Monitor. Sammler schickt jeden 2. Tick Liter genau (gepackt nur
  0,1 %). Pumpen-Fluss und Batterie ueber Formel-Bausteine (Typ 10, e="...") zusammengefasst.

### 08.10. ~21:26: Abteile v1.4 - Sprit als Tabelle (Sicherung 'vor Abteile v1.4', tools/chip_tauschen.py)
- Andre: Sprit-Anzeige unuebersichtlich (Zeilen liefen ineinander), es sind 8 Tanks (je Liquid Meter einer - meine
  Querschnitt-Deutung "vorn ein Tank" war falsch). Jetzt 8 Balken in 2 Zeilen (SB/BB) x 4 Abschnitte, Bug rechts.
  Neues Werkzeug tools/chip_tauschen.py fuer reine Skript-Tausche.

### 08.10. ~21:53: Schotten-Chip + Abteile v1.5 (Sicherung 'vor Schotten-Chip (Andres Stand 21-44)', tools/schotten_update.py)
- Andre: Wasser rein -> automatisch alle Schotten zu; je Tuer ein Knopf zum Oeffnen von Hand (5 Kippschalter
  button_toggle_2side, je Schottwand einer an der Backbord-Tuer -> schaltet beide Tueren der Wand); Anzeige ohne Punkte.
- Chip Schotten 4x3 an der Decke des Chip-Raums; Abteile v1.5: Liste mit Namen/Balken, Tueren-Kaestchen, Auto zu 0,5 %.

### 08.10. ~22:01: Abteile v1.6 - LECK statt OFFEN (Sicherung 'vor Abteile v1.6', tools/chip_tauschen.py)
- Andres Test mit C4-Loch im Vorschiff: Schotten gingen automatisch zu (Auto zu funktioniert), Vorschiff zeigte
  'OFFEN' (kein geschlossener Raum). Jetzt: Hoehe zum Wasser < 0 = LECK (rot, zaehlt als voll), sonst OFFEN; Namen
  mit BB/SB, wenn die Seiten getrennt sind; 'BUG' unter den Tank-Balken war abgeschnitten (x 267). Ein Tank stand auf
  0 % und VERBR 89,8 L/s - wohl ebenfalls vom C4 (Tank leckt).

### 08.10. ~22:40: Ferngesteuerter Jet v1.0 (Sicherungen 'small Jet vor Chip-Ausbau', 'small Jet vor Jet-Chip', 'Figet Marena vor Jet-Steuerung'; tools/jet_update.py)
- small Jet: 9 alte Chips (Drone receptor/send data + 5 Frequenz-Chips) raus, 44 Logik-Kabel weg; Andre: Physik-Sensor
  + Platzhalter 4x4; Schiff: 2 Funkgeraete (Dach x +-7) + Video-Empfaenger. Chips Jet Flug (lua/jet.lua) und Jet
  Steuerung (lua/jet_steuerung.lua), Pruefstand tools/test_jet.py (25 ok, mit Dreh-Modell 30/60/120 m/s).
- Offen: Landung (Andre noch nicht entschieden), Test im Spiel (Ruder-Vorzeichen!).

### 09.10. ~18:35: Schiff v3.4 - gemeinsamer Temperatur-Regler (Sicherung 'Figet Marena vor Schiff v3.4 (09.10.)', tools/chip_tauschen.py)
- Auswertung Fahrt 07.10.: Vollgas Gang 7 ab kalt +15 Grad/min; bis 75 Grad 60 kn, darueber bricht die Leistung ein
  (80-85 Grad 48 kn bei gleichen Drosseln). Ab 95 Grad drosselte jeder Motor allein und die Regler schaukelten: Seiten
  abwechselnd 10 % / 55 % Gas, 18-29 kn, Schiff zog hin und her (= Andres 'nur noch 35 kn, lenkt komisch' vom 07.10.).
  Die Luft-Kuehlung (48 Electric Radiator, alle mit Luefter und Strom) traegt dauerhaft nur ca. ein Drittel Gas.
- v3.4: EINE Gas-Grenze fuer alle 4 Motoren; Ziel 70 Grad ('Temp Ziel'), sanft angefahren ('Temp Anflug s' 60,
  'Temp Regel' 0.2), TEMP im Helm nur, wenn die Temperatur wirklich Gas wegnimmt. Pruefstand test_temperatur mit
  Waermemodell (Verzoegerung 15/25 s, auch ganze Grad): haelt 70 +-1.5, alle Motoren gleich. chip_tauschen.py kann
  jetzt Eigenschaften neu vorgeben ("Temp Ziel=70"), sonst blieben alte Werte.
- Andre: B (Meerwasser-Waermetauscher) nein - Meerwasser verschleisst. C (E-Motoren zum Tempo-Halten) ja: Andre baut
  die Motoren, dann Chip-Anbindung (Batterie-Schutz, Anschluesse durch Zusammenlegen von 'Motor L/R an' und
  'Rueckwaerts L/R' frei machen).
- Im Spiel zu pruefen: Dauer-Tempo bei 70 Grad (Modell ca. 22 % Gas), ob das Gas ruhig bleibt (liefert das Spiel nur
  ganze Grad, schwankt es mehr), Fahrtenschreiber an.

### 10.10. ~14:30: Mehrspieler-Hilfe gebaut, ~14:40 eingebaut (Sicherung 'Figet Marena vor Mehrspieler-Hilfe (10.10.)')
- Befund 09.10. (Andre Host, Freund Mitspieler): beim Freund Zielliste leer, Pings/Kamera-Zoom nur ab und zu, Schuesse
  ca. 10 %; Tuerme drehen richtig. Grund (Entwickler, Geometa #22188): Lua laeuft auf jedem PC selbst, ihr Zustand wird
  nicht abgeglichen; Mitspieler laden nicht alle Fahrzeuge. Siehe wissen/mechaniken/README.md, Abschnitt Mehrspieler.
- Lage v3.4: Takt auf Bool 21-24 (zaehlt je Tick 0..15), sonst nichts geaendert (test_lage.py alles ok; 8189 Zeichen).
- Bildschirm v3.7: neues Skript lua/mitspieler.lua vor BILD (BILD selbst unveraendert, 8182 Zeichen voll). Beim Host
  reicht es alles durch; springt der Takt (Zwischenstand vom Host beim Mitspieler), 4 Spruenge in 60 s = Mitspieler-
  Modus: die 5 Plaetze + Bedrohung aus dem letzten Host-Stand gelten bis 'MP halten s' (10), Anzeige 'MP <s>S' oben auf
  dem Radar. 'Mehrspieler-Hilfe' 0 = aus. Erste Idee (Kennung blitzt kurz auf) verworfen: Host-Logs zeigten 26-mal Ziele,
  die zwischen Platz und Topf pendeln.
- Pruefstand tools/test_mitspieler.py: alle 236 613 Lage-Logzeilen seit 04.10. als Host (4-mal enger) -> nie aktiv,
  0 Abweichungen; Host-Stoerungen (Takt fehlt alle 30 s, Lage haengt 5 s) -> nie aktiv; Mitspieler-Modell (Stand alle
  30/120/300/600 Ticks) -> erkannt nach 1/4/10/20 s, Host-Ziele zu 99/96/91/85 % sichtbar. Das Mitspieler-Modell ist
  eine Annahme - erst der Test mit dem Freund zeigt, ob es so ist.
- Einbau: tools/chip_tauschen.py "Figet Marena Lage" "Figet Marena Lage v3.4.xml" --schreiben, dann
  "Figet Marena Bildschirm" "Figet Marena Bildschirm v3.7.xml" --schreiben (vorher sichern, Spiel aus/Schiff nicht geladen).

### 10.10. ~15:30: Schotten v2.0 - ein Kippschalter je Tuer (Sicherung 'Figet Marena vor Schotten v2.0 (10.10.)', tools/schotten2_update.py)
- Andre: Knoepfe waren nur an Backbord, jeder oeffnete beide Tueren seiner Wand; gedacht war pro Tuer ein Knopf.
- 5 Kippschalter (2 Seiten) an Steuerbord statt des Wandblocks an der gespiegelten Stelle (Drehung gespiegelt, zweiter
  Block dahinter frei), Strom von Batterie (-4,-13,-46). Chip 4x3 -> 6x4 an derselben Decke (x -2..3, z -53..-50),
  17 alte Kabel weg, 27 neu. Pruefstand tools/test_schotten.py (10 ok) und Nachbau sim/ mit der Probe-Datei: jeder
  Knopf schaltet genau seine Tuer, 0 verworfene Kabel. Im Spiel zu pruefen: sitzen die neuen Schalter richtig (Seite).

### 10.10. ~17:30: E-Motoren (Plan C gegen Ueberhitzung) - Schiff v3.5, Flossen v1.8 (Sicherung 'Figet Marena vor E-Motoren (10.10.)', tools/emotor_update.py)
- Andre: 2 grosse E-Motoren (±8,-13,-96) per T-Stueck an der Welle vor den Getrieben, statt der kleinen Generatoren.
- E-Gas = Hebel minus Temperatur-Grenze (mal 'E-Motor Anteil'), Batterie-Schutz 50/55 %, Richtung je Seite, Test-Modus.
  Kanaele: Zahl 20 (vorher Bugstrahl-Anzeige) = E-Gas; Batterie ueber Flossen-Chip Kanal 21 -> Schiff Kanal 25;
  'Motor L/R an' und 'Rueckwaerts L/R' je zusammengelegt (72 + 1 Kabel umgelegt), dort jetzt 'E-Motor L/R'.
- Pruefstand: heiss Diesel 22 % + E 78 %, Batterie-Schwelle, Test-Modus, ohne Batterie aus. Nachbau mit der Probe-Datei:
  96 Pumpen + 48 Luefter an, E-Gas an beiden Motoren gleich, beide Rueckwaerts-Getriebe, 0 verworfene Kabel.
- Im Spiel zu pruefen: Drehrichtung (linker Motor ist gespiegelt eingebaut!) mit 'E-Motor Test' 1; wie lange die
  Batterien halten (keine Generatoren mehr); bringt der E-Motor bei heissen Dieseln wirklich mehr Tempo?

### 10.10. ~17:26: Schiff v3.6 (Tempo halten, Hebel), Autopilot v1.3, Sitz beschriftet (Sicherung 'Figet Marena vor Schiff v3.6 + Sitz (10.10.)')
- Andre: E-Motor hat nicht dieselbe Leistung -> v3.6 haelt stattdessen das Tempo vom Beginn der Drosselung (PI auf das
  Tempo, Soll folgt dem Hebel mit ^0,4). Modell: E 150 % -> Tempo exakt, E-Gas 0,51; E 50 % / 20 % -> voll.
- Andre: Hebel-Anzeige lief nach dem Loslassen von W weiter. Ursache (Log ap 09.10.): Sitz-Achse W/S steigt/faellt
  langsam (ca. 3 s). Jetzt von Hand: Taste gedrueckt = volle Hebel-Geschwindigkeit, losgelassen = steht. Autopilot setzt
  Bool 29 (v1.3), dann wie bisher anteilig. Dazu: Temperatur-Grenze folgt dem Hebel sofort, wenn kalt (Fehler seit v3.4).
- Steuersitz beschriftet (H1-H6, Leertaste, A/D, W/S, Pfeile), tools/sitz_beschriften.py.
- Nachbau mit der echten Datei: Hebel steht 0,25 s nach dem Loslassen; Autopilot-Knopf -> Bool 29 an/aus; 0 verworfene
  Kabel. Im Spiel: Drehrichtung der E-Motoren noch offen ('E-Motor Test').

### 10.10. ~17:55: Hitze-Test ohne Regelung (Andre; 'Temp Ziel' 200, 'E-Motor Anteil' 0 per Datei, Notschutz 115 bleibt)
- Vollgas nur Diesel: 67-68 kn bis ~75 Grad (3,7 min), dann 60 / 48 / 41 kn; nach 9,7 min 87/92/101/97 Grad, nur noch
  +1 Grad/min - Gleichgewicht ~90-105 Grad, 115 nie erreicht. Mit Regler 70 Grad + E vorher: 28,5 kn. -> 70 Grad war zu
  vorsichtig (Andre: "ab 90 Grad Sorgen"). R1 laeuft ~14 Grad heisser als L1 (Kuehlkreis R1 pruefen?).
- Vorschlag an Andre: 'Temp Ziel' 105 (oder 95) nur als Schutz; E-Motoren auch bei Hitze-Leistungsverlust ab ~75 Grad
  (Tempo halten). Offen: Drehrichtungs-Test ('E-Motor Richtung L' steht schon auf -1).
- Stand der Datei bis zur Entscheidung: 'Temp Ziel' 200, 'E-Motor Anteil' 0, 'E-Motor Richtung L' -1.

### 10.10. ~19:10: E-Tests, Batterien, Raumkuehlung
- E-Motor-Tests (Test-Modus): Richtung L -1 = Linksdreh (links rueckwaerts); nur links +1 = Rechtsdreh -> beide +1
  richtig. Beide +1, nur E: hoechstens ~15 kn, faellt in 2,5 min auf 11 kn (Leistung haengt an der Batterie-Ladung,
  Andre). E-Motoren = wenige Prozent der Diesel-Leistung - als Notantrieb und kleiner Zuschuss. Test-Modus wieder aus,
  'Temp Ziel' 105.
- R1 ~14 Grad heisser als L1: Kuehlteile je Motor gleich (12 Kuehler, 24 Pumpen); rechte Welle dreht schneller
  (15,9 / 15,3 RPS) seit dem E-Motor-Umbau - Verdacht: gespiegelter linker E-Motor bremst leicht.
- Andre: 8 neue grosse Batterien (jetzt 12 + 2 mittlere, ein Netz); Hilfs-Diesel je Seite geplant (Chip 'Hilfsmotoren'
  von Claude, sobald gebaut); Raumkuehlung: 4 Air-Air Heat Exchanger + 10 Pumpen (verkabelt: 'Motoren an' + Strom).

### 10.10. ~19:30: Raumtemperatur gemessen
- 2 Temperature Probes (+-2,-7,-82) -> Chip 'Figet Marena Raumtemperatur' -> Strom 'mr' (Log waffen_20261010_192340).
- Vollgas 6 min (fahrt_20261010_170327 ab 19:25): Raumluft 2,6 -> 7,4 Grad (BB und SB fast gleich), Motoren
  L1/L2/R1/R2 dabei 79/83/88/86 Grad, Tempo 66 -> 52 kn wie immer ab ~75 Grad.
- Ergebnis: der Maschinenraum wird nicht heiss, die Raumkuehlung kann nichts bringen (Motorkurven mit/ohne gleich).
  Vorschlag an Andre: Tauscher + Pumpen ausbauen (Gewicht ~2 kn, Pumpen ziehen Batteriestrom der E-Motoren);
  Probes + Chip duerfen bleiben (leicht). Weiter mit Hilfs-Diesel je Seite.

### Reihenfolge (Andre 08.10.)
1. Autopilot (v1.0 eingebaut 08.10., Test im Spiel steht aus): Kurs/Tempo halten, Karte (screen.drawMap) mit Wegpunkten zum Antippen, Ausweichen ueber 2-3 Laser am Bug
   (Lua kann das Gelaende der Karte nicht auslesen). Andre baut: Autopilot-Knopf, Karten-Monitor, Laser. Chip zwischen
   Sitz und Schiffsfuehrung (gibt Ruder/Fahrhebel vor).
2. Kleinigkeiten: LED-Licht in allen Kabinen, Decklichter. (08.10.: 55 RGB-Lampen + Licht-Chip eingebaut)
3. Liquid Meter je Abteil + Anzeige im Steuerraum, Schotten (noch zu bauen) alle schliessen. (08.10.: eingebaut)
4. Mehr Lenzpumpen (automatisch je Abteil). (08.10.: Andres Lenzleitung + Automatik eingebaut)
5. Ueberhitzung: Temperatur-Regler gleich fuer alle Motoren und sanft; danach ggf. Elektromotoren/Fluid Jets zum Halten
   des Tempos waehrend des Abkuehlens. (09.10.: Regler v3.4 eingebaut; E-Motoren: Andre baut, dann Chip)
6. Raketen raus, dafuer Andres Flugzeug: ferngesteuert, Maussteuerung (Blick wie Swifter), Kamera; eigener Sitz, allein
   per Umschaltung am Hauptsitz. Claude: Steuerlogik mit Stabilisierung, Funkstrecke (Steuerung hin, Flugdaten zurueck),
   Sitz-Umschaltung, Kamerabild mit Anzeige. Andre baut zuerst.
