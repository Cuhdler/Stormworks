# Strom

Aus dem Wiki (Seite „Electricity“, Stand v1.15.2, August 2025) in eigenen Worten [W], plus eigene Befunde [G].

## Einheiten [W]

- Keine echten Einheiten. „Spannung“ = Ladestand der Batterie (0..1, „SV“): bei halber Ladung laufen Motoren halb so
  schnell. Über 1 geht nicht → Reihen- oder Parallelschaltung von Batterien ist egal.
- Leistung in „Swatt“, Energie in „Swatt-Sekunden“ (SWs).
- Mit „Strom unendlich“ in den Einstellungen läuft alles voll, egal was angeschlossen ist.

## Batterien [W]

| Batterie | Speicher | Preis | Masse | Größe |
|---|---|---|---|---|
| klein | 1 600 SWs | 150 $ | 10 | 1×2×1 |
| mittel | 12 800 SWs | 1 200 $ | 60 | 3×2×2 |
| groß | 256 000 SWs | 10 000 $ | 800 | 7×5×5 |
| Hardpoint-Anschluss | 300 SWs | 20 $ | 2 | 1×1×2 |

Große Batterien sind leichter und kleiner je Energie als mehrere kleine. Batterie-Ausgang „Charge“ = Ladung 0..1 [S].
Alle über Strom-Kabel verbundenen Batterien bilden ein Netz (Figet Marena: alle 6 in einem Netz) [G].

## Erzeugen [W]

- **Generator: Leistung = Drehzahl² × Konstante.** Konstanten: klein 0,00642 (1×1×1, 600 $), mittel 0,241 (3×3×3),
  groß 1,138 (5×5×5), Lichtmaschine (Modular) 0,0054. Beispiel: kleiner Generator bei 13,73 RPS → 1,21 Swatt.
- Solarzelle 1×1: höchstens 0,0027 Swatt (Sonne direkt, kein Regen/Nebel), nachts nichts; groß 5×5: 0,068.
- Ladesäule an der Werkbank: bis 400 Swatt (eine leere Batterie), wird gegen voll langsamer.
- Elektro-Lader: überträgt bis 0,6 Swatt zwischen zwei Netzen, abhängig von der Quell-Ladung.

## Verbrauch bei voller Ladung [W]

| Teil | Swatt |
|---|---|
| Schweißgerät (fest) | 30,2 |
| RX Directional groß an / aus | 23,8 / 5,49 |
| RX Directional an / aus | 18,3 / 3,66 |
| Radar AWACS / Schüssel / Phalanx / einfach / Raketen | 2,75 / 0,92 / 0,60 / 0,37 / 0,13 |
| Heizung | 0,065 |
| Radio RX Huge / Large / Medium / Small | 0,054 / 0,014 / 0,0057 / 0,0057 |
| Kamera mittel / klein | 0,057 |
| Video-Sender | 0,0057 |
| Transponder, Lampe, Suchscheinwerfer, Rundumlicht | 0,011 |
| Knöpfe | 0 |
| Anlasser Diesel groß / mittel / klein | 35,7–600 / 11–600 / 3,66–340 (ohne bis mit Last) |

## Stromausfall [W]

- Blitz in der Nähe, Fahrzeug über 120 m Höhe: ~10 s kein Strom, Sicherungen fliegen raus.
- EMP: ~500 m Wirkung, Motoren aus (auch bei fester Gas-Zahl), nach 55 s kommt Strom zurück, nach 60 s voll.
- Beschädigte Batterien liefern nichts mehr (auch repariert leer → nachladen).
- Hoher Verbrauch (Anlasser) lässt andere Teile kurz schwächer laufen (Lampen flackern).
- Folgen: Elektromotoren langsamer, Anlasser zu schwach (Motor braucht ≥ 2 RPS), Lampen aus,
  **elektrische Türen/Luken gehen ohne Strom AUF** (Dichtigkeit!), Knöpfe/Hebel ohne Strom nicht bedienbar (außer
  Tastenfeld, Chip, Steuersitz).

## Tipps [W]

- Beim Anlassen Kupplung auf 0, erst über 3 RPS einkuppeln (spart Strom, Motor kommt besser).
- Sicherung (Circuit Breaker) zwischen Batterie und Verbrauchern: offen = nichts verbraucht (Fahrzeug bleibt startbar).
- Flugzeug gegen EMP/Blitz: Fallschirm, der bei Stromausfall auslöst (z. B. Laser misst dann 0, Verzögerung > 10 s).
