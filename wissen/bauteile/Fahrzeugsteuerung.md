# Fahrzeugsteuerung (Kategorie 1)

Aus den Spieldaten erzeugt von `tools/bauteile_holen.py` - nicht von Hand ändern.

## Compact Pilot Seat (`seat_compact`)

*The compact pilot seat lets you translate keyboard presses into output signals that can control logic components.*
It provides 4 number outputs that produce a standard value ranging from -1 to 1, and 6 on/off outputs. You can get in and out of the compact pilot seat by interacting with it using [$[action_use_seat]].

- Größe 3x5x3 Blöcke (voxel [-1, 0, -1] .. [1, 4, 1]), Masse 7, Preis 100, Tags: basic,seat,control,pilot
- Werte: button_type=0, cable_radius=0, constraint_axis=0, door_lower_limit=0, door_upper_limit=0, dynamic_max_rotation=0, force_emitter_max_vector=0, light_fov=0, light_intensity=0, light_range=0, magnet_force=0, max_motor_force=0, max_motor_speed=5, pump_pressure=0, radar_range=3, rudder_surface_area=0, seat_pose=1, type=1, wheel_radius=0

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Occupied | An/Aus | Ausgang | (0, 0, 0) | Outputs an on signal if this seat is occupied by a character. |
| Trigger [$[action_trigger]] | An/Aus | Ausgang | (0, 2, 1) | Outputs an on signal when [$[action_trigger]] is held, and off when it is not. |
| Look X | Zahl | Ausgang | (-1, 4, 1) | Outputs the character look direction in turns along the X-axis. |
| Look Y | Zahl | Ausgang | (1, 4, 1) | Outputs the character look direction in turns along the Y-axis. |
| Axis 1 [$[action_left]]/[$[action_right]] | Zahl | Ausgang | (-1, 1, 0) | Outputs a standard value between -1 and 1, controlled using [$[action_left]] and [$[action_right]]. [$[action_left]] causes the output value to move towards -1, and [$[action_right]] moves it towards 1. |
| Axis 2 [$[action_up]]/[$[action_down]] | Zahl | Ausgang | (1, 1, 0) | Outputs a standard value between -1 and 1, controlled using [$[action_up]] and [$[action_down]]. [$[action_down]] causes the output value to move towards -1, and [$[action_up]] moves it towards 1. |
| Axis 3 [$[action_pedal_left]]/[$[action_pedal_right]] | Zahl | Ausgang | (-1, 0, 0) | Outputs a standard value between -1 and 1, controlled using [$[action_pedal_left]] and [$[action_pedal_right]]. [$[action_pedal_left]] causes the output value to move towards -1, and [$[action_pedal_right]] moves it towards 1. |
| Axis 4 [$[action_throttle_up]]/[$[action_throttle_down]] | Zahl | Ausgang | (1, 0, 0) | Outputs a standard value between -1 and 1, controlled using [$[action_throttle_up]] and [$[action_throttle_down]]. [$[action_throttle_down]] causes the output value to move towards -1, and [$[action_throttle_up]] moves it towards 1. |
| Hotkey 1 [$[action_hotkey_1]] | An/Aus | Ausgang | (-1, 2, -1) | Outputs an on signal when [$[action_hotkey_1]] is held, and off when it is not. |
| Hotkey 2 [$[action_hotkey_2]] | An/Aus | Ausgang | (-1, 1, -1) | Outputs an on signal when [$[action_hotkey_2]] is held, and off when it is not. |
| Hotkey 3 [$[action_hotkey_3]] | An/Aus | Ausgang | (-1, 0, -1) | Outputs an on signal when [$[action_hotkey_3]] is held, and off when it is not. |
| Hotkey 4 [$[action_hotkey_4]] | An/Aus | Ausgang | (1, 2, -1) | Outputs an on signal when [$[action_hotkey_4]] is held, and off when it is not. |
| Hotkey 5 [$[action_hotkey_5]] | An/Aus | Ausgang | (1, 1, -1) | Outputs an on signal when [$[action_hotkey_5]] is held, and off when it is not. |
| Hotkey 6 [$[action_hotkey_6]] | An/Aus | Ausgang | (1, 0, -1) | Outputs an on signal when [$[action_hotkey_6]] is held, and off when it is not. |
| Seat data | Composite | Ausgang | (0, 0, 1) | Outputs the axis, hotkey and occupied data from the seat. (On/Off 1+ : Hotkeys) (On/Off 31 : Trigger) (On/Off 32 : Occupied) (Value 1 : [$[action_left]]/[$[action_right]]) (Value 2 : [$[action_up]]/[$[action_down]]) (Value 3 : [$[action_pedal_left]]/[$[action_pedal_right]]) (Value 4 : [$[action_throttle_up]]/[$[action_throttle_down]]) (Value 9 : Look X)  (Value 10 : Look Y) |
| Headset Audio | Ton | Ausgang | (-1, 4, 0) |  |
| Headset Audio | Ton | Eingang | (1, 4, 0) |  |
| Headset Video | Video | Eingang | (1, 4, 0) | Displays video UI overlay on a helmet mounted display. |

## Control Fin Large (`control_fin_large`)

*The fin can be attached to the surface of a vehicle to direct its motion.*
It takes a number input between -1 and 1 that represent the two extremes of the fin's rotation.

- Größe 1x3x3 Blöcke (voxel [0, 0, -1] .. [0, 2, 1]), Masse 10, Preis 350, Tags: boat,basic
- Werte: cable_radius=0.02, door_lower_limit=0, door_upper_limit=0, dynamic_max_rotation=0.25, dynamic_min_rotation=-0.25, light_intensity=0, magnet_force=0, max_motor_force=0, max_motor_speed=5, pump_pressure=0, rudder_surface_area=12, type=18

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Rotation | Zahl | Eingang | (0, 0, 1) | Accepts a value between -1 and 1 that represent the two extremes of the fin's rotation. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Control Fin Medium (`control_fin_medium`)

*The fin can be attached to the surface of a vehicle to direct its motion.*
It takes a number input between -1 and 1 that represent the two extremes of the fin's rotation.

- Größe 1x2x3 Blöcke (voxel [0, 0, -1] .. [0, 1, 1]), Masse 5, Preis 150, Tags: boat,basic
- Werte: cable_radius=0.02, door_lower_limit=0, door_upper_limit=0, dynamic_max_rotation=0.25, dynamic_min_rotation=-0.25, light_intensity=0, magnet_force=0, max_motor_force=0, max_motor_speed=5, pump_pressure=0, rudder_surface_area=8, type=18

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Rotation | Zahl | Eingang | (0, 0, 1) | Accepts a value between -1 and 1 that represent the two extremes of the fin's rotation. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Control Fin Small (`control_fin_small`)

*The fin can be attached to the surface of a vehicle to direct its motion.*
It takes a number input between -1 and 1 that represent the two extremes of the fin's rotation.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 2, Preis 50, Tags: boat,basic
- Werte: dynamic_max_rotation=0.25, dynamic_min_rotation=-0.25, rudder_surface_area=2, type=18

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Rotation | Zahl | Eingang | (0, 0, 0) | Accepts a value between -1 and 1 that represent the two extremes of the fin's rotation. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Control Handle (`seat_handle`)

*A compact control handle.*
You can get in and out of the position by interacting with it using [$[action_use_seat]].

- Größe 3x7x3 Blöcke (voxel [-1, -4, -2] .. [1, 2, 0]), Masse 1, Preis 50, Tags: basic,seat,control,pilot
- Werte: button_type=0, cable_length=0, cable_radius=0, constraint_axis=0, door_lower_limit=0, door_upper_limit=0, dynamic_max_rotation=0, light_fov=0, light_intensity=0, light_range=0, magnet_force=0, max_motor_force=0, max_motor_speed=5, pump_pressure=0, radar_range=3, rudder_surface_area=0, seat_pose=6, type=1, wheel_radius=0

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Occupied | An/Aus | Ausgang | (0, 0, -2) | Outputs an on signal if the handle is occupied by a character. |
| Trigger [$[action_trigger]] | An/Aus | Ausgang | (0, 0, 0) | Outputs an on signal when [$[action_trigger]] is held, and off when it is not. |
| Look X | Zahl | Ausgang | (-1, 2, -1) | Outputs the character look direction in turns along the X-axis. |
| Look Y | Zahl | Ausgang | (1, 2, -1) | Outputs the character look direction in turns along the Y-axis. |
| Axis 1 [$[action_left]]/[$[action_right]] | Zahl | Ausgang | (-1, 0, -1) | Outputs a standard value between -1 and 1, controlled using [$[action_left]] and [$[action_right]]. [$[action_left]] causes the output value to move towards -1, and [$[action_right]] moves it towards 1. |
| Axis 2 [$[action_up]]/[$[action_down]] | Zahl | Ausgang | (1, 0, -1) | Outputs a standard value between -1 and 1, controlled using [$[action_up]] and [$[action_down]]. [$[action_down]] causes the output value to move towards -1, and [$[action_up]] moves it towards 1. |
| Axis 3 [$[action_pedal_left]]/[$[action_pedal_right]] | Zahl | Ausgang | (-1, -1, -1) | Outputs a standard value between -1 and 1, controlled using [$[action_pedal_left]] and [$[action_pedal_right]]. [$[action_pedal_left]] causes the output value to move towards -1, and [$[action_pedal_right]] moves it towards 1. |
| Axis 4 [$[action_throttle_up]]/[$[action_throttle_down]] | Zahl | Ausgang | (1, -1, -1) | Outputs a standard value between -1 and 1, controlled using [$[action_throttle_up]] and [$[action_throttle_down]]. [$[action_throttle_down]] causes the output value to move towards -1, and [$[action_throttle_up]] moves it towards 1. |
| Hotkey 1 [$[action_hotkey_1]] | An/Aus | Ausgang | (-1, 1, -2) | Outputs an on signal when [$[action_hotkey_1]] is held, and off when it is not. |
| Hotkey 2 [$[action_hotkey_2]] | An/Aus | Ausgang | (-1, 0, -2) | Outputs an on signal when [$[action_hotkey_2]] is held, and off when it is not. |
| Hotkey 3 [$[action_hotkey_3]] | An/Aus | Ausgang | (-1, -1, -2) | Outputs an on signal when [$[action_hotkey_3]] is held, and off when it is not. |
| Hotkey 4 [$[action_hotkey_4]] | An/Aus | Ausgang | (1, 1, -2) | Outputs an on signal when [$[action_hotkey_4]] is held, and off when it is not. |
| Hotkey 5 [$[action_hotkey_5]] | An/Aus | Ausgang | (1, 0, -2) | Outputs an on signal when [$[action_hotkey_5]] is held, and off when it is not. |
| Hotkey 6 [$[action_hotkey_6]] | An/Aus | Ausgang | (1, -1, -2) | Outputs an on signal when [$[action_hotkey_6]] is held, and off when it is not. |
| Seat data | Composite | Ausgang | (0, 0, 0) | Outputs the axis, hotkey and occupied data from the helm. (On/Off 1+ : Hotkeys) (On/Off 31 : Trigger) (On/Off 32 : Occupied) (Value 1 : [$[action_left]]/[$[action_right]]) (Value 2 : [$[action_up]]/[$[action_down]]) (Value 3 : [$[action_pedal_left]]/[$[action_pedal_right]]) (Value 4 : [$[action_throttle_up]]/[$[action_throttle_down]]) (Value 9 : Look X)  (Value 10 : Look Y) |
| Headset Audio | Ton | Ausgang | (-1, 2, -2) |  |
| Headset Audio | Ton | Eingang | (1, 2, -2) |  |
| Headset Video | Video | Eingang | (1, 2, -2) | Displays video UI overlay on a helmet mounted display. |

