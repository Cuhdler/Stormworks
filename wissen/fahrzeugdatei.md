# Fahrzeugdatei (XML) lesen und richtig bearbeiten

Für eine KI, die an Andres Stormworks-Fahrzeugen arbeiten soll. Hier steht, wie eine Fahrzeugdatei aufgebaut ist
(`data_version="3"`), wie man sich darin zurechtfindet und wie man sie bearbeitet, ohne etwas kaputt zu machen.
Die Beispiele stammen von der Figet Marena; die Regeln gelten für jedes Fahrzeug (belegt an Schiff, small Jet,
Rescue Heli und allen Fahrzeugen in `dataehicles`).

- **Original auf Andres PC:** `%APPDATA%\Stormworks\data\vehicles\Figet Marena.xml`
- **Größe:** ca. 5 MB, rund 55 000 Teile, 52 Körper, knapp 900 Kabel.
- **Mehr zum Schiff** (welches Teil wo sitzt, welcher Chip was macht): `SCHIFF_UEBERSICHT.md`, Abschnitt 2 und 4.

---

## 1. Goldene Regeln

1. **Erst sichern:** Vor jedem Schreiben eine Kopie nach `backup\Figet Marena vor <Schritt>.xml` legen.
2. **Spiel beachten:** Das Schiff darf beim Schreiben nicht im Editor offen sein. Danach lädt Andre es im Spiel
   **neu, ohne vorher zu speichern**. Sonst speichert der Editor den alten Stand über deine Änderung.
3. **Datei-Zeit prüfen:** Andre baut parallel. Vor dem Schreiben die Änderungszeit der Datei ansehen. Ist sie neuer
   als dein letzter Stand, die Datei neu einlesen und die Änderung neu anwenden, nie einen alten Stand
   zurückschreiben.
4. **Nur Text ersetzen, nie umformatieren:** Kein „Pretty Print“, kein Einrücken, kein XML-Parser, der die Datei neu
   schreibt. Nur genau die Stelle ändern, die geändert werden soll. Lesen und schreiben als UTF-8, Zeilenenden
   unverändert lassen (in Python `newline=""`).
5. **Probe:** Erst in eine Testdatei schreiben und prüfen, dass sich **nur** das Gewollte geändert hat. Erst dann
   ins Original.
6. **Teile baut Andre selbst** im Spiel-Editor. Per Datei werden nur Kabel, Einstellungen und Microcontroller
   geändert.
7. **Nie in einen Microcontroller hinein einfügen.** Microcontroller enthalten selbst `<components>` und `<c ...>`.
   Neue Teile kommen nur in die oberste Ebene eines Körpers.

---

## 2. Koordinaten

- **Einheit:** 1 Block = 0,25 m. Alle Positionen in der Datei sind ganze Blöcke.
- **Achsen:**
  - **x:** links negativ, rechts positiv.
  - **y:** oben positiv.
  - **z:** Bug positiv, Heck negativ.
- **Ausdehnung:** Rumpf x −19…19, y −21 (Kiel) bis 43 (Mast), z −155 (Heck) bis 69 (Bug).
- **Fehlende Werte sind 0:** `<vp y="17" z="11"/>` heißt (0, 17, 11), `<vp/>` heißt (0, 0, 0).
- **Ein Koordinatensystem:** Alle Körper (Rumpf, Türme, Gelenke, Raketen) und alle Kabel benutzen dasselbe System.

**Ein paar Fixpunkte zum Orientieren:**

| Was | Position |
|---|---|
| Steuersitz | (0,17,−10) |
| Hauptmonitor 9×5 | (0,22,−6) |
| Instrumentenblock (Master Arm usw.) | (−2,19,−8) |
| Physik-Sensor (für alle Waffen-Chips) | (0,27,−38) |
| Chip-Raum (Waffen-Chips an den Wänden x ±5) | um (0,8,−55) |
| Schiffsführungs-Chip | (0,−12,−41) |
| Batterien Medium L/R | (−8,−19,−65) / (8,−19,−65) |
| Getriebe je Seite (A, B, C, Rückwärts) | (±8,−16,−98…−101) |

---

## 3. Aufbau der Datei

