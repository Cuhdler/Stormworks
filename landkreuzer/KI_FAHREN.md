# KI Landkreuzer – Fahr-KI und Karte

**Stand:** 08.10.2026. Zwei Lua-Skripte für den Radpanzer (27,5 × 9,5 m, 7 Räder je Seite, Panzerlenkung) und ein
Prüfstand im Rechner. Im Spiel noch **nicht** erprobt – alles unten unter „Im Spiel prüfen“ ist offen.

| Datei | Was |
|---|---|
| `lua/ki_fahren.lua` | das Fahr-Gehirn (Antrieb links/rechts) |
| `lua/ki_karte.lua` | Touch-Karte im Cockpit (Monitor 3×3 oder 5×3) |
| `tools/ki_props.py` | alle Properties mit Standardwert und Erklärung (`PROPS_FAHREN`, `PROPS_KARTE`, `PROPS`) |
| `tools/test_ki.py` | Prüfstand: Simulator + 57 Prüfungen (auch Wald, Damm, Tal, holpriger Boden, Lenk-Variante, 0,6 m höhere Räder, Stehen am Hang), am Ende „ALLES OK“ |

---

## 1. Was die KI macht

- **Schalter „KI an“** (kommt mit Startverzögerung/Pause vom Klebe-Skript): der Panzer merkt sich die Stelle als
  **Heimat** und fährt allein.
- **Wegpunkte** (bis 8) tippt Andre auf der Karte an. Die KI fährt sie der Reihe nach ab. Im **Revier-Modus** (Knopf
  „Revier“, grün = an, beim Start an) geht es danach wieder von vorn los, sonst bleibt er am letzten stehen.
- **Ohne Wegpunkte** im Revier-Modus: Zufallspunkte höchstens „Revier m“ um die Heimat. Am Punkt bleibt er
  „Patrouille Pause s“ stehen (die Türme arbeiten weiter), dann der nächste Punkt.
- **Schalter „Nach Hause“**: zurück zur Heimat und dort warten; Schalter aus = weiter wie vorher.
- **W/S/A/D am Sitz** = sofort Handbetrieb (auch bei KI aus). 2 s nach dem Loslassen fährt die KI weiter.
- **Kampf**: meldet das Waffensystem ein Ziel näher als „Kampf Abstand m“, hält er an (stabile Plattform) und dreht
  den Bug zum Ziel (±„Kampf Winkel Grad“). Näher als „Mindestabstand m“: rückwärts, Bug bleibt zum Ziel. 5 s ohne
  Ziel: weiter auf der Route.
- **Batterie** unter „Batterie min“: anhalten. Unter 30 %: nur 60 % Tempo. Ist der Eingang nicht angeschlossen
  (immer 0), gilt die Batterie als unbekannt – kein Halt.
- Dazu im **Klebe-Skript** (`lua/ki_kleber.lua`, vor der Fahr-KI): Startverzögerung (30 s) und Waffen-Verzögerung
  (60 s), unter „Heim Batterie“ (40 %) von selbst nach Hause, **Schutzzone** (300 m um den Startpunkt und um die
  Freund-Punkte der Karte): Ziele dort bekommen keinen Schuss und werden nicht angefahren; Auto-Chaff nur mit Ziel.
- **Hält die Stelle**, wenn das Soll-Tempo 0 ist (Kampf, Pause, am Ziel, Batterie leer, LASER?).

### Hindernisse, Hänge, Wasser, Kanten
- Die **drei Front-Laser** (mit 7er-Rädern 2,4 m hoch, gerade nach vorn, 3,5 m auseinander) decken die Fahrgasse ab. Ein Hang mit
  Winkel a erscheint dem Strahl erst bei d = 2,4 / tan(a − Nick) – eine Wand und ein Hang sehen von weitem gleich aus.
  Darum: ab „Hindernis m“ langsamer, unter „Notstopp m“ nur kriechen. Hebt ein Hang den Bug an, geht der Strahl über
  ihn weg und er fährt weiter; kommt eine Wand näher als ca. 4,2 m (= steiler als „Steigung max Grad“), setzt er
  zurück und dreht zur freieren Seite.
