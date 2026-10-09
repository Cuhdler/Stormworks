# Bloecke (Kategorie 0)

Aus den Spieldaten erzeugt von `tools/bauteile_holen.py` - nicht von Hand ändern.

## Block (`01_block`)

*Basic cube-shaped building block.*
The block is a quarter-metre in size. Components can be attached to all 6 faces.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 2, Tags: basic
- Werte: buoy_factor=1.000000, buoy_force=100.000000, buoy_radius=1.000000, button_type=0, constraint_axis=0, constraint_range_of_motion=0.000000, door_lower_limit=0.000000, door_upper_limit=0.000000, dynamic_max_rotation=0.000000, dynamic_min_rotation=0.000000, engine_max_force=1000.000000, force_emitter_max_force=1000.000000, force_emitter_max_vector=0.000000, light_fov=0.000000, light_intensity=0.000000, light_range=0.000000, magnet_force=0.000000, max_motor_force=0.000000, rudder_surface_area=0.000000, type=0, wheel_radius=0.000000

## Inverse Pyramid (`04_invpyramid`)

*Basic inverse pyramid-shaped building block.*
Components can be attached to all faces, with the exception of the triangular face. Inverse pyramids are useful for closing gaps between perpendicular lines of wedge and pyramid blocks.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 0.75, Preis 2, Tags: basic
- Werte: block_type=3, button_type=0, cable_radius=0, constraint_axis=0, door_lower_limit=0, door_upper_limit=0, dynamic_max_rotation=0, force_emitter_max_vector=0, light_fov=0, light_intensity=0, light_range=0, magnet_force=0, max_motor_force=0, max_motor_speed=5, rudder_surface_area=0, type=0, wheel_radius=0

## Inverse Pyramid 1x2 (`07_invpyramid_2`)

*1x2 inverse pyramid-shaped building block.*
Components can be attached to all faces, with the exception of the triangular face. Inverse pyramids are useful for closing gaps between perpendicular lines of wedge and pyramid blocks.

- Größe 1x1x2 Blöcke (voxel [0, 0, -1] .. [0, 0, 0]), Masse 1.5, Preis 2, Tags: basic
- Werte: block_type=6, button_type=0, cable_radius=0, constraint_axis=0, door_lower_limit=0, door_upper_limit=0, dynamic_max_rotation=0, force_emitter_max_vector=0, light_fov=0, light_intensity=0, light_range=0, magnet_force=0, max_motor_force=0, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, type=0, wheel_radius=0

## Inverse Pyramid 1x4 (`10_invpyramid_4`)

*1x4 inverse pyramid-shaped building block.*
Components can be attached to all faces, with the exception of the triangular face. Inverse pyramids are useful for closing gaps between perpendicular lines of wedge and pyramid blocks.

- Größe 1x1x4 Blöcke (voxel [0, 0, -3] .. [0, 0, 0]), Masse 3, Preis 4, Tags: basic
- Werte: block_type=9, button_type=0, cable_radius=0, constraint_axis=0, door_lower_limit=0, door_upper_limit=0, dynamic_max_rotation=0, force_emitter_max_vector=0, light_fov=0, light_intensity=0, light_range=0, magnet_force=0, max_motor_force=0, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, type=0, wheel_radius=0

## Inverse Pyramid 2x2 (`14_invpyramid_2x2`)

*2x2 inverse pyramid-shaped building block.*
Components can be attached to all faces, with the exception of the triangular face. Pyramids can act as a corner-piece for perpendicular lines of wedge blocks.

- Größe 2x1x2 Blöcke (voxel [-1, 0, -1] .. [0, 0, 0]), Masse 3, Preis 4, Tags: basic
- Werte: block_type=13, button_type=0, cable_radius=0, constraint_axis=0, door_lower_limit=0, door_upper_limit=0, dynamic_max_rotation=0, force_emitter_max_vector=0, light_fov=0, light_intensity=0, light_range=0, magnet_force=0, max_motor_force=0, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, type=0, wheel_radius=0

## Inverse Pyramid 2x4 (`15_invpyramid_2x4`)

*2x4 inverse pyramid-shaped building block.*
Components can be attached to all faces, with the exception of the triangular face. Pyramids can act as a corner-piece for perpendicular lines of wedge blocks.

