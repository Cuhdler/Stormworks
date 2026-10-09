# Sensoren (Kategorie 7)

Aus den Spieldaten erzeugt von `tools/bauteile_holen.py` - nicht von Hand ändern.

## Altimeter (`altimeter`)

*An altitude sensor.*
Outputs distance above sea-level in meters.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 20, Tags: aeroplane,airplane,helicopter
- Werte: cable_length=0, cable_radius=0.02, light_intensity=0, logic_gate_type=18, magnet_force=0, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, type=16

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Altitude | Zahl | Ausgang | (0, 0, 0) | The measured altitude of the component in metres above sea-level. |

## Angular Speed Sensor (`angular_speed_sensor`)

*This sensor outputs its current angular speed in rotations per second, allowing you to measure how fast your vehicle is rotating.*
This sensor outputs the angular speed of the component about the component's y axis.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 20
- Werte: cable_radius=0.02, light_intensity=0, logic_gate_type=49, magnet_force=0, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, type=16

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Angular Speed | Zahl | Ausgang | (0, 0, 0) | The sensor's angular speed in rotations per second. |

## Astronomy Sensor (`astronomy_sensor`)

*A sensor that provides raw space navigation data.*
Outputs relative position data based on the optimal target trajectory between the earth and moon.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 150
- Werte: logic_gate_type=62, piston_cam=0, piston_len=0, radar_range=0, radar_speed=0, type=16

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Data | Composite | Ausgang | (0, 0, 0) | Outputs [1] x position in metres, [2] y position in metres (earth sea level is 0), [3] z position in metres, [4] euler rotation x, [5] euler rotation y, [6] euler rotation z, [7] angular velocity x, [8] angular velocity y, [9] angular velocity z, [10] local z tilt and [11] local x tilt to the respective composite channels. |

## Barometer (`barometer`)

*Measures the current air pressure.*
Returns the pressure in atmospheres of the compartment or current altitude.

- Größe 1x2x1 Blöcke (voxel [0, 0, 0] .. [0, 1, 0]), Masse 1, Preis 20
- Werte: type=24, water_component_type=30

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Pressure | Zahl | Ausgang | (0, 0, 0) |  |

## Compass Sensor (`compass_sensor`)

*A digital compass that outputs a number value representing the turn that must be made for it to face north.*
The sensor has a display to visualise the direction of north. The measured output is taken relative to the white arrow on the face of the display.

- Größe 1x2x1 Blöcke (voxel [0, 0, 0] .. [0, 1, 0]), Masse 1, Preis 20
- Werte: buoy_factor=1.000000, buoy_force=100.000000, buoy_radius=1.000000, constraint_range_of_motion=0.000000, door_lower_limit=-1.000000, door_upper_limit=1.000000, dynamic_min_rotation=0.000000, engine_max_force=1000.000000, force_emitter_max_force=1000.000000, force_emitter_max_vector=1.000000, light_fov=1.000000, light_intensity=0.000000, light_range=1.000000, logic_gate_type=31, magnet_force=0.000000, max_motor_force=100.000000, rudder_surface_area=0.000000, type=16, wheel_radius=0.250000

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Compass Reading | Zahl | Ausgang | (0, 0, 0) | The angle measured in turns that the needle is rotated from the white arrow on the display. |
| Backlight | An/Aus | Eingang | (0, 1, 0) | Enables the backlight when receiving an on signal. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Contact Sensor (`pressure_sensor`)

*A sensor activated by contact pressure.*
Setting the resistance property will tune the amount of contact required to depress the sensor. When depressed, an on signal will be produced.

- Größe 1x2x1 Blöcke (voxel [0, 0, 0] .. [0, 1, 0]), Masse 1, Preis 20
- Werte: cable_length=0, cable_radius=0.02, light_intensity=0, logic_gate_type=58, magnet_force=0, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, type=16

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Output | An/Aus | Ausgang | (0, 0, 0) | Outputs an on signal when the contact sensor is depressed. |

## Distance Sensor (`distance_sensor`)

*A laser distance sensor with a maximum measurement range of 500m.*
The reading can be read from the sensor's number output and is measured in metres (1 metre = 4 blocks).

- Größe 1x2x1 Blöcke (voxel [0, 0, 0] .. [0, 1, 0]), Masse 1, Preis 20, Tags: laser,lazer
- Werte: buoy_factor=1.000000, buoy_force=100.000000, buoy_radius=1.000000, constraint_range_of_motion=0.000000, door_lower_limit=-1.000000, door_upper_limit=1.000000, dynamic_min_rotation=0.000000, engine_max_force=1000.000000, force_emitter_max_force=1000.000000, force_emitter_max_vector=1.000000, light_fov=1.000000, light_intensity=0.000000, light_range=1.000000, logic_gate_type=23, magnet_force=0.000000, max_motor_force=100.000000, rudder_surface_area=0.000000, type=16, wheel_radius=0.250000

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Distance | Zahl | Ausgang | (0, 0, 0) | The measured distance in metres. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Fishfinder (`fish_finder`)