- Ein Außenstrahl deutlich kürzer als der andere = schmales Hindernis → zur freien Seite lenken.
- **Treffer-Gedächtnis**: die Strahlen decken nur ±3,5 m ab, der Panzer ist ±4,75 m breit, die Seiten-Laser sitzen
  in der Mitte. Darum merkt sich die KI Treffer als Ort und dreht nicht zu Punkten hin, die neben dem Rumpf oder
  voraus liegen; an Wänden hält sie früh und sanft Abstand (beim Wegdrehen schwenkt das lange Heck zur Wand).
- **Sackgasse** (vorn zu, beide Seiten enger als „Breite m“): gerade zurück, bis der ganze Rumpf draußen ist; die
  ganze Sackgasse wird gemerkt und künftig umfahren.
- **Bug-Laser** (senkrecht nach unten): Grundwert lernt er beim Stehen vor dem KI-Start („Boden Laser Hoehe m“ = 0).
  Daraus folgen auch die Höhen der Front-Laser und des Physik-Sensors (Automatik) – die Radgröße ist also egal.
  - Boden unter dem Bug unter 0,5 m über dem Meer = **Wasser** → kräftig bremsen, zurück. Je tiefer der Boden unter
    dem Bug, desto langsamer (ab 10 m über „Wasser Hoehe m“), damit 50 t bergab rechtzeitig stehen.
  - Boden fällt **plötzlich** mehr als „Absturz m“ weg (steiler als „Steigung max“) = **Kante** → zurück. Über eine
    Kuppe ragt der Bug nur langsam hinaus – das zählt nicht.
- **Schräglage** über „Kipp max Grad“: bei Nick zurück, bei Roll langsam vor und zur hohen Seite drehen.
- **Gefährliche Stellen** (8, die ältesten fallen raus) stoßen den Kurs ab und lenken um sie herum. Revier-Punkte
  meiden sie und Orte, an denen er schon tief (unter „Wasser Hoehe m“) war.
- **Festgefahren** (Befehl groß, weder Fahrt noch Drehung, 3 s): 3 s in Gegenrichtung mit Drehung.
- **Stehen am Hang**: Elektromotoren ohne Gas bremsen nicht. Soll er stehen (Kampf, Pause, am Ziel), hält der
  Tempo-Regler die Stelle mit den Motoren (im Simulator am 15°-Hang 30 s lang auf 0,1 m genau; vorher rollte er
  16 m zurück). Auf ebenem Boden kostet das fast keinen Strom.
- Ein Ziel, das **3 Fehlschläge** bringt (festgefahren 1, Gefahr 2, 60 s ohne 5 m näher 1), wird übersprungen –
  z. B. ein Wegpunkt im See oder unter einer Klippe.

### Rad-Richtung und Lernen
„Rad Richtung links/rechts“ (1/−1) drehen die Ausgänge um (rechts ist gespiegelt eingebaut → −1). Mit „Richtung
lernen“ = 1 fährt er nach dem Einschalten bis 2 s gerade an und merkt selbst, wenn eine Seite (oder beide) falsch
herum dreht. Das Gelernte gilt bis zum Neustart des Skripts – der Status-Monitor zeigt es rot (L! / R!; Bool 5/6 am Ausgang), dann das Property
richtig stellen.

### Tempo
Das Tempo vorwärts rechnet die KI selbst aus der Ortsänderung (Kanal 7/8 des Physik-Sensors werden nicht gebraucht).

---

## 2. Zustände (Ausgang Zahl 3, Kopfzeile der Karte)

| Nr | Karte | Bedeutung |
|---|---|---|
| 0 | AUS | KI aus, kein Handbetrieb |
| 1 | HAND | Handbetrieb (W/S/A/D) oder 2 s Pause danach |
| 2 | WEGPUNKT | fährt zum Wegpunkt (oder nach Hause) |
| 3 | REVIER | fährt zum Revier-Punkt |
| 4 | AUSWEICHEN | Hindernis vorn: kriechen, ausweichen |
| 5 | ZURUECK | zurücksetzen / freifahren / aus der Sackgasse |
| 6 | KAMPF | Ziel in Reichweite: steht, Bug zum Ziel |
| 7 | BATTERIE | Batterie leer: steht |
| 8 | GEFAHR | Wasser, Kante oder Schräglage |
| 9 | WARTET | am Ziel, zu Hause, Patrouillen-Pause |
| 10 | LASER? | Laser vorn Mitte (Zahl 10) oder Bug-Laser (14) meldet 0: blind – steht (hält die Stelle) |

