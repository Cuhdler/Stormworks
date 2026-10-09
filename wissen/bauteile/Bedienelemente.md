# Bedienelemente (Kategorie 2)

Aus den Spieldaten erzeugt von `tools/bauteile_holen.py` - nicht von Hand ändern.

## Clutch (`torque_clutch`)

*A clutch for managing the transmission of power between two nodes.*
The number input controls the amount of power transmitted.

- Größe 1x2x1 Blöcke (voxel [0, 0, 0] .. [0, 1, 0]), Masse 2, Preis 50, Tags: basic
- Werte: cable_length=-431602080, force_emitter_max_force=2000, type=33

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| RPS B | Drehmoment | Eingang | (0, 1, 0) | Power connection B. |
| RPS A | Drehmoment | Eingang | (0, 0, 0) | Power connection A. |
| Clutch Pressure | Zahl | Eingang | (0, 0, 0) | A number between 0 and 1 representing the clutch engagement factor. |
| Electric | Strom | Eingang | (0, 0, 0) | The electric connection to power the component. |

## Compact Linear Track Base (`linear_compact_base`)

*A compact slider that moves along a modular linear track.*
You can build the track using the Compact Linear Track Extension component. The speed of the slider can be set using its number input.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 2, Preis 20
- Werte: buoy_factor=1.000000, buoy_force=100.000000, buoy_radius=1.000000, child_name=linear_compact_head, constraint_axis=2, constraint_range_of_motion=0.000000, constraint_type=1, door_lower_limit=-1.000000, door_upper_limit=1.000000, dynamic_min_rotation=0.000000, engine_max_force=1000.000000, extender_name=linear_compact_module, force_emitter_max_force=1000.000000, force_emitter_max_vector=1.000000, light_fov=1.000000, light_intensity=0.000000, light_range=1.000000, magnet_force=1.000000, max_motor_force=10000.000000, rudder_surface_area=0.000000, type=7, wheel_radius=0.250000
- Zweiter Körper (Gelenk) bei [0, 1, 0]

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Slider Speed | Zahl | Eingang | (0, 0, 0) |  |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Compact Linear Track Extension (`linear_compact_module`)

*An extension piece that can be used to build compact linear tracks.*
A Compact Linear Track Base must be attached somewhere along the track for it to function.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 20
- Werte: buoy_factor=1.000000, buoy_force=100.000000, buoy_radius=1.000000, constraint_axis=2, constraint_range_of_motion=0.000000, constraint_type=1, door_lower_limit=-1.000000, door_upper_limit=1.000000, dynamic_min_rotation=0.000000, engine_max_force=1000.000000, force_emitter_max_force=1000.000000, force_emitter_max_vector=1.000000, light_fov=1.000000, light_intensity=0.000000, light_range=1.000000, magnet_force=1.000000, max_motor_force=200.000000, rudder_surface_area=0.000000, type=9, wheel_radius=0.250000

## Compact Linear Track Head (`linear_compact_head`)


- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 3, Preis 0
- Werte: buoy_factor=1.000000, buoy_force=100.000000, buoy_radius=1.000000, constraint_range_of_motion=0.000000, door_lower_limit=-1.000000, door_upper_limit=1.000000, dynamic_min_rotation=0.000000, engine_max_force=1000.000000, force_emitter_max_force=1000.000000, force_emitter_max_vector=1.000000, light_fov=1.000000, light_intensity=0.000000, light_range=1.000000, magnet_force=1.000000, max_motor_force=100.000000, rudder_surface_area=0.000000, type=7, wheel_radius=0.250000

## Compact Pivot (`multibody_compact_pivot_b`)


- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 0
- Werte: buoy_factor=1.000000, buoy_force=100.000000, buoy_radius=1.000000, constraint_range_of_motion=0.000000, door_lower_limit=-1.000000, door_upper_limit=1.000000, dynamic_min_rotation=0.000000, engine_max_force=1000.000000, force_emitter_max_force=1000.000000, force_emitter_max_vector=1.000000, light_fov=1.000000, light_intensity=1.000000, light_range=1.000000, magnet_force=1.000000, max_motor_force=100.000000, rudder_surface_area=1.000000, type=7, wheel_radius=0.250000

## Compact Pivot (Power) (`multibody_compact_pivot_torque_a`)

*A small pivot that can rotate freely about its axis.*

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 40
- Werte: child_name=multibody_compact_pivot_torque_b, max_motor_force=200, type=7
- Zweiter Körper (Gelenk) bei [0, 1, 0]

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| RPS | Drehmoment | Ausgang | (0, 0, 0) | Power connection for transfering mechanical energy. |

## Compact Pivot (Power) (`multibody_compact_pivot_torque_b`)


- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 0
- Werte: type=7

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| RPS | Drehmoment | Ausgang | (0, 0, 0) | Power connection for transfering mechanical energy. |

## Compact Robotic Pivot (`multibody_compact_pivot_robotic_a`)

*A small robotic pivot that will orientate towards the input value within its range of motion.*
The pivot has a range of motion of 0.25 turns in both directions. A standard input value sets the target orientation within the pivot's range of motion. The pivot's speed can be configured by selecting it with the select tool.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 40
- Werte: buoy_factor=1.000000, buoy_force=100.000000, buoy_radius=1.000000, child_name=multibody_compact_pivot_b, constraint_range_of_motion=0.500000, door_lower_limit=-1.000000, door_upper_limit=1.000000, dynamic_max_rotation=0.000000, dynamic_min_rotation=0.000000, engine_max_force=1000.000000, force_emitter_max_force=1000.000000, force_emitter_max_vector=1.000000, light_fov=1.000000, light_intensity=1.000000, light_range=1.000000, magnet_force=1.000000, max_motor_force=200.000000, rudder_surface_area=1.000000, type=7, wheel_radius=0.250000
- Zweiter Körper (Gelenk) bei [0, 1, 0]

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Rotation Target | Zahl | Eingang | (0, 0, 0) | The standard value setting the orientation within the range of motion. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Compact Velocity Pivot (`multibody_compact_pivot_velocity_a`)

*A small pivot that will continuously rotate at a set input speed.*
Inputting a value of 0 will cause it to stop.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 40
- Werte: buoy_factor=1.000000, buoy_force=100.000000, buoy_radius=1.000000, child_name=multibody_compact_pivot_b, constraint_range_of_motion=0.000000, door_lower_limit=-1.000000, door_upper_limit=1.000000, dynamic_max_rotation=0.000000, dynamic_min_rotation=0.000000, engine_max_force=1000.000000, force_emitter_max_force=1000.000000, force_emitter_max_vector=1.000000, light_fov=1.000000, light_intensity=1.000000, light_range=1.000000, magnet_force=1.000000, max_motor_force=100.000000, rudder_surface_area=1.000000, type=7, wheel_radius=0.250000
- Zweiter Körper (Gelenk) bei [0, 1, 0]

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Rotational Speed | Zahl | Eingang | (0, 0, 0) | The speed at which the pivot should rotate. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Door Frame Controller (`door_frame_controller`)

*Controller unit for sealing door frames.*
Placing the controller as part of a door frame will let you lock the door when closed, and check whether the door is closed enough to be forming a seal. Only one controller should be placed per frame.

- Größe 2x1x1 Blöcke (voxel [-1, 0, 0] .. [0, 0, 0]), Masse 10, Preis 100
- Werte: cable_length=-431602080, custom_door_type=4, type=30

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Lock Seal | An/Aus | Eingang | (0, 0, 0) | Controls if the door panel will lock in place when sealed. |
| Seal State | An/Aus | Ausgang | (-1, 0, 0) | Indicates if the door panel is closed and forming a seal. |

## Door Frame Corner (`door_frame_corner`)

*A corner piece for building openings to sealed fluid compartments.*
To create a valid frame, there must be a continuous loop of frame parts in a consistent orientation with no other parts inside the frame.

- Größe 2x2x1 Blöcke (voxel [-1, 0, 0] .. [0, 1, 0]), Masse 15, Preis 50
- Werte: cable_length=-431602080, custom_door_type=1, type=30

## Door Frame Edge (`door_frame_straight`)

*A straight edge for building openings to sealed fluid compartments.*
To create a valid frame, there must be a continuous loop of frame parts in a consistent orientation with no other parts inside the frame.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 5, Preis 10
- Werte: cable_length=-431602080, type=30

## Door Panel Corner (`door_panel_corner`)