*A sensor that returns information about a fish within 100m when submerged.*
This sensor outputs the relative angle, distance and depth to a random detected fish within its range using sound waves when submerged.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 10, Preis 500, Tags: sonar
- Werte: radar_range=100, type=62

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |
| Activate | An/Aus | Eingang | (0, 0, 0) | Enable the Fishfinder. |
| Fish Data | Composite | Ausgang | (0, 0, 0) | Outputs data for a detected fish. On/Off 1: Returns true when a fish is detected. Value 1: The yaw angle between the sensor and the detected fish measured in turns, Value 2: The horizontal distance from the sensor to the detected fish measured in metres, Value 3: The depth from the sensor to the fish measured in metres. |

## Gas Meter (`gas_measure`)

*A device to measure how much gas is within an enclosed volume.*
This will output a quantity in litres and the total capacity in litres.

- Größe 1x2x1 Blöcke (voxel [0, 0, 0] .. [0, 1, 0]), Masse 1, Preis 20
- Werte: logic_gate_subtype=1, type=24, water_component_type=1

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Gas Level | Zahl | Ausgang | (0, 0, 0) | Returns the number of litres of gas in an enclosed volume. |
| Fluid Capacity | Zahl | Ausgang | (0, 1, 0) | Returns the total capacity of an enclosed volume in litres, or 0 if not enclosed. |
| Composite Data | Composite | Ausgang | (0, 0, 0) | Outputs the volumes of individual gas types on their respective channel. The data can be directly merged with a Liquid meter. The Air fluid type is equivalent to the sum of the oxygen, carbon dioxide and nitrogen values. Channels: 4-Air, 5-CO2, 8-Steam, 11-Oxygen, 12-Nitrogen, 13-Hydrogen. |

## GPS Sensor (`gps_sensor`)

*Outputs its x and y world coordinates according to its location on the map.*
The coordinates represent an offset from the centre of the world, measured in metres. You can check the world coordinates of any location by looking at your map.

- Größe 1x1x2 Blöcke (voxel [0, 0, 0] .. [0, 0, 1]), Masse 1, Preis 20
- Werte: buoy_factor=1.000000, buoy_force=100.000000, buoy_radius=1.000000, constraint_range_of_motion=0.000000, door_lower_limit=-1.000000, door_upper_limit=1.000000, dynamic_min_rotation=0.000000, engine_max_force=1000.000000, force_emitter_max_force=1000.000000, force_emitter_max_vector=1.000000, light_fov=1.000000, light_intensity=0.000000, light_range=1.000000, logic_gate_type=30, magnet_force=0.000000, max_motor_force=100.000000, rudder_surface_area=0.000000, type=16, wheel_radius=0.250000

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| X Coordinate | Zahl | Ausgang | (0, 0, 0) | The x coordinate of this component on the world map. |
| Y Coordinate | Zahl | Ausgang | (0, 0, 1) | The y coordinate of this component on the world map. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Humidity Sensor (`humidity_sensor`)

*A humidity sensor for measuring the current fog and visibility meteorological conditions.*
The reading can be read from the sensor's number output and is measured from 0 (no fog) to 1 (max fog).

- Größe 1x2x1 Blöcke (voxel [0, 0, 0] .. [0, 1, 0]), Masse 1, Preis 400
- Werte: cable_radius=0, light_intensity=0, logic_gate_type=39, magnet_force=0, max_motor_speed=5, rudder_surface_area=0, type=16

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Humidity Factor | Zahl | Ausgang | (0, 0, 0) | The level of humidity in the air, relating to the fog visibility. |

## Impact Sensor (`impact_sensor`)

*A sensor activated by a sudden change in velocity.*
Setting the impact threshold property will tune the sensitivity for impacts. When the instant change in velocity from an impact exceeds the threshold, an on signal is produced.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 20
- Werte: cable_length=0, cable_radius=0.02, light_intensity=0, logic_gate_type=57, magnet_force=0, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, type=16

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Output | An/Aus | Ausgang | (0, 0, 0) | Outputs an on signal when instant change in velocity exceeds the impact threshold. |

## Laser Distance Sensor (`laser_distance_sensor`)

*A laser distance sensor with a maximum measurement range of 4000m.*
The reading can be read from the sensor's number output and is measured in metres (1 metre = 4 blocks). Can be pivoted up to 0.125 turns using composite input.

- Größe 1x4x1 Blöcke (voxel [0, 0, 0] .. [0, 3, 0]), Masse 1, Preis 100
- Werte: logic_gate_type=23, rudder_surface_area=0, type=16

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Distance | Zahl | Ausgang | (0, 0, 0) | The measured distance in metres. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |
| Active | An/Aus | Eingang | (0, 1, 0) | Controls whether or not the laser is active. |
| Wavelength | Zahl | Eingang | (0, 2, 0) | The specific light wavelength to emit (whole number). |
| Pivot | Composite | Eingang | (0, 2, 0) | Inputs for laser X/Y pivot. (Value 1 : Pivot X) (Value 2 : Pivot Y) |

## Laser Point Sensor (`laser_point_sensor`)

*A sensor that outputs a relative x and y position of a laser point that it can see within its field of view.*
The closest point to the center of the sensor's field of view will be reported. It outputs a value of -1 to 1 on composite number channel 1 for the x position, and a value of -1 to 1 on composite number channel 2 for the y position. Composite on/off channel 1 is set to on when a point is visible. The -1 to 1 values map to an fov of -cos(0.5) to cos(0.5) in both the x and y directions.