Grob, verkürzt:

```xml
<?xml version="1.0" encoding="UTF-8"?><vehicle data_version="3" bodies_id="889">
  <editor_placement_offset .../><authors/>      (im Original mit Steam-Namen; vor dem Hochladen ins Repo durch <authors/> ersetzen)
  <bodies>
    <body unique_id="657"><components> ...alle Teile des Rumpfs... </components></body>
    <body unique_id="791"><components> ... </components></body>      (Türme, Gelenke, Raketen ...)
  </bodies>
  <logic_node_links> ...alle Kabel des ganzen Schiffs... </logic_node_links>
</vehicle>
```

- **Fast alles steht in einer einzigen Zeile.** Nur die Lua-Skripte in den Microcontrollern enthalten echte
  Zeilenumbrüche. Darum nie zeilenweise arbeiten, sondern mit Suchen und Ersetzen im ganzen Text.
- **Der erste Körper (`unique_id="657"`) ist der Rumpf**, mit den weitaus meisten Teilen. Die anderen 51 Körper
  sind Teile hinter Gelenken und Drehkränzen (Türme, Rohre, Kamera-Gelenke) und die 24 Raketen.

### 3.1 Ein Teil (`<c>`)

```xml
<c d="modular_engine_gearbox_1x1"><o r="1,0,0,0,0,1,0,-1,0" bc="969696" ac="969696" sc="6" gear_ratio_2="2"><vp x="-8" y="-16" z="-98"/><logic_slots><slot/><slot/><slot/><slot/></logic_slots></o></c>
```

| Stück | Bedeutung |
|---|---|
| `d="..."` | **Art des Teils** (Name der Spiel-Definition). Fehlt `d`, ist es ein normaler Block. |
| `t="..."` | **Spiegelung** als Bitmaske: 1 = x, 2 = y, 4 = z gespiegelt. Fehlt `t`, ist nichts gespiegelt. |
| `r="..."` | **Drehung** als 3×3-Matrix, zeilenweise (9 Zahlen). **Fehlt `r`, ist es `0,0,1,-1,0,0,0,-1,0`, nicht ungedreht** (siehe unten). |
| `bc`, `ac`, `sc` | Farben und interne Werte. **Nicht anfassen.** |
| weitere Attribute | **Einstellungen** des Teils, z. B. `gear_ratio_2`, `m_fov_x`, `m_sweep_mode` |
| `<vp .../>` | **Position** des Teils (Bezugsblock) |
| `<logic_slots>` | ein `<slot/>` je Anschluss des Teils. Beim Kabel-Legen **nicht** ändern. |
| weitere Kind-Elemente | weitere Einstellungen, z. B. `<m_sweep_speed text="1" value="1"/>` oder beim Instrumentenblock `<display_1 ...>` |

**Ein Teil eindeutig finden:** über Art und Position, z. B. `d="radar_advanced"` und `<vp y="17" z="11"/>`. Die
Position allein reicht nicht, weil bei Gelenken und Drehkränzen zwei Teile auf derselben Stelle liegen können.

**Einstellungen, die man kennen muss:**
- **Getriebe:** `gear_ratio_2` ist ein Index für „Ratio On“: 0 = 1:−1, 1 = 1:1, 2 = 6:5, 3 = 3:2.
- **Radar:** `m_sweep_mode="4"` = manueller Modus; `m_fov_x` / `m_fov_y` = Öffnungswinkel.
- **Instrumentenblock:** jedes Element ist ein `<display_N name="..." channel="K">`.
  - `channel` zählt ab 0: `channel="1"` heißt Bool 2.
  - Ohne `channel` schreibt das Element auf Bool 1. Deshalb lagen früher alle vier Schalter auf Bool 1.
- **Gespiegelte Teile** verhalten sich teils anders: gespiegelte Radare zählen Winkel gespiegelt, gespiegelte
  Drehkränze drehen andersherum.
- `custom_name="..."`: im Editor vergebener Name eines Knopfs oder Teils.

**Drehung `r` genauer** [G]:
- Zeile0 = wohin lokales x zeigt, Zeile1 = lokales y, Zeile2 = lokales z. Lokaler Punkt p → Welt:
  `vp + p.x·Zeile0 + p.y·Zeile1 + p.z·Zeile2`.
