# Anzeigen (Kategorie 6)

Aus den Spieldaten erzeugt von `tools/bauteile_holen.py` - nicht von Hand ändern.

## Artificial Horizon (`artificial_horizon`)

*The artificial horizon shows you the orientation of your vehicle with respect to the horizon line.*
The horizon ball rotates up and down as your vehicle's pitch changes, and the central line gives an indication of your vehicle's roll. This is a useful component to have in your helicopter to make it easier to fly at night and in thick fog. An on/off signal can be used to toggle the backlight.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 20, Tags: basic
- Werte: buoy_factor=1.000000, buoy_force=100.000000, buoy_radius=1.000000, constraint_range_of_motion=0.000000, door_lower_limit=-1.000000, door_upper_limit=1.000000, dynamic_min_rotation=0.000000, engine_max_force=1000.000000, force_emitter_max_force=1000.000000, force_emitter_max_vector=1.000000, indicator_type=2, light_fov=1.000000, light_intensity=0.000000, light_range=1.000000, magnet_force=1.000000, max_motor_force=100.000000, rudder_surface_area=0.000000, type=21, wheel_radius=0.250000

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Backlight | An/Aus | Eingang | (0, 0, 0) | Enables the backlight when receiving an on signal. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Buzzer (`buzzer`)

*A buzzer that will play a selected sound when toggled from off to on.*
The type of sound, volume, and pitch can be customised by selecting this component with the select tool. It has an audible range of 30m.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 100, Tags: sound,audio,siren
- Werte: cable_radius=0.02, indicator_type=6, m_pump_pressure=0.01, type=21

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Buzzer | An/Aus | Eingang | (0, 0, 0) | Plays the selected sound when toggled from off to on. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Clock (`clock`)

*An analogue clock display that outputs a number value representing the time of day.*
The clock has a display to visualise the time of day or night. The 12 o'clock position is the white arrow on the face of the display.

- Größe 1x2x1 Blöcke (voxel [0, 0, 0] .. [0, 1, 0]), Masse 1, Preis 100, Tags: basic
- Werte: cable_radius=0, light_intensity=0, logic_gate_type=42, magnet_force=0, max_motor_speed=5, rudder_surface_area=0, type=16

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Time | Zahl | Ausgang | (0, 0, 0) | The time as a factor of a day, from 0 (midnight) to 1 (midnight). |
| Backlight | An/Aus | Eingang | (0, 1, 0) | Enables the backlight when receiving an on signal. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Compass Ball (`compass`)

*The compass rotates to point to north on the map.*
It is one of several tools that can be used to aid navigation in low visibility situations. An on/off signal controls whether or not the compass' backlight is enabled.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 20, Tags: basic
- Werte: buoy_factor=1.000000, buoy_force=100.000000, buoy_radius=1.000000, constraint_range_of_motion=0.000000, door_lower_limit=-1.000000, door_upper_limit=1.000000, dynamic_min_rotation=0.000000, engine_max_force=1000.000000, force_emitter_max_force=1000.000000, force_emitter_max_vector=1.000000, indicator_type=4, light_fov=1.000000, light_intensity=0.000000, light_range=1.000000, magnet_force=1.000000, max_motor_force=100.000000, rudder_surface_area=0.000000, type=21, wheel_radius=0.250000

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Backlight | An/Aus | Eingang | (0, 0, 0) | Enables the backlight when receiving an on signal. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Dial (`dial`)

*A dial with a rotating needle for displaying numerical values.*
The dial's face represents values ranging from -1 to 1 by default. This can be configured by selecting it with the select tool. Values outside this range will cause the needle to wrap around, but can be scaled to fit using additional logic components if necessary. An on/off signal can be used to toggle the backlight.

- Größe 1x2x1 Blöcke (voxel [0, 0, 0] .. [0, 1, 0]), Masse 1, Preis 20, Tags: basic
- Werte: buoy_factor=1.000000, buoy_force=100.000000, buoy_radius=1.000000, constraint_range_of_motion=0.000000, door_lower_limit=-1.000000, door_upper_limit=1.000000, dynamic_min_rotation=0.000000, engine_max_force=1000.000000, force_emitter_max_force=1000.000000, force_emitter_max_vector=1.000000, light_fov=1.000000, light_intensity=0.000000, light_range=1.000000, magnet_force=1.000000, max_motor_force=100.000000, rudder_surface_area=0.000000, type=21, wheel_radius=0.250000

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Value to Display | Zahl | Eingang | (0, 0, 0) | The numerical value to display, ideally scaled to be within a -1 to 1 range. |
| Backlight | An/Aus | Eingang | (0, 1, 0) | Enables the backlight when receiving an on signal. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Digital Display (`digital_display`)