- Größe 1x3x1 Blöcke (voxel [0, 0, 0] .. [0, 2, 0]), Masse 2, Preis 100
- Werte: cable_radius=0.02, light_intensity=0, logic_gate_type=48, magnet_force=0, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, type=16

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |
| Data Output | Composite | Ausgang | (0, 1, 0) | On/Off channel 1: is laser detected. Number channel 1, 2: X, Y position within the sensors 120 degree field of view. |
| Wavelength | Zahl | Eingang | (0, 0, 0) | The specific light wavelength to detect (whole number). |

## Laser Sensor (Missile) (`radar_advanced_missile_laser`)

*A short range sensor that returns information about detected laser points within its view.*
This sensor is designed for missiles and acts along the Z axis, with an output node that passes data to course correct linked rocket fin components toward the closest target. The sensor also outputs data for up to 8 detected laser points.

- Größe 1x2x1 Blöcke (voxel [0, 0, 0] .. [0, 1, 0]), Masse 5, Preis 800
- Werte: logic_gate_type=50, radar_range=5000, radar_speed=0.03, radar_type=2, rudder_surface_area=0, type=56

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |
| Activate | An/Aus | Eingang | (0, 0, 0) | Enable the Laser Sensor. |
| Sensor Data | Composite | Ausgang | (0, 0, 0) | Outputs data for up to 8 targets. On/Off 1-8 : Target 1 Found, Target 2 Found, etc... Values 1-32 : Target 1 Distance, Target 1 Azimuth Angle, Target 1 Elevation Angle, Target 1 Time Since Detection, Target 2 Distance, Target 2 Azimuth Angle, Target 2 Elevation Angle, Target 2 Time Since Detection, etc... |
| Missile Output | Composite | Ausgang | (0, 1, 0) | Outputs yaw and pitch rotations toward the most immediate target. (Value 1 : Yaw) (Value 2 : Pitch). Link this directly into a rocket fins component. |
| Wavelength | Zahl | Eingang | (0, 1, 0) | The specific light wavelength to detect (whole number). |

## Linear Speed Sensor (`linear_speed_sensor`)

*This sensor outputs its current linear speed in m/s, allowing you to measure how fast your vehicle is travelling.*
This sensor outputs the speed of the component in one of 4 modes. Modes can be changed by selecting the sensor.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 20
- Werte: buoy_factor=1.000000, buoy_force=100.000000, buoy_radius=1.000000, constraint_range_of_motion=0.000000, door_lower_limit=-1.000000, door_upper_limit=1.000000, dynamic_min_rotation=0.000000, engine_max_force=1000.000000, force_emitter_max_force=1000.000000, force_emitter_max_vector=1.000000, light_fov=1.000000, light_intensity=0.000000, light_range=1.000000, logic_gate_type=19, magnet_force=0.000000, max_motor_force=100.000000, rudder_surface_area=0.000000, type=16, wheel_radius=0.250000

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Linear Speed | Zahl | Ausgang | (0, 0, 0) | The sensor's linear speed in m/s. |

## Liquid Meter (`water_measure`)

*A device to measure how much liquid is within an enclosed volume.*
This will output a quantity in litres and the total capacity in litres. If not inside an enclosed volume, it will give the height relative to the water surface.

- Größe 1x2x1 Blöcke (voxel [0, 0, 0] .. [0, 1, 0]), Masse 1, Preis 20, Tags: fluid,measure
- Werte: type=24, water_component_type=1

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Liquid Level | Zahl | Ausgang | (0, 0, 0) | Returns the number of litres of liquid in an enclosed volume, or height relative to water if not enclosed. |
| Fluid Capacity | Zahl | Ausgang | (0, 1, 0) | Returns the total capacity of an enclosed volume in litres, or 0 if not enclosed. |
| Composite Data | Composite | Ausgang | (0, 0, 0) | Outputs the volumes of individual liquid types on their respective channel. The data can be directly merged with a Gas meter. Channels: 1-Water, 2-Diesel, 3-Jet Fuel, 6-Oil, 7-Seawater, 9-Slurry, 10-Saturated Slurry |

## Microphone (`mic`)

*A microphone for transmitting player voice data.*
A simple microphone that picks up voice data from nearby players. (Range : 15)

- Größe 1x2x1 Blöcke (voxel [0, 0, 0] .. [0, 1, 0]), Masse 1, Preis 250
- Werte: cable_radius=0.02, light_intensity=0, logic_gate_type=51, magnet_force=0, max_motor_speed=5, pump_pressure=0, radar_range=5000, rudder_surface_area=0, type=16

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Audio | Ton | Ausgang | (0, 0, 0) | Audio data connection. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |
| Activate | An/Aus | Eingang | (0, 0, 0) | Activate the microphone. |
| Transmit | An/Aus | Ausgang | (0, 1, 0) | If the microphone is currently transmitting. |

## Physics Sensor (`physics_sensor`)

