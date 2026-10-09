# Fluessigkeiten (Kategorie 9)

Aus den Spieldaten erzeugt von `tools/bauteile_holen.py` - nicht von Hand ändern.

## Air Filter (`air_filter`)

*Port used to allow air in and out of a fluid system.*

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 50, Tags: air
- Werte: cable_radius=0.02, max_motor_speed=5, pump_pressure=0, type=24

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Air | Fluessigkeit/Gas | Ausgang | (0, 0, 0) | Allows fluid to flow in and out of an enclosed volume. |

## Air Ram (`modular_engine_air_ram`)

*Port used to allow air in and out of a fluid system.*

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 50, Tags: air
- Werte: cable_radius=0.02, max_motor_speed=5, pump_pressure=0, type=24

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Air | Fluessigkeit/Gas | Ausgang | (0, 0, 0) | Allows fluid to flow in and out of an enclosed volume. |

## Air Scoop Intake 1x1 (`scoop_intake_2`)

*An air intake component.*
An air intake component that performs better at higher velocity.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 30
- Werte: cable_length=0, cable_radius=0.02, type=24, water_component_type=15

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Fluid | Fluessigkeit/Gas | Eingang | (0, 0, 0) | Air output port. |

## Air-Air Heat Exchanger 2x2 (`heat_exchanger_2_2`)

*A heat exchanger that averages heat between two air systems.*
A heat exchanger that averages heat between two air systems at a rate proportional to the component's size.

- Größe 2x1x2 Blöcke (voxel [0, 0, 0] .. [1, 0, 1]), Masse 4, Preis 30
- Werte: type=24, water_component_type=17

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Air A In | Fluessigkeit/Gas | Eingang | (0, 0, 0) | Input air port. |
| Air A Out | Fluessigkeit/Gas | Eingang | (1, 0, 0) | Output air port. |
| Air B In | Fluessigkeit/Gas | Eingang | (0, 0, 1) | Input air port. |
| Air B Out | Fluessigkeit/Gas | Eingang | (1, 0, 1) | Output air port. |
| Temp A | Zahl | Ausgang | (0, 0, 0) | Compartment temperature. |
| Temp B | Zahl | Ausgang | (0, 0, 1) | Compartment temperature. |

## Air-Air Heat Exchanger 2x5 (`heat_exchanger_5_5`)

*A heat exchanger that averages heat between two air systems.*
A heat exchanger that averages heat between two air systems at a rate proportional to the component's size.

- Größe 2x5x5 Blöcke (voxel [0, -2, -2] .. [1, 2, 2]), Masse 10, Preis 70
- Werte: type=24, water_component_type=17

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Air A In | Fluessigkeit/Gas | Eingang | (0, 2, -2) | Input air port. |
| Air A Out | Fluessigkeit/Gas | Eingang | (0, 2, 2) | Output air port. |
| Air B In | Fluessigkeit/Gas | Eingang | (1, 2, -2) | Input air port. |
| Air B Out | Fluessigkeit/Gas | Eingang | (1, 2, 2) | Output air port. |
| Temp A | Zahl | Ausgang | (0, 0, 0) | Compartment temperature. |
| Temp B | Zahl | Ausgang | (0, 0, 1) | Compartment temperature. |

## Air-Air Heat Exchanger 3x9 (`heat_exchanger_9_9`)

*A heat exchanger that averages heat between two air systems.*
A heat exchanger that averages heat between two air systems at a rate proportional to the component's size.

- Größe 3x9x9 Blöcke (voxel [-1, -4, -4] .. [1, 4, 4]), Masse 27, Preis 100
- Werte: type=24, water_component_type=17

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Air A In | Fluessigkeit/Gas | Eingang | (-1, 4, -3) | Input air port. |
| Air A Out | Fluessigkeit/Gas | Eingang | (-1, 4, 3) | Output air port. |
| Air B In | Fluessigkeit/Gas | Eingang | (1, 4, -3) | Input air port. |
| Air B Out | Fluessigkeit/Gas | Eingang | (1, 4, 3) | Output air port. |
| Temp A | Zahl | Ausgang | (0, 0, 0) | Compartment temperature. |
| Temp B | Zahl | Ausgang | (0, 0, 1) | Compartment temperature. |

## Air-Liquid Heat Exchanger 1x2 (`air_exchanger`)

*A heat exchanger that averages heat between air and a liquid.*
An intercooler that averages heat between air and a liquid at a rate proportional to the component's size.

- Größe 1x1x2 Blöcke (voxel [0, 0, 0] .. [0, 0, 1]), Masse 2, Preis 15
- Werte: type=24, water_component_type=18

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Air In | Fluessigkeit/Gas | Eingang | (0, 0, 0) | Input air port. |
| Air Out | Fluessigkeit/Gas | Eingang | (0, 0, 1) | Output air port. |
| Fluid In | Fluessigkeit/Gas | Eingang | (0, 0, 0) | Input fluid port. |
| Fluid Out | Fluessigkeit/Gas | Eingang | (0, 0, 1) | Output fluid port. |
| Temp A | Zahl | Ausgang | (0, 0, 0) | Compartment air temperature. |
| Temp B | Zahl | Ausgang | (0, 0, 1) | Compartment water temperature. |

## Air-Liquid Heat Exchanger 5x2 (`air_exchanger_5_2`)

