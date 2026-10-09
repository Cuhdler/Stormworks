# Modulare-Motoren (Kategorie 13)

Aus den Spieldaten erzeugt von `tools/bauteile_holen.py` - nicht von Hand ändern.

## Modular Engine Air Manifold (`modular_engine_air_manifold`)

*A modular engine air manifold.*
Attach a manifold to a cylinder to provide a connection for air to that cylinder. Cylinders that are chained directly adjacent to each other can share a single manifold.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 10
- Werte: cable_length=-431602080, engine_module_type=28, type=52

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Throttle | Zahl | Eingang | (0, 0, 0) |  |
| Air | Fluessigkeit/Gas | Eingang | (0, 0, 0) |  |

## Modular Engine Alternator (`modular_engine_alternator`)

*A modular engine alternator.*
Alternators convert mechanical energy from a Drive Belt into electric charge.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 30
- Werte: cable_length=-431602080, electric_magnitude=0.05, electric_type=1, engine_max_force=0.5, engine_module_type=5, force_emitter_max_force=100, type=52

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Clutch Pressure | Zahl | Eingang | (0, 0, 0) |  |
| Electric | Strom | Ausgang | (0, 0, 0) |  |

## Modular Engine Clutch 1x1 (`modular_engine_clutch`)

*A modular engine clutch.*
Attach a clutch to a crankshaft block to control the torque made available to the connected system.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 15
- Werte: cable_length=-431602080, electric_magnitude=1, engine_max_force=0.6, engine_module_type=3, force_emitter_max_force=200, type=52

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Clutch Pressure | Zahl | Eingang | (0, 0, 0) |  |
| RPS | Drehmoment | Eingang | (0, 0, 0) | The power supplied by the engine for inputting to other components. |

## Modular Engine Clutch 3x3 (`modular_engine_clutch_3x3`)

*A modular engine clutch.*
Attach a clutch to a crankshaft block to control the torque made available to the connected system.

- Größe 3x1x3 Blöcke (voxel [-1, 0, -1] .. [1, 0, 1]), Masse 9, Preis 25
- Werte: cable_length=-431602080, electric_magnitude=1, engine_max_force=5, engine_module_type=21, force_emitter_max_force=2000, type=52

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Clutch Pressure | Zahl | Eingang | (0, 0, 0) |  |
| RPS | Drehmoment | Eingang | (0, 0, 0) | The power supplied by the engine for inputting to other components. |

## Modular Engine Clutch 5x5 (`modular_engine_clutch_5x5`)

*A modular engine clutch.*
Attach a clutch to a crankshaft block to control the torque made available to the connected system.

- Größe 5x1x5 Blöcke (voxel [-2, 0, -2] .. [2, 0, 2]), Masse 25, Preis 50
- Werte: cable_length=-431602080, electric_magnitude=1, engine_max_force=10, engine_module_type=26, force_emitter_max_force=20000, type=52

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Clutch Pressure | Zahl | Eingang | (0, 0, 0) |  |
| RPS | Drehmoment | Eingang | (0, 0, 0) | The power supplied by the engine for inputting to other components. |

## Modular Engine Coolant Manifold (`modular_engine_coolant_manifold`)

*A modular engine coolant manifold.*
Attach a manifold to a cylinder to provide a connection for coolant to that cylinder. Cylinders that are chained directly adjacent to each other can share a single manifold.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 10
- Werte: cable_length=-431602080, engine_module_type=8, type=52

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Coolant A | Fluessigkeit/Gas | Eingang | (0, 0, 0) |  |
| Coolant B | Fluessigkeit/Gas | Ausgang | (0, 0, 0) |  |

## Modular Engine Crankshaft 1x1 (`modular_engine_crankshaft`)

*A modular engine crankshaft block.*
The crankshaft is the core of an engine. Attach cylinders to the outer surfaces to generate power. Multiple crankshaft blocks can be placed adajcent to each other to form larger engines.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 50
- Werte: cable_length=-431602080, engine_max_force=0.7, type=52

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| RPS | Zahl | Ausgang | (0, 0, 0) | Output value giving data info on engine speed. |