*A corner piece for building door panels.*
A valid door panel can be created with a loop of door panel pieces, filled with blocks flush to the outer face. Door panels must also fill a door frame and be built in their closed position within the frame to be valid.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 5, Preis 20
- Werte: cable_length=-431602080, custom_door_type=3, type=30

## Door Panel Edge (`door_panel_straight`)

*A straight edge piece for building door panels.*
A valid door panel can be created with a loop of door panel pieces, filled with blocks flush to the outer face. Door panels must also fill a door frame and be built in their closed position within the frame to be valid.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 5, Preis 10
- Werte: cable_length=-431602080, custom_door_type=2, type=30

## Electric Connector (`connector_electric`)

*A small electric connector that can be used to transfer electric energy between vehicles.*
Two electric connectors will attach when they are within close proximity. When connected, electric energy will flow freely between the connectors.

- Größe 1x2x1 Blöcke (voxel [0, 0, 0] .. [0, 1, 0]), Masse 2, Preis 20, Tags: magnet
- Werte: cable_radius=0, connector_type=4, light_intensity=0, logic_gate_type=1, magnet_force=0.1, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, type=17

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Release Connector | An/Aus | Eingang | (0, 0, 0) | Release the connector when receiving an on signal. |
| Connected | An/Aus | Ausgang | (0, 1, 0) | Outputs an on signal if the connector is attached to another connector. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |
| Composite Data Send | Composite | Eingang | (0, 0, 0) | Composite data to send to the connected connector. |
| Composite Data Receive | Composite | Ausgang | (0, 1, 0) | Composite data to receive from the connected connector. |
| Video Data Send | Video | Eingang | (0, 0, 0) | Video data to send to the connected connector. |
| Video Data Receive | Video | Ausgang | (0, 1, 0) | Video data to receive from the connected connector. |

## Fluid Connector (`connector_water`)

*A fluid connector that can be used to transfer fluid between vehicles.*
Two fluid connectors will attach when they are within close proximity. When connected, fluid will flow freely between the connectors.

- Größe 1x2x1 Blöcke (voxel [0, 0, 0] .. [0, 1, 0]), Masse 2, Preis 20, Tags: magnet
- Werte: cable_radius=0, connector_type=3, light_intensity=0, logic_gate_type=1, magnet_force=0.1, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, type=17

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Release Connector | An/Aus | Eingang | (0, 0, 0) | Release the connector when receiving an on signal. |
| Connected | An/Aus | Ausgang | (0, 1, 0) | Outputs an on signal if the connector is attached to another connector. |
| Fluid | Fluessigkeit/Gas | Ausgang | (0, 0, 0) | Fluid connection to link to another fluid connector. |
| Composite Data Send | Composite | Eingang | (0, 0, 0) | Composite data to send to the connected connector. |
| Composite Data Receive | Composite | Ausgang | (0, 1, 0) | Composite data to receive from the connected connector. |
| Video Data Send | Video | Eingang | (0, 0, 0) | Video data to send to the connected connector. |
| Video Data Receive | Video | Ausgang | (0, 1, 0) | Video data to receive from the connected connector. |

## Gearbox (`torque_gearbox`)

*Gearbox for changing the torque and speed across power connections.*
The ratio can be toggled between two values which can be set in the properties.

- Größe 1x2x2 Blöcke (voxel [0, 0, -1] .. [0, 1, 0]), Masse 8, Preis 100
- Werte: cable_length=-431602080, torque_component_type=1, type=33

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| RPS A | Drehmoment | Eingang | (0, 0, -1) | Power connection A. |
| RPS B | Drehmoment | Eingang | (0, 1, 0) | Power connection B. |
| Gear Switch | An/Aus | Eingang | (0, 1, -1) | Toggle between the two gear ratios. |
| Electric | Strom | Eingang | (0, 0, 0) | The electric connection to power the component. |

## Gearbox (`torque_gearbox_2`)

*Gearbox for changing the torque and speed across power connections.*
The ratio can be toggled between two values which can be set in the properties. This gearbox operates up to a torque difference of 4000.

- Größe 1x2x2 Blöcke (voxel [0, 0, 0] .. [0, 1, 1]), Masse 8, Preis 100
- Werte: cable_length=-431602080, force_emitter_max_force=9999999, torque_component_type=1, type=33

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| RPS A | Drehmoment | Eingang | (0, 0, 0) | Power connection A. |
| RPS B | Drehmoment | Eingang | (0, 1, 1) | Power connection B. |
| Gear Switch | An/Aus | Eingang | (0, 1, 0) | Toggle between the two gear ratios. |
| Electric | Strom | Eingang | (0, 0, 1) | The electric connection to power the component. |

## Gearbox 1x1 (`modular_engine_gearbox_1x1`)

*Gearbox for changing the torque and speed across power connections.*
The ratio can be toggled between two values which can be set in the properties.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 50, Tags: basic
- Werte: cable_length=-431602080, force_emitter_max_force=200, torque_component_type=1, type=33

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| RPS A | Drehmoment | Eingang | (0, 0, 0) | Power connection A. |
| RPS B | Drehmoment | Eingang | (0, 0, 0) | Power connection B. |
| Gear Switch | An/Aus | Eingang | (0, 0, 0) | Toggle between the two gear ratios. |
| Electric | Strom | Eingang | (0, 0, 0) | The electric connection to power the component. |

## Gearbox 3x3 (`modular_engine_gearbox_3x3`)

*Gearbox for changing the torque and speed across power connections.*
The ratio can be toggled between two values which can be set in the properties.

- Größe 3x2x3 Blöcke (voxel [-1, 0, -1] .. [1, 1, 1]), Masse 9, Preis 100
- Werte: cable_length=-431602080, force_emitter_max_force=1200, torque_component_type=1, type=33

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| RPS A | Drehmoment | Eingang | (0, 0, 0) | Power connection A. |
| RPS B | Drehmoment | Eingang | (0, 1, 0) | Power connection B. |
| Gear Switch | An/Aus | Eingang | (0, 1, 0) | Toggle between the two gear ratios. |
| Electric | Strom | Eingang | (0, 0, 0) | The electric connection to power the component. |

## Gearbox 5x5 (`modular_engine_gearbox_5x5`)

*Gearbox for changing the torque and speed across power connections.*
The ratio can be toggled between two values which can be set in the properties.

- Größe 5x3x5 Blöcke (voxel [-2, -1, -2] .. [2, 1, 2]), Masse 25, Preis 150
- Werte: cable_length=-431602080, force_emitter_max_force=5000, torque_component_type=1, type=33

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| RPS A | Drehmoment | Eingang | (0, -1, 0) | Power connection A. |
| RPS B | Drehmoment | Eingang | (0, 1, 0) | Power connection B. |
| Gear Switch | An/Aus | Eingang | (0, 1, 0) | Toggle between the two gear ratios. |
| Electric | Strom | Eingang | (0, -1, 0) | The electric connection to power the component. |

## Hardpoint Connector Attachment (`connector_hardpoint_b`)

*A hardpoint connector for building detachable vehicle sections.*
A hardpoint body will connect to a hardpoint attachment when correctly aligned, fixing the two components in place while transferring logic and fluid.

- Größe 1x2x1 Blöcke (voxel [0, 0, 0] .. [0, 1, 0]), Masse 2, Preis 20
- Werte: cable_radius=0, connector_type=8, light_intensity=0, logic_gate_type=1, magnet_force=0.1, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, type=17

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Launched | An/Aus | Ausgang | (0, 0, 0) | Outputs an on signal if the connector is sent a launch signal by the parent. |
| Fluid | Fluessigkeit/Gas | Ausgang | (0, 0, 0) | Fluid connection to link to another fluid connector. |
| Composite Data Send | Composite | Eingang | (0, 1, 0) | Composite data to send to the connected connector. |
| Composite Data Receive | Composite | Ausgang | (0, 0, 0) | Composite data to receive from the connected connector. |
| Video Data Send | Video | Eingang | (0, 1, 0) | Video data to send to the connected connector. |
| Video Data Receive | Video | Ausgang | (0, 0, 0) | Video data to receive from the connected connector. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Hardpoint Connector Attachment (Round) (`connector_hardpoint_b_round`)

*A hardpoint connector for building detachable vehicle sections.*
A hardpoint body will connect to a hardpoint attachment when correctly aligned, fixing the two components in place while transferring logic and fluid.