*Displays a 5 digit (6 with decimal point disabled) signed numerical value with optional decimal point.*
The position of the decimal point can be configured by selecting this component with the select tool, allowing you to control the number of decimal places in the output.

- Größe 1x1x2 Blöcke (voxel [0, 0, 0] .. [0, 0, 1]), Masse 2, Preis 20, Tags: basic
- Werte: buoy_factor=1.000000, buoy_force=100.000000, buoy_radius=1.000000, constraint_range_of_motion=0.000000, door_lower_limit=-1.000000, door_upper_limit=1.000000, dynamic_min_rotation=0.000000, engine_max_force=1000.000000, force_emitter_max_force=1000.000000, force_emitter_max_vector=1.000000, indicator_type=3, light_fov=1.000000, light_intensity=0.000000, light_range=1.000000, magnet_force=1.000000, max_motor_force=100.000000, rudder_surface_area=0.000000, type=21, wheel_radius=0.250000

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Value to Display | Zahl | Eingang | (0, 0, 0) | The numerical value to display. |
| Backlight | An/Aus | Eingang | (0, 0, 1) | Enables the backlight when receiving an on signal. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Gauge Display (`gauge_display`)

*A display with two needles that can be positioned independently.*
The primary needle is white and the secondary needle is red. The positions of the needles represent values ranging from -1 to 1 by default. This range can be configured by selecting the display with the select tool.

- Größe 1x2x2 Blöcke (voxel [0, 0, 0] .. [0, 1, 1]), Masse 2, Preis 20
- Werte: buoy_factor=1.000000, buoy_force=100.000000, buoy_radius=1.000000, constraint_range_of_motion=0.000000, door_lower_limit=-1.000000, door_upper_limit=1.000000, dynamic_min_rotation=0.000000, engine_max_force=1000.000000, force_emitter_max_force=1000.000000, force_emitter_max_vector=1.000000, indicator_type=5, light_fov=1.000000, light_intensity=0.000000, light_range=1.000000, magnet_force=1.000000, max_motor_force=100.000000, rudder_surface_area=0.000000, type=21, wheel_radius=0.250000

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Primary Display Value | Zahl | Eingang | (0, 0, 0) | The numerical value that sets the position of the white needle. |
| Secondary Display Value | Zahl | Eingang | (0, 0, 1) | The numerical value that sets the position of the red needle. |
| Backlight | An/Aus | Eingang | (0, 1, 0) | Enables the backlight when receiving an on signal. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## HUD Large (`monitor_hud_3`)

*A clear projection heads up display screen.*
Displays video data.

- Größe 3x1x3 Blöcke (voxel [-1, 0, -1] .. [1, 0, 1]), Masse 18, Preis 10000
- Werte: cable_length=0, monitor_border=0.02, monitor_inset=0.01, type=43

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Video Signal | Video | Eingang | (0, 0, 0) |  |
| Touch Output | Composite | Ausgang | (0, 0, 0) |  |
| Electric | Strom | Eingang | (0, 0, 0) |  |
| Power Switch | An/Aus | Eingang | (0, 0, 0) | Controls whether or not the screen is switched on. |

## HUD Small (`monitor_hud_1`)

*A clear projection heads up display screen.*
Displays video data.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 2, Preis 2000
- Werte: cable_length=0, monitor_border=0.02, monitor_inset=0.01, type=43

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Video Signal | Video | Eingang | (0, 0, 0) |  |
| Touch Output | Composite | Ausgang | (0, 0, 0) |  |
| Electric | Strom | Eingang | (0, 0, 0) |  |
| Power Switch | An/Aus | Eingang | (0, 0, 0) | Controls whether or not the screen is switched on. |

## Indicator Light (`indicator`)

*A simple light that can be used as an indicator in logic systems.*

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 20, Tags: basic
- Werte: buoy_factor=1.000000, buoy_force=100.000000, buoy_radius=1.000000, constraint_range_of_motion=0.000000, door_lower_limit=-1.000000, door_upper_limit=1.000000, dynamic_min_rotation=0.000000, engine_max_force=1000.000000, force_emitter_max_force=1000.000000, force_emitter_max_vector=1.000000, indicator_type=1, light_fov=1.000000, light_intensity=0.000000, light_range=1.000000, magnet_force=1.000000, max_motor_force=100.000000, rudder_surface_area=0.000000, type=21, wheel_radius=0.250000

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Indicator Light | An/Aus | Eingang | (0, 0, 0) | Switches the light on when receiving an on signal. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Indicator Light (RGB) (`indicator_rgb`)