## Control Surface (Large) (`control_surface_large`)

*The control surface can be attached to a surface of the vehicle to apply force as air or water is flowing over it.*
It takes a number input between -1 and 1 that represent the two extremes of the fin's rotation.

- Größe 1x5x17 Blöcke (voxel [0, 0, -8] .. [0, 4, 8]), Masse 25, Preis 500, Tags: airplane,aeroplane,basic
- Werte: cable_radius=0, dynamic_max_rotation=0.785398, dynamic_min_rotation=-0.785398, rudder_surface_area=70, type=18

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Rotation | Zahl | Eingang | (0, 0, 1) | Accepts a value between -1 and 1 that represent the two extremes of the rudder's rotation. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Control Surface (Medium) (`control_surface_medium`)

*The control surface can be attached to a surface of the vehicle to apply force as air or water is flowing over it.*
It takes a number input between -1 and 1 that represent the two extremes of the fin's rotation.

- Größe 1x4x11 Blöcke (voxel [0, 0, -5] .. [0, 3, 5]), Masse 15, Preis 250, Tags: airplane,aeroplane,basic
- Werte: cable_radius=0, dynamic_max_rotation=0.785398, dynamic_min_rotation=-0.785398, rudder_surface_area=28, type=18

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Rotation | Zahl | Eingang | (0, 0, 1) | Accepts a value between -1 and 1 that represent the two extremes of the rudder's rotation. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Control Surface (Small) (`control_surface_small`)

*The control surface can be attached to a surface of the vehicle to apply force as air or water is flowing over it.*
It takes a number input between -1 and 1 that represent the two extremes of the fin's rotation.

- Größe 1x3x7 Blöcke (voxel [0, 0, -3] .. [0, 2, 3]), Masse 10, Preis 150, Tags: airplane,aeroplane,basic
- Werte: cable_radius=0, dynamic_max_rotation=0.785398, dynamic_min_rotation=-0.785398, rudder_surface_area=10, type=18

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Rotation | Zahl | Eingang | (0, 0, 1) | Accepts a value between -1 and 1 that represent the two extremes of the rudder's rotation. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Data Logger (Bool) (`data_logger_bool`)

*A bool data logging block for unit tests.*
Link to the bool output node of another component to record data for unit tests.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 1
- Werte: type=61

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Bool In | An/Aus | Eingang | (0, 0, 0) |  |

## Data Logger (Number) (`data_logger_number`)

*A number data logging block for unit tests.*
Link to the number output node of another component to record data for unit tests.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 1
- Werte: type=61

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Number In | Zahl | Eingang | (0, 0, 0) |  |

## Driver seat (`seat_racing`)

*The driver seat lets you translate keyboard presses into output signals that can control logic components.*
It provides 4 number outputs that produce a standard value ranging from -1 to 1, and 6 on/off outputs. You can get in and out of the driver seat by interacting with it using [$[action_use_seat]].

- Größe 3x5x4 Blöcke (voxel [-1, 0, -1] .. [1, 4, 2]), Masse 10, Preis 100, Tags: basic,seat,control,pilot
- Werte: button_type=0, cable_radius=0, constraint_axis=0, door_lower_limit=0, door_upper_limit=0, dynamic_max_rotation=0, force_emitter_max_vector=0, light_fov=0, light_intensity=0, light_range=0, magnet_force=0, max_motor_force=0, max_motor_speed=5, pump_pressure=0, radar_range=3, rudder_surface_area=0, seat_pose=5, type=1, wheel_radius=0

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Occupied | An/Aus | Ausgang | (0, 0, 0) | Outputs an on signal if this seat is occupied by a character. |
| Trigger [$[action_trigger]] | An/Aus | Ausgang | (0, 2, 1) | Outputs an on signal when [$[action_trigger]] is held, and off when it is not. |
| Look X | Zahl | Ausgang | (-1, 4, 1) | Outputs the character look direction in turns along the X-axis. |
| Look Y | Zahl | Ausgang | (1, 4, 1) | Outputs the character look direction in turns along the Y-axis. |
| Axis 1 [$[action_left]]/[$[action_right]] | Zahl | Ausgang | (-1, 1, 0) | Outputs a standard value between -1 and 1, controlled using [$[action_left]] and [$[action_right]]. [$[action_left]] causes the output value to move towards -1, and [$[action_right]] moves it towards 1. |
| Axis 2 [$[action_up]]/[$[action_down]] | Zahl | Ausgang | (1, 1, 0) | Outputs a standard value between -1 and 1, controlled using [$[action_up]] and [$[action_down]]. [$[action_down]] causes the output value to move towards -1, and [$[action_up]] moves it towards 1. |
| Axis 3 [$[action_pedal_left]]/[$[action_pedal_right]] | Zahl | Ausgang | (-1, 0, 0) | Outputs a standard value between -1 and 1, controlled using [$[action_pedal_left]] and [$[action_pedal_right]]. [$[action_pedal_left]] causes the output value to move towards -1, and [$[action_pedal_right]] moves it towards 1. |
| Axis 4 [$[action_throttle_up]]/[$[action_throttle_down]] | Zahl | Ausgang | (1, 0, 0) | Outputs a standard value between -1 and 1, controlled using [$[action_throttle_up]] and [$[action_throttle_down]]. [$[action_throttle_down]] causes the output value to move towards -1, and [$[action_throttle_up]] moves it towards 1. |
| Hotkey 1 [$[action_hotkey_1]] | An/Aus | Ausgang | (-1, 2, -1) | Outputs an on signal when [$[action_hotkey_1]] is held, and off when it is not. |
| Hotkey 2 [$[action_hotkey_2]] | An/Aus | Ausgang | (-1, 1, -1) | Outputs an on signal when [$[action_hotkey_2]] is held, and off when it is not. |
| Hotkey 3 [$[action_hotkey_3]] | An/Aus | Ausgang | (-1, 0, -1) | Outputs an on signal when [$[action_hotkey_3]] is held, and off when it is not. |
| Hotkey 4 [$[action_hotkey_4]] | An/Aus | Ausgang | (1, 2, -1) | Outputs an on signal when [$[action_hotkey_4]] is held, and off when it is not. |
| Hotkey 5 [$[action_hotkey_5]] | An/Aus | Ausgang | (1, 1, -1) | Outputs an on signal when [$[action_hotkey_5]] is held, and off when it is not. |
| Hotkey 6 [$[action_hotkey_6]] | An/Aus | Ausgang | (1, 0, -1) | Outputs an on signal when [$[action_hotkey_6]] is held, and off when it is not. |
| Seat data | Composite | Ausgang | (0, 0, 2) | Outputs the axis, hotkey and occupied data from the seat. (On/Off 1+ : Hotkeys) (On/Off 31 : Trigger) (On/Off 32 : Occupied) (Value 1 : [$[action_left]]/[$[action_right]]) (Value 2 : [$[action_up]]/[$[action_down]]) (Value 3 : [$[action_pedal_left]]/[$[action_pedal_right]]) (Value 4 : [$[action_throttle_up]]/[$[action_throttle_down]]) (Value 9 : Look X)  (Value 10 : Look Y) |
| Headset Audio | Ton | Ausgang | (-1, 4, 0) |  |
| Headset Audio | Ton | Eingang | (1, 4, 0) |  |
| Headset Video | Video | Eingang | (1, 4, 0) | Displays video UI overlay on a helmet mounted display. |

## Fin Rudder (`rudder_surface`)

*The fin rudder can be attached to the keel of a boat to control its yaw, allowing you to steer left and right.*
It takes a number input between -1 and 1 that represent the two extremes of the fin's rotation.

- Größe 1x2x3 Blöcke (voxel [0, 0, -1] .. [0, 1, 1]), Masse 5, Preis 100, Tags: boat,basic
- Werte: dynamic_max_rotation=0.785398, dynamic_min_rotation=-0.785398, rudder_surface_area=3.2, type=18

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Rotation | Zahl | Eingang | (0, 0, 1) | Accepts a value between -1 and 1 that represent the two extremes of the rudder's rotation. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Friction Pad (`friction_block`)

*Friction pad that grips to surfaces.*
High friction pad that grips any surface it touches.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 15
- Werte: cable_radius=0.02, light_intensity=0, magnet_force=0, max_motor_speed=5, phys_collision_dampen=2000, pump_pressure=0, rudder_surface_area=0, seat_health_per_sec=1, type=55, wheel_radius=0.14

## Gyro (`gyro`)

*The gyroscope takes 4 standard value signals representing the desired yaw, pitch, roll and vertical motion of a helicopter.*
It outputs stabilised values that can be sent to rotors and engines to make them much easier to control. An on/off input allows you to activate and deactivate the internal auto-hover circuit. When auto-hover is enabled, the gyroscope will attempt to keep your helicopter steady.

- Größe 5x1x3 Blöcke (voxel [-2, 0, -1] .. [2, 0, 1]), Masse 10, Preis 500, Tags: helicopter
- Werte: buoy_factor=1.000000, buoy_force=100.000000, buoy_radius=1.000000, constraint_range_of_motion=0.000000, door_lower_limit=-1.000000, door_upper_limit=1.000000, dynamic_min_rotation=0.000000, engine_max_force=1000.000000, force_emitter_max_force=1000.000000, force_emitter_max_vector=1.000000, light_fov=1.000000, light_intensity=0.000000, light_range=1.000000, magnet_force=0.000000, max_motor_force=0.000000, rudder_surface_area=0.000000, type=14, wheel_radius=0.250000

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Roll | Zahl | Eingang | (-2, 0, -1) | Accepts a standard value between -1 and 1 representing the desired roll speed. |
| Stabilised Roll | Zahl | Ausgang | (-1, 0, -1) | Outputs a standard value between -1 and 1 representing a stabilised roll speed. |
| Pitch | Zahl | Eingang | (1, 0, -1) | Accepts a standard value between -1 and 1 representing the desired pitch speed. |
| Stabilised Pitch | Zahl | Ausgang | (2, 0, -1) | Outputs a standard value between -1 and 1 representing a stabilised pitch speed. |
| Yaw | Zahl | Eingang | (-2, 0, 1) | Accepts a standard value between -1 and 1 representing the desired yaw speed. |
| Stabilised Yaw | Zahl | Ausgang | (-1, 0, 1) | Outputs a standard value between -1 and 1 representing a stabilised yaw speed. |
| Up/Down | Zahl | Eingang | (1, 0, 1) | Accepts a standard value between -1 and 1 representing the desired vertical speed. |
| Stabilised Up/Down | Zahl | Ausgang | (2, 0, 1) | Outputs a standard value between 0 and 1 representing a stabilised upward thrust. |
| Auto-hover | An/Aus | Eingang | (0, 0, 0) | Enables the gyroscope's auto-hover circuit when receiving an on signal. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Helm (`seat_helm`)

*A steering helm with steering wheel.*
You can get in and out of the position by interacting with it using [$[action_use_seat]]. You can place a rescued survivor in any position by using [$[action_use_seat]] while carrying them.