- Größe 1x2x1 Blöcke (voxel [0, 0, 0] .. [0, 1, 0]), Masse 2, Preis 20
- Werte: cable_radius=0, connector_type=8, light_intensity=0, logic_gate_type=1, magnet_force=0.1, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, type=17

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Launched | An/Aus | Ausgang | (0, 0, 0) | Outputs an on signal if the connector is sent a launch signal by the parent. |
| Fluid | Fluessigkeit/Gas | Ausgang | (0, 0, 0) | Fluid connection to link to another fluid connector. |
| Composite Data Send | Composite | Eingang | (0, 1, 0) | Composite data to send to the connected connector. |
| Composite Data Receive | Composite | Ausgang | (0, 0, 0) | Composite data to receive from the connected connector. |
| Video Data Send | Video | Eingang | (0, 1, 0) | Video data to send to the connected connector. |
| Video Data Receive | Video | Ausgang | (0, 0, 0) | Video data to receive from the connected connector. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Hardpoint Connector Body (`connector_hardpoint_a`)

*A hardpoint connector for building detachable vehicle sections.*
A hardpoint body will connect to a hardpoint attachment when correctly aligned, fixing the two components in place while transferring logic and fluid. The hardpoint body can release the connection by receiving an on/off input signal.

- Größe 1x1x3 Blöcke (voxel [0, 0, -1] .. [0, 0, 1]), Masse 2, Preis 20
- Werte: cable_radius=0, connector_type=7, light_intensity=0, logic_gate_type=1, magnet_force=0.1, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, type=17

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Ordinance Type | Zahl | Ausgang | (0, 0, -1) | Returns the ordinance type of the attached object. |
| Release | An/Aus | Eingang | (0, 0, 0) | Release the connector when receiving an on signal. |
| Launch | An/Aus | Eingang | (0, 0, 1) | Release the connector and activate the ordinance when receiving an on signal. |
| Fluid | Fluessigkeit/Gas | Ausgang | (0, 0, 1) | Fluid connection to link to another fluid connector. |
| Composite Data Send | Composite | Eingang | (0, 0, 0) | Composite data to send to the connected connector. |
| Composite Data Receive | Composite | Ausgang | (0, 0, -1) | Composite data to receive from the connected connector. |
| Video Data Send | Video | Eingang | (0, 0, 0) | Video data to send to the connected connector. |
| Video Data Receive | Video | Ausgang | (0, 0, -1) | Video data to receive from the connected connector. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Hinge Connector (`connector_hinge`)

*A small magnetic connector that can be used to attach two or more vehicles together.*
Two connectors will attach when they are within close proximity and both are switched on. They will connect along their long edge and hinge along this axis. An on/off output allows you to check whether or not this connector is currently attached to anything.

- Größe 1x2x3 Blöcke (voxel [0, 0, -1] .. [0, 1, 1]), Masse 3, Preis 40, Tags: magnet
- Werte: buoy_factor=1.000000, buoy_force=100.000000, buoy_radius=1.000000, connector_type=2, constraint_range_of_motion=0.000000, door_lower_limit=-1.000000, door_upper_limit=1.000000, dynamic_min_rotation=0.000000, engine_max_force=1000.000000, force_emitter_max_force=1000.000000, force_emitter_max_vector=1.000000, light_fov=1.000000, light_intensity=0.000000, light_range=1.000000, logic_gate_type=1, magnet_force=0.15, max_motor_force=100.000000, rudder_surface_area=0.000000, type=17, wheel_radius=0.250000

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Magnet Toggle | An/Aus | Eingang | (0, 0, 0) | Enables the connector's magnet when receiving an on signal. |
| Connected | An/Aus | Ausgang | (0, 0, 1) | Outputs an on signal if the connector is attached to another connector. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |
| Composite Data Send | Composite | Eingang | (0, 0, 0) | Composite data to send to the connected connector. |
| Composite Data Receive | Composite | Ausgang | (0, 0, 1) | Composite data to receive from the connected connector. |
| Video Data Send | Video | Eingang | (0, 0, 0) | Video data to send to the connected connector. |
| Video Data Receive | Video | Ausgang | (0, 1, 0) | Video data to receive from the connected connector. |

## Hinged Dock Door (`door_dock_large`)

*Hinged door that can be opened and closed using an on/off signal.*

- Größe 9x5x1 Blöcke (voxel [-4, -2, 0] .. [4, 2, 0]), Masse 20, Preis 300, Tags: door,basic
- Werte: cable_radius=0, door_lower_limit=-2, door_side_dist=6, door_up_dist=2, dynamic_max_rotation=0, light_intensity=0, magnet_force=0.2, max_motor_force=0, pump_pressure=0, rudder_surface_area=0, type=29

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Open/Close | An/Aus | Eingang | (0, 1, 0) | Opens the door when receiving an on signal, and closes it when receiving an off signal. |
| Magnet Toggle | An/Aus | Eingang | (0, 2, 0) | Enables the door's magnet when receiving an on signal. |
| Connected | An/Aus | Ausgang | (-1, 2, 0) | Outputs an on signal if the door is attached to another door. |
| On/Off Sent | An/Aus | Eingang | (1, -1, 0) | An on/off signal to send to a connected door. |
| On/Off Received | An/Aus | Ausgang | (1, 0, 0) | The on/off signal received from a connected door. |
| Number Sent | Zahl | Eingang | (1, 1, 0) | A number signal to send to a connected door. |
| Number Received | Zahl | Ausgang | (1, 2, 0) | The number value received from a connected door. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |
| Composite output | Composite | Ausgang | (0, -1, 0) | Composite data output. |
| Composite input | Composite | Eingang | (0, 0, 0) | Composite data input. |

## Hinged Dock Hatch (`door_dock_small`)

*Hinged door that can be opened and closed using an on/off signal.*

- Größe 5x5x1 Blöcke (voxel [-2, -2, 0] .. [2, 2, 0]), Masse 15, Preis 200, Tags: door,basic
- Werte: cable_radius=0, door_lower_limit=-2, door_side_dist=2, door_up_dist=2, dynamic_max_rotation=0, light_intensity=0, magnet_force=0.2, max_motor_force=0, pump_pressure=0, rudder_surface_area=0, type=29

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Open/Close | An/Aus | Eingang | (0, 1, 0) | Opens the door when receiving an on signal, and closes it when receiving an off signal. |
| Magnet Toggle | An/Aus | Eingang | (0, 2, 0) | Enables the door's magnet when receiving an on signal. |
| Connected | An/Aus | Ausgang | (-1, 2, 0) | Outputs an on signal if the door is attached to another door. |
| On/Off Sent | An/Aus | Eingang | (1, -1, 0) | An on/off signal to send to a connected door. |
| On/Off Received | An/Aus | Ausgang | (1, 0, 0) | The on/off signal received from a connected door. |
| Number Sent | Zahl | Eingang | (1, 1, 0) | A number signal to send to a connected door. |
| Number Received | Zahl | Ausgang | (1, 2, 0) | The number value received from a connected door. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |
| Composite output | Composite | Ausgang | (0, -1, 0) | Composite data output. |
| Composite input | Composite | Eingang | (0, 0, 0) | Composite data input. |

## Hinged Door (`door_manual_large`)

*Hinged door that can be opened and closed by hand and locked using an on/off signal.*

- Größe 7x4x1 Blöcke (voxel [-3, -2, 0] .. [3, 1, 0]), Masse 20, Preis 200, Tags: door,basic
- Werte: cable_radius=0, door_lower_limit=-2, door_side_dist=6, door_up_dist=2, dynamic_max_rotation=0, light_intensity=0, magnet_force=0.2, max_motor_force=0, pump_pressure=0, rudder_surface_area=0, type=50

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Lock | An/Aus | Eingang | (0, 1, 0) | Locks the door when receiving an on signal. |

## Hinged Hatch (`door_manual_small`)

*Hinged door that can be opened and closed by hand and locked using an on/off signal.*

- Größe 3x4x1 Blöcke (voxel [-1, -2, 0] .. [1, 1, 0]), Masse 15, Preis 150, Tags: door,basic
- Werte: cable_radius=0, door_lower_limit=-2, door_side_dist=2, door_up_dist=2, dynamic_max_rotation=0, light_intensity=0, magnet_force=0.2, max_motor_force=0, pump_pressure=0, rudder_surface_area=0, type=50

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Lock | An/Aus | Eingang | (0, 1, 0) | Locks the door when receiving an on signal. |

## Key Button (`button_key`)