---

## 3. Kanäle

### ki_fahren.lua
**Eingang** (Composite) – Zahlen: 1 Ost, 2 Höhe, 3 Nord, 4 Kompass (U), 5 Nick (U), 6 Roll (U), 7/8 ungenutzt,
9/10/11 Front-Laser links/Mitte/rechts, 12/13 Seiten-Laser links/rechts, 14 Bug-Laser unten, 15 Heck-Laser,
16 Batterie (0..1, 0 = nicht angeschlossen), 17 A/D (+ rechts), 18 W/S (+ vor), 20/21 Ziel Ost/Nord, 22 Ziel Höhe
(ungenutzt), 23/24 Tipp Ost/Nord, 25 Kartenbefehl (1 Wegpunkte löschen, 2 Revier-Modus um).
Bools: 1 KI an, 2 Sitz besetzt, 3 Tipp-Puls, 4 Ziel gültig, 5 Befehl-Puls, 6 Nach Hause.

**Ausgang** – Zahlen: 1/2 Antrieb links/rechts (−1..1, mit Rad-Richtung), 3 Zustand, 4/5 aktuelles Ziel (im Kampf
der Feind), 6 Soll-Kurs (U im Uhrzeigersinn), 7/8 Heimat, 9 Revier m, 10 Zahl der Wegpunkte, 11 aktueller Wegpunkt,
12–27 Wegpunkte (Ost/Nord-Paare), 28 Soll-Tempo m/s, 29 Lenkbefehl roh (−1..1, + rechtsherum), 30 Fahrbefehl roh
(−1..1, + vor) – beide vor Rad-Richtung/Lernen, auch im Handbetrieb, 31 eigener Kurs (U im Uhrzeigersinn ab Nord),
32 Tempo vorwärts m/s.
Bools: 1 Antrieb aktiv, 2 Waffen frei (KI an, kein Handbetrieb), 3 Revier-Modus, 4 Wegpunkt erreicht (Puls),
5/6 Richtung links/rechts umgelernt.

### ki_karte.lua
**Eingang** = Ausgang von ki_fahren (Zahl 3–28, 31/32, Bool 1–4), vom Chip überschrieben:
Zahl 1/2 = Touch x/y (Monitor-Zahl 3/4), **Zahl 29/30 = eigener Ort Ost/Nord vom Physik-Sensor (Zahl 1/3)**,
Bool 32 = Touch gedrückt (Monitor-Bool 1). Die Monitorgröße liest das Skript selbst.
**Ausgang**: Zahl 23/24 Tipp Ost/Nord, 25 Befehl; Bool 3 Tipp-Puls, 5 Befehl-Puls (je 1 Tick, gleiche Kanäle wie
die Eingänge von ki_fahren – der Chip kann sie direkt durchreichen); Zahl 1–8 Freund-Punkte Ost/Nord, 9 ihre Zahl
(an das Klebe-Skript, Zahl 4–12).

**Bedienung**: Karte kurz antippen = Wegpunkt (zählt beim Loslassen). Finger 1,5 s halten = Freund-Punkt (weitere
Schutzzone, höchstens 4; nochmal halten = weg). Knöpfe unten: „Loeschen“ (zweimal binnen 3 s tippen – einmal wäre zu
leicht aus Versehen), „−“ weiter weg, „+“ näher dran, „Revier“ (an/aus); bei den Knöpfen zählt das Aufsetzen.

---

## 4. Properties