- Größe 3x7x5 Blöcke (voxel [-1, -3, -4] .. [1, 3, 0]), Masse 15, Preis 150, Tags: basic,seat,control,pilot
- Werte: button_type=0, cable_length=0, cable_radius=0, constraint_axis=0, door_lower_limit=0, door_upper_limit=0, dynamic_max_rotation=0, light_fov=0, light_intensity=0, light_range=0, magnet_force=0, max_motor_force=0, max_motor_speed=5, pump_pressure=0, radar_range=3, rudder_surface_area=0, seat_pose=2, type=1, wheel_radius=0

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Occupied | An/Aus | Ausgang | (0, 0, -2) | Outputs an on signal if the helm is occupied by a character. |
| Trigger [$[action_trigger]] | An/Aus | Ausgang | (0, 0, -1) | Outputs an on signal when [$[action_trigger]] is held, and off when it is not. |
| Look X | Zahl | Ausgang | (-1, -2, 0) | Outputs the character look direction in turns along the X-axis. |
| Look Y | Zahl | Ausgang | (1, -2, 0) | Outputs the character look direction in turns along the Y-axis. |
| Axis 1 [$[action_left]]/[$[action_right]] | Zahl | Ausgang | (-1, 0, 0) | Outputs a standard value between -1 and 1, controlled using [$[action_left]] and [$[action_right]]. [$[action_left]] causes the output value to move towards -1, and [$[action_right]] moves it towards 1. |
| Axis 2 [$[action_up]]/[$[action_down]] | Zahl | Ausgang | (1, 0, 0) | Outputs a standard value between -1 and 1, controlled using [$[action_up]] and [$[action_down]]. [$[action_down]] causes the output value to move towards -1, and [$[action_up]] moves it towards 1. |
| Axis 3 [$[action_pedal_left]]/[$[action_pedal_right]] | Zahl | Ausgang | (-1, -1, 0) | Outputs a standard value between -1 and 1, controlled using [$[action_pedal_left]] and [$[action_pedal_right]]. [$[action_pedal_left]] causes the output value to move towards -1, and [$[action_pedal_right]] moves it towards 1. |
| Axis 4 [$[action_throttle_up]]/[$[action_throttle_down]] | Zahl | Ausgang | (1, -1, 0) | Outputs a standard value between -1 and 1, controlled using [$[action_throttle_up]] and [$[action_throttle_down]]. [$[action_throttle_down]] causes the output value to move towards -1, and [$[action_throttle_up]] moves it towards 1. |
| Hotkey 1 [$[action_hotkey_1]] | An/Aus | Ausgang | (-1, 2, -3) | Outputs an on signal when [$[action_hotkey_1]] is held, and off when it is not. |
| Hotkey 2 [$[action_hotkey_2]] | An/Aus | Ausgang | (-1, 1, -3) | Outputs an on signal when [$[action_hotkey_2]] is held, and off when it is not. |
| Hotkey 3 [$[action_hotkey_3]] | An/Aus | Ausgang | (-1, 0, -3) | Outputs an on signal when [$[action_hotkey_3]] is held, and off when it is not. |
| Hotkey 4 [$[action_hotkey_4]] | An/Aus | Ausgang | (1, 2, -3) | Outputs an on signal when [$[action_hotkey_4]] is held, and off when it is not. |
| Hotkey 5 [$[action_hotkey_5]] | An/Aus | Ausgang | (1, 1, -3) | Outputs an on signal when [$[action_hotkey_5]] is held, and off when it is not. |
| Hotkey 6 [$[action_hotkey_6]] | An/Aus | Ausgang | (1, 0, -3) | Outputs an on signal when [$[action_hotkey_6]] is held, and off when it is not. |
| Seat data | Composite | Ausgang | (0, 0, 0) | Outputs the axis, hotkey and occupied data from the helm. (On/Off 1+ : Hotkeys) (On/Off 31 : Trigger) (On/Off 32 : Occupied) (Value 1 : [$[action_left]]/[$[action_right]]) (Value 2 : [$[action_up]]/[$[action_down]]) (Value 3 : [$[action_pedal_left]]/[$[action_pedal_right]]) (Value 4 : [$[action_throttle_up]]/[$[action_throttle_down]]) (Value 9 : Look X)  (Value 10 : Look Y) |
| Headset Audio | Ton | Ausgang | (-1, -3, 0) |  |
| Headset Audio | Ton | Eingang | (1, -3, 0) |  |
| Headset Video | Video | Eingang | (1, -3, 0) | Displays video UI overlay on a helmet mounted display. |

## Keel (Large) (`keel_large`)

*A large boat keel used for sailing.*
The keel resists rolling forces while submerged, helping to keep a boat upright and stable. The keel also resists lateral sliding forces, causing the majority of a boats movement to be in the direction of the keel axis. When combined with the force provided by a sail, this allows a sailboat to move forward in a crosswind, or even upwind.

- Größe 3x9x25 Blöcke (voxel [-1, -4, -12] .. [1, 4, 12]), Masse 2000, Preis 2000, Tags: boat,basic
- Werte: dynamic_max_rotation=0.785398, dynamic_min_rotation=-0.785398, rudder_surface_area=13, rudder_type=2, type=18

## Keel (Medium) (`keel_medium`)

*A medium boat keel used for sailing.*
The keel resists rolling forces while submerged, helping to keep a boat upright and stable. The keel also resists lateral sliding forces, causing the majority of a boats movement to be in the direction of the keel axis. When combined with the force provided by a sail, this allows a sailboat to move forward in a crosswind, or even upwind.

- Größe 3x7x15 Blöcke (voxel [-1, -3, -7] .. [1, 3, 7]), Masse 1000, Preis 1000, Tags: boat,basic
- Werte: dynamic_max_rotation=0.785398, dynamic_min_rotation=-0.785398, rudder_surface_area=13, rudder_type=2, type=18

## Keel (Small) (`keel_small`)

*A small boat keel used for sailing.*
The keel resists rolling forces while submerged, helping to keep a boat upright and stable. The keel also resists lateral sliding forces, causing the majority of a boats movement to be in the direction of the keel axis. When combined with the force provided by a sail, this allows a sailboat to move forward in a crosswind, or even upwind.

- Größe 1x5x9 Blöcke (voxel [0, -2, -4] .. [0, 2, 4]), Masse 500, Preis 300, Tags: boat,basic
- Werte: dynamic_max_rotation=0.785398, dynamic_min_rotation=-0.785398, rudder_surface_area=13, rudder_type=2, type=18

## Keep Active Block (`no_sleep`)

*A keep alive marking block.*
When on a vehicle, the vehicle will not despawn when out of range.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 100, Tags: no_sleep
- Werte: metadata_component_type=0, type=46

## Large Landing Wheel (`wheel_coaster_large`)

*Large landing wheel that requires no engine power and spins freely.*
You cannot control the forward and backward rotation of this wheel, but it can be locked into place by sending an on signal to the brake input.

- Größe 3x4x3 Blöcke (voxel [-1, 0, -1] .. [1, 3, 1]), Masse 8, Preis 50, Tags: basic
- Werte: phys_collision_dampen=2000, rudder_surface_area=0, type=4, wheel_radius=0.58

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Brake | An/Aus | Eingang | (0, 0, 0) | Locks the wheel into place when receiving an on signal. |
| Variable Brake | Zahl | Eingang | (0, 1, -1) | A value between 0 and 1 for soft braking |

## Map Icon Block (`map_icon`)

*A vehicle tracking block.*
When on a vehicle, the vehicle will show on the map and other vehicles in the group will be hidden. The custom name set here will be the name set on the map.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 100
- Werte: type=46

## Medium Wheel (`wheel_medium`)

*Medium wheel that can be controlled using an engine.*
The wheel will rotate forwards and backwards depending on power received from a connected engine. It can be rotated left and right by sending a number signal to the steering input. It can also be locked into place by sending an on signal to the brake input.

- Größe 7x5x7 Blöcke (voxel [-3, 0, -3] .. [3, 4, 3]), Masse 10, Preis 100, Tags: steerable,steering,basic
- Werte: phys_collision_dampen=2000, rudder_surface_area=0, type=4, wheel_radius=0.98

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Brake | An/Aus | Eingang | (0, 0, 0) | Locks the wheel into place when receiving an on signal. |
| RPS | Drehmoment | Eingang | (0, 0, 0) | Receives power generated by an engine to control forward and backward rotation. |
| Variable Brake | Zahl | Eingang | (0, 1, -1) | A value between 0 and 1 for soft braking |
| Steering | Zahl | Eingang | (0, 1, 1) | Accepts a value between -1 and 1 that represents the extremes of the wheels steering rotation |

## Pilot Seat (`seat`)

*The pilot seat lets you translate keyboard presses into output signals that can control logic components.*
It provides 4 number outputs that produce a standard value ranging from -1 to 1, and 6 on/off outputs. You can get in and out of the pilot seat by interacting with it using [$[action_use_seat]].

- Größe 3x6x4 Blöcke (voxel [-1, -1, -1] .. [1, 4, 2]), Masse 24, Preis 100, Tags: basic,seat,control,pilot
- Werte: button_type=0, cable_radius=0, constraint_axis=0, door_lower_limit=0, door_upper_limit=0, dynamic_max_rotation=0, force_emitter_max_vector=0, light_fov=0, light_intensity=0, light_range=0, magnet_force=0, max_motor_force=0, max_motor_speed=5, pump_pressure=0, radar_range=3, rudder_surface_area=0, seat_pose=1, type=1, wheel_radius=0

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Occupied | An/Aus | Ausgang | (0, 0, 0) | Outputs an on signal if this seat is occupied by a character. |
| Trigger [$[action_trigger]] | An/Aus | Ausgang | (0, 2, 1) | Outputs an on signal when [$[action_trigger]] is held, and off when it is not. |
| Look X | Zahl | Ausgang | (-1, 4, 1) | Outputs the character look direction in turns along the X-axis. |
| Look Y | Zahl | Ausgang | (1, 4, 1) | Outputs the character look direction in turns along the Y-axis. |
| Axis 1 [$[action_left]]/[$[action_right]] | Zahl | Ausgang | (-1, 1, 2) | Outputs a standard value between -1 and 1, controlled using [$[action_left]] and [$[action_right]]. [$[action_left]] causes the output value to move towards -1, and [$[action_right]] moves it towards 1. |
| Axis 2 [$[action_up]]/[$[action_down]] | Zahl | Ausgang | (1, 1, 2) | Outputs a standard value between -1 and 1, controlled using [$[action_up]] and [$[action_down]]. [$[action_down]] causes the output value to move towards -1, and [$[action_up]] moves it towards 1. |
| Axis 3 [$[action_pedal_left]]/[$[action_pedal_right]] | Zahl | Ausgang | (-1, -1, 2) | Outputs a standard value between -1 and 1, controlled using [$[action_pedal_left]] and [$[action_pedal_right]]. [$[action_pedal_left]] causes the output value to move towards -1, and [$[action_pedal_right]] moves it towards 1. |
| Axis 4 [$[action_throttle_up]]/[$[action_throttle_down]] | Zahl | Ausgang | (1, -1, 2) | Outputs a standard value between -1 and 1, controlled using [$[action_throttle_up]] and [$[action_throttle_down]]. [$[action_throttle_down]] causes the output value to move towards -1, and [$[action_throttle_up]] moves it towards 1. |
| Hotkey 1 [$[action_hotkey_1]] | An/Aus | Ausgang | (-1, 2, -1) | Outputs an on signal when [$[action_hotkey_1]] is held, and off when it is not. |
| Hotkey 2 [$[action_hotkey_2]] | An/Aus | Ausgang | (-1, 1, -1) | Outputs an on signal when [$[action_hotkey_2]] is held, and off when it is not. |
| Hotkey 3 [$[action_hotkey_3]] | An/Aus | Ausgang | (-1, 0, -1) | Outputs an on signal when [$[action_hotkey_3]] is held, and off when it is not. |
| Hotkey 4 [$[action_hotkey_4]] | An/Aus | Ausgang | (1, 2, -1) | Outputs an on signal when [$[action_hotkey_4]] is held, and off when it is not. |
| Hotkey 5 [$[action_hotkey_5]] | An/Aus | Ausgang | (1, 1, -1) | Outputs an on signal when [$[action_hotkey_5]] is held, and off when it is not. |
| Hotkey 6 [$[action_hotkey_6]] | An/Aus | Ausgang | (1, 0, -1) | Outputs an on signal when [$[action_hotkey_6]] is held, and off when it is not. |
| Seat data | Composite | Ausgang | (0, 0, 1) | Outputs the axis, hotkey and occupied data from the seat. (On/Off 1+ : Hotkeys) (On/Off 31 : Trigger) (On/Off 32 : Occupied) (Value 1 : [$[action_left]]/[$[action_right]]) (Value 2 : [$[action_up]]/[$[action_down]]) (Value 3 : [$[action_pedal_left]]/[$[action_pedal_right]]) (Value 4 : [$[action_throttle_up]]/[$[action_throttle_down]]) (Value 9 : Look X)  (Value 10 : Look Y) |
| Headset Audio | Ton | Ausgang | (-1, 4, 0) |  |
| Headset Audio | Ton | Eingang | (1, 4, 0) |  |
| Headset Video | Video | Eingang | (1, 4, 0) | Displays video UI overlay on a helmet mounted display. |