*A heat exchanger that averages heat between air and a liquid.*
An intercooler that averages heat between air and a liquid at a rate proportional to the component's size.

- Größe 1x2x5 Blöcke (voxel [0, -1, -2] .. [0, 0, 2]), Masse 7, Preis 30
- Werte: type=24, water_component_type=18

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Air In | Fluessigkeit/Gas | Eingang | (0, -1, -2) | Input air port. |
| Air Out | Fluessigkeit/Gas | Eingang | (0, -1, 2) | Output air port. |
| Fluid In | Fluessigkeit/Gas | Eingang | (0, 0, -1) | Input fluid port. |
| Fluid Out | Fluessigkeit/Gas | Eingang | (0, 0, 1) | Output fluid port. |
| Temp A | Zahl | Ausgang | (0, 0, 0) | Compartment air temperature. |
| Temp B | Zahl | Ausgang | (0, 0, 1) | Compartment water temperature. |

## Air-Liquid Heat Exchanger 5x3 (`air_exchanger_5_3`)

*A heat exchanger that averages heat between air and a liquid.*
An intercooler that averages heat between air and a liquid at a rate proportional to the component's size.

- Größe 3x3x5 Blöcke (voxel [-1, -1, -2] .. [1, 1, 2]), Masse 45, Preis 50
- Werte: type=24, water_component_type=18

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Air In | Fluessigkeit/Gas | Eingang | (0, 0, -2) | Input air port. |
| Air Out | Fluessigkeit/Gas | Eingang | (0, 0, 2) | Output air port. |
| Fluid In | Fluessigkeit/Gas | Eingang | (0, 1, -1) | Input fluid port. |
| Fluid Out | Fluessigkeit/Gas | Eingang | (0, 1, 1) | Output fluid port. |
| Temp A | Zahl | Ausgang | (0, 0, 0) | Compartment air temperature. |
| Temp B | Zahl | Ausgang | (0, 0, 1) | Compartment water temperature. |

## Air-Liquid Heat Exchanger 9x3 (`air_exchanger_9_3`)

*A heat exchanger that averages heat between air and a liquid.*
An intercooler that averages heat between air and a liquid at a rate proportional to the component's size.

- Größe 3x3x9 Blöcke (voxel [-1, -1, -4] .. [1, 1, 4]), Masse 81, Preis 80
- Werte: type=24, water_component_type=18

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Air In | Fluessigkeit/Gas | Eingang | (0, 0, -4) | Input air port. |
| Air Out | Fluessigkeit/Gas | Eingang | (0, 0, 4) | Output air port. |
| Fluid In | Fluessigkeit/Gas | Eingang | (0, 1, -3) | Input fluid port. |
| Fluid Out | Fluessigkeit/Gas | Eingang | (0, 1, 3) | Output fluid port. |
| Temp A | Zahl | Ausgang | (0, 0, 0) | Compartment air temperature. |
| Temp B | Zahl | Ausgang | (0, 0, 1) | Compartment water temperature. |

## Air-Liquid Heat Exchanger 9x5 (`air_exchanger_9_5`)

*A heat exchanger that averages heat between air and a liquid.*
An intercooler that averages heat between air and a liquid at a rate proportional to the component's size.

- Größe 5x5x9 Blöcke (voxel [-2, -2, -4] .. [2, 2, 4]), Masse 225, Preis 150
- Werte: type=24, water_component_type=18

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Air In | Fluessigkeit/Gas | Eingang | (0, 0, -4) | Input air port. |
| Air Out | Fluessigkeit/Gas | Eingang | (0, 0, 4) | Output air port. |
| Fluid In | Fluessigkeit/Gas | Eingang | (0, 2, -2) | Input fluid port. |
| Fluid Out | Fluessigkeit/Gas | Eingang | (0, 2, 2) | Output fluid port. |
| Temp A | Zahl | Ausgang | (0, 0, 0) | Compartment air temperature. |
| Temp B | Zahl | Ausgang | (0, 0, 1) | Compartment water temperature. |

## Catalytic Converter (`catalytic_converter`)

*Reduces particles from exhausts.*
Catalytic converter that removes fumes and decreases the number of exhaust particles emitted from an exhaust.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 100
- Werte: cable_length=0, cable_radius=0.02, type=24, water_component_type=13

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Exhaust In | Fluessigkeit/Gas | Eingang | (0, 0, 0) |  |
| Exhaust Out | Fluessigkeit/Gas | Eingang | (0, 0, 0) |  |

## Centrifugal Separator (`separator`)

*A tank that can be spun to separate contained fluids.*
Provide torque to begin spinning the separator, fluid output ports will separate with increased effectiveness based on the spin speed.

- Größe 5x9x5 Blöcke (voxel [-2, -4, -2] .. [2, 4, 2]), Masse 80, Preis 480, Tags: oil
- Werte: type=24, water_component_type=28

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| RPS | Drehmoment | Ausgang | (0, 4, 0) | RPS input node for spinning the centrifuge. |
| Fluid In | Fluessigkeit/Gas | Eingang | (2, 2, -2) | Input fluid port. |
| Fluid Out | Fluessigkeit/Gas | Ausgang | (0, -4, 0) | Main output fluid port. |
| Dense Fluid Out | Fluessigkeit/Gas | Ausgang | (-1, -4, 0) | Output port that will filter the denser fluid when the centrifuge is operating at high speed. |