- **Fehlt `r`, ist die Drehung `0,0,1,-1,0,0,0,-1,0`** (08.10. aus den Kabeln aller Fahrzeuge bestimmt: erklärt
  122 Teile, die Grunddrehung nur 4). Das Spiel schreibt die Grunddrehung ausdrücklich (`r="1,0,0,0,1,0,0,0,1"`).
  Folge des alten Irrtums: ein Monitor ohne `r` stand senkrecht und kopfüber; Kabel an versetzten Anschlüssen
  zeigten daneben und wurden vom Spiel beim Laden verworfen.
- **Ausdehnung:** Teile aus mehreren Blöcken reichen von `vp + Drehung·voxel_min` bis `voxel_max` (Größen in
  `wissen/bauteile/INDEX.md`). Ein Teil belegt mehr als seinen `vp` – bei der Platzsuche die ganze Ausdehnung rechnen.

**Spiegeln `t` genauer** [G]: Bits 1 = x, 2 = y, 4 = z. Wirkt **lokal, vor der Drehung** (bestätigt an 38 Kabeln,
0 widersprechen). Der Spiegel-Befehl im Editor setzt das Bit der lokalen Achse, die zur Welt-x zeigt.

**Monitore** [G]: Bildseite = lokal +y, Bild-oben = lokal +z, Bild-rechts = lokal −x (von vorn gesehen). Monitore
liegen um `vp` mittig (z. B. 5×3: x −2..2, z −1..1) → 180° um die Bildachse drehen ändert die belegte Fläche nicht.
Auflösung 32 px je Block.

**Anstrich** [G]: `sc="N,RRGGBB,..."` = Farben der Teilflächen; `bc`/`bc2`/`bc3` = Grundfarben (z. B. Rahmen, Türen),
`ac` = Zusatzfarbe. Fenster nur `bc`; Lampen, Anzeigen und Monitore kein `bc`.

### 3.2 Kabel (`<logic_node_links>`)

Alle Kabel stehen am Ende der Datei, für alle Körper gemeinsam:

```xml
<logic_node_link type="4"><voxel_pos_0 x="8" y="-19" z="-65"/><voxel_pos_1 x="15" y="-19" z="-56"/></logic_node_link>
```

- **Richtung:** `voxel_pos_0` ist der **Ausgang** (Quelle), `voxel_pos_1` der **Eingang** (Ziel). Beide sind die
  Weltpositionen der Anschlüsse, nicht die Positionen der Teile.
- **`type`:**

  | type | Kabelart |
  |---|---|
  | fehlt (0) | An/Aus |
  | 1 | Zahl |
  | 4 | Strom |
  | 5 | Composite |
  | 6 | Video |
  | 7 | Ton |
  | 8 | Munitionsgurt / Seil (selten, nicht anfassen) |

- **Mehrere Ausgänge zusammen:** Ein Ausgang darf an viele Eingänge gehen, ein Eingang hat höchstens ein Kabel
  seiner Art.
- **Gleiche Position, verschiedene Anschlüsse:** Auf einem Block können mehrere Anschlüsse liegen (z. B. Strom und
  Drehzahl). Erst `type` und Richtung machen ein Kabel eindeutig.
- **Rohre, Wellen und Riemen** sind **keine** Kabel. Sie verbinden sich nur dadurch, dass die Teile passend
  nebeneinanderstehen. Das gibt es in der Datei nicht als Eintrag.

### 3.3 Microcontroller

Ein Microcontroller ist ein Teil `d="microprocessor"`, in dessen `<o>` die ganze Chip-Definition steckt:

```xml
<c d="microprocessor"><o r="0,-1,0,1,0,0,0,0,1" sc="22"><microprocessor_definition name="Figet Marena Schutz" description="..." width="2" length="3" ...>
  <nodes>
    <n id="1" component_id="1"><node label="Instrumente" mode="1" type="5" description="..."/></n>
    <n id="3" component_id="11"><node label="Chaff links" description="..."><position z="2"/></node></n>
    ...
  </nodes>
  <group> ...Logik-Bausteine, Eigenschaften, Lua-Skripte... </group>
</microprocessor_definition><vp x="-5" y="13" z="-51"/><logic_slots><slot/>...</logic_slots></o></c>
```