## Pilot Seat (HOTAS) (`seat_hotas`)

*The pilot seat lets you translate controller presses into output signals that can control logic components.*
It provides 10 number outputs that produce a standard value ranging from -1 to 1, and 48 on/off outputs. You can get in and out of the pilot seat by interacting with it using [$[action_use_seat]]. Designed for use with HOTAS controllers.

- Größe 3x6x5 Blöcke (voxel [-1, -1, -2] .. [1, 4, 2]), Masse 50, Preis 250, Tags: basic,seat,control,pilot
- Werte: button_type=0, cable_length=0, cable_radius=0, constraint_axis=0, door_lower_limit=0, door_upper_limit=0, dynamic_max_rotation=0, force_emitter_max_vector=0, light_fov=0, light_intensity=0, light_range=0, magnet_force=0, max_motor_force=0, max_motor_speed=5, pump_pressure=0, radar_range=3, rudder_surface_area=0, seat_pose=1, type=1, wheel_radius=0

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Occupied | An/Aus | Ausgang | (0, 0, 1) | Outputs an on signal if this seat is occupied by a character. |
| Trigger [$[action_trigger]] | An/Aus | Ausgang | (0, 2, 1) | Outputs an on signal when [$[action_trigger]] is held, and off when it is not. |
| Look X | Zahl | Ausgang | (-1, 4, 1) | Outputs the character look direction in turns along the X-axis. |
| Look Y | Zahl | Ausgang | (1, 4, 1) | Outputs the character look direction in turns along the Y-axis. |
| Axis 1 [$[action_left]]/[$[action_right]] | Zahl | Ausgang | (-1, 1, 2) | Outputs a standard value between -1 and 1, controlled using [$[action_left]] and [$[action_right]]. [$[action_left]] causes the output value to move towards -1, and [$[action_right]] moves it towards 1. |
| Axis 2 [$[action_up]]/[$[action_down]] | Zahl | Ausgang | (0, 1, 2) | Outputs a standard value between -1 and 1, controlled using [$[action_up]] and [$[action_down]]. [$[action_down]] causes the output value to move towards -1, and [$[action_up]] moves it towards 1. |
| Axis 3 [$[action_pedal_left]]/[$[action_pedal_right]] | Zahl | Ausgang | (1, 1, 2) | Outputs a standard value between -1 and 1, controlled using [$[action_pedal_left]] and [$[action_pedal_right]]. [$[action_pedal_left]] causes the output value to move towards -1, and [$[action_pedal_right]] moves it towards 1. |
| Axis 4 [$[action_throttle_up]]/[$[action_throttle_down]] | Zahl | Ausgang | (-1, 0, 2) | Outputs a standard value between -1 and 1, controlled using [$[action_throttle_up]] and [$[action_throttle_down]]. [$[action_throttle_down]] causes the output value to move towards -1, and [$[action_throttle_up]] moves it towards 1. |
| Axis 5 | Zahl | Ausgang | (0, 0, 2) | Outputs a standard value between -1 and 1, controlled using the controller axis. |
| Axis 6 | Zahl | Ausgang | (1, 0, 2) | Outputs a standard value between -1 and 1, controlled using the controller axis. |
| Axis 7 | Zahl | Ausgang | (-1, -1, 2) | Outputs a standard value between -1 and 1, controlled using the controller axis. |
| Axis 8 | Zahl | Ausgang | (1, -1, 2) | Outputs a standard value between -1 and 1, controlled using the controller axis. |
| Hotkey 1 [$[action_hotkey_1]] | An/Aus | Ausgang | (-1, 4, 0) | Outputs an on signal when [$[action_hotkey_1]] is held, and off when it is not. |
| Hotkey 2 [$[action_hotkey_2]] | An/Aus | Ausgang | (0, 4, 0) | Outputs an on signal when [$[action_hotkey_2]] is held, and off when it is not. |
| Hotkey 3 [$[action_hotkey_3]] | An/Aus | Ausgang | (1, 4, 0) | Outputs an on signal when [$[action_hotkey_3]] is held, and off when it is not. |
| Hotkey 4 [$[action_hotkey_4]] | An/Aus | Ausgang | (-1, 3, 0) | Outputs an on signal when [$[action_hotkey_4]] is held, and off when it is not. |
| Hotkey 5 [$[action_hotkey_5]] | An/Aus | Ausgang | (0, 3, 0) | Outputs an on signal when [$[action_hotkey_5]] is held, and off when it is not. |
| Hotkey 6 [$[action_hotkey_6]] | An/Aus | Ausgang | (1, 3, 0) | Outputs an on signal when [$[action_hotkey_6]] is held, and off when it is not. |
| Hotkey 7 | An/Aus | Ausgang | (-1, 2, 0) | Outputs an on signal when the controller button is held, and off when it is not. |
| Hotkey 8 | An/Aus | Ausgang | (0, 2, 0) | Outputs an on signal when the controller button is held, and off when it is not. |
| Hotkey 9 | An/Aus | Ausgang | (1, 2, 0) | Outputs an on signal when the controller button is held, and off when it is not. |
| Hotkey 10 | An/Aus | Ausgang | (-1, 1, 0) | Outputs an on signal when the controller button is held, and off when it is not. |
| Hotkey 11 | An/Aus | Ausgang | (0, 1, 0) | Outputs an on signal when the controller button is held, and off when it is not. |
| Hotkey 12 | An/Aus | Ausgang | (1, 1, 0) | Outputs an on signal when the controller button is held, and off when it is not. |
| Hotkey 13 | An/Aus | Ausgang | (-1, 0, 0) | Outputs an on signal when the controller button is held, and off when it is not. |
| Hotkey 14 | An/Aus | Ausgang | (0, 0, 0) | Outputs an on signal when the controller button is held, and off when it is not. |
| Hotkey 15 | An/Aus | Ausgang | (1, 0, 0) | Outputs an on signal when the controller button is held, and off when it is not. |
| Hotkey 16 | An/Aus | Ausgang | (-1, -1, 0) | Outputs an on signal when the controller button is held, and off when it is not. |
| Hotkey 17 | An/Aus | Ausgang | (0, -1, 0) | Outputs an on signal when the controller button is held, and off when it is not. |
| Hotkey 18 | An/Aus | Ausgang | (1, -1, 0) | Outputs an on signal when the controller button is held, and off when it is not. |
| Hotkey 19 | An/Aus | Ausgang | (-1, 4, -1) | Outputs an on signal when the controller button is held, and off when it is not. |
| Hotkey 20 | An/Aus | Ausgang | (0, 4, -1) | Outputs an on signal when the controller button is held, and off when it is not. |
| Hotkey 21 | An/Aus | Ausgang | (1, 4, -1) | Outputs an on signal when the controller button is held, and off when it is not. |
| Hotkey 22 | An/Aus | Ausgang | (-1, 3, -1) | Outputs an on signal when the controller button is held, and off when it is not. |
| Hotkey 23 | An/Aus | Ausgang | (0, 3, -1) | Outputs an on signal when the controller button is held, and off when it is not. |
| Hotkey 24 | An/Aus | Ausgang | (1, 3, -1) | Outputs an on signal when the controller button is held, and off when it is not. |
| Hotkey 25 | An/Aus | Ausgang | (-1, 2, -1) | Outputs an on signal when the controller button is held, and off when it is not. |
| Hotkey 26 | An/Aus | Ausgang | (0, 2, -1) | Outputs an on signal when the controller button is held, and off when it is not. |
| Hotkey 27 | An/Aus | Ausgang | (1, 2, -1) | Outputs an on signal when the controller button is held, and off when it is not. |
| Hotkey 28 | An/Aus | Ausgang | (-1, 1, -1) | Outputs an on signal when the controller button is held, and off when it is not. |
| Hotkey 29 | An/Aus | Ausgang | (0, 1, -1) | Outputs an on signal when the controller button is held, and off when it is not. |
| Hotkey 30 | An/Aus | Ausgang | (1, 1, -1) | Outputs an on signal when the controller button is held, and off when it is not. |
| Hotkey 31 | An/Aus | Ausgang | (-1, 0, -1) | Outputs an on signal when the controller button is held, and off when it is not. |
| Hotkey 32 | An/Aus | Ausgang | (0, 0, -1) | Outputs an on signal when the controller button is held, and off when it is not. |
| Hotkey 33 | An/Aus | Ausgang | (1, 0, -1) | Outputs an on signal when the controller button is held, and off when it is not. |
| Hotkey 34 | An/Aus | Ausgang | (-1, -1, -1) | Outputs an on signal when the controller button is held, and off when it is not. |
| Hotkey 35 | An/Aus | Ausgang | (0, -1, -1) | Outputs an on signal when the controller button is held, and off when it is not. |
| Hotkey 36 | An/Aus | Ausgang | (1, -1, -1) | Outputs an on signal when the controller button is held, and off when it is not. |
| Hotkey 37 | An/Aus | Ausgang | (-1, 4, -2) | Outputs an on signal when the controller button is held, and off when it is not. |
| Hotkey 38 | An/Aus | Ausgang | (0, 4, -2) | Outputs an on signal when the controller button is held, and off when it is not. |
| Hotkey 39 | An/Aus | Ausgang | (1, 4, -2) | Outputs an on signal when the controller button is held, and off when it is not. |
| Hotkey 40 | An/Aus | Ausgang | (-1, 3, -2) | Outputs an on signal when the controller button is held, and off when it is not. |
| Hotkey 41 | An/Aus | Ausgang | (0, 3, -2) | Outputs an on signal when the controller button is held, and off when it is not. |
| Hotkey 42 | An/Aus | Ausgang | (1, 3, -2) | Outputs an on signal when the controller button is held, and off when it is not. |
| Hotkey 43 | An/Aus | Ausgang | (-1, 2, -2) | Outputs an on signal when the controller button is held, and off when it is not. |
| Hotkey 44 | An/Aus | Ausgang | (0, 2, -2) | Outputs an on signal when the controller button is held, and off when it is not. |
| Hotkey 45 | An/Aus | Ausgang | (1, 2, -2) | Outputs an on signal when the controller button is held, and off when it is not. |
| Hotkey 46 | An/Aus | Ausgang | (-1, 1, -2) | Outputs an on signal when the controller button is held, and off when it is not. |
| Hotkey 47 | An/Aus | Ausgang | (0, 1, -2) | Outputs an on signal when the controller button is held, and off when it is not. |
| Hotkey 48 | An/Aus | Ausgang | (1, 1, -2) | Outputs an on signal when the controller button is held, and off when it is not. |
| Seat data | Composite | Ausgang | (0, 0, 1) | Outputs the axis, hotkey and occupied data from the seat. (On/Off 1+ : Hotkeys) (On/Off 31 : Trigger) (On/Off 32 : Occupied) (Value 1 : [$[action_left]]/[$[action_right]]) (Value 2 : [$[action_up]]/[$[action_down]]) (Value 3 : [$[action_pedal_left]]/[$[action_pedal_right]]) (Value 4 : [$[action_throttle_up]]/[$[action_throttle_down]]) (Values 5/6/7/8 : Controller Axes) (Value 9 : Look X)  (Value 10 : Look Y) |
| Headset Audio | Ton | Ausgang | (-1, 4, 0) |  |
| Headset Audio | Ton | Eingang | (1, 4, 0) |  |
| Headset Video | Video | Eingang | (1, 4, 0) | Displays video UI overlay on a helmet mounted display. |