| Name | Standard | Erklärung |
|---|---|---|
| Tempo m/s | 8 | Reisetempo der KI auf freier Strecke |
| Vollgas m/s | 12 | Tempo bei Vollgas auf ebenem Boden (Vorsteuerung des Tempo-Reglers) |
| Kriech m/s | 1.5 | Schleich-Tempo nah an Hindernissen, am Wasser, in Schräglage |
| Rampe s | 1 | Fahrbefehl 0 → voll in so vielen Sekunden (Bremsen 3×, bei Gefahr 4× schneller) |
| Lenk Staerke | 4 | wie kräftig auf den Kurs gelenkt wird |
| Dreh Gas | 0.6 | Lenkbefehl beim Drehen auf der Stelle |
| Rad Richtung links | 1 | Vorzeichen linker Antrieb |
| Rad Richtung rechts | −1 | Vorzeichen rechter Antrieb (gespiegelt eingebaut) |
| Richtung lernen | 1 | falsch drehende Seiten selbst erkennen (0 = aus) |
| Ziel Radius m | 20 | so nah = Wegpunkt erreicht |
| Revier m | 400 | Radius für Revier-Punkte um die Heimat |
| Patrouille Pause s | 45 | Pause am Revier-Punkt (0 = gleich weiter) |
| Hindernis m | 25 | ab hier langsamer und zur freien Seite lenken |
| Notstopp m | 8 | darunter nur kriechen, bis klar ist: Hang oder Hindernis |
| Steigung max Grad | 30 | steiler = Hindernis |
| Kipp max Grad | 25 | mehr Schräglage = Gefahr |
| Wasser Hoehe m | 3 | eigene Höhe darunter: kriechen; Boden unter dem Bug: ab 10 m darüber langsamer |
| Wasser Stopp m | 1.5 | eigene Höhe darunter: sofort zurück |
| Absturz m | 2.5 | so viel tiefer und plötzlich = Kante |
| Breite m | 9.5 | Breite mit Rädern |
| Laenge m | 27.5 | Länge (Physik-Sensor in der Mitte, Bug-Laser vorn) |
| Laser Hoehe m | 0 | Höhe der Front-Laser über dem Boden; 0 = Automatik (Bug-Laser-Grundwert + 0,8 m, passt zu jeder Radgröße) |
| Boden Laser Hoehe m | 0 | Grundwert des Bug-Lasers; 0 = beim Stehen vor dem Start lernen |
| Sensor Hoehe m | 0 | Höhe des Physik-Sensors über dem Boden; 0 = Automatik (Bug-Laser-Grundwert + 0,55 m) |
| Kampf Abstand m | 1500 | Ziel näher = anhalten |
| Kampf Tempo m/s | 0 | Tempo im Kampf |
| Kampf Winkel Grad | 30 | Bug so weit zum Ziel drehen (0 = nicht drehen) |
| Mindestabstand m | 150 | Ziel näher = rückwärts |
| Batterie min | 0.1 | darunter anhalten (0 = aus) |
| Kompass Richtung | −1 | Kompass zählt gegen den Uhrzeigersinn |
| Nick Richtung | 1 | Bug hoch = positiv |
| Roll Richtung | −1 | Physik-Sensor meldet „rechte Seite tief“ negativ (so arbeiten die Flossen des Schiffs, im Spiel bewährt) |
| Zoom Start (Karte) | 1 | Karten-Zoom beim Einschalten |

---

## 5. Grenzen (was die KI nicht kann)

- **Lücke zwischen Außenstrahl und Bordwand** (3,5 m bis 4,75 m seitlich): ein schmaler Pfosten genau dort wird erst
  bemerkt, wenn er schon einmal getroffen wurde oder ein Seiten-Laser ihn sah. Im Prüfstand: von 10 Dauerläufen
  (je 10 min) streifte einer dreimal einen runden Fels, der genau in dieser Lücke lag; die anderen 9 ohne Stoß. Flache Hindernisse unter 2,4 m sieht
  kein Front-Laser – dafür gibt es die Festfahr-Erkennung.
- **Dichter Wald** (Bäume im Mittel 30 m auseinander): von 8 zufälligen Wäldern schafft sie 5, in 3 bleibt sie
  hängen (viele Stöße). Die Lenk-Variante schafft 4 von 8, streift aber deutlich weniger (69 statt 97 Stöße). Versucht und verworfen: zwei Eck-Laser ganz außen am Bug (mit Gedächtnis 3/8, nur bremsen
  und weglenken 3/8 – beides schlechter). Lichter Wald (Prüfung „Wald“) geht.
- **Träge Kettenlenkung:** Im Simulator dreht der Panzer bei vollem Links/Rechts-Unterschied mit 23°/s
  (`SKID` in `test_ki.py`). Mit einem Drittel davon (ein 27-m-Fahrzeug rutscht im Spiel vielleicht schwerer)
  bestehen noch alle Einzelprüfungen (Wegpunkte, Wand, Sackgasse, See, Klippe, Hügel, Kampf), in den
  10-Minuten-Dauerläufen kommt er aber deutlich weniger weit. Dreht er im Spiel so träge: Lenk-Variante nehmen.