## Modular Engine Crankshaft 3x1 (`modular_engine_crankshaft_3x1`)

*A modular engine crankshaft block.*
The crankshaft is the core of an engine. Attach cylinders to the outer surfaces to generate power. Multiple crankshaft blocks can be placed adajcent to each other to form larger engines.

- Größe 3x1x3 Blöcke (voxel [-1, 0, -1] .. [1, 0, 1]), Masse 9, Preis 50
- Werte: cable_length=-431602080, engine_max_force=8, engine_module_type=18, type=52

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| RPS | Zahl | Ausgang | (0, 0, 0) | Output value giving data info on engine speed. |

## Modular Engine Crankshaft 3x3 (`modular_engine_crankshaft_3x3`)

*A modular engine crankshaft block.*
The crankshaft is the core of an engine. Attach cylinders to the outer surfaces to generate power. Multiple crankshaft blocks can be placed adajcent to each other to form larger engines.

- Größe 3x3x3 Blöcke (voxel [-1, -1, -1] .. [1, 1, 1]), Masse 27, Preis 150
- Werte: cable_length=-431602080, engine_max_force=15, engine_module_type=19, type=52

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| RPS | Zahl | Ausgang | (0, 0, 0) | Output value giving data info on engine speed. |

## Modular Engine Crankshaft 5x5 (`modular_engine_crankshaft_5x5`)

*A modular engine crankshaft block.*
The crankshaft is the core of an engine. Attach cylinders to the outer surfaces to generate power. Multiple crankshaft blocks can be placed adajcent to each other to form larger engines.

- Größe 5x5x5 Blöcke (voxel [-2, -2, -2] .. [2, 2, 2]), Masse 100, Preis 350
- Werte: cable_length=-431602080, engine_max_force=25, engine_module_type=25, type=52

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| RPS | Zahl | Ausgang | (0, 0, 0) | Output value giving data info on engine speed. |

## Modular Engine Crankshaft Converter 3 to 1 (`modular_engine_crankshaft_converter_3x3`)

*A modular engine crankshaft block.*
The crankshaft is the core of an engine. This component efficiently converts torque between different size crankshafts. Multiple crankshaft blocks can be placed adajcent to each other to form larger engines.

- Größe 3x1x3 Blöcke (voxel [-1, 0, -1] .. [1, 0, 1]), Masse 9, Preis 75
- Werte: cable_length=-431602080, engine_max_force=8.0, engine_module_type=20, type=52

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| RPS | Zahl | Ausgang | (0, 0, 0) | Output value giving data info on engine speed. |

## Modular Engine Crankshaft Converter 5 to 3 (`modular_engine_crankshaft_converter_5x5`)

*A modular engine crankshaft block.*
The crankshaft is the core of an engine. This component efficiently converts torque between different size crankshafts. Multiple crankshaft blocks can be placed adajcent to each other to form larger engines.

- Größe 5x1x5 Blöcke (voxel [-2, 0, -2] .. [2, 0, 2]), Masse 27, Preis 275
- Werte: cable_length=-431602080, engine_max_force=15, engine_module_type=24, type=52

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| RPS | Zahl | Ausgang | (0, 0, 0) | Output value giving data info on engine speed. |

## Modular Engine Cylinder 1x1 (`modular_engine_cylinder_straight`)

*A modular engine cylinder.*
Attach a cylinder to a crankshafts outer surface to produce power for an engine. The cylinder requires a manifold to move air, fuel, and exhaust through the cylinder. Cylinders that are chained directly adjacent to each other can share a single manifold.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 50
- Werte: cable_length=-431602080, engine_max_force=0.6, engine_module_type=1, type=52

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Composite Data | Composite | Ausgang | (0, 0, 0) | Outputs data from the cylinder. (Value 1 : Air Volume) (Value 2 : Fuel Volume) (Value 3 : Temperature) |

## Modular Engine Cylinder 3x3 (`modular_engine_piston_3x3`)

*A modular engine cylinder.*
Attach a cylinder to a crankshafts outer surface to produce power for an engine. The cylinder requires a manifold to move air, fuel, and exhaust through the cylinder. Cylinders that are chained directly adjacent to each other can share a single manifold.

