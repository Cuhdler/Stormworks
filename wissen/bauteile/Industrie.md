# Industrie (Kategorie 14)

Aus den Spieldaten erzeugt von `tools/bauteile_holen.py` - nicht von Hand ändern.

## Duct (`steam_coal_duct`)

*A basic resource duct.*
Transports resources through the connected system.

- Größe 3x3x3 Blöcke (voxel [-1, -1, -1] .. [1, 1, 1]), Masse 12, Preis 50, Tags: steam,coal,fishing
- Werte: cable_length=-431602080, seat_health_per_sec=1, steam_component_capacity=42.1875, steam_component_type=7, type=53

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Fill Level | Zahl | Ausgang | (0, 0, 0) |  |

## Duct Large (`steam_coal_duct_l`)

*A basic resource duct.*
Transports resources through the connected system.

- Größe 5x5x9 Blöcke (voxel [-2, -2, -4] .. [2, 2, 4]), Masse 112, Preis 150, Tags: steam,coal,fishing
- Werte: cable_length=-431602080, seat_health_per_sec=1, steam_component_capacity=351.5625, steam_component_type=7, type=53

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Fill Level | Zahl | Ausgang | (0, 0, 0) |  |

## Duct Medium (`steam_coal_duct_m`)

*A basic resource duct.*
Transports resources through the connected system.

- Größe 5x5x5 Blöcke (voxel [-2, -2, -2] .. [2, 2, 2]), Masse 62, Preis 100, Tags: steam,coal,fishing
- Werte: cable_length=-431602080, seat_health_per_sec=1, steam_component_capacity=195.3125, steam_component_type=7, type=53

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Fill Level | Zahl | Ausgang | (0, 0, 0) |  |

## Electric Furnace (`furnace_electric`)

*An electrically powered furnace.*
Produces large amounts of heat from electricity.

- Größe 3x5x3 Blöcke (voxel [-1, -2, -1] .. [1, 2, 1]), Masse 220, Preis 900, Tags: firebox
- Werte: steam_component_type=11, type=53

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Temperature | Zahl | Ausgang | (0, 0, 0) | Temperature of the coolant that is being heated. |
| Enable | An/Aus | Eingang | (0, -1, 0) | Activate the electric furnace. |
| Coolant In | Fluessigkeit/Gas | Eingang | (0, 2, 0) | In port for fluid to be heated by the furnace. |
| Coolant Out | Fluessigkeit/Gas | Eingang | (0, -2, 0) | Out port for fluid to be heated by the furnace. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Firebox (`steam_coal_firebox`)

*A coal powered firebox.*
Produces large amounts of heat. Can be supplied with a mineral duct. Consumes 1 coal to ignite the fire.

- Größe 3x3x5 Blöcke (voxel [-1, -1, -2] .. [1, 1, 2]), Masse 100, Preis 100, Tags: steam,coal
- Werte: steam_component_type=4, type=53

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Coal Level | Zahl | Ausgang | (0, 1, 0) |  |
| Temperature | Zahl | Ausgang | (0, 0, 0) | Temperature of the coolant that is being heated. |
| Ignition | An/Aus | Eingang | (0, -1, 0) | Activate to consume a coal and ignite the firebox. |
| Coolant In | Fluessigkeit/Gas | Eingang | (-1, -1, -1) | In port for fluid to be heated by the firebox. |
| Coolant Out | Fluessigkeit/Gas | Eingang | (-1, -1, 1) | Out port for fluid to be heated by the firebox. |
| Air | Fluessigkeit/Gas | Eingang | (-1, 1, -1) | Port for supplying air to the fire. |
| Exhaust | Fluessigkeit/Gas | Ausgang | (-1, 1, 1) | Port for removing exhaust from burnt coal. |

## Firebox Large (`steam_coal_firebox_l`)

*A coal powered firebox.*
Produces large amounts of heat. Can be supplied with a duct. Consumes 1 coal to ignite the fire.

