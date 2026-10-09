# Spezialausruestung (Kategorie 4)

Aus den Spieldaten erzeugt von `tools/bauteile_holen.py` - nicht von Hand ändern.

## Bed (`seat_bed`)

*A bed.*
You can get in and out of the bed by interacting with it using [$[action_use_seat]]. You can place a rescued survivor in any bed by using [$[action_use_seat]] while carrying them.

- Größe 3x4x7 Blöcke (voxel [-1, 0, -3] .. [1, 3, 3]), Masse 20, Preis 250, Tags: basic
- Werte: button_type=0, cable_radius=0, constraint_axis=0, door_lower_limit=0, door_upper_limit=0, dynamic_max_rotation=0, light_fov=0, light_intensity=0, light_range=0, magnet_force=0, max_motor_force=0, max_motor_speed=5, rudder_surface_area=0, seat_pose=3, type=1, wheel_radius=0

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Occupied | An/Aus | Ausgang | (0, 0, 0) | Outputs an on signal if this bed is occupied by a character. |

## Buoyancy Float Block (`buoyancy_float_block`)

*A block-shaped buoyant float.*

- Größe 4x4x4 Blöcke (voxel [-1, -1, -1] .. [2, 2, 2]), Masse 1, Preis 50, Tags: basic
- Werte: buoy_factor=0.5, buoy_radius=0.75, cable_radius=0, rudder_surface_area=0, type=3

## Buoyancy Float Pyramid (`buoyancy_float_pyramid`)

*A pyramid-shaped buoyant float.*

- Größe 4x4x4 Blöcke (voxel [-1, -1, -1] .. [2, 2, 2]), Masse 1, Preis 50, Tags: basic
- Werte: buoy_factor=0.5, buoy_radius=0.75, cable_radius=0, rudder_surface_area=0, type=3

## Buoyancy Float Wedge (`buoyancy_float_wedge`)

*A wedge-shaped buoyant float.*

- Größe 4x4x4 Blöcke (voxel [-1, -1, -1] .. [2, 2, 2]), Masse 1, Preis 50, Tags: basic
- Werte: buoy_factor=0.5, buoy_radius=0.75, cable_radius=0, rudder_surface_area=0, type=3

## Camera Gimbal (`camera_gimbal`)

*A gimbal camera with video output feed.*
Has an infrared mode as well as pivot controls, a variable field of view.

- Größe 3x3x3 Blöcke (voxel [-1, 0, -1] .. [1, 2, 1]), Masse 50, Preis 5000
- Werte: cable_length=0, camera_fov_max=0.025, camera_fov_min=2.2, type=42

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Camera Feed | Video | Ausgang | (0, 0, 0) |  |
| Electric | Strom | Eingang | (0, 0, 0) |  |
| Infrared Mode | An/Aus | Eingang | (0, 0, 0) | Controls whether or not the infrared mode is switched on. |
| Field of View | Zahl | Eingang | (0, 1, 0) | Controls the level of zoom of the camera. |
| Pivot Rotation | Zahl | Eingang | (-1, 2, 0) | Controls the rotation of the camera base. |
| Pitch Rotation | Zahl | Eingang | (1, 2, 0) | Controls the rotation of the camera head. |

## Camera Medium (`camera_med`)

*A camera with video output feed.*
Has infrared mode as well as variable field of view. Can be pivoted up to 0.125 turns using composite input.

- Größe 1x2x1 Blöcke (voxel [0, 0, 0] .. [0, 1, 0]), Masse 10, Preis 3000
- Werte: camera_fov_max=0.025, camera_fov_min=2.2, type=42

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Camera Feed | Video | Ausgang | (0, 0, 0) |  |
| Electric | Strom | Eingang | (0, 0, 0) |  |
| Infrared Mode | An/Aus | Eingang | (0, 0, 0) | Controls whether or not the infrared mode is switched on. |
| Field of View | Zahl | Eingang | (0, 1, 0) | Controls the level of zoom of the camera. |
| Pivot | Composite | Eingang | (0, 0, 0) | Inputs for camera X/Y pivot. (Value 1 : Pivot X) (Value 2 : Pivot Y) |

## Camera Small (`camera_small`)

*A camera with video output feed.*
Can be pivoted up to 0.125 turns using composite input.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 5, Preis 1000
- Werte: type=42

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Camera Feed | Video | Ausgang | (0, 0, 0) |  |
| Electric | Strom | Eingang | (0, 0, 0) |  |
| Pivot | Composite | Eingang | (0, 0, 0) | Inputs for camera X/Y pivot. (Value 1 : Pivot X) (Value 2 : Pivot Y) |

## Camera Stabilized (`camera_gimbal_laser`)

*A stabilized gimbal camera with video output feed.*
Has an infrared mode, variable field of view, stabilized and tracking modes.

- Größe 3x3x3 Blöcke (voxel [-1, 0, -1] .. [1, 2, 1]), Masse 60, Preis 50000, Tags: laser,lazer
- Werte: cable_length=0, camera_fov_max=0.025, camera_fov_min=2.2, type=42

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Camera Feed | Video | Ausgang | (0, 0, 0) |  |
| Electric | Strom | Eingang | (0, 0, 0) |  |
| Infrared Mode | An/Aus | Eingang | (0, 0, 0) | Controls whether or not the infrared mode is switched on. |
| Enable Laser | An/Aus | Eingang | (0, 2, 0) | Enables the Laser. |
| Field of View | Zahl | Eingang | (0, 1, 0) | Controls the level of zoom of the camera. |
| Pivot Rotation | Zahl | Eingang | (-1, 2, 0) | Controls the rotation of the camera base. |
| Pitch Rotation | Zahl | Eingang | (1, 2, 0) | Controls the rotation of the camera head. |
| Laser Distance | Zahl | Ausgang | (-1, 1, 0) | The measured distance in meters. |
| Stabilizer Mode | An/Aus | Eingang | (1, 1, 0) | Enable stabilization to keep the camera focused in its current direction. |
| Tracker Mode | An/Aus | Eingang | (1, 0, 0) | Enable tracking to direct the camera at the current lazed position. |
| Composite Output | Composite | Ausgang | (-1, 0, 0) | Composite value channels: 1: x position of laser target, 2: y position of laser target, 3: z position of laser target, 4: pitch of component in turns, 5: yaw of component in turns |
| Laser Wavelength | Zahl | Eingang | (0, 0, -1) | The specific light wavelength to emit (whole number). |

## Electric Cable Pulley (`winch_pulley_cable`)

*A pulley that changes attached cable lengths based on forces applied to cables.*
Draw a rope logic link between two rope nodes to form a cable. Cables will slide based on difference in force applied to each cable.

- Größe 3x1x3 Blöcke (voxel [-1, 0, -1] .. [1, 0, 1]), Masse 25, Preis 250, Tags: basic
- Werte: cable_length=150, cable_radius=0.05, logic_gate_subtype=9, type=48
- Zweiter Körper (Gelenk) bei [0, 3, 2]

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Rope 1 Length | Zahl | Ausgang | (1, 0, 0) | The current length of rope 1 in metres. |
| Rope 2 Length | Zahl | Ausgang | (-1, 0, 0) | The current length of rope 2 in metres. |
| Rope 2 | Seil/Munition | Eingang | (-1, 0, 1) |  |
| Rope 1 | Seil/Munition | Eingang | (1, 0, 1) |  |

## Electric Cable Pulley (Corner) (`winch_pulley_cable_corner`)

*A pulley that changes attached cable lengths based on forces applied to cables.*
Draw a rope logic link between two rope nodes to form a cable. Cables will slide based on difference in force applied to each cable.

- Größe 3x1x3 Blöcke (voxel [-1, 0, -1] .. [1, 0, 1]), Masse 25, Preis 250, Tags: basic
- Werte: cable_length=150, cable_radius=0.05, logic_gate_subtype=9, type=48
- Zweiter Körper (Gelenk) bei [0, 3, 2]

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Rope 1 Length | Zahl | Ausgang | (1, 0, 0) | The current length of rope 1 in metres. |
| Rope 2 Length | Zahl | Ausgang | (0, 0, -1) | The current length of rope 2 in metres. |
| Rope 2 | Seil/Munition | Eingang | (-1, 0, -1) |  |
| Rope 1 | Seil/Munition | Eingang | (1, 0, 1) |  |

## Electrical Cable Anchor (`rope_hook_composite`)

*An anchor point for a basic data/electric cable.*
Draw a rope logic link between two Electrical Cable Anchors to form a cable. Limited to only one link but can transfer Data and Electric across the link.

- Größe 1x2x1 Blöcke (voxel [0, 0, 0] .. [0, 1, 0]), Masse 1, Preis 15, Tags: basic
- Werte: cable_radius=0.03, force_emitter_blade_physics_length=4.1, force_emitter_default_pitch=1, force_emitter_max_force=10000, logic_gate_subtype=2, type=48

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Rope Node | Seil/Munition | Eingang | (0, 1, 0) |  |
| Electric Node | Strom | Eingang | (0, 0, 0) |  |
| Composite Input | Composite | Eingang | (0, 0, 0) | Composite data to send to the connected anchor. |
| Composite Output | Composite | Ausgang | (0, 1, 0) | Composite data to receive from the connected anchor. |
| On/Off Input | An/Aus | Eingang | (0, 0, 0) | On/Off data to send to the connected anchor. |
| On/Off Output | An/Aus | Ausgang | (0, 1, 0) | On/Off data to receive from the connected anchor. |
| Video Data Send | Video | Eingang | (0, 0, 0) | Video data to send to the connected anchor. |
| Video Data Receive | Video | Ausgang | (0, 1, 0) | Video data to receive from the connected anchor. |
| Audio Data Send | Ton | Eingang | (0, 0, 0) | Audio data to send to the connected anchor. |
| Audio Data Receive | Ton | Ausgang | (0, 1, 0) | Audio data to receive from the connected anchor. |

## Equipment inventory (Binoculars) (`inventory_equipment_binoculars`)