- Größe 2x1x4 Blöcke (voxel [-1, 0, -3] .. [0, 0, 0]), Masse 6, Preis 8, Tags: basic
- Werte: block_type=14, button_type=0, cable_radius=0, constraint_axis=0, door_lower_limit=0, door_upper_limit=0, dynamic_max_rotation=0, force_emitter_max_vector=0, light_fov=0, light_intensity=0, light_range=0, magnet_force=0, max_motor_force=0, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, type=0, wheel_radius=0

## Inverse Pyramid 4x4 (`16_invpyramid_4x4`)

*4x4 inverse pyramid-shaped building block.*
Components can be attached to all faces, with the exception of the triangular face. Pyramids can act as a corner-piece for perpendicular lines of wedge blocks.

- Größe 4x1x4 Blöcke (voxel [-3, 0, -3] .. [0, 0, 0]), Masse 12, Preis 16, Tags: basic
- Werte: block_type=15, button_type=0, cable_radius=0, constraint_axis=0, door_lower_limit=0, door_upper_limit=0, dynamic_max_rotation=0, force_emitter_max_vector=0, light_fov=0, light_intensity=0, light_range=0, magnet_force=0, max_motor_force=0, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, type=0, wheel_radius=0

## Ladder (`ladder_small`)

*Single ladder rung. Multiple rungs can placed on top of each other to form a ladder of abitrary length.*
You can attach to the ladder by interacting with [$[action_use_seat]], then detach again with either [$[action_use_seat]] or [$[action_jump]]. You will automatically detach from the ladder when you reach the top.

- Größe 3x4x1 Blöcke (voxel [-1, 0, 0] .. [1, 3, 0]), Masse 3, Preis 5, Tags: basic
- Werte: buoy_factor=1.000000, buoy_force=100.000000, buoy_radius=1.000000, constraint_range_of_motion=0.000000, door_lower_limit=-1.000000, door_upper_limit=1.000000, dynamic_min_rotation=0.000000, engine_max_force=1000.000000, force_emitter_max_force=1000.000000, force_emitter_max_vector=1.000000, light_fov=1.000000, light_intensity=0.000000, light_range=1.000000, magnet_force=1.000000, max_motor_force=100.000000, rudder_surface_area=0.000000, type=19, wheel_radius=0.250000

## Physics Flooder (`physics_flooder`)

*A device that floods an enclosed volume with physics for optimisation.*
Floods an enclosed volume with massless physics, allowing for physics shape optimisation without comprimising vehicle integrity.

- Größe 1x2x1 Blöcke (voxel [0, 0, 0] .. [0, 1, 0]), Masse 1, Preis 20
- Werte: cable_radius=0.02, max_motor_speed=5, pump_pressure=0, type=24, water_component_type=19

## Pipe Angle (`trans_angle`)

*An angled pipe for transferring to components from an engine.*

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 5, Tags: basic
- Werte: buoy_factor=0.5, buoy_force=1, button_type=0, cable_radius=0.02, constraint_axis=0, door_lower_limit=0, door_upper_limit=0, dynamic_max_rotation=0, engine_max_force=200, force_emitter_max_force=950, force_emitter_max_vector=0, light_fov=0, light_intensity=0, light_range=0, magnet_force=0, max_motor_force=0, max_motor_speed=5, pump_pressure=0, trans_conn_type=1, type=6, wheel_radius=0

## Pipe Angle (Enclosed) (`trans_block_angle`)

*An angled pipe for transferring to components from an engine.*

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 5
- Werte: buoy_factor=0.5, buoy_force=1, button_type=0, cable_radius=0.02, constraint_axis=0, door_lower_limit=0, door_upper_limit=0, dynamic_max_rotation=0, engine_max_force=200, force_emitter_max_force=950, force_emitter_max_vector=0, light_fov=0, light_intensity=0, light_range=0, magnet_force=0, max_motor_force=0, max_motor_speed=5, pump_pressure=0, trans_conn_type=1, type=6, wheel_radius=0

## Pipe Cross (Enclosed) (`trans_block_cross`)