- **Anschlüsse (`<node>`):**
  - `mode="1"` = Eingang, fehlt `mode` = Ausgang.
  - `type` wie bei den Kabeln (fehlt = An/Aus).
  - `<position x z>` = Feld auf dem Chip, fehlt sie, ist es Feld (0, 0).
- **Eigenschaften** (die Werte, die man im Editor mit dem Auswahl-Werkzeug sieht):
  `<c type="34"><object id=".." n="Name"><v text="1.5" value="1.5"/></object></c>`.
  Andre ändert Chip-Eigenschaften nicht selbst. Neue Werte kommen per neuer Chip-Version.
- **`sc` eines Chips** = 2·w·l + 2·(w+l) (w, l = Breite, Länge des Chips).
- **Eingebettete Form:** ohne `component_states`/`component_bridge_states`, `mode="0"`/`type="0"` weggelassen.
  Eigenschaften lassen sich direkt in der Datei ändern (`tools/chip_eigenschaft.py`).
- **Lua-Skripte:** stehen im Attribut `script="..."` eines `<c type="56">`.
  - Escaping: `<` als `&lt;`, `>` als `&gt;`, `&` als `&amp;`.
  - Doppelte Anführungszeichen im Lua vermeiden und nur `'...'` benutzen.
  - Zeilenumbrüche sind echt.
  - Höchstens 8192 Zeichen je Skript.
- **Weltposition eines Chip-Anschlusses:** Feld (x, z), Chip-Position vp, Drehung r = (r0 … r8):

  ```
  Welt = ( vp.x + r0*x + r6*z ,  vp.y + r1*x + r7*z ,  vp.z + r2*x + r8*z )
  ```

  Beispiel Schutz-Chip: vp (−5,13,−51), r `0,-1,0,1,0,0,0,0,1` → Feld (x, z) liegt bei (−5, 13−x, −51+z).
- **`<logic_slots>`** des Microcontrollers: genau ein `<slot/>` je `<node>`.
- **Chip tauschen:** Die Anschlüsse müssen in Reihenfolge, Feld und Typ gleich bleiben, sonst passen die Kabel
  nicht mehr. Neue Anschlüsse immer **hinten anhängen**. Der Name in `microprocessor_definition name="..."` ist der
  sicherste Weg, einen Chip zu finden.

### 3.4 Weltposition eines Anschlusses an einem normalen Teil

Wo ein Anschluss eines Teils liegt, steht in der Spiel-Definition des Teils:
`<Spielordner>\rom\data\definitions\<d>.xml` (auf Andres PC
`E:\SteamLibrary\steamapps\common\Stormworks\rom\data\definitions`).

Darin: `<logic_node label="..." mode=".." type=".."><position x y z/></logic_node>`, relativ zum Teil.

1. **Spiegeln:** Für jede Achse i (0 = x, 1 = y, 2 = z), deren Bit in `t` gesetzt ist, `p[i] = −p[i]`.
2. **Drehen:** `q[i] = r[i]*p[0] + r[3+i]*p[1] + r[6+i]*p[2]`.
3. **Verschieben:** Welt = vp + q.

So rechnen Andres Werkzeuge. Die Formel ist an allen eindeutigen Kabeln in der Datei geprüft.

---

## 4. Werkzeug-Bausteine (Python)

Getestet an der Datei vom 04.10.2026. Nur lesen, nichts wird geschrieben.