## Cryo Cooler (`cryo_cooler`)

*A powered component that creates a temperature difference between two liquid systems.*
A component that cools liquid A and transfers the heat to liquid B.

- Größe 1x1x0 Blöcke (voxel [0, 0, 0] .. [0, 0, -1]), Masse 4, Preis 30
- Werte: type=24, water_component_type=33

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Liquid A In | Fluessigkeit/Gas | Eingang | (0, 1, -1) | Input liquid port for liquid that gets cooled. |
| Liquid A Out | Fluessigkeit/Gas | Eingang | (0, 0, -1) | Output liquid port for liquid that gets cooled. |
| Liquid B In | Fluessigkeit/Gas | Eingang | (0, 1, 0) | Input liquid port for liquid that gets warmed. |
| Liquid B Out | Fluessigkeit/Gas | Eingang | (0, 0, 0) | Output liquid port for liquid that gets warmed. |
| Temp A | Zahl | Ausgang | (0, 1, -1) | Compartment temperature. |
| Temp B | Zahl | Ausgang | (0, 1, 0) | Compartment temperature. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |
| On/Off | An/Aus | Eingang | (0, 0, 0) | Controls whether or not the component transfers heat between liquids. |

## Desalinator (`desalinator`)

*A pipe that slowly converts seawater to freshwater.*
A pipe with a fine desalination filter that slowly converts seawater to freshwater and allows free flow of freshwater.

- Größe 1x5x1 Blöcke (voxel [0, -2, 0] .. [0, 2, 0]), Masse 5, Preis 400, Tags: basic
- Werte: cable_length=-431602080, seat_health_per_sec=1, type=24, water_component_type=24

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Fluid In | Fluessigkeit/Gas | Eingang | (0, -2, 0) | Seawater connection. |
| Fluid Out | Fluessigkeit/Gas | Eingang | (0, 2, 0) | Freshwater connection. |

## Fluid Exhaust (`fluid_exhaust`)

*An exhaust port for fluid systems.*
Fluid can flow in and out of the port as part of a fluid system.

- Größe 1x2x1 Blöcke (voxel [0, 0, 0] .. [0, 1, 0]), Masse 1, Preis 100, Tags: basic
- Werte: cable_length=-431602080, seat_health_per_sec=1, type=24

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Fluid | Fluessigkeit/Gas | Eingang | (0, 0, 0) | Allows fluid to flow in and out of an enclosed volume or the ocean. |

## Fluid Filter (`fluid_filter`)

*The fluid filter only allows certain types of fluid across the valve.*
The valve can be configured to select which fluids may pass across the two directional valve.

- Größe 1x2x1 Blöcke (voxel [0, 0, 0] .. [0, 1, 0]), Masse 5, Preis 400, Tags: basic
- Werte: cable_length=-431602080, seat_health_per_sec=1, type=24, water_component_type=10

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Fluid A | Fluessigkeit/Gas | Eingang | (0, 0, 0) | Fluid connection. |
| Fluid B | Fluessigkeit/Gas | Eingang | (0, 1, 0) | Fluid connection. |
| Flow Rate | Zahl | Ausgang | (0, 0, 0) | Fluid flow rate in L/s. |

## Fluid Filter (`fluid_filter_v2`)

*The fluid filter can prevent liquids or gases crossing the valve.*
The valve can be configured to select which fluid groups may pass across the two directional valve. Liquids or gases.

- Größe 1x2x1 Blöcke (voxel [0, 0, 0] .. [0, 1, 0]), Masse 5, Preis 400, Tags: basic
- Werte: type=24, water_component_type=27

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Fluid A | Fluessigkeit/Gas | Eingang | (0, 0, 0) | Fluid connection. |
| Fluid B | Fluessigkeit/Gas | Eingang | (0, 1, 0) | Fluid connection. |

## Fluid Flow Valve (`fluid_valve_flow`)

*A one way valve for controlling fluid flow.*
Allows fluid to move from the input side of the valve to the output but resists fluid flow in the other direction.

- Größe 1x2x1 Blöcke (voxel [0, 0, 0] .. [0, 1, 0]), Masse 4, Preis 100, Tags: basic
- Werte: cable_radius=0, max_motor_speed=5, pump_pressure=0, type=24, water_component_type=3

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Fluid In | Fluessigkeit/Gas | Ausgang | (0, 1, 0) | Fluid connection for the valve input. |
| Fluid Out | Fluessigkeit/Gas | Ausgang | (0, 0, 0) | Fluid connection for the valve output. |
| Flow Rate | Zahl | Ausgang | (0, 1, 0) | Fluid flow rate in L/s. |

## Fluid Heat Radiator (`fluid_radiator`)

*Radiator type cooler for fluid.*
Fluid inside the cooler will lose temperature.

- Größe 3x3x1 Blöcke (voxel [-1, -1, 0] .. [1, 1, 0]), Masse 10, Preis 200, Tags: basic
- Werte: cable_length=-431602080, seat_health_per_sec=1, type=24, water_component_type=9

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Fluid A | Fluessigkeit/Gas | Eingang | (1, 1, 0) | Fluid Connection. |
| Fluid B | Fluessigkeit/Gas | Eingang | (-1, 1, 0) | Fluid Connection. |

## Fluid Heat Radiator 3x3 (Electric) (`fluid_radiator_electric`)