*A small equipment storage unit containing a pair of binoculars.*
Hold [$[action_equipment_use]] to zoom in on faraway objects.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 50, Tags: basic
- Werte: cable_length=-431602080, inventory_class=1, inventory_default_item=6, seat_health_per_sec=1, type=32

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Equipment inventory (C4 Detonator) (`inventory_equipment_c4_detonator`)

*A small equipment storage unit containing a C-4 remote detonator.*
Press [$[action_equipment_use]] to detonate armed C-4 explosives.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 50, Tags: weapon,explosive
- Werte: cable_length=-431602080, inventory_class=1, inventory_default_item=32, seat_health_per_sec=1, type=32

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Equipment inventory (C4 Explosive) (`inventory_equipment_c4`)

*A small equipment storage unit containing C-4 plastic explosive.*
Press [$[action_equipment_use]] to arm and plant the C-4 explosive on a nearby surface.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 50, Tags: weapon,explosive
- Werte: cable_length=-431602080, inventory_class=1, inventory_default_item=31, seat_health_per_sec=1, type=32

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Equipment inventory (Cable) (`inventory_equipment_cable`)

*A large equipment storage unit containing 20m of electrical cable.*
Press [$[action_equipment_use]] to attach the cable to an unoccupied electrical cable anchor. Interacting with [$[action_interact_left]]/[$[action_interact_right]] on an occupied electical cable anchor will retrieve the cable if the player has inventory space to hold it.

- Größe 1x1x3 Blöcke (voxel [0, 0, -1] .. [0, 0, 1]), Masse 3, Preis 200, Tags: basic
- Werte: cable_length=-431602080, inventory_class=2, inventory_default_item=7, seat_health_per_sec=1, type=32

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Equipment inventory (Compass) (`inventory_equipment_compass`)

*A small equipment storage unit containing a compass.*
When held, the red needle of the compass will point northwards. The compass also displays a bearing on the equipment hotbar UI.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 50, Tags: basic
- Werte: cable_length=-431602080, inventory_class=1, inventory_default_item=8, seat_health_per_sec=1, type=32

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Equipment inventory (Defibrillator) (`inventory_equipment_defibrillator`)

*A large equipment storage unit containing a defibrillator.*
Press [$[action_equipment_use]] on an incapacitated survivor to revive them. Requires electric charge to function, and will recharge when placed into a powered large equipment storage unit.

- Größe 1x1x3 Blöcke (voxel [0, 0, -1] .. [0, 0, 1]), Masse 3, Preis 200, Tags: basic
- Werte: cable_length=-431602080, inventory_class=2, inventory_default_item=9, seat_health_per_sec=1, type=32

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Equipment inventory (Dog Whistle) (`inventory_equipment_dog_whistle`)

*A small equipment storage unit containing a dog whistle.*
Hold [$[action_equipment_use]] to sound the whistle. Nearby dogs will respond to certain whistle patterns. 1 long burst = Wait. 2 short bursts = Follow.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 50
- Werte: cable_length=-431602080, inventory_class=1, inventory_default_item=73, seat_health_per_sec=1, type=32

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Equipment inventory (Fire Extinguisher) (`inventory_equipment_fire_extinguisher`)

*A large equipment storage unit containing a fire extinguisher.*
Hold [$[action_equipment_use]] to spray a stream of water capable of extinguishing fires. This equipment has a limited water capacity and cannot be refilled.

- Größe 1x1x3 Blöcke (voxel [0, 0, -1] .. [0, 0, 1]), Masse 3, Preis 200, Tags: basic,mission
- Werte: cable_length=-431602080, inventory_class=2, inventory_default_item=10, seat_health_per_sec=1, type=32

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Equipment inventory (First Aid Kit) (`inventory_equipment_first_aid`)

*A small equipment storage unit containing a first aid kit.*
Press [$[action_equipment_use]] to heal yourself, or heal a survivor highlighted by your crosshair.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 50, Tags: basic,mission
- Werte: cable_length=-431602080, inventory_class=1, inventory_default_item=11, seat_health_per_sec=1, type=32

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Equipment inventory (Fishing Rod) (`inventory_equipment_fishing_rod`)

*A large equipment storage unit containing a fishing rod.*
Hold and release [$[action_equipment_use]] to load and cast the fishing line. Hold [$[action_equipment_use]] to reel in the fishing line. Press [$[action_equipment_secondary]] before casting to cycle the sink depth of the hook.

- Größe 1x1x3 Blöcke (voxel [0, 0, -1] .. [0, 0, 1]), Masse 3, Preis 200, Tags: basic,fishing
- Werte: cable_length=-431602080, inventory_class=2, inventory_default_item=81, seat_health_per_sec=1, type=32

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Equipment inventory (Flare) (`inventory_equipment_flare`)

*A small equipment storage unit containing flares.*
Press [$[action_equipment_use]] to throw a red smoke flare which burns for a long time.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 50
- Werte: cable_length=-431602080, inventory_class=1, inventory_default_item=12, seat_health_per_sec=1, type=32

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Equipment inventory (Flaregun Ammo) (`inventory_equipment_flaregun_ammo`)

*A small equipment storage unit containing a box of flaregun ammo.*
Press [$[action_equipment_use]] to reload an equipped flaregun.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 50
- Werte: cable_length=-431602080, inventory_class=1, inventory_default_item=14, seat_health_per_sec=1, type=32

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Equipment inventory (Flaregun) (`inventory_equipment_flaregun`)

*A small equipment storage unit containing a flaregun preloaded with 1 flaregun round.*
Press [$[action_equipment_use]] to fire a red illumination flare that burns for a short time, and [$[action_equipment_secondary]] to reload.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 50
- Werte: cable_length=-431602080, inventory_class=1, inventory_default_item=13, seat_health_per_sec=1, type=32

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Equipment inventory (Flashlight) (`inventory_equipment_flashlight`)

*A small equipment storage unit containing a flashlight.*
Press [$[action_equipment_use]] to toggle the flashlight on or off. Requires electric charge to function, and will recharge when placed into a powered small equipment storage unit.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 50, Tags: basic
- Werte: cable_length=-431602080, inventory_class=1, inventory_default_item=15, seat_health_per_sec=1, type=32

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Equipment inventory (Glowstick) (`inventory_equipment_glowstick`)

*A small equipment storage unit containing glowsticks.*
Press [$[action_equipment_use]] to throw a glowstick which emits light for an extended time. The editor paint tool can be used to set the glowstick hue.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 50
- Werte: cable_length=-431602080, inventory_class=1, inventory_default_item=72, seat_health_per_sec=1, type=32

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Equipment Inventory (Hand Grenade) (`inventory_equipment_grenade`)

*A small equipment storage unit containing a hand grenade.*
Press [$[action_equipment_use]] to throw a hand grenade, which will detonate after a short delay.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 50, Tags: weapon,explosive
- Werte: cable_length=-431602080, inventory_class=1, inventory_default_item=41, seat_health_per_sec=1, type=32

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Equipment inventory (Hose) (`inventory_equipment_hose`)

*A large equipment storage unit containing 20m of fluid hosing.*
Press [$[action_equipment_use]] to attach the hose to an unoccupied fluid hose anchor. Interacting with [$[action_interact_left]]/[$[action_interact_right]] on an occupied fluid hose anchor will retrieve the hose if the player has inventory space to hold it. If the hose contains water, press [$[action_equipment_secondary]] to toggle open the hose valve and allow the water to flow freely.

- Größe 1x1x3 Blöcke (voxel [0, 0, -1] .. [0, 0, 1]), Masse 3, Preis 200, Tags: basic
- Werte: cable_length=-431602080, inventory_class=2, inventory_default_item=16, seat_health_per_sec=1, type=32

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Equipment inventory (Night Vision Binoculars) (`inventory_equipment_night_vision_binoculars`)

*A small equipment storage unit containing a pair of night vision binoculars.*
Hold [$[action_equipment_use]] to zoom in on faraway objects. The night vision effect provides improved visibility in low light conditions, but hinders visibility in daylight. Requires electric charge to function, and will recharge when placed into a powered small equipment storage unit.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 50, Tags: basic
- Werte: cable_length=-431602080, inventory_class=1, inventory_default_item=17, seat_health_per_sec=1, type=32

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Equipment inventory (Oxygen Mask) (`inventory_equipment_oxygen_mask`)

*A small equipment storage unit containing an oxygen mask.*
Press [$[action_equipment_use]] to recover your breath while underwater. This equipment has a limited air capacity, and will refill when placed into a powered small equipment storage unit.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 50, Tags: basic
- Werte: cable_length=-431602080, inventory_class=1, inventory_default_item=18, seat_health_per_sec=1, type=32

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Equipment Inventory (Pistol Ammo) (`inventory_equipment_pistol_ammo`)

*A small equipment storage unit containing a pistol ammo magazine.*
Press [$[action_equipment_use]] to reload an equipped pistol.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 50, Tags: weapon,firearm,gun
- Werte: cable_length=-431602080, inventory_class=1, inventory_default_item=36, seat_health_per_sec=1, type=32

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Equipment inventory (Pistol) (`inventory_equipment_pistol`)

*A small equipment storage unit containing a pistol.*
Press [$[action_equipment_use]] to fire, and [$[action_equipment_secondary]] to reload. The pistol is compact enough for a belt holster, and can be accurate when recoil is carefully managed.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 200, Tags: weapon,firearm,gun
- Werte: cable_length=-431602080, inventory_class=1, inventory_default_item=35, seat_health_per_sec=1, type=32

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Equipment inventory (Radiation Detector) (`inventory_equipment_geiger_counter`)

*A small equipment storage unit containing a radiation detector.*
Press [$[action_equipment_use]] to toggle radiation detection on or off. Requires electric charge to function, and will recharge when placed into a powered small equipment storage unit.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 50, Tags: geiger,radiation
- Werte: cable_length=-431602080, inventory_class=1, inventory_default_item=30, seat_health_per_sec=1, type=32

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Equipment inventory (Radio Signal Locator) (`inventory_equipment_radio_signal_locator`)

*A large equipment storage unit containing a handheld transponder locator.*
Press [$[action_equipment_use]] to toggle the locator on or off. When active, the locator produces audible beeps that increase in frequency as the player nears an active transponder. The handheld locator has a shorter detection range than the vehicle mounted locator, but can narrow down the target location to a smaller area. Requires electric charge to function, and will recharge when placed into a powered large equipment storage unit.