```python
import os, re

VEH = os.path.join(os.environ["APPDATA"], "Stormworks", "data", "vehicles", "Figet Marena.xml")
s = open(VEH, encoding="utf-8", newline="").read()


def xyz(attr):
    """' x="-8" z="-98"' -> (-8, 0, -98)"""
    d = dict(re.findall(r'(\w)="(-?\d+)"', attr or ""))
    return tuple(int(d.get(k, 0)) for k in "xyz")


def vox(tag, p):
    """('vp', (-8, 0, -98)) -> '<vp x="-8" z="-98"/>'  (Nullen fallen weg, wie im Spiel)"""
    return "<%s%s/>" % (tag, "".join(' %s="%d"' % (k, v) for k, v in zip("xyz", p) if v))


def teile(s):
    """Alle Teile ausser dem Innenleben der Microcontroller: Liste (Art, Position, r, t)."""
    ohne_mc = re.sub(r"<microprocessor_definition.*?</microprocessor_definition>", "", s, flags=re.S)
    out = []
    for m in re.finditer(r'<c(?: d="([^"]+)")?(?: t="(\d+)")?><o ([^>]*)>(?:(?!</c>).)*?<vp([^/]*)/>', ohne_mc, re.S):
        r = re.search(r'r="([^"]*)"', m.group(3))
        rr = [int(float(v)) for v in (r.group(1) if r else "0,0,1,-1,0,0,0,-1,0").split(",")]
        out.append((m.group(1) or "block", xyz(m.group(4)), rr, int(m.group(2) or 0)))
    return out


def kabel(s):
    """Alle Kabel: Liste (Typ, Ausgang-Position, Eingang-Position)."""
    li, le = s.index("<logic_node_links>"), s.index("</logic_node_links>")
    return [(int(t or 0), xyz(a), xyz(b)) for t, a, b in re.findall(
        r'<logic_node_link(?: type="(\d+)")?><voxel_pos_0([^/]*)/><voxel_pos_1([^/]*)/></logic_node_link>', s[li:le])]


def chip_anschluesse(s, name):
    """Anschluesse eines Microcontrollers: {Name: (Weltposition, 'Eingang'/'Ausgang', Typ)}."""
    i = s.index('<microprocessor_definition name="%s"' % name)
    kopf = s[s.rindex('<c d="microprocessor"', 0, i):i]
    r = re.search(r'r="([^"]*)"', kopf)
    r = [int(float(v)) for v in (r.group(1) if r else "0,0,1,-1,0,0,0,-1,0").split(",")]
    e = s.index("</microprocessor_definition>", i)
    vp = xyz(re.match(r"</microprocessor_definition><vp([^/]*)/>", s[e:]).group(1))
    out = {}
    for m in re.finditer(r'<node label="([^"]*)"([^>]*?)(?:/>|><position([^/]*)/></node>)', s[i:e]):
        x, _, z = xyz(m.group(3))
        welt = tuple(vp[k] + r[k] * x + r[6 + k] * z for k in range(3))
        typ = re.search(r'type="(\d+)"', m.group(2))
        out[m.group(1)] = (welt, "Eingang" if 'mode="1"' in m.group(2) else "Ausgang", int(typ.group(1)) if typ else 0)
    return out


# Beispiele
alle = teile(s)
print([t for t in alle if t[0] == "modular_engine_gearbox_1x1"])           # alle Getriebe
print([t for t in alle if t[1] == (0, 27, -38)])                           # was liegt am Physik-Sensor-Platz?
print(chip_anschluesse(s, "Figet Marena Schutz"))                          # Anschluesse des Schutz-Chips
schutz = chip_anschluesse(s, "Figet Marena Schutz")
pos = schutz["Pumpen"][0]
print([k for k in kabel(s) if pos in (k[1], k[2])])                        # Kabel am Anschluss "Pumpen"
print(re.findall(r'<microprocessor_definition name="([^"]*)"', s))         # Namen aller Chips
```

---

## 5. Typische Änderungen

### 5.1 Eine Einstellung eines Teils ändern

1. Das Teil über Art **und** Position finden.
2. Nur innerhalb dieses Teils (von `<c d="..."` bis zum zugehörigen `</o></c>`) ersetzen.
3. Prüfen, dass genau **eine** Stelle geändert wurde.

```python
# Nur zur Erklaerung, NICHT wirklich machen: Getriebe A links von 6:5 (Index 2) auf 3:2 (Index 3)
alt = '<c d="modular_engine_gearbox_1x1"><o r="1,0,0,0,0,1,0,-1,0" bc="969696" ac="969696" sc="6" gear_ratio_2="2"><vp x="-8" y="-16" z="-98"/>'
assert s.count(alt) == 1
neu_s = s.replace(alt, alt.replace('gear_ratio_2="2"', 'gear_ratio_2="3"'))
```