- Größe 3x3x3 Blöcke (voxel [-1, -1, -1] .. [1, 1, 1]), Masse 27, Preis 100
- Werte: cable_length=-431602080, engine_max_force=12, engine_module_type=22, type=52

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Composite Data | Composite | Ausgang | (0, 1, 0) | Outputs data from the cylinder. (Value 1 : Air Volume) (Value 2 : Fuel Volume) (Value 3 : Temperature) |

## Modular Engine Cylinder 5x5 (`modular_engine_piston_5x5`)

*A modular engine cylinder.*
Attach a cylinder to a crankshafts outer surface to produce power for an engine. The cylinder requires a manifold to move air, fuel, and exhaust through the cylinder. Cylinders that are chained directly adjacent to each other can share a single manifold.

- Größe 5x5x5 Blöcke (voxel [-2, -2, -2] .. [2, 2, 2]), Masse 100, Preis 150
- Werte: cable_length=-431602080, engine_max_force=15, engine_module_type=27, type=52

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Composite Data | Composite | Ausgang | (0, 2, 0) | Outputs data from the cylinder. (Value 1 : Air Volume) (Value 2 : Fuel Volume) (Value 3 : Temperature) |

## Modular Engine Drive Belt 1x1 (`modular_engine_drive_belt`)

*A modular engine drive belt.*
The drive belt attaches to the crankshaft and provides an interface for starters, alternators and pumps.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 30
- Werte: cable_length=-431602080, electric_magnitude=1, engine_max_force=0.6, engine_module_type=4, type=52

## Modular Engine Drive Belt 3x3 (`modular_engine_power_manifold_3x3`)

*A modular engine drive belt.*
The drive belt attaches to the crankshaft and provides an interface for starters, alternators and pumps.

- Größe 3x1x3 Blöcke (voxel [-1, 0, -1] .. [1, 0, 1]), Masse 9, Preis 80
- Werte: cable_length=-431602080, engine_max_force=5, engine_module_type=17, type=52

## Modular Engine Drive Belt 5x5 (`modular_engine_power_manifold_5x5`)

*A modular engine drive belt.*
The drive belt attaches to the crankshaft and provides an interface for starters, alternators and pumps.

- Größe 5x1x5 Blöcke (voxel [-2, 0, -2] .. [2, 0, 2]), Masse 27, Preis 160
- Werte: cable_length=-431602080, engine_max_force=5, engine_module_type=23, type=52

## Modular Engine Exhaust Manifold (Corner) (`modular_engine_exhaust_manifold_corner`)

*A modular engine manifold.*
Attach a manifold to a cylinder to provide an exhaust output connection for that cylinder. Cylinders that are chained directly adjacent to each other can share a single manifold.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 10
- Werte: cable_length=-431602080, engine_module_type=10, type=52

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Exhaust | Fluessigkeit/Gas | Ausgang | (0, 0, 0) |  |

## Modular Engine Exhaust Manifold (Straight) (`modular_engine_exhaust_manifold_straight`)

*A modular engine manifold.*
Attach a manifold to a cylinder to provide an exhaust output connection for that cylinder. Cylinders that are chained directly adjacent to each other can share a single manifold.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 10
- Werte: cable_length=-431602080, engine_module_type=11, type=52

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Exhaust | Fluessigkeit/Gas | Ausgang | (0, 0, 0) |  |

## Modular Engine Fluid Pump (`modular_engine_fluid_pump`)

*A modular engine fluid pump.*
An pump that attaches to a Drive Belt to mechanically push fluid around a system.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 50
- Werte: cable_length=-431602080, engine_max_force=0.5, engine_module_type=6, type=52

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Clutch Pressure | Zahl | Eingang | (0, 0, 0) |  |
| Fluid In | Fluessigkeit/Gas | Eingang | (0, 0, 0) |  |
| Fluid Out | Fluessigkeit/Gas | Ausgang | (0, 0, 0) |  |

## Modular Engine Flywheel 1x1 (`modular_engine_flywheel`)