- Größe 5x5x7 Blöcke (voxel [-2, -2, -3] .. [2, 2, 3]), Masse 400, Preis 200, Tags: steam,coal
- Werte: steam_component_type=4, type=53

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Coal Level | Zahl | Ausgang | (0, 1, 0) |  |
| Temperature | Zahl | Ausgang | (0, 0, 0) | Temperature of the coolant that is being heated. |
| Ignition | An/Aus | Eingang | (0, -1, 0) | Activate to consume a coal and ignite the firebox. |
| Coolant In | Fluessigkeit/Gas | Eingang | (-2, -1, -1) | In port for fluid to be heated by the firebox. |
| Coolant Out | Fluessigkeit/Gas | Eingang | (-2, -1, 1) | Out port for fluid to be heated by the firebox. |
| Air | Fluessigkeit/Gas | Eingang | (-2, 1, -1) | Port for supplying air to the fire. |
| Exhaust | Fluessigkeit/Gas | Ausgang | (-2, 1, 1) | Port for removing exhaust from burnt coal. |

## Flexible Duct (`steam_coal_flex`)

*A flexible resource duct.*
Transports resources through the connected system. Flexible ducts can be connected together by rope nodes to transfer resources.

- Größe 3x2x3 Blöcke (voxel [-1, 0, -1] .. [1, 1, 1]), Masse 20, Preis 50, Tags: steam,coal,fishing
- Werte: cable_length=-431602080, logic_gate_subtype=12, seat_health_per_sec=1, steam_component_type=14, type=53

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Duct | Seil/Munition | Eingang | (0, 0, 0) |  |

## Funnel Duct (`steam_coal_funnel`)

*A funnel for moving resources.*
Can be toggled to slowly move resources out of the connected system.

- Größe 3x2x3 Blöcke (voxel [-1, 0, -1] .. [1, 1, 1]), Masse 20, Preis 50, Tags: steam,coal,fishing
- Werte: cable_length=-431602080, seat_health_per_sec=1, steam_component_type=6, type=53

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Open | An/Aus | Eingang | (0, 0, 0) |  |

## Hopper (`steam_coal_hopper`)

*A hopper that can accept bulk minerals, ingots, and fish.*
Pouring resources into the receptacle will add it to the connected system.

- Größe 3x3x3 Blöcke (voxel [-1, -1, -1] .. [1, 1, 1]), Masse 12, Preis 50, Tags: steam,coal,fishing
- Werte: cable_length=-431602080, seat_health_per_sec=1, steam_component_type=5, type=53

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Fill Level | Zahl | Ausgang | (0, 0, 0) |  |

## Hopper Large (`steam_coal_hopper_l`)

*A hopper that can accept bulk minerals, ingots, and fish.*
Pouring resources into the receptacle will add it to the connected system.

- Größe 5x5x9 Blöcke (voxel [-2, -2, -4] .. [2, 2, 4]), Masse 112, Preis 150, Tags: steam,coal,fishing
- Werte: cable_length=-431602080, seat_health_per_sec=1, steam_component_type=5, type=53

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Fill Level | Zahl | Ausgang | (0, 0, 0) |  |

## Hopper Medium (`steam_coal_hopper_m`)

*A hopper that can accept bulk minerals, ingots, and fish.*
Pouring resources into the receptacle will add it to the connected system.

- Größe 5x5x5 Blöcke (voxel [-2, -2, -2] .. [2, 2, 2]), Masse 62, Preis 100, Tags: steam,coal,fishing
- Werte: cable_length=-431602080, seat_health_per_sec=1, steam_component_type=5, type=53

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Fill Level | Zahl | Ausgang | (0, 0, 0) |  |

## Industrial Diesel Furnace (`furnace_industrial`)

*A diesel powered furnace.*
Produces large amounts of heat by burning supplied diesel. Consumes a portion of the diesel reserve to ignite the fire.