- Größe 1x1x3 Blöcke (voxel [0, 0, -1] .. [0, 0, 1]), Masse 3, Preis 200, Tags: mission
- Werte: cable_length=-431602080, inventory_class=2, inventory_default_item=20, seat_health_per_sec=1, type=32

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Equipment inventory (Radio) (`inventory_equipment_radio`)

*A small equipment storage unit containing a handheld radio.*
Hold [$[action_equipment_use]] transmit voice audio. Press [$[action_equipment_secondary]] to cycle between frequencies 0~8, or turn the radio off. When a frequency is selected, the radio will transmit and receive voice audio on that frequency only. Requires electric charge to function, and will recharge when placed into a powered small equipment storage unit. (Max Effective Range : 500m)

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 50, Tags: basic
- Werte: cable_length=-431602080, inventory_class=1, inventory_default_item=19, seat_health_per_sec=1, type=32

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Equipment inventory (Remote Control Unit) (`inventory_equipment_remote_control`)

*A small equipment storage unit containing a remote control unit.*
Press [$[action_equipment_use]] to toggle the remote control on or off. Press [$[action_equipment_secondary]] to cycle between frequencies 0~8. When active, the remote control uses the basic vehicle pilot seat input bindings and transmits them as composite radio data on the selected frequency. Requires electric charge to function, and will recharge when placed into a powered small equipment storage unit. (Max Effective Range : 500m)

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 50
- Werte: cable_length=-431602080, inventory_class=1, inventory_default_item=21, seat_health_per_sec=1, type=32

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Equipment inventory (Rifle Ammo) (`inventory_equipment_rifle_ammo`)

*A small equipment storage unit containing a rifle ammo magazine.*
Press [$[action_equipment_use]] to reload an equipped rifle.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 50, Tags: weapon,firearm,gun
- Werte: cable_length=-431602080, inventory_class=1, inventory_default_item=40, seat_health_per_sec=1, type=32

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Equipment inventory (Rifle) (`inventory_equipment_rifle`)

*A large equipment storage unit containing a rifle.*
Press [$[action_equipment_use]] to fire, and [$[action_equipment_secondary]] to reload. The rifle fires accurate and powerful shots for long-range engagements.

- Größe 1x1x3 Blöcke (voxel [0, 0, -1] .. [0, 0, 1]), Masse 3, Preis 200, Tags: weapon,firearm,gun
- Werte: cable_length=-431602080, inventory_class=2, inventory_default_item=39, seat_health_per_sec=1, type=32

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Equipment inventory (Rope) (`inventory_equipment_rope`)

*A large equipment storage unit containing 20m of rope.*
Press [$[action_equipment_use]] to attach the rope to any rope anchor. Interacting with [$[action_interact_left]]/[$[action_interact_right]] on an occupied rope anchor will retrieve the rope if the player has inventory space to hold it.

- Größe 1x1x3 Blöcke (voxel [0, 0, -1] .. [0, 0, 1]), Masse 3, Preis 200, Tags: basic
- Werte: cable_length=-431602080, inventory_class=2, inventory_default_item=22, seat_health_per_sec=1, type=32

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Equipment inventory (SMG Ammo) (`inventory_equipment_smg_ammo`)

*A small equipment storage unit containing a submachine gun ammo magazine.*
Press [$[action_equipment_use]] to reload an equipped submachine gun.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 50, Tags: weapon,firearm,gun
- Werte: cable_length=-431602080, inventory_class=1, inventory_default_item=38, seat_health_per_sec=1, type=32

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Equipment inventory (SMG) (`inventory_equipment_smg`)

*A large equipment storage unit containing a submachine gun.*
Press [$[action_equipment_use]] to fire, and [$[action_equipment_secondary]] to reload. The SMG has a high rate of fire and magazine capacity.

- Größe 1x1x3 Blöcke (voxel [0, 0, -1] .. [0, 0, 1]), Masse 3, Preis 200, Tags: weapon,firearm,gun
- Werte: cable_length=-431602080, inventory_class=2, inventory_default_item=37, seat_health_per_sec=1, type=32

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Equipment inventory (Speargun Ammo) (`inventory_equipment_speargun_ammo`)

*A small equipment storage unit containing a box of speargun ammo.*
Press [$[action_equipment_use]] to reload an equipped speargun.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 50, Tags: weapon,firearm,gun
- Werte: cable_length=-431602080, inventory_class=1, inventory_default_item=34, seat_health_per_sec=1, type=32

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Equipment inventory (Speargun) (`inventory_equipment_speargun`)

*A large equipment storage unit containing a speargun.*
Press [$[action_equipment_use]] to fire, and [$[action_equipment_secondary]] to reload. The speargun can be fired underwater and spears travel through the water more effectively than bullets.

- Größe 1x1x3 Blöcke (voxel [0, 0, -1] .. [0, 0, 1]), Masse 3, Preis 200, Tags: weapon,firearm,gun
- Werte: cable_length=-431602080, inventory_class=2, inventory_default_item=33, seat_health_per_sec=1, type=32

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Equipment inventory (Strobe Light) (`inventory_equipment_strobe_light`)

*A small equipment storage unit containing a strobe light.*
Press [$[action_equipment_use]] to toggle the strobe light on or off. Press [$[action_equipment_secondary]] to toggle MOB (man overboard) mode, which will automatically turn the strobe light on if the player is submerged in water. The strobe light will continue to function when unequipped or discarded. Requires electric charge to function, and will recharge when placed into a powered small equipment storage unit.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 50
- Werte: cable_length=-431602080, inventory_class=1, inventory_default_item=23, seat_health_per_sec=1, type=32

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Equipment inventory (Strobe Light, Infrared) (`inventory_equipment_strobe_light_infrared`)

*A small equipment storage unit containing an infrared strobe light.*
Press [$[action_equipment_use]] to toggle the strobe light on or off. Press [$[action_equipment_secondary]] to toggle MOB (man overboard) mode, which will automatically turn the strobe light on if the player is submerged in water. The strobe light will continue to function when unequipped or discarded. The infrared strobe light flashes are only visible to infrared cameras. Requires electric charge to function, and will recharge when placed into a powered small equipment storage unit.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 50
- Werte: cable_length=-431602080, inventory_class=1, inventory_default_item=24, seat_health_per_sec=1, type=32

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Equipment inventory (Transponder) (`inventory_equipment_transponder`)

*A small equipment storage unit containing a handheld transponder.*
Press [$[action_equipment_use]] to toggle the transponder on or off. Press [$[action_equipment_secondary]] to toggle MOB (man overboard) mode, which will automatically turn the transponder on if the player is submerged in water. The transponder will continue to function when unequipped or discarded. Requires electric charge to function, and will recharge when placed into a powered small equipment storage unit.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 50, Tags: mission
- Werte: cable_length=-431602080, inventory_class=1, inventory_default_item=25, seat_health_per_sec=1, type=32

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Equipment inventory (Underwater Welding Torch) (`inventory_equipment_underwater_welding_torch`)

*A large equipment storage unit containing an underwater welding torch.*
Hold [$[action_equipment_use]] to repair damaged vehicle components highlighted by the players crosshair. The underwater welding torch holds less fuel than the standard welding torch, but can be operated while submerged in water. This equipment has a limited fuel capacity and cannot be refilled.

- Größe 1x1x3 Blöcke (voxel [0, 0, -1] .. [0, 0, 1]), Masse 3, Preis 200, Tags: basic
- Werte: cable_length=-431602080, inventory_class=2, inventory_default_item=26, seat_health_per_sec=1, type=32

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Equipment inventory (Welding Torch) (`inventory_equipment_welding_torch`)

*A large equipment storage unit containing a welding torch.*
Hold [$[action_equipment_use]] to repair damaged vehicle components highlighted by the players crosshair. This equipment has a limited fuel capacity and cannot be refilled.

- Größe 1x1x3 Blöcke (voxel [0, 0, -1] .. [0, 0, 1]), Masse 3, Preis 200, Tags: basic
- Werte: cable_length=-431602080, inventory_class=2, inventory_default_item=27, seat_health_per_sec=1, type=32

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Flare Launcher (`flare_launcher`)

*Single-use flare launcher for signalling and illumination.*
Set the flare canister type and launch velocity in the component properties.

- Größe 1x2x1 Blöcke (voxel [0, 0, 0] .. [0, 1, 0]), Masse 1, Preis 10
- Werte: button_type=0, cable_radius=0.02, constraint_axis=0, door_lower_limit=0, door_upper_limit=0, dynamic_max_rotation=0, force_emitter_max_vector=0, light_fov=0, light_intensity=0, light_range=0, magnet_force=0, max_motor_force=0, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, type=49, wheel_radius=0

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Launch | An/Aus | Eingang | (0, 0, 0) |  |
| Launch Passthrough | An/Aus | Ausgang | (0, 1, 0) |  |

## Fluid Cannon (`watercannon`)

*A fluid cannon that fires pressurized water for putting out fires.*
The cannon is a turret and can rotate on 2 axis.

- Größe 3x3x3 Blöcke (voxel [-1, 0, -1] .. [1, 2, 1]), Masse 11, Preis 100
- Werte: cable_radius=0.02, pump_pressure=0, type=24, water_component_type=2

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Turret Swivel | Zahl | Eingang | (-1, 0, -1) | Yaw axis servo control for the cannon head. |
| Nozzle Pitch | Zahl | Eingang | (1, 0, -1) | Pitch axis servo control for the cannon head. |
| Fluid Supply | Fluessigkeit/Gas | Eingang | (0, 0, 0) | The fluid input to output from the nozzle. Filters to water only. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Fluid Hose Anchor (`rope_hook_fluid`)

*An anchor point for a basic fluid hose.*
Draw a rope logic link between two Fluid Hose Anchors to form a hose. Limited to only one link but can transfer fluid across the link.