*Sensor component that outputs various physics measurements such as position and velocity.*
Outputs physics information to a composite logic node. Requires Electric for GPS position functionality. This component is directed along its local Y axis.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 20
- Werte: logic_gate_type=61, type=16

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Composite Output | Composite | Ausgang | (0, 0, 0) | Outputs [1] x position, [2] y position, [3] z position, [4] euler rotation x, [5] euler rotation y, [6] euler rotation z, [7] linear velocity x, [8] linear velocity y, [9] linear velocity z, [10] angular velocity x, [11] angular velocity y, [12] angular velocity z, [13] absolute linear velocity, [14] absolute angular velocity, [15] local z tilt, [16] local x tilt and [17] compass heading (-0.5 to 0.5) to the respective composite channels. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Player Sensor (`player_sensor`)

*A sensor that outputs the number of players detected within an area.*
If the sensor is facing into a sealed room, only players inside that room will be detected. Likewise, players inside sealed rooms will not be detected if the sensor is placed on the outside. The size of the area and types of players to detect can be changed by selecting this component with the select tool.

- Größe 1x2x1 Blöcke (voxel [0, 0, 0] .. [0, 1, 0]), Masse 1, Preis 50
- Werte: cable_radius=0.02, light_intensity=0, logic_gate_type=47, magnet_force=0, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, type=16

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Number Detected | Zahl | Ausgang | (0, 1, 0) | The number of players detected by the sensor. |
| Detected | An/Aus | Ausgang | (0, 0, 0) | Outputs an on signal if any players are detected. |

## Radar (`radar`)

*A short range Radar that returns information about a detected object within its view.*
This sensor outputs the distance and angle to a detected object within its range and field of view using radio waves. (Range : 5000) (Max FOV : 0.125)

- Größe 3x1x3 Blöcke (voxel [-1, 0, -1] .. [1, 0, 1]), Masse 10, Preis 1000
- Werte: cable_radius=0.02, light_intensity=0, logic_gate_type=50, magnet_force=0, max_motor_speed=5, pump_pressure=0, radar_range=5000, rudder_surface_area=0, type=16

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| FOV | Zahl | Eingang | (0, 0, 1) | The sensor's yaw field of view in turns from 0.01 to 0.125. |
| Facing Yaw | Zahl | Eingang | (1, 0, 0) | The sensor's yaw direction in turns from -0.5 to 0.5. |
| Target Distance | Zahl | Ausgang | (-1, 0, 0) | The distance to the target in meters. |
| Signal Strength | Zahl | Ausgang | (-1, 0, 1) | The strength of the returned signal. |
| Elevation Angle | Zahl | Ausgang | (0, 0, -1) | The pitch angle between the sensor and the target in turns. |
| Target Found | An/Aus | Ausgang | (0, 0, 0) | Returns if an object has been detected. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Radar (AWACS) (`radar_advanced_awacs`)

*A long range radar that returns information about a detected object within its view.*
This sensor outputs the distance and relative angle to a detected object within its range and field of view using radio waves. Sensitivity is based on FOV, target size, and distance.

- Größe 37x5x37 Blöcke (voxel [-18, -2, -18] .. [18, 2, 18]), Masse 1100, Preis 10000
- Werte: logic_gate_type=50, radar_range=500000, radar_speed=0.015, rudder_surface_area=0, type=56

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |
| Activate | An/Aus | Eingang | (0, 0, 0) | Enable the Radar. |
| Radar Data | Composite | Ausgang | (0, 0, 0) | Outputs data for up to 8 targets. On/Off 1-8 : Target 1 Found, Target 2 Found, etc... Values 1-32 : Target 1 Distance, Target 1 Azimuth Angle, Target 1 Elevation Angle, Target 1 Time Since Detection, Target 2 Distance, Target 2 Azimuth Angle, Target 2 Elevation Angle, Target 2 Time Since Detection, etc... |
| Radar Rotation | Zahl | Ausgang | (0, -1, 0) | Current radar rotation from forward in turns. |
| Gimbal Input | Composite | Eingang | (0, 1, 0) | Inputs rotation data for radar in manual mode. Value 1: The yaw angle of the radar measured in turns, Value 2: The pitch angle of the radar measured in turns from -0.125 to 0.125. |

## Radar (Basic) (`radar_advanced`)

*A radar that returns information about a detected object within its view.*
This sensor outputs the distance and relative angle to a detected object within its range and field of view using radio waves. Sensitivity is based on FOV, target size, and distance.

- Größe 3x1x3 Blöcke (voxel [-1, 0, -1] .. [1, 0, 1]), Masse 10, Preis 1000
- Werte: cable_radius=0.02, light_intensity=0, logic_gate_type=50, magnet_force=0, max_motor_speed=5, pump_pressure=0, radar_range=60000, radar_speed=0.04, rudder_surface_area=0, type=56

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |
| Activate | An/Aus | Eingang | (0, 0, 0) | Enable the Radar. |
| Radar Data | Composite | Ausgang | (0, 0, 0) | Outputs data for up to 8 targets. On/Off 1-8 : Target 1 Found, Target 2 Found, etc... Values 1-32 : Target 1 Distance, Target 1 Azimuth Angle, Target 1 Elevation Angle, Target 1 Time Since Detection, Target 2 Distance, Target 2 Azimuth Angle, Target 2 Elevation Angle, Target 2 Time Since Detection, etc... |
| Radar Rotation | Zahl | Ausgang | (1, 0, 0) | Current radar rotation from forward in turns. |
| Gimbal Input | Composite | Eingang | (-1, 0, 0) | Inputs rotation data for radar in manual mode. Value 1: The yaw angle of the radar measured in turns, Value 2: The pitch angle of the radar measured in turns from -0.125 to 0.125. |

