# Bauteil-Verzeichnis

Aus den Spieldaten erzeugt von `tools/bauteile_holen.py` (759 Bauteile) - **nicht von Hand ändern**, nach einem Spiel-Update neu erzeugen. Erklärung und Erfahrungen aus dem Spiel: [README.md](README.md).

Größe in Blöcken (x y z, lokal). Masse in Spiel-Einheiten (1 = 10 kg), Preis in $. Anschlüsse: E = Eingang, A = Ausgang (bei Welle, Flüssigkeit und Strom ist die Richtung egal).

## Bloecke (Kategorie 0) - Einzelheiten: [Bloecke.md](Bloecke.md)

| Name | Datei-Name | Größe | Masse | Preis | Anschlüsse |
|---|---|---|---|---|---|
| Block | `01_block` | 1x1x1 | 1 | 2 |  |
| Inverse Pyramid | `04_invpyramid` | 1x1x1 | 0.75 | 2 |  |
| Inverse Pyramid 1x2 | `07_invpyramid_2` | 1x1x2 | 1.5 | 2 |  |
| Inverse Pyramid 1x4 | `10_invpyramid_4` | 1x1x4 | 3 | 4 |  |
| Inverse Pyramid 2x2 | `14_invpyramid_2x2` | 2x1x2 | 3 | 4 |  |
| Inverse Pyramid 2x4 | `15_invpyramid_2x4` | 2x1x4 | 6 | 8 |  |
| Inverse Pyramid 4x4 | `16_invpyramid_4x4` | 4x1x4 | 12 | 16 |  |
| Ladder | `ladder_small` | 3x4x1 | 3 | 5 |  |
| Physics Flooder | `physics_flooder` | 1x2x1 | 1 | 20 |  |
| Pipe Angle | `trans_angle` | 1x1x1 | 1 | 5 |  |
| Pipe Angle (Enclosed) | `trans_block_angle` | 1x1x1 | 1 | 5 |  |
| Pipe Cross (Enclosed) | `trans_block_cross` | 1x1x1 | 1 | 5 |  |
| Pipe Cross Corner (Enclosed) | `trans_block_cross_corner` | 1x1x1 | 1 | 5 |  |
| Pipe Omni (Enclosed) | `trans_block_omni` | 1x1x1 | 1 | 5 |  |
| Pipe Straight | `trans_straight` | 1x1x1 | 1 | 5 |  |
| Pipe Straight (Enclosed) | `trans_block_straight` | 1x1x1 | 1 | 5 |  |
| Pipe T-Piece Corner (Enclosed) | `trans_block_t_corner` | 1x1x1 | 1 | 5 |  |
| Pivot | `multibody_pivot_b` | 1x1x1 | 1 | 0 |  |
| Pyramid | `03_pyramid` | 1x1x1 | 0.25 | 2 |  |
| Pyramid 1x2 | `06_pyramid_2` | 1x1x2 | 0.5 | 2 |  |
| Pyramid 1x4 | `09_pyramid_4` | 1x1x4 | 1 | 4 |  |
| Pyramid 2x2 | `11_pyramid_2x2` | 2x1x2 | 1 | 4 |  |
| Pyramid 2x4 | `12_pyramid_2x4` | 2x1x4 | 2 | 8 |  |
| Pyramid 4x4 | `13_pyramid_4x4` | 4x1x4 | 4 | 16 |  |
| Robotic Pivot | `multibody_robotic_pivot_01_b` | 1x1x1 | 1 | 0 | E Drehmoment |
| Robotic Pivot | `multibody_robotic_pivot_01_b_fluid` | 1x1x1 | 1 | 0 | E Fluessigkeit/Gas |
| Robotic Pivot | `multibody_velocity_pivot_b` | 1x1x1 | 1 | 0 |  |
| Stair Step | `stair_segment` | 3x1x2 | 6 | 20 |  |
| Stair Top | `stair_top` | 3x1x2 | 6 | 20 |  |
| Static Block | `01_block_static` | 1x1x1 | 1 | 10 |  |
| Turret Ring (Large) | `multibody_turret_large_b` | 9x1x9 | 36 | 0 |  |
| Turret Ring (Medium) | `multibody_turret_medium_b` | 7x1x7 | 22 | 0 |  |
| Turret Ring (Small) | `multibody_turret_small_b` | 5x1x5 | 14 | 0 |  |
| Velocity Pivot | `multibody_velocity_pivot_01_b_fluid` | 1x1x1 | 1 | 0 | E Fluessigkeit/Gas |
| Velocity Pivot | `multibody_velocity_pivot_01_b_torque` | 1x1x1 | 1 | 0 | E Drehmoment |
| Wedge | `02_wedge` | 1x1x1 | 0.5 | 2 |  |
| Wedge 1x2 | `05_wedge_2` | 1x1x2 | 1 | 2 |  |
| Wedge 1x4 | `08_wedge_4` | 1x1x4 | 2 | 4 |  |
| Weight Block | `01_block_weight` | 1x1x1 | 10 | 5 |  |

## Fahrzeugsteuerung (Kategorie 1) - Einzelheiten: [Fahrzeugsteuerung.md](Fahrzeugsteuerung.md)

| Name | Datei-Name | Größe | Masse | Preis | Anschlüsse |
|---|---|---|---|---|---|
| Compact Pilot Seat | `seat_compact` | 3x5x3 | 7 | 100 | 8x A An/Aus, A Composite, A Ton, 6x A Zahl, E Ton, E Video |
| Control Fin Large | `control_fin_large` | 1x3x3 | 10 | 350 | E Strom, E Zahl |
| Control Fin Medium | `control_fin_medium` | 1x2x3 | 5 | 150 | E Strom, E Zahl |
| Control Fin Small | `control_fin_small` | 1x1x1 | 2 | 50 | E Strom, E Zahl |
| Control Handle | `seat_handle` | 3x7x3 | 1 | 50 | 8x A An/Aus, A Composite, A Ton, 6x A Zahl, E Ton, E Video |
| Control Surface (Large) | `control_surface_large` | 1x5x17 | 25 | 500 | E Strom, E Zahl |
| Control Surface (Medium) | `control_surface_medium` | 1x4x11 | 15 | 250 | E Strom, E Zahl |
| Control Surface (Small) | `control_surface_small` | 1x3x7 | 10 | 150 | E Strom, E Zahl |
| Data Logger (Bool) | `data_logger_bool` | 1x1x1 | 1 | 1 | E An/Aus |
| Data Logger (Number) | `data_logger_number` | 1x1x1 | 1 | 1 | E Zahl |
| Driver seat | `seat_racing` | 3x5x4 | 10 | 100 | 8x A An/Aus, A Composite, A Ton, 6x A Zahl, E Ton, E Video |
| Fin Rudder | `rudder_surface` | 1x2x3 | 5 | 100 | E Strom, E Zahl |
| Friction Pad | `friction_block` | 1x1x1 | 1 | 15 |  |
| Gyro | `gyro` | 5x1x3 | 10 | 500 | 4x A Zahl, E An/Aus, E Strom, 4x E Zahl |
| Helm | `seat_helm` | 3x7x5 | 15 | 150 | 8x A An/Aus, A Composite, A Ton, 6x A Zahl, E Ton, E Video |
| Keel (Large) | `keel_large` | 3x9x25 | 2000 | 2000 |  |
| Keel (Medium) | `keel_medium` | 3x7x15 | 1000 | 1000 |  |
| Keel (Small) | `keel_small` | 1x5x9 | 500 | 300 |  |
| Keep Active Block | `no_sleep` | 1x1x1 | 1 | 100 |  |
| Large Landing Wheel | `wheel_coaster_large` | 3x4x3 | 8 | 50 | E An/Aus, E Zahl |
| Map Icon Block | `map_icon` | 1x1x1 | 1 | 100 |  |
| Medium Wheel | `wheel_medium` | 7x5x7 | 10 | 100 | E An/Aus, E Drehmoment, 2x E Zahl |
| Pilot Seat | `seat` | 3x6x4 | 24 | 100 | 8x A An/Aus, A Composite, A Ton, 6x A Zahl, E Ton, E Video |
| Pilot Seat (HOTAS) | `seat_hotas` | 3x6x5 | 50 | 250 | 50x A An/Aus, A Composite, A Ton, 10x A Zahl, E Ton, E Video |
| Radio RX Huge | `rx_huge` | 1x9x1 | 20 | 5000 | A Composite, A Zahl, E Composite, E Strom, 2x E Zahl |
| Radio RX Huge | `rx_huge_v2` | 1x9x1 | 20 | 3000 | A Composite, A Ton, A Zahl, E An/Aus, E Composite, E Strom, E Ton, E Zahl |
| Radio RX Large | `rx_large` | 1x5x1 | 12 | 200 | A Composite, A Zahl, E Composite, E Strom, 2x E Zahl |
| Radio RX Large | `rx_large_v2` | 1x5x1 | 12 | 1000 | A Composite, A Ton, A Zahl, E An/Aus, E Composite, E Strom, E Ton, E Zahl |
| Radio RX Medium | `rx_med` | 1x4x1 | 8 | 1000 | A Composite, A Zahl, E Composite, E Strom, 2x E Zahl |
| Radio RX Medium | `rx_med_v2` | 1x4x1 | 8 | 500 | A Composite, A Ton, A Zahl, E An/Aus, E Composite, E Strom, E Ton, E Zahl |
| Radio RX Small | `rx_small` | 1x2x1 | 5 | 500 | A Composite, E Composite, E Strom, 2x E Zahl |
| Radio RX Small | `rx_small_v2` | 1x2x1 | 5 | 200 | A Composite, A Ton, E An/Aus, E Composite, E Strom, E Ton, E Zahl |
| Radio Video Recv | `rx_video_r` | 1x4x1 | 10 | 1000 | A Video, A Zahl, E Strom, E Zahl |
| Radio Video Xmit | `rx_video_x` | 1x4x1 | 10 | 2000 | E Strom, E Video, E Zahl |
| Rudder | `rudder` | 3x4x3 | 10 | 150 | E Strom, E Zahl |
| RX Directional | `rx_directional` | 5x4x5 | 20 | 5000 | A Composite, A Ton, A Video, A Zahl, E An/Aus, E Composite, E Strom, E Ton, E Video, 3x E Zahl |
| RX Directional (Large) | `rx_directional_large` | 9x6x9 | 35 | 8000 | A Composite, A Ton, A Video, A Zahl, E An/Aus, E Composite, E Strom, E Ton, E Video, 3x E Zahl |
| Saddle Seat | `seat_saddle` | 3x4x4 | 5 | 75 | 8x A An/Aus, A Composite, A Ton, 6x A Zahl, E Ton, E Video |
| Ski | `ski` | 3x2x13 | 12 | 200 | E Zahl |
| Ski (Small) | `ski_small` | 1x2x9 | 8 | 100 | E Zahl |
| Small Wheel | `wheel_small` | 3x4x3 | 5 | 30 | E An/Aus, E Drehmoment, 2x E Zahl |
| Space Seat | `seat_space` | 3x7x3 | 3 | 500 | 8x A An/Aus, A Composite, A Ton, 6x A Zahl, E Fluessigkeit/Gas, E Ton, E Video |
| Tank Drive Wheel (Huge) | `wheel_tank_drive_7` | 7x5x7 | 80 | 450 | E An/Aus, E Drehmoment |
| Tank Drive Wheel (Large) | `wheel_tank_drive_5` | 5x3x5 | 40 | 350 | E An/Aus, E Drehmoment |
| Tank Drive Wheel (Medium) | `wheel_tank_drive_5_2` | 5x3x5 | 30 | 300 | E An/Aus, E Drehmoment |
| Tank Drive Wheel (Small) | `wheel_tank_drive_1` | 3x2x3 | 20 | 200 | E An/Aus, E Drehmoment |
| Tank Drive Wheel (Small/Wide) | `wheel_tank_drive_1_wide` | 3x3x3 | 25 | 250 | E An/Aus, E Drehmoment |
| Tank Wheel (Huge) | `wheel_tank_7` | 7x5x7 | 80 | 350 | E An/Aus |
| Tank Wheel (Large) | `wheel_tank_5` | 5x3x5 | 40 | 250 | E An/Aus |
| Tank Wheel (Medium) | `wheel_tank_5_2` | 5x3x5 | 30 | 200 | E An/Aus |
| Tank Wheel (Small) | `wheel_tank_1` | 3x2x3 | 20 | 100 | E An/Aus |
| Tank Wheel (Small/Wide) | `wheel_tank_1_wide` | 3x3x3 | 25 | 100 | E An/Aus |
| Wheel 3x3 | `wheel_advanced_3` | 3x2x3 | 10 | 100 | E An/Aus, E Drehmoment, 2x E Zahl |
| Wheel 3x3 (Suspension) | `wheel_advanced_3_sus` | 3x3x3 | 15 | 150 | E An/Aus, E Drehmoment, 2x E Zahl |
| Wheel 5x5 | `wheel_advanced_5` | 5x3x5 | 20 | 150 | E An/Aus, E Drehmoment, 2x E Zahl |
| Wheel 5x5 (Suspension) | `wheel_advanced_5_sus` | 5x5x5 | 30 | 200 | E An/Aus, E Drehmoment, 2x E Zahl |
| Wheel 7x7 | `wheel_advanced_7` | 7x4x7 | 40 | 200 | E An/Aus, E Drehmoment, 2x E Zahl |
| Wheel 7x7 (Suspension) | `wheel_advanced_7_sus` | 7x6x7 | 60 | 250 | E An/Aus, E Drehmoment, 2x E Zahl |
| Wheel 9x9 | `wheel_advanced_9` | 9x5x9 | 80 | 250 | E An/Aus, E Drehmoment, 2x E Zahl |
| Wheel 9x9 (Suspension) | `wheel_advanced_9_sus` | 9x8x10 | 120 | 300 | E An/Aus, E Drehmoment, 2x E Zahl |
| Wheel Coaster | `wheel_coaster` | 3x3x3 | 4 | 25 | E An/Aus, E Zahl |
| Wing Front Section (Small) | `wing_small_front` | 1x7x3 | 5 | 100 |  |
| Wing Section (Large) | `wing_large` | 3x7x16 | 20 | 500 |  |
| Wing Section (Medium) | `wing_medium` | 2x3x10 | 15 | 350 |  |
| Wing Section (Small) | `wing_small` | 1x3x6 | 8 | 150 |  |
| Wing Section (XLarge) | `wing_xl` | 3x7x22 | 30 | 800 |  |
| Wing Section (XXLarge) | `wing_xxl` | 3x7x28 | 50 | 1500 |  |