## Radio RX Huge (`rx_huge`)

*A radio data transmitter and receiver.*
Sends and receives data on the specified frequencies.

- Größe 1x9x1 Blöcke (voxel [0, 0, 0] .. [0, 8, 0]), Masse 20, Preis 5000
- Werte: cable_length=0, rx_length=1.91, rx_range=20000, type=45

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Data Send | Composite | Eingang | (0, 0, 0) |  |
| Data Recv | Composite | Ausgang | (0, 1, 0) |  |
| Electric | Strom | Eingang | (0, 0, 0) |  |
| Frequency Send | Zahl | Eingang | (0, 0, 0) |  |
| Frequency Recv | Zahl | Eingang | (0, 1, 0) |  |
| Signal Strength | Zahl | Ausgang | (0, 2, 0) |  |

## Radio RX Huge (`rx_huge_v2`)

*A radio data transmitter and receiver.*
Sends and receives data on the specified frequency. Transmit Mode defaults to receive. (Max effective range at ground level : 20km)

- Größe 1x9x1 Blöcke (voxel [0, 0, 0] .. [0, 8, 0]), Masse 20, Preis 3000
- Werte: cable_length=0, rx_length=1.91, rx_range=20000, type=45

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Audio Recv | Ton | Ausgang | (0, 1, 0) | Output for received audio data. |
| Audio Send | Ton | Eingang | (0, 0, 0) | Input for audio data to send. |
| Data Recv | Composite | Ausgang | (0, 1, 0) | Output for received composite data. |
| Data Send | Composite | Eingang | (0, 0, 0) | Input for composite data to send. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical input. |
| Frequency | Zahl | Eingang | (0, 1, 0) | Radio Send/Receive Frequency. |
| Signal Strength | Zahl | Ausgang | (0, 2, 0) | Strength of connection signal. |
| Transmit Mode | An/Aus | Eingang | (0, 0, 0) | Whether the radio is transmitting or receiving. |

## Radio RX Large (`rx_large`)

*A radio data transmitter and receiver.*
Sends and receives data on the specified frequencies.

- Größe 1x5x1 Blöcke (voxel [0, 0, 0] .. [0, 4, 0]), Masse 12, Preis 200
- Werte: cable_length=0, rx_range=4000, type=45

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Data Send | Composite | Eingang | (0, 0, 0) |  |
| Data Recv | Composite | Ausgang | (0, 1, 0) |  |
| Electric | Strom | Eingang | (0, 0, 0) |  |
| Frequency Send | Zahl | Eingang | (0, 0, 0) |  |
| Frequency Recv | Zahl | Eingang | (0, 1, 0) |  |
| Signal Strength | Zahl | Ausgang | (0, 2, 0) |  |

## Radio RX Large (`rx_large_v2`)

*A radio data transmitter and receiver.*
Sends and receives data on the specified frequency. Transmit Mode defaults to receive. (Max effective range at ground level : 4km)

- Größe 1x5x1 Blöcke (voxel [0, 0, 0] .. [0, 4, 0]), Masse 12, Preis 1000
- Werte: cable_length=0, rx_range=4000, type=45

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Audio Recv | Ton | Ausgang | (0, 1, 0) | Output for received audio data. |
| Audio Send | Ton | Eingang | (0, 0, 0) | Input for audio data to send. |
| Data Recv | Composite | Ausgang | (0, 1, 0) | Output for received composite data. |
| Data Send | Composite | Eingang | (0, 0, 0) | Input for composite data to send. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical input. |
| Frequency | Zahl | Eingang | (0, 1, 0) | Radio Send/Receive Frequency. |
| Signal Strength | Zahl | Ausgang | (0, 2, 0) | Strength of connection signal. |
| Transmit Mode | An/Aus | Eingang | (0, 0, 0) | Whether the radio is transmitting or receiving. |

## Radio RX Medium (`rx_med`)

*A radio data transmitter and receiver.*
Sends and receives data on the specified frequencies.

- Größe 1x4x1 Blöcke (voxel [0, 0, 0] .. [0, 3, 0]), Masse 8, Preis 1000
- Werte: cable_length=0, rx_length=0.66, rx_range=1000, type=45

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Data Send | Composite | Eingang | (0, 0, 0) |  |
| Data Recv | Composite | Ausgang | (0, 1, 0) |  |
| Electric | Strom | Eingang | (0, 0, 0) |  |
| Frequency Send | Zahl | Eingang | (0, 0, 0) |  |
| Frequency Recv | Zahl | Eingang | (0, 1, 0) |  |
| Signal Strength | Zahl | Ausgang | (0, 2, 0) |  |

## Radio RX Medium (`rx_med_v2`)

*A radio data transmitter and receiver.*
Sends and receives data on the specified frequency. Transmit Mode defaults to receive. (Max effective range at ground level : 1km)

- Größe 1x4x1 Blöcke (voxel [0, 0, 0] .. [0, 3, 0]), Masse 8, Preis 500
- Werte: cable_length=0, rx_length=0.66, rx_range=1000, type=45

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Audio Recv | Ton | Ausgang | (0, 1, 0) | Output for received audio data. |
| Audio Send | Ton | Eingang | (0, 0, 0) | Input for audio data to send. |
| Data Recv | Composite | Ausgang | (0, 1, 0) | Output for received composite data. |
| Data Send | Composite | Eingang | (0, 0, 0) | Input for composite data to send. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical input. |
| Frequency | Zahl | Eingang | (0, 1, 0) | Radio Send/Receive Frequency. |
| Signal Strength | Zahl | Ausgang | (0, 2, 0) | Strength of connection signal. |
| Transmit Mode | An/Aus | Eingang | (0, 0, 0) | Whether the radio is transmitting or receiving. |

## Radio RX Small (`rx_small`)

*A radio data transmitter and receiver.*
Sends and receives data on the specified frequencies.

- Größe 1x2x1 Blöcke (voxel [0, 0, 0] .. [0, 1, 0]), Masse 5, Preis 500
- Werte: cable_length=0, rx_range=100, type=45

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Data Send | Composite | Eingang | (0, 0, 0) |  |
| Data Recv | Composite | Ausgang | (0, 1, 0) |  |
| Electric | Strom | Eingang | (0, 0, 0) |  |
| Frequency Send | Zahl | Eingang | (0, 0, 0) |  |
| Frequency Recv | Zahl | Eingang | (0, 1, 0) |  |

## Radio RX Small (`rx_small_v2`)

*A radio data transmitter and receiver.*
Sends and receives data on the specified frequency. Transmit Mode defaults to receive. (Max effective range at ground level : 100m)

- Größe 1x2x1 Blöcke (voxel [0, 0, 0] .. [0, 1, 0]), Masse 5, Preis 200
- Werte: cable_length=0, rx_range=100, type=45

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Audio Recv | Ton | Ausgang | (0, 1, 0) | Output for received audio data. |
| Audio Send | Ton | Eingang | (0, 0, 0) | Input for audio data to send. |
| Data Recv | Composite | Ausgang | (0, 1, 0) | Output for received composite data. |
| Data Send | Composite | Eingang | (0, 0, 0) | Input for composite data to send. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical input. |
| Frequency | Zahl | Eingang | (0, 1, 0) | Radio Send/Receive Frequency. |
| Transmit Mode | An/Aus | Eingang | (0, 0, 0) | Whether the radio is transmitting or receiving. |

## Radio Video Recv (`rx_video_r`)

*A radio receiver for receiving video signals.*
Receives a video signal on the frequency specified.

- Größe 1x4x1 Blöcke (voxel [0, 0, 0] .. [0, 3, 0]), Masse 10, Preis 1000
- Werte: cable_length=0, rx_range=10000, type=45

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Video Recv | Video | Ausgang | (0, 0, 0) |  |
| Electric | Strom | Eingang | (0, 0, 0) |  |
| Frequency Recv | Zahl | Eingang | (0, 0, 0) |  |
| Signal Strength | Zahl | Ausgang | (0, 1, 0) |  |

## Radio Video Xmit (`rx_video_x`)

*A radio transmitter for sending video signals.*
Sends a video signal on the frequency specified. (Max Effective Range : 10000m)

- Größe 1x4x1 Blöcke (voxel [0, 0, 0] .. [0, 3, 0]), Masse 10, Preis 2000
- Werte: cable_length=0, rx_range=10000, type=45

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Video Send | Video | Eingang | (0, 0, 0) |  |
| Electric | Strom | Eingang | (0, 0, 0) |  |
| Frequency Send | Zahl | Eingang | (0, 0, 0) |  |

## Rudder (`rudder`)

*The rudder can be attached to the underside of a boat to control its yaw, allowing you to steer left and right.*
It takes a number input between -1 and 1 that represent the two extremes of the rudder's rotation.

- Größe 3x4x3 Blöcke (voxel [-1, 0, -1] .. [1, 3, 1]), Masse 10, Preis 150, Tags: boat,basic
- Werte: dynamic_max_rotation=0.785398, dynamic_min_rotation=-0.785398, rudder_surface_area=13, type=18

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Rotation | Zahl | Eingang | (0, 0, 1) | Accepts a value between -1 and 1 that represent the two extremes of the rudder's rotation. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## RX Directional (`rx_directional`)

*A powerful directional radio and video data transmitter and receiver.*
Must be pointed at the target RX device. Sends and receives data on the specified frequency. Transmit Mode defaults to receive. (Max effective range at ground level : 8000km)

- Größe 5x4x5 Blöcke (voxel [-2, -1, -2] .. [2, 2, 2]), Masse 20, Preis 5000
- Werte: rx_length=0, rx_range=8000000, type=45

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Audio Recv | Ton | Ausgang | (0, 1, 0) | Output for received audio data. |
| Audio Send | Ton | Eingang | (0, 0, 0) | Input for audio data to send. |
| Data Recv | Composite | Ausgang | (0, 1, 0) | Output for received composite data. |
| Data Send | Composite | Eingang | (0, 0, 0) | Input for composite data to send. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical input. |
| Frequency | Zahl | Eingang | (0, 1, 0) | Radio Send/Receive Frequency. |
| Signal Strength | Zahl | Ausgang | (0, -1, 0) | Strength of connection signal. |
| Transmit Mode | An/Aus | Eingang | (0, 0, 0) | Whether the radio is transmitting or receiving. |
| Target Pitch | Zahl | Eingang | (0, 1, 1) | Target dish pitch in turns. Max 0.1 |
| Target Yaw | Zahl | Eingang | (-1, 1, 0) | Target dish yaw in turns. |
| Video Send | Video | Eingang | (1, 1, 0) | Input for video data to send. |
| Video Recv | Video | Ausgang | (0, 1, -1) | Output for recieved video data. |