## Radar (Dish) (`radar_advanced_dish`)

*A radar that returns information about a detected object within its view.*
This sensor outputs the distance and relative angle to a detected object within its range and field of view using radio waves. Sensitivity is based on FOV, target size, and distance.

- Größe 19x10x20 Blöcke (voxel [-9, -1, -10] .. [9, 8, 9]), Masse 550, Preis 5000
- Werte: cable_radius=0.02, light_intensity=0, logic_gate_type=50, magnet_force=0, max_motor_speed=5, pump_pressure=0, radar_range=200000, radar_speed=0.02, rudder_surface_area=0, type=56

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |
| Activate | An/Aus | Eingang | (0, 0, 0) | Enable the Radar. |
| Radar Data | Composite | Ausgang | (0, 0, 0) | Outputs data for up to 8 targets. On/Off 1-8 : Target 1 Found, Target 2 Found, etc... Values 1-32 : Target 1 Distance, Target 1 Azimuth Angle, Target 1 Elevation Angle, Target 1 Time Since Detection, Target 2 Distance, Target 2 Azimuth Angle, Target 2 Elevation Angle, Target 2 Time Since Detection, etc... |
| Radar Rotation | Zahl | Ausgang | (0, 1, 0) | Current radar rotation from forward in turns. |
| Gimbal Input | Composite | Eingang | (0, 2, 0) | Inputs rotation data for radar in manual mode. Value 1: The yaw angle of the radar measured in turns, Value 2: The pitch angle of the radar measured in turns from -0.125 to 0.125. |

## Radar (Dish) (`radar_dish`)

*A medium range, fixed rotation Radar that returns information about a detected object within its view.*
This fixed sensor outputs the distance and angle to a detected object within its range and field of view using radio waves. (Range : 20000) (Max FOV : 0.125)

- Größe 21x10x11 Blöcke (voxel [-10, 0, -2] .. [10, 9, 8]), Masse 150, Preis 3000
- Werte: cable_radius=0.02, light_intensity=0, logic_gate_type=50, magnet_force=0, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, type=16

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| FOV | Zahl | Eingang | (0, 0, 1) | The sensor's yaw field of view in turns from 0.01 to 0.125. |
| Target Distance | Zahl | Ausgang | (-1, 0, 0) | The distance to the target in meters. |
| Signal Strength | Zahl | Ausgang | (-1, 0, 1) | The strength of the returned signal. |
| Elevation Angle | Zahl | Ausgang | (0, 0, -1) | The pitch angle between the sensor and the target in turns. |
| Target Found | An/Aus | Ausgang | (0, 0, 0) | Returns if an object has been detected. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Radar (Huge) (`radar_huge`)

*A long range, multi-target Radar that returns detailed information through composite channels about detected objects within its view.*
This sensor outputs the distance and relative angles to up to 8 detected objects within its range and field of view using radio waves and outputs all detected targets through composite channels. (Range : 50000) (Max FOV : 0.125)

- Größe 37x5x37 Blöcke (voxel [-18, 0, -18] .. [18, 4, 18]), Masse 1100, Preis 10000
- Werte: cable_radius=0.02, light_intensity=0, logic_gate_subtype=3, logic_gate_type=50, magnet_force=0, max_motor_speed=5, pump_pressure=0, radar_range=50000, rudder_surface_area=0, type=16

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| FOV | Zahl | Eingang | (0, 0, 1) | The sensor's yaw field of view in turns from 0.01 to 0.125. |
| Facing Yaw | Zahl | Eingang | (1, 0, 0) | The sensor's yaw direction in turns from -0.5 to 0.5. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |
| Radar Data | Composite | Ausgang | (0, 0, 0) | Outputs data for up to 8 targets. On/Off 1-8 : Target 1 Found, Target 2 Found, etc... Values 1-32 : Target 1 Distance, Target 1 Azimuth Angle, Target 1 Elevation Angle, Target 1 Time Since Detection, Target 2 Distance, Target 2 Azimuth Angle, Target 2 Elevation Angle, Target 2 Time Since Detection, etc... |

## Radar (Large) (`radar_large`)

*A medium range, highly configurable Radar that returns detailed information about a detected object within its view.*
This sensor outputs the distance and relative angles to a detected object within its range and field of view using radio waves. This sensor uniquely allows the changing of it's pitch direction. (Range : 20000) (Max FOV : 0.250)