- Größe 1x2x1 Blöcke (voxel [0, 0, 0] .. [0, 1, 0]), Masse 1, Preis 15, Tags: basic
- Werte: cable_radius=0.04, logic_gate_subtype=1, type=48

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Rope Node | Seil/Munition | Eingang | (0, 1, 0) |  |
| Fluid Node | Fluessigkeit/Gas | Eingang | (0, 0, 0) |  |

## Fluid Hose Pulley (`winch_pulley_hose`)

*A pulley that changes attached hose lengths based on forces applied to hoses.*
Draw a rope logic link between two rope nodes to form a hose. Hoses will slide based on difference in force applied to each hose.

- Größe 3x1x3 Blöcke (voxel [-1, 0, -1] .. [1, 0, 1]), Masse 25, Preis 250, Tags: basic
- Werte: cable_length=150, cable_radius=0.05, logic_gate_subtype=8, type=48
- Zweiter Körper (Gelenk) bei [0, 3, 2]

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Rope 1 Length | Zahl | Ausgang | (1, 0, 0) | The current length of rope 1 in metres. |
| Rope 2 Length | Zahl | Ausgang | (-1, 0, 0) | The current length of rope 2 in metres. |
| Rope 2 | Seil/Munition | Eingang | (-1, 0, 1) |  |
| Rope 1 | Seil/Munition | Eingang | (1, 0, 1) |  |
| Fluid Node 1 | Fluessigkeit/Gas | Ausgang | (0, 0, 0) |  |
| Fluid Node 2 | Fluessigkeit/Gas | Ausgang | (0, 0, 0) |  |

## Fluid Hose Pulley (Corner) (`winch_pulley_hose_corner`)

*A pulley that changes attached hose lengths based on forces applied to hoses.*
Draw a rope logic link between two rope nodes to form a hose. Hoses will slide based on difference in force applied to each hose.

- Größe 3x1x3 Blöcke (voxel [-1, 0, -1] .. [1, 0, 1]), Masse 25, Preis 250, Tags: basic
- Werte: cable_length=150, cable_radius=0.05, logic_gate_subtype=8, type=48
- Zweiter Körper (Gelenk) bei [0, 3, 2]

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Rope 1 Length | Zahl | Ausgang | (1, 0, 0) | The current length of rope 1 in metres. |
| Rope 2 Length | Zahl | Ausgang | (0, 0, -1) | The current length of rope 2 in metres. |
| Rope 2 | Seil/Munition | Eingang | (-1, 0, -1) |  |
| Rope 1 | Seil/Munition | Eingang | (1, 0, 1) |  |
| Fluid Node 1 | Fluessigkeit/Gas | Ausgang | (0, 0, 0) |  |
| Fluid Node 2 | Fluessigkeit/Gas | Ausgang | (0, 0, 0) |  |

## Fluid Nozzle (`water_nozzle`)

*A fluid nozzle that fires pressurized water for putting out fires.*
The angle of spray can be adjusted.

- Größe 1x2x1 Blöcke (voxel [0, 0, 0] .. [0, 1, 0]), Masse 1, Preis 100, Tags: cannon,basic
- Werte: cable_radius=0.02, pump_pressure=0, type=24, water_component_type=2

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Fluid Supply | Fluessigkeit/Gas | Eingang | (0, 0, 0) | The fluid input to output from the nozzle. |
| Spray Angle | Zahl | Eingang | (0, 1, 0) | Adjustable spray angle from 0 (focused) to 1 (spread). |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Foghorn (`foghorn`)

*A ship's foghorn that will sound when receiving an on signal.*
It has an audible range of 1500m.

- Größe 4x3x3 Blöcke (voxel [-1, 0, -1] .. [2, 2, 1]), Masse 5, Preis 200, Tags: boat,sound,audio
- Werte: cable_radius=0.02, indicator_type=7, m_pump_pressure=0.01, type=21

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Horn | An/Aus | Eingang | (-1, 1, 0) | Sounds the horn when recieving an on signal. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Harness (`seat_harness`)

*A rescue harness.*
You can get in and out of the harness by interacting with it using [$[action_use_seat]]. You can place a rescued survivor in any harness by using [$[action_use_seat]] while carrying them.

- Größe 3x6x3 Blöcke (voxel [-1, 0, -1] .. [1, 5, 1]), Masse 20, Preis 150, Tags: basic,seat
- Werte: button_type=0, cable_length=0, cable_radius=0, constraint_axis=0, door_lower_limit=0, door_upper_limit=0, dynamic_max_rotation=0, light_fov=0, light_intensity=0, light_range=0, magnet_force=0, max_motor_force=0, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, seat_pose=4, type=1, wheel_radius=0

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Occupied | An/Aus | Ausgang | (0, 0, 0) | Outputs an on signal if this harness is occupied by a character. |
| Trigger [$[action_trigger]] | An/Aus | Ausgang | (0, 0, 0) | Outputs an on signal when [$[action_trigger]] is held, and off when it is not. |
| Hotkey 1 [$[action_hotkey_1]] | An/Aus | Ausgang | (0, 2, -1) | Outputs an on signal when [$[action_hotkey_1]] is held, and off when it is not. |
| Hotkey 2 [$[action_hotkey_2]] | An/Aus | Ausgang | (0, 1, -1) | Outputs an on signal when [$[action_hotkey_2]] is held, and off when it is not. |
| Hotkey 3 [$[action_hotkey_3]] | An/Aus | Ausgang | (0, 0, -1) | Outputs an on signal when [$[action_hotkey_3]] is held, and off when it is not. |
| Hotkey 4 [$[action_hotkey_4]] | An/Aus | Ausgang | (0, 2, 1) | Outputs an on signal when [$[action_hotkey_4]] is held, and off when it is not. |
| Hotkey 5 [$[action_hotkey_5]] | An/Aus | Ausgang | (0, 1, 1) | Outputs an on signal when [$[action_hotkey_5]] is held, and off when it is not. |
| Hotkey 6 [$[action_hotkey_6]] | An/Aus | Ausgang | (0, 0, 1) | Outputs an on signal when [$[action_hotkey_6]] is held, and off when it is not. |
| Seat Data | Composite | Ausgang | (-1, 0, 0) | Outputs the axis, hotkey and occupied data from the seat. (On/Off 1+ : Hotkeys) (On/Off 31 : Trigger) (On/Off 32 : Occupied) (Value 1 : [$[action_left]]/[$[action_right]]) (Value 2 : [$[action_up]]/[$[action_down]]) (Value 3 : [$[action_pedal_left]]/[$[action_pedal_right]]) (Value 4 : [$[action_throttle_up]]/[$[action_throttle_down]]) |

## Heater (`heater`)

*A small heater that will provide warmth in a radius.*
When enabled, the heater will warm either the compartment it is within or any players within a 10m radius, allowing them to survive cold temperatures.

- Größe 1x1x3 Blöcke (voxel [0, 0, -1] .. [0, 0, 1]), Masse 3, Preis 50, Tags: basic
- Werte: type=39

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Heating Element | An/Aus | Eingang | (0, 0, 0) | Enables the heating element when receiving an on signal. |
| Electric | Strom | Eingang | (0, 0, -1) | Electrical power connection. |

## Hose (`water_hose`)

*A building block attached to the end of a mechanical hose that can be raised and lowered.*
This can be used to transport water between Two bodies. Two on/off signals are used to control whether the hose is moving up (towards the base) or down (away from the base). A number output allows you to measure the hose's current length if necessary. The maximum length of the hose is 16 metres (64 blocks). The speed of the hose mechanism can be configured by selecting this component with the select tool.

- Größe 3x4x3 Blöcke (voxel [-1, 0, -1] .. [1, 3, 1]), Masse 25, Preis 100
- Werte: cable_radius=0.05, child_name=water_hose_b, constraint_axis=2, constraint_range_of_motion=30, constraint_type=1, light_intensity=0, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, type=20
- Zweiter Körper (Gelenk) bei [0, 3, 3]

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Fluid | Fluessigkeit/Gas | Ausgang | (0, 0, 0) | Fluid connection for the hose coil. |
| Hose Up | An/Aus | Eingang | (-1, 0, 1) | Raises the hose up when receiving an on signal. |
| Hose Down | An/Aus | Eingang | (-1, 0, -1) | Lowers the hose down when receiving an on signal. |
| Hose Length | Zahl | Ausgang | (-1, 0, 0) | The current length of the hose in metres. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Huge Winch (`rope_hook_winch_huge`)

*A mechanical winch that can transfer data/electric/fluid through an attached cable, with an extension length of 600m.*
Draw a rope logic link between two Rope Nodes to form a cable. Can be extended and retracted.

- Größe 9x7x7 Blöcke (voxel [-4, 0, -3] .. [4, 6, 3]), Masse 400, Preis 5000, Tags: basic
- Werte: cable_length=600, cable_radius=0.07, logic_gate_subtype=3, type=48
- Zweiter Körper (Gelenk) bei [0, 2, 5]

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Down | An/Aus | Eingang | (-1, 0, 0) | Lowers the winch cable down when receiving an on signal. |
| Up | An/Aus | Eingang | (1, 0, 0) | Raises the winch cable up when receiving an on signal. |
| Rope Node | Seil/Munition | Eingang | (0, 1, 0) |  |
| Electric Node | Strom | Eingang | (0, 0, 0) |  |
| Composite Input | Composite | Eingang | (0, 0, 0) | Composite data to send to the connected anchor. |
| Composite Output | Composite | Ausgang | (0, 1, 0) | Composite data to receive from the connected anchor. |
| On/Off Input | An/Aus | Eingang | (0, 0, 0) | On/Off data to send to the connected anchor. |
| On/Off Output | An/Aus | Ausgang | (0, 1, 0) | On/Off data to receive from the connected anchor. |
| Video Data Send | Video | Eingang | (0, 0, 0) | Video data to send to the connected anchor. |
| Video Data Receive | Video | Ausgang | (0, 1, 0) | Video data to receive from the connected anchor. |
| Audio Data Send | Ton | Eingang | (0, 0, 0) | Audio data to send to the connected anchor. |
| Audio Data Receive | Ton | Ausgang | (0, 1, 0) | Audio data to receive from the connected anchor. |
| Length | Zahl | Ausgang | (-1, 1, 0) | The current length of the winch cable in metres. |
| Fluid | Fluessigkeit/Gas | Ausgang | (0, 0, 0) | Fluid connection for the hose coil. |
| Speed | Zahl | Eingang | (1, 1, 0) | The speed of the winch clamped to a relative range of -1 to 1. |
| Detach Rope | An/Aus | Eingang | (0, 2, 3) |  |