- Größe 5x5x7 Blöcke (voxel [-2, -2, -3] .. [2, 2, 3]), Masse 350, Preis 750, Tags: firebox
- Werte: steam_component_type=12, type=53

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Diesel Level | Zahl | Ausgang | (0, 1, 0) |  |
| Temperature | Zahl | Ausgang | (0, 0, 0) | Temperature of the coolant that is being heated. |
| Ignition | An/Aus | Eingang | (0, -1, 0) | Activate to consume diesel and ignite the furnace. |
| Coolant In | Fluessigkeit/Gas | Eingang | (-2, -1, -1) | In port for fluid to be heated by the furnace. |
| Coolant Out | Fluessigkeit/Gas | Eingang | (-2, -1, 1) | Out port for fluid to be heated by the furnace. |
| Air In | Fluessigkeit/Gas | Eingang | (-2, 1, -1) | Port for supplying air. |
| Exhaust Out | Fluessigkeit/Gas | Ausgang | (-2, 1, 1) | Port for removing exhaust from the furnace. |
| Diesel In | Fluessigkeit/Gas | Eingang | (0, 0, -3) | Port for supplying diesel fuel. |

## Lobster Pot (`lobster_pot`)

*A trap for lobsters and crabs.*
A portable trap for catching lobsters and crabs on the sea floor.

- Größe 5x3x5 Blöcke (voxel [-2, -1, -2] .. [2, 1, 2]), Masse 45, Preis 150, Tags: crab,fishing
- Werte: type=63

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Release | An/Aus | Eingang | (0, 0, 0) | When on, releases captured crabs and lobsters. When off, keeps them contained. |
| Fill Level | Zahl | Ausgang | (0, -1, 0) |  |

## Mineral Converter (`mineral_converter`)

*A basic mineral duct.*
Transports minerals through the connected system.

- Größe 3x3x3 Blöcke (voxel [-1, -1, -1] .. [1, 1, 1]), Masse 80, Preis 250000, Tags: steam,coal
- Werte: steam_component_type=8, type=53

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Mineral Level | Zahl | Ausgang | (0, 0, 0) |  |
| water | Fluessigkeit/Gas | Eingang | (0, 1, 0) |  |

## Net Anchor (`rope_hook_net`)

*An anchor point for a fishing net.*
Draw a rope logic link between four Net Anchors in a loop to form a net.

- Größe 1x3x1 Blöcke (voxel [0, -1, 0] .. [0, 1, 0]), Masse 3, Preis 15, Tags: basic,fishing
- Werte: force_emitter_blade_physics_length=4.1, force_emitter_default_pitch=1, force_emitter_max_force=10000, logic_gate_subtype=7, type=48

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Net Node | Seil/Munition | Eingang | (0, 1, 0) |  |
| Release Catch | An/Aus | Eingang | (0, 1, 0) |  |
| Extend | An/Aus | Eingang | (0, 0, 0) |  |
| Retract | An/Aus | Eingang | (0, -1, 0) |  |
| Net Data | Composite | Ausgang | (0, 0, 0) | Outputs attached net data. Value 1: net fill level, Value 2: net extend factor. |

## Nuclear Control Rod (`steam_nuclear_control_rod`)

*A Control Rod.*
Can be inserted into a fuel assembly to decrease the rate of reaction of adjacent rods.

- Größe 1x17x1 Blöcke (voxel [0, -8, 0] .. [0, 8, 0]), Masse 100, Preis 250, Tags: reactor
- Werte: cable_length=-431602080, nuclear_component_type=2, seat_health_per_sec=1, steam_component_type=10, type=54

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Insertion Target | Zahl | Eingang | (0, 0, 0) |  |
| Insertion | Zahl | Ausgang | (0, 1, 0) |  |

## Nuclear Fuel Assembly (`steam_nuclear_fuel_assembly`)

*A Fuel assembly powered by uranium ingots.*
A fuel rod can be inserted into the assembly to facilitate a fission reaction. Fuel rods consume uranium ingots from the workbench inventory to fuel.