- Größe 7x16x7 Blöcke (voxel [-3, 0, -3] .. [3, 15, 3]), Masse 300, Preis 5000
- Werte: cable_radius=0.02, light_intensity=0, logic_gate_subtype=2, logic_gate_type=50, magnet_force=0, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, type=16

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| FOV | Zahl | Eingang | (0, 0, 1) | The sensor's yaw and pitch field of view in turns from 0.01 to 0.125. |
| Facing Yaw | Zahl | Eingang | (1, 0, 0) | The sensor's yaw direction in turns from -0.5 to 0.5. |
| Facing Pitch | Zahl | Eingang | (1, 0, 1) | The sensor's pitch direction in turns from -0.25 to 0.25. |
| Target Distance | Zahl | Ausgang | (-1, 0, 0) | The distance to the target in meters. |
| Signal Strength | Zahl | Ausgang | (-1, 0, 1) | The strength of the returned signal. |
| Elevation Angle | Zahl | Ausgang | (0, 0, -1) | The pitch angle between the sensor and the target in turns. |
| Azimuth Angle | Zahl | Ausgang | (-1, 0, -1) | The yaw angle between the sensor and the target in turns. |
| Target Found | An/Aus | Ausgang | (0, 0, 0) | Returns if an object has been detected. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Radar (Missile) (`radar_advanced_missile`)

*A short range radar that returns information about a detected object within its view.*
This sensor outputs the distance and relative angle to a detected object within its range and field of view using radio waves. This sensor is designed for missiles and its radar acts along the Z axis. Sensitivity is based on FOV, target size, and distance.

- Größe 1x2x1 Blöcke (voxel [0, 0, 0] .. [0, 1, 0]), Masse 5, Preis 800
- Werte: cable_radius=0.02, light_intensity=0, logic_gate_type=50, magnet_force=0, max_motor_speed=5, pump_pressure=0, radar_speed=0.03, radar_type=1, rudder_surface_area=0, type=56

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |
| Activate | An/Aus | Eingang | (0, 0, 0) | Enable the Radar. |
| Radar Data | Composite | Ausgang | (0, 0, 0) | Outputs data for up to 8 targets. On/Off 1-8 : Target 1 Found, Target 2 Found, etc... Values 1-32 : Target 1 Distance, Target 1 Azimuth Angle, Target 1 Elevation Angle, Target 1 Time Since Detection, Target 2 Distance, Target 2 Azimuth Angle, Target 2 Elevation Angle, Target 2 Time Since Detection, etc... |
| Missile Output | Composite | Ausgang | (0, 1, 0) | Outputs yaw and pitch rotations toward the most immediate target. (Value 1 : Yaw) (Value 2 : Pitch). Link this directly into a rocket fins component. |
| Radar Rotation | Zahl | Ausgang | (0, 1, 0) | Current radar rotation from forward in turns. |

## Radar (Phalanx) (`radar_advanced_phalanx`)

*A radar that returns information about a detected object within its view.*
This sensor outputs the distance and relative angle to a detected object within its range and field of view using radio waves. Sensitivity is based on FOV, target size, and distance.

- Größe 3x3x3 Blöcke (voxel [-1, 0, -1] .. [1, 2, 1]), Masse 55, Preis 2000
- Werte: cable_radius=0.02, light_intensity=0, logic_gate_type=50, magnet_force=0, max_motor_speed=5, pump_pressure=0, radar_range=100000, radar_speed=0.03, rudder_surface_area=0, type=56

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |
| Activate | An/Aus | Eingang | (0, 0, 0) | Enable the Radar. |
| Radar Data | Composite | Ausgang | (0, 0, 0) | Outputs data for up to 8 targets. On/Off 1-8 : Target 1 Found, Target 2 Found, etc... Values 1-32 : Target 1 Distance, Target 1 Azimuth Angle, Target 1 Elevation Angle, Target 1 Time Since Detection, Target 2 Distance, Target 2 Azimuth Angle, Target 2 Elevation Angle, Target 2 Time Since Detection, etc... |
| Radar Rotation | Zahl | Ausgang | (0, 1, 0) | Current radar rotation from forward in turns. |
| Gimbal Input | Composite | Eingang | (0, 2, 0) | Inputs rotation data for radar in manual mode. Value 1: The yaw angle of the radar measured in turns, Value 2: The pitch angle of the radar measured in turns from -0.125 to 0.125. |

## Radar Detector (`radar_detector`)

*A sensor that can detect radar waves.*
This sensor outputs an On signal when it detects a radio wave.

- Größe 1x2x1 Blöcke (voxel [0, 0, 0] .. [0, 1, 0]), Masse 1, Preis 1000
- Werte: cable_radius=0.02, light_intensity=0, logic_gate_type=56, magnet_force=0, max_motor_speed=5, pump_pressure=0, radar_range=5000, rudder_surface_area=0, type=16

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Detected | An/Aus | Ausgang | (0, 0, 0) | Returns an On signal when it detects a radio wave. |

## Radiation Detector (`radiation_detector`)

*A sensor to detect radiation.*
Outputs radiation dose rate per second at its location.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 250, Tags: geiger,radiation
- Werte: cable_radius=0.02, light_intensity=0, logic_gate_type=59, magnet_force=0, max_motor_speed=5, pump_pressure=0, radar_range=5000, rudder_surface_area=0, type=16

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Radiation | Zahl | Ausgang | (0, 0, 0) | The detected radiation dose rate. |

## Rain Sensor (`rain_sensor`)