## Bedienelemente (Kategorie 2) - Einzelheiten: [Bedienelemente.md](Bedienelemente.md)

| Name | Datei-Name | Größe | Masse | Preis | Anschlüsse |
|---|---|---|---|---|---|
| Clutch | `torque_clutch` | 1x2x1 | 2 | 50 | 2x E Drehmoment, E Strom, E Zahl |
| Compact Linear Track Base | `linear_compact_base` | 1x1x1 | 2 | 20 | E Strom, E Zahl |
| Compact Linear Track Extension | `linear_compact_module` | 1x1x1 | 1 | 20 |  |
| Compact Linear Track Head | `linear_compact_head` | 1x1x1 | 3 | 0 |  |
| Compact Pivot | `multibody_compact_pivot_b` | 1x1x1 | 1 | 0 |  |
| Compact Pivot (Power) | `multibody_compact_pivot_torque_a` | 1x1x1 | 1 | 40 | A Drehmoment |
| Compact Pivot (Power) | `multibody_compact_pivot_torque_b` | 1x1x1 | 1 | 0 | A Drehmoment |
| Compact Robotic Pivot | `multibody_compact_pivot_robotic_a` | 1x1x1 | 1 | 40 | E Strom, E Zahl |
| Compact Velocity Pivot | `multibody_compact_pivot_velocity_a` | 1x1x1 | 1 | 40 | E Strom, E Zahl |
| Door Frame Controller | `door_frame_controller` | 2x1x1 | 10 | 100 | A An/Aus, E An/Aus |
| Door Frame Corner | `door_frame_corner` | 2x2x1 | 15 | 50 |  |
| Door Frame Edge | `door_frame_straight` | 1x1x1 | 5 | 10 |  |
| Door Panel Corner | `door_panel_corner` | 1x1x1 | 5 | 20 |  |
| Door Panel Edge | `door_panel_straight` | 1x1x1 | 5 | 10 |  |
| Electric Connector | `connector_electric` | 1x2x1 | 2 | 20 | A An/Aus, A Composite, A Video, E An/Aus, E Composite, E Strom, E Video |
| Fluid Connector | `connector_water` | 1x2x1 | 2 | 20 | A An/Aus, A Composite, A Fluessigkeit/Gas, A Video, E An/Aus, E Composite, E Video |
| Gearbox | `torque_gearbox` | 1x2x2 | 8 | 100 | E An/Aus, 2x E Drehmoment, E Strom |
| Gearbox | `torque_gearbox_2` | 1x2x2 | 8 | 100 | E An/Aus, 2x E Drehmoment, E Strom |
| Gearbox 1x1 | `modular_engine_gearbox_1x1` | 1x1x1 | 1 | 50 | E An/Aus, 2x E Drehmoment, E Strom |
| Gearbox 3x3 | `modular_engine_gearbox_3x3` | 3x2x3 | 9 | 100 | E An/Aus, 2x E Drehmoment, E Strom |
| Gearbox 5x5 | `modular_engine_gearbox_5x5` | 5x3x5 | 25 | 150 | E An/Aus, 2x E Drehmoment, E Strom |
| Hardpoint Connector Attachment | `connector_hardpoint_b` | 1x2x1 | 2 | 20 | A An/Aus, A Composite, A Fluessigkeit/Gas, A Video, E Composite, E Strom, E Video |
| Hardpoint Connector Attachment (Round) | `connector_hardpoint_b_round` | 1x2x1 | 2 | 20 | A An/Aus, A Composite, A Fluessigkeit/Gas, A Video, E Composite, E Strom, E Video |
| Hardpoint Connector Body | `connector_hardpoint_a` | 1x1x3 | 2 | 20 | A Composite, A Fluessigkeit/Gas, A Video, A Zahl, 2x E An/Aus, E Composite, E Strom, E Video |
| Hinge Connector | `connector_hinge` | 1x2x3 | 3 | 40 | A An/Aus, A Composite, A Video, E An/Aus, E Composite, E Strom, E Video |
| Hinged Dock Door | `door_dock_large` | 9x5x1 | 20 | 300 | 2x A An/Aus, A Composite, A Zahl, 3x E An/Aus, E Composite, E Strom, E Zahl |
| Hinged Dock Hatch | `door_dock_small` | 5x5x1 | 15 | 200 | 2x A An/Aus, A Composite, A Zahl, 3x E An/Aus, E Composite, E Strom, E Zahl |
| Hinged Door | `door_manual_large` | 7x4x1 | 20 | 200 | E An/Aus |
| Hinged Hatch | `door_manual_small` | 3x4x1 | 15 | 150 | E An/Aus |
| Key Button | `button_key` | 1x2x1 | 1 | 20 | A An/Aus, E An/Aus, E Strom |
| Large Connector | `connector_large` | 3x2x3 | 20 | 50 | 2x A An/Aus, A Composite, A Drehmoment, A Video, A Zahl, 2x E An/Aus, E Composite, E Fluessigkeit/Gas, E Strom, E Video, E Zahl |
| Large Keypad | `button_keypad_large` | 1x2x2 | 1 | 40 | A An/Aus, 2x A Zahl, E An/Aus, E Strom |
| Linear Track Base | `linear_base` | 3x2x1 | 3 | 40 | A Zahl, 2x E An/Aus, E Drehmoment, E Fluessigkeit/Gas, E Strom |
| Linear Track Extension | `linear_module` | 3x2x1 | 3 | 10 |  |
| Linear Track Head | `linear_head` | 3x1x1 | 3 | 0 | E Drehmoment, E Fluessigkeit/Gas |
| Lockable Button | `button_lock` | 1x2x1 | 1 | 20 | A An/Aus, E An/Aus, E Strom |
| Mag All | `magall` | 1x3x1 | 5 | 250 | A An/Aus, A Zahl, E An/Aus, E Strom |
| Piston Suspension | `multibody_piston_suspension_a` | 1x2x1 | 20 | 20 |  |
| Piston Suspension | `multibody_piston_suspension_b` | 1x1x1 | 20 | 0 |  |
| Pivot | `multibody_pivot_a` | 1x2x1 | 1 | 20 |  |
| Pivot (Power) | `multibody_pivot_torque_a` | 1x2x1 | 1 | 20 | A Drehmoment |
| Pneumatic Piston | `linear_matic_a` | 1x3x1 | 5 | 100 | A Zahl, E Fluessigkeit/Gas, E Strom, E Zahl |
| Pneumatic Piston | `linear_matic_b` | 1x2x1 | 3 | 0 | E Fluessigkeit/Gas |
| Push Button | `button_push` | 1x2x1 | 1 | 10 | A An/Aus, E An/Aus, E Strom |
| Push Button (2 Sided) | `button_push_2side` | 1x2x1 | 1 | 10 | A An/Aus, E An/Aus, E Strom |
| Reaction Wheel | `gyroscopic_stabilizer` | 3x1x3 | 15 | 300 | E Strom, E Zahl |
| Reaction Wheel (Large) | `gyroscopic_stabilizer_large` | 5x3x5 | 80 | 700 | E Strom, E Zahl |
| Reaction Wheel (Small) | `gyroscopic_stabilizer_small` | 1x1x1 | 2 | 150 | E Strom, E Zahl |
| Robotic Door Hinge | `multibody_door_hinge_a` | 1x2x3 | 3 | 400 | A Zahl, E Strom, E Zahl |
| Robotic Door Hinge | `multibody_door_hinge_b` | 1x1x3 | 3 | 0 |  |
| Robotic Hinge | `multibody_robotic_hinge_01_a` | 1x2x3 | 3 | 400 | A Zahl, E Drehmoment, E Fluessigkeit/Gas, E Strom, E Zahl |
| Robotic Hinge | `multibody_robotic_hinge_01_b` | 1x1x3 | 3 | 0 | E Drehmoment, E Fluessigkeit/Gas |
| Robotic Pivot (Fluid) | `multibody_robotic_pivot_01_a_fluid` | 3x1x3 | 9 | 200 | A Zahl, E Fluessigkeit/Gas, E Strom, E Zahl |
| Robotic Pivot (Power) | `multibody_robotic_pivot_01_a` | 3x1x3 | 9 | 200 | A Zahl, E Drehmoment, E Strom, E Zahl |
| Sliding Connector Gripper | `connector_slider_gripper` | 1x2x1 | 2 | 20 | 2x E An/Aus |
| Sliding Connector Track | `connector_slider_track` | 1x1x1 | 2 | 10 |  |
| Sliding Door | `door_manual` | 1x7x6 | 20 | 50 | E An/Aus |
| Sliding Door (Electric) | `door` | 1x7x6 | 20 | 70 | E An/Aus, E Strom |
| Sliding Hatch | `door_manual_sliding_small` | 1x3x6 | 20 | 40 | E An/Aus |
| Sliding Hatch (Electric) | `hatch` | 1x3x6 | 15 | 50 | E An/Aus, E Strom |
| Small Connector | `connector_small` | 1x2x1 | 2 | 20 | A An/Aus, A Composite, A Video, E An/Aus, E Composite, E Strom, E Video |
| Small Keypad | `button_keypad_small` | 1x2x1 | 1 | 20 | A Zahl, E An/Aus, E Strom |
| Suspension | `multibody_suspension_a` | 2x3x3 | 5 | 50 | E Drehmoment |
| Suspension | `multibody_suspension_b` | 1x1x1 | 3 | 0 | A Drehmoment |
| Throttle Lever | `button_throttle_lever` | 2x2x1 | 1 | 30 | A Zahl, 2x E An/Aus, E Strom |
| Toggle Button | `button_toggle` | 1x2x1 | 1 | 10 | A An/Aus, E An/Aus, E Strom |
| Toggle Button (2 Sided) | `button_toggle_2side` | 1x2x1 | 1 | 10 | A An/Aus, E An/Aus, E Strom |
| Torque Connector | `connector_torque` | 1x2x1 | 2 | 20 | A An/Aus, A Composite, A Drehmoment, A Video, E An/Aus, E Composite, E Video |
| Turret Ring (Large) | `multibody_turret_large_a` | 9x1x9 | 36 | 100 | A Zahl, E Strom, E Zahl |
| Turret Ring (Medium) | `multibody_turret_medium_a` | 7x1x7 | 22 | 75 | A Zahl, E Strom, E Zahl |
| Turret Ring (Small) | `multibody_turret_small_a` | 5x1x5 | 14 | 50 | A Zahl, E Strom, E Zahl |
| Velocity Pivot | `multibody_velocity_pivot_a` | 3x1x3 | 9 | 25 | A Zahl, E Strom, E Zahl |
| Velocity Pivot (Fluid) | `multibody_velocity_pivot_01_a_fluid` | 3x1x3 | 9 | 200 | A Zahl, E Fluessigkeit/Gas, E Strom, E Zahl |
| Velocity Pivot (Power) | `multibody_velocity_pivot_01_a_torque` | 3x1x3 | 9 | 200 | A Zahl, E Drehmoment, E Strom, E Zahl |

## Antrieb (Kategorie 3) - Einzelheiten: [Antrieb.md](Antrieb.md)