*A modular engine crankshaft flywheel.*
The crankshaft is the core of an engine. A flywheel piece sits as part of the crankshaft and acts as a momentum (energy) store for a running engine, but also makes the engine harder to start.

- Größe 3x1x3 Blöcke (voxel [-1, 0, -1] .. [1, 0, 1]), Masse 100, Preis 450
- Werte: cable_length=-431602080, engine_frictionless_force=150, engine_max_force=150, type=52

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| RPS | Zahl | Ausgang | (0, 0, 0) | Output value giving data info on engine speed. |

## Modular Engine Flywheel 3x3 (`modular_engine_flywheel_3x3`)

*A modular engine crankshaft flywheel.*
The crankshaft is the core of an engine. A flywheel piece sits as part of the crankshaft and acts as a momentum (energy) store for a running engine, but also makes the engine harder to start.

- Größe 5x1x5 Blöcke (voxel [-2, 0, -2] .. [2, 0, 2]), Masse 200, Preis 650
- Werte: cable_length=-431602080, engine_frictionless_force=600, engine_max_force=600, engine_module_type=19, type=52

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| RPS | Zahl | Ausgang | (0, 0, 0) | Output value giving data info on engine speed. |

## Modular Engine Flywheel 5x5 (`modular_engine_flywheel_5x5`)

*A modular engine crankshaft flywheel.*
The crankshaft is the core of an engine. A flywheel piece sits as part of the crankshaft and acts as a momentum (energy) store for a running engine, but also makes the engine harder to start.

- Größe 7x1x7 Blöcke (voxel [-3, 0, -3] .. [3, 0, 3]), Masse 300, Preis 850
- Werte: cable_length=-431602080, engine_frictionless_force=2400, engine_max_force=2400, engine_module_type=25, type=52

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| RPS | Zahl | Ausgang | (0, 0, 0) | Output value giving data info on engine speed. |

## Modular Engine Fuel Manifold (`modular_engine_intake_manifold`)

*A modular engine fuel manifold.*
Attach a manifold to a cylinder to provide a connection for fuel to that cylinder. Cylinders that are chained directly adjacent to each other can share a single manifold.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 10
- Werte: cable_length=-431602080, engine_module_type=9, type=52

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Throttle | Zahl | Eingang | (0, 0, 0) |  |
| Fuel | Fluessigkeit/Gas | Eingang | (0, 0, 0) |  |

## Modular Engine Manifold (Corner) (`modular_engine_manifold_corner`)

*A modular engine manifold.*
Attach a manifold to a cylinder to provide connections for air, fuel, and exhaust for that cylinder. Cylinders that are chained directly adjacent to each other can share a single manifold.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 10
- Werte: cable_length=-431602080, engine_module_type=13, type=52

## Modular Engine Manifold (Straight) (`modular_engine_manifold_straight`)

*A modular engine manifold.*
Attach a manifold to a cylinder to provide connections for air, fuel, and exhaust for that cylinder. Cylinders that are chained directly adjacent to each other can share a single manifold.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 10
- Werte: cable_length=-431602080, engine_module_type=14, type=52

## Modular Engine Manifold (T) (`modular_engine_manifold_t`)

*A modular engine manifold.*
Attach a manifold to a cylinder to provide connections for air, fuel, and exhaust for that cylinder. Cylinders that are chained directly adjacent to each other can share a single manifold.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 10
- Werte: cable_length=-431602080, engine_module_type=15, type=52

## Modular Engine Starter (`modular_engine_starter`)

*A modular engine starter.*
Attach a starter to a Drive Belt component and supply power to apply an inefficient force on the engine to get it started.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 30
- Werte: cable_length=-431602080, electric_magnitude=0.2, electric_type=1, engine_max_force=0.5, engine_module_type=7, type=52

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Starter | An/Aus | Eingang | (0, 0, 0) |  |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Modular Engine Temperature Sensor (`modular_engine_sensor_temperature`)

*A modular engine temperature sensor.*
Attach to a crankshaft to provide temperature information.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 50
- Werte: cable_length=-431602080, electric_magnitude=0.05, electric_type=1, engine_module_type=16, type=52

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Temperature | Zahl | Ausgang | (0, 0, 0) |  |