*An X-shaped pipe segment that can be used to branch piping into four directions.*

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 5
- Werte: buoy_factor=0.5, buoy_force=1, button_type=0, cable_radius=0.02, constraint_axis=0, door_lower_limit=0, door_upper_limit=0, dynamic_max_rotation=0, engine_max_force=200, force_emitter_max_force=950, force_emitter_max_vector=0, light_fov=0, light_intensity=0, light_range=0, magnet_force=0, max_motor_force=0, max_motor_speed=5, pump_pressure=0, trans_conn_type=1, type=6, wheel_radius=0

## Pipe Cross Corner (Enclosed) (`trans_block_cross_corner`)

*An X-shaped pipe segment that can be used to branch piping into five directions.*

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 5, Tags: basic
- Werte: buoy_factor=0.5, buoy_force=1, button_type=0, cable_radius=0.02, constraint_axis=0, door_lower_limit=0, door_upper_limit=0, dynamic_max_rotation=0, engine_max_force=200, force_emitter_max_force=950, force_emitter_max_vector=0, light_fov=0, light_intensity=0, light_range=0, magnet_force=0, max_motor_force=0, max_motor_speed=5, pump_pressure=0, trans_conn_type=1, type=6, wheel_radius=0

## Pipe Omni (Enclosed) (`trans_block_omni`)

*An omnidirectional pipe segment.*

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 5
- Werte: buoy_factor=0.5, buoy_force=1, button_type=0, cable_radius=0.02, constraint_axis=0, door_lower_limit=0, door_upper_limit=0, dynamic_max_rotation=0, engine_max_force=200, force_emitter_max_force=950, force_emitter_max_vector=0, light_fov=0, light_intensity=0, light_range=0, magnet_force=0, max_motor_force=0, max_motor_speed=5, pump_pressure=0, trans_conn_type=1, type=6, wheel_radius=0

## Pipe Straight (`trans_straight`)

*A straight section of pipe for transferring to components from an engine.*

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 5, Tags: basic
- Werte: buoy_factor=0.5, buoy_force=1, button_type=0, cable_radius=0.02, constraint_axis=0, door_lower_limit=0, door_upper_limit=0, dynamic_max_rotation=0, engine_max_force=200, force_emitter_max_force=950, force_emitter_max_vector=0, light_fov=0, light_intensity=0, light_range=0, magnet_force=0, max_motor_force=0, max_motor_speed=5, pump_pressure=0, type=6, wheel_radius=0

## Pipe Straight (Enclosed) (`trans_block_straight`)

*A straight section of pipe for transferring to components from an engine.*

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 5
- Werte: buoy_factor=0.5, buoy_force=1, button_type=0, cable_radius=0.02, constraint_axis=0, door_lower_limit=0, door_upper_limit=0, dynamic_max_rotation=0, engine_max_force=200, force_emitter_max_force=950, force_emitter_max_vector=0, light_fov=0, light_intensity=0, light_range=0, magnet_force=0, max_motor_force=0, max_motor_speed=5, pump_pressure=0, type=6, wheel_radius=0

## Pipe T-Piece Corner (Enclosed) (`trans_block_t_corner`)

*A T-shaped pipe segment that can be used to branch piping into four directions.*

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 5
- Werte: buoy_factor=0.5, buoy_force=1, button_type=0, cable_radius=0.02, constraint_axis=0, door_lower_limit=0, door_upper_limit=0, dynamic_max_rotation=0, engine_max_force=200, force_emitter_max_force=950, force_emitter_max_vector=0, light_fov=0, light_intensity=0, light_range=0, magnet_force=0, max_motor_force=0, max_motor_speed=5, pump_pressure=0, trans_conn_type=1, type=6, wheel_radius=0

## Pivot (`multibody_pivot_b`)


- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 0
- Werte: buoy_factor=1.000000, buoy_force=100.000000, buoy_radius=1.000000, button_type=0, constraint_axis=0, constraint_range_of_motion=0.000000, door_lower_limit=0.000000, door_upper_limit=0.000000, dynamic_max_rotation=0.000000, dynamic_min_rotation=0.000000, engine_max_force=1000.000000, force_emitter_max_force=1000.000000, force_emitter_max_vector=1.000000, light_fov=0.000000, light_intensity=0.000000, light_range=0.000000, magnet_force=0.000000, max_motor_force=0.000000, rudder_surface_area=0.000000, type=7, wheel_radius=0.000000