| Name | Datei-Name | Größe | Masse | Preis | Anschlüsse |
|---|---|---|---|---|---|
| Aircraft Propeller | `aircraft_propeller` | 11x2x11 | 2 | 125 | E Drehmoment, E Zahl |
| Azimuth Thruster | `azimuth_thruster` | 3x3x4 | 4 | 150 | E Drehmoment |
| Giant Propeller | `giga_prop_small` | 9x3x9 | 100 | 500 | E Drehmoment |
| Heavy Large Rotor | `heavy_rotor_large` | 37x4x37 | 20 | 1450 | E Drehmoment, 3x E Zahl |
| Heavy Rotor | `heavy_rotor` | 25x4x25 | 10 | 850 | E Drehmoment, 3x E Zahl |
| Huge Rotor | `huge_rotor` | 33x3x33 | 20 | 250 | E Drehmoment, 3x E Zahl |
| Large Ducted Fan | `fan_large` | 7x1x7 | 10 | 100 | E Drehmoment |
| Large Electric Motor | `motor_large` | 5x5x5 | 400 | 5000 | E Drehmoment, E Strom, E Zahl |
| Large Engine | `engine_diesel` | 5x8x11 | 400 | 3000 | A Drehmoment, 3x A Fluessigkeit/Gas, 2x A Zahl, E An/Aus, 3x E Fluessigkeit/Gas, E Strom, E Zahl |
| Large Pitchable Propeller | `propeller_pitch_large` | 19x5x19 | 100 | 600 | E Drehmoment, E Zahl |
| Large Propeller | `large_propeller` | 5x2x5 | 20 | 250 | E Drehmoment |
| Large Rotor | `large_rotor` | 33x3x33 | 10 | 150 | E Drehmoment, 3x E Zahl |
| Liquid Fuel Rocket | `liquid_rocket` | 5x9x5 | 60 | 4500 | E An/Aus, 2x E Fluessigkeit/Gas, 3x E Zahl |
| Liquid Fuel Rocket (Large) | `liquid_rocket_large` | 7x13x7 | 80 | 6500 | E An/Aus, 2x E Fluessigkeit/Gas, 3x E Zahl |
| Liquid Fuel Rocket (Small) | `liquid_rocket_small` | 3x7x3 | 40 | 2500 | E An/Aus, 2x E Fluessigkeit/Gas, 3x E Zahl |
| Medium Electric Motor | `motor_medium` | 3x3x3 | 100 | 1500 | E Drehmoment, E Strom, E Zahl |
| Medium Engine | `aircraft_engine` | 3x4x7 | 80 | 1000 | A Drehmoment, 3x A Fluessigkeit/Gas, 2x A Zahl, E An/Aus, 3x E Fluessigkeit/Gas, E Strom, E Zahl |
| Pitchable Propeller | `propeller_pitch` | 11x3x11 | 40 | 300 | E Drehmoment, E Zahl |
| Rotor (Large) | `rotor_coaxial_large` | 53x2x53 | 20 | 1050 | A Drehmoment, E Drehmoment, 3x E Zahl |
| Rotor (Light) | `rotor_coaxial_light` | 9x1x9 | 4 | 150 | A Drehmoment, E Drehmoment, 3x E Zahl |
| Rotor (Small) | `rotor_coaxial_small` | 27x2x27 | 10 | 250 | A Drehmoment, E Drehmoment, 3x E Zahl |
| Rotor (Tail) | `tail_rotor` | 11x2x11 | 4 | 100 | E Drehmoment, E Zahl |
| Rotor End (Light) | `rotor_coaxial_light_end` | 9x1x9 | 4 | 150 | E Drehmoment, 3x E Zahl |
| Rotor Propeller (Large) | `rotor_coaxial_prop` | 31x2x31 | 30 | 1850 | A Drehmoment, E Drehmoment, 3x E Zahl |
| Rotor Propeller (Small) | `rotor_coaxial_prop_small` | 21x2x21 | 20 | 850 | A Drehmoment, E Drehmoment, 3x E Zahl |
| Rotor Propeller End (Large) | `rotor_coaxial_prop_end` | 31x3x31 | 30 | 1850 | E Drehmoment, 3x E Zahl |
| Rotor Propeller End (Small) | `rotor_coaxial_prop_small_end` | 21x3x21 | 20 | 850 | E Drehmoment, 3x E Zahl |
| Small Ducted Fan | `fan_small` | 5x1x5 | 6 | 50 | E Drehmoment |
| Small Electric Motor | `motor_small` | 1x1x1 | 5 | 450 | E Drehmoment, E Strom, E Zahl |
| Small Engine | `engine` | 3x3x3 | 30 | 400 | A Drehmoment, 2x A Fluessigkeit/Gas, 2x A Zahl, E An/Aus, 3x E Fluessigkeit/Gas, E Strom, E Zahl |
| Small Pitchable Propeller | `propeller_pitch_small` | 3x1x3 | 10 | 75 | E Drehmoment, E Zahl |
| Small Propeller | `propeller` | 1x3x1 | 3 | 75 | E Drehmoment |
| Solid Rocket Booster (Huge) | `solid_rocket_nozzle_huge` | 7x4x7 | 50 | 2000 | A Zahl, E An/Aus |
| Solid Rocket Booster (Large) | `solid_rocket_nozzle_large` | 5x4x5 | 30 | 800 | A Zahl, E An/Aus |
| Solid Rocket Booster (Medium) | `solid_rocket_nozzle_medium` | 3x4x3 | 20 | 300 | A Zahl, E An/Aus |
| Solid Rocket Booster (Small) | `solid_rocket_nozzle_small` | 1x1x1 | 5 | 100 | E An/Aus |
| Solid Rocket Fuel (Huge) | `solid_rocket_huge` | 7x3x7 | 50 | 500 |  |
| Solid Rocket Fuel (Huge) (Fins) | `solid_rocket_huge_fins` | 7x3x7 | 50 | 1000 | E Composite, E Strom |
| Solid Rocket Fuel (Large) | `solid_rocket_large` | 5x3x5 | 30 | 400 |  |
| Solid Rocket Fuel (Large) (Fins) | `solid_rocket_large_fins` | 5x3x5 | 30 | 800 | E Composite, E Strom |
| Solid Rocket Fuel (Medium) | `solid_rocket_medium` | 3x3x3 | 20 | 200 |  |
| Solid Rocket Fuel (Medium) (Fins) | `solid_rocket_medium_fins` | 3x3x3 | 20 | 400 | E Composite, E Strom |
| Solid Rocket Fuel (Small) | `solid_rocket_small` | 1x1x1 | 5 | 100 |  |
| Solid Rocket Fuel (Small) (Fins) | `solid_rocket_small_fins` | 1x1x1 | 5 | 200 | E Composite, E Strom |
| Torque Crank | `torque_crank` | 1x2x1 | 4 | 25 | A Drehmoment |
| Torque Meter | `torque_meter` | 1x2x1 | 4 | 25 | A Drehmoment, 2x A Zahl |
| Train Wheel Assembly Classic | `train_wheels` | 13x5x11 | 400 | 100 | A An/Aus, E An/Aus, E Drehmoment, E Strom, E Zahl |
| Train Wheel Assembly Flanged A | `train_wheels_dynamic_flanged` | 3x4x9 | 200 | 50 | A An/Aus, E An/Aus, E Zahl |
| Train Wheel Assembly Flanged B | `train_wheels_dynamic_flanged_b` | 3x4x9 | 200 | 50 | A An/Aus, E An/Aus, E Zahl |
| Train Wheel Assembly Flanged C | `train_wheels_dynamic_flanged_c` | 3x4x9 | 200 | 50 | A An/Aus, E An/Aus, E Zahl |
| Train Wheel Assembly Flanged D | `train_wheels_dynamic_flanged_d` | 3x4x9 | 200 | 50 | A An/Aus, E An/Aus, E Zahl |
| Train Wheel Assembly Medium | `train_wheels_dynamic_steam_basic_mid` | 5x4x9 | 200 | 50 | A An/Aus, E An/Aus, E Drehmoment, E Zahl |
| Train Wheel Assembly Small | `train_wheels_dynamic_steam_small_basic` | 3x4x9 | 200 | 50 | A An/Aus, E An/Aus, E Drehmoment, E Zahl |
| Train Wheel Assembly Steam Large A | `train_wheels_dynamic_steam_large` | 9x5x9 | 400 | 100 | A An/Aus, E An/Aus, E Zahl |
| Train Wheel Assembly Steam Large B | `train_wheels_dynamic_steam_large_b` | 9x5x9 | 400 | 100 | A An/Aus, E An/Aus, E Zahl |
| Train Wheel Assembly Steam Medium A | `train_wheels_dynamic_steam_mid` | 5x4x9 | 200 | 50 | A An/Aus, E An/Aus, E Zahl |
| Train Wheel Assembly Steam Medium B | `train_wheels_dynamic_steam_mid_b` | 5x4x9 | 200 | 50 | A An/Aus, E An/Aus, E Zahl |
| Train Wheel Assembly Steam Small A | `train_wheels_dynamic_steam_small` | 3x4x9 | 200 | 50 | A An/Aus, E An/Aus, E Zahl |
| Train Wheel Assembly Steam Small B | `train_wheels_dynamic_steam_small_b` | 3x4x9 | 200 | 50 | A An/Aus, E An/Aus, E Zahl |
| Train Wheel Assembly x1 | `train_wheels_dynamic_x1` | 5x4x9 | 200 | 50 | A An/Aus, E An/Aus, E Drehmoment, E Zahl |
| Train Wheel Assembly x1 Small | `train_wheels_dynamic_x1_small` | 5x4x9 | 200 | 50 | A An/Aus, E An/Aus, E Drehmoment, E Zahl |
| Train Wheel Assembly x1 Small (Compact) | `train_wheels_dynamic_x1_xsmall` | 3x4x9 | 150 | 50 | A An/Aus, E An/Aus, E Drehmoment, E Zahl |
| Train Wheel Assembly x2 | `train_wheels_dynamic_x2` | 13x4x9 | 350 | 100 | A An/Aus, E An/Aus, E Drehmoment, E Strom, E Zahl |
| Train Wheel Assembly x3 | `train_wheels_dynamic_x3` | 21x4x11 | 450 | 150 | A An/Aus, E An/Aus, E Drehmoment, E Strom, E Zahl |
| Train Wheel Drive Piston Large | `train_wheels_piston_large` | 5x3x11 | 600 | 600 | 4x A Fluessigkeit/Gas, E An/Aus |
| Train Wheel Drive Piston Medium | `train_wheels_piston_mid` | 5x2x11 | 400 | 400 | 4x A Fluessigkeit/Gas, E An/Aus |
| Train Wheel Drive Piston Small | `train_wheels_piston` | 3x2x11 | 300 | 300 | 4x A Fluessigkeit/Gas, E An/Aus |
| Turbine Engine | `turbine` | 3x3x7 | 45 | 150 | A Drehmoment, E An/Aus, E Strom, E Zahl |

## Spezialausruestung (Kategorie 4) - Einzelheiten: [Spezialausruestung.md](Spezialausruestung.md)