*A button that must be held down for a set duration before activating.*
Once activated, interacting with the button again will deactivate it instantly. The hold duration can be customised by selecting this component with the select tool. The external input can be used to simulate interacting with the button down using the output of another component. The button's default state can be configured by selecting it with the select component.

- Größe 1x2x1 Blöcke (voxel [0, 0, 0] .. [0, 1, 0]), Masse 1, Preis 20, Tags: basic
- Werte: buoy_factor=1.000000, buoy_force=100.000000, buoy_radius=1.000000, button_type=2, constraint_range_of_motion=0.000000, door_lower_limit=0.000000, door_upper_limit=0.000000, dynamic_max_rotation=0.000000, dynamic_min_rotation=0.000000, engine_max_force=1000.000000, force_emitter_max_force=1000.000000, force_emitter_max_vector=1.000000, light_fov=0.000000, light_intensity=0.000000, light_range=0.000000, magnet_force=0.000000, max_motor_force=0.000000, rudder_surface_area=0.000000, type=8, wheel_radius=0.250000

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Activated | An/Aus | Ausgang | (0, 0, 0) | Outputs an on signal when interacting with the button for the set duration. |
| External Input | An/Aus | Eingang | (0, 1, 0) | Allows an external on/off signal to hold the button down. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Large Connector (`connector_large`)

*A magnetic connector that can be used to attach two or more vehicles together.*
Two large connectors will attach when they are within close proximity and both are switched on. The additional inputs and outputs allow you to send and receive power and signals between two connected magnets, giving you a limited amount of control over a linked vehicle. An additional on/off output allows you to check whether or not this connector is currently attached to anything.

- Größe 3x2x3 Blöcke (voxel [-1, 0, -1] .. [1, 1, 1]), Masse 20, Preis 50, Tags: magnet
- Werte: cable_radius=0.02, light_intensity=0, logic_gate_type=1, magnet_force=0.2, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, type=17

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Magnet Toggle | An/Aus | Eingang | (0, 0, 0) | Enables the connector's magnet when receiving an on signal. |
| On/Off Sent | An/Aus | Eingang | (-1, 1, 0) | An on/off signal to send to a connected magnet. |
| Number Received | Zahl | Ausgang | (0, 1, 1) | The number value received from a connected magnet. |
| Number Sent | Zahl | Eingang | (1, 1, 0) | A number signal to send to a connected magnet. |
| Connected | An/Aus | Ausgang | (-1, 0, 0) | Outputs an on signal if the connector is attached to another connector. |
| On/Off Received | An/Aus | Ausgang | (0, 1, -1) | The on/off signal received from a connected magnet. |
| RPS | Drehmoment | Ausgang | (0, 0, 1) | Power connection for transfering mechanical energy to another connector. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |
| Fluid | Fluessigkeit/Gas | Eingang | (0, 0, -1) | Fluid connection for transfering fluid to another connector. |
| Composite Data Send | Composite | Eingang | (0, 0, 0) | Composite data to send to the connected connector. |
| Composite Data Receive | Composite | Ausgang | (0, 1, 0) | Composite data to receive from the connected connector. |
| Video Data Send | Video | Eingang | (0, 0, 0) | Video data to send to the connected connector. |
| Video Data Receive | Video | Ausgang | (0, 1, 0) | Video data to receive from the connected connector. |

## Large Keypad (`button_keypad_large`)

*A keypad that allows 2 numbers to be input.*
Interacting with the keypad will show a menu where the 2 numbers can be entered, along with a button for quickly inputting waypoint coordinates. A short pulse will be emitted from the keypad's pulse node when the confirm button is clicked and the stored numbers will be continuously output from the other output nodes. An on/off signal controls whether or not the keypad's backlight is enabled.

- Größe 1x2x2 Blöcke (voxel [0, 0, 0] .. [0, 1, 1]), Masse 1, Preis 40, Tags: button,input
- Werte: button_type=6, cable_radius=0.02, door_lower_limit=0, door_upper_limit=0, dynamic_max_rotation=0, light_fov=0, light_intensity=0, light_range=0, magnet_force=0, max_motor_force=0, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, type=8

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Output A | Zahl | Ausgang | (0, 0, 0) | Outputs the first stored value. |
| Backlight | An/Aus | Eingang | (0, 1, 0) | Enables the backlight when receiving an on signal. |
| Output B | Zahl | Ausgang | (0, 0, 1) | Outputs the second stored value. |
| Pulse | An/Aus | Ausgang | (0, 1, 1) | Emits a short pulse when a value is entered. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Linear Track Base (`linear_base`)

*A slider that moves along a modular linear track.*
You can build the track using the Linear Track Extension component. This base component provides 3 blocks that can be built on. A pair of on/off signals allow you to control the up and down motion of the slider, and a numerical output lets you measure the slider's offset from its starting position. Multiple slider bases can run along the same track. The up/down speed can be configured by selecting this component with the select tool.

- Größe 3x2x1 Blöcke (voxel [-1, 0, 0] .. [1, 1, 0]), Masse 3, Preis 40
- Werte: cable_radius=0.02, child_name=linear_head, constraint_axis=2, constraint_type=1, extender_name=linear_module, light_intensity=0, max_motor_force=20000, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, type=7
- Zweiter Körper (Gelenk) bei [0, 2, 0]

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Down | An/Aus | Eingang | (0, 0, 0) | Moves the slider in the track's down direction (indicated by the hollow arrow). |
| Up | An/Aus | Eingang | (-1, 0, 0) | Moves the slider in the track's up direction (indicated by the filled arrow). |
| Slider Position | Zahl | Ausgang | (1, 0, 0) | The measured offset of the slider from its starting position. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |
| RPS | Drehmoment | Eingang | (-1, 0, 0) | Power connection for transfering mechanical energy. |
| Fluid | Fluessigkeit/Gas | Eingang | (1, 0, 0) | Fluid connection for transfering fluid. |

## Linear Track Extension (`linear_module`)

*An extension piece that can be used to build linear tracks.*
A Linear Track Base must be attached somewhere along the track for it to function.

- Größe 3x2x1 Blöcke (voxel [-1, 0, 0] .. [1, 1, 0]), Masse 3, Preis 10
- Werte: buoy_factor=1.000000, buoy_force=100.000000, buoy_radius=1.000000, constraint_axis=2, constraint_range_of_motion=0.000000, constraint_type=1, door_lower_limit=-1.000000, door_upper_limit=1.000000, dynamic_min_rotation=0.000000, engine_max_force=1000.000000, force_emitter_max_force=1000.000000, force_emitter_max_vector=1.000000, light_fov=1.000000, light_intensity=0.000000, light_range=1.000000, magnet_force=1.000000, max_motor_force=200.000000, rudder_surface_area=0.000000, type=9, wheel_radius=0.250000

## Linear Track Head (`linear_head`)


- Größe 3x1x1 Blöcke (voxel [-1, 0, 0] .. [1, 0, 0]), Masse 3, Preis 0
- Werte: cable_radius=0.02, light_intensity=0, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, type=7

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| RPS | Drehmoment | Eingang | (-1, 0, 0) | Power connection for transfering mechanical energy. |
| Fluid | Fluessigkeit/Gas | Eingang | (1, 0, 0) | Fluid connection for transfering fluid. |

## Lockable Button (`button_lock`)

*A toggle button that can only be interacted with when unlocked.*
An on signal must be sent to the button's unlock node to allow player interaction. The button's default state can be configured by selecting it with the select component.

- Größe 1x2x1 Blöcke (voxel [0, 0, 0] .. [0, 1, 0]), Masse 1, Preis 20
- Werte: buoy_factor=1.000000, buoy_force=100.000000, buoy_radius=1.000000, button_type=3, constraint_range_of_motion=0.000000, door_lower_limit=0.000000, door_upper_limit=0.000000, dynamic_max_rotation=0.000000, dynamic_min_rotation=0.000000, engine_max_force=1000.000000, force_emitter_max_force=1000.000000, force_emitter_max_vector=1.000000, light_fov=0.000000, light_intensity=0.000000, light_range=0.000000, magnet_force=0.000000, max_motor_force=0.000000, rudder_surface_area=0.000000, type=8, wheel_radius=0.250000

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Toggled | An/Aus | Ausgang | (0, 0, 0) | Outputs an on/off signal that can be toggled by interacting with [$[action_interact_left]]/[$[action_interact_right]] when unlocked. |
| Unlock | An/Aus | Eingang | (0, 1, 0) | Allows the button to be interacted with when receiving an on signal. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Mag All (`magall`)

