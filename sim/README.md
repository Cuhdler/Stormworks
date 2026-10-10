# Simulator – eine „Kopie von Stormworks“ für die Chips

Der Simulator lädt eine **echte Fahrzeugdatei** (oder eine Chip-Datei) und führt ihre Microcontroller Tick für Tick
aus, so wie das Spiel es tut: alle Bausteine, alle Lua-Skripte, alle Kabel zwischen den Chips. So lassen sich ganze
Ketten aus mehreren Chips am PC prüfen, ohne das Spiel zu starten. Dazu gibt es einen **Mehrspieler-Modus** (Host +
Mitspieler), um zu sehen, was ein Mitspieler zu sehen bekommt.

**Keine Physik.** Was Sensoren melden (Liquid Meter, Physik-Sensor, Sitz, Uhr …), gibt ein **Szenario** vor
(eine Python-Funktion). Was Motoren, Türen, Lampen usw. daraus machen, rechnet der Simulator nicht – er zeigt nur,
welche Werte bei ihnen ankommen.

Stand: 10.10.2026. Kennzeichen [G]/[W]/[V] wie in `wissen/README.md`.

## Dateien

| Datei | Inhalt |
|---|---|
| `swsim.py` | Einstieg: alles Wichtige zum Importieren, dazu die Kommandozeile |
| `chip.py` | ein Microcontroller: Datei lesen, Bausteine, Takt |
| `ausdruck.py` | Formeln der Formel-Bausteine (`x*y+z`, `clamp(...)`, `x&(!y)`) |
| `lua_block.py` | Lua-Skript-Baustein: eigenes Lua 5.3 je Skript, Stormworks-Befehle nachgebaut |
| `fahrzeug.py` | Fahrzeugdatei: Teile, Anschlüsse, Kabel; mehrere Chips zusammen |
| `mehrspieler.py` | Host + Mitspieler |
| `beispiel_szenario.py` | lauffähiges Beispiel (Wassereinbruch) |
| `test_sim.py` | Prüfstand für den Simulator |

Der Simulator liest nur. Er schreibt nie in `%APPDATA%\Stormworks` und nie in eine Fahrzeugdatei.

## Voraussetzung

Python 3 mit **lupa** (Lua 5.3 für Python): `pip install lupa`. Dasselbe brauchen schon die Prüfstände in `tools/`.

## Schnellstart (Kommandozeile)

```
python sim/swsim.py liste "Figet Marena"                          Chips, Bausteine, verworfene Kabel
python sim/swsim.py verbindungen "Figet Marena" "Figet Marena Schotten"   was an jedem Anschluss hängt
python sim/swsim.py lauf "Figet Marena" "Figet Marena Licht" --ticks 60   Chip(s) ohne Fühler-Werte laufen lassen
python sim/swsim.py datei "build/Figet Marena Licht v1.0.xml"     eine Chip-Datei laufen lassen
python sim/swsim.py typen                                         alle Baustein-Typen auf dem PC: bekannt?
python sim/test_sim.py                                            Prüfstand (ca. 15 s)
python sim/beispiel_szenario.py                                   Beispiel
```

Statt eines Pfads reicht der Fahrzeugname; gesucht wird in `%APPDATA%\Stormworks\data\vehicles`.

## Benutzen aus Python

```python
import sys
sys.path.insert(0, "sim")
import swsim

# 1. Ein Chip allein (aus der Fahrzeugdatei oder aus einer Chip-Datei)
chip = swsim.chip_aus_fahrzeug("Figet Marena", "Figet Marena Licht")
# chip = swsim.Chip.aus_datei("build/Figet Marena Licht v1.0.xml")
chip.setze("Uhr", 0.5)                                   # Eingang (bleibt, bis er neu gesetzt wird)
chip.setze("Lage", swsim.composite(None, {25: True}))   # Composite: {Kanal: Zahl}, {Kanal: An/Aus}
for _ in range(10):
    chip.tick()
print(chip.lese("Licht Steuerraum"))                     # Ausgang
print(chip.verzoegerung("Uhr", "Licht Steuerraum"))      # 3 = so viele Ticks spaeter kommt eine Aenderung an
print(chip.fehler(), chip.hinweise())                    # Lua-Fehler, Hinweise (z. B. property-Name falsch)

# 2. Mehrere Chips mit den Kabeln aus der Fahrzeugdatei
fz = swsim.Fahrzeug("Figet Marena", chips=["Figet Marena Abteile Sammler", "Figet Marena Abteile",
                                           "Figet Marena Schotten"])        # chips=None: alle Chips
fz.teil(d="water_measure", pos=(-18, -15, -40)).setze("Liquid Level", 50.0)   # Fuehler-Ausgang setzen
fz.tick(60)
print(fz.teil(d="door", pos=(-4, -12, 3)).lese("Open/Close"))                 # was beim Stellglied ankommt
print(fz.teil(d="monitor_9", pos=(8, 21, -23)).texte("Video Signal", 288, 160))  # Texte aus onDraw
print("\n".join(fz.verbindungen("Figet Marena Schotten")))
print("\n".join(fz.bericht()))                           # verworfene Kabel, Lua-Fehler, vermutete Bausteine
```

