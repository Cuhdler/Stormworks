# Ohne-Kategorie (Kategorie -1)

Aus den Spieldaten erzeugt von `tools/bauteile_holen.py` - nicht von Hand ändern.

## Handle (`handle`)

*A handle that you can attach to by interacting with [$[action_interact_left]] or [$[action_interact_right]].*
Interacting with [$[action_interact_left]] or [$[action_interact_right]] again will detach that hand. The handle can be used to drag vehicles around. If a vehicle is too heavy to move, you will be detached automatically when you move outside the handle's interaction range.

- Größe 1x2x1 Blöcke (voxel [0, 0, 0] .. [0, 1, 0]), Masse 1, Preis 5, Tags: basic
- Werte: rudder_surface_area=0, type=22

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Occupied | An/Aus | Ausgang | (0, 0, 0) | Outputs an on signal if a player is attached to the handle. |

## Pipe Angle Corner (`trans_corner`)

*A T-shaped pipe segment that can be used to branch piping into three directions.*

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 5, Tags: basic
- Werte: buoy_factor=0.5, buoy_force=1, engine_max_force=200, force_emitter_max_force=950, trans_conn_type=2, type=6

## Pipe Angle Corner (Enclosed) (`trans_block_corner`)

*A T-shaped pipe segment that can be used to branch piping into three directions.*

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 5
- Werte: buoy_factor=0.5, buoy_force=1, engine_max_force=200, force_emitter_max_force=950, trans_conn_type=2, type=6

## Pipe Cross (`trans_cross`)

*An X-shaped pipe segment that can be used to branch piping into four directions.*

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 5, Tags: basic
- Werte: buoy_factor=0.5, buoy_force=1, engine_max_force=200, force_emitter_max_force=950, trans_conn_type=2, type=6

## Pipe Cross Corner (`trans_cross_corner`)

*An X-shaped pipe segment that can be used to branch piping into five directions.*

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 5, Tags: basic
- Werte: buoy_factor=0.5, buoy_force=1, engine_max_force=200, force_emitter_max_force=950, trans_conn_type=2, type=6

## Pipe Omni (`trans_omni`)

*An omnidirectional pipe segment.*

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 5, Tags: basic
- Werte: buoy_factor=0.5, buoy_force=1, engine_max_force=200, force_emitter_max_force=950, trans_conn_type=2, type=6

## Pipe T-Piece (`trans_t`)

*A T-shaped pipe segment that can be used to branch piping into three directions.*

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 5, Tags: basic
- Werte: buoy_factor=0.5, buoy_force=1, engine_max_force=200, force_emitter_max_force=950, trans_conn_type=2, type=6

## Pipe T-Piece (Enclosed) (`trans_block_t`)

*A T-shaped pipe segment that can be used to branch piping into three directions.*

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 5
- Werte: buoy_factor=0.5, buoy_force=1, engine_max_force=200, force_emitter_max_force=950, trans_conn_type=2, type=6

## Pipe T-Piece Corner (`trans_t_corner`)

*A T-shaped pipe segment that can be used to branch piping into four directions.*

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 5, Tags: basic
- Werte: buoy_factor=0.5, buoy_force=1, engine_max_force=200, force_emitter_max_force=950, trans_conn_type=2, type=6

## Pivot (Power) (`multibody_pivot_torque_b`)


- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 0
- Werte: rudder_surface_area=0, type=7

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| RPS | Drehmoment | Ausgang | (0, 0, 0) | Power connection for transfering mechanical energy. |