*A small connector that will attach to most surfaces.*
While the connector is active the end will glow and it will stick to most surfaces that it touches. The connection will break if enough stress (200) is applied.

- Größe 1x3x1 Blöcke (voxel [0, 0, 0] .. [0, 2, 0]), Masse 5, Preis 250, Tags: magnet
- Werte: cable_radius=0, connector_type=1, light_intensity=0, logic_gate_type=1, magnet_force=0.1, max_motor_speed=5, rudder_surface_area=0, type=27

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Magnet Toggle | An/Aus | Eingang | (0, 0, 0) | Enables the connector's magnet when receiving an on signal. |
| Connected | An/Aus | Ausgang | (0, 1, 0) | Outputs an on signal if the connector is attached to another connector. |
| Force | Zahl | Ausgang | (0, 2, 0) | Outputs the current force stress on the connector. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Piston Suspension (`multibody_piston_suspension_a`)

*A shock absorber that can be used to improve handling of land-based vehicles.*
A dampened hydraulic sprung piston.

- Größe 1x2x1 Blöcke (voxel [0, 0, 0] .. [0, 1, 0]), Masse 20, Preis 20
- Werte: cable_radius=0.02, child_name=multibody_piston_suspension_b, constraint_range_of_motion=0.5, constraint_type=1, light_intensity=0, magnet_force=0, max_motor_force=1000, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, type=7
- Zweiter Körper (Gelenk) bei [0, 2, 0]

## Piston Suspension (`multibody_piston_suspension_b`)


- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 20, Preis 0
- Werte: cable_radius=0.02, constraint_type=1, light_intensity=0, magnet_force=0, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, type=7

## Pivot (`multibody_pivot_a`)

*A basic pivot that can move freely.*
The pivot can rotate to 0.25 turns in both directions.

- Größe 1x2x1 Blöcke (voxel [0, 0, 0] .. [0, 1, 0]), Masse 1, Preis 20, Tags: hinge
- Werte: button_type=0, cable_length=0, cable_radius=0.02, child_name=multibody_pivot_b, constraint_axis=2, constraint_range_of_motion=0.5, door_lower_limit=0, door_upper_limit=0, dynamic_max_rotation=0, light_fov=0, light_intensity=0, light_range=0, magnet_force=0, max_motor_force=20, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, type=7, wheel_radius=0
- Zweiter Körper (Gelenk) bei [0, 2, 0]

## Pivot (Power) (`multibody_pivot_torque_a`)

*A basic pivot that can move freely.*
The pivot can rotate to 0.25 turns in both directions.

- Größe 1x2x1 Blöcke (voxel [0, 0, 0] .. [0, 1, 0]), Masse 1, Preis 20, Tags: hinge
- Werte: child_name=multibody_pivot_torque_b, constraint_axis=2, constraint_range_of_motion=0.5, max_motor_force=20, rudder_surface_area=0, type=7
- Zweiter Körper (Gelenk) bei [0, 2, 0]

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| RPS | Drehmoment | Ausgang | (0, 0, 0) | Power connection for transfering mechanical energy. |

## Pneumatic Piston (`linear_matic_a`)

*A pneumatic piston that can be expanded and contracted.*
A standard value input sets the target position that the piston rod should move to. There is also an output for taking a measurement of the rod's current position. The piston can expand by a length of 1 metre, making it a total of 2.25m (9 blocks) tall when expanded and 1.25m (5 blocks) tall when contracted. The piston's speed can be configured by selecting it with the select tool.

- Größe 1x3x1 Blöcke (voxel [0, 0, 0] .. [0, 2, 0]), Masse 5, Preis 100
- Werte: cable_radius=0.02, child_name=linear_matic_b, constraint_range_of_motion=1, constraint_type=1, light_intensity=0, max_motor_force=200000, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, type=7
- Zweiter Körper (Gelenk) bei [0, 6, 0]

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Piston Rod Target Position | Zahl | Eingang | (0, 0, 0) | Takes a standard value representing the desired position of the rod. |
| Piston Rod Position | Zahl | Ausgang | (0, 1, 0) | The measured position of the rod between -0.5 and 0.5 metres. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |
| Fluid | Fluessigkeit/Gas | Eingang | (0, 0, 0) | Fluid connection for transfering fluid. |

## Pneumatic Piston (`linear_matic_b`)


- Größe 1x2x1 Blöcke (voxel [0, -1, 0] .. [0, 0, 0]), Masse 3, Preis 0
- Werte: cable_radius=0.02, light_intensity=0, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, type=7

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Fluid | Fluessigkeit/Gas | Eingang | (0, 0, 0) |  |

## Push Button (`button_push`)

*A button that outputs an on signal when you interact with [$[action_interact_left]]/[$[action_interact_right]], and an off signal when not interacting.*
An external on/off signal can also be used to control whether or not the button is pressed, allowing you to chain multiple buttons together to unify their outputs.

- Größe 1x2x1 Blöcke (voxel [0, 0, 0] .. [0, 1, 0]), Masse 1, Preis 10, Tags: basic
- Werte: buoy_factor=1.000000, buoy_force=100.000000, buoy_radius=1.000000, button_type=0, constraint_range_of_motion=0.000000, door_lower_limit=0.000000, door_upper_limit=0.000000, dynamic_max_rotation=0.000000, dynamic_min_rotation=0.000000, engine_max_force=1000.000000, force_emitter_max_force=1000.000000, force_emitter_max_vector=1.000000, light_fov=0.000000, light_intensity=0.000000, light_range=0.000000, magnet_force=0.000000, max_motor_force=0.000000, rudder_surface_area=0.000000, type=8, wheel_radius=0.250000

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Pressed | An/Aus | Ausgang | (0, 0, 0) | Outputs an on signal when you interact wtih [$[action_interact_left]]/[$[action_interact_right]], and an off signal otherwise. |
| External Input | An/Aus | Eingang | (0, 1, 0) | Allows an external on/off signal to control whether or not the button is pressed. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Push Button (2 Sided) (`button_push_2side`)

*A button that outputs an on signal when interacting with [$[action_interact_left]]/[$[action_interact_right]].*
An external on/off signal can also be used to control whether or not the button is pressed, allowing you to chain multiple buttons together to unify their outputs.

- Größe 1x2x1 Blöcke (voxel [0, 0, 0] .. [0, 1, 0]), Masse 1, Preis 10, Tags: basic
- Werte: button_type=0, cable_radius=0.02, door_lower_limit=0, door_upper_limit=0, dynamic_max_rotation=0, light_fov=0, light_intensity=0, light_range=0, magnet_force=0, max_motor_force=0, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, type=8

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Pressed | An/Aus | Ausgang | (0, 0, 0) | Outputs an on signal when you interact with [$[action_interact_left]]/[$[action_interact_right]], and an off signal otherwise. |
| External Input | An/Aus | Eingang | (0, 1, 0) | Allows an external on/off signal to control whether or not the button is pressed. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Reaction Wheel (`gyroscopic_stabilizer`)

*A stabilization system that outputs a force to counter the input rotation.*
This component can be wired directly to an aligned angular rotation sensor to stabilize its rotation.

- Größe 3x1x3 Blöcke (voxel [-1, 0, -1] .. [1, 0, 1]), Masse 15, Preis 300
- Werte: force_emitter_max_force=100, piston_cam=0, piston_len=0, radar_range=0, radar_speed=0, type=60

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |
| Rotation | Zahl | Eingang | (0, 0, 0) | Input rotation value. |

## Reaction Wheel (Large) (`gyroscopic_stabilizer_large`)

*A stabilization system that outputs a force to counter the input rotation.*
This component can be wired directly to an aligned angular rotation sensor to stabilize its rotation.

- Größe 5x3x5 Blöcke (voxel [-2, -1, -2] .. [2, 1, 2]), Masse 80, Preis 700
- Werte: piston_cam=0, piston_len=0, radar_range=0, radar_speed=0, type=60

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |
| Rotation | Zahl | Eingang | (0, 0, 0) | Input rotation value. |

## Reaction Wheel (Small) (`gyroscopic_stabilizer_small`)

*A stabilization system that outputs a force to counter the input rotation.*
This component can be wired directly to an aligned angular rotation sensor to stabilize its rotation.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 2, Preis 150
- Werte: force_emitter_max_force=10, piston_cam=0, piston_len=0, radar_range=0, radar_speed=0, type=60

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |
| Rotation | Zahl | Eingang | (0, 0, 0) | Input rotation value. |