## RX Directional (Large) (`rx_directional_large`)

*A powerful directional radio and video data transmitter and receiver.*
Must be pointed at the target RX device. Sends and receives data on the specified frequency. Transmit Mode defaults to receive. (Max effective range at ground level : 10000km)

- Größe 9x6x9 Blöcke (voxel [-4, -1, -4] .. [4, 4, 4]), Masse 35, Preis 8000
- Werte: rx_length=0, rx_range=10000000, type=45

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Audio Recv | Ton | Ausgang | (0, 1, 0) | Output for received audio data. |
| Audio Send | Ton | Eingang | (0, 0, 0) | Input for audio data to send. |
| Data Recv | Composite | Ausgang | (0, 1, 0) | Output for received composite data. |
| Data Send | Composite | Eingang | (0, 0, 0) | Input for composite data to send. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical input. |
| Frequency | Zahl | Eingang | (0, 1, 0) | Radio Send/Receive Frequency. |
| Signal Strength | Zahl | Ausgang | (0, 2, 0) | Strength of connection signal. |
| Transmit Mode | An/Aus | Eingang | (0, 0, 0) | Whether the radio is transmitting or receiving. |
| Target Pitch | Zahl | Eingang | (0, 0, 1) | Target dish pitch in turns. Max 0.1 |
| Target Yaw | Zahl | Eingang | (-1, 0, 0) | Target dish yaw in turns. |
| Video Send | Video | Eingang | (1, 0, 0) | Input for video data to send. |
| Video Recv | Video | Ausgang | (0, 0, -1) | Output for recieved video data. |

## Saddle Seat (`seat_saddle`)

*A small padded seat with control handlebars.*
You can get in and out of the seat by interacting with it using [$[action_use_seat]]. You can place a rescued survivor in any seat by using [$[action_use_seat]] while carrying them.

- Größe 3x4x4 Blöcke (voxel [-1, 0, -1] .. [1, 3, 2]), Masse 5, Preis 75, Tags: basic,seat
- Werte: cable_radius=0, rudder_surface_area=0, seat_pose=8, type=1

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Occupied | An/Aus | Ausgang | (0, 0, -1) | Outputs an on signal if the seat is occupied by a character. |
| Trigger [$[action_trigger]] | An/Aus | Ausgang | (0, 1, 2) | Outputs an on signal when [$[action_trigger]] is held, and off when it is not. |
| Look X | Zahl | Ausgang | (-1, 3, 0) | Outputs the character look direction in turns along the X-axis. |
| Look Y | Zahl | Ausgang | (1, 3, 0) | Outputs the character look direction in turns along the Y-axis. |
| Axis 1 [$[action_left]]/[$[action_right]] | Zahl | Ausgang | (-1, 1, 0) | Outputs a standard value between -1 and 1, controlled using [$[action_left]] and [$[action_right]]. [$[action_left]] causes the output value to move towards -1, and [$[action_right]] moves it towards 1. |
| Axis 2 [$[action_up]]/[$[action_down]] | Zahl | Ausgang | (1, 1, 0) | Outputs a standard value between -1 and 1, controlled using [$[action_up]] and [$[action_down]]. [$[action_down]] causes the output value to move towards -1, and [$[action_up]] moves it towards 1. |
| Axis 3 [$[action_pedal_left]]/[$[action_pedal_right]] | Zahl | Ausgang | (-1, 0, 0) | Outputs a standard value between -1 and 1, controlled using [$[action_pedal_left]] and [$[action_pedal_right]]. [$[action_pedal_left]] causes the output value to move towards -1, and [$[action_pedal_right]] moves it towards 1. |
| Axis 4 [$[action_throttle_up]]/[$[action_throttle_down]] | Zahl | Ausgang | (1, 0, 0) | Outputs a standard value between -1 and 1, controlled using [$[action_throttle_up]] and [$[action_throttle_down]]. [$[action_throttle_down]] causes the output value to move towards -1, and [$[action_throttle_up]] moves it towards 1. |
| Hotkey 1 [$[action_hotkey_1]] | An/Aus | Ausgang | (-1, 2, -1) | Outputs an on signal when [$[action_hotkey_1]] is held, and off when it is not. |
| Hotkey 2 [$[action_hotkey_2]] | An/Aus | Ausgang | (-1, 1, -1) | Outputs an on signal when [$[action_hotkey_2]] is held, and off when it is not. |
| Hotkey 3 [$[action_hotkey_3]] | An/Aus | Ausgang | (-1, 0, -1) | Outputs an on signal when [$[action_hotkey_3]] is held, and off when it is not. |
| Hotkey 4 [$[action_hotkey_4]] | An/Aus | Ausgang | (1, 2, -1) | Outputs an on signal when [$[action_hotkey_4]] is held, and off when it is not. |
| Hotkey 5 [$[action_hotkey_5]] | An/Aus | Ausgang | (1, 1, -1) | Outputs an on signal when [$[action_hotkey_5]] is held, and off when it is not. |
| Hotkey 6 [$[action_hotkey_6]] | An/Aus | Ausgang | (1, 0, -1) | Outputs an on signal when [$[action_hotkey_6]] is held, and off when it is not. |
| Seat data | Composite | Ausgang | (0, 0, 0) | Outputs the axis, hotkey and occupied data from the seat. (On/Off 1+ : Hotkeys) (On/Off 31 : Trigger) (On/Off 32 : Occupied) (Value 1 : [$[action_left]]/[$[action_right]]) (Value 2 : [$[action_up]]/[$[action_down]]) (Value 3 : [$[action_pedal_left]]/[$[action_pedal_right]]) (Value 4 : [$[action_throttle_up]]/[$[action_throttle_down]]) (Value 9 : Look X)  (Value 10 : Look Y) |
| Headset Audio | Ton | Ausgang | (-1, 3, -1) |  |
| Headset Audio | Ton | Eingang | (1, 3, -1) |  |
| Headset Video | Video | Eingang | (1, 3, -1) | Displays video UI overlay on a helmet mounted display. |

## Ski (`ski`)

*A wide hinged ski.*
This component has low friction moving along its length, but grips laterally.

- Größe 3x2x13 Blöcke (voxel [-1, 0, -6] .. [1, 1, 6]), Masse 12, Preis 200
- Werte: cable_length=-431602080, constraint_axis=0, type=40

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Steering | Zahl | Eingang | (0, 0, 0) | Accepts a value between -1 and 1 that represents the extremes of the steering rotation. |

## Ski (Small) (`ski_small`)

*A small hinged ski.*
This component has low friction moving along its length, but grips laterally.

- Größe 1x2x9 Blöcke (voxel [0, 0, -4] .. [0, 1, 4]), Masse 8, Preis 100
- Werte: cable_length=-431602080, constraint_axis=0, type=40

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Steering | Zahl | Eingang | (0, 0, 0) | Accepts a value between -1 and 1 that represents the extremes of the steering rotation. |

## Small Wheel (`wheel_small`)

*Small wheel that can be controlled using an engine.*
The wheel will rotate forwards and backwards depending on power received from a connected engine. It can be rotated left and right by sending a number signal to the steering input. It can also be locked into place by sending an on signal to the brake input.

- Größe 3x4x3 Blöcke (voxel [-1, 0, -1] .. [1, 3, 1]), Masse 5, Preis 30, Tags: steerable,steering,basic
- Werte: phys_collision_dampen=2000, rudder_surface_area=0, seat_health_per_sec=1, type=4, wheel_radius=0.58

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Brake | An/Aus | Eingang | (0, 0, 0) | Locks the wheel into place when receiving an on signal. |
| RPS | Drehmoment | Eingang | (0, 0, 0) | Receives power generated by an engine to control forward and backward rotation. |
| Variable Brake | Zahl | Eingang | (0, 1, -1) | A value between 0 and 1 for soft braking |
| Steering | Zahl | Eingang | (0, 1, 1) | Accepts a value between -1 and 1 that represents the extremes of the wheels steering rotation |

## Space Seat (`seat_space`)

*The space seat lets you translate keyboard presses into output signals that can control logic components.*
It provides 4 number outputs that produce a standard value ranging from -1 to 1, and 6 on/off outputs. You can get in and out of the space seat by interacting with it using [$[action_use_seat]].

- Größe 3x7x3 Blöcke (voxel [-1, -4, 0] .. [1, 2, 2]), Masse 3, Preis 500, Tags: basic,seat,control,pilot
- Werte: cable_radius=0, radar_range=3, rudder_surface_area=0, seat_pose=7, type=1

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Occupied | An/Aus | Ausgang | (0, 0, 2) | Outputs an on signal if the handle is occupied by a character. |
| Trigger [$[action_trigger]] | An/Aus | Ausgang | (0, 0, 0) | Outputs an on signal when [$[action_trigger]] is held, and off when it is not. |
| Look X | Zahl | Ausgang | (-1, 2, 1) | Outputs the character look direction in turns along the X-axis. |
| Look Y | Zahl | Ausgang | (1, 2, 1) | Outputs the character look direction in turns along the Y-axis. |
| Axis 1 [$[action_left]]/[$[action_right]] | Zahl | Ausgang | (-1, 0, 1) | Outputs a standard value between -1 and 1, controlled using [$[action_left]] and [$[action_right]]. [$[action_left]] causes the output value to move towards -1, and [$[action_right]] moves it towards 1. |
| Axis 2 [$[action_up]]/[$[action_down]] | Zahl | Ausgang | (1, 0, 1) | Outputs a standard value between -1 and 1, controlled using [$[action_up]] and [$[action_down]]. [$[action_down]] causes the output value to move towards -1, and [$[action_up]] moves it towards 1. |
| Axis 3 [$[action_pedal_left]]/[$[action_pedal_right]] | Zahl | Ausgang | (-1, -1, 1) | Outputs a standard value between -1 and 1, controlled using [$[action_pedal_left]] and [$[action_pedal_right]]. [$[action_pedal_left]] causes the output value to move towards -1, and [$[action_pedal_right]] moves it towards 1. |
| Axis 4 [$[action_throttle_up]]/[$[action_throttle_down]] | Zahl | Ausgang | (1, -1, 1) | Outputs a standard value between -1 and 1, controlled using [$[action_throttle_up]] and [$[action_throttle_down]]. [$[action_throttle_down]] causes the output value to move towards -1, and [$[action_throttle_up]] moves it towards 1. |
| Hotkey 1 [$[action_hotkey_1]] | An/Aus | Ausgang | (-1, 1, 2) | Outputs an on signal when [$[action_hotkey_1]] is held, and off when it is not. |
| Hotkey 2 [$[action_hotkey_2]] | An/Aus | Ausgang | (-1, 0, 2) | Outputs an on signal when [$[action_hotkey_2]] is held, and off when it is not. |
| Hotkey 3 [$[action_hotkey_3]] | An/Aus | Ausgang | (-1, -1, 2) | Outputs an on signal when [$[action_hotkey_3]] is held, and off when it is not. |
| Hotkey 4 [$[action_hotkey_4]] | An/Aus | Ausgang | (1, 1, 2) | Outputs an on signal when [$[action_hotkey_4]] is held, and off when it is not. |
| Hotkey 5 [$[action_hotkey_5]] | An/Aus | Ausgang | (1, 0, 2) | Outputs an on signal when [$[action_hotkey_5]] is held, and off when it is not. |
| Hotkey 6 [$[action_hotkey_6]] | An/Aus | Ausgang | (1, -1, 2) | Outputs an on signal when [$[action_hotkey_6]] is held, and off when it is not. |
| Seat data | Composite | Ausgang | (0, -1, 0) | Outputs the axis, hotkey and occupied data from the helm. (On/Off 1+ : Hotkeys) (On/Off 31 : Trigger) (On/Off 32 : Occupied) (Value 1 : [$[action_left]]/[$[action_right]]) (Value 2 : [$[action_up]]/[$[action_down]]) (Value 3 : [$[action_pedal_left]]/[$[action_pedal_right]]) (Value 4 : [$[action_throttle_up]]/[$[action_throttle_down]]) (Value 9 : Look X)  (Value 10 : Look Y) |
| Headset Audio | Ton | Ausgang | (-1, 2, 2) |  |
| Headset Audio | Ton | Eingang | (1, 2, 2) |  |
| Headset Video | Video | Eingang | (1, 2, 2) | Displays video UI overlay on a helmet mounted display. |
| Fluid In | Fluessigkeit/Gas | Eingang | (0, 0, 0) |  |