*Radiator type cooler for fluid.*
Fluid inside the cooler will lose temperature, supplying electric for the fan will increase the rate of exchange.

- Größe 3x1x3 Blöcke (voxel [-1, 0, -1] .. [1, 0, 1]), Masse 10, Preis 400
- Werte: cable_length=-431602080, seat_health_per_sec=1, type=24, water_component_type=9

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Fluid A | Fluessigkeit/Gas | Eingang | (-1, 0, -1) | Fluid Connection. |
| Fluid B | Fluessigkeit/Gas | Ausgang | (-1, 0, 1) | Fluid Connection. |
| Electric | Strom | Ausgang | (0, 0, 0) |  |
| Fan On/Off | An/Aus | Eingang | (1, 0, 0) |  |
| Temperature | Zahl | Ausgang | (1, 0, 1) |  |

## Fluid Heat Radiator 5x5 (Electric) (`fluid_radiator_electric_5`)

*Radiator type cooler for fluid.*
Fluid inside the cooler will lose temperature, supplying electric for the fan will increase the rate of exchange.

- Größe 5x1x5 Blöcke (voxel [-2, 0, -2] .. [2, 0, 2]), Masse 25, Preis 700
- Werte: cable_length=-431602080, seat_health_per_sec=1, type=24, water_component_type=9

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Fluid A | Fluessigkeit/Gas | Eingang | (-2, 0, -2) | Fluid Connection. |
| Fluid B | Fluessigkeit/Gas | Eingang | (-2, 0, 2) | Fluid Connection. |
| Electric | Strom | Ausgang | (0, 0, 0) |  |
| Fan On/Off | An/Aus | Eingang | (1, 0, 0) |  |
| Temperature | Zahl | Ausgang | (1, 0, 1) |  |

## Fluid Heat Sink (`fluid_heat_sink`)

*Heat sink type cooler for fluid.*
Fluid inside the cooler will lose temperature.

- Größe 5x3x1 Blöcke (voxel [-2, -1, 0] .. [2, 1, 0]), Masse 18, Preis 300
- Werte: cable_length=-431602080, seat_health_per_sec=1, type=24, water_component_type=9

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Fluid A | Fluessigkeit/Gas | Eingang | (2, 1, 0) | Fluid Connection. |
| Fluid B | Fluessigkeit/Gas | Eingang | (-2, 1, 0) | Fluid Connection. |

## Fluid Intake (`fluid_intake`)

*Port used to allow fluid in and out of a fluid system.*
Place the port inside of an enclosed volume to connect to that volume, or outside of the vehicle to connect to the exterior.

- Größe 3x2x1 Blöcke (voxel [-1, 0, 0] .. [1, 1, 0]), Masse 1, Preis 100, Tags: air
- Werte: cable_length=-431602080, seat_health_per_sec=1, type=24

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Fluid | Fluessigkeit/Gas | Ausgang | (0, 0, 0) | Allows fluid to flow in and out of an enclosed volume or the exterior. |

## Fluid Jet (`water_jet`)

*A fluid impeller and jet nozzle for ocean propulsion.*
Converts mechanical power and water into a high power jet for generating thrust.

- Größe 3x7x3 Blöcke (voxel [-1, 0, -1] .. [1, 6, 1]), Masse 10, Preis 3000, Tags: basic
- Werte: cable_length=-431602080, type=24, water_component_type=11

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Fluid Flow In | Fluessigkeit/Gas | Eingang | (0, 0, 1) | Fluid inlet to supply jet. |
| RPS | Drehmoment | Eingang | (0, 0, 0) | Mechanical power input to power jet. |
| Vertical Trim | Zahl | Eingang | (0, 3, 0) | Vertical nozzle angle to control jet direction. |
| Deflector A | Zahl | Eingang | (-1, 3, 0) | Left bucket defector control input. |
| Deflector B | Zahl | Eingang | (1, 3, 0) | Right bucket defector control input. |
| Electric | Strom | Eingang | (0, 4, 0) | Electrical power connection. |

## Fluid On/Off Valve (`fluid_valve_on_off`)

*An on/off fluid valve.*
Controls flow from one side of the valve to the other. Fluid can flow in both directions.

- Größe 2x2x1 Blöcke (voxel [-1, 0, 0] .. [0, 1, 0]), Masse 4, Preis 100, Tags: basic
- Werte: cable_radius=0, max_motor_speed=5, pump_pressure=0, type=24, water_component_type=4

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Fluid In | Fluessigkeit/Gas | Ausgang | (0, 0, 0) | Fluid input connection for the valve. |
| Fluid Out | Fluessigkeit/Gas | Ausgang | (0, 1, 0) | Fluid output connection for the valve. |
| Valve Control | An/Aus | Eingang | (-1, 0, 0) | Valve gate control for opening and closing the valve. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |
| Flow Rate | Zahl | Ausgang | (0, 0, 0) | Fluid flow rate in L/s. |

## Fluid On/Off Valve (Manual) (`fluid_valve_on_off_manual`)

*An on/off fluid valve with a manual handle.*
Interacting with [$[action_interact_left]]/[$[action_interact_right]] will open / close the valve. Controls flow from one side of the valve to the other. Fluid can flow in both directions.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 100, Tags: basic
- Werte: cable_radius=0, type=24, water_component_type=21

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Fluid In | Fluessigkeit/Gas | Ausgang | (0, 0, 0) | Fluid input connection for the valve. |
| Fluid Out | Fluessigkeit/Gas | Ausgang | (0, 0, 0) | Fluid output connection for the valve. |
| Flow Rate | Zahl | Ausgang | (0, 0, 0) | Fluid flow rate in L/s. |