## Robotic Door Hinge (`multibody_door_hinge_a`)

*A powered robotic hinge for custom sealable doors.*
The hinge has a range of motion of 0.25 in each direction. A standard input value sets the target orientation within the pivot's range of motion. The measured rotation of the hinge can be read from its output. The hinge's speed can be configured by selecting it with the select tool.

- Größe 1x2x3 Blöcke (voxel [0, 0, -1] .. [0, 1, 1]), Masse 3, Preis 400
- Werte: cable_radius=0.02, child_name=multibody_door_hinge_b, constraint_axis=2, constraint_range_of_motion=0.5, custom_door_type=5, light_intensity=0, max_motor_force=400, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, type=7
- Zweiter Körper (Gelenk) bei [0, 2, 0]

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Rotation Target | Zahl | Eingang | (0, 0, 0) | The standard value setting the orientation within the range of motion. |
| Current Rotation | Zahl | Ausgang | (0, 0, -1) | The hinge's measured rotation between -0.25 and 0.25. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Robotic Door Hinge (`multibody_door_hinge_b`)


- Größe 1x1x3 Blöcke (voxel [0, 0, -1] .. [0, 0, 1]), Masse 3, Preis 0
- Werte: cable_radius=0.02, constraint_axis=2, custom_door_type=5, light_intensity=0, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, type=7
- Zweiter Körper (Gelenk) bei [0, 2, 0]

## Robotic Hinge (`multibody_robotic_hinge_01_a`)

*A powered robotic hinge that will orientate towards the input value within its range of motion.*
The hinge has a range of motion of 0.25 turns in both directions. A standard input value sets the target orientation within the pivot's range of motion. The measured rotation of the hinge can be read from its output. The hinge's speed can be configured by selecting it with the select tool.

- Größe 1x2x3 Blöcke (voxel [0, 0, -1] .. [0, 1, 1]), Masse 3, Preis 400
- Werte: cable_radius=0.02, child_name=multibody_robotic_hinge_01_b, constraint_axis=2, constraint_range_of_motion=0.5, light_intensity=0, max_motor_force=400, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, type=7
- Zweiter Körper (Gelenk) bei [0, 2, 0]

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Rotation Target | Zahl | Eingang | (0, 0, 0) | The standard value setting the orientation within the range of motion. |
| Current Rotation | Zahl | Ausgang | (0, 0, -1) | The hinge's measured rotation between -0.25 and 0.25. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |
| RPS | Drehmoment | Eingang | (0, 0, 1) | Power connection for transfering mechanical energy. |
| Fluid | Fluessigkeit/Gas | Eingang | (0, 0, -1) | Fluid connection for transfering fluid. |

## Robotic Hinge (`multibody_robotic_hinge_01_b`)


- Größe 1x1x3 Blöcke (voxel [0, 0, -1] .. [0, 0, 1]), Masse 3, Preis 0
- Werte: cable_radius=0.02, constraint_axis=2, light_intensity=0, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, type=7
- Zweiter Körper (Gelenk) bei [0, 2, 0]

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| RPS | Drehmoment | Eingang | (0, 0, 1) | Power connection for transfering mechanical energy. |
| Fluid | Fluessigkeit/Gas | Eingang | (0, 0, -1) | Fluid connection for transfering fluid. |

## Robotic Pivot (Fluid) (`multibody_robotic_pivot_01_a_fluid`)

*A robotic pivot that will orientate towards the input value within its range of motion.*
The pivot has a range of motion of 0.25 turns in both directions. A standard input value sets the target orientation within the pivot's range of motion. The measured rotation of the pivot can be read from its output. The pivot's speed can be configured by selecting it with the select tool.

- Größe 3x1x3 Blöcke (voxel [-1, 0, -1] .. [1, 0, 1]), Masse 9, Preis 200
- Werte: button_type=0, cable_radius=0.02, child_name=multibody_robotic_pivot_01_b_fluid, constraint_range_of_motion=0.5, door_lower_limit=0, door_upper_limit=0, dynamic_max_rotation=0, light_fov=0, light_intensity=0, light_range=0, magnet_force=0, max_motor_force=200, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, type=7, wheel_radius=0
- Zweiter Körper (Gelenk) bei [0, 1, 0]

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Rotation Target | Zahl | Eingang | (0, 0, 0) | The standard value setting the orientation within the range of motion. |
| Current Rotation | Zahl | Ausgang | (0, 0, -1) | The pivot's measured rotation between -0.25 and 0.25. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |
| Fluid | Fluessigkeit/Gas | Eingang | (0, 0, 1) | Fluid connection for transfering fluids. |

## Robotic Pivot (Power) (`multibody_robotic_pivot_01_a`)

*A robotic pivot that will orientate towards the input value within its range of motion.*
The pivot has a range of motion of 0.25 turns in both directions. A standard input value sets the target orientation within the pivot's range of motion. The measured rotation of the pivot can be read from its output. The pivot's speed can be configured by selecting it with the select tool.

- Größe 3x1x3 Blöcke (voxel [-1, 0, -1] .. [1, 0, 1]), Masse 9, Preis 200
- Werte: button_type=0, cable_radius=0.02, child_name=multibody_robotic_pivot_01_b, constraint_range_of_motion=0.5, door_lower_limit=0, door_upper_limit=0, dynamic_max_rotation=0, light_fov=0, light_intensity=0, light_range=0, magnet_force=0, max_motor_force=200, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, type=7, wheel_radius=0
- Zweiter Körper (Gelenk) bei [0, 1, 0]

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Rotation Target | Zahl | Eingang | (0, 0, 0) | The standard value setting the orientation within the range of motion. |
| Current Rotation | Zahl | Ausgang | (0, 0, -1) | The pivot's measured rotation between -0.25 and 0.25. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |
| RPS | Drehmoment | Eingang | (0, 0, 1) | Power connection for transfering mechanical energy. |

## Sliding Connector Gripper (`connector_slider_gripper`)

*A connector that will attach to and slide along a connector track.*
The gripper will attach to a track when they are aligned and close enough, and will detach when it slides off the end or receives an on signal to the connector release input. The brake can be enabled to prevent the gripper from sliding along the track.

- Größe 1x2x1 Blöcke (voxel [0, 0, 0] .. [0, 1, 0]), Masse 2, Preis 20
- Werte: cable_radius=0.02, connector_type=5, constraint_axis=2, constraint_type=1, light_intensity=0, max_motor_force=10000, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, seat_health_per_sec=1, type=17
- Zweiter Körper (Gelenk) bei [0, 1, 0]

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Release Connector | An/Aus | Eingang | (0, 0, 0) | Releases the connector when receiving an on signal. |
| Brake | An/Aus | Eingang | (0, 1, 0) | Enables the gripper's brake to keep it in place on the track. |

## Sliding Connector Track (`connector_slider_track`)

*A connector that can be used to build a track for grippers to attach to.*
Gripper connectors will attach to the track when aligned and close enough, and will detach when they slide off the end.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 2, Preis 10
- Werte: cable_radius=0.02, connector_type=6, constraint_axis=2, constraint_type=1, light_intensity=0, max_motor_force=10000, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, seat_health_per_sec=1, type=17
- Zweiter Körper (Gelenk) bei [0, 1, 0]

## Sliding Door (`door_manual`)

*Sliding door that can be opened and closed by hand and locked using an on/off signal.*

- Größe 1x7x6 Blöcke (voxel [0, -3, -2] .. [0, 3, 3]), Masse 20, Preis 50, Tags: door,basic
- Werte: cable_radius=0, door_lower_limit=-2, door_side_dist=2, door_up_dist=6, dynamic_max_rotation=0, light_intensity=0, magnet_force=0, max_motor_force=0, pump_pressure=0, rudder_surface_area=0, type=51

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Lock | An/Aus | Eingang | (0, 1, 0) | Locks the door when receiving an on signal. |

## Sliding Door (Electric) (`door`)

*Sliding door that can be opened and closed using an on/off signal.*

- Größe 1x7x6 Blöcke (voxel [0, -3, -2] .. [0, 3, 3]), Masse 20, Preis 70, Tags: door,basic
- Werte: cable_radius=0, door_lower_limit=-2, door_side_dist=2, door_up_dist=6, dynamic_max_rotation=0, light_intensity=0, magnet_force=0, max_motor_force=0, pump_pressure=0, rudder_surface_area=0, type=13

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Open/Close | An/Aus | Eingang | (0, 1, 0) | Opens the door when receiving an on signal, and closes it when receiving an off signal. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Sliding Hatch (`door_manual_sliding_small`)