- **Wand oder Hang** erkennt sie erst bei ca. 4 m: vor Hindernissen kriecht sie deshalb das letzte Stück.
- **Kanten seitlich** sieht nur der Bug-Laser, wenn der Bug drüber ist. Schräg an eine Kante herangefahren kann eine
  Ecke überstehen, bevor die KI es merkt.
- **Bremsweg**: der Bug-Laser sieht erst, wenn der Bug über Kante/Wasser ist; bis zum Schwerpunkt sind es 14 m. Aus
  8 m/s braucht der Panzer im Simulator ca. 8–11 m. Bremst er im Spiel schlechter, „Tempo m/s“ senken.
- Revier-Punkte kennt die KI nur als Koordinaten – ob dort Wasser oder eine Klippe ist, merkt sie erst vor Ort
  (dann wird der Punkt übersprungen und die Stelle gemieden).
- Alles Gelernte (gefährliche Stellen, Richtung, Bug-Laser-Grundwert) ist nach einem Neustart des Skripts weg.
- Das Spiel läuft im Gefecht mit 20–40 Ticks/s; die Zeiten (2 s, 3 s, 5 s) zählt die KI in Ticks, also Spielzeit.

---

## 6. Im Spiel prüfen

1. **Kompass**: KI an, Wegpunkt genau nördlich tippen – fährt er nach Norden? Sonst „Kompass Richtung“ umdrehen.
2. **Rad-Richtung**: mit W fährt er vor, mit D dreht er rechts? Rot L! / R! auf dem Status-Monitor = umgelernt → Property
   richtig stellen.
3. **Nick/Roll-Vorzeichen**: am Hang Bug hoch → Physik-Sensor Nick positiv? Rechte Seite tief → Roll **negativ**
   (so ist es bei den Flossen des Schiffs)? Sonst „Nick Richtung“ bzw. „Roll Richtung“ umdrehen.
4. **Bug-Laser**: Grundwert auf ebenem Boden (Zahl 14) notieren; an einer Böschung zum Wasser: hält er rechtzeitig?
   Trifft der Laser die Wasseroberfläche oder den Grund? (beides wird erkannt)
5. **Front-Laser**: vor einer Hauswand – kriecht er heran und setzt bei ca. 4 m zurück? An einem sanften Hügel
   (unter 20°) – fährt er hinauf?
6. **Bremsweg** aus 8 m/s mit vollem Gegengas messen (muss unter ca. 12 m liegen).
7. **Drehen auf der Stelle**: wie schnell (Grad/s) und wie viel Platz braucht er wirklich?
8. **Karte**: Monitor-Touch richtig herum? Tipp setzt den Wegpunkt dort, wo der Finger war? Zoom-Stufen sinnvoll?
9. **Kampf**: mit Ziel von der Lagezentrale – bleibt er stehen und dreht den Bug zum Ziel?
10. **Batterie**: Eingang angeschlossen? Bei 30 % langsamer, bei 10 % Halt.

---

## 7. Prüfstand

```
python landkreuzer/tools/test_ki.py            # alle Prüfungen (ca. 1 min), am Ende "ALLES OK"
python landkreuzer/tools/test_ki.py wand see   # nur einzelne (Teil des Namens)
```
Braucht Python mit `lupa`. Der Prüfstand lädt die Skripte wie im Spiel (nur die dort vorhandenen Lua-Namen, Eingänge
nur in `onTick`, Bildschirm/Karte nur in `onDraw`) und prüft die Größe nach dem Verkleinern (≤ 8000 Zeichen, auch mit
`tools/build_mc.py`). Der Simulator: Welt mit Ebene, Hügel, See mit Strand, Klippe, Wänden, Häusern, flachem Fels;
Panzer 27,5 × 9,5 m mit Panzerlenkung (Laser an den Stellen wie im gebauten Fahrzeug), 7 Radpaaren (kippt über eine Kante erst, wenn die Mitte drüber ist) und allen
Lasern wie im Fahrzeug. Szenarien: Wegpunkte, Wand, Hügel, Sackgasse (zu eng zum Drehen), See, Klippe, flacher Fels
(festgefahren), Revier, Dauerläufe 10 min in gemischter Welt, Hand, KI aus, Kampf, Batterie, Pause, Nach Hause,
Richtung lernen, Karte.