| Name | Datei-Name | Größe | Masse | Preis | Anschlüsse |
|---|---|---|---|---|---|
| Bed | `seat_bed` | 3x4x7 | 20 | 250 | A An/Aus |
| Buoyancy Float Block | `buoyancy_float_block` | 4x4x4 | 1 | 50 |  |
| Buoyancy Float Pyramid | `buoyancy_float_pyramid` | 4x4x4 | 1 | 50 |  |
| Buoyancy Float Wedge | `buoyancy_float_wedge` | 4x4x4 | 1 | 50 |  |
| Camera Gimbal | `camera_gimbal` | 3x3x3 | 50 | 5000 | A Video, E An/Aus, E Strom, 3x E Zahl |
| Camera Medium | `camera_med` | 1x2x1 | 10 | 3000 | A Video, E An/Aus, E Composite, E Strom, E Zahl |
| Camera Small | `camera_small` | 1x1x1 | 5 | 1000 | A Video, E Composite, E Strom |
| Camera Stabilized | `camera_gimbal_laser` | 3x3x3 | 60 | 50000 | A Composite, A Video, A Zahl, 4x E An/Aus, E Strom, 4x E Zahl |
| Electric Cable Pulley | `winch_pulley_cable` | 3x1x3 | 25 | 250 | 2x A Zahl, 2x E Seil/Munition |
| Electric Cable Pulley (Corner) | `winch_pulley_cable_corner` | 3x1x3 | 25 | 250 | 2x A Zahl, 2x E Seil/Munition |
| Electrical Cable Anchor | `rope_hook_composite` | 1x2x1 | 1 | 15 | A An/Aus, A Composite, A Ton, A Video, E An/Aus, E Composite, E Seil/Munition, E Strom, E Ton, E Video |
| Equipment inventory (Binoculars) | `inventory_equipment_binoculars` | 1x1x1 | 1 | 50 | E Strom |
| Equipment inventory (C4 Detonator) | `inventory_equipment_c4_detonator` | 1x1x1 | 1 | 50 | E Strom |
| Equipment inventory (C4 Explosive) | `inventory_equipment_c4` | 1x1x1 | 1 | 50 | E Strom |
| Equipment inventory (Cable) | `inventory_equipment_cable` | 1x1x3 | 3 | 200 | E Strom |
| Equipment inventory (Compass) | `inventory_equipment_compass` | 1x1x1 | 1 | 50 | E Strom |
| Equipment inventory (Defibrillator) | `inventory_equipment_defibrillator` | 1x1x3 | 3 | 200 | E Strom |
| Equipment inventory (Dog Whistle) | `inventory_equipment_dog_whistle` | 1x1x1 | 1 | 50 | E Strom |
| Equipment inventory (Fire Extinguisher) | `inventory_equipment_fire_extinguisher` | 1x1x3 | 3 | 200 | E Strom |
| Equipment inventory (First Aid Kit) | `inventory_equipment_first_aid` | 1x1x1 | 1 | 50 | E Strom |
| Equipment inventory (Fishing Rod) | `inventory_equipment_fishing_rod` | 1x1x3 | 3 | 200 | E Strom |
| Equipment inventory (Flare) | `inventory_equipment_flare` | 1x1x1 | 1 | 50 | E Strom |
| Equipment inventory (Flaregun Ammo) | `inventory_equipment_flaregun_ammo` | 1x1x1 | 1 | 50 | E Strom |
| Equipment inventory (Flaregun) | `inventory_equipment_flaregun` | 1x1x1 | 1 | 50 | E Strom |
| Equipment inventory (Flashlight) | `inventory_equipment_flashlight` | 1x1x1 | 1 | 50 | E Strom |
| Equipment inventory (Glowstick) | `inventory_equipment_glowstick` | 1x1x1 | 1 | 50 | E Strom |
| Equipment Inventory (Hand Grenade) | `inventory_equipment_grenade` | 1x1x1 | 1 | 50 | E Strom |
| Equipment inventory (Hose) | `inventory_equipment_hose` | 1x1x3 | 3 | 200 | E Strom |
| Equipment inventory (Night Vision Binoculars) | `inventory_equipment_night_vision_binoculars` | 1x1x1 | 1 | 50 | E Strom |
| Equipment inventory (Oxygen Mask) | `inventory_equipment_oxygen_mask` | 1x1x1 | 1 | 50 | E Strom |
| Equipment Inventory (Pistol Ammo) | `inventory_equipment_pistol_ammo` | 1x1x1 | 1 | 50 | E Strom |
| Equipment inventory (Pistol) | `inventory_equipment_pistol` | 1x1x1 | 1 | 200 | E Strom |
| Equipment inventory (Radiation Detector) | `inventory_equipment_geiger_counter` | 1x1x1 | 1 | 50 | E Strom |
| Equipment inventory (Radio Signal Locator) | `inventory_equipment_radio_signal_locator` | 1x1x3 | 3 | 200 | E Strom |
| Equipment inventory (Radio) | `inventory_equipment_radio` | 1x1x1 | 1 | 50 | E Strom |
| Equipment inventory (Remote Control Unit) | `inventory_equipment_remote_control` | 1x1x1 | 1 | 50 | E Strom |
| Equipment inventory (Rifle Ammo) | `inventory_equipment_rifle_ammo` | 1x1x1 | 1 | 50 | E Strom |
| Equipment inventory (Rifle) | `inventory_equipment_rifle` | 1x1x3 | 3 | 200 | E Strom |
| Equipment inventory (Rope) | `inventory_equipment_rope` | 1x1x3 | 3 | 200 | E Strom |
| Equipment inventory (SMG Ammo) | `inventory_equipment_smg_ammo` | 1x1x1 | 1 | 50 | E Strom |
| Equipment inventory (SMG) | `inventory_equipment_smg` | 1x1x3 | 3 | 200 | E Strom |
| Equipment inventory (Speargun Ammo) | `inventory_equipment_speargun_ammo` | 1x1x1 | 1 | 50 | E Strom |
| Equipment inventory (Speargun) | `inventory_equipment_speargun` | 1x1x3 | 3 | 200 | E Strom |
| Equipment inventory (Strobe Light) | `inventory_equipment_strobe_light` | 1x1x1 | 1 | 50 | E Strom |
| Equipment inventory (Strobe Light, Infrared) | `inventory_equipment_strobe_light_infrared` | 1x1x1 | 1 | 50 | E Strom |
| Equipment inventory (Transponder) | `inventory_equipment_transponder` | 1x1x1 | 1 | 50 | E Strom |
| Equipment inventory (Underwater Welding Torch) | `inventory_equipment_underwater_welding_torch` | 1x1x3 | 3 | 200 | E Strom |
| Equipment inventory (Welding Torch) | `inventory_equipment_welding_torch` | 1x1x3 | 3 | 200 | E Strom |
| Flare Launcher | `flare_launcher` | 1x2x1 | 1 | 10 | A An/Aus, E An/Aus |
| Fluid Cannon | `watercannon` | 3x3x3 | 11 | 100 | E Fluessigkeit/Gas, E Strom, 2x E Zahl |
| Fluid Hose Anchor | `rope_hook_fluid` | 1x2x1 | 1 | 15 | E Fluessigkeit/Gas, E Seil/Munition |
| Fluid Hose Pulley | `winch_pulley_hose` | 3x1x3 | 25 | 250 | 2x A Fluessigkeit/Gas, 2x A Zahl, 2x E Seil/Munition |
| Fluid Hose Pulley (Corner) | `winch_pulley_hose_corner` | 3x1x3 | 25 | 250 | 2x A Fluessigkeit/Gas, 2x A Zahl, 2x E Seil/Munition |
| Fluid Nozzle | `water_nozzle` | 1x2x1 | 1 | 100 | E Fluessigkeit/Gas, E Strom, E Zahl |
| Foghorn | `foghorn` | 4x3x3 | 5 | 200 | E An/Aus, E Strom |
| Harness | `seat_harness` | 3x6x3 | 20 | 150 | 8x A An/Aus, A Composite |
| Heater | `heater` | 1x1x3 | 3 | 50 | E An/Aus, E Strom |
| Hose | `water_hose` | 3x4x3 | 25 | 100 | A Fluessigkeit/Gas, A Zahl, 2x E An/Aus, E Strom |
| Huge Winch | `rope_hook_winch_huge` | 9x7x7 | 400 | 5000 | A An/Aus, A Composite, A Fluessigkeit/Gas, A Ton, A Video, A Zahl, 4x E An/Aus, E Composite, E Seil/Munition, E Strom, E Ton, E Video, E Zahl |
| Huge Winch | `winch_huge_a` | 9x7x7 | 400 | 5000 | A Fluessigkeit/Gas, A Zahl, 2x E An/Aus, E Strom |
| Landing Float | `landing_float` | 3x3x9 | 1 | 50 |  |
| Large equipment inventory (Empty) | `inventory_medium` | 1x1x3 | 3 | 50 | E Strom |
| Large Winch | `rope_hook_winch_large` | 3x4x3 | 100 | 800 | A An/Aus, A Composite, A Fluessigkeit/Gas, A Ton, A Video, A Zahl, 4x E An/Aus, E Composite, E Seil/Munition, E Strom, E Ton, E Video, E Zahl |
| Large Winch | `winch_large_a` | 3x4x3 | 100 | 800 | A Fluessigkeit/Gas, A Zahl, 2x E An/Aus, E Strom |
| Light | `small_light` | 1x2x1 | 1 | 20 | E An/Aus, E Strom |
| Light (RGB) | `small_light_rgb` | 1x2x1 | 1 | 50 | E Composite, E Strom |
| Medical Bed | `seat_medical` | 3x4x7 | 40 | 2500 | A An/Aus |
| Medium Winch | `rope_hook_winch` | 3x2x1 | 20 | 250 | A An/Aus, A Composite, A Fluessigkeit/Gas, A Ton, A Video, A Zahl, 3x E An/Aus, E Composite, E Seil/Munition, E Strom, E Ton, E Video, E Zahl |
| Medium Winch | `winch_a` | 3x2x1 | 20 | 250 | A Fluessigkeit/Gas, A Zahl, 2x E An/Aus, E Strom |
| Megaphone Speaker (Large) | `speaker_large` | 3x3x5 | 10 | 1000 | A An/Aus, E Strom, E Ton |
| Megaphone Speaker (Small) | `speaker_medium` | 1x1x2 | 3 | 500 | A An/Aus, E Strom, E Ton |
| Mineral Drill | `mineral_drill` | 3x6x3 | 110 | 20000 | E Drehmoment |
| Mounted End-Effector | `vehicle_tool_interact` | 1x2x1 | 10 | 1000 | E An/Aus, E Strom |
| Mounted Welder | `vehicle_tool_welder` | 1x2x1 | 10 | 1000 | E An/Aus, E Strom |
| Outfit Inventory (Arctic) | `inventory_outfit_arctic` | 3x3x1 | 9 | 500 | E Strom |
| Outfit Inventory (Armor Vest) | `inventory_outfit_wep_armor_vest` | 3x3x1 | 9 | 1500 | E Strom |
| Outfit Inventory (Black Hawk Vest) | `inventory_outfit_wep_black_hawk_vest` | 3x3x1 | 9 | 500 | E Strom |
| Outfit Inventory (Bomb Disposal) | `inventory_outfit_wep_bomb_disposal` | 3x3x1 | 9 | 1500 | E Strom |
| Outfit Inventory (Chest Rig) | `inventory_outfit_wep_chest_rig` | 3x3x1 | 9 | 500 | E Strom |
| Outfit Inventory (Diving) | `inventory_outfit_diving` | 3x3x1 | 9 | 2000 | E Fluessigkeit/Gas, E Strom |
| Outfit Inventory (Empty) | `inventory_outfit` | 3x3x1 | 9 | 50 | E Strom |
| Outfit Inventory (Firefighter SCBA) | `inventory_outfit_firefighter_scba` | 3x3x1 | 9 | 1000 | E Fluessigkeit/Gas, E Strom |
| Outfit Inventory (Firefighter) | `inventory_outfit_firefighter` | 3x3x1 | 9 | 500 | E Strom |
| Outfit Inventory (Hazmat) | `inventory_outfit_hazmat` | 3x3x1 | 9 | 500 | E Strom |
| Outfit Inventory (Parachute) | `inventory_outfit_parachute` | 3x3x1 | 9 | 500 | E Strom |
| Outfit Inventory (Plate Vest) | `inventory_outfit_wep_plate_vest` | 3x3x1 | 9 | 800 | E Strom |
| Outfit Inventory (Scuba) | `inventory_outfit_scuba` | 3x3x1 | 9 | 500 | E Fluessigkeit/Gas, E Strom |
| Outfit Inventory (Space Exploration) | `inventory_outfit_space_suit_exploration` | 3x3x1 | 9 | 10000 | E Fluessigkeit/Gas, E Strom |
| Outfit Inventory (Space) | `inventory_outfit_space_suit` | 3x3x1 | 9 | 5000 | E Fluessigkeit/Gas, E Strom |
| Padded Seat | `seat_padded` | 2x4x2 | 2 | 25 | A An/Aus |
| Passenger Seat | `passenger_seat` | 3x5x3 | 20 | 50 | A An/Aus |
| Passenger Seat | `seat_passenger` | 3x5x3 | 6 | 50 | A An/Aus |
| RCS Thruster | `rcs_thruster` | 1x1x1 | 1 | 140 | E Composite, E Fluessigkeit/Gas, E Strom |
| Rope Anchor | `rope_hook` | 1x2x1 | 1 | 15 | E An/Aus, E Seil/Munition |
| Rope Pulley | `winch_pulley` | 3x1x3 | 25 | 250 | 2x A Zahl, 2x E Seil/Munition |
| Rope Pulley (Corner) | `winch_pulley_corner` | 3x1x3 | 25 | 250 | 2x A Zahl, 2x E Seil/Munition |
| Rotating Light | `rotating_light` | 1x1x1 | 1 | 50 | E An/Aus, E Strom |
| Saddle Passenger Seat | `seat_saddle_passenger` | 3x4x2 | 3 | 25 | A An/Aus |
| Sail Anchor | `rope_hook_sail` | 1x2x1 | 3 | 50 | E An/Aus, E Seil/Munition |
| Search Light | `searchlight` | 3x3x3 | 20 | 30 | E An/Aus, E Strom, E Zahl |
| Siren | `siren` | 3x3x5 | 5 | 200 | E An/Aus, E Strom |
| Small equipment inventory (Empty) | `inventory_small` | 1x1x1 | 1 | 50 | E Strom |
| Small Spotlight (Block) | `searchlight_small` | 1x2x1 | 1 | 20 | E An/Aus, E Composite, E Strom |
| Small Spotlight (Mounted) | `searchlight_small_2` | 1x1x1 | 1 | 20 | E An/Aus, E Composite, E Strom |
| Small Winch | `rope_hook_winch_small` | 1x2x1 | 10 | 100 | A Fluessigkeit/Gas, 2x E An/Aus, E Seil/Munition, E Strom |
| Small Winch | `winch_electric` | 1x2x1 | 10 | 100 | A Fluessigkeit/Gas, 2x E An/Aus, E Strom |
| Sonar Noisemaker | `sonar_jammer` | 1x1x3 | 1 | 250 | E An/Aus, E Strom |
| Stretcher | `seat_stretcher` | 3x3x7 | 80 | 250 | A An/Aus |
| Transponder | `transponder` | 1x1x1 | 1 | 20 | E An/Aus, E Strom |
| Vehicle Parachute | `parachute` | 3x1x3 | 5 | 500 | E An/Aus |
| winch end | `water_hose_b` | 1x1x1 | 20 | 0 | A Fluessigkeit/Gas |
| winch end | `winch_b` | 1x1x1 | 20 | 0 | A Fluessigkeit/Gas |
| winch end | `winch_electric_b` | 1x1x1 | 20 | 0 | A Fluessigkeit/Gas |
| winch end | `winch_huge_b` | 1x1x1 | 20 | 0 | A Fluessigkeit/Gas |
| winch end | `winch_large_b` | 1x1x1 | 20 | 0 | A Fluessigkeit/Gas |

## Logik (Kategorie 5) - Einzelheiten: [Logik.md](Logik.md)