- Ein Teil findet man mit `fz.teil(d=Art, pos=Bezugsblock vp, name=custom_name oder Chip-Name)`; das Ergebnis muss
  eindeutig sein, sonst nennt die Fehlermeldung die Kandidaten.
- **Fühler** = Ausgänge von Teilen, die nicht simuliert werden: `teil.setze(Label, Wert)`. Auch ein Chip, der nicht
  in `chips=` steht, ist so ein Fühler (z. B. den Lage-Chip weglassen und sein Composite „Lage“ selbst setzen).
  `fz.fuehler()` listet, was die laufenden Chips lesen.
- **Stellglieder** = Eingänge von Teilen: `teil.lese(Label)`. `fz.stellglieder()` listet sie.
- Video: `teil.zeichne(Label, breite, hoehe)` ruft `onDraw` aller Skripte, deren Bild dort ankommt, und gibt alle
  `screen.*`-Aufrufe zurück; `teil.texte(...)` nur die Texte.
- HTTP: `Fahrzeug(..., http_antwort=lambda port, anfrage: "ok")` – höchstens eine Anfrage je Tick für das ganze
  Fahrzeug, die Antwort (`httpReply`) kommt im nächsten Tick. Ohne `http_antwort` werden Anfragen nur mitgeschrieben
  (`fz.http_log`), es kommt keine Antwort.

## Szenario-Beispiel

Ein Szenario ist eine Funktion `szenario(fz, tick)`, die der Simulator vor jedem Tick ruft
(ausführlich in `beispiel_szenario.py`):

```python
def szenario(fz, tick):
    if tick == 0:
        for teil in fz.daten.nach_art()["water_measure"]:     # alle Liquid Meter: dicht, 1000 L, leer
            g = swsim.TeilGriff(fz, teil)
            g.setze("Fluid Capacity", 1000.0)
            g.setze("Liquid Level", 0.0)
        fz.teil(d="clock").setze("Time", 0.5)                  # Mittag
    sitz = swsim.composite({2: 1.0 if 60 <= tick < 300 else 0.0}, {1: 30 <= tick < 33})   # W, Hotkey 1
    fz.teil(d="seat_compact", pos=(0, 17, -10)).setze("Seat data", sitz)
    if tick == 600:
        fz.teil(d="water_measure", pos=(-18, -15, -40)).setze("Liquid Level", 50.0)

fz = swsim.Fahrzeug("Figet Marena", chips=["Figet Marena Autopilot", "Figet Marena Schiffsfuehrung",
                                           "Figet Marena Abteile Sammler", "Figet Marena Abteile",
                                           "Figet Marena Schotten"])
fz.tick(900, szenario)
```

Ein Motormodell, Wellen usw. gehören ins Szenario (Beispiel: `SimSchiff` in `test_sim.py` hängt das Motormodell
aus `tools/test_schiff.py` an den Schiffsführungs-Chip).

## Takt: wann kommt ein Wert an?

| Einstellung | Standard | Bedeutung | Quelle |
|---|---|---|---|
| `takt="spiel"` | ja | Jeder Baustein im Chip braucht **einen Tick**: er rechnet mit den Ausgaben seiner Quellen vom letzten Tick, alle gleichzeitig. Eine Kette aus n Bausteinen braucht n Ticks. | [V] |
| `takt="sofort"` | | alles im selben Tick, in Kabel-Reihenfolge. Nur zum Vergleich mit den direkten Lua-Prüfständen in `tools/`. | – |
| `bruecken_takt=False` | ja | Die Anschluss-Brücken des Chips (Ein-/Ausgänge) kosten keinen eigenen Tick. `True`: je einen. | [V] |
| zwischen Teilen | | Ein Chip liest am Tickanfang, was Fühler in diesem Tick zeigen und was andere Chips im **letzten** Tick ausgegeben haben (Kabel = 1 Tick). | [V] |
| `float32=True` | ja | Zahlen an Anschlüssen, in Composites und Bausteinen sind 32-Bit-Kommazahlen. In Lua selbst rechnet das Skript genau (64 Bit). | [G] |
| `lua_halten=True` | ja | Ein Lua-Ausgang behält seinen Wert, bis das Skript ihn neu setzt. `False`: jeden Tick zurück auf 0. | [V] |