*An advanced indicator that can be controlled using a microcontroller.*
Three channels of the composite input can be used to set the red, green and blue components of the indicator's color using numbers between 0 and 1. The light can also operate in HSV mode, where the 3 inputs correspond to the hue, saturation and value (brightness) of the color between 0 and 1. The color mode and input channels can be customised by selecting this component with the select tool.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 50, Tags: basic
- Werte: cable_radius=0.02, composite_type=1, indicator_type=1, light_intensity=0, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, type=38

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Color Data | Composite | Eingang | (0, 0, 0) | Composite link containing the indicator's color data. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Instrument Panel (`instrument_display`)

*A customisable panel that can have up to 4 different instruments, controlled by a composite signal from a microcontroller.*
The 4 instruments can be selected in the properties window. Each type of instrument has options for choosing the composite channels that they read from or write to. Composite signals are bridged from the input node to the output node to enable displays to be chained together. Instruments marked as '(On/Off)' require multiple on/off signals to control each of their segments individually.

- Größe 1x2x1 Blöcke (voxel [0, 0, 0] .. [0, 1, 0]), Masse 1, Preis 200
- Werte: button_type=0, cable_radius=0.02, composite_type=2, constraint_axis=0, door_lower_limit=0, door_upper_limit=0, dynamic_max_rotation=0, force_emitter_max_vector=0, light_fov=0, light_intensity=0, light_range=0, magnet_force=0, max_motor_force=0, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, type=38, wheel_radius=0

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Out Signal | Composite | Ausgang | (0, 0, 0) | Output signal containing data set by buttons on the display. |
| In Signal | Composite | Eingang | (0, 1, 0) | Input signal containing data to be displayed. |
| Electric | Strom | Ausgang | (0, 0, 0) | Electrical power connection. |
| Backlight | An/Aus | Eingang | (0, 0, 0) | Enables the backlight when receiving an on signal. |

## Laser Beacon (`laser_beacon`)

*A beacon that produces a laser point light, visible by laser point sensors.*

- Größe 1x2x1 Blöcke (voxel [0, 0, 0] .. [0, 1, 0]), Masse 1, Preis 5
- Werte: cable_radius=0.02, indicator_type=10, light_intensity=0, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, type=21

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Beacon Light | An/Aus | Eingang | (0, 0, 0) | Switches the beacon on when receiving an on signal. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |
| Wavelength | Zahl | Eingang | (0, 1, 0) | The specific light wavelength to emit (whole number). |

## Monitor 1x1 (`monitor_1`)

*A video screen.*
Displays video data.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 4, Preis 500
- Werte: cable_length=0, monitor_border=0.022, monitor_inset=0.012, type=43

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Video Signal | Video | Eingang | (0, 0, 0) |  |
| Touch Output | Composite | Ausgang | (0, 0, 0) |  |
| Electric | Strom | Eingang | (0, 0, 0) |  |
| Power Switch | An/Aus | Eingang | (0, 0, 0) | Controls whether or not the screen is switched on. |

## Monitor 1x2 (`monitor_1x2`)

*A video screen.*
Displays video data.

- Größe 2x1x1 Blöcke (voxel [0, 0, 0] .. [1, 0, 0]), Masse 8, Preis 1000
- Werte: cable_length=0, monitor_border=0.022, monitor_inset=0.012, type=43

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Video Signal | Video | Eingang | (0, 0, 0) |  |
| Touch Output | Composite | Ausgang | (0, 0, 0) |  |
| Electric | Strom | Eingang | (0, 0, 0) |  |
| Power Switch | An/Aus | Eingang | (0, 0, 0) | Controls whether or not the screen is switched on. |

## Monitor 1x3 (`monitor_1x3`)

*A video screen.*
Displays video data.

- Größe 3x1x1 Blöcke (voxel [-1, 0, 0] .. [1, 0, 0]), Masse 12, Preis 1500
- Werte: cable_length=0, monitor_border=0.022, monitor_inset=0.012, type=43

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Video Signal | Video | Eingang | (0, 0, 0) |  |
| Touch Output | Composite | Ausgang | (0, 0, 0) |  |
| Electric | Strom | Eingang | (0, 0, 0) |  |
| Power Switch | An/Aus | Eingang | (0, 0, 0) | Controls whether or not the screen is switched on. |

## Monitor 2x2 (`monitor_2`)

*A video screen.*
Displays video data.

- Größe 2x1x2 Blöcke (voxel [-1, 0, 0] .. [0, 0, 1]), Masse 16, Preis 2000
- Werte: cable_length=0, monitor_border=0.022, monitor_inset=0.012, type=43

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Video Signal | Video | Eingang | (0, 0, 0) |  |
| Touch Output | Composite | Ausgang | (0, 0, 0) |  |
| Electric | Strom | Eingang | (0, 0, 0) |  |
| Power Switch | An/Aus | Eingang | (0, 0, 0) | Controls whether or not the screen is switched on. |

## Monitor 2x3 (`monitor_2x3`)