| Name | Datei-Name | Größe | Masse | Preis | Anschlüsse |
|---|---|---|---|---|---|
| Abs | `gate_float_abs` | 1x1x2 | 1 | 20 | A Zahl, E Zahl |
| Add | `gate_float_add` | 2x1x2 | 1 | 20 | A Zahl, 2x E Zahl |
| And | `gate_bool_and` | 2x1x2 | 1 | 20 | A An/Aus, 2x E An/Aus |
| Blinker | `gate_bool_blink` | 1x1x2 | 1 | 20 | A An/Aus, E An/Aus |
| Capacitor | `gate_bool_capacitor` | 1x1x2 | 1 | 20 | A An/Aus, E An/Aus |
| Clamp | `gate_float_clamp` | 1x1x2 | 1 | 20 | A Zahl, E Zahl |
| Constant Number | `gate_float_constant` | 1x1x1 | 1 | 20 | A Zahl |
| Constant On Signal | `gate_bool_constant` | 1x1x1 | 1 | 20 | A An/Aus |
| Counter | `gate_float_counter` | 1x1x2 | 1 | 20 | A Zahl, E Zahl |
| Counter (Ping Pong) | `gate_float_counter_ping_pong` | 1x1x2 | 1 | 20 | A Zahl, E Zahl |
| Delay | `gate_bool_delay` | 1x1x2 | 1 | 20 | A An/Aus, E An/Aus |
| Divide | `gate_float_divide` | 2x1x2 | 1 | 20 | A An/Aus, A Zahl, 2x E Zahl |
| Exponent | `gate_float_exponent` | 1x1x2 | 1 | 20 | A Zahl, E Zahl |
| Function (1 input) | `gate_function_small` | 1x1x2 | 1 | 80 | A Zahl, E Zahl |
| Function (3 inputs) | `gate_function_large` | 2x1x2 | 1 | 100 | A Zahl, 3x E Zahl |
| Greater-than | `gate_float_greater_than` | 2x1x2 | 1 | 20 | A An/Aus, 2x E Zahl |
| JK Flip-Flop | `gate_jk_flipflop` | 2x1x2 | 1 | 20 | 2x A An/Aus, 2x E An/Aus |
| Less-Than | `gate_float_less_than` | 2x1x2 | 1 | 20 | A An/Aus, 2x E Zahl |
| Memory Register | `gate_float_register` | 2x1x2 | 1 | 20 | A Zahl, 2x E An/Aus, E Zahl |
| Microprocessor | `microprocessor` | 1x1x1 | 1 | 100 |  |
| Modulo | `gate_float_modulo` | 2x1x2 | 1 | 20 | A Zahl, 2x E Zahl |
| Multiply | `gate_float_multiply` | 2x1x2 | 1 | 20 | A Zahl, 2x E Zahl |
| Not | `gate_bool_not` | 1x1x2 | 1 | 20 | A An/Aus, E An/Aus |
| Numerical Inverter | `gate_float_invert` | 1x1x2 | 1 | 20 | A Zahl, E Zahl |
| Numerical Junction | `gate_float_switch` | 2x1x2 | 1 | 20 | 2x A Zahl, E An/Aus, E Zahl |
| Numerical Switchbox | `gate_float_switch_input` | 2x1x2 | 1 | 20 | A Zahl, E An/Aus, 2x E Zahl |
| Or | `gate_bool_or` | 2x1x2 | 1 | 20 | A An/Aus, 2x E An/Aus |
| PID Controller | `gate_pid_controller` | 2x1x2 | 1 | 100 | A Zahl, E An/Aus, 2x E Zahl |
| Power Add | `gate_torque_add` | 2x1x2 | 1 | 20 | A Drehmoment |
| Power Meter | `gate_torque_multimeter` | 2x1x2 | 1 | 20 | A Drehmoment |
| Push to Toggle | `gate_push_to_toggle` | 1x1x2 | 1 | 20 | A An/Aus, E An/Aus |
| SR Latch | `gate_sr_latch` | 2x1x2 | 1 | 20 | 2x A An/Aus, 2x E An/Aus |
| Subtract | `gate_float_subtract` | 2x1x2 | 1 | 20 | A Zahl, 2x E Zahl |
| Threshold Gate | `gate_float_threshold` | 1x1x2 | 1 | 20 | A An/Aus, E Zahl |
| Train Junction Controller | `gate_train_junction` | 1x1x2 | 1 | 20 | A An/Aus, E An/Aus |
| Trigonometry | `gate_float_sin` | 1x1x2 | 1 | 20 | A Zahl, E Zahl |
| Up/Down | `gate_up_down` | 2x1x2 | 1 | 20 | A Zahl, 2x E An/Aus |
| Xor | `gate_bool_xor` | 2x1x2 | 1 | 20 | A An/Aus, 2x E An/Aus |

## Anzeigen (Kategorie 6) - Einzelheiten: [Anzeigen.md](Anzeigen.md)

| Name | Datei-Name | Größe | Masse | Preis | Anschlüsse |
|---|---|---|---|---|---|
| Artificial Horizon | `artificial_horizon` | 1x1x1 | 1 | 20 | E An/Aus, E Strom |
| Buzzer | `buzzer` | 1x1x1 | 1 | 100 | E An/Aus, E Strom |
| Clock | `clock` | 1x2x1 | 1 | 100 | A Zahl, E An/Aus, E Strom |
| Compass Ball | `compass` | 1x1x1 | 1 | 20 | E An/Aus, E Strom |
| Dial | `dial` | 1x2x1 | 1 | 20 | E An/Aus, E Strom, E Zahl |
| Digital Display | `digital_display` | 1x1x2 | 2 | 20 | E An/Aus, E Strom, E Zahl |
| Gauge Display | `gauge_display` | 1x2x2 | 2 | 20 | E An/Aus, E Strom, 2x E Zahl |
| HUD Large | `monitor_hud_3` | 3x1x3 | 18 | 10000 | A Composite, E An/Aus, E Strom, E Video |
| HUD Small | `monitor_hud_1` | 1x1x1 | 2 | 2000 | A Composite, E An/Aus, E Strom, E Video |
| Indicator Light | `indicator` | 1x1x1 | 1 | 20 | E An/Aus, E Strom |
| Indicator Light (RGB) | `indicator_rgb` | 1x1x1 | 1 | 50 | E Composite, E Strom |
| Instrument Panel | `instrument_display` | 1x2x1 | 1 | 200 | A Composite, A Strom, E An/Aus, E Composite |
| Laser Beacon | `laser_beacon` | 1x2x1 | 1 | 5 | E An/Aus, E Strom, E Zahl |
| Monitor 1x1 | `monitor_1` | 1x1x1 | 4 | 500 | A Composite, E An/Aus, E Strom, E Video |
| Monitor 1x2 | `monitor_1x2` | 2x1x1 | 8 | 1000 | A Composite, E An/Aus, E Strom, E Video |
| Monitor 1x3 | `monitor_1x3` | 3x1x1 | 12 | 1500 | A Composite, E An/Aus, E Strom, E Video |
| Monitor 2x2 | `monitor_2` | 2x1x2 | 16 | 2000 | A Composite, E An/Aus, E Strom, E Video |
| Monitor 2x3 | `monitor_2x3` | 3x1x2 | 24 | 3000 | A Composite, E An/Aus, E Strom, E Video |
| Monitor 3x3 | `monitor_3` | 3x1x3 | 36 | 4500 | A Composite, E An/Aus, E Strom, E Video |
| Monitor 5x3 | `monitor_5` | 5x1x3 | 60 | 7500 | A Composite, E An/Aus, E Strom, E Video |
| Monitor 9x5 | `monitor_9` | 9x1x5 | 180 | 20000 | A Composite, E An/Aus, E Strom, E Video |
| Paintable Indicator | `sign` | 1x1x1 | 2 | 100 | E An/Aus, E Strom |
| Paintable Sign | `sign_na` | 1x1x1 | 1 | 50 |  |
| Speaker (Small) | `speaker` | 1x2x1 | 1 | 250 | A An/Aus, E Strom, E Ton |
| Viewing Scope | `viewing_scope` | 1x1x1 | 5 | 2000 | A An/Aus, E Strom, E Video |

## Sensoren (Kategorie 7) - Einzelheiten: [Sensoren.md](Sensoren.md)

| Name | Datei-Name | Größe | Masse | Preis | Anschlüsse |
|---|---|---|---|---|---|
| Altimeter | `altimeter` | 1x1x1 | 1 | 20 | A Zahl |
| Angular Speed Sensor | `angular_speed_sensor` | 1x1x1 | 1 | 20 | A Zahl |
| Astronomy Sensor | `astronomy_sensor` | 1x1x1 | 1 | 150 | A Composite |
| Barometer | `barometer` | 1x2x1 | 1 | 20 | A Zahl |
| Compass Sensor | `compass_sensor` | 1x2x1 | 1 | 20 | A Zahl, E An/Aus, E Strom |
| Contact Sensor | `pressure_sensor` | 1x2x1 | 1 | 20 | A An/Aus |
| Distance Sensor | `distance_sensor` | 1x2x1 | 1 | 20 | A Zahl, E Strom |
| Fishfinder | `fish_finder` | 1x1x1 | 10 | 500 | A Composite, E An/Aus, E Strom |
| Gas Meter | `gas_measure` | 1x2x1 | 1 | 20 | A Composite, 2x A Zahl |
| GPS Sensor | `gps_sensor` | 1x1x2 | 1 | 20 | 2x A Zahl, E Strom |
| Humidity Sensor | `humidity_sensor` | 1x2x1 | 1 | 400 | A Zahl |
| Impact Sensor | `impact_sensor` | 1x1x1 | 1 | 20 | A An/Aus |
| Laser Distance Sensor | `laser_distance_sensor` | 1x4x1 | 1 | 100 | A Zahl, E An/Aus, E Composite, E Strom, E Zahl |
| Laser Point Sensor | `laser_point_sensor` | 1x3x1 | 2 | 100 | A Composite, E Strom, E Zahl |
| Laser Sensor (Missile) | `radar_advanced_missile_laser` | 1x2x1 | 5 | 800 | 2x A Composite, E An/Aus, E Strom, E Zahl |
| Linear Speed Sensor | `linear_speed_sensor` | 1x1x1 | 1 | 20 | A Zahl |
| Liquid Meter | `water_measure` | 1x2x1 | 1 | 20 | A Composite, 2x A Zahl |
| Microphone | `mic` | 1x2x1 | 1 | 250 | A An/Aus, A Ton, E An/Aus, E Strom |
| Physics Sensor | `physics_sensor` | 1x1x1 | 1 | 20 | A Composite, E Strom |
| Player Sensor | `player_sensor` | 1x2x1 | 1 | 50 | A An/Aus, A Zahl |
| Radar | `radar` | 3x1x3 | 10 | 1000 | A An/Aus, 3x A Zahl, E Strom, 2x E Zahl |
| Radar (AWACS) | `radar_advanced_awacs` | 37x5x37 | 1100 | 10000 | A Composite, A Zahl, E An/Aus, E Composite, E Strom |
| Radar (Basic) | `radar_advanced` | 3x1x3 | 10 | 1000 | A Composite, A Zahl, E An/Aus, E Composite, E Strom |
| Radar (Dish) | `radar_advanced_dish` | 19x10x20 | 550 | 5000 | A Composite, A Zahl, E An/Aus, E Composite, E Strom |
| Radar (Dish) | `radar_dish` | 21x10x11 | 150 | 3000 | A An/Aus, 3x A Zahl, E Strom, E Zahl |
| Radar (Huge) | `radar_huge` | 37x5x37 | 1100 | 10000 | A Composite, E Strom, 2x E Zahl |
| Radar (Large) | `radar_large` | 7x16x7 | 300 | 5000 | A An/Aus, 4x A Zahl, E Strom, 3x E Zahl |
| Radar (Missile) | `radar_advanced_missile` | 1x2x1 | 5 | 800 | 2x A Composite, A Zahl, E An/Aus, E Strom |
| Radar (Phalanx) | `radar_advanced_phalanx` | 3x3x3 | 55 | 2000 | A Composite, A Zahl, E An/Aus, E Composite, E Strom |
| Radar Detector | `radar_detector` | 1x2x1 | 1 | 1000 | A An/Aus |
| Radiation Detector | `radiation_detector` | 1x1x1 | 1 | 250 | A Zahl |
| Rain Sensor | `rain_sensor` | 1x2x1 | 1 | 180 | A Zahl |
| Sonar (Large) | `radar_sonar` | 7x2x7 | 25 | 1000 | A An/Aus, 3x A Zahl, E Strom, 2x E Zahl |
| Sonar (Large) | `sonar_advanced_7` | 7x5x7 | 200 | 4000 | A Composite, 2x E An/Aus, E Strom |
| Sonar (Medium) | `sonar_advanced_5` | 5x3x5 | 50 | 2000 | A Composite, 2x E An/Aus, E Strom |
| Sonar (Small) | `radar_sonar_small` | 3x1x3 | 10 | 1000 | A An/Aus, 3x A Zahl, E Strom, 2x E Zahl |
| Sonar (Small) | `sonar_advanced` | 3x1x3 | 10 | 1000 | 2x A Composite, 2x E An/Aus, E Strom |
| Temperature Probe | `temperature_probe` | 1x1x1 | 1 | 250 | A Zahl |
| Tilt Sensor | `rotation_sensor` | 1x1x1 | 1 | 20 | A Zahl |
| Transponder Locator | `transponder_locator` | 1x2x1 | 1 | 20 | A An/Aus, E An/Aus, E Strom |
| Wind Sensor | `wind_sensor` | 1x2x1 | 1 | 200 | 2x A Zahl |

## Deko (Kategorie 8) - Einzelheiten: [Deko.md](Deko.md)