## Huge Winch (`winch_huge_a`)

*A building block attached to the end of a 500m mechanical winch that can be raised and lowered.*
The winch is operated electrically, and outputs its current length.

- Größe 9x7x7 Blöcke (voxel [-4, 0, -3] .. [4, 6, 3]), Masse 400, Preis 5000
- Werte: cable_length=500, cable_radius=0.05, child_name=winch_b, constraint_axis=2, constraint_range_of_motion=30, constraint_type=1, light_intensity=0, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, type=20
- Zweiter Körper (Gelenk) bei [0, 2, 5]

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Up | An/Aus | Eingang | (-1, 0, 0) | Raises the winch cable up when receiving an on signal. |
| Down | An/Aus | Eingang | (1, 0, 0) | Lowers the winch cable down when receiving an on signal. |
| Length | Zahl | Ausgang | (0, 0, 0) | The current length of the winch cable in metres. |
| Electric | Strom | Eingang | (0, 0, 1) | Electrical power connection. |
| Fluid | Fluessigkeit/Gas | Ausgang | (0, 0, 0) | Fluid connection for the hose coil. |

## Landing Float (`landing_float`)

*A buoyant float.*
Ideal for attaching to helicopters to allow them to land on the ocean.

- Größe 3x3x9 Blöcke (voxel [-1, -2, -4] .. [1, 0, 4]), Masse 1, Preis 50, Tags: basic
- Werte: buoy_factor=0.5, buoy_radius=0.75, button_type=0, cable_radius=0, constraint_axis=0, door_lower_limit=0, door_upper_limit=0, dynamic_max_rotation=0, light_fov=0, light_intensity=0, light_range=0, magnet_force=0, max_motor_force=0, max_motor_speed=5, rudder_surface_area=0, type=3, wheel_radius=0

## Large equipment inventory (Empty) (`inventory_medium`)

*An empty large equipment storage unit.*
Only large handheld equipment can be stored in this unit. When connected to an electric power source, any rechargable equipment stored in the unit will drain a small amount of electricity until recharged to 100% capacity.

- Größe 1x1x3 Blöcke (voxel [0, 0, -1] .. [0, 0, 1]), Masse 3, Preis 50, Tags: basic
- Werte: cable_length=-431602080, inventory_class=2, seat_health_per_sec=1, type=32

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Large Winch (`rope_hook_winch_large`)

*A mechanical winch that can transfer data/electric/fluid through an attached cable, with an extension length of 150m.*
Draw a rope logic link between two Rope Nodes to form a cable. Can be extended and retracted.

- Größe 3x4x3 Blöcke (voxel [-1, 0, -1] .. [1, 3, 1]), Masse 100, Preis 800, Tags: basic
- Werte: cable_length=150, cable_radius=0.05, logic_gate_subtype=3, type=48
- Zweiter Körper (Gelenk) bei [0, 3, 2]

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Down | An/Aus | Eingang | (-1, 1, 0) | Lowers the winch cable down when receiving an on signal. |
| Up | An/Aus | Eingang | (1, 1, 0) | Raises the winch cable up when receiving an on signal. |
| Rope Node | Seil/Munition | Eingang | (0, 1, 0) |  |
| Electric Node | Strom | Eingang | (0, 0, 0) |  |
| Composite Input | Composite | Eingang | (0, 0, 0) | Composite data to send to the connected anchor. |
| Composite Output | Composite | Ausgang | (0, 1, 0) | Composite data to receive from the connected anchor. |
| On/Off Input | An/Aus | Eingang | (0, 0, 0) | On/Off data to send to the connected anchor. |
| On/Off Output | An/Aus | Ausgang | (0, 1, 0) | On/Off data to receive from the connected anchor. |
| Video Data Send | Video | Eingang | (0, 0, 0) | Video data to send to the connected anchor. |
| Video Data Receive | Video | Ausgang | (0, 1, 0) | Video data to receive from the connected anchor. |
| Audio Data Send | Ton | Eingang | (0, 0, 0) | Audio data to send to the connected anchor. |
| Audio Data Receive | Ton | Ausgang | (0, 1, 0) | Audio data to receive from the connected anchor. |
| Length | Zahl | Ausgang | (-1, 0, 0) | The current length of the winch cable in metres. |
| Fluid | Fluessigkeit/Gas | Ausgang | (0, 0, 0) | Fluid connection for the hose coil. |
| Speed | Zahl | Eingang | (1, 0, 0) | The speed of the winch clamped to a relative range of -1 to 1. |
| Detach Rope | An/Aus | Eingang | (0, 3, 1) |  |

## Large Winch (`winch_large_a`)

*A building block attached to the end of a 100m mechanical winch that can be raised and lowered.*
The winch is operated electrically, and outputs its current length.

- Größe 3x4x3 Blöcke (voxel [-1, 0, -1] .. [1, 3, 1]), Masse 100, Preis 800
- Werte: cable_length=100, cable_radius=0.05, child_name=winch_b, constraint_axis=2, constraint_range_of_motion=30, constraint_type=1, light_intensity=0, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, type=20
- Zweiter Körper (Gelenk) bei [0, 3, 2]

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Up | An/Aus | Eingang | (-1, 0, 0) | Raises the winch cable up when receiving an on signal. |
| Down | An/Aus | Eingang | (1, 0, 0) | Lowers the winch cable down when receiving an on signal. |
| Length | Zahl | Ausgang | (0, 0, 0) | The current length of the winch cable in metres. |
| Electric | Strom | Eingang | (0, 0, 1) | Electrical power connection. |
| Fluid | Fluessigkeit/Gas | Ausgang | (0, 0, 0) | Fluid connection for the hose coil. |

## Light (`small_light`)

*A basic light that can be controlled using an on/off signal.*

- Größe 1x2x1 Blöcke (voxel [0, 0, 0] .. [0, 1, 0]), Masse 1, Preis 20
- Werte: button_type=0, cable_radius=0.02, door_lower_limit=0, door_upper_limit=0, dynamic_max_rotation=0, light_fov=0, light_range=10, magnet_force=0, max_motor_force=0, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, type=10

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Light Switch | An/Aus | Eingang | (0, 0, 0) | Controls whether or not the light is switched on. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Light (RGB) (`small_light_rgb`)

*An advanced light that can be controlled using a microcontroller.*
Three channels of the composite input can be used to set the red, green and blue components of the light's color using numbers between 0 and 1. The light can also operate in HSV mode, where the 3 inputs correspond to the hue, saturation and value (brightness) of the color between 0 and 1. The color mode and input channels can be customised by selecting this component with the select tool.

- Größe 1x2x1 Blöcke (voxel [0, 0, 0] .. [0, 1, 0]), Masse 1, Preis 50
- Werte: button_type=0, cable_radius=0.02, door_lower_limit=0, door_upper_limit=0, dynamic_max_rotation=0, light_fov=0, light_range=10, magnet_force=0, max_motor_force=0, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, type=38

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Color Data | Composite | Eingang | (0, 0, 0) | Composite link containing the light's color data. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Medical Bed (`seat_medical`)

*A bed equiped with medical monitoring equipment, slowly heals injured characters.*
You can get in and out of the medical bed by interacting with it using [$[action_use_seat]]. You can place a rescued survivor in any medical bed by using [$[action_use_seat]] while carrying them.

- Größe 3x4x7 Blöcke (voxel [-1, 0, -3] .. [1, 3, 3]), Masse 40, Preis 2500, Tags: basic
- Werte: button_type=0, cable_radius=0, constraint_axis=0, door_lower_limit=0, door_upper_limit=0, dynamic_max_rotation=0, light_fov=0, light_intensity=0, light_range=0, magnet_force=0, max_motor_force=0, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, seat_health_per_sec=1, seat_pose=3, type=1, wheel_radius=0

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Occupied | An/Aus | Ausgang | (0, 0, 0) | Outputs an on signal if this bed is occupied by a character. |

## Medium Winch (`rope_hook_winch`)

*A mechanical winch that can transfer data/electric/fluid through an attached cable, with an extension length of 40m.*
Draw a rope logic link between two Rope Nodes to form a cable. Can be extended and retracted.

- Größe 3x2x1 Blöcke (voxel [-1, 0, 0] .. [1, 1, 0]), Masse 20, Preis 250, Tags: basic
- Werte: cable_length=40, cable_radius=0.03, logic_gate_subtype=3, type=48
- Zweiter Körper (Gelenk) bei [0, 1, 2]

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Down | An/Aus | Eingang | (-1, 1, 0) | Lowers the winch cable down when receiving an on signal. |
| Up | An/Aus | Eingang | (1, 1, 0) | Raises the winch cable up when receiving an on signal. |
| Rope Node | Seil/Munition | Eingang | (0, 1, 0) |  |
| Electric Node | Strom | Eingang | (0, 0, 0) |  |
| Composite Input | Composite | Eingang | (0, 0, 0) | Composite data to send to the connected anchor. |
| Composite Output | Composite | Ausgang | (0, 1, 0) | Composite data to receive from the connected anchor. |
| On/Off Input | An/Aus | Eingang | (0, 0, 0) | On/Off data to send to the connected anchor. |
| On/Off Output | An/Aus | Ausgang | (0, 1, 0) | On/Off data to receive from the connected anchor. |
| Video Data Send | Video | Eingang | (0, 0, 0) | Video data to send to the connected anchor. |
| Video Data Receive | Video | Ausgang | (0, 1, 0) | Video data to receive from the connected anchor. |
| Audio Data Send | Ton | Eingang | (0, 0, 0) | Audio data to send to the connected anchor. |
| Audio Data Receive | Ton | Ausgang | (0, 1, 0) | Audio data to receive from the connected anchor. |
| Length | Zahl | Ausgang | (-1, 0, 0) | The current length of the winch cable in metres. |
| Fluid | Fluessigkeit/Gas | Ausgang | (0, 0, 0) | Fluid connection for the hose coil. |
| Speed | Zahl | Eingang | (1, 0, 0) | The speed of the winch clamped to a relative range of -1 to 1. |