*A video screen.*
Displays video data.

- Größe 3x1x2 Blöcke (voxel [-1, 0, 0] .. [1, 0, 1]), Masse 24, Preis 3000
- Werte: cable_length=0, monitor_border=0.022, monitor_inset=0.012, type=43

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Video Signal | Video | Eingang | (0, 0, 0) |  |
| Touch Output | Composite | Ausgang | (0, 0, 0) |  |
| Electric | Strom | Eingang | (0, 0, 0) |  |
| Power Switch | An/Aus | Eingang | (0, 0, 0) | Controls whether or not the screen is switched on. |

## Monitor 3x3 (`monitor_3`)

*A video screen.*
Displays video data.

- Größe 3x1x3 Blöcke (voxel [-1, 0, -1] .. [1, 0, 1]), Masse 36, Preis 4500
- Werte: cable_length=0, monitor_border=0.022, monitor_inset=0.012, type=43

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Video Signal | Video | Eingang | (0, 0, 0) |  |
| Touch Output | Composite | Ausgang | (0, 0, 0) |  |
| Electric | Strom | Eingang | (0, 0, 0) |  |
| Power Switch | An/Aus | Eingang | (0, 0, 0) | Controls whether or not the screen is switched on. |

## Monitor 5x3 (`monitor_5`)

*A video screen.*
Displays video data.

- Größe 5x1x3 Blöcke (voxel [-2, 0, -1] .. [2, 0, 1]), Masse 60, Preis 7500
- Werte: cable_length=0, monitor_border=0.022, monitor_inset=0.012, type=43

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Video Signal | Video | Eingang | (0, 0, 0) |  |
| Touch Output | Composite | Ausgang | (0, 0, 0) |  |
| Electric | Strom | Eingang | (0, 0, 0) |  |
| Power Switch | An/Aus | Eingang | (0, 0, 0) | Controls whether or not the screen is switched on. |

## Monitor 9x5 (`monitor_9`)

*A video screen.*
Displays video data.

- Größe 9x1x5 Blöcke (voxel [-4, 0, -2] .. [4, 0, 2]), Masse 180, Preis 20000
- Werte: cable_length=0, monitor_border=0.022, monitor_inset=0.012, type=43

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Video Signal | Video | Eingang | (0, 0, 0) |  |
| Touch Output | Composite | Ausgang | (0, 0, 0) |  |
| Electric | Strom | Eingang | (0, 0, 0) |  |
| Power Switch | An/Aus | Eingang | (0, 0, 0) | Controls whether or not the screen is switched on. |

## Paintable Indicator (`sign`)

*A backlit indicator for displaying painted detail.*
This block has a paintable surface where small grid squares can be painted individually. Use additive painting mode to paint the backlight grid. The backlight can be enabled by using an on signal and a name can be set with the select tool that will be visible when the indicator is looked at by a player.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 2, Preis 100, Tags: sign,basic
- Werte: button_type=0, cable_radius=0.02, constraint_axis=0, door_lower_limit=0, door_upper_limit=0, dynamic_max_rotation=0, force_emitter_max_vector=0, light_fov=0, light_intensity=0, light_range=0, magnet_force=0, max_motor_force=0, max_motor_speed=5, rudder_surface_area=0, type=28, wheel_radius=0

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Backlight | An/Aus | Eingang | (0, 0, 0) | Switches the backlight on when receiving an on signal. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Paintable Sign (`sign_na`)

*Sign block for displaying painted detail.*
This block has a paintable surface where small grid squares can be painted individually.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 50, Tags: basic
- Werte: rudder_surface_area=0, type=28

## Speaker (Small) (`speaker`)

*A speaker capable of playing audio data to players within its range.*
A small speaker capable of playing audio data to nearby players. (Range : 15)

- Größe 1x2x1 Blöcke (voxel [0, 0, 0] .. [0, 1, 0]), Masse 1, Preis 250
- Werte: cable_radius=0.02, light_intensity=0, logic_gate_type=52, magnet_force=0, max_motor_speed=5, pump_pressure=0, radar_range=15, rudder_surface_area=0, type=16

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Audio | Ton | Eingang | (0, 0, 0) | Audio data connection. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |
| Is Transmit | An/Aus | Ausgang | (0, 1, 0) | If the speaker is currently transmitting. |

## Viewing Scope (`viewing_scope`)

*A viewing scope.*
Interact to display video data at full detail.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 5, Preis 2000
- Werte: monitor_border=0.022, monitor_inset=0.012, type=64

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Video Signal | Video | Eingang | (0, 0, 0) |  |
| Electric | Strom | Eingang | (0, 0, 0) |  |
| Occupied | An/Aus | Ausgang | (0, 0, 0) | Outputs an on signal if this viewing scope is occupied by a character. |