| Name | Datei-Name | Größe | Masse | Preis | Anschlüsse |
|---|---|---|---|---|---|
| Flag (Large) | `flag_large` | 1x7x1 | 3 | 100 |  |
| Flag (Medium) | `flag_medium` | 1x5x1 | 2 | 75 |  |
| Flag (Small) | `flag_small` | 1x3x1 | 1 | 25 |  |
| Large Tyre | `tyre_large` | 5x2x5 | 12 | 20 |  |
| Railing Segment Corner | `railing_segment_corner` | 1x4x1 | 2 | 30 |  |
| Railing Segment Corner Diagonal | `railing_segment_corner_diag` | 1x4x1 | 2 | 30 |  |
| Railing Segment Curve | `railing_segment_curve` | 3x4x3 | 5 | 40 |  |
| Railing Segment End | `railing_segment_end` | 1x4x1 | 2 | 30 |  |
| Railing Segment End Diagonal | `railing_segment_end_diag` | 1x4x1 | 2 | 30 |  |
| Railing Segment End Incline | `railing_segment_angle_end` | 1x5x1 | 2 | 30 |  |
| Railing Segment Extension | `railing_segment_extension` | 1x4x1 | 2 | 30 |  |
| Railing Segment Extension Diagonal | `railing_segment_extension_diag` | 1x4x1 | 2 | 30 |  |
| Railing Segment Extension Incline | `railing_extension_angle` | 1x4x1 | 2 | 30 |  |
| Railing Segment Incline | `railing_segment_angle` | 1x5x1 | 2 | 30 |  |
| Railing Segment Middle | `railing_segment_middle` | 1x4x1 | 2 | 30 |  |
| Railing Segment Middle Diagonal | `railing_segment_middle_diag` | 1x4x1 | 2 | 30 |  |
| Small Tyre | `tyre_small` | 3x1x3 | 4 | 15 |  |

## Fluessigkeiten (Kategorie 9) - Einzelheiten: [Fluessigkeiten.md](Fluessigkeiten.md)

| Name | Datei-Name | Größe | Masse | Preis | Anschlüsse |
|---|---|---|---|---|---|
| Air Filter | `air_filter` | 1x1x1 | 1 | 50 | A Fluessigkeit/Gas |
| Air Ram | `modular_engine_air_ram` | 1x1x1 | 1 | 50 | A Fluessigkeit/Gas |
| Air Scoop Intake 1x1 | `scoop_intake_2` | 1x1x1 | 1 | 30 | E Fluessigkeit/Gas |
| Air-Air Heat Exchanger 2x2 | `heat_exchanger_2_2` | 2x1x2 | 4 | 30 | 2x A Zahl, 4x E Fluessigkeit/Gas |
| Air-Air Heat Exchanger 2x5 | `heat_exchanger_5_5` | 2x5x5 | 10 | 70 | 2x A Zahl, 4x E Fluessigkeit/Gas |
| Air-Air Heat Exchanger 3x9 | `heat_exchanger_9_9` | 3x9x9 | 27 | 100 | 2x A Zahl, 4x E Fluessigkeit/Gas |
| Air-Liquid Heat Exchanger 1x2 | `air_exchanger` | 1x1x2 | 2 | 15 | 2x A Zahl, 4x E Fluessigkeit/Gas |
| Air-Liquid Heat Exchanger 5x2 | `air_exchanger_5_2` | 1x2x5 | 7 | 30 | 2x A Zahl, 4x E Fluessigkeit/Gas |
| Air-Liquid Heat Exchanger 5x3 | `air_exchanger_5_3` | 3x3x5 | 45 | 50 | 2x A Zahl, 4x E Fluessigkeit/Gas |
| Air-Liquid Heat Exchanger 9x3 | `air_exchanger_9_3` | 3x3x9 | 81 | 80 | 2x A Zahl, 4x E Fluessigkeit/Gas |
| Air-Liquid Heat Exchanger 9x5 | `air_exchanger_9_5` | 5x5x9 | 225 | 150 | 2x A Zahl, 4x E Fluessigkeit/Gas |
| Catalytic Converter | `catalytic_converter` | 1x1x1 | 1 | 100 | 2x E Fluessigkeit/Gas |
| Centrifugal Separator | `separator` | 5x9x5 | 80 | 480 | A Drehmoment, 2x A Fluessigkeit/Gas, E Fluessigkeit/Gas |
| Cryo Cooler | `cryo_cooler` | 1x1x0 | 4 | 30 | 2x A Zahl, E An/Aus, 4x E Fluessigkeit/Gas, E Strom |
| Desalinator | `desalinator` | 1x5x1 | 5 | 400 | 2x E Fluessigkeit/Gas |
| Fluid Exhaust | `fluid_exhaust` | 1x2x1 | 1 | 100 | E Fluessigkeit/Gas |
| Fluid Filter | `fluid_filter` | 1x2x1 | 5 | 400 | A Zahl, 2x E Fluessigkeit/Gas |
| Fluid Filter | `fluid_filter_v2` | 1x2x1 | 5 | 400 | 2x E Fluessigkeit/Gas |
| Fluid Flow Valve | `fluid_valve_flow` | 1x2x1 | 4 | 100 | 2x A Fluessigkeit/Gas, A Zahl |
| Fluid Heat Radiator | `fluid_radiator` | 3x3x1 | 10 | 200 | 2x E Fluessigkeit/Gas |
| Fluid Heat Radiator 3x3 (Electric) | `fluid_radiator_electric` | 3x1x3 | 10 | 400 | A Fluessigkeit/Gas, A Strom, A Zahl, E An/Aus, E Fluessigkeit/Gas |
| Fluid Heat Radiator 5x5 (Electric) | `fluid_radiator_electric_5` | 5x1x5 | 25 | 700 | A Strom, A Zahl, E An/Aus, 2x E Fluessigkeit/Gas |
| Fluid Heat Sink | `fluid_heat_sink` | 5x3x1 | 18 | 300 | 2x E Fluessigkeit/Gas |
| Fluid Intake | `fluid_intake` | 3x2x1 | 1 | 100 | A Fluessigkeit/Gas |
| Fluid Jet | `water_jet` | 3x7x3 | 10 | 3000 | E Drehmoment, E Fluessigkeit/Gas, E Strom, 3x E Zahl |
| Fluid On/Off Valve | `fluid_valve_on_off` | 2x2x1 | 4 | 100 | 2x A Fluessigkeit/Gas, A Zahl, E An/Aus, E Strom |
| Fluid On/Off Valve (Manual) | `fluid_valve_on_off_manual` | 1x1x1 | 1 | 100 | 2x A Fluessigkeit/Gas, A Zahl |
| Fluid Port | `water_inlet` | 1x2x1 | 1 | 50 | A Fluessigkeit/Gas |
| Fluid Port | `water_outlet` | 1x2x1 | 1 | 50 | A Fluessigkeit/Gas |
| Fluid Port End | `fluid_port_end` | 1x1x1 | 1 | 50 | A Fluessigkeit/Gas |
| Fluid Pressure Sensor | `fluid_pressure` | 1x2x1 | 4 | 100 | A Fluessigkeit/Gas, A Zahl |
| Fluid Pump | `water_pump` | 3x1x1 | 4 | 100 | A Zahl, E An/Aus, 2x E Fluessigkeit/Gas, E Strom |
| Fluid Pump (Manual) | `water_pump_manual` | 2x3x1 | 4 | 100 | A Fluessigkeit/Gas, A Zahl, E Fluessigkeit/Gas |
| Fluid Slot Port | `water_suction_duct` | 3x2x4 | 12 | 100 | A Fluessigkeit/Gas |
| Fluid Spawner | `water_spawner` | 1x2x1 | 1 | 20 |  |
| Fluid Tank Large | `fluid_tank_large` | 3x3x5 | 22 | 20 | 2x A Zahl, 2x E Fluessigkeit/Gas |
| Fluid Tank Medium | `fluid_tank_medium` | 2x2x3 | 6 | 20 | 2x A Zahl, 2x E Fluessigkeit/Gas |
| Fluid Tank Small | `fluid_tank_small` | 1x1x2 | 1 | 20 | 2x A Zahl, 2x E Fluessigkeit/Gas |
| Fluid Variable Valve | `fluid_valve_variable` | 2x2x1 | 4 | 100 | 2x A Fluessigkeit/Gas, A Zahl, E Strom, E Zahl |
| Fractional Distillation Port | `distillation_tray` | 3x5x3 | 36 | 80 | A Fluessigkeit/Gas |
| Gas Relief Valve | `relief_valve_gas` | 1x1x1 | 2 | 150 | 2x A Fluessigkeit/Gas, A Zahl |
| Gas Tank (Huge) | `fluid_tank_compressed_gas_5_9` | 5x9x5 | 22 | 20 | 2x A Zahl, E Fluessigkeit/Gas |
| Gas Tank (Large) | `fluid_tank_compressed_gas_3_7` | 3x7x3 | 12 | 20 | 2x A Zahl, E Fluessigkeit/Gas |
| Gas Tank (Medium) | `fluid_tank_compressed_gas_1_7` | 1x7x1 | 5 | 20 | 2x A Zahl, E Fluessigkeit/Gas |
| Gas Tank (Small) | `fluid_tank_compressed_gas_1_3` | 1x3x1 | 2 | 20 | 2x A Zahl, E Fluessigkeit/Gas |
| Hydrogen Electrolyser | `electrolyser` | 1x6x3 | 16 | 575 | 2x A Fluessigkeit/Gas, E An/Aus, E Strom |
| Hydrogen Fuel Cell | `hydrogen_fuel_cell` | 3x5x3 | 50 | 800 | A Fluessigkeit/Gas, 2x E Fluessigkeit/Gas, E Strom |
| Impeller Pump | `turbocharger` | 3x1x3 | 9 | 50 | A Drehmoment, A Zahl, 2x E Fluessigkeit/Gas |
| Impeller Pump (Small) | `turbocharger_small` | 1x1x1 | 1 | 40 | A Drehmoment, A Zahl, 2x E Fluessigkeit/Gas |
| Large Fluid Pump | `water_pump_large` | 2x2x2 | 10 | 200 | A Zahl, E An/Aus, 2x E Fluessigkeit/Gas, E Strom |
| Liquid Relief Valve | `relief_valve_liquid` | 1x1x1 | 2 | 150 | 2x A Fluessigkeit/Gas, A Zahl |
| Liquid-Liquid Heat Exchanger 2x2 | `intercooler` | 1x2x2 | 4 | 30 | 2x A Zahl, 4x E Fluessigkeit/Gas |
| Liquid-Liquid Heat Exchanger 5x5 | `intercooler_large` | 1x5x5 | 16 | 50 | 2x A Zahl, 4x E Fluessigkeit/Gas |
| Slurry Filter | `slurry_filter` | 5x15x9 | 140 | 320 | 2x A Fluessigkeit/Gas, 2x E Fluessigkeit/Gas |
| Steam Whistle | `steam_whistle` | 1x4x1 | 4 | 50 | E An/Aus, E Fluessigkeit/Gas |

## Elektrik (Kategorie 10) - Einzelheiten: [Elektrik.md](Elektrik.md)

| Name | Datei-Name | Größe | Masse | Preis | Anschlüsse |
|---|---|---|---|---|---|
| Electric Battery Large | `battery_large` | 7x5x5 | 800 | 10000 | A Zahl, E Strom |
| Electric Battery Medium | `battery_medium` | 3x2x2 | 60 | 1200 | A Zahl, E Strom |
| Electric Battery Small | `battery_small` | 2x1x1 | 10 | 150 | A Zahl, E Strom |
| Electric Charger | `electric_diode` | 1x1x2 | 1 | 100 | 2x A Strom |
| Electric Circuit Breaker | `electric_curcuit_breaker` | 1x2x1 | 1 | 100 | 2x E Strom |
| Electric Relay | `electric_relay` | 3x1x1 | 1 | 100 | 2x A Strom, E An/Aus |
| Large Generator | `generator_large` | 5x5x5 | 400 | 12000 | A Zahl, E Drehmoment, E Strom |
| Large Solar Cell | `solar_large` | 5x1x5 | 40 | 8000 | E Strom |
| Medium Generator | `generator_medium` | 3x3x3 | 100 | 2000 | A Zahl, E Drehmoment, E Strom |
| Small Generator | `generator_small` | 1x1x1 | 5 | 600 | A Zahl, E Drehmoment, E Strom |
| Solar Cell | `solar` | 1x1x1 | 2 | 400 | E Strom |

## Strahltriebwerke (Kategorie 11) - Einzelheiten: [Strahltriebwerke.md](Strahltriebwerke.md)

| Name | Datei-Name | Größe | Masse | Preis | Anschlüsse |
|---|---|---|---|---|---|
| Jet Combustion Chamber | `jet_engine_combustion_chamber` | 3x3x3 | 20 | 200 | 3x A Zahl, E Fluessigkeit/Gas, E Zahl |
| Jet Compressor | `jet_engine_compressor` | 3x5x3 | 20 | 200 | 3x A Zahl, E An/Aus, E Strom |
| Jet Duct Angle | `jet_engine_duct_angle` | 3x3x3 | 5 | 50 |  |
| Jet Duct Cross | `jet_engine_duct_cross` | 3x3x3 | 5 | 50 |  |
| Jet Duct Diagonal | `jet_engine_duct_diagonal` | 3x3x4 | 5 | 50 |  |
| Jet Duct Straight | `jet_engine_duct_straight` | 3x1x3 | 3 | 30 |  |
| Jet Duct T | `jet_engine_duct_t` | 3x3x3 | 5 | 50 |  |
| Jet Exhaust | `jet_engine_exhaust_basic` | 3x2x3 | 5 | 500 | 2x A Zahl, E Zahl |
| Jet Exhaust Afterburner | `jet_engine_exhaust_afterburner` | 3x5x3 | 10 | 750 | 2x A Zahl, E An/Aus, E Fluessigkeit/Gas, E Zahl |
| Jet Exhaust Rotating | `jet_engine_exhaust_rotating` | 3x4x3 | 10 | 800 | 2x A Zahl, E Strom, 2x E Zahl |
| Jet Turbine Medium | `jet_engine_turbine_medium` | 3x3x3 | 20 | 200 | 3x A Zahl, E Drehmoment, E Strom |
| Jet Turbine Small | `jet_engine_turbine_small` | 3x2x3 | 15 | 150 | 3x A Zahl, E Strom |
| Large Jet Intake | `jet_engine_intake_large` | 7x2x7 | 10 | 500 | 2x A Zahl |
| Small Jet Intake | `jet_engine_intake_small` | 3x1x3 | 5 | 250 | 2x A Zahl |