## Pyramid (`03_pyramid`)

*Basic pyramid-shaped building block.*
Components can be attached to all faces, with the exception of the triangular face. Pyramids can act as a corner-piece for perpendicular lines of wedge blocks.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 0.25, Preis 2, Tags: basic
- Werte: block_type=2, button_type=0, cable_radius=0, constraint_axis=0, door_lower_limit=0, door_upper_limit=0, dynamic_max_rotation=0, force_emitter_max_vector=0, light_fov=0, light_intensity=0, light_range=0, magnet_force=0, max_motor_force=0, max_motor_speed=5, rudder_surface_area=0, type=0, wheel_radius=0

## Pyramid 1x2 (`06_pyramid_2`)

*1x2 pyramid-shaped building block.*
Components can be attached to all faces, with the exception of the triangular face. Pyramids can act as a corner-piece for perpendicular lines of wedge blocks.

- Größe 1x1x2 Blöcke (voxel [0, 0, -1] .. [0, 0, 0]), Masse 0.5, Preis 2, Tags: basic
- Werte: block_type=5, button_type=0, cable_radius=0.02, constraint_axis=0, door_lower_limit=0, door_upper_limit=0, dynamic_max_rotation=0, force_emitter_max_vector=0, light_fov=0, light_intensity=0, light_range=0, magnet_force=0, max_motor_force=0, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, type=0, wheel_radius=0

## Pyramid 1x4 (`09_pyramid_4`)

*1x4 pyramid-shaped building block.*
Components can be attached to all faces, with the exception of the triangular face. Pyramids can act as a corner-piece for perpendicular lines of wedge blocks.

- Größe 1x1x4 Blöcke (voxel [0, 0, -3] .. [0, 0, 0]), Masse 1, Preis 4, Tags: basic
- Werte: block_type=8, button_type=0, cable_radius=0, constraint_axis=0, door_lower_limit=0, door_upper_limit=0, dynamic_max_rotation=0, force_emitter_max_vector=0, light_fov=0, light_intensity=0, light_range=0, magnet_force=0, max_motor_force=0, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, type=0, wheel_radius=0

## Pyramid 2x2 (`11_pyramid_2x2`)

*2x2 pyramid-shaped building block.*
Components can be attached to all faces, with the exception of the triangular face. Pyramids can act as a corner-piece for perpendicular lines of wedge blocks.

- Größe 2x1x2 Blöcke (voxel [-1, 0, -1] .. [0, 0, 0]), Masse 1, Preis 4, Tags: basic
- Werte: block_type=10, button_type=0, cable_radius=0, constraint_axis=0, door_lower_limit=0, door_upper_limit=0, dynamic_max_rotation=0, force_emitter_max_vector=0, light_fov=0, light_intensity=0, light_range=0, magnet_force=0, max_motor_force=0, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, type=0, wheel_radius=0

## Pyramid 2x4 (`12_pyramid_2x4`)

*2x4 pyramid-shaped building block.*
Components can be attached to all faces, with the exception of the triangular face. Pyramids can act as a corner-piece for perpendicular lines of wedge blocks.

- Größe 2x1x4 Blöcke (voxel [-1, 0, -3] .. [0, 0, 0]), Masse 2, Preis 8, Tags: basic
- Werte: block_type=11, button_type=0, cable_radius=0, constraint_axis=0, door_lower_limit=0, door_upper_limit=0, dynamic_max_rotation=0, force_emitter_max_vector=0, light_fov=0, light_intensity=0, light_range=0, magnet_force=0, max_motor_force=0, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, type=0, wheel_radius=0

## Pyramid 4x4 (`13_pyramid_4x4`)

*4x4 pyramid-shaped building block.*
Components can be attached to all faces, with the exception of the triangular face. Pyramids can act as a corner-piece for perpendicular lines of wedge blocks.

- Größe 4x1x4 Blöcke (voxel [-3, 0, -3] .. [0, 0, 0]), Masse 4, Preis 16, Tags: basic
- Werte: block_type=12, button_type=0, cable_radius=0, constraint_axis=0, door_lower_limit=0, door_upper_limit=0, dynamic_max_rotation=0, force_emitter_max_vector=0, light_fov=0, light_intensity=0, light_range=0, magnet_force=0, max_motor_force=0, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, type=0, wheel_radius=0