## Fluid Port (`water_inlet`)

*Port used to allow fluid in and out of a fluid system.*
Place the port inside of an enclosed volume to connect to that volume, or outside of the vehicle to connect to the ocean.

- Größe 1x2x1 Blöcke (voxel [0, 0, 0] .. [0, 1, 0]), Masse 1, Preis 50, Tags: air,basic
- Werte: cable_radius=0.02, max_motor_speed=5, pump_pressure=0, type=24

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Fluid | Fluessigkeit/Gas | Ausgang | (0, 0, 0) | Allows fluid to flow in and out of an enclosed volume or the ocean. |

## Fluid Port (`water_outlet`)

*Port used to allow fluid in and out of a fluid system.*
Place the port inside of an enclosed volume to connect to that volume, or outside of the vehicle to connect to the ocean.

- Größe 1x2x1 Blöcke (voxel [0, 0, 0] .. [0, 1, 0]), Masse 1, Preis 50, Tags: pump
- Werte: cable_radius=0.02, max_motor_speed=5, pump_pressure=0, type=24

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Fluid | Fluessigkeit/Gas | Ausgang | (0, 0, 0) | Allows fluid to flow in and out of an enclosed volume or the ocean. |

## Fluid Port End (`fluid_port_end`)

*Port used to allow fluid in and out of a fluid system.*
Place the port inside of an enclosed volume to connect to that volume, or outside of the vehicle to connect to the ocean.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 50, Tags: air,basic
- Werte: type=24

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Fluid | Fluessigkeit/Gas | Ausgang | (0, 0, 0) | Allows fluid to flow in and out of an enclosed volume or the ocean. |

## Fluid Pressure Sensor (`fluid_pressure`)

*A sensor for reading fluid pressure.*
Measures the fluid pressure in the connected fluid network.

- Größe 1x2x1 Blöcke (voxel [0, 0, 0] .. [0, 1, 0]), Masse 4, Preis 100
- Werte: cable_radius=0, max_motor_speed=5, pump_pressure=0, type=24, water_component_type=6

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Fluid | Fluessigkeit/Gas | Ausgang | (0, 0, 0) | Fluid to measure the pressure of. |
| Pressure | Zahl | Ausgang | (0, 1, 0) | The pressure reading of the fluid. |

## Fluid Pump (`water_pump`)

*A small fluid pump.*
Connect to an inlet and outlet to create a pumping system to move fluid around a vehicle.

- Größe 3x1x1 Blöcke (voxel [-1, 0, 0] .. [1, 0, 0]), Masse 4, Preis 100, Tags: basic
- Werte: cable_radius=0, max_motor_speed=5, pump_pressure=10, type=25

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| On/Off | An/Aus | Eingang | (0, 0, 0) | Controls whether or not the fluid is being pumped through. |
| Fluid In | Fluessigkeit/Gas | Eingang | (-1, 0, 0) | Connect to an inlet component to take fluid into the system. |
| Fluid Out | Fluessigkeit/Gas | Eingang | (1, 0, 0) | Connect to an outlet component to release fluid from the system. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |
| Flow Rate | Zahl | Ausgang | (-1, 0, 0) | Fluid flow rate in L/s. |

## Fluid Pump (Manual) (`water_pump_manual`)

*A small fluid pump with a manual handle.*
Hold [$[action_interact_left]]/[$[action_interact_right]] to create pressure in the pump. Connect to an inlet and outlet to create a pumping system to move fluid around a vehicle.

- Größe 2x3x1 Blöcke (voxel [-1, -1, 0] .. [0, 1, 0]), Masse 4, Preis 100, Tags: basic
- Werte: cable_radius=0, pump_pressure=3, type=24, water_component_type=22

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Fluid In | Fluessigkeit/Gas | Eingang | (0, -1, 0) | Connect to an inlet component to take fluid into the system. |
| Fluid Out | Fluessigkeit/Gas | Ausgang | (0, 1, 0) | Connect to an outlet component to release fluid from the system. |
| Flow Rate | Zahl | Ausgang | (0, -1, 0) | Fluid flow rate in L/s. |

## Fluid Slot Port (`water_suction_duct`)

*Port used to allow fluid in and out of a fluid system.*
Place the port inside of an enclosed volume to connect to that volume, or outside of the vehicle to connect to the ocean.

- Größe 3x2x4 Blöcke (voxel [-1, 0, 0] .. [1, 1, 3]), Masse 12, Preis 100, Tags: basic
- Werte: cable_length=-431602080, type=24, water_component_type=12

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Fluid | Fluessigkeit/Gas | Ausgang | (0, 0, 0) | Allows fluid to flow in and out of an enclosed volume or the ocean. |

## Fluid Spawner (`water_spawner`)

*A component to mark an enclosed area to be spawned with fluid inside.*
The fluid spawner for helping with custom fluid tanks, so they can be spawned full, without a need to fill after spawning. Gases are spawned compressed (60atm).

- Größe 1x2x1 Blöcke (voxel [0, 0, 0] .. [0, 1, 0]), Masse 1, Preis 20, Tags: basic
- Werte: cable_radius=0.02, max_motor_speed=5, pump_pressure=0, seat_health_per_sec=1, type=24, water_component_type=7