## Waffen (Kategorie 12) - Einzelheiten: [Waffen.md](Waffen.md)

| Name | Datei-Name | Größe | Masse | Preis | Anschlüsse |
|---|---|---|---|---|---|
| Artillery Cannon | `gun_xl` | 3x22x3 | 200 | 100 | A An/Aus, 2x E An/Aus, E Zahl |
| Artillery Cannon Barrel Extension | `gun_xl_barrel` | 3x4x3 | 80 | 50 |  |
| Artillery Cannon Barrel Extension | `gun_xl_barrel_1` | 3x4x3 | 80 | 50 |  |
| Artillery Cannon Barrel Extension | `gun_xl_barrel_2` | 3x4x3 | 80 | 50 |  |
| Artillery Cannon Barrel Extension | `gun_xl_barrel_3` | 3x4x3 | 80 | 50 |  |
| Artillery Cannon Belt (Connector) | `gun_belt_receiver_xl` | 1x1x4 | 4 | 100 | 2x A An/Aus |
| Artillery Cannon Belt (Corner Inner) | `gun_belt_corner_flat_xl` | 1x4x4 | 15 | 100 | A An/Aus |
| Artillery Cannon Belt (Corner Outer) | `gun_belt_corner_flat_reverse_xl` | 1x4x4 | 15 | 100 | A An/Aus |
| Artillery Cannon Belt (Corner) | `gun_belt_corner_xl` | 1x1x4 | 4 | 100 | A An/Aus |
| Artillery Cannon Belt (Feeder) | `gun_belt_loader_xl` | 1x1x5 | 5 | 100 | A An/Aus, E An/Aus, E Strom |
| Artillery Cannon Belt (Flexible) | `gun_belt_flex_xl` | 1x2x4 | 4 | 100 | E Seil/Munition |
| Artillery Cannon Belt (Junction) | `gun_belt_junction_xl` | 1x1x4 | 4 | 100 | A An/Aus, E An/Aus |
| Artillery Cannon Belt (Straight) | `gun_belt_straight_xl` | 1x1x4 | 4 | 100 | A An/Aus |
| Artillery Cannon Muzzle Brake | `gun_xl_muzzle` | 3x5x3 | 80 | 50 |  |
| Artillery Cannon Muzzle Brake | `gun_xl_muzzle_1` | 3x5x3 | 80 | 50 |  |
| Artillery Cannon Muzzle Brake | `gun_xl_muzzle_2` | 3x5x3 | 80 | 50 |  |
| Autocannon Ammo Drum (Large) | `gun_drum_large` | 4x3x4 | 40 | 100 | A Zahl |
| Autocannon Ammo Drum (Medium) | `gun_drum_medium` | 3x3x3 | 20 | 100 | A Zahl |
| Autocannon Ammo Drum (Small) | `gun_drum_small` | 2x3x2 | 10 | 100 | A Zahl |
| Autocannon Belt (Connector) | `gun_belt_receiver` | 1x1x3 | 3 | 100 | 2x A An/Aus |
| Autocannon Belt (Corner Flat) | `gun_belt_corner_flat` | 1x3x3 | 9 | 100 | A An/Aus |
| Autocannon Belt (Corner) | `gun_belt_corner` | 1x1x3 | 3 | 100 | A An/Aus |
| Autocannon Belt (Feeder) | `gun_belt_loader` | 1x1x4 | 4 | 100 | A An/Aus, E An/Aus, E Strom |
| Autocannon Belt (Flexible) | `gun_belt_flex` | 1x2x3 | 3 | 100 | E Seil/Munition |
| Autocannon Belt (Junction) | `gun_belt_junction` | 1x1x3 | 3 | 100 | A An/Aus, E An/Aus |
| Autocannon Belt (Straight) | `gun_belt_straight` | 1x1x3 | 3 | 100 | A An/Aus |
| Battle Cannon | `gun_l` | 3x12x2 | 100 | 100 | A An/Aus, 2x E An/Aus, E Zahl |
| Battle Cannon Barrel Extension | `gun_l_barrel` | 1x3x1 | 40 | 50 |  |
| Battle Cannon Barrel Extension | `gun_l_barrel_1` | 3x3x3 | 40 | 50 |  |
| Battle Cannon Barrel Extension | `gun_l_barrel_2` | 1x3x2 | 40 | 50 |  |
| Battle Cannon Barrel Extension | `gun_l_barrel_3` | 3x3x3 | 40 | 50 |  |
| Battle Cannon Belt (Connector) | `gun_belt_receiver_l` | 1x1x3 | 3 | 100 | 2x A An/Aus |
| Battle Cannon Belt (Corner Inner) | `gun_belt_corner_flat_l` | 1x3x3 | 9 | 100 | A An/Aus |
| Battle Cannon Belt (Corner Outer) | `gun_belt_corner_flat_reverse_l` | 1x3x3 | 9 | 100 | A An/Aus |
| Battle Cannon Belt (Corner) | `gun_belt_corner_l` | 1x1x3 | 3 | 100 | A An/Aus |
| Battle Cannon Belt (Feeder) | `gun_belt_loader_l` | 1x1x4 | 4 | 100 | A An/Aus, E An/Aus, E Strom |
| Battle Cannon Belt (Flexible) | `gun_belt_flex_l` | 1x2x3 | 3 | 100 | E Seil/Munition |
| Battle Cannon Belt (Junction) | `gun_belt_junction_l` | 1x1x3 | 3 | 100 | A An/Aus, E An/Aus |
| Battle Cannon Belt (Straight) | `gun_belt_straight_l` | 1x1x3 | 3 | 100 | A An/Aus |
| Battle Cannon Muzzle Brake | `gun_l_muzzle` | 1x4x1 | 40 | 50 |  |
| Battle Cannon Muzzle Brake | `gun_l_muzzle_1` | 3x4x1 | 40 | 50 |  |
| Battle Cannon Muzzle Brake | `gun_l_muzzle_2` | 3x4x3 | 40 | 50 |  |
| Bertha Cannon | `gun_xxl` | 5x30x5 | 500 | 100 | A An/Aus, 2x E An/Aus, E Zahl |
| Bertha Cannon Barrel Extension | `gun_xxl_barrel` | 3x4x3 | 200 | 50 |  |
| Bertha Cannon Belt (Connector) | `gun_belt_receiver_xxl` | 3x3x7 | 63 | 100 | 2x A An/Aus |
| Bertha Cannon Belt (Corner Inner) | `gun_belt_corner_flat_xxl` | 3x7x7 | 138 | 100 | A An/Aus |
| Bertha Cannon Belt (Corner Outer) | `gun_belt_corner_flat_reverse_xxl` | 3x7x7 | 138 | 100 | A An/Aus |
| Bertha Cannon Belt (Corner) | `gun_belt_corner_xxl` | 3x3x7 | 63 | 100 | A An/Aus |
| Bertha Cannon Belt (Feeder) | `gun_belt_loader_xxl` | 3x3x10 | 90 | 100 | A An/Aus, E An/Aus, E Strom |
| Bertha Cannon Belt (Flexible) | `gun_belt_flex_xxl` | 3x4x7 | 63 | 100 | E Seil/Munition |
| Bertha Cannon Belt (Junction) | `gun_belt_junction_xxl` | 3x3x7 | 63 | 100 | A An/Aus, E An/Aus |
| Bertha Cannon Belt (Straight) | `gun_belt_straight_xxl` | 3x3x7 | 63 | 100 | A An/Aus |
| Heavy Autocannon | `gun_m` | 1x10x1 | 50 | 100 | A An/Aus, E An/Aus, E Strom, E Zahl |
| Heavy Autocannon Barrel Extension | `gun_m_barrel` | 1x3x1 | 20 | 50 |  |
| Heavy Autocannon Barrel Extension | `gun_m_barrel_1` | 1x3x1 | 20 | 50 |  |
| Heavy Autocannon Barrel Extension | `gun_m_barrel_2` | 1x3x2 | 20 | 50 |  |
| Heavy Autocannon Barrel Extension | `gun_m_barrel_3` | 1x3x2 | 20 | 50 |  |
| Heavy Autocannon Muzzle Brake | `gun_m_muzzle` | 1x4x1 | 20 | 50 |  |
| Heavy Autocannon Muzzle Brake | `gun_m_muzzle_1` | 1x4x1 | 20 | 50 |  |
| Heavy Autocannon Muzzle Brake | `gun_m_muzzle_2` | 1x4x1 | 20 | 50 |  |
| Light Autocannon | `gun_s` | 2x6x1 | 25 | 100 | A An/Aus, E An/Aus, E Strom |
| Light Autocannon Barrel Extension | `gun_s_barrel` | 1x3x1 | 10 | 50 |  |
| Light Autocannon Muzzle Brake | `gun_s_muzzle` | 1x2x1 | 3 | 50 |  |
| Light Autocannon Muzzle Brake | `gun_s_muzzle_1` | 1x2x1 | 3 | 50 |  |
| Light Autocannon Muzzle Brake | `gun_s_muzzle_2` | 1x2x1 | 3 | 50 |  |
| Light Autocannon Muzzle Brake | `gun_s_muzzle_3` | 1x2x1 | 3 | 50 |  |
| Machine Gun | `gun_xs` | 1x4x1 | 10 | 50 | A An/Aus, E An/Aus |
| Machine Gun Ammo Box | `gun_drum_xsmall` | 1x1x1 | 5 | 20 | A Zahl |
| Machine Gun Ammo Box (Large) | `gun_drum_xsmall_2` | 1x2x2 | 20 | 30 | A Zahl |
| Rocket Launcher | `gun_rocket_launcher` | 1x8x1 | 50 | 100 | 2x A An/Aus, E An/Aus |
| Rotary Autocannon | `gun_v` | 4x13x2 | 400 | 100 | A An/Aus, E An/Aus, E Strom |
| Rotary Autocannon Barrel Extension | `gun_v_barrel` | 1x4x1 | 40 | 50 |  |
| Warhead (EMP) | `warhead_emp` | 5x13x5 | 500 | 200 | E An/Aus |
| Warhead (Large) | `warhead_large` | 5x9x5 | 400 | 100 | E An/Aus |
| Warhead (Medium) | `warhead_medium` | 3x5x3 | 80 | 50 | E An/Aus |
| Warhead (Small) | `warhead_small` | 1x2x1 | 15 | 25 | E An/Aus |
| Warhead Body (Large) | `warhead_body_large` | 5x9x5 | 400 | 100 | E An/Aus |
| Warhead Body (Medium) | `warhead_body_medium` | 3x5x3 | 80 | 50 | E An/Aus |
| Warhead Body (Small) | `warhead_body_small` | 1x2x1 | 15 | 25 | E An/Aus |

## Modulare-Motoren (Kategorie 13) - Einzelheiten: [Modulare-Motoren.md](Modulare-Motoren.md)

| Name | Datei-Name | Größe | Masse | Preis | Anschlüsse |
|---|---|---|---|---|---|
| Modular Engine Air Manifold | `modular_engine_air_manifold` | 1x1x1 | 1 | 10 | E Fluessigkeit/Gas, E Zahl |
| Modular Engine Alternator | `modular_engine_alternator` | 1x1x1 | 1 | 30 | A Strom, E Zahl |
| Modular Engine Clutch 1x1 | `modular_engine_clutch` | 1x1x1 | 1 | 15 | E Drehmoment, E Zahl |
| Modular Engine Clutch 3x3 | `modular_engine_clutch_3x3` | 3x1x3 | 9 | 25 | E Drehmoment, E Zahl |
| Modular Engine Clutch 5x5 | `modular_engine_clutch_5x5` | 5x1x5 | 25 | 50 | E Drehmoment, E Zahl |
| Modular Engine Coolant Manifold | `modular_engine_coolant_manifold` | 1x1x1 | 1 | 10 | A Fluessigkeit/Gas, E Fluessigkeit/Gas |
| Modular Engine Crankshaft 1x1 | `modular_engine_crankshaft` | 1x1x1 | 1 | 50 | A Zahl |
| Modular Engine Crankshaft 3x1 | `modular_engine_crankshaft_3x1` | 3x1x3 | 9 | 50 | A Zahl |
| Modular Engine Crankshaft 3x3 | `modular_engine_crankshaft_3x3` | 3x3x3 | 27 | 150 | A Zahl |
| Modular Engine Crankshaft 5x5 | `modular_engine_crankshaft_5x5` | 5x5x5 | 100 | 350 | A Zahl |
| Modular Engine Crankshaft Converter 3 to 1 | `modular_engine_crankshaft_converter_3x3` | 3x1x3 | 9 | 75 | A Zahl |
| Modular Engine Crankshaft Converter 5 to 3 | `modular_engine_crankshaft_converter_5x5` | 5x1x5 | 27 | 275 | A Zahl |
| Modular Engine Cylinder 1x1 | `modular_engine_cylinder_straight` | 1x1x1 | 1 | 50 | A Composite |
| Modular Engine Cylinder 3x3 | `modular_engine_piston_3x3` | 3x3x3 | 27 | 100 | A Composite |
| Modular Engine Cylinder 5x5 | `modular_engine_piston_5x5` | 5x5x5 | 100 | 150 | A Composite |
| Modular Engine Drive Belt 1x1 | `modular_engine_drive_belt` | 1x1x1 | 1 | 30 |  |
| Modular Engine Drive Belt 3x3 | `modular_engine_power_manifold_3x3` | 3x1x3 | 9 | 80 |  |
| Modular Engine Drive Belt 5x5 | `modular_engine_power_manifold_5x5` | 5x1x5 | 27 | 160 |  |
| Modular Engine Exhaust Manifold (Corner) | `modular_engine_exhaust_manifold_corner` | 1x1x1 | 1 | 10 | A Fluessigkeit/Gas |
| Modular Engine Exhaust Manifold (Straight) | `modular_engine_exhaust_manifold_straight` | 1x1x1 | 1 | 10 | A Fluessigkeit/Gas |
| Modular Engine Fluid Pump | `modular_engine_fluid_pump` | 1x1x1 | 1 | 50 | A Fluessigkeit/Gas, E Fluessigkeit/Gas, E Zahl |
| Modular Engine Flywheel 1x1 | `modular_engine_flywheel` | 3x1x3 | 100 | 450 | A Zahl |
| Modular Engine Flywheel 3x3 | `modular_engine_flywheel_3x3` | 5x1x5 | 200 | 650 | A Zahl |
| Modular Engine Flywheel 5x5 | `modular_engine_flywheel_5x5` | 7x1x7 | 300 | 850 | A Zahl |
| Modular Engine Fuel Manifold | `modular_engine_intake_manifold` | 1x1x1 | 1 | 10 | E Fluessigkeit/Gas, E Zahl |
| Modular Engine Manifold (Corner) | `modular_engine_manifold_corner` | 1x1x1 | 1 | 10 |  |
| Modular Engine Manifold (Straight) | `modular_engine_manifold_straight` | 1x1x1 | 1 | 10 |  |
| Modular Engine Manifold (T) | `modular_engine_manifold_t` | 1x1x1 | 1 | 10 |  |
| Modular Engine Starter | `modular_engine_starter` | 1x1x1 | 1 | 30 | E An/Aus, E Strom |
| Modular Engine Temperature Sensor | `modular_engine_sensor_temperature` | 1x1x1 | 1 | 50 | A Zahl |