*A rain sensor for measuring the current meteorological conditions.*
The reading can be read from the sensor's number output and is measured from 0 (no rain) to 1 (max rain).

- Größe 1x2x1 Blöcke (voxel [0, 0, 0] .. [0, 1, 0]), Masse 1, Preis 180
- Werte: cable_radius=0, light_intensity=0, logic_gate_type=40, magnet_force=0, max_motor_speed=5, rudder_surface_area=0, type=16

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Rain Factor | Zahl | Ausgang | (0, 0, 0) | The amount of current rain fall from 0 to 1. |

## Sonar (Large) (`radar_sonar`)

*A short range Sonar that returns information about a detected underwater object within its view.*
This sensor outputs the distance and angle to a detected underwater object within its range and field of view using sound waves. (Range : 3000) (Max FOV : 0.125)

- Größe 7x2x7 Blöcke (voxel [-3, 0, -3] .. [3, 1, 3]), Masse 25, Preis 1000
- Werte: cable_radius=0.02, light_intensity=0, logic_gate_subtype=1, logic_gate_type=50, magnet_force=0, max_motor_speed=5, pump_pressure=0, radar_range=3000, rudder_surface_area=0, type=16

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| FOV | Zahl | Eingang | (0, 0, 1) | The sensor's yaw field of view in turns from 0.01 to 0.125. |
| Facing Yaw | Zahl | Eingang | (1, 0, 0) | The sensor's yaw direction in turns from -0.5 to 0.5. |
| Target Distance | Zahl | Ausgang | (-1, 0, 0) | The distance to the target in meters. |
| Signal Strength | Zahl | Ausgang | (-1, 0, 1) | The strength of the returned signal. |
| Elevation Angle | Zahl | Ausgang | (0, 0, -1) | The pitch angle between the sensor and the target in turns. |
| Target Found | An/Aus | Ausgang | (0, 0, 0) | Returns if an object has been detected. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Sonar (Large) (`sonar_advanced_7`)

*A sonar that returns information about a detected objects within 200km.*
This sensor outputs the relative angle to detected objects within its range using underwater sound waves. The sensor will passively detect certain noisy components such as propellers or engines but can also send out a loud ping to detect quiet underwater bodies. While the ping input is held passive signals will be supressed. After activating a ping additional detected signals will appear momentarily in the data channel as the signal returns to the sonar. Activating another ping will override the previous ping and no further data will be returned from the old signal.

- Größe 7x5x7 Blöcke (voxel [-3, -2, -3] .. [3, 2, 3]), Masse 200, Preis 4000
- Werte: logic_gate_type=50, radar_range=200000, radar_speed=0.04, rudder_surface_area=0, type=57

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |
| Activate | An/Aus | Eingang | (0, 0, 0) | Enable the Sonar. |
| Ping | An/Aus | Eingang | (1, 0, 0) | Send a ping and listen for return sounds. |
| Sonar Data | Composite | Ausgang | (0, 0, 0) | Outputs data for up to 16 targets. On/Off 1-16 : Target 1 Found, Target 2 Found, Etc... Values 1-32: Target 1 Pivot, Target 1 Pitch, Target 2 Pivot, Target 2 Pitch, Etc... |

## Sonar (Medium) (`sonar_advanced_5`)

*A sonar that returns information about a detected objects within 100km.*
This sensor outputs the relative angle to detected objects within its range using underwater sound waves. The sensor will passively detect certain noisy components such as propellers or engines but can also send out a loud ping to detect quiet underwater bodies. While the ping input is held passive signals will be supressed. After activating a ping additional detected signals will appear momentarily in the data channel as the signal returns to the sonar. Activating another ping will override the previous ping and no further data will be returned from the old signal.

- Größe 5x3x5 Blöcke (voxel [-2, -1, -2] .. [2, 1, 2]), Masse 50, Preis 2000
- Werte: logic_gate_type=50, radar_range=100000, radar_speed=0.04, rudder_surface_area=0, type=57

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |
| Activate | An/Aus | Eingang | (0, 0, 0) | Enable the Sonar. |
| Ping | An/Aus | Eingang | (1, 0, 0) | Send a ping and listen for return sounds. |
| Sonar Data | Composite | Ausgang | (0, 0, 0) | Outputs data for up to 16 targets. On/Off 1-16 : Target 1 Found, Target 2 Found, Etc... Values 1-32: Target 1 Pivot, Target 1 Pitch, Target 2 Pivot, Target 2 Pitch, Etc... |

## Sonar (Small) (`radar_sonar_small`)

*A short range Sonar that returns information about a detected underwater object within its view.*
This sensor outputs the distance and angle to a detected underwater object within its range and field of view using sound waves. (Range : 1000) (Max FOV : 0.125)

