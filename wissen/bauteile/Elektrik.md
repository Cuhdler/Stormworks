# Elektrik (Kategorie 10)

Aus den Spieldaten erzeugt von `tools/bauteile_holen.py` - nicht von Hand ändern.

## Electric Battery Large (`battery_large`)

*A large battery array for storing electrical charge.*

- Größe 7x5x5 Blöcke (voxel [-3, -2, -2] .. [3, 2, 2]), Masse 800, Preis 10000, Tags: basic
- Werte: cable_length=-431602080, electric_charge_capacity=256000, electric_type=2, seat_health_per_sec=1, type=31

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Electric Store | Strom | Eingang | (0, 2, 0) | Energy storage for the electrical system. |
| Charge | Zahl | Ausgang | (-1, 2, 0) | Data output giving the charge of the battery from 0 to 1. |

## Electric Battery Medium (`battery_medium`)

*A medium battery for storing electrical charge.*

- Größe 3x2x2 Blöcke (voxel [-1, 0, 0] .. [1, 1, 1]), Masse 60, Preis 1200, Tags: basic
- Werte: cable_length=-431602080, electric_charge_capacity=12800, electric_type=2, seat_health_per_sec=1, type=31

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Electric Store | Strom | Eingang | (0, 1, 1) | Energy storage for the electrical system. |
| Charge | Zahl | Ausgang | (-1, 1, 1) | Data output giving the charge of the battery from 0 to 1. |

## Electric Battery Small (`battery_small`)

*A small battery for storing electrical charge.*

- Größe 2x1x1 Blöcke (voxel [-1, 0, 0] .. [0, 0, 0]), Masse 10, Preis 150, Tags: basic
- Werte: cable_length=-431602080, electric_charge_capacity=1600, electric_type=2, seat_health_per_sec=1, type=31

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Electric Store | Strom | Eingang | (0, 0, 0) | Energy storage for the electrical system. |
| Charge | Zahl | Ausgang | (-1, 0, 0) | Data output giving the charge of the battery from 0 to 1. |

## Electric Charger (`electric_diode`)

*A one-way charger.*
The charger transfers electric one-way between its nodes when there is a significant discrepancy in charge. It can be used to recharge batteries.

- Größe 1x1x2 Blöcke (voxel [0, 0, 0] .. [0, 0, 1]), Masse 1, Preis 100
- Werte: cable_length=-431602080, electric_type=6, seat_health_per_sec=1, type=31

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Electric In | Strom | Ausgang | (0, 0, 0) | Input node for electric. |
| Electric Out | Strom | Ausgang | (0, 0, 1) | Output node for electric. |

## Electric Circuit Breaker (`electric_curcuit_breaker`)

*A circuit breaker for electrical systems.*
When turned on, the circuit breaker closes the circuit, allowing electrical energy to flow between terminals A and B.

- Größe 1x2x1 Blöcke (voxel [0, 0, 0] .. [0, 1, 0]), Masse 1, Preis 100, Tags: basic
- Werte: cable_length=-431602080, electric_type=3, seat_health_per_sec=1, type=31

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Electric A | Strom | Eingang | (0, 0, 0) | Terminal A electrical connection. |
| Electric B | Strom | Eingang | (0, 1, 0) | Terminal B electrical connection. |

## Electric Relay (`electric_relay`)

*A relay for electrical systems.*
When turned on, the relay closes the circuit, allowing electrical energy to flow between terminals A and B.

- Größe 3x1x1 Blöcke (voxel [-1, 0, 0] .. [1, 0, 0]), Masse 1, Preis 100, Tags: basic
- Werte: cable_length=-431602080, electric_type=4, seat_health_per_sec=1, type=31

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Electric A | Strom | Ausgang | (-1, 0, 0) | Terminal A electrical connection. |
| Electric B | Strom | Ausgang | (1, 0, 0) | Terminal B electrical connection. |
| Relay State | An/Aus | Eingang | (0, 0, 0) | Input to set if the electrical connection is made. |

## Large Generator (`generator_large`)

*A large generator unit for converting mechanical power to electricity.*

- Größe 5x5x5 Blöcke (voxel [-2, -2, -2] .. [2, 2, 2]), Masse 400, Preis 12000, Tags: basic
- Werte: cable_length=-431602080, electric_charge_capacity=100, electric_magnitude=0.85, electric_type=1, force_emitter_max_force=125, seat_health_per_sec=1, type=31

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| RPS | Drehmoment | Eingang | (0, -2, 0) | The torque power input to convert to electric energy. |
| Electric | Strom | Eingang | (0, 2, 0) | The electric connection to output electric energy. |
| Output | Zahl | Ausgang | (0, 0, 0) | Data output giving the electrical generation of the generator. |

## Large Solar Cell (`solar_large`)

*A large solar cell for generating electricity.*
The cell generates electrical current based on time of day and angle towards the sun.

- Größe 5x1x5 Blöcke (voxel [-2, 0, -2] .. [2, 0, 2]), Masse 40, Preis 8000, Tags: basic
- Werte: electric_type=5, type=31

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Electric | Strom | Eingang | (0, 0, 0) | The electric connection to output electric energy. |

## Medium Generator (`generator_medium`)

*A medium generator unit for converting mechanical power to electricity.*

- Größe 3x3x3 Blöcke (voxel [-1, -1, -1] .. [1, 1, 1]), Masse 100, Preis 2000, Tags: basic
- Werte: cable_length=-431602080, electric_charge_capacity=10, electric_magnitude=0.75, electric_type=1, force_emitter_max_force=30, seat_health_per_sec=1, type=31

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| RPS | Drehmoment | Eingang | (0, -1, 0) | The torque power input to convert to electric energy. |
| Electric | Strom | Eingang | (0, 1, 0) | The electric connection to output electric energy. |
| Output | Zahl | Ausgang | (0, 0, 0) | Data output giving the electrical generation of the generator. |

## Small Generator (`generator_small`)

*A small generator unit for converting mechanical power to electricity.*

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 5, Preis 600, Tags: basic
- Werte: cable_length=-431602080, electric_charge_capacity=1, electric_magnitude=0.6, electric_type=1, force_emitter_max_force=1, seat_health_per_sec=1, type=31

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| RPS | Drehmoment | Eingang | (0, 0, 0) | The torque power input to convert to electric energy. |
| Electric | Strom | Eingang | (0, 0, 0) | The electric connection to output electric energy. |
| Output | Zahl | Ausgang | (0, 0, 0) | Data output giving the electrical generation of the generator. |

## Solar Cell (`solar`)

*A solar cell for generating electricity.*
The cell generates electrical current based on time of day and angle towards the sun.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 2, Preis 400, Tags: basic
- Werte: electric_type=5, type=31

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Electric | Strom | Eingang | (0, 0, 0) | The electric connection to output electric energy. |