## Fluid Tank Large (`fluid_tank_large`)

*A tank for storing fluid.*
The tank will spawn full of the selected fluid type.

- Größe 3x3x5 Blöcke (voxel [-1, -2, -2] .. [1, 0, 2]), Masse 22, Preis 20, Tags: basic
- Werte: cable_radius=0.02, max_motor_speed=5, pump_pressure=0, seat_health_per_sec=1, type=24, water_component_type=8

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Stored Fluid | Fluessigkeit/Gas | Eingang | (-1, 0, 0) | The fluid connection for the stored contents. |
| Tank Content | Zahl | Ausgang | (-1, 0, -1) | The amount of fluid in the tank in litres. |
| Stored Fluid | Fluessigkeit/Gas | Eingang | (-1, -2, 0) | The fluid connection for the stored contents. |
| Tank Pressure | Zahl | Ausgang | (0, -1, 0) | The pressure in the tank in atmospheres. |

## Fluid Tank Medium (`fluid_tank_medium`)

*A tank for storing fluid.*
The tank will spawn full of the selected fluid type.

- Größe 2x2x3 Blöcke (voxel [0, -1, -1] .. [1, 0, 1]), Masse 6, Preis 20, Tags: basic
- Werte: cable_radius=0.02, max_motor_speed=5, pump_pressure=0, seat_health_per_sec=1, type=24, water_component_type=8

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Stored Fluid | Fluessigkeit/Gas | Eingang | (0, 0, 0) | The fluid connection for the stored contents. |
| Tank Content | Zahl | Ausgang | (0, 0, -1) | The amount of fluid in the tank in litres. |
| Stored Fluid | Fluessigkeit/Gas | Eingang | (0, -1, 0) | The fluid connection for the stored contents. |
| Tank Pressure | Zahl | Ausgang | (0, -1, 0) | The pressure in the tank in atmospheres. |

## Fluid Tank Small (`fluid_tank_small`)

*A tank for storing fluid.*
The tank will spawn full of the selected fluid type.

- Größe 1x1x2 Blöcke (voxel [0, 0, -1] .. [0, 0, 0]), Masse 1, Preis 20, Tags: basic
- Werte: cable_radius=0.02, max_motor_speed=5, pump_pressure=0, seat_health_per_sec=1, type=24, water_component_type=8

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Stored Fluid | Fluessigkeit/Gas | Eingang | (0, 0, 0) | The fluid connection for the stored contents. |
| Tank Content | Zahl | Ausgang | (0, 0, -1) | The amount of fluid in the tank in litres. |
| Stored Fluid | Fluessigkeit/Gas | Eingang | (0, 0, 0) | The fluid connection for the stored contents. |
| Tank Pressure | Zahl | Ausgang | (0, 0, 0) | The pressure in the tank in atmospheres. |

## Fluid Variable Valve (`fluid_valve_variable`)

*A variable fluid valve.*
Controls flow from one side of the valve to the other. Fluid can flow in both directions.

- Größe 2x2x1 Blöcke (voxel [-1, 0, 0] .. [0, 1, 0]), Masse 4, Preis 100, Tags: basic
- Werte: cable_radius=0, max_motor_speed=5, pump_pressure=0, type=24, water_component_type=5

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Fluid In | Fluessigkeit/Gas | Ausgang | (0, 0, 0) | Fluid input connection for the valve. |
| Fluid Out | Fluessigkeit/Gas | Ausgang | (0, 1, 0) | Fluid output connection for the valve. |
| Valve Control | Zahl | Eingang | (-1, 0, 0) | Valve gate control for opening and closing the valve. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |
| Flow Rate | Zahl | Ausgang | (0, 0, 0) | Fluid flow rate in L/s. |

## Fractional Distillation Port (`distillation_tray`)

*Port used to collect output in a distillation column.*
Place the port inside of an enclosed volume to connect to that volume. Outputs different fluids based on height relative to the bottom of the compartment.

- Größe 3x5x3 Blöcke (voxel [-1, -2, -1] .. [1, 2, 1]), Masse 36, Preis 80, Tags: oil,refining,refine
- Werte: type=24, water_component_type=26

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Fluid | Fluessigkeit/Gas | Ausgang | (0, -2, 0) | Collects distilled fluids from an enclosed volume. |

## Gas Relief Valve (`relief_valve_gas`)

*A relief valve for gases in a system.*
The valve allows gases to pass across the two directional valve.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 2, Preis 150, Tags: basic,fluid,filter
- Werte: logic_gate_subtype=1, type=24, water_component_type=32

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Fluid A | Fluessigkeit/Gas | Ausgang | (0, 0, 0) |  |
| Fluid B | Fluessigkeit/Gas | Ausgang | (0, 0, 0) |  |
| Flow Rate | Zahl | Ausgang | (0, 0, 0) | Fluid flow rate in L/s. |

## Gas Tank (Huge) (`fluid_tank_compressed_gas_5_9`)

*A tank for storing gas.*
The tank will spawn full of the selected fluid type.