- Größe 1x12x1 Blöcke (voxel [0, -5, 0] .. [0, 6, 0]), Masse 80, Preis 500, Tags: reactor
- Werte: cable_length=-431602080, seat_health_per_sec=1, steam_component_type=8, type=54

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Release Fuel Rod | An/Aus | Eingang | (0, 1, 0) |  |
| Fuel Rod Temperature | Zahl | Ausgang | (0, 0, 0) |  |

## Nuclear Fuel Rod (`steam_nuclear_fuel_rod`)

*A Radioactive Fuel Rod.*
Can be inserted into a fuel assembly to start the nuclear fission process.

- Größe 1x9x1 Blöcke (voxel [0, -4, 0] .. [0, 4, 0]), Masse 80, Preis 2500, Tags: reactor
- Werte: cable_length=-431602080, nuclear_component_type=1, seat_health_per_sec=1, steam_component_type=9, type=54

## Oil Rig Drill Clamp (`oil_rig_drill_grabber`)

*A clamp for moving drill rods into place.*

- Größe 3x2x3 Blöcke (voxel [-1, 0, -1] .. [1, 1, 1]), Masse 30, Preis 100
- Werte: type=59

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Clamp Rod | An/Aus | Eingang | (0, 1, -1) | Attach a drill rod to the clamp. |
| Rod Clamped | An/Aus | Ausgang | (0, 1, 0) | Returns true when a drill rod is attached. |
| Slider Velocity | Zahl | Eingang | (0, 1, 1) | Slides an attached drill rod up or down the clamp. |

## Oil Rig Drill Clamp (End) (`oil_rig_drill_grabber_end`)

*A clamp for moving drill rods into place.*

- Größe 1x2x1 Blöcke (voxel [0, 0, 0] .. [0, 1, 0]), Masse 5, Preis 500
- Werte: type=59

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Clamp Rod | An/Aus | Eingang | (0, 0, 0) | Attach a drill rod to the clamp. |
| Rod Clamped | An/Aus | Ausgang | (0, 1, 0) | Returns true when a drill rod is attached. |

## Oil Rig Drill Connector (`oil_rig_drill_connector`)

*A clamp for moving drill rods into place.*
It can connect drill rods together to lengthen them, or separate drill rods to shorten them.

- Größe 3x2x7 Blöcke (voxel [-1, 0, -3] .. [1, 1, 3]), Masse 50, Preis 100
- Werte: oil_component_type=1, type=59

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Clamp Rod | An/Aus | Eingang | (0, 0, 0) | Attach a drill rod to the clamp. |
| Rod Clamped | An/Aus | Ausgang | (0, 1, 0) | Returns true when a drill rod is attached. |
| Slider Velocity | Zahl | Eingang | (0, 1, -1) | Moves an attached drill rod up or down the clamp. |
| Connect/Disconnect | An/Aus | Eingang | (0, 0, 2) | Connects or disconnects a pair of drill rods when the ends are aligned at the connection point. |
| Connector Aligned | An/Aus | Ausgang | (0, 1, 2) | Returns true when the connection point aligns over the end of a pair of drill rods. |

## Oil Rig Drill Swivel (`oil_rig_drill_swivel`)

*A swivel for transferring fluids through a drill rod.*
The swivel connects to the end of a drill rod, and has fluid ports for drilling slurry and crude oil. Pumping a supply of drilling slurry through a drill rod is required for effective drilling.

- Größe 3x5x3 Blöcke (voxel [-1, -2, -1] .. [1, 2, 1]), Masse 30, Preis 1000
- Werte: oil_component_type=4, type=59

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Clamp Rod | An/Aus | Eingang | (0, 1, 0) | Attach a drill rod to the swivel. |
| Rod Clamped | An/Aus | Ausgang | (0, 2, 0) | Returns true when a drill rod is attached. |
| Fluid In | Fluessigkeit/Gas | Eingang | (1, -1, 0) | Fluid port to transfer drilling slurry through an attached rod linked to a well. |
| Fluid Out | Fluessigkeit/Gas | Eingang | (-1, -1, 0) | Fluid port to transfer drilling slurry from an attached rod linked to a well. |