## Tank Drive Wheel (Huge) (`wheel_tank_drive_7`)

*Huge drive wheel for tracked vehicles.*
The wheel will form a track with other wheels of the same size and orientation that are placed in line and on the same body.

- Größe 7x5x7 Blöcke (voxel [-3, 0, -3] .. [3, 4, 3]), Masse 80, Preis 450, Tags: steerable,steering
- Werte: phys_collision_dampen=2000, rudder_surface_area=0, seat_health_per_sec=1, type=41, wheel_radius=1, wheel_suspension_height=0.75, wheel_type=3, wheel_wishbone_length=0.62

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Brake | An/Aus | Eingang | (0, 0, 0) | Locks the wheel into place when receiving an on signal. |
| RPS | Drehmoment | Eingang | (0, 0, 0) | Receives power generated by an engine to control forward and backward rotation. |

## Tank Drive Wheel (Large) (`wheel_tank_drive_5`)

*Large drive wheel for tracked vehicles.*
The wheel will form a track with other wheels of the same size and orientation that are placed in line and on the same body.

- Größe 5x3x5 Blöcke (voxel [-2, 0, -2] .. [2, 2, 2]), Masse 40, Preis 350, Tags: steerable,steering
- Werte: phys_collision_dampen=2000, rudder_surface_area=0, seat_health_per_sec=1, type=41, wheel_radius=0.625, wheel_suspension_height=0.75, wheel_type=2, wheel_wishbone_length=0.46

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Brake | An/Aus | Eingang | (0, 0, 0) | Locks the wheel into place when receiving an on signal. |
| RPS | Drehmoment | Eingang | (0, 0, 0) | Receives power generated by an engine to control forward and backward rotation. |

## Tank Drive Wheel (Medium) (`wheel_tank_drive_5_2`)

*Medium drive wheel for tracked vehicles.*
The wheel will form a track with other wheels of the same size and orientation that are placed in line and on the same body.

- Größe 5x3x5 Blöcke (voxel [-2, 0, -2] .. [2, 2, 2]), Masse 30, Preis 300, Tags: steerable,steering
- Werte: phys_collision_dampen=2000, rudder_surface_area=0, seat_health_per_sec=1, type=41, wheel_radius=0.625, wheel_suspension_height=0.75, wheel_type=4, wheel_wishbone_length=0.46

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Brake | An/Aus | Eingang | (0, 0, 0) | Locks the wheel into place when receiving an on signal. |
| RPS | Drehmoment | Eingang | (0, 0, 0) | Receives power generated by an engine to control forward and backward rotation. |

## Tank Drive Wheel (Small) (`wheel_tank_drive_1`)

*Small drive wheel for tracked vehicles.*
The wheel will form a track with other wheels of the same size and orientation that are placed in line and on the same body.

- Größe 3x2x3 Blöcke (voxel [-1, 0, -1] .. [1, 1, 1]), Masse 20, Preis 200, Tags: steerable,steering
- Werte: phys_collision_dampen=2000, rudder_surface_area=0, seat_health_per_sec=1, type=41, wheel_radius=0.4, wheel_suspension_height=0.75, wheel_type=1, wheel_wishbone_length=0.28

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Brake | An/Aus | Eingang | (0, 0, 0) | Locks the wheel into place when receiving an on signal. |
| RPS | Drehmoment | Eingang | (0, 0, 0) | Receives power generated by an engine to control forward and backward rotation. |

## Tank Drive Wheel (Small/Wide) (`wheel_tank_drive_1_wide`)

*Widened small drive wheel for tracked vehicles.*
The wheel will form a track with other wheels of the same size and orientation that are placed in line and on the same body.

- Größe 3x3x3 Blöcke (voxel [-1, 0, -1] .. [1, 2, 1]), Masse 25, Preis 250, Tags: steerable,steering
- Werte: phys_collision_dampen=2000, rudder_surface_area=0, seat_health_per_sec=1, type=41, wheel_radius=0.4, wheel_suspension_height=0.75, wheel_type=8, wheel_wishbone_length=0.28

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Brake | An/Aus | Eingang | (0, 0, 0) | Locks the wheel into place when receiving an on signal. |
| RPS | Drehmoment | Eingang | (0, 0, 0) | Receives power generated by an engine to control forward and backward rotation. |

## Tank Wheel (Huge) (`wheel_tank_7`)

*Huge wheel for tracked vehicles.*
A drive wheel is required to rotate the connected track. The wheel will form a track with other wheels of the same size and orientation that are placed in line and on the same body.

- Größe 7x5x7 Blöcke (voxel [-3, 0, -3] .. [3, 4, 3]), Masse 80, Preis 350, Tags: steerable,steering
- Werte: phys_collision_dampen=2000, rudder_surface_area=0, seat_health_per_sec=1, type=41, wheel_radius=1, wheel_suspension_height=0.75, wheel_type=3, wheel_wishbone_length=0.62

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Brake | An/Aus | Eingang | (0, 0, 0) | Locks the wheel into place when receiving an on signal. |

## Tank Wheel (Large) (`wheel_tank_5`)

*Large wheel for tracked vehicles.*
A drive wheel is required to rotate the connected track. The wheel will form a track with other wheels of the same size and orientation that are placed in line and on the same body.

- Größe 5x3x5 Blöcke (voxel [-2, 0, -2] .. [2, 2, 2]), Masse 40, Preis 250, Tags: steerable,steering
- Werte: phys_collision_dampen=2000, rudder_surface_area=0, seat_health_per_sec=1, type=41, wheel_radius=0.625, wheel_suspension_height=0.75, wheel_type=2, wheel_wishbone_length=0.46

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Brake | An/Aus | Eingang | (0, 0, 0) | Locks the wheel into place when receiving an on signal. |

## Tank Wheel (Medium) (`wheel_tank_5_2`)

*Medium wheel for tracked vehicles.*
A drive wheel is required to rotate the connected track. The wheel will form a track with other wheels of the same size and orientation that are placed in line and on the same body.

- Größe 5x3x5 Blöcke (voxel [-2, 0, -2] .. [2, 2, 2]), Masse 30, Preis 200, Tags: steerable,steering
- Werte: phys_collision_dampen=2000, rudder_surface_area=0, seat_health_per_sec=1, type=41, wheel_radius=0.625, wheel_suspension_height=0.75, wheel_type=4, wheel_wishbone_length=0.46

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Brake | An/Aus | Eingang | (0, 0, 0) | Locks the wheel into place when receiving an on signal. |

## Tank Wheel (Small) (`wheel_tank_1`)

*Small wheel for tracked vehicles.*
A drive wheel is required to rotate the connected track. The wheel will form a track with other wheels of the same size and orientation that are placed in line and on the same body.

- Größe 3x2x3 Blöcke (voxel [-1, 0, -1] .. [1, 1, 1]), Masse 20, Preis 100, Tags: steerable,steering
- Werte: phys_collision_dampen=2000, rudder_surface_area=0, seat_health_per_sec=1, type=41, wheel_radius=0.4, wheel_suspension_height=0.75, wheel_type=1, wheel_wishbone_length=0.28

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Brake | An/Aus | Eingang | (0, 0, 0) | Locks the wheel into place when receiving an on signal. |

## Tank Wheel (Small/Wide) (`wheel_tank_1_wide`)

*Widened small wheel for tracked vehicles.*
A drive wheel is required to rotate the connected track. The wheel will form a track with other wheels of the same size and orientation that are placed in line and on the same body.

- Größe 3x3x3 Blöcke (voxel [-1, 0, -1] .. [1, 2, 1]), Masse 25, Preis 100, Tags: steerable,steering
- Werte: phys_collision_dampen=2000, rudder_surface_area=0, seat_health_per_sec=1, type=41, wheel_radius=0.4, wheel_suspension_height=0.75, wheel_type=8, wheel_wishbone_length=0.28

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Brake | An/Aus | Eingang | (0, 0, 0) | Locks the wheel into place when receiving an on signal. |

## Wheel 3x3 (`wheel_advanced_3`)

*Small steerable wheel with power connection and braking.*
The wheel will rotate forwards and backwards depending on power received. It can be rotated left and right by sending a number signal to the steering input. It can also be locked into place by sending an on signal to the brake input.

- Größe 3x2x3 Blöcke (voxel [-1, 0, -1] .. [1, 1, 1]), Masse 10, Preis 100, Tags: steerable,steering,basic
- Werte: phys_collision_dampen=2000, rudder_surface_area=0, seat_health_per_sec=1, type=41, wheel_radius=0.35, wheel_suspension_height=0.5, wheel_wishbone_length=0.75, wheel_wishbone_margin=0.075

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Brake | An/Aus | Eingang | (0, 0, 0) | Locks the wheel into place when receiving an on signal. |
| RPS | Drehmoment | Eingang | (0, 0, 0) | Receives power generated by an engine to control forward and backward rotation. |
| Variable Brake | Zahl | Eingang | (0, 1, -1) | A value between 0 and 1 for soft braking |
| Steering | Zahl | Eingang | (0, 1, 1) | Accepts a value between -1 and 1 that represents the extremes of the wheels steering rotation |

## Wheel 3x3 (Suspension) (`wheel_advanced_3_sus`)

*Small steerable wheel with suspension, power connection, and braking.*
The wheel will rotate forwards and backwards depending on power received. It can be rotated left and right by sending a number signal to the steering input. It can also be locked into place by sending an on signal to the brake input.

- Größe 3x3x3 Blöcke (voxel [-1, 0, -1] .. [1, 2, 1]), Masse 15, Preis 150, Tags: steerable,steering
- Werte: phys_collision_dampen=2000, rudder_surface_area=0, seat_health_per_sec=1, type=41, wheel_radius=0.35, wheel_suspension_height=0.5, wheel_suspension_offset=0.375, wheel_wishbone_length=0.5, wheel_wishbone_margin=0.02

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Brake | An/Aus | Eingang | (0, 0, 0) | Locks the wheel into place when receiving an on signal. |
| RPS | Drehmoment | Eingang | (0, 0, 0) | Receives power generated by an engine to control forward and backward rotation. |
| Variable Brake | Zahl | Eingang | (0, 2, -1) | A value between 0 and 1 for soft braking |
| Steering | Zahl | Eingang | (0, 2, 1) | Accepts a value between -1 and 1 that represents the extremes of the wheels steering rotation |