*Sliding door that can be opened and closed by hand and locked using an on/off signal.*

- Größe 1x3x6 Blöcke (voxel [0, -1, -2] .. [0, 1, 3]), Masse 20, Preis 40, Tags: door,basic
- Werte: cable_radius=0, door_lower_limit=-2, door_side_dist=2, door_up_dist=2, door_upper_limit=0.9, dynamic_max_rotation=0, light_intensity=0, magnet_force=0, max_motor_force=0, pump_pressure=0, rudder_surface_area=0, type=51

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Lock | An/Aus | Eingang | (0, 1, 0) | Locks the door when receiving an on signal. |

## Sliding Hatch (Electric) (`hatch`)

*Sliding hatch that can be opened and closed using an on/off signal.*

- Größe 1x3x6 Blöcke (voxel [0, -1, -2] .. [0, 1, 3]), Masse 15, Preis 50, Tags: door,basic
- Werte: cable_radius=0, door_lower_limit=-2, door_side_dist=2, door_up_dist=2, door_upper_limit=0.9, dynamic_max_rotation=0, light_intensity=0, magnet_force=0, max_motor_force=0, pump_pressure=0, rudder_surface_area=0, type=13

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Hatch Open/Close | An/Aus | Eingang | (0, 0, 0) | Opens the hatch when receiving an on signal, and closes it when receiving an off signal. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Small Connector (`connector_small`)

*A small magnetic connector that can be used to attach two or more vehicles together.*
Two small connectors will attach when they are within close proximity and both are switched on. An on/off output allows you to check whether or not this connector is currently attached to anything.

- Größe 1x2x1 Blöcke (voxel [0, 0, 0] .. [0, 1, 0]), Masse 2, Preis 20, Tags: magnet
- Werte: buoy_factor=1.000000, buoy_force=100.000000, buoy_radius=1.000000, connector_type=1, constraint_range_of_motion=0.000000, door_lower_limit=-1.000000, door_upper_limit=1.000000, dynamic_min_rotation=0.000000, engine_max_force=1000.000000, force_emitter_max_force=1000.000000, force_emitter_max_vector=1.000000, light_fov=1.000000, light_intensity=0.000000, light_range=1.000000, logic_gate_type=1, magnet_force=0.100000, max_motor_force=100.000000, rudder_surface_area=0.000000, type=17, wheel_radius=0.250000

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Magnet Toggle | An/Aus | Eingang | (0, 0, 0) | Enables the connector's magnet when receiving an on signal. |
| Connected | An/Aus | Ausgang | (0, 1, 0) | Outputs an on signal if the connector is attached to another connector. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |
| Composite Data Send | Composite | Eingang | (0, 0, 0) | Composite data to send to the connected connector. |
| Composite Data Receive | Composite | Ausgang | (0, 1, 0) | Composite data to receive from the connected connector. |
| Video Data Send | Video | Eingang | (0, 0, 0) | Video data to send to the connected connector. |
| Video Data Receive | Video | Ausgang | (0, 1, 0) | Video data to receive from the connected connector. |

## Small Keypad (`button_keypad_small`)

*A keypad that allows a number to be input.*
Interacting with the keypad will show a menu where the number can be entered. The stored numbers will be continuously output from the other output node. An on/off signal controls whether or not the keypad's backlight is enabled.

- Größe 1x2x1 Blöcke (voxel [0, 0, 0] .. [0, 1, 0]), Masse 1, Preis 20, Tags: button,input
- Werte: button_type=5, cable_radius=0.02, door_lower_limit=0, door_upper_limit=0, dynamic_max_rotation=0, light_fov=0, light_intensity=0, light_range=0, magnet_force=0, max_motor_force=0, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, type=8

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Output | Zahl | Ausgang | (0, 0, 0) | Outputs the stored value. |
| Backlight | An/Aus | Eingang | (0, 1, 0) | Enables the backlight when receiving an on signal. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Suspension (`multibody_suspension_a`)

*A shock absorber that can be used to improve handling of land-based vehicles.*
Power can be passed through the suspension, allowing you to attach and control a wheel at the end.

- Größe 2x3x3 Blöcke (voxel [0, 0, -1] .. [1, 2, 1]), Masse 5, Preis 50
- Werte: cable_length=0, cable_radius=0.02, child_name=multibody_suspension_b, constraint_axis=0, constraint_range_of_motion=0.5, constraint_type=1, light_intensity=0, magnet_force=0, max_motor_force=1000, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, type=7
- Zweiter Körper (Gelenk) bei [0, 3, 0]

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| RPS | Drehmoment | Eingang | (0, 0, 0) | Power connection for transfering mechanical energy. |

## Suspension (`multibody_suspension_b`)


- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 3, Preis 0
- Werte: cable_length=0, cable_radius=0.02, constraint_type=1, light_intensity=0, magnet_force=0, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, type=7

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| RPS | Drehmoment | Ausgang | (0, 0, 0) | Power connection for transfering mechanical energy. |

## Throttle Lever (`button_throttle_lever`)

*A throttle lever that acts as two buttons controlling one number output.*
The output ranges from -1 to 1, and will increase/decrease depending on which half of the lever you interact with. The two on/off inputs can be used to control the lever externally with different buttons. The speed of the lever can be configured by selecting this component with the select tool.

- Größe 2x2x1 Blöcke (voxel [0, 0, 0] .. [1, 1, 0]), Masse 1, Preis 30, Tags: basic
- Werte: button_type=4, cable_radius=0, door_lower_limit=0, door_upper_limit=0, dynamic_max_rotation=0, light_fov=0, light_intensity=0, light_range=0, magnet_force=0, max_motor_force=0, max_motor_speed=5, rudder_surface_area=0, type=8

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Up | An/Aus | Eingang | (1, 1, 0) | Increases the Throttle Value when input is held. |
| Down | An/Aus | Eingang | (0, 1, 0) | Decreases the Throttle Value when input is held. |
| Throttle | Zahl | Ausgang | (0, 0, 0) | Outputs the stored Throttle Value. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Toggle Button (`button_toggle`)

*A button that toggles between sending an on or off signal when you press [$[action_interact_left]]/[$[action_interact_right]] on it.*
An external on/off signal can also be used to control whether or not the button is pressed, allowing you to chain multiple buttons together to unify their outputs. The button's default state can be configured by selecting it with the select component.

- Größe 1x2x1 Blöcke (voxel [0, 0, 0] .. [0, 1, 0]), Masse 1, Preis 10, Tags: basic
- Werte: buoy_factor=1.000000, buoy_force=100.000000, buoy_radius=1.000000, constraint_range_of_motion=0.000000, door_lower_limit=0.000000, door_upper_limit=0.000000, dynamic_max_rotation=0.000000, dynamic_min_rotation=0.000000, engine_max_force=1000.000000, force_emitter_max_force=1000.000000, force_emitter_max_vector=1.000000, light_fov=0.000000, light_intensity=0.000000, light_range=0.000000, magnet_force=0.000000, max_motor_force=0.000000, rudder_surface_area=0.000000, type=8, wheel_radius=0.250000

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Toggled | An/Aus | Ausgang | (0, 0, 0) | Outputs an on/off signal that can be toggled by interacting with [$[action_interact_left]]/[$[action_interact_right]]. |
| External Input | An/Aus | Eingang | (0, 1, 0) | Allows an external on/off signal to control whether or not the button is pressed. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Toggle Button (2 Sided) (`button_toggle_2side`)

*A button that toggles between sending an on or off signal when you press [$[action_interact_left]]/[$[action_interact_right]] on it.*
An external on/off signal can also be used to control whether or not the button is pressed, allowing you to chain multiple buttons together to unify their outputs. The button's default state can be configured by selecting it with the select component.

- Größe 1x2x1 Blöcke (voxel [0, 0, 0] .. [0, 1, 0]), Masse 1, Preis 10, Tags: basic
- Werte: cable_radius=0.02, door_lower_limit=0, door_upper_limit=0, dynamic_max_rotation=0, light_fov=0, light_intensity=0, light_range=0, magnet_force=0, max_motor_force=0, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, type=8

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Toggled | An/Aus | Ausgang | (0, 0, 0) | Outputs an on/off signal that can be toggled by interacting with [$[action_interact_left]]/[$[action_interact_right]]. |
| External Input | An/Aus | Eingang | (0, 1, 0) | Allows an external on/off signal to control whether or not the button is pressed. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Torque Connector (`connector_torque`)