## Oil Rig Pumpjack (`oil_rig_pumpjack`)

*A pumpjack for extracting crude oil from a drilled oil well.*
Pulling the piston of the pumpjack with enough force will lift the piston, pulling fluid through the pump. A mechanical force capable of repeatedly cycling the piston is required to pump fluid effectively.

- Größe 3x11x3 Blöcke (voxel [-1, -7, -1] .. [1, 3, 1]), Masse 200, Preis 1000
- Werte: child_name=oil_rig_pumpjack_b, constraint_range_of_motion=2.5, constraint_type=1, pump_pressure=10000, type=7
- Zweiter Körper (Gelenk) bei [0, 7, 0]

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Fluid Out | Fluessigkeit/Gas | Eingang | (0, 2, 1) |  |

## Oil Rig Pumpjack B (`oil_rig_pumpjack_b`)


- Größe 1x10x1 Blöcke (voxel [0, -3, 0] .. [0, 6, 0]), Masse 500, Preis 0
- Werte: constraint_type=1, type=7

## Oil Rig Rod Storage (`oil_rig_drill_storage`)

*A storage rack for drill rods.*
Contains a single drill rod when spawned.

- Größe 1x2x41 Blöcke (voxel [0, -1, -20] .. [0, 0, 20]), Masse 10, Preis 50
- Werte: oil_component_type=2, type=59

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Rod Stored | An/Aus | Ausgang | (0, -1, 0) | Returns true when a drill rod is stored in the component. |

## Oil Rig Rotary Table (`oil_rig_drill_driver`)

*A rotary table for drilling in an oil rig.*
Torque provided by an external motor rotates the table, which can rotate a drill rod placed through the center of the table.

- Größe 7x3x7 Blöcke (voxel [-3, -1, -3] .. [3, 1, 3]), Masse 500, Preis 1000
- Werte: oil_component_type=3, type=59

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Clamp | An/Aus | Eingang | (0, 0, 0) | Attach a drill rod to the table. This will transfer any rotation of the table to the attached drill rod. |
| Torque | Drehmoment | Eingang | (-3, 0, 0) | Torque connection to power the rotation of the table. |
| RPS | Zahl | Ausgang | (0, 1, 0) | The rotations per second of the table. |

## Oil Rig Well Head (`oil_rig_well_head`)

*A well head for oil drilling.*
Once anchored to the terrain, a drill rod can be inserted into a well head to begin drilling a well. In order to drill effectively a drill rod should be driven by a rotary table and forced downward toward the terrain. A continuous supply of drilling slurry must be provided through the drill rod via a swivel, and the saturated drilling slurry extracted from the well head fluid port.

- Größe 9x25x9 Blöcke (voxel [-4, -12, -4] .. [4, 12, 4]), Masse 1000, Preis 5000
- Werte: oil_component_type=5, type=59

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Anchor | An/Aus | Eingang | (0, -7, 0) | Extend / retract piles to anchor the well head to the terrain, allowing for a new well to be drilled. The well head must be close to the terrain (~1m) and upright (+-30 degrees) to be anchored. Unanchoring the well will reset any drilling progress made. |
| Is Anchored | An/Aus | Ausgang | (0, -8, 0) | Returns true when the well head is anchored to the terrain. |
| Drill Depth | Zahl | Ausgang | (0, -9, 0) | Returns the depth of an attached drill rod in meters. |
| Well Depth | Zahl | Ausgang | (0, -10, 0) | Returns the depth of the drilled well in meters. |

## Steam Boiler (`steam_boiler`)