## Medium Winch (`winch_a`)

*A building block attached to the end of a 20m mechanical winch that can be raised and lowered.*
The winch is operated electrically, and outputs its current length.

- Größe 3x2x1 Blöcke (voxel [-1, 0, 0] .. [1, 1, 0]), Masse 20, Preis 250
- Werte: cable_length=20, cable_radius=0.02, child_name=winch_b, constraint_axis=2, constraint_range_of_motion=30, constraint_type=1, light_intensity=0, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, type=20
- Zweiter Körper (Gelenk) bei [0, 1, 2]

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Up | An/Aus | Eingang | (-1, 0, 0) | Raises the winch cable up when receiving an on signal. |
| Down | An/Aus | Eingang | (1, 0, 0) | Lowers the winch cable down when receiving an on signal. |
| Length | Zahl | Ausgang | (0, 0, 0) | The current length of the winch cable in metres. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |
| Fluid | Fluessigkeit/Gas | Ausgang | (0, 0, 0) | Fluid connection for the hose coil. |

## Megaphone Speaker (Large) (`speaker_large`)

*A speaker capable of playing audio data to players within its range.*
A large megaphone capable of playing audio data to players within its range. (Range : 1000)

- Größe 3x3x5 Blöcke (voxel [-1, -1, 0] .. [1, 1, 4]), Masse 10, Preis 1000
- Werte: cable_radius=0.02, light_intensity=0, logic_gate_type=52, magnet_force=0, max_motor_speed=5, pump_pressure=0, radar_range=1000, rudder_surface_area=0, type=16

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Audio | Ton | Eingang | (0, 0, 0) | Audio data connection. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |
| Is Transmit | An/Aus | Ausgang | (0, 0, 1) | If the speaker is currently transmitting. |

## Megaphone Speaker (Small) (`speaker_medium`)

*A speaker capable of playing audio data to players within its range.*
A small megaphone capable of playing audio data to players within its range. (Range : 300)

- Größe 1x1x2 Blöcke (voxel [0, 0, 0] .. [0, 0, 1]), Masse 3, Preis 500
- Werte: cable_radius=0.02, light_intensity=0, logic_gate_type=52, magnet_force=0, max_motor_speed=5, pump_pressure=0, radar_range=300, rudder_surface_area=0, type=16

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Audio | Ton | Eingang | (0, 0, 0) | Audio data connection. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |
| Is Transmit | An/Aus | Ausgang | (0, 0, 1) | If the speaker is currently transmitting. |

## Mineral Drill (`mineral_drill`)

*A vehicle mounted drill for mining ore deposits.*
The mineral drill can be driven by torque to mine ore deposits in the world. Extracted minerals can be transferred to an attached hopper.

- Größe 3x6x3 Blöcke (voxel [-1, -2, -1] .. [1, 3, 1]), Masse 110, Preis 20000, Tags: mining,ore,coal
- Werte: steam_component_type=9, type=53

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Drill Shaft | Drehmoment | Eingang | (0, -2, 0) |  |

## Mounted End-Effector (`vehicle_tool_interact`)

*A vehicle mounted end-effector.*
The end-effector can interact with button components.

- Größe 1x2x1 Blöcke (voxel [0, 0, 0] .. [0, 1, 0]), Masse 10, Preis 1000
- Werte: type=58

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |
| Activate | An/Aus | Eingang | (0, 0, 0) | Enable end-effector. |

## Mounted Welder (`vehicle_tool_welder`)

*A vehicle mounted welding torch.*
The welding torch can repair components. This welder is electrically powered and works underwater.

- Größe 1x2x1 Blöcke (voxel [0, 0, 0] .. [0, 1, 0]), Masse 10, Preis 1000
- Werte: type=58

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |
| Activate | An/Aus | Eingang | (0, 0, 0) | Enable welding torch. |

## Outfit Inventory (Arctic) (`inventory_outfit_arctic`)

*An outfit inventory unit containing specialist thermal clothing for surviving Arctic temperatures.*
When equipped, it will increase your temperature enough to survive in colder weather conditions. Its thermal effectiveness is reduced when wet.

- Größe 3x3x1 Blöcke (voxel [-1, -1, 0] .. [1, 1, 0]), Masse 9, Preis 500, Tags: basic
- Werte: cable_length=-431602080, inventory_class=3, inventory_default_item=5, seat_health_per_sec=1, type=32

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Outfit Inventory (Armor Vest) (`inventory_outfit_wep_armor_vest`)

*An outfit inventory unit containing specialist millitary clothing for projectile protection.*
When equipped, damage from projectiles to the body and head is greatly reduced.  Wearing the outfit significantly limits movement speed.

- Größe 3x3x1 Blöcke (voxel [-1, -1, 0] .. [1, 1, 0]), Masse 9, Preis 1500, Tags: basic
- Werte: cable_length=-431602080, inventory_class=3, inventory_default_item=78, seat_health_per_sec=1, type=32

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Outfit Inventory (Black Hawk Vest) (`inventory_outfit_wep_black_hawk_vest`)

*An outfit inventory unit containing specialist millitary clothing for projectile protection.*
When equipped, damage from projectiles to the body is reduced slightly.

- Größe 3x3x1 Blöcke (voxel [-1, -1, 0] .. [1, 1, 0]), Masse 9, Preis 500, Tags: basic
- Werte: cable_length=-431602080, inventory_class=3, inventory_default_item=76, seat_health_per_sec=1, type=32

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Outfit Inventory (Bomb Disposal) (`inventory_outfit_wep_bomb_disposal`)

*An outfit inventory unit containing specialist millitary clothing for explosive protection.*
When equipped, damage from explosives is drastically reduced. Damage from projectiles to the body and head is slightly reduced. Wearing the outfit greatly limits movement speed.

- Größe 3x3x1 Blöcke (voxel [-1, -1, 0] .. [1, 1, 0]), Masse 9, Preis 1500, Tags: basic
- Werte: cable_length=-431602080, inventory_class=3, inventory_default_item=74, seat_health_per_sec=1, type=32

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Outfit Inventory (Chest Rig) (`inventory_outfit_wep_chest_rig`)

*An outfit inventory unit containing specialist millitary clothing for projectile protection.*
When equipped, damage from projectiles to the body is reduced slightly and damage to the head is significantly reduced.

- Größe 3x3x1 Blöcke (voxel [-1, -1, 0] .. [1, 1, 0]), Masse 9, Preis 500, Tags: basic
- Werte: cable_length=-431602080, inventory_class=3, inventory_default_item=75, seat_health_per_sec=1, type=32

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Outfit Inventory (Diving) (`inventory_outfit_diving`)

*An outfit inventory unit containing specialist diving equipment.*
When equipped, it will allow deep sea diving to a depth of 230m, and provides air for 10 minutes. The air tank can be refilled by storing the gear in an outfit inventory unit with an attached air input or via space seat.

- Größe 3x3x1 Blöcke (voxel [-1, -1, 0] .. [1, 1, 0]), Masse 9, Preis 2000, Tags: basic
- Werte: cable_length=-431602080, inventory_class=3, inventory_default_item=1, seat_health_per_sec=1, type=32

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |
| Fluid In | Fluessigkeit/Gas | Eingang | (0, -1, 0) |  |

## Outfit Inventory (Empty) (`inventory_outfit`)

*An empty outfit storage unit.*
Interacting with [$[action_interact_left]]/[$[action_interact_right]] will equip/store the selected outfit. Only specialist outfits can be stored in this unit. When connected to an electric power source, any rechargable outfits stored in the unit will drain a small amount of electricity until recharged to 100% capacity.

- Größe 3x3x1 Blöcke (voxel [-1, -1, 0] .. [1, 1, 0]), Masse 9, Preis 50, Tags: basic
- Werte: cable_length=-431602080, inventory_class=3, seat_health_per_sec=1, type=32

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Outfit Inventory (Firefighter SCBA) (`inventory_outfit_firefighter_scba`)

*An outfit inventory unit containing specialist firefighting gear.*
When equipped, it will absorb 95% of damage dealt by fires, and provides breathable air for the user. The air tank can be refilled by storing the gear in an outfit inventory unit.

- Größe 3x3x1 Blöcke (voxel [-1, -1, 0] .. [1, 1, 0]), Masse 9, Preis 1000, Tags: basic
- Werte: cable_length=-431602080, inventory_class=3, inventory_default_item=149, seat_health_per_sec=1, type=32

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |
| Fluid In | Fluessigkeit/Gas | Eingang | (0, -1, 0) |  |

## Outfit Inventory (Firefighter) (`inventory_outfit_firefighter`)

*An outfit inventory unit containing specialist firefighting gear.*
When equipped, it will absorb 95% of damage dealt by fires.

- Größe 3x3x1 Blöcke (voxel [-1, -1, 0] .. [1, 1, 0]), Masse 9, Preis 500, Tags: basic
- Werte: cable_length=-431602080, inventory_class=3, inventory_default_item=2, seat_health_per_sec=1, type=32

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Outfit Inventory (Hazmat) (`inventory_outfit_hazmat`)

*An outfit inventory unit containing specialist hazmat gear.*
When equipped, it will absorb 95% of incoming radiation.

- Größe 3x3x1 Blöcke (voxel [-1, -1, 0] .. [1, 1, 0]), Masse 9, Preis 500, Tags: basic,radiation
- Werte: cable_length=-431602080, inventory_class=3, inventory_default_item=29, seat_health_per_sec=1, type=32

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Outfit Inventory (Parachute) (`inventory_outfit_parachute`)

*An outfit inventory unit containing a single-use parachute.*
When selected, press [$[action_equipment_use]] while falling to deploy the parachute. It will then open when you are falling fast enough. Press [$[action_equipment_secondary]] to close the parachute. This parachute is single-use once equipped but can be refolded by storing it in an outfit inventory unit.