Fehlt ein Attribut (der Wert steht auf Standard), muss es neu eingefügt werden. Die Reihenfolge der Attribute
wie bei gleichartigen Teilen in der Datei halten.

### 5.2 Ein Kabel hinzufügen

1. **Anschlüsse bestimmen:** Weltposition, Richtung und Typ von Ausgang und Eingang ausrechnen (Abschnitt 3.3 / 3.4).
2. **Passt es?** Ausgang wirklich `mode` 0, Eingang `mode` 1, beide gleicher Typ.
3. **Eingang frei?** Es gibt noch kein Kabel dieses Typs an diesem Eingang.
4. **Strom:** Braucht das Zielteil Strom, auch ein Strom-Kabel (type 4) von einer Batterie legen.
5. **Einfügen:** direkt vor `</logic_node_links>`.

```python
k = '<logic_node_link type="1">%s%s</logic_node_link>' % (vox("voxel_pos_0", ausgang), vox("voxel_pos_1", eingang))
assert k not in s
le = s.index("</logic_node_links>")
neu_s = s[:le] + k + s[le:]
```

Für An/Aus-Kabel fällt `type` weg: `<logic_node_link><voxel_pos_0 .../><voxel_pos_1 .../></logic_node_link>`.

### 5.3 Ein Kabel entfernen

Den genauen Text des Kabels suchen (`s.count(k) == 1` prüfen) und durch `""` ersetzen.

### 5.4 Einen Microcontroller ersetzen (neue Version)

1. Den Bereich `<microprocessor_definition name="...">` … `</microprocessor_definition>` des alten Chips durch die
   neue Definition ersetzen.
2. Alles drumherum (`<c d="microprocessor"><o ...>`, `<vp>`, `<logic_slots>`) bleibt.
3. **Vorher prüfen:** Die Liste der `<node>` (Name, mode, type, position) ist am Anfang identisch, neue Anschlüsse
   nur hinten. Sonst hängen die Kabel an falschen Anschlüssen.
4. Kommen neue Anschlüsse dazu, je Anschluss ein `<slot/>` in `<logic_slots>` ergänzen.

### 5.5 Prüfen, dass nur das Gewollte geändert wurde

```python
import difflib
a = s.replace("><", ">\n<").splitlines()
b = neu_s.replace("><", ">\n<").splitlines()
for z in difflib.unified_diff(a, b, lineterm="", n=0):
    print(z)
```

Die Ausgabe darf nur die beabsichtigten Zeilen zeigen. Erst dann schreiben:

```python
open(VEH, "w", encoding="utf-8", newline="").write(neu_s)
```

---

## 6. Häufige Fehler

- **Teil im Chip gefunden statt im Schiff:** In Microcontrollern gibt es auch `<c ...>` und `<components>`. Vor dem
  Suchen die Chip-Definitionen ausblenden (wie in `teile()`).
- **Falscher Körper:** Neue Teile gehören in den Rumpf (erster Körper). Eingefügt wird vor dessen letztem
  `</components>`, nie vor einem `</components>` innerhalb eines Microcontrollers.
- **Kabel an die Teil-Position statt an den Anschluss gelegt:** Ein Anschluss liegt oft einen oder mehrere Blöcke
  neben `vp`. Immer über die Definition rechnen.
- **Gespiegelte Teile** (`t`) vergessen: Dann liegt der Anschluss auf der falschen Seite.
- **Ganze Datei durch einen XML-Parser geschrieben:** Attribut-Reihenfolge, Leerzeichen und Escaping ändern sich.
  Das Spiel lädt es vielleicht noch, aber Andres Werkzeuge finden ihre Textstellen nicht mehr.
- **Datei geschrieben, während Andre gespeichert hat:** Datei-Zeit vorher und direkt vor dem Schreiben prüfen.
- **Nach dem Schreiben im Spiel gespeichert statt neu geladen:** Die Änderung ist weg. Andre daran erinnern.
- **Erfolg behauptet ohne Test:** Ob ein Kabel richtig sitzt, zeigt erst das Spiel. Das ehrlich so sagen und Andre
  sagen, was er prüfen soll.