Alle Optionen gibt es bei `Chip(...)`, `Fahrzeug(...)` und `Mehrspieler(...)`.

## Bausteine (Typ-Nummer im Chip)

Die Nummern stammen aus der Bibliothek sw_mc_lib (github.com/stormworks-utils/sw_mc_lib, Datei `Types.py`) [W] und
passen zu allen 609 Chips auf Andres PC (Auswertung 10.10.: `python sim/swsim.py typen`). Im Spiel mit Andres Chips
belegt [G] sind 10, 22, 29, 31, 34, 40, 41, 53, 56, 57 und die Brücken 0–7. „Rechenweise [V]“ heißt: was der
Baustein ist, ist sicher, aber wie er genau rechnet, ist geraten – solche Bausteine meldet `fz.bericht()` / `chip.vermutet`.

| Typ | Baustein | Rechenweise |
|---|---|---|
| 0–5 | NICHT, UND, ODER, XOR, NAND, NOR | sicher |
| 6, 7, 8 | Plus, Minus, Mal | sicher |
| 9 | Geteilt | durch 0 = unendlich [V] |
| 10, 36, 45 | Formel mit 3, 8, 1 Eingängen (x y z w a b c d) | Funktionen siehe `ausdruck.py`; `%` wie fmod, `round` .5 weg von 0 [V] |
| 11 | Begrenzen (min/max) | sicher |
| 12 | Schwelle: an, wenn min ≤ x ≤ max | sicher |
| 13 | Zahlen-Speicher (in1 setzen, in2 zurück auf r, in3 Wert) | Reset vor Set, Startwert 0 [V] |
| 14 | Betrag | sicher |
| 15, 16 | Konstante Zahl, Konstante An | sicher |
| 17, 18 | Größer, Kleiner | sicher |
| 19, 20, 33, 34, 58 | Eigenschaft Schieber, Auswahl, Schalter, Zahl, Text | Werte wie in der Datei; Lua liest sie mit `property.*` |
| 21 | Zahlen-Weiche (Ausgang 0 bei an, 1 bei aus) | Reihenfolge der Ausgänge [V] |
| 22, 53, 57, 59 | Umschalter Zahl, Composite, Video, Ton: in1 bei an, in2 bei aus, in3 Schalter | sicher (22: sw_mc_lib [W]) |
| 23, 39 | PID, PID erweitert | P = kp·e, I += ki·e/60, D = kd·Δe·60 [V] |
| 24, 25 | SR-Speicher, JK-Flipflop (Ausgang 0 = Q, 1 = nicht Q) | Vorrang [V] |
| 26 | Kondensator (ct/dt Lade-/Entladezeit s) | an, sobald voll, bis leer [V] |
| 27 | Blinker (on/off Dauer s) | beginnt mit an [V] |
| 28 | Druck-Schalter (Push to Toggle) | sicher |
| 29, 31 | Composite lesen An/Aus, Zahl (`i` Kanal ab 0) | sicher; Kanal-Eingang in2 [V] |
| 35 | Delta (Änderung je Tick) | sicher |
| 37 | Zähler (hoch/runter/zurück, i, min, max, m) | zählt jeden Tick, solange an; Start 0 [V] |
| 38 | Modulo | wie fmod [V] |
| 40, 41 | Composite schreiben Zahl, An/Aus (`count`, `offset`, `inc`) | nur angeschlossene Eingänge ändern ihren Kanal (sicher); Start-Kanal-Eingang `inoff` [V] |
| 42 | Gleich (Toleranz e) | \|a−b\| < e [V] |
| 43, 44 | Tooltip Zahl, An/Aus | keine Ausgänge |
| 46, 47 | An/Aus-Formel mit 4, 8 Eingängen (nicht `!`, und `&`, oder `\|`, entweder-oder `^`) | Vorrang ! vor & vor ^ vor \| [V] |
| 48 | Puls (m: 0 an→aus, 1 aus→an = Standard, 2 jede Änderung) | sicher |
| 49–52 | Zeitglied TON, TOF, RTO, RTF (in1 an, in2 Dauer, in3 Reset; u: 0 s, 1 Ticks) | [V] |
| 56 | Lua-Skript (in1 Composite, in2 Video; Ausgang 0 Composite, 1 Video) | siehe unten |
| Brücken 0–9 | Eingang/Ausgang für An/Aus, Zahl, Composite, Video, Ton | sicher |