- Größe 3x3x1 Blöcke (voxel [-1, -1, 0] .. [1, 1, 0]), Masse 9, Preis 500, Tags: basic
- Werte: cable_length=-431602080, inventory_class=3, inventory_default_item=4, seat_health_per_sec=1, type=32

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Outfit Inventory (Plate Vest) (`inventory_outfit_wep_plate_vest`)

*An outfit inventory unit containing specialist millitary clothing for projectile protection.*
When equipped, damage from projectiles to the body is reduced significantly and damage to the head is greatly reduced.  Wearing the outfit significantly limits movement speed.

- Größe 3x3x1 Blöcke (voxel [-1, -1, 0] .. [1, 1, 0]), Masse 9, Preis 800, Tags: basic
- Werte: cable_length=-431602080, inventory_class=3, inventory_default_item=77, seat_health_per_sec=1, type=32

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Outfit Inventory (Scuba) (`inventory_outfit_scuba`)

*An outfit inventory unit containing specialist scuba gear.*
When equipped, it will allow diving to a depth of 40m, and provides air for 2 minutes. The air tank can be refilled by storing the gear in an outfit inventory unit with an attached air input or via space seat.

- Größe 3x3x1 Blöcke (voxel [-1, -1, 0] .. [1, 1, 0]), Masse 9, Preis 500, Tags: basic
- Werte: cable_length=-431602080, inventory_class=3, inventory_default_item=3, seat_health_per_sec=1, type=32

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |
| Fluid In | Fluessigkeit/Gas | Eingang | (0, -1, 0) |  |

## Outfit Inventory (Space Exploration) (`inventory_outfit_space_suit_exploration`)

*An outfit inventory unit containing specialist Space Exploration gear required for surviving in space. The air tank can be refilled by storing the gear in an outfit inventory unit with an attached air input or via space seat.*
When equipped, it will protect against low temperatures, low pressures and provide oxygen.

- Größe 3x3x1 Blöcke (voxel [-1, -1, 0] .. [1, 1, 0]), Masse 9, Preis 10000, Tags: space
- Werte: inventory_class=3, inventory_default_item=80, type=32

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |
| Fluid In | Fluessigkeit/Gas | Eingang | (0, -1, 0) |  |

## Outfit Inventory (Space) (`inventory_outfit_space_suit`)

*An outfit inventory unit containing specialist Space Exploration gear required for surviving in space. The air tank can be refilled by storing the gear in an outfit inventory unit with an attached air input or via space seat.*
When equipped, it will protect against low temperatures, low pressures and provide oxygen.

- Größe 3x3x1 Blöcke (voxel [-1, -1, 0] .. [1, 1, 0]), Masse 9, Preis 5000, Tags: space
- Werte: inventory_class=3, inventory_default_item=79, type=32

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |
| Fluid In | Fluessigkeit/Gas | Eingang | (0, -1, 0) |  |

## Padded Seat (`seat_padded`)

*A small padded passenger seat.*
You can get in and out of the seat by interacting with it using [$[action_use_seat]]. You can place a rescued survivor in any seat by using [$[action_use_seat]] while carrying them.

- Größe 2x4x2 Blöcke (voxel [0, 0, 0] .. [1, 3, 1]), Masse 2, Preis 25, Tags: basic,seat
- Werte: button_type=0, cable_radius=0, constraint_axis=0, door_lower_limit=0, door_upper_limit=0, dynamic_max_rotation=0, light_fov=0, light_intensity=0, light_range=0, magnet_force=0, max_motor_force=0, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, type=1, wheel_radius=0

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Occupied | An/Aus | Ausgang | (0, 0, 0) | Outputs an on signal if this seat is occupied by a character. |

## Passenger Seat (`passenger_seat`)

*A basic passenger seat.*
You can get in and out of the seat by interacting with it using [$[action_use_seat]]. You can place a rescued survivor in any seat by using [$[action_use_seat]] while carrying them.

- Größe 3x5x3 Blöcke (voxel [-1, 0, -1] .. [1, 4, 1]), Masse 20, Preis 50
- Werte: button_type=0, cable_radius=0, constraint_axis=0, door_lower_limit=0, door_upper_limit=0, dynamic_max_rotation=0, light_fov=0, light_intensity=0, light_range=0, magnet_force=0, max_motor_force=0, max_motor_speed=5, pump_pressure=0, radar_range=3, rudder_surface_area=0, type=1, wheel_radius=0

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Occupied | An/Aus | Ausgang | (0, 0, 0) | Outputs an on signal if this seat is occupied by a character. |

## Passenger Seat (`seat_passenger`)

*A basic passenger seat.*
You can get in and out of the seat by interacting with it using [$[action_use_seat]]. You can place a rescued survivor in any seat by using [$[action_use_seat]] while carrying them.

- Größe 3x5x3 Blöcke (voxel [-1, 0, -1] .. [1, 4, 1]), Masse 6, Preis 50, Tags: basic,seat
- Werte: button_type=0, cable_radius=0, constraint_axis=0, door_lower_limit=0, door_upper_limit=0, dynamic_max_rotation=0, light_fov=0, light_intensity=0, light_range=0, magnet_force=0, max_motor_force=0, max_motor_speed=5, pump_pressure=0, radar_range=3, rudder_surface_area=0, type=1, wheel_radius=0

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Occupied | An/Aus | Ausgang | (0, 0, 0) | Outputs an on signal if this seat is occupied by a character. |

## RCS Thruster (`rcs_thruster`)

*A fluid jet that fires pressurized air for altitude control and translation.*
The reaction control system can fire in 4 non-cardinal directions resulting in 5 directions of motion. RCS thrusters also have body relative activation modes where thrusters will collaborate from different orientations to achieve the desired translation or rotation. The RCS thruster also has positional and rotational stabilization toggles.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 140
- Werte: type=24, water_component_type=29

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Composite Input | Composite | Eingang | (0, 0, 0) | Composite bool channels: 1:Component X+, 2:Component X-, 3:Component Z+, 4:Component Z-, 5:Enable position stabilization, 6:Enable rotation stabilization, 7:Body X+, 8:Body X-, 9:Body Y+, 10:Body Y-, 11:Body Z+, 12:Body Z-, 13:Body Rotate X+, 14:Body Rotate X-, 15:Body Rotate Y+, 16:Body Rotate Y-, 17:Body Rotate Z+, 18:Body Rotate Z- |
| Fluid Supply | Fluessigkeit/Gas | Eingang | (0, 0, 0) | The fluid input to output from the thruster. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Rope Anchor (`rope_hook`)

*An anchor point for a basic rope.*
Draw a rope logic link between two Rope Anchors to form a rope.

- Größe 1x2x1 Blöcke (voxel [0, 0, 0] .. [0, 1, 0]), Masse 1, Preis 15, Tags: basic
- Werte: force_emitter_blade_physics_length=4.1, force_emitter_default_pitch=1, force_emitter_max_force=10000, type=48

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Rope Node | Seil/Munition | Eingang | (0, 1, 0) |  |
| Detach Rope | An/Aus | Eingang | (0, 0, 0) |  |

## Rope Pulley (`winch_pulley`)

*A pulley that changes attached rope lengths based on forces applied to ropes.*
Draw a rope logic link between two rope nodes to form a rope. Ropes will slide based on difference in force applied to each rope.

- Größe 3x1x3 Blöcke (voxel [-1, 0, -1] .. [1, 0, 1]), Masse 25, Preis 250, Tags: basic
- Werte: cable_length=150, cable_radius=0.05, logic_gate_subtype=5, type=48
- Zweiter Körper (Gelenk) bei [0, 3, 2]

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Rope 1 Length | Zahl | Ausgang | (1, 0, 0) | The current length of rope 1 in metres. |
| Rope 2 Length | Zahl | Ausgang | (-1, 0, 0) | The current length of rope 2 in metres. |
| Rope 2 | Seil/Munition | Eingang | (-1, 0, 1) |  |
| Rope 1 | Seil/Munition | Eingang | (1, 0, 1) |  |

## Rope Pulley (Corner) (`winch_pulley_corner`)

*A pulley that changes attached rope lengths based on forces applied to ropes.*
Draw a rope logic link between two rope nodes to form a rope. Ropes will slide based on difference in force applied to each rope.

- Größe 3x1x3 Blöcke (voxel [-1, 0, -1] .. [1, 0, 1]), Masse 25, Preis 250, Tags: basic
- Werte: cable_length=150, cable_radius=0.05, logic_gate_subtype=5, type=48
- Zweiter Körper (Gelenk) bei [0, 3, 2]

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Rope 1 Length | Zahl | Ausgang | (1, 0, 0) | The current length of rope 1 in metres. |
| Rope 2 Length | Zahl | Ausgang | (0, 0, -1) | The current length of rope 2 in metres. |
| Rope 2 | Seil/Munition | Eingang | (-1, 0, -1) |  |
| Rope 1 | Seil/Munition | Eingang | (1, 0, 1) |  |

## Rotating Light (`rotating_light`)

*A rotating light that can be controlled using an on/off signal.*

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 50, Tags: beacon,warning
- Werte: composite_type=3, dynamic_min_rotation=-3.141593, light_fov=0.4, light_range=120, light_type=1, type=11

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Light Switch | An/Aus | Eingang | (0, 0, 0) | Controls whether or not the light is switched on. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Saddle Passenger Seat (`seat_saddle_passenger`)

*A small padded passenger seat.*
You can get in and out of the seat by interacting with it using [$[action_use_seat]]. You can place a rescued survivor in any seat by using [$[action_use_seat]] while carrying them.

- Größe 3x4x2 Blöcke (voxel [-1, 0, -1] .. [1, 3, 0]), Masse 3, Preis 25, Tags: basic,seat
- Werte: cable_radius=0, rudder_surface_area=0, type=1

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Occupied | An/Aus | Ausgang | (0, 0, -1) | Outputs an on signal if the seat is occupied by a character. |

## Sail Anchor (`rope_hook_sail`)