*A boiler for evaporating water into steam.*
The boiler should be connected to a firebox to supply heat for evaporation. Control the rate of evaporation to maintain consistent output steam pressure.

- Größe 5x5x7 Blöcke (voxel [-2, -2, -3] .. [2, 2, 3]), Masse 500, Preis 250
- Werte: cable_length=-431602080, seat_health_per_sec=1, type=53

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Coolant A | Fluessigkeit/Gas | Eingang | (0, 2, -1) | Port for supplying hot fluid to heat the contents of the boiler. |
| Coolant B | Fluessigkeit/Gas | Eingang | (0, 2, 1) | Port for supplying hot fluid to heat the contents of the boiler. |
| Water In | Fluessigkeit/Gas | Eingang | (0, 0, -3) |  |
| Steam Out | Fluessigkeit/Gas | Ausgang | (0, 0, 3) |  |
| Fluid Volume | Zahl | Ausgang | (0, 0, 0) |  |
| Temperature | Zahl | Ausgang | (0, 0, 1) |  |

## Steam Condenser (`steam_condenser`)

*A condenser for converting steam back to water.*
The condenser should be continously cooled to function efficiently.

- Größe 3x5x5 Blöcke (voxel [-1, -2, -2] .. [1, 2, 2]), Masse 250, Preis 250
- Werte: cable_length=-431602080, seat_health_per_sec=1, steam_component_type=1, type=53

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Coolant A | Fluessigkeit/Gas | Eingang | (0, 2, -1) | Port for supplying cold fluid to cool the contents of the condenser. |
| Coolant B | Fluessigkeit/Gas | Eingang | (0, 2, 1) | Port for supplying cold fluid to cool the contents of the condenser. |
| Steam In | Fluessigkeit/Gas | Eingang | (0, 0, -2) |  |
| Water Out | Fluessigkeit/Gas | Ausgang | (0, 0, 2) |  |
| Fluid Volume | Zahl | Ausgang | (0, 0, 0) |  |
| Temperature | Zahl | Ausgang | (0, 0, 1) |  |

## Steam Piston (Large) (`steam_piston_5x5`)

*A steam powered piston that converts steam pressure into torque.*
Steam pressurized through the outer coupling extends the piston and steam pressurized through the inner coupling retracts the piston. Alternating pressure to the couplings based on the piston position will allow the crankpin to rotate continuously.

- Größe 5x15x5 Blöcke (voxel [-2, -1, -2] .. [2, 13, 2]), Masse 300, Preis 2400
- Werte: engine_module_type=29, piston_cam=0.216, piston_len=1.2, steam_component_type=3, type=53, water_component_type=23

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| RPS | Drehmoment | Ausgang | (0, 0, 2) | Power connection A. |
| RPS | Drehmoment | Ausgang | (0, 0, -2) | Power connection B. |
| Steam In | Fluessigkeit/Gas | Ausgang | (2, 12, 0) |  |
| Steam Out | Fluessigkeit/Gas | Ausgang | (-2, 12, 0) |  |
| Steam In | Fluessigkeit/Gas | Ausgang | (2, 9, 0) |  |
| Steam Out | Fluessigkeit/Gas | Ausgang | (-2, 9, 0) |  |
| RPS | Zahl | Ausgang | (0, 0, 0) |  |
| Piston Position | Zahl | Ausgang | (0, 2, 0) |  |

## Steam Piston (Medium) (`steam_piston_3x3`)

*A steam powered piston that converts steam pressure into torque.*
Steam pressurized through the outer coupling extends the piston and steam pressurized through the inner coupling retracts the piston. Alternating pressure to the couplings based on the piston position will allow the crankpin to rotate continuously.