Unbekannt sind nur 30 und 32 (alte Composite-Schreib-Bausteine) und 54/55 (Zahl ↔ Composite-Bits); sie kommen in
keiner Datei auf dem PC vor. Ein unbekannter Typ gibt eine klare Meldung mit Typ, Chip und Baustein-Nummer.
Untergruppen im Chip (`<groups>` mit Inhalt) kann der Simulator noch nicht.

## Lua im Simulator

- Jedes Skript hat sein eigenes Lua 5.3 (lupa). Es fehlt, was im Spiel fehlt (`print`, `pcall`, `select`,
  `setmetatable`, `os`, `math.atan2` … – Liste aus `wissen/microcontroller/lua.md`). Aufruf = Absturz wie im Spiel.
- Ein Laufzeitfehler stoppt das Skript für immer; die Ausgänge behalten ihren letzten Wert. `chip.fehler()` nennt ihn.
- `onTick` läuft jeden Tick. `onDraw` nur auf Abruf (`zeichne`/`texte`), mit wählbarer Bildgröße.
- Eingang in `onDraw` lesen: dieses Bild bricht ab (im Spiel „draw error 202“) und es gibt einen Hinweis.
- `property.getNumber/getBool/getText` lesen die Eigenschafts-Bausteine des Chips; ein falscher Name gibt einen Hinweis.
- `screen.*` außerhalb von `onDraw` zeichnet nichts (Hinweis). `map.screenToMap/mapToScreen` wie in
  `landkreuzer/tools/chip_sim.py`. `debug.log` landet in `block.log`.

## Mehrspieler-Modus

```python
mp = swsim.Mehrspieler("Figet Marena", chips=["Figet Marena Licht"], abgleich_ticks=120,
                       gast_fuehler={"Figet Marena Lage": "fehlt"})
mp.tick(3600, szenario)        # szenario(host, tick) setzt die Fuehler beim Host
mp.host.teil(...).lese(...), mp.gast.teil(...).lese(...)
```

**Das Modell ist eine Vermutung [V] und nicht im Spiel bestätigt.** Darum ist alles einstellbar:

1. Host und Gast haben je ihre eigenen Lua-Skripte; Lua-Variablen werden nie abgeglichen (Entwickler, Geometa #22188 [W]).
2. Fühler-Werte (Physik) sind beim Gast dieselben wie beim Host, außer `gast_fuehler` sagt etwas anderes:
   Schlüssel = Bauteil-Art (`"radar_advanced"`), `(Art, Position)`, `(Art, Position, Label)` oder ein Chip-Name;
   Wert = `"gleich"`, `"fehlt"` (Anschluss leer) oder eine Funktion `f(wert, tick) -> wert` (z. B. nur manche Ziele).
   Mit `mp.tick(n, szenario, szenario_gast)` kann man dem Gast auch eigene Werte geben.
3. Alle `abgleich_ticks` Ticks („Zwischenstand“, z. B. 30, 120, 600; 0 = nie) ersetzen die Werte an den
   Chip-Anschlüssen des Hosts (Ein- und Ausgänge, ohne Video) die des Gasts. Dazwischen rechnen die Chips des Gasts selbst.
4. Nicht abgeglichen: Video (jeder zeichnet selbst), innere Werte der Logik-Bausteine (Speicher, Zähler …).

Beobachtung 09.10. (Andre Host, Freund Mitspieler): Abteile- und Autopilot-Monitor beim Mitspieler richtig, Zielliste
leer, Radar-Pings nur ab und zu. Das passt zum Modell: Chips, die nur gleiche Fühler brauchen, zeigen beim Gast
dasselbe; was vom Radar des Hosts abhängt, sieht der Gast nur nach einem Zwischenstand.

## Was geprüft ist (`python sim/test_sim.py`, 10.10.2026: ALLES OK)

- **Bausteine** an einem kleinen Test-Chip: 3 NICHT hintereinander = 2 Ticks später (sofort: 0, mit Brücken-Takt: 4),
  Formel, Composite schreiben mit Lücke, Composite lesen, Umschalter, Puls, Druck-Schalter, Schwelle, 32-Bit-Zahlen,
  Lua mit Eigenschaft und onDraw, `print` stoppt das Skript, unbekannter Typ gibt klare Meldung.
- **Alle 609 Chips** auf dem PC (alle Fahrzeuge + microprocessors) laden und laufen 10 Ticks, alle Typen bekannt.
- **Schiffsführung** aus der Fahrzeugdatei gegen `lua/schiff.lua` direkt (`tools/test_schiff.py`):
  Takt sofort 5700 Ticks mit Motormodell: 0 Abweichungen (alle Ausgänge, alle 32 Skript-Kanäle, Helm-Anzeige);
  Andres Prüfungen `test_motor` + `test_system` mit dem Chip: 27/27 ok.
  Takt spiel 4200 Ticks: 0 Abweichungen, wenn der direkte Lauf die Sitz-Werte so viele Ticks später bekommt, wie
  Bausteine davor liegen (An/Aus 4, Zahlen 8, abgezählt in `tools/build_schiff.py`).
  Hotkey 1 → „Motor L an“ 5 Ticks später = 6 Bausteine.
- **Licht, Schotten, Abteile Sammler** aus der Fahrzeugdatei gegen ihre `lua/`-Datei: 0 Abweichungen.
- **Fahrzeug-Netz:** alle 1050 Kabel der Figet Marena treffen einen Anschluss; Anschluss-Lage 2885/2885 gleich wie
  `landkreuzer/tools/fz.py` mit den Spieldaten; ein Kabel ins Leere wird gemeldet. Sieben Chips zusammen: Sitz H1 →
  Autopilot → Schiffsführung → Pumpe an nach genau Bausteine + Kabel (Tick 36); Wasser im Abteil → Sammler → Abteile
  → Schotten → alle 10 Türen zu nach 10 Ticks; Lampe und Abteil-Monitor bekommen ihre Werte; HTTP-Schreiber.
- **Mehrspieler:** gleiche Fühler → Türen und Abteil-Monitor beim Gast gleich wie beim Host. Bedrohung kommt beim
  Gast nicht an: ohne Abgleich nie rot, Zwischenstand alle 120 Ticks → immer rot (rot hält 5 s), alle 600 Ticks → die
  Hälfte der Zeit rot.

## Befunde beim Prüfen (10.10.)

- Im Takt „spiel“ bestehen 24 von 27 Prüfungen aus `tools/test_schiff.py`; anders sind: das Ruder ist 8 Ticks später
  wieder auf null (38 statt 30 Ticks nach dem Loslassen), die Hotkey-4-Seite im Helm erscheint nach 6 Ticks statt 1
  (die Prüfung schaut nach 2), bei Vollgas nach 34 s 99 % statt 100 % Gas. Das zeigt, was die Verzögerung durch die
  Bausteine ausmacht – falls das Spiel wirklich einen Tick je Baustein braucht.
- KI Landkreuzer: ein Zahl-Kabel von (0,−3,−14) zum Chip-Eingang „Batterie“ (−2,2,−20) zeigt auf den Strom-Anschluss
  der Batterie statt auf ihren Ausgang „Charge“ (−1 Block daneben) – das Spiel verwirft es, der Eingang bleibt 0.
- Figet Marena: Eingang „Knopf Schotten“ des Abteil-Chips hat kein Kabel (`fz.verbindungen(...)`).

## Bekannte Lücken

- Keine Physik, kein Strom (alle Teile arbeiten, auch ohne Batterie), keine Flüssigkeiten, kein Radar – alles das
  kommt aus dem Szenario.
- Video: nur die Zeichen-Aufrufe der Lua-Skripte (`screen.*`), keine Pixel und keine Kamerabilder.
- Ton: wird nur durchgereicht.
- Die mit [V] markierten Bausteine und Takt-Regeln sind nicht im Spiel gemessen.
- Reihenfolge der Chips innerhalb eines Ticks im Takt „spiel“: egal (alle lesen vom letzten Tick); wie das Spiel
  wirklich ordnet, ist unbekannt.
- Mehrspieler: nur das Modell oben; Abgleich innerer Bausteine und Bandbreiten-Effekte (Fahrzeuge weit weg) fehlen.
- Untergruppen in Chips, Typen 30/32/54/55.

## Offene Fragen (im Spiel prüfen)

1. Braucht wirklich jeder Baustein einen Tick? Und die Anschluss-Brücken? Test: Chip mit 10 NICHT-Bausteinen in
   Reihe, Eingang und Ausgang an zwei Lampen, per Lua-Schreiber Tick-genau mitschreiben.
2. Behält ein Lua-Ausgang seinen Wert, wenn das Skript ihn nicht mehr setzt (`lua_halten`)? Test: Wert nur setzen,
   solange ein Knopf gedrückt ist, und an einer Zahlenanzeige ablesen.
3. Mehrspieler: Werden Chip-Anschlüsse abgeglichen, wie oft, und auch innere Bausteine?
4. Rechenweise von PID, Kondensator, Zähler, Zeitgliedern (nur für fremde Chips wichtig – Andres Chips nutzen sie nicht).