## Industrie (Kategorie 14) - Einzelheiten: [Industrie.md](Industrie.md)

| Name | Datei-Name | Größe | Masse | Preis | Anschlüsse |
|---|---|---|---|---|---|
| Duct | `steam_coal_duct` | 3x3x3 | 12 | 50 | A Zahl |
| Duct Large | `steam_coal_duct_l` | 5x5x9 | 112 | 150 | A Zahl |
| Duct Medium | `steam_coal_duct_m` | 5x5x5 | 62 | 100 | A Zahl |
| Electric Furnace | `furnace_electric` | 3x5x3 | 220 | 900 | A Zahl, E An/Aus, 2x E Fluessigkeit/Gas, E Strom |
| Firebox | `steam_coal_firebox` | 3x3x5 | 100 | 100 | A Fluessigkeit/Gas, 2x A Zahl, E An/Aus, 3x E Fluessigkeit/Gas |
| Firebox Large | `steam_coal_firebox_l` | 5x5x7 | 400 | 200 | A Fluessigkeit/Gas, 2x A Zahl, E An/Aus, 3x E Fluessigkeit/Gas |
| Flexible Duct | `steam_coal_flex` | 3x2x3 | 20 | 50 | E Seil/Munition |
| Funnel Duct | `steam_coal_funnel` | 3x2x3 | 20 | 50 | E An/Aus |
| Hopper | `steam_coal_hopper` | 3x3x3 | 12 | 50 | A Zahl |
| Hopper Large | `steam_coal_hopper_l` | 5x5x9 | 112 | 150 | A Zahl |
| Hopper Medium | `steam_coal_hopper_m` | 5x5x5 | 62 | 100 | A Zahl |
| Industrial Diesel Furnace | `furnace_industrial` | 5x5x7 | 350 | 750 | A Fluessigkeit/Gas, 2x A Zahl, E An/Aus, 4x E Fluessigkeit/Gas |
| Lobster Pot | `lobster_pot` | 5x3x5 | 45 | 150 | A Zahl, E An/Aus |
| Mineral Converter | `mineral_converter` | 3x3x3 | 80 | 250000 | A Zahl, E Fluessigkeit/Gas |
| Net Anchor | `rope_hook_net` | 1x3x1 | 3 | 15 | A Composite, 3x E An/Aus, E Seil/Munition |
| Nuclear Control Rod | `steam_nuclear_control_rod` | 1x17x1 | 100 | 250 | A Zahl, E Zahl |
| Nuclear Fuel Assembly | `steam_nuclear_fuel_assembly` | 1x12x1 | 80 | 500 | A Zahl, E An/Aus |
| Nuclear Fuel Rod | `steam_nuclear_fuel_rod` | 1x9x1 | 80 | 2500 |  |
| Oil Rig Drill Clamp | `oil_rig_drill_grabber` | 3x2x3 | 30 | 100 | A An/Aus, E An/Aus, E Zahl |
| Oil Rig Drill Clamp (End) | `oil_rig_drill_grabber_end` | 1x2x1 | 5 | 500 | A An/Aus, E An/Aus |
| Oil Rig Drill Connector | `oil_rig_drill_connector` | 3x2x7 | 50 | 100 | 2x A An/Aus, 2x E An/Aus, E Zahl |
| Oil Rig Drill Swivel | `oil_rig_drill_swivel` | 3x5x3 | 30 | 1000 | A An/Aus, E An/Aus, 2x E Fluessigkeit/Gas |
| Oil Rig Pumpjack | `oil_rig_pumpjack` | 3x11x3 | 200 | 1000 | E Fluessigkeit/Gas |
| Oil Rig Pumpjack B | `oil_rig_pumpjack_b` | 1x10x1 | 500 | 0 |  |
| Oil Rig Rod Storage | `oil_rig_drill_storage` | 1x2x41 | 10 | 50 | A An/Aus |
| Oil Rig Rotary Table | `oil_rig_drill_driver` | 7x3x7 | 500 | 1000 | A Zahl, E An/Aus, E Drehmoment |
| Oil Rig Well Head | `oil_rig_well_head` | 9x25x9 | 1000 | 5000 | A An/Aus, 2x A Zahl, E An/Aus |
| Steam Boiler | `steam_boiler` | 5x5x7 | 500 | 250 | A Fluessigkeit/Gas, 2x A Zahl, 3x E Fluessigkeit/Gas |
| Steam Condenser | `steam_condenser` | 3x5x5 | 250 | 250 | A Fluessigkeit/Gas, 2x A Zahl, 3x E Fluessigkeit/Gas |
| Steam Piston (Large) | `steam_piston_5x5` | 5x15x5 | 300 | 2400 | 2x A Drehmoment, 4x A Fluessigkeit/Gas, 2x A Zahl |
| Steam Piston (Medium) | `steam_piston_3x3` | 3x9x3 | 120 | 600 | 2x A Drehmoment, 4x A Fluessigkeit/Gas, 2x A Zahl |
| Steam Piston (Small) | `steam_piston` | 1x6x1 | 12 | 90 | 2x A Drehmoment, 4x A Fluessigkeit/Gas, 2x A Zahl |
| Steam Turbine | `steam_turbine` | 5x9x5 | 500 | 250 | 2x A Drehmoment, A Fluessigkeit/Gas, E Fluessigkeit/Gas |
| Vacuum Duct | `steam_coal_vacuum` | 3x3x3 | 20 | 50 | E An/Aus, E Strom |
| Water Extractor | `water_extractor` | 3x3x3 | 20 | 100 | A Fluessigkeit/Gas, E An/Aus, E Strom |

## Fenster (Kategorie 15) - Einzelheiten: [Fenster.md](Fenster.md)

| Name | Datei-Name | Größe | Masse | Preis | Anschlüsse |
|---|---|---|---|---|---|
| Porthole | `window_porthole` | 1x5x3 | 8 | 50 |  |
| Porthole Small | `window_port` | 1x3x3 | 6 | 30 |  |
| Window 1x1 | `window_1x1` | 1x1x1 | 1 | 5 |  |
| Window 1x2 | `window_2x1` | 1x2x1 | 2 | 10 |  |
| Window 1x3 | `window_narrow` | 1x3x1 | 2 | 15 |  |
| Window 2x2 | `window_2x2` | 1x2x2 | 3 | 20 |  |
| Window 2x3 | `window_3x2` | 1x3x2 | 4 | 25 |  |
| Window 3x3 | `window_large` | 1x3x3 | 4 | 45 |  |
| Window Angle 1x1x1 | `window_1x1_wedge` | 1x1x1 | 1 | 5 |  |
| Window Angle 1x2x2 | `window_angle_m_1x2x2` | 2x2x1 | 2 | 20 |  |
| Window Angle 1x3x3 | `window_narrow_angle` | 3x3x1 | 2 | 45 |  |
| Window Angle 1x4x4 | `window_angle_xl_1x4x4` | 4x4x1 | 3 | 80 |  |
| Window Angle 2x1x1 | `window_angle_s_1x2` | 1x1x2 | 1 | 10 |  |
| Window Angle 2x2x2 | `window_angle_m_2x2x2` | 2x2x2 | 3 | 30 |  |
| Window Angle 2x3x3 | `window_angle_l_2x3x3` | 3x3x2 | 4 | 10 |  |
| Window Angle 2x4x4 | `window_angle_xl_2x4x4` | 4x4x2 | 5 | 160 |  |
| Window Angle 3x1x1 | `window_small_angle` | 1x1x3 | 2 | 15 |  |
| Window Angle 3x2x2 | `window_angle_m_3x2x2` | 2x2x3 | 4 | 60 |  |
| Window Angle 3x3x3 | `window_large_angle` | 3x3x3 | 5 | 135 |  |
| Window Angle 3x4x4 | `window_angle_xl_3x4x4` | 4x4x3 | 6 | 240 |  |
| Window Corner 2x3 | `window_corner_small` | 1x3x2 | 2 | 30 |  |
| Window Corner 3x4 | `window_corner` | 1x4x3 | 4 | 60 |  |
| Window Corner Full 1x1 | `window_corner_full_1x1` | 1x1x1 | 1 | 5 |  |
| Window Corner Full 2x2 | `window_corner_full_small` | 1x2x2 | 2 | 20 |  |
| Window Corner Full 3x3 | `window_corner_full_medium` | 1x3x3 | 4 | 45 |  |
| Window Corner Full 4x4 | `window_corner_full_large` | 1x4x4 | 5 | 80 |  |
| Window Diamond 1x1x2 | `window_diamond_s_1x1` | 2x1x1 | 1 | 5 |  |
| Window Diamond 1x2x3 | `window_diamond_m_1x2x3` | 3x2x1 | 2 | 15 |  |
| Window Diamond 1x3x4 | `window_diamond_l_1x3x4` | 4x3x1 | 2 | 30 |  |
| Window Diamond 1x4x5 | `window_diamond_xl_1x4x5` | 5x4x1 | 3 | 50 |  |
| Window Diamond 2x2x3 | `window_diamond_m_2x2x3` | 4x2x2 | 3 | 30 |  |
| Window Diamond 2x3x4 | `window_diamond_l_2x3x4` | 5x3x2 | 4 | 60 |  |
| Window Diamond 2x4x5 | `window_diamond_xl_2x4x5` | 6x4x2 | 5 | 100 |  |
| Window Diamond 3x2x3 | `window_diamond_m_3x2x3` | 5x2x3 | 4 | 45 |  |
| Window Diamond 3x3x4 | `window_diamond_l_3x3x4` | 6x3x3 | 5 | 90 |  |
| Window Diamond 3x4x5 | `window_diamond_xl_3x4x5` | 7x4x3 | 5 | 150 |  |
| Window Inverse Pyramid 1x1 | `window_1x1_inv_pyramid` | 1x1x1 | 1 | 5 |  |
| Window Inverse Pyramid 2x2x2 | `window_2x2_inv_pyramid` | 2x2x2 | 2 | 15 |  |
| Window Pyramid 1x1x1 | `window_1x1_pyramid` | 1x1x1 | 1 | 5 |  |
| Window Pyramid 2x2x2 | `window_2x2_pyramid` | 2x2x2 | 2 | 15 |  |
| Window Pyramid 3x3x3 | `window_corner_2` | 3x3x3 | 4 | 135 |  |

## Ohne-Kategorie (Kategorie -1) - Einzelheiten: [Ohne-Kategorie.md](Ohne-Kategorie.md)

| Name | Datei-Name | Größe | Masse | Preis | Anschlüsse |
|---|---|---|---|---|---|
| Handle | `handle` | 1x2x1 | 1 | 5 | A An/Aus |
| Pipe Angle Corner | `trans_corner` | 1x1x1 | 1 | 5 |  |
| Pipe Angle Corner (Enclosed) | `trans_block_corner` | 1x1x1 | 1 | 5 |  |
| Pipe Cross | `trans_cross` | 1x1x1 | 1 | 5 |  |
| Pipe Cross Corner | `trans_cross_corner` | 1x1x1 | 1 | 5 |  |
| Pipe Omni | `trans_omni` | 1x1x1 | 1 | 5 |  |
| Pipe T-Piece | `trans_t` | 1x1x1 | 1 | 5 |  |
| Pipe T-Piece (Enclosed) | `trans_block_t` | 1x1x1 | 1 | 5 |  |
| Pipe T-Piece Corner | `trans_t_corner` | 1x1x1 | 1 | 5 |  |
| Pivot (Power) | `multibody_pivot_torque_b` | 1x1x1 | 1 | 0 | A Drehmoment |