## Robotic Pivot (`multibody_robotic_pivot_01_b`)


- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 0
- Werte: button_type=0, cable_radius=0.02, door_lower_limit=0, door_upper_limit=0, dynamic_max_rotation=0, light_fov=0, light_intensity=0, light_range=0, magnet_force=0, max_motor_force=0, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, type=7, wheel_radius=0

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| RPS | Drehmoment | Eingang | (0, 0, 0) | Power connection for transfering mechanical energy. |

## Robotic Pivot (`multibody_robotic_pivot_01_b_fluid`)


- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 0
- Werte: button_type=0, cable_radius=0.02, door_lower_limit=0, door_upper_limit=0, dynamic_max_rotation=0, light_fov=0, light_intensity=0, light_range=0, magnet_force=0, max_motor_force=0, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, type=7, wheel_radius=0

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Fluid | Fluessigkeit/Gas | Eingang | (0, 0, 0) | Fluid connection for transfering fluids. |

## Robotic Pivot (`multibody_velocity_pivot_b`)


- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 0
- Werte: button_type=0, cable_radius=0.02, door_lower_limit=0, door_upper_limit=0, dynamic_max_rotation=0, light_fov=0, light_intensity=0, light_range=0, magnet_force=0, max_motor_force=0, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, type=7, wheel_radius=0

## Stair Step (`stair_segment`)

*A single step that can be stacked to create a staircase.*

- Größe 3x1x2 Blöcke (voxel [0, 0, -1] .. [2, 0, 0]), Masse 6, Preis 20, Tags: basic
- Werte: buoy_factor=1.000000, buoy_force=100.000000, buoy_radius=1.000000, constraint_range_of_motion=0.000000, door_lower_limit=-1.000000, door_upper_limit=1.000000, dynamic_min_rotation=0.000000, engine_max_force=1000.000000, force_emitter_max_force=1000.000000, force_emitter_max_vector=1.000000, light_fov=1.000000, light_intensity=1.000000, light_range=1.000000, magnet_force=1.000000, max_motor_force=100.000000, rudder_surface_area=1.000000, type=9, wheel_radius=0.250000

## Stair Top (`stair_top`)

*A single step that can be used at the top of a staircase to make it flush with a platform.*

- Größe 3x1x2 Blöcke (voxel [0, 0, -1] .. [2, 0, 0]), Masse 6, Preis 20, Tags: step,basic
- Werte: cable_radius=0.02, max_motor_speed=5, pump_pressure=0, type=9

## Static Block (`01_block_static`)

*Static root block used as a base for all vehicles.*
This block cannot be removed.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 10
- Werte: button_type=0, cable_length=0, cable_radius=0.02, constraint_axis=0, door_lower_limit=0, door_upper_limit=0, dynamic_max_rotation=0, force_emitter_max_vector=0, light_fov=0, light_intensity=0, light_range=0, magnet_force=0, max_motor_force=0, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, type=0, wheel_radius=0

## Turret Ring (Large) (`multibody_turret_large_b`)


- Größe 9x1x9 Blöcke (voxel [-4, 0, 0] .. [4, 0, 8]), Masse 36, Preis 0
- Werte: button_type=0, cable_radius=0.02, door_lower_limit=0, door_side_dist=6, door_up_dist=6, door_upper_limit=0, dynamic_max_rotation=0, light_fov=0, light_intensity=0, light_range=0, magnet_force=0, max_motor_force=0, max_motor_speed=0.5, pump_pressure=0, rudder_surface_area=0, type=7, wheel_radius=0

## Turret Ring (Medium) (`multibody_turret_medium_b`)


- Größe 7x1x7 Blöcke (voxel [-3, 0, 0] .. [3, 0, 6]), Masse 22, Preis 0
- Werte: button_type=0, cable_radius=0.02, door_lower_limit=0, door_side_dist=4, door_up_dist=4, door_upper_limit=0, dynamic_max_rotation=0, light_fov=0, light_intensity=0, light_range=0, magnet_force=0, max_motor_force=0, max_motor_speed=1, pump_pressure=0, rudder_surface_area=0, type=7, wheel_radius=0

## Turret Ring (Small) (`multibody_turret_small_b`)