- Größe 3x9x3 Blöcke (voxel [-1, 0, -1] .. [1, 8, 1]), Masse 120, Preis 600
- Werte: engine_module_type=29, piston_cam=0.146, piston_len=0.686, steam_component_type=3, type=53, water_component_type=23

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| RPS | Drehmoment | Ausgang | (0, 0, 1) | Power connection A. |
| RPS | Drehmoment | Ausgang | (0, 0, -1) | Power connection B. |
| Steam In | Fluessigkeit/Gas | Ausgang | (1, 8, 0) |  |
| Steam Out | Fluessigkeit/Gas | Ausgang | (-1, 8, 0) |  |
| Steam In | Fluessigkeit/Gas | Ausgang | (1, 5, 0) |  |
| Steam Out | Fluessigkeit/Gas | Ausgang | (-1, 5, 0) |  |
| RPS | Zahl | Ausgang | (0, 0, 0) |  |
| Piston Position | Zahl | Ausgang | (0, 2, 0) |  |

## Steam Piston (Small) (`steam_piston`)

*A steam powered piston that converts steam pressure into torque.*
Steam pressurized through the outer coupling extends the piston and steam pressurized through the inner coupling retracts the piston. Alternating pressure to the couplings based on the piston position will allow the crankpin to rotate continuously.

- Größe 1x6x1 Blöcke (voxel [0, 0, 0] .. [0, 5, 0]), Masse 12, Preis 90
- Werte: engine_module_type=29, steam_component_type=3, type=53, water_component_type=23

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| RPS | Drehmoment | Ausgang | (0, 0, 0) | Power connection A. |
| RPS | Drehmoment | Ausgang | (0, 0, 0) | Power connection B. |
| Steam In | Fluessigkeit/Gas | Ausgang | (0, 5, 0) |  |
| Steam Out | Fluessigkeit/Gas | Ausgang | (0, 5, 0) |  |
| Steam In | Fluessigkeit/Gas | Ausgang | (0, 3, 0) |  |
| Steam Out | Fluessigkeit/Gas | Ausgang | (0, 3, 0) |  |
| RPS | Zahl | Ausgang | (0, 0, 0) |  |
| Piston Position | Zahl | Ausgang | (0, 2, 0) |  |

## Steam Turbine (`steam_turbine`)

*A steam powered turbine.*
Produces torque based on the force generated by steam passing through the turbine.

- Größe 5x9x5 Blöcke (voxel [-2, -4, -2] .. [2, 4, 2]), Masse 500, Preis 250
- Werte: cable_length=-431602080, seat_health_per_sec=1, steam_component_type=2, type=53

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Steam In | Fluessigkeit/Gas | Eingang | (2, -2, 0) |  |
| Steam Out | Fluessigkeit/Gas | Ausgang | (2, 2, 0) |  |
| RPS | Drehmoment | Ausgang | (0, 4, 0) |  |
| RPS | Drehmoment | Ausgang | (0, -4, 0) |  |

## Vacuum Duct (`steam_coal_vacuum`)

*A vacuum for moving resources.*
Can be toggled to move resources through the vacuum. The vacuum can transport resources from ducts and hoppers immediately in front of the vacuum nozzle.

- Größe 3x3x3 Blöcke (voxel [-1, 0, -1] .. [1, 2, 1]), Masse 20, Preis 50, Tags: steam,coal,fishing
- Werte: cable_length=-431602080, seat_health_per_sec=1, steam_component_type=13, type=53

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Active | An/Aus | Eingang | (0, 0, 0) |  |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical input. |

## Water Extractor (`water_extractor`)

*A machine to process minerals into water.*
Extracts water from hydrous ores when supplied with electric power.

- Größe 3x3x3 Blöcke (voxel [-1, -1, -1] .. [1, 1, 1]), Masse 20, Preis 100, Tags: industry,space
- Werte: cable_length=-431602080, logic_gate_subtype=12, seat_health_per_sec=1, steam_component_type=15, type=53

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Power | Strom | Eingang | (0, 0, 0) |  |
| Process | An/Aus | Eingang | (0, 0, 0) |  |
| Water Out | Fluessigkeit/Gas | Ausgang | (0, -1, 0) |  |