*A small torque connector that can be used to transfer mechanical energy between vehicles.*
Two torque connectors will attach when they are within close proximity. When connected, mechanical energy will be transferred between the connectors.

- Größe 1x2x1 Blöcke (voxel [0, 0, 0] .. [0, 1, 0]), Masse 2, Preis 20, Tags: magnet
- Werte: cable_radius=0, connector_type=9, logic_gate_type=1, magnet_force=0.1, rudder_surface_area=0, type=17

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Release Connector | An/Aus | Eingang | (0, 0, 0) | Release the connector when receiving an on signal. |
| Connected | An/Aus | Ausgang | (0, 1, 0) | Outputs an on signal if the connector is attached to another connector. |
| RPS | Drehmoment | Ausgang | (0, 0, 0) | Power connection for transfering mechanical energy. |
| Composite Data Send | Composite | Eingang | (0, 0, 0) | Composite data to send to the connected connector. |
| Composite Data Receive | Composite | Ausgang | (0, 1, 0) | Composite data to receive from the connected connector. |
| Video Data Send | Video | Eingang | (0, 0, 0) | Video data to send to the connected connector. |
| Video Data Receive | Video | Ausgang | (0, 1, 0) | Video data to receive from the connected connector. |

## Turret Ring (Large) (`multibody_turret_large_a`)

*A large turret ring that can rotate continuously.*
A turret ring rotates in the same way as a velocity pivot. The gap inside the turret ring creates a door seal, and can be used to extend a sealed volume through the turret ring.

- Größe 9x1x9 Blöcke (voxel [-4, 0, 0] .. [4, 0, 8]), Masse 36, Preis 100
- Werte: button_type=0, cable_length=0, cable_radius=0.02, child_name=multibody_turret_large_b, door_lower_limit=0, door_side_dist=6, door_up_dist=6, door_upper_limit=0, dynamic_max_rotation=0, light_fov=0, light_intensity=0, light_range=0, magnet_force=0, max_motor_force=2000, max_motor_speed=0.5, pump_pressure=0, rudder_surface_area=0, type=7, wheel_radius=0
- Zweiter Körper (Gelenk) bei [0, 1, 0]

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Rotational Speed | Zahl | Eingang | (0, 0, 0) | The speed at which the turret should rotate. |
| Current Rotation | Zahl | Ausgang | (-1, 0, 0) | The turrets measured rotation expressed in fractions of full turns. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Turret Ring (Medium) (`multibody_turret_medium_a`)

*A medium turret ring that can rotate continuously.*
A turret ring rotates in the same way as a velocity pivot. The gap inside the turret ring creates a door seal, and can be used to extend a sealed volume through the turret ring.

- Größe 7x1x7 Blöcke (voxel [-3, 0, 0] .. [3, 0, 6]), Masse 22, Preis 75
- Werte: button_type=0, cable_length=0, cable_radius=0.02, child_name=multibody_turret_medium_b, door_lower_limit=0, door_side_dist=4, door_up_dist=4, door_upper_limit=0, dynamic_max_rotation=0, light_fov=0, light_intensity=0, light_range=0, magnet_force=0, max_motor_force=1000, max_motor_speed=1, pump_pressure=0, rudder_surface_area=0, type=7, wheel_radius=0
- Zweiter Körper (Gelenk) bei [0, 1, 0]

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Rotational Speed | Zahl | Eingang | (0, 0, 0) | The speed at which the turret should rotate. |
| Current Rotation | Zahl | Ausgang | (-1, 0, 0) | The turrets measured rotation expressed in fractions of full turns. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Turret Ring (Small) (`multibody_turret_small_a`)

*A small turret ring that can rotate continuously.*
A turret ring rotates in the same way as a velocity pivot. The gap inside the turret ring creates a door seal, and can be used to extend a sealed volume through the turret ring.

- Größe 5x1x5 Blöcke (voxel [-2, 0, 0] .. [2, 0, 4]), Masse 14, Preis 50
- Werte: button_type=0, cable_length=0, cable_radius=0.02, child_name=multibody_turret_small_b, door_lower_limit=0, door_side_dist=2, door_up_dist=2, door_upper_limit=0, dynamic_max_rotation=0, light_fov=0, light_intensity=0, light_range=0, magnet_force=0, max_motor_force=500, max_motor_speed=2, pump_pressure=0, rudder_surface_area=0, type=7, wheel_radius=0
- Zweiter Körper (Gelenk) bei [0, 1, 0]

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Rotational Speed | Zahl | Eingang | (0, 0, 0) | The speed at which the turret should rotate. |
| Current Rotation | Zahl | Ausgang | (-1, 0, 0) | The turrets measured rotation expressed in fractions of full turns. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Velocity Pivot (`multibody_velocity_pivot_a`)

*A pivot that will continuously rotate at a set input speed.*
Inputting a value of 0 will cause it to stop. The pivot's current rotation can be read from its output. An output of 1 corresponds to one full turn, and -1 to a full turn in the opposite direction.

- Größe 3x1x3 Blöcke (voxel [-1, 0, -1] .. [1, 0, 1]), Masse 9, Preis 25
- Werte: buoy_factor=1.000000, buoy_force=100.000000, buoy_radius=1.000000, button_type=0, child_name=multibody_velocity_pivot_b, constraint_range_of_motion=0.000000, door_lower_limit=0.000000, door_upper_limit=0.000000, dynamic_max_rotation=0.000000, dynamic_min_rotation=0.000000, engine_max_force=1000.000000, force_emitter_max_force=1000.000000, force_emitter_max_vector=1.000000, light_fov=0.000000, light_intensity=0.000000, light_range=0.000000, magnet_force=0.000000, max_motor_force=1000.000000, rudder_surface_area=0.000000, type=7, wheel_radius=0.000000
- Zweiter Körper (Gelenk) bei [0, 1, 0]

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Rotational Speed | Zahl | Eingang | (0, 0, 0) | The speed at which the pivot should rotate. |
| Current Rotation | Zahl | Ausgang | (-1, 0, 0) | The pivot's measured rotation expressed in fractions of full turns. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Velocity Pivot (Fluid) (`multibody_velocity_pivot_01_a_fluid`)

*A pivot that will continuously rotate at a set input speed.*
Inputting a value of 0 will cause it to stop. The pivot's current rotation can be read from its output. An output of 1 corresponds to one full turn, and -1 to a full turn in the opposite direction.

- Größe 3x1x3 Blöcke (voxel [-1, 0, -1] .. [1, 0, 1]), Masse 9, Preis 200
- Werte: child_name=multibody_velocity_pivot_01_b_fluid, constraint_range_of_motion=0.5, max_motor_force=1000, rudder_surface_area=0, type=7
- Zweiter Körper (Gelenk) bei [0, 1, 0]

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Rotational Speed | Zahl | Eingang | (0, 0, 0) | The speed at which the pivot should rotate. |
| Current Rotation | Zahl | Ausgang | (0, 0, -1) | The pivot's measured rotation expressed in fractions of full turns. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |
| Fluid | Fluessigkeit/Gas | Eingang | (0, 0, 1) | Fluid connection for transfering fluids. |

## Velocity Pivot (Power) (`multibody_velocity_pivot_01_a_torque`)

*A pivot that will continuously rotate at a set input speed.*
Inputting a value of 0 will cause it to stop. The pivot's current rotation can be read from its output. An output of 1 corresponds to one full turn, and -1 to a full turn in the opposite direction.

- Größe 3x1x3 Blöcke (voxel [-1, 0, -1] .. [1, 0, 1]), Masse 9, Preis 200
- Werte: button_type=0, cable_radius=0.02, child_name=multibody_velocity_pivot_01_b_torque, constraint_range_of_motion=0.5, door_lower_limit=0, door_upper_limit=0, dynamic_max_rotation=0, light_fov=0, light_intensity=0, light_range=0, magnet_force=0, max_motor_force=1000, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, type=7, wheel_radius=0
- Zweiter Körper (Gelenk) bei [0, 1, 0]

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Rotational Speed | Zahl | Eingang | (0, 0, 0) | The speed at which the pivot should rotate. |
| Current Rotation | Zahl | Ausgang | (0, 0, -1) | The pivot's measured rotation expressed in fractions of full turns. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |
| RPS | Drehmoment | Eingang | (0, 0, 1) | Power connection for transfering mechanical energy. |