- Größe 5x1x5 Blöcke (voxel [-2, 0, 0] .. [2, 0, 4]), Masse 14, Preis 0
- Werte: button_type=0, cable_radius=0.02, door_lower_limit=0, door_side_dist=2, door_up_dist=2, door_upper_limit=0, dynamic_max_rotation=0, light_fov=0, light_intensity=0, light_range=0, magnet_force=0, max_motor_force=0, max_motor_speed=2, pump_pressure=0, rudder_surface_area=0, type=7, wheel_radius=0

## Velocity Pivot (`multibody_velocity_pivot_01_b_fluid`)


- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 0
- Werte: button_type=0, cable_radius=0.02, door_lower_limit=0, door_upper_limit=0, dynamic_max_rotation=0, light_fov=0, light_intensity=0, light_range=0, magnet_force=0, max_motor_force=0, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, type=7, wheel_radius=0

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Fluid | Fluessigkeit/Gas | Eingang | (0, 0, 0) | Fluid connection for transfering fluids. |

## Velocity Pivot (`multibody_velocity_pivot_01_b_torque`)


- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 0
- Werte: button_type=0, cable_radius=0.02, door_lower_limit=0, door_upper_limit=0, dynamic_max_rotation=0, light_fov=0, light_intensity=0, light_range=0, magnet_force=0, max_motor_force=0, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, type=7, wheel_radius=0

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| RPS | Drehmoment | Eingang | (0, 0, 0) | Power connection for transfering mechanical energy. |

## Wedge (`02_wedge`)

*Basic wedge-shaped building block.*
Components can be attached to all faces, with the exception of the sloped face.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 0.5, Preis 2, Tags: basic
- Werte: block_type=1, button_type=0, cable_radius=0.02, constraint_axis=0, door_lower_limit=0, door_upper_limit=0, dynamic_max_rotation=0, force_emitter_max_vector=0, light_fov=0, light_intensity=0, light_range=0, magnet_force=0, max_motor_force=0, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, type=0, wheel_radius=0

## Wedge 1x2 (`05_wedge_2`)

*1x2 wedge-shaped building block.*
Components can be attached to all faces, with the exception of the sloped face.

- Größe 1x1x2 Blöcke (voxel [0, 0, -1] .. [0, 0, 0]), Masse 1, Preis 2, Tags: basic
- Werte: block_type=4, button_type=0, cable_radius=0.02, constraint_axis=0, door_lower_limit=0, door_upper_limit=0, dynamic_max_rotation=0, force_emitter_max_vector=0, light_fov=0, light_intensity=0, light_range=0, magnet_force=0, max_motor_force=0, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, type=0, wheel_radius=0

## Wedge 1x4 (`08_wedge_4`)

*1x4 wedge-shaped building block.*
Components can be attached to all faces, with the exception of the sloped face.

- Größe 1x1x4 Blöcke (voxel [0, 0, -3] .. [0, 0, 0]), Masse 2, Preis 4, Tags: basic
- Werte: block_type=7, button_type=0, cable_radius=0.02, constraint_axis=0, door_lower_limit=0, door_upper_limit=0, dynamic_max_rotation=0, force_emitter_max_vector=0, light_fov=0, light_intensity=0, light_range=0, magnet_force=0, max_motor_force=0, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, type=0, wheel_radius=0

## Weight Block (`01_block_weight`)

*Basic cube-shaped building block with an increased mass.*
Weight blocks have a larger impact on the vehicle's centre of mass, making them useful for balance and stability.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 10, Preis 5, Tags: basic
- Werte: buoy_factor=1.000000, buoy_force=100.000000, buoy_radius=1.000000, button_type=0, constraint_axis=0, constraint_range_of_motion=0.000000, door_lower_limit=0.000000, door_upper_limit=0.000000, dynamic_max_rotation=0.000000, dynamic_min_rotation=0.000000, engine_max_force=1000.000000, force_emitter_max_force=1000.000000, force_emitter_max_vector=0.000000, light_fov=0.000000, light_intensity=0.000000, light_range=0.000000, magnet_force=0.000000, max_motor_force=0.000000, phys_collision_dampen=2000, rudder_surface_area=0.000000, type=0, wheel_radius=0.000000