- Größe 5x9x5 Blöcke (voxel [-2, -4, -2] .. [2, 4, 2]), Masse 22, Preis 20, Tags: fluid
- Werte: seat_health_per_sec=1, type=24, water_component_type=20

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Stored Gas | Fluessigkeit/Gas | Eingang | (0, -4, 0) | The fluid connection for the stored contents. |
| Tank Content | Zahl | Ausgang | (0, 0, 0) | The amount of gas in the tank in litres. |
| Tank Pressure | Zahl | Ausgang | (0, -1, 0) | The pressure in the tank in atmospheres. |

## Gas Tank (Large) (`fluid_tank_compressed_gas_3_7`)

*A tank for storing gas.*
The tank will spawn full of the selected fluid type.

- Größe 3x7x3 Blöcke (voxel [-1, -3, -1] .. [1, 3, 1]), Masse 12, Preis 20, Tags: fluid
- Werte: seat_health_per_sec=1, type=24, water_component_type=20

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Stored Gas | Fluessigkeit/Gas | Eingang | (0, -3, 0) | The fluid connection for the stored contents. |
| Tank Content | Zahl | Ausgang | (0, 0, 0) | The amount of gas in the tank in litres. |
| Tank Pressure | Zahl | Ausgang | (0, -1, 0) | The pressure in the tank in atmospheres. |

## Gas Tank (Medium) (`fluid_tank_compressed_gas_1_7`)

*A tank for storing gas.*
The tank will spawn full of the selected fluid type.

- Größe 1x7x1 Blöcke (voxel [0, -3, 0] .. [0, 3, 0]), Masse 5, Preis 20, Tags: fluid
- Werte: seat_health_per_sec=1, type=24, water_component_type=20

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Stored Gas | Fluessigkeit/Gas | Eingang | (0, -3, 0) | The fluid connection for the stored contents. |
| Tank Content | Zahl | Ausgang | (0, 0, 0) | The amount of fluid in the tank in litres. |
| Tank Pressure | Zahl | Ausgang | (0, -1, 0) | The pressure in the tank in atmospheres. |

## Gas Tank (Small) (`fluid_tank_compressed_gas_1_3`)

*A tank for storing gas.*
The tank will spawn full of the selected fluid type.

- Größe 1x3x1 Blöcke (voxel [0, -1, 0] .. [0, 1, 0]), Masse 2, Preis 20, Tags: fluid
- Werte: seat_health_per_sec=1, type=24, water_component_type=20

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Stored Gas | Fluessigkeit/Gas | Eingang | (0, -1, 0) | The fluid connection for the stored contents. |
| Tank Content | Zahl | Ausgang | (0, 0, 0) | The amount of gas in the tank in litres. |
| Tank Pressure | Zahl | Ausgang | (0, -1, 0) | The pressure in the tank in atmospheres. |

## Hydrogen Electrolyser (`electrolyser`)

*A machine that separates water into hydrogen and oxygen.*
Submerge the electrodes into a volume of water and provide electric to separate freshwater.

- Größe 1x6x3 Blöcke (voxel [0, 0, -1] .. [0, 5, 1]), Masse 16, Preis 575
- Werte: type=24, water_component_type=31

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Oxygen Out | Fluessigkeit/Gas | Ausgang | (0, 0, -1) |  |
| Hydrogen Out | Fluessigkeit/Gas | Ausgang | (0, 0, 1) |  |
| Electric | Strom | Eingang | (0, 0, 0) |  |
| Enable | An/Aus | Eingang | (0, 0, 0) |  |

## Hydrogen Fuel Cell (`hydrogen_fuel_cell`)

*A hydrogen fuel cell capable of generating electric power.*
Pumping hydrogen and oxygen into the fuel cell generates power while creating water as a byproduct.

- Größe 3x5x3 Blöcke (voxel [-1, -2, -1] .. [1, 2, 1]), Masse 50, Preis 800
- Werte: type=24, water_component_type=34

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Electric | Strom | Eingang | (0, 0, 0) | The electric connection to output electric energy. |
| Oxygen In | Fluessigkeit/Gas | Eingang | (-1, -2, 0) |  |
| Hydrogen In | Fluessigkeit/Gas | Eingang | (1, -2, 0) |  |
| Water Out | Fluessigkeit/Gas | Ausgang | (0, 2, 0) |  |

## Impeller Pump (`turbocharger`)

*An Impeller Pump that can push fluid through a system.*
An Impeller that will force fluid through the system when torque is applied.

- Größe 3x1x3 Blöcke (voxel [-1, 0, -1] .. [1, 0, 1]), Masse 9, Preis 50
- Werte: cable_length=0, cable_radius=0.02, max_motor_force=2, pump_pressure=9, type=24, water_component_type=14

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Fluid In | Fluessigkeit/Gas | Eingang | (0, 0, 0) |  |
| RPS | Drehmoment | Ausgang | (0, 0, 0) |  |
| Fluid Out | Fluessigkeit/Gas | Eingang | (-1, 0, 1) |  |
| Flow Rate | Zahl | Ausgang | (0, 0, 0) | Fluid flow rate in L/s. |

## Impeller Pump (Small) (`turbocharger_small`)

*An Impeller Pump that can push fluid through a system.*
An Impeller that will force fluid through the system when torque is applied.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 40
- Werte: cable_length=0, cable_radius=0.02, max_motor_force=1, pump_pressure=1, type=24, water_component_type=14

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Fluid In | Fluessigkeit/Gas | Eingang | (0, 0, 0) |  |
| RPS | Drehmoment | Ausgang | (0, 0, 0) |  |
| Fluid Out | Fluessigkeit/Gas | Eingang | (0, 0, 0) |  |
| Flow Rate | Zahl | Ausgang | (0, 0, 0) | Fluid flow rate in L/s. |