*An anchor point for a sail.*
Draw a rope logic link between four Sail Anchors in a loop to form a sail. A sail will convert force from the wind to the direction of the sail facing. The sail force is strongest when fully facing the wind to act as a parachute, but also has a strong force when facing slightly off a right-angle from the wind to act as a wing. A keel is recommended for sailboats to apply sail forces in a useful direction.

- Größe 1x2x1 Blöcke (voxel [0, 0, 0] .. [0, 1, 0]), Masse 3, Preis 50, Tags: basic
- Werte: force_emitter_blade_physics_length=4.1, force_emitter_default_pitch=1, force_emitter_max_force=10000, logic_gate_subtype=10, type=48

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Sail Node | Seil/Munition | Eingang | (0, 1, 0) |  |
| Take In/Out Sails | An/Aus | Eingang | (0, 1, 0) | While active, allows the ropes forming the sail to spool freely. |

## Search Light (`searchlight`)

*A spotlight that can be rotated up and down.*
The light has a standard value input that sets the target orientation within the its range of motion. It can rotate a quarter turn in both directions. An on/off signal is used to switch the light on and off. It has a range of 120m.

- Größe 3x3x3 Blöcke (voxel [-1, -1, -1] .. [1, 1, 1]), Masse 20, Preis 30, Tags: spotlight,basic
- Werte: cable_radius=0.02, door_lower_limit=0, door_upper_limit=0, dynamic_max_rotation=6.28, dynamic_min_rotation=3.14, light_fov=0.4, light_intensity=7, light_range=120, light_type=1, magnet_force=0, max_motor_force=0, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, type=11

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Light Switch | An/Aus | Eingang | (1, 0, 0) | Controls whether or not the light is switched on. |
| Rotation | Zahl | Eingang | (0, 0, -1) | Standard value between -1 and 1 representing the target orientation of the light. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Siren (`siren`)

*A warning siren with a large audible range.*
It has an audible range of 3000m.

- Größe 3x3x5 Blöcke (voxel [-1, -1, -2] .. [1, 1, 2]), Masse 5, Preis 200, Tags: sound,audio
- Werte: indicator_type=11, type=21

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Horn | An/Aus | Eingang | (0, 0, 0) | Sounds the horn when recieving an on signal. |
| Electric | Strom | Eingang | (0, -1, 0) | Electrical power connection. |

## Small equipment inventory (Empty) (`inventory_small`)

*An empty small equipment storage unit.*
Only small handheld equipment can be stored in this unit. When connected to an electric power source, any rechargable equipment stored in the unit will drain a small amount of electricity until recharged to 100% capacity.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 50, Tags: basic
- Werte: cable_length=-431602080, inventory_class=1, seat_health_per_sec=1, type=32

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Small Spotlight (Block) (`searchlight_small`)

*A small spotlight that can be controlled using an on/off signal.*
It has a range of 60m. Can be pivoted up to 0.125 turns using composite input.

- Größe 1x2x1 Blöcke (voxel [0, 0, 0] .. [0, 1, 0]), Masse 1, Preis 20
- Werte: light_fov=0.698132, light_intensity=3.5, light_range=60, light_type=1, rudder_surface_area=0, type=10

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Light Switch | An/Aus | Eingang | (0, 0, 0) | Controls whether or not the light is switched on. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |
| Pivot | Composite | Eingang | (0, 0, 0) | Inputs for spotlight X/Y pivot. (Value 1 : Pivot X) (Value 2 : Pivot Y) |

## Small Spotlight (Mounted) (`searchlight_small_2`)

*A small spotlight that can be controlled using an on/off signal.*
It has a range of 60m. Can be pivoted up to 0.125 turns using composite input.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 20
- Werte: light_fov=0.698132, light_intensity=3.5, light_range=60, light_type=1, rudder_surface_area=0, type=10

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Light Switch | An/Aus | Eingang | (0, 0, 0) | Controls whether or not the light is switched on. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |
| Pivot | Composite | Eingang | (0, 0, 0) | Inputs for spotlight X/Y pivot. (Value 1 : Pivot X) (Value 2 : Pivot Y) |

## Small Winch (`rope_hook_winch_small`)

*A mechanical winch that can transfer electric/fluid through an attached cable, with an extension length of 10m.*
Draw a rope logic link between two Rope Nodes to form a cable. Can be extended and retracted.

- Größe 1x2x1 Blöcke (voxel [0, -1, 0] .. [0, 0, 0]), Masse 10, Preis 100
- Werte: cable_length=10, force_emitter_blade_physics_length=4.1, force_emitter_default_pitch=1, force_emitter_max_force=10000, logic_gate_subtype=3, type=48
- Zweiter Körper (Gelenk) bei [0, 0, 2]

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Down | An/Aus | Eingang | (0, 0, 0) | Lowers the winch cable down when receiving an on signal. |
| Up | An/Aus | Eingang | (0, -1, 0) | Raises the winch cable up when receiving an on signal. |
| Rope Node | Seil/Munition | Eingang | (0, 0, 0) |  |
| Electric Node | Strom | Eingang | (0, -1, 0) |  |
| Fluid | Fluessigkeit/Gas | Ausgang | (0, -1, 0) | Fluid connection for the hose coil. |

## Small Winch (`winch_electric`)

*A building block attached to the end of a 10m mechanical winch that can be raised and lowered.*
The winch is operated electrically, and outputs its current length.

- Größe 1x2x1 Blöcke (voxel [0, -1, 0] .. [0, 0, 0]), Masse 10, Preis 100
- Werte: cable_length=10, cable_radius=0.02, child_name=winch_electric_b, constraint_axis=2, constraint_range_of_motion=10, constraint_type=1, seat_health_per_sec=1, type=20
- Zweiter Körper (Gelenk) bei [0, 0, 2]

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Up | An/Aus | Eingang | (0, -1, 0) |  |
| Down | An/Aus | Eingang | (0, 0, 0) |  |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |
| Fluid | Fluessigkeit/Gas | Ausgang | (0, -1, 0) | Fluid connection for the hose coil. |

## Sonar Noisemaker (`sonar_jammer`)

*A distracting device for sonar.*
Emits a very loud noise at an inaudible frequency when activated, as a decoy or distraction for sonar components that are listening passively.

- Größe 1x1x3 Blöcke (voxel [0, 0, -1] .. [0, 0, 1]), Masse 1, Preis 250
- Werte: logic_gate_type=60, radar_range=5000, rudder_surface_area=0, type=16

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Enable | An/Aus | Eingang | (0, 0, 0) | Enable the noisemaker. |
| Electric | Strom | Eingang | (0, 0, 1) | Electrical connection. |

## Stretcher (`seat_stretcher`)

*A strecher that connects below an attachment point.*
You can get in and out of the stretcher by interacting with it using [$[action_use_seat]]. You can place a rescued survivor in any stretcher by using [$[action_use_seat]] while carrying them.

- Größe 3x3x7 Blöcke (voxel [-1, 0, -3] .. [1, 2, 3]), Masse 80, Preis 250, Tags: basic
- Werte: button_type=0, cable_radius=0, constraint_axis=0, door_lower_limit=0, door_upper_limit=0, dynamic_max_rotation=0, light_fov=0, light_intensity=0, light_range=0, magnet_force=0, max_motor_force=0, max_motor_speed=5, rudder_surface_area=0, seat_pose=3, type=1, wheel_radius=0

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Occupied | An/Aus | Ausgang | (0, 0, 0) | Outputs an on signal if this bed is occupied by a character. |

## Transponder (`transponder`)

*An emergency search and rescue transponder.*
When activated, emits a continuous transponder signal that can be detected over great distances by any transponder locator.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 20, Tags: basic,mission
- Werte: cable_length=0, cable_radius=0.02, light_intensity=0, logic_gate_type=54, magnet_force=0, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, type=16

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |
| Active | An/Aus | Eingang | (0, 0, 0) | Emit a continuous transponder signal when active. |

## Vehicle Parachute (`parachute`)

*A single-use parachute that can be deployed to reduce a vehicle's velocity.*
The parachute will deploy when receiving an on signal, and will close when not. Once deployed, it will open at a speed of 20m/s and stall when it drops below 5m/s. Once opened, the single use will be consumed and it must be returned to a workbench to be refolded. The size of the parachute can be customised by selecting this component with the select tool.

- Größe 3x1x3 Blöcke (voxel [-1, 0, -1] .. [1, 0, 1]), Masse 5, Preis 500
- Werte: button_type=0, cable_radius=0.02, constraint_axis=0, door_lower_limit=0, door_upper_limit=0, dynamic_max_rotation=0, force_emitter_max_vector=0, light_fov=0, light_intensity=0, light_range=0, magnet_force=0, max_motor_force=0, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, type=35, wheel_radius=0

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Deploy | An/Aus | Eingang | (0, 0, 0) | Deploy the parachute. The parachute will close when it stalls or stops receiving an on signal. |

## winch end (`water_hose_b`)


- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 20, Preis 0
- Werte: cable_length=0, cable_radius=0, light_intensity=0, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, type=7

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Fluid | Fluessigkeit/Gas | Ausgang | (0, 0, 0) | Fluid connection for the end of the hose. |

## winch end (`winch_b`)


- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 20, Preis 0
- Werte: cable_length=0, cable_radius=0, light_intensity=0, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, type=7

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Fluid | Fluessigkeit/Gas | Ausgang | (0, 0, 0) | Fluid connection for the end of the hose. |

## winch end (`winch_electric_b`)


- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 20, Preis 0
- Werte: cable_length=0, cable_radius=0, light_intensity=0, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, type=7

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Fluid | Fluessigkeit/Gas | Ausgang | (0, 0, 0) | Fluid connection for the end of the hose. |

## winch end (`winch_huge_b`)


- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 20, Preis 0
- Werte: cable_length=0, cable_radius=0, light_intensity=0, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, type=7

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Fluid | Fluessigkeit/Gas | Ausgang | (0, 0, 0) | Fluid connection for the end of the hose. |

## winch end (`winch_large_b`)


- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 20, Preis 0
- Werte: cable_length=0, cable_radius=0, light_intensity=0, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, type=7

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Fluid | Fluessigkeit/Gas | Ausgang | (0, 0, 0) | Fluid connection for the end of the hose. |