## Wheel 5x5 (`wheel_advanced_5`)

*Medium steerable wheel with power connection and braking.*
The wheel will rotate forwards and backwards depending on power received. It can be rotated left and right by sending a number signal to the steering input. It can also be locked into place by sending an on signal to the brake input.

- Größe 5x3x5 Blöcke (voxel [-2, 0, -2] .. [2, 2, 2]), Masse 20, Preis 150, Tags: steerable,steering,basic
- Werte: phys_collision_dampen=2000, rudder_surface_area=0, seat_health_per_sec=1, type=41, wheel_radius=0.58, wheel_suspension_height=0.75, wheel_width=0.5, wheel_wishbone_length=1

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Brake | An/Aus | Eingang | (0, 0, 0) | Locks the wheel into place when receiving an on signal. |
| RPS | Drehmoment | Eingang | (0, 0, 0) | Receives power generated by an engine to control forward and backward rotation. |
| Variable Brake | Zahl | Eingang | (0, 1, -1) | A value between 0 and 1 for soft braking |
| Steering | Zahl | Eingang | (0, 1, 1) | Accepts a value between -1 and 1 that represents the extremes of the wheels steering rotation |

## Wheel 5x5 (Suspension) (`wheel_advanced_5_sus`)

*Medium steerable wheel with suspension, power connection, and braking.*
The wheel will rotate forwards and backwards depending on power received. It can be rotated left and right by sending a number signal to the steering input. It can also be locked into place by sending an on signal to the brake input.

- Größe 5x5x5 Blöcke (voxel [-2, 0, -2] .. [2, 4, 2]), Masse 30, Preis 200, Tags: steerable,steering
- Werte: phys_collision_dampen=2000, rudder_surface_area=0, seat_health_per_sec=1, type=41, wheel_radius=0.58, wheel_suspension_height=0.75, wheel_suspension_offset=0.625, wheel_width=0.5, wheel_wishbone_length=0.75, wheel_wishbone_margin=0.02

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Brake | An/Aus | Eingang | (0, 0, 0) | Locks the wheel into place when receiving an on signal. |
| RPS | Drehmoment | Eingang | (0, 0, 0) | Receives power generated by an engine to control forward and backward rotation. |
| Variable Brake | Zahl | Eingang | (0, 3, -1) | A value between 0 and 1 for soft braking |
| Steering | Zahl | Eingang | (0, 3, 1) | Accepts a value between -1 and 1 that represents the extremes of the wheels steering rotation |

## Wheel 7x7 (`wheel_advanced_7`)

*Large steerable wheel with power connection and braking.*
The wheel will rotate forwards and backwards depending on power received. It can be rotated left and right by sending a number signal to the steering input. It can also be locked into place by sending an on signal to the brake input.

- Größe 7x4x7 Blöcke (voxel [-3, 0, -3] .. [3, 3, 3]), Masse 40, Preis 200, Tags: steerable,steering,basic
- Werte: phys_collision_dampen=2000, rudder_surface_area=0, seat_health_per_sec=1, type=41, wheel_radius=0.85, wheel_suspension_height=0.75, wheel_width=0.75, wheel_wishbone_length=1

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Brake | An/Aus | Eingang | (0, 0, 0) | Locks the wheel into place when receiving an on signal. |
| RPS | Drehmoment | Eingang | (0, 0, 0) | Receives power generated by an engine to control forward and backward rotation. |
| Variable Brake | Zahl | Eingang | (0, 1, -1) | A value between 0 and 1 for soft braking |
| Steering | Zahl | Eingang | (0, 1, 1) | Accepts a value between -1 and 1 that represents the extremes of the wheels steering rotation |

## Wheel 7x7 (Suspension) (`wheel_advanced_7_sus`)

*Large steerable wheel with suspension, power connection, and braking.*
The wheel will rotate forwards and backwards depending on power received. It can be rotated left and right by sending a number signal to the steering input. It can also be locked into place by sending an on signal to the brake input.

- Größe 7x6x7 Blöcke (voxel [-3, 0, -3] .. [3, 5, 3]), Masse 60, Preis 250, Tags: steerable,steering
- Werte: phys_collision_dampen=2000, rudder_surface_area=0, seat_health_per_sec=1, type=41, wheel_radius=0.85, wheel_suspension_offset=0.625, wheel_width=0.75, wheel_wishbone_length=0.75, wheel_wishbone_margin=0.02

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Brake | An/Aus | Eingang | (0, 0, 0) | Locks the wheel into place when receiving an on signal. |
| RPS | Drehmoment | Eingang | (0, 0, 0) | Receives power generated by an engine to control forward and backward rotation. |
| Variable Brake | Zahl | Eingang | (0, 3, -1) | A value between 0 and 1 for soft braking |
| Steering | Zahl | Eingang | (0, 3, 1) | Accepts a value between -1 and 1 that represents the extremes of the wheels steering rotation |

## Wheel 9x9 (`wheel_advanced_9`)

*XLarge steerable wheel with power connection and braking.*
The wheel will rotate forwards and backwards depending on power received. It can be rotated left and right by sending a number signal to the steering input. It can also be locked into place by sending an on signal to the brake input.

- Größe 9x5x9 Blöcke (voxel [-4, 0, -4] .. [4, 4, 4]), Masse 80, Preis 250, Tags: steerable,steering,basic
- Werte: phys_collision_dampen=2000, rudder_surface_area=0, seat_health_per_sec=1, type=41, wheel_radius=1.05, wheel_width=1.0

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Brake | An/Aus | Eingang | (0, 0, 0) | Locks the wheel into place when receiving an on signal. |
| RPS | Drehmoment | Eingang | (0, 0, 0) | Receives power generated by an engine to control forward and backward rotation. |
| Variable Brake | Zahl | Eingang | (0, 1, -1) | A value between 0 and 1 for soft braking |
| Steering | Zahl | Eingang | (0, 1, 1) | Accepts a value between -1 and 1 that represents the extremes of the wheels steering rotation |

## Wheel 9x9 (Suspension) (`wheel_advanced_9_sus`)

*XLarge steerable wheel with suspension, power connection, and braking.*
The wheel will rotate forwards and backwards depending on power received. It can be rotated left and right by sending a number signal to the steering input. It can also be locked into place by sending an on signal to the brake input.

- Größe 9x8x10 Blöcke (voxel [-4, 0, -4] .. [4, 7, 5]), Masse 120, Preis 300, Tags: steerable,steering
- Werte: phys_collision_dampen=2000, rudder_surface_area=0, seat_health_per_sec=1, type=41, wheel_radius=1.05, wheel_suspension_height=1.25, wheel_suspension_offset=0.875, wheel_width=1.0, wheel_wishbone_length=1, wheel_wishbone_margin=0.02, wheel_wishbone_offset=0.25

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Brake | An/Aus | Eingang | (0, 0, 0) | Locks the wheel into place when receiving an on signal. |
| RPS | Drehmoment | Eingang | (0, 0, 0) | Receives power generated by an engine to control forward and backward rotation. |
| Variable Brake | Zahl | Eingang | (0, 4, -1) | A value between 0 and 1 for soft braking |
| Steering | Zahl | Eingang | (0, 4, 1) | Accepts a value between -1 and 1 that represents the extremes of the wheels steering rotation |

## Wheel Coaster (`wheel_coaster`)

*Simple small wheel that requires no engine power and spins freely.*
You cannot control the forward and backward rotation of this wheel, but it can be locked into place by sending an on signal to the brake input.

- Größe 3x3x3 Blöcke (voxel [-1, 0, -1] .. [1, 2, 1]), Masse 4, Preis 25, Tags: basic
- Werte: phys_collision_dampen=2000, rudder_surface_area=0, type=4, wheel_radius=0.4

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Brake | An/Aus | Eingang | (0, 0, 0) | Locks the wheel into place when receiving an on signal. |
| Variable Brake | Zahl | Eingang | (0, 1, -1) | A value between 0 and 1 for soft braking |

## Wing Front Section (Small) (`wing_small_front`)

*The wing front surface cuts through the air while resisting movement against the flat plane of its surface. The aerofoil section also provides lift.*
Wing surface to provide lift and cut through the air.

- Größe 1x7x3 Blöcke (voxel [0, -3, -2] .. [0, 3, 0]), Masse 5, Preis 100, Tags: airplane,aeroplane,basic
- Werte: cable_radius=0, dynamic_max_rotation=0.785398, dynamic_min_rotation=-0.785398, rudder_surface_area=4, rudder_type=1, type=18

## Wing Section (Large) (`wing_large`)

*The wing surface cuts through the air while resisting movement against the flat plane of its surface. The aerofoil section also provides lift.*
Wing surface to provide lift and cut through the air.

- Größe 3x7x16 Blöcke (voxel [-1, -3, -14] .. [1, 3, 1]), Masse 20, Preis 500, Tags: airplane,aeroplane,basic
- Werte: cable_radius=0, dynamic_max_rotation=0.785398, dynamic_min_rotation=-0.785398, rudder_surface_area=40, rudder_type=1, type=18

## Wing Section (Medium) (`wing_medium`)

*The wing surface cuts through the air while resisting movement against the flat plane of its surface. The aerofoil section also provides lift.*
Wing surface to provide lift and cut through the air.

- Größe 2x3x10 Blöcke (voxel [0, -1, -8] .. [1, 1, 1]), Masse 15, Preis 350, Tags: airplane,aeroplane,basic
- Werte: cable_radius=0, dynamic_max_rotation=0.785398, dynamic_min_rotation=-0.785398, rudder_surface_area=20, rudder_type=1, type=18

## Wing Section (Small) (`wing_small`)

*The wing surface cuts through the air while resisting movement against the flat plane of its surface. The aerofoil section also provides lift.*
Wing surface to provide lift and cut through the air.

- Größe 1x3x6 Blöcke (voxel [0, -1, -5] .. [0, 1, 0]), Masse 8, Preis 150, Tags: airplane,aeroplane,basic
- Werte: cable_radius=0, dynamic_max_rotation=0.785398, dynamic_min_rotation=-0.785398, rudder_surface_area=8, rudder_type=1, type=18

## Wing Section (XLarge) (`wing_xl`)

*The wing surface cuts through the air while resisting movement against the flat plane of its surface. The aerofoil section also provides lift.*
Wing surface to provide lift and cut through the air.

- Größe 3x7x22 Blöcke (voxel [-1, -3, -20] .. [1, 3, 1]), Masse 30, Preis 800, Tags: airplane,aeroplane,basic
- Werte: cable_radius=0, dynamic_max_rotation=0.785398, dynamic_min_rotation=-0.785398, rudder_surface_area=70, rudder_type=1, type=18

## Wing Section (XXLarge) (`wing_xxl`)

*The wing surface cuts through the air while resisting movement against the flat plane of its surface. The aerofoil section also provides lift.*
Wing surface to provide lift and cut through the air.

- Größe 3x7x28 Blöcke (voxel [-1, -3, -26] .. [1, 3, 1]), Masse 50, Preis 1500, Tags: airplane,aeroplane
- Werte: cable_radius=0, dynamic_max_rotation=0.785398, dynamic_min_rotation=-0.785398, rudder_surface_area=120, rudder_type=1, type=18