## Large Fluid Pump (`water_pump_large`)

*A large fluid pump.*
Connect to an inlet and outlet to create a pumping system to move fluid around a vehicle.

- Größe 2x2x2 Blöcke (voxel [-1, 0, 0] .. [0, 1, 1]), Masse 10, Preis 200, Tags: basic
- Werte: cable_radius=0, max_motor_speed=5, pump_pressure=100, type=25

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Fluid In | Fluessigkeit/Gas | Eingang | (0, 1, 0) | Connect to an inlet component to take fluid into the system. |
| Fluid Out | Fluessigkeit/Gas | Eingang | (-1, 1, 1) | Connect to an outlet component to release fluid from the system. |
| On/Off | An/Aus | Eingang | (0, 0, 1) | Controls whether or not the fluid is being pumped. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |
| Flow Rate | Zahl | Ausgang | (0, 1, 0) | Fluid flow rate in L/s. |

## Liquid Relief Valve (`relief_valve_liquid`)

*A relief valve for liquids in a system.*
The valve allows liquids to pass across the two directional valve.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 2, Preis 150, Tags: basic,fluid,filter
- Werte: type=24, water_component_type=32

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Fluid A | Fluessigkeit/Gas | Ausgang | (0, 0, 0) |  |
| Fluid B | Fluessigkeit/Gas | Ausgang | (0, 0, 0) |  |
| Flow Rate | Zahl | Ausgang | (0, 0, 0) | Fluid flow rate in L/s. |

## Liquid-Liquid Heat Exchanger 2x2 (`intercooler`)

*A heat exchanger that averages heat between two liquid systems.*
A heat exchanger that averages heat between two liquid systems at a rate proportional to the component's size.

- Größe 1x2x2 Blöcke (voxel [0, 0, -1] .. [0, 1, 0]), Masse 4, Preis 30
- Werte: cable_length=0, cable_radius=0.02, type=24, water_component_type=16

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Fluid A In | Fluessigkeit/Gas | Eingang | (0, 1, -1) | Input fluid port. |
| Fluid A Out | Fluessigkeit/Gas | Eingang | (0, 0, -1) | Output fluid port. |
| Fluid B In | Fluessigkeit/Gas | Eingang | (0, 1, 0) | Input fluid port. |
| Fluid B Out | Fluessigkeit/Gas | Eingang | (0, 0, 0) | Output fluid port. |
| Temp A | Zahl | Ausgang | (0, 0, -1) | Compartment temperature. |
| Temp B | Zahl | Ausgang | (0, 0, 0) | Compartment temperature. |

## Liquid-Liquid Heat Exchanger 5x5 (`intercooler_large`)

*A heat exchanger that averages heat between two liquid systems.*
A heat exchanger that averages heat between two liquid systems at a rate proportional to the component's size.

- Größe 1x5x5 Blöcke (voxel [0, -2, -2] .. [0, 2, 2]), Masse 16, Preis 50
- Werte: type=24, water_component_type=16

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Fluid A In | Fluessigkeit/Gas | Eingang | (0, 2, -2) | Input fluid port. |
| Fluid A Out | Fluessigkeit/Gas | Eingang | (0, -2, -2) | Output fluid port. |
| Fluid B In | Fluessigkeit/Gas | Eingang | (0, 2, 2) | Input fluid port. |
| Fluid B Out | Fluessigkeit/Gas | Eingang | (0, -2, 2) | Output fluid port. |
| Temp A | Zahl | Ausgang | (0, 0, 0) | Compartment temperature. |
| Temp B | Zahl | Ausgang | (0, 0, 1) | Compartment temperature. |

## Slurry Filter (`slurry_filter`)

*A filter that slowly desaturates slurry.*
A pipe with a solids filter that consumes fresh water to slowly convert saturated slurry to slurry and allows free flow of slurry.

- Größe 5x15x9 Blöcke (voxel [-2, -7, -4] .. [2, 7, 4]), Masse 140, Preis 320
- Werte: type=24, water_component_type=25

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Water In | Fluessigkeit/Gas | Eingang | (0, 6, -4) | Water Input. |
| Water Out | Fluessigkeit/Gas | Ausgang | (0, 6, 4) | Water Output. |
| Slurry In | Fluessigkeit/Gas | Eingang | (-2, 4, -4) | Saturated Slurry input. |
| Slurry Out | Fluessigkeit/Gas | Ausgang | (0, -7, 4) | Slurry output. |

## Steam Whistle (`steam_whistle`)

*A steam powered signal whistle.*
When open, the steam whistle produces sound as steam flows through the pipe connection. The whistle pitch can be set in the component properties menu.

- Größe 1x4x1 Blöcke (voxel [0, -1, 0] .. [0, 2, 0]), Masse 4, Preis 50, Tags: steam power
- Werte: cable_radius=0.02, max_motor_speed=5, pump_pressure=0, steam_component_type=8, type=24, water_component_type=23

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Fluid | Fluessigkeit/Gas | Eingang | (0, -1, 0) | Allows steam to flow out. |
| Open | An/Aus | Eingang | (0, 0, 0) | Opens the steam whistle, allowing steam to flow through. |