- Größe 3x1x3 Blöcke (voxel [-1, 0, -1] .. [1, 0, 1]), Masse 10, Preis 1000
- Werte: cable_radius=0.02, light_intensity=0, logic_gate_subtype=1, logic_gate_type=50, magnet_force=0, max_motor_speed=5, pump_pressure=0, radar_range=1000, rudder_surface_area=0, type=16

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| FOV | Zahl | Eingang | (0, 0, 1) | The sensor's yaw field of view in turns from 0.01 to 0.125. |
| Facing Yaw | Zahl | Eingang | (1, 0, 0) | The sensor's yaw direction in turns from -0.5 to 0.5. |
| Target Distance | Zahl | Ausgang | (-1, 0, 0) | The distance to the target in meters. |
| Signal Strength | Zahl | Ausgang | (-1, 0, 1) | The strength of the returned signal. |
| Elevation Angle | Zahl | Ausgang | (0, 0, -1) | The pitch angle between the sensor and the target in turns. |
| Target Found | An/Aus | Ausgang | (0, 0, 0) | Returns if an object has been detected. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Sonar (Small) (`sonar_advanced`)

*A sonar that returns information about a detected objects within 60km.*
This sensor outputs the relative angle to detected objects within its range using underwater sound waves. The sensor will passively detect certain noisy components such as propellers or engines but can also send out a loud ping to detect quiet underwater bodies. While the ping input is held passive signals will be supressed. After activating a ping additional detected signals will appear momentarily in the data channel as the signal returns to the sonar. Activating another ping will override the previous ping and no further data will be returned from the old signal.

- Größe 3x1x3 Blöcke (voxel [-1, 0, -1] .. [1, 0, 1]), Masse 10, Preis 1000
- Werte: logic_gate_type=50, radar_range=60000, radar_speed=0.04, rudder_surface_area=0, type=57

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |
| Activate | An/Aus | Eingang | (0, 0, 0) | Enable the Sonar. |
| Ping | An/Aus | Eingang | (1, 0, 0) | Send a ping and listen for return sounds. |
| Sonar Data | Composite | Ausgang | (0, 0, 0) | Outputs data for up to 16 targets. On/Off 1-16 : Target 1 Found, Target 2 Found, Etc... Values 1-32: Target 1 Pivot, Target 1 Pitch, Target 2 Pivot, Target 2 Pitch, Etc... |
| Torpedo Output | Composite | Ausgang | (1, 0, 0) | Outputs x and y data for the most immediate target. Link this directly into a rocket fins component. |

## Temperature Probe (`temperature_probe`)

*A sensor to determine temperature.*
A sensor that outputs the current temperature of an enclosed space in Celcius, if not within an enclosed volume it outputs the ambient air temperature at its location.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 250
- Werte: cable_radius=0.02, light_intensity=0, logic_gate_type=53, magnet_force=0, max_motor_speed=5, pump_pressure=0, radar_range=5000, rudder_surface_area=0, type=16

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Temperature | Zahl | Ausgang | (0, 0, 0) | The detected temperature in degrees. |

## Tilt Sensor (`rotation_sensor`)

*A sensor that measures how much it has tilted, relative to the horizon.*
The measurement is expressed in terms of turns, with an output range of -0.25 to 0.25 turns. A value of zero points towards the horizon.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 20
- Werte: buoy_factor=1.000000, buoy_force=100.000000, buoy_radius=1.000000, constraint_range_of_motion=0.000000, door_lower_limit=-1.000000, door_upper_limit=1.000000, dynamic_min_rotation=0.000000, engine_max_force=1000.000000, force_emitter_max_force=1000.000000, force_emitter_max_vector=1.000000, light_fov=1.000000, light_intensity=0.000000, light_range=1.000000, logic_gate_type=20, magnet_force=0.000000, max_motor_force=100.000000, rudder_surface_area=0.000000, type=16, wheel_radius=0.250000

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Tilt | Zahl | Ausgang | (0, 0, 0) | The measured tilt relative to the horizon. |

## Transponder Locator (`transponder_locator`)

*An emergency search and rescue transponder locator.*
Detects all transponder signals over great distances. Outputs the strongest signal strength detected, transponder signal strengths will decrease with distance.

- Größe 1x2x1 Blöcke (voxel [0, 0, 0] .. [0, 1, 0]), Masse 1, Preis 20, Tags: basic,mission
- Werte: cable_length=0, cable_radius=0.02, light_intensity=0, logic_gate_type=55, magnet_force=0, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, type=16

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Transponder Pulse | An/Aus | Ausgang | (0, 1, 0) | Emits a periodic boolean pulse, with a frequency determined by the distance to the nearest transponder signal. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |
| Active | An/Aus | Eingang | (0, 0, 0) | Detects any transponder signals when active. |

## Wind Sensor (`wind_sensor`)

*A wind sensor for measuring relative wind speed and direction.*
The sensor outputs the wind direction relative to the orientation of the base of the sensor (in number of turns from -0.5 to 0.5) and the wind speed in m/s. Wind data is relative to the speed of the sensor and only measures wind in the plane of the sensor.

- Größe 1x2x1 Blöcke (voxel [0, 0, 0] .. [0, 1, 0]), Masse 1, Preis 200
- Werte: cable_radius=0, light_intensity=0, logic_gate_type=41, magnet_force=0, max_motor_speed=5, rudder_surface_area=0, type=16

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Wind Speed | Zahl | Ausgang | (0, 0, 0) | The relative wind velocity. |
| Wind Direction | Zahl | Ausgang | (0, 1, 0) | The direction of the wind relative to the component. |
