# Waffen (Kategorie 12)

Aus den Spieldaten erzeugt von `tools/bauteile_holen.py` - nicht von Hand ändern.

## Artillery Cannon (`gun_xl`)

*An artillery cannon.*
Artillery cannons fire high caliber explosive and armor-piercing shells over great distances.

- Größe 3x22x3 Blöcke (voxel [-1, -5, -1] .. [1, 16, 1]), Masse 200, Preis 100, Tags: weapon,cannon,artillery
- Werte: cable_length=-431602080, weapon_barrel_length_voxels=16, weapon_class=5, weapon_type=2

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Trigger | An/Aus | Eingang | (0, 0, 0) | When true: fires a loaded shell. |
| Loaded | An/Aus | Ausgang | (0, 1, 0) | Returns true when a shell is loaded and ready to fire. |
| Open Breech | An/Aus | Eingang | (1, -2, 0) | When true: opens the breech to allow shells to be loaded. |
| Fuse Timer | Zahl | Eingang | (0, -2, 0) | Sets the optional time-delay fuse in seconds for high-explosive and fragmentation ammo types. |

## Artillery Cannon Barrel Extension (`gun_xl_barrel`)

*An artillery cannon barrel extension.*
Barrel extensions increase weapon accuracy, but also produce more recoil force.

- Größe 3x4x3 Blöcke (voxel [-1, -1, -1] .. [1, 2, 1]), Masse 80, Preis 50, Tags: weapon,cannon,artillery
- Werte: cable_length=-431602080, weapon_barrel_length_voxels=4, weapon_class=5, weapon_type=4

## Artillery Cannon Barrel Extension (`gun_xl_barrel_1`)

*An artillery cannon barrel extension.*
Barrel extensions increase weapon accuracy, but also produce more recoil force.

- Größe 3x4x3 Blöcke (voxel [-1, -1, -1] .. [1, 2, 1]), Masse 80, Preis 50, Tags: weapon,cannon,artillery
- Werte: cable_length=-431602080, weapon_barrel_length_voxels=4, weapon_class=5, weapon_type=4

## Artillery Cannon Barrel Extension (`gun_xl_barrel_2`)

*An artillery cannon barrel extension.*
Barrel extensions increase weapon accuracy, but also produce more recoil force.

- Größe 3x4x3 Blöcke (voxel [-1, -1, -1] .. [1, 2, 1]), Masse 80, Preis 50, Tags: weapon,cannon,artillery
- Werte: cable_length=-431602080, weapon_barrel_length_voxels=4, weapon_class=5, weapon_type=4

## Artillery Cannon Barrel Extension (`gun_xl_barrel_3`)

*An artillery cannon barrel extension.*
Barrel extensions increase weapon accuracy, but also produce more recoil force.

- Größe 3x4x3 Blöcke (voxel [-1, -1, -1] .. [1, 2, 1]), Masse 80, Preis 50, Tags: weapon,cannon,artillery
- Werte: cable_length=-431602080, weapon_barrel_length_voxels=4, weapon_class=5, weapon_type=4

## Artillery Cannon Belt (Connector) (`gun_belt_receiver_xl`)

*An artillery cannon ammo belt.*
Cannon ammo belts can store and transfer ammo shells. Connector belts allow ammo transfers between vehicles. Spawned ammo type can be set in component properties window.

- Größe 1x1x4 Blöcke (voxel [0, 0, -1] .. [0, 0, 2]), Masse 4, Preis 100, Tags: weapon,cannon,belt,artillery
- Werte: cable_length=-431602080, weapon_ammo_capacity=1, weapon_belt_type=2, weapon_class=5

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Contains Ammo | An/Aus | Ausgang | (0, 0, 1) | Returns true if the belt contains a shell. |
| Connected | An/Aus | Ausgang | (0, 0, 0) | Returns true when two nearby receivers are aligned, and can transfer ammo between them. |

## Artillery Cannon Belt (Corner Inner) (`gun_belt_corner_flat_xl`)

*An artillery cannon ammo belt.*
Cannon ammo belts can store and transfer ammo shells. Spawned ammo type can be set in component properties window.

- Größe 1x4x4 Blöcke (voxel [0, -1, -2] .. [0, 2, 1]), Masse 15, Preis 100, Tags: weapon,cannon,belt,artillery
- Werte: cable_length=-431602080, weapon_ammo_capacity=1, weapon_class=5

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Contains Ammo | An/Aus | Ausgang | (0, 0, 0) | Returns true if the belt contains a shell. |

## Artillery Cannon Belt (Corner Outer) (`gun_belt_corner_flat_reverse_xl`)

*An artillery cannon ammo belt.*
Cannon ammo belts can store and transfer ammo shells. Spawned ammo type can be set in component properties window.

- Größe 1x4x4 Blöcke (voxel [0, -1, -1] .. [0, 2, 2]), Masse 15, Preis 100, Tags: weapon,cannon,belt,artillery
- Werte: cable_length=-431602080, weapon_ammo_capacity=1, weapon_class=5

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Contains Ammo | An/Aus | Ausgang | (0, 0, 0) | Returns true if the belt contains a shell. |

## Artillery Cannon Belt (Corner) (`gun_belt_corner_xl`)

*An artillery cannon ammo belt.*
Cannon ammo belts can store and transfer ammo shells. Spawned ammo type can be set in component properties window.

- Größe 1x1x4 Blöcke (voxel [0, 0, -1] .. [0, 0, 2]), Masse 4, Preis 100, Tags: weapon,cannon,belt,artillery
- Werte: cable_length=-431602080, weapon_ammo_capacity=1, weapon_class=5

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Contains Ammo | An/Aus | Ausgang | (0, 0, 0) | Returns true if the belt contains a shell. |

## Artillery Cannon Belt (Feeder) (`gun_belt_loader_xl`)

*An artillery cannon ammo belt.*
Cannon ammo belts can store and transfer ammo shells. Feeder belts transfer ammo forwards using electric power. Spawned ammo type can be set in component properties window.

- Größe 1x1x5 Blöcke (voxel [0, 0, -2] .. [0, 0, 2]), Masse 5, Preis 100, Tags: weapon,cannon,belt,artillery
- Werte: cable_length=-431602080, weapon_ammo_capacity=1, weapon_belt_type=1, weapon_class=5

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Feed | An/Aus | Eingang | (0, 0, -2) | Transfer shells in the direction of the arrow. |
| Contains Ammo | An/Aus | Ausgang | (0, 0, 0) | Returns true if the belt contains a shell. |
| Electric | Strom | Eingang | (0, 0, -2) | Electrical power connection. |

## Artillery Cannon Belt (Flexible) (`gun_belt_flex_xl`)

*An artillery cannon ammo belt.*
Flexible belts can be connected together by rope nodes to transfer ammo. Cannon ammo belts can store and transfer ammo shells. Spawned ammo type can be set in component properties window.

- Größe 1x2x4 Blöcke (voxel [0, 0, -1] .. [0, 1, 2]), Masse 4, Preis 100, Tags: weapon,cannon,belt,artillery
- Werte: cable_length=-431602080, logic_gate_subtype=11, weapon_ammo_capacity=1, weapon_belt_type=4, weapon_class=5

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Ammo | Seil/Munition | Eingang | (0, 1, 0) |  |

## Artillery Cannon Belt (Junction) (`gun_belt_junction_xl`)

*An artillery cannon ammo belt.*
Cannon ammo belts can store and transfer ammo shells. Junction belts redirect the path of ammo transfer. Spawned ammo type can be set in component properties window.

- Größe 1x1x4 Blöcke (voxel [0, 0, -1] .. [0, 0, 2]), Masse 4, Preis 100, Tags: weapon,cannon,belt,artillery
- Werte: cable_length=-431602080, weapon_ammo_capacity=1, weapon_belt_type=3, weapon_class=5

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Contains Ammo | An/Aus | Ausgang | (0, 0, 1) | Returns true if the belt contains a shell. |
| Junction Switch | An/Aus | Eingang | (0, 0, 0) | Switches the ammo transfer T-junction between the left and right sides. |

## Artillery Cannon Belt (Straight) (`gun_belt_straight_xl`)

*An artillery cannon ammo belt.*
Cannon ammo belts can store and transfer ammo shells. Spawned ammo type can be set in component properties window.

- Größe 1x1x4 Blöcke (voxel [0, 0, -1] .. [0, 0, 2]), Masse 4, Preis 100, Tags: weapon,cannon,belt,artillery
- Werte: cable_length=-431602080, weapon_ammo_capacity=1, weapon_class=5

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Contains Ammo | An/Aus | Ausgang | (0, 0, 0) | Returns true if the belt contains a shell. |

## Artillery Cannon Muzzle Brake (`gun_xl_muzzle`)

*A artillery cannon muzzle brake.*
A muzzle brake will reduce weapon recoil force when added to the end of a weapon barrel.

- Größe 3x5x3 Blöcke (voxel [-1, -1, -1] .. [1, 3, 1]), Masse 80, Preis 50, Tags: weapon,cannon,artillery
- Werte: cable_length=-431602080, weapon_barrel_length_voxels=4, weapon_class=5, weapon_type=7

## Artillery Cannon Muzzle Brake (`gun_xl_muzzle_1`)

*A artillery cannon muzzle brake.*
A muzzle brake will reduce weapon recoil force when added to the end of a weapon barrel.

- Größe 3x5x3 Blöcke (voxel [-1, -1, -1] .. [1, 3, 1]), Masse 80, Preis 50, Tags: weapon,cannon,artillery
- Werte: cable_length=-431602080, weapon_barrel_length_voxels=4, weapon_class=5, weapon_type=7

## Artillery Cannon Muzzle Brake (`gun_xl_muzzle_2`)

*A artillery cannon muzzle brake.*
A muzzle brake will reduce weapon recoil force when added to the end of a weapon barrel.

- Größe 3x5x3 Blöcke (voxel [-1, -1, -1] .. [1, 3, 1]), Masse 80, Preis 50, Tags: weapon,cannon,artillery
- Werte: cable_length=-431602080, weapon_barrel_length_voxels=4, weapon_class=5, weapon_type=7

## Autocannon Ammo Drum (Large) (`gun_drum_large`)

*A large capacity autocannon ammo drum.*
Ammo drums store autocannon cartridges of the caliber specified in the component properties window. Differing calibers cannot be mixed within a single ammo drum.

- Größe 4x3x4 Blöcke (voxel [-1, -1, -2] .. [2, 1, 1]), Masse 40, Preis 100, Tags: weapon,autocannon,belt
- Werte: cable_length=-431602080, weapon_ammo_capacity=500, weapon_type=5

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Ammo Count | Zahl | Ausgang | (-1, -1, 0) | Outputs the total ammo count stored in the drum. |

## Autocannon Ammo Drum (Medium) (`gun_drum_medium`)

*A medium capacity autocannon ammo drum.*
Ammo drums store autocannon cartridges of the caliber specified in the component properties window. Differing calibers cannot be mixed within a single ammo drum.

- Größe 3x3x3 Blöcke (voxel [-1, -1, -1] .. [1, 1, 1]), Masse 20, Preis 100, Tags: weapon,autocannon,belt
- Werte: cable_length=-431602080, weapon_ammo_capacity=200, weapon_type=5

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Ammo Count | Zahl | Ausgang | (-1, -1, 0) | Outputs the total ammo count stored in the drum. |

## Autocannon Ammo Drum (Small) (`gun_drum_small`)

*A small capacity autocannon ammo drum.*
Ammo drums store autocannon cartridges of the caliber specified in the component properties window. Differing calibers cannot be mixed within a single ammo drum.

- Größe 2x3x2 Blöcke (voxel [0, -1, -1] .. [1, 1, 0]), Masse 10, Preis 100, Tags: weapon,autocannon,belt
- Werte: cable_length=-431602080, weapon_ammo_capacity=100, weapon_type=5

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Ammo Count | Zahl | Ausgang | (0, -1, 0) | Outputs the total ammo count stored in the drum. |

## Autocannon Belt (Connector) (`gun_belt_receiver`)

*An autocannon ammo belt.*
Autocannon belts can transfer all calibers of autocannon ammo. Connector belts allow ammo transfers between vehicles.

- Größe 1x1x3 Blöcke (voxel [0, 0, -1] .. [0, 0, 1]), Masse 3, Preis 100, Tags: weapon,autocannon,belt
- Werte: cable_length=-431602080, weapon_ammo_capacity=1, weapon_belt_type=2

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Contains Ammo | An/Aus | Ausgang | (0, 0, 1) | Returns true if the belt contains a shell. |
| Connected | An/Aus | Ausgang | (0, 0, 0) |  |

## Autocannon Belt (Corner Flat) (`gun_belt_corner_flat`)

*An autocannon ammo belt.*
Autocannon belts can transfer all calibers of autocannon ammo.

- Größe 1x3x3 Blöcke (voxel [0, -1, -1] .. [0, 1, 1]), Masse 9, Preis 100, Tags: weapon,autocannon,belt
- Werte: cable_length=-431602080, weapon_ammo_capacity=1

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Contains Ammo | An/Aus | Ausgang | (0, 0, 0) | Returns true if the belt contains a shell. |

## Autocannon Belt (Corner) (`gun_belt_corner`)

*An autocannon ammo belt.*
Autocannon belts can transfer all calibers of autocannon ammo.

- Größe 1x1x3 Blöcke (voxel [0, 0, -1] .. [0, 0, 1]), Masse 3, Preis 100, Tags: weapon,autocannon,belt
- Werte: cable_length=-431602080, weapon_ammo_capacity=1

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Contains Ammo | An/Aus | Ausgang | (0, 0, 0) | Returns true if the belt contains a shell. |

## Autocannon Belt (Feeder) (`gun_belt_loader`)

*An autocannon ammo belt.*
Autocannon belts can transfer all calibers of autocannon ammo. Feeder belts transfer ammo forwards using electric power.

- Größe 1x1x4 Blöcke (voxel [0, 0, -2] .. [0, 0, 1]), Masse 4, Preis 100, Tags: weapon,autocannon,belt
- Werte: cable_length=-431602080, weapon_ammo_capacity=1, weapon_belt_type=1

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Feed | An/Aus | Eingang | (0, 0, -2) | Transfer cartridges in the direction of the arrow. |
| Contains Ammo | An/Aus | Ausgang | (0, 0, 0) | Returns true if the belt contains a shell. |
| Electric | Strom | Eingang | (0, 0, -2) | Electrical power connection. |

## Autocannon Belt (Flexible) (`gun_belt_flex`)

*An autocannon ammo belt.*
Flexible belts can be connected together by rope nodes to transfer ammo. Autocannon belts can transfer all calibers of autocannon ammo.

- Größe 1x2x3 Blöcke (voxel [0, 0, -1] .. [0, 1, 1]), Masse 3, Preis 100, Tags: weapon,autocannon,belt
- Werte: cable_length=-431602080, logic_gate_subtype=11, weapon_ammo_capacity=1, weapon_belt_type=4

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Ammo | Seil/Munition | Eingang | (0, 1, 0) |  |

## Autocannon Belt (Junction) (`gun_belt_junction`)

*An autocannon ammo belt.*
Autocannon belts can transfer all calibers of autocannon ammo. Junction belts redirect the path of ammo transfer.

- Größe 1x1x3 Blöcke (voxel [0, 0, -1] .. [0, 0, 1]), Masse 3, Preis 100, Tags: weapon,autocannon,belt
- Werte: cable_length=-431602080, weapon_ammo_capacity=1, weapon_belt_type=3

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Contains Ammo | An/Aus | Ausgang | (0, 0, 1) | Returns true if the belt contains a shell. |
| Junction Switch | An/Aus | Eingang | (0, 0, 0) | Switches the ammo transfer T-junction between the left and right sides. |

## Autocannon Belt (Straight) (`gun_belt_straight`)

*An autocannon ammo belt.*
Autocannon belts can transfer all calibers of autocannon ammo.

- Größe 1x1x3 Blöcke (voxel [0, 0, -1] .. [0, 0, 1]), Masse 3, Preis 100, Tags: weapon,autocannon,belt
- Werte: cable_length=-431602080, weapon_ammo_capacity=1

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Contains Ammo | An/Aus | Ausgang | (0, 0, 0) | Returns true if the belt contains a shell. |

## Battle Cannon (`gun_l`)

*A battle cannon.*
Battle cannons provide powerful, consistent firepower in a compact form.

- Größe 3x12x2 Blöcke (voxel [-1, -4, 0] .. [1, 7, 1]), Masse 100, Preis 100, Tags: weapon,cannon,battle
- Werte: cable_length=-431602080, weapon_barrel_length_voxels=7, weapon_class=4, weapon_type=2

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Trigger | An/Aus | Eingang | (0, 1, 0) | When true: fires a loaded shell. |
| Loaded | An/Aus | Ausgang | (0, 0, 0) | Returns true when a shell is loaded and ready to fire. |
| Open Breech | An/Aus | Eingang | (0, -1, 0) | When true: opens the breech to allow shells to be loaded. |
| Fuse Timer | Zahl | Eingang | (0, -2, 0) | Sets the optional time-delay fuse in seconds for high-explosive and fragmentation ammo types. |

## Battle Cannon Barrel Extension (`gun_l_barrel`)

*A battle cannon barrel extension.*
Barrel extensions increase weapon accuracy, but also produce more recoil force.

- Größe 1x3x1 Blöcke (voxel [0, -1, 0] .. [0, 1, 0]), Masse 40, Preis 50, Tags: weapon,cannon,battle
- Werte: cable_length=-431602080, weapon_barrel_length_voxels=3, weapon_class=4, weapon_type=4

## Battle Cannon Barrel Extension (`gun_l_barrel_1`)

*A battle cannon barrel extension.*
Barrel extensions increase weapon accuracy, but also produce more recoil force.

- Größe 3x3x3 Blöcke (voxel [-1, -1, -1] .. [1, 1, 1]), Masse 40, Preis 50, Tags: weapon,cannon,battle
- Werte: cable_length=-431602080, weapon_barrel_length_voxels=3, weapon_class=4, weapon_type=4

## Battle Cannon Barrel Extension (`gun_l_barrel_2`)

*A battle cannon barrel extension.*
Barrel extensions increase weapon accuracy, but also produce more recoil force.

- Größe 1x3x2 Blöcke (voxel [0, -1, -1] .. [0, 1, 0]), Masse 40, Preis 50, Tags: weapon,cannon,battle
- Werte: cable_length=-431602080, weapon_barrel_length_voxels=3, weapon_class=4, weapon_type=4

## Battle Cannon Barrel Extension (`gun_l_barrel_3`)

*A battle cannon barrel extension.*
Barrel extensions increase weapon accuracy, but also produce more recoil force.

- Größe 3x3x3 Blöcke (voxel [-1, -1, -1] .. [1, 1, 1]), Masse 40, Preis 50, Tags: weapon,cannon,battle
- Werte: cable_length=-431602080, weapon_barrel_length_voxels=3, weapon_class=4, weapon_type=4

## Battle Cannon Belt (Connector) (`gun_belt_receiver_l`)

*A battle cannon ammo belt.*
Cannon ammo belts can store and transfer ammo shells. Connector belts allow ammo transfers between vehicles. Spawned ammo type can be set in component properties window.

- Größe 1x1x3 Blöcke (voxel [0, 0, -1] .. [0, 0, 1]), Masse 3, Preis 100, Tags: weapon,cannon,belt,battle
- Werte: cable_length=-431602080, weapon_ammo_capacity=1, weapon_belt_type=2, weapon_class=4

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Contains Ammo | An/Aus | Ausgang | (0, 0, 1) | Returns true if the belt contains a shell. |
| Connected | An/Aus | Ausgang | (0, 0, 0) | Returns true when two nearby receivers are aligned, and can transfer ammo between them. |

## Battle Cannon Belt (Corner Inner) (`gun_belt_corner_flat_l`)

*A battle cannon ammo belt.*
Cannon ammo belts can store and transfer ammo shells. Spawned ammo type can be set in component properties window.

- Größe 1x3x3 Blöcke (voxel [0, -1, -1] .. [0, 1, 1]), Masse 9, Preis 100, Tags: weapon,cannon,belt,battle
- Werte: cable_length=-431602080, weapon_ammo_capacity=1, weapon_class=4

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Contains Ammo | An/Aus | Ausgang | (0, 0, 0) | Returns true if the belt contains a shell. |

## Battle Cannon Belt (Corner Outer) (`gun_belt_corner_flat_reverse_l`)

*A battle cannon ammo belt.*
Cannon ammo belts can store and transfer ammo shells. Spawned ammo type can be set in component properties window.

- Größe 1x3x3 Blöcke (voxel [0, -1, -1] .. [0, 1, 1]), Masse 9, Preis 100, Tags: weapon,cannon,belt,battle
- Werte: cable_length=-431602080, weapon_ammo_capacity=1, weapon_class=4

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Contains Ammo | An/Aus | Ausgang | (0, 0, 0) | Returns true if the belt contains a shell. |

## Battle Cannon Belt (Corner) (`gun_belt_corner_l`)

*A battle cannon ammo belt.*
Cannon ammo belts can store and transfer ammo shells. Spawned ammo type can be set in component properties window.

- Größe 1x1x3 Blöcke (voxel [0, 0, -1] .. [0, 0, 1]), Masse 3, Preis 100, Tags: weapon,cannon,belt,battle
- Werte: cable_length=-431602080, weapon_ammo_capacity=1, weapon_class=4

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Contains Ammo | An/Aus | Ausgang | (0, 0, 0) | Returns true if the belt contains a shell. |

## Battle Cannon Belt (Feeder) (`gun_belt_loader_l`)

*A battle cannon ammo belt.*
Cannon ammo belts can store and transfer ammo shells. Feeder belts transfer ammo forwards using electric power. Spawned ammo type can be set in component properties window.

- Größe 1x1x4 Blöcke (voxel [0, 0, -2] .. [0, 0, 1]), Masse 4, Preis 100, Tags: weapon,cannon,belt,battle
- Werte: cable_length=-431602080, weapon_ammo_capacity=1, weapon_belt_type=1, weapon_class=4

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Feed | An/Aus | Eingang | (0, 0, -2) | Transfer shells in the direction of the arrow. |
| Contains Ammo | An/Aus | Ausgang | (0, 0, 0) | Returns true if the belt contains a shell. |
| Electric | Strom | Eingang | (0, 0, -2) | Electrical power connection. |

## Battle Cannon Belt (Flexible) (`gun_belt_flex_l`)

*A battle cannon ammo belt.*
Flexible belts can be connected together by rope nodes to transfer ammo. Cannon ammo belts can store and transfer ammo shells. Spawned ammo type can be set in component properties window.

- Größe 1x2x3 Blöcke (voxel [0, 0, -1] .. [0, 1, 1]), Masse 3, Preis 100, Tags: weapon,cannon,belt,battle
- Werte: cable_length=-431602080, logic_gate_subtype=11, weapon_ammo_capacity=1, weapon_belt_type=4, weapon_class=4

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Ammo | Seil/Munition | Eingang | (0, 1, 0) |  |

## Battle Cannon Belt (Junction) (`gun_belt_junction_l`)

*A battle cannon ammo belt.*
Cannon ammo belts can store and transfer ammo shells. Junction belts redirect the path of ammo transfer. Spawned ammo type can be set in component properties window.

- Größe 1x1x3 Blöcke (voxel [0, 0, -1] .. [0, 0, 1]), Masse 3, Preis 100, Tags: weapon,cannon,belt,battle
- Werte: cable_length=-431602080, weapon_ammo_capacity=1, weapon_belt_type=3, weapon_class=4

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Contains Ammo | An/Aus | Ausgang | (0, 0, 1) | Returns true if the belt contains a shell. |
| Junction Switch | An/Aus | Eingang | (0, 0, 0) | Switches the ammo transfer T-junction between the left and right sides. |

## Battle Cannon Belt (Straight) (`gun_belt_straight_l`)

*A battle cannon ammo belt.*
Cannon ammo belts can store and transfer ammo shells. Spawned ammo type can be set in component properties window.

- Größe 1x1x3 Blöcke (voxel [0, 0, -1] .. [0, 0, 1]), Masse 3, Preis 100, Tags: weapon,cannon,belt,battle
- Werte: cable_length=-431602080, weapon_ammo_capacity=1, weapon_class=4

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Contains Ammo | An/Aus | Ausgang | (0, 0, 0) | Returns true if the belt contains a shell. |

## Battle Cannon Muzzle Brake (`gun_l_muzzle`)

*A battle cannon muzzle brake.*
A muzzle brake will reduce weapon recoil force when added to the end of a weapon barrel.

- Größe 1x4x1 Blöcke (voxel [0, -1, 0] .. [0, 2, 0]), Masse 40, Preis 50, Tags: weapon,cannon,battle
- Werte: cable_length=-431602080, weapon_barrel_length_voxels=3, weapon_class=4, weapon_type=7

## Battle Cannon Muzzle Brake (`gun_l_muzzle_1`)

*A battle cannon muzzle brake.*
A muzzle brake will reduce weapon recoil force when added to the end of a weapon barrel.

- Größe 3x4x1 Blöcke (voxel [-1, -1, 0] .. [1, 2, 0]), Masse 40, Preis 50, Tags: weapon,cannon,battle
- Werte: cable_length=-431602080, weapon_barrel_length_voxels=3, weapon_class=4, weapon_type=7

## Battle Cannon Muzzle Brake (`gun_l_muzzle_2`)

*A battle cannon muzzle brake.*
A muzzle brake will reduce weapon recoil force when added to the end of a weapon barrel.

- Größe 3x4x3 Blöcke (voxel [-1, -1, -1] .. [1, 2, 1]), Masse 40, Preis 50, Tags: weapon,cannon,battle
- Werte: cable_length=-431602080, weapon_barrel_length_voxels=3, weapon_class=4, weapon_type=7

## Bertha Cannon (`gun_xxl`)

*A Bertha cannon.*
The Bertha cannon fires devastating high explosive mortar shells, with a wide radius of destruction.

- Größe 5x30x5 Blöcke (voxel [-2, -9, -2] .. [2, 20, 2]), Masse 500, Preis 100, Tags: weapon,cannon,bertha
- Werte: cable_length=-431602080, weapon_barrel_length_voxels=20, weapon_class=6, weapon_type=2

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Trigger | An/Aus | Eingang | (0, 0, 0) | When true: fires a loaded shell. |
| Loaded | An/Aus | Ausgang | (0, 1, 0) | Returns true when a shell is loaded and ready to fire. |
| Open Breech | An/Aus | Eingang | (2, -3, 0) | When true: opens the breech to allow shells to be loaded. |
| Fuse Timer | Zahl | Eingang | (0, -3, -1) | Sets the optional time-delay fuse in seconds for high-explosive and fragmentation ammo types. |

## Bertha Cannon Barrel Extension (`gun_xxl_barrel`)

*A Bertha cannon barrel extension.*
Barrel extensions increase weapon accuracy, but also produce more recoil force.

- Größe 3x4x3 Blöcke (voxel [-1, -1, -1] .. [1, 2, 1]), Masse 200, Preis 50, Tags: weapon,cannon,bertha
- Werte: cable_length=-431602080, weapon_barrel_length_voxels=4, weapon_class=6, weapon_type=4

## Bertha Cannon Belt (Connector) (`gun_belt_receiver_xxl`)

*A bertha cannon ammo belt.*
Cannon ammo belts can store and transfer ammo shells. Connector belts allow ammo transfers between vehicles. Spawned ammo type can be set in component properties window. Bertha shells are too large to be moved by hand.

- Größe 3x3x7 Blöcke (voxel [-1, -1, -3] .. [1, 1, 3]), Masse 63, Preis 100, Tags: weapon,cannon,belt,bertha
- Werte: cable_length=-431602080, weapon_ammo_capacity=1, weapon_belt_type=2, weapon_class=6

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Contains Ammo | An/Aus | Ausgang | (0, 0, 1) | Returns true if the belt contains a shell. |
| Connected | An/Aus | Ausgang | (0, 0, 0) | Returns true when two nearby receivers are aligned, and can transfer ammo between them. |

## Bertha Cannon Belt (Corner Inner) (`gun_belt_corner_flat_xxl`)

*A bertha cannon ammo belt.*
Cannon ammo belts can store and transfer ammo shells. Spawned ammo type can be set in component properties window. Bertha shells are too large to be moved by hand.

- Größe 3x7x7 Blöcke (voxel [-1, -3, -3] .. [1, 3, 3]), Masse 138, Preis 100, Tags: weapon,cannon,belt,bertha
- Werte: cable_length=-431602080, weapon_ammo_capacity=1, weapon_class=6

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Contains Ammo | An/Aus | Ausgang | (0, 0, 0) | Returns true if the belt contains a shell. |

## Bertha Cannon Belt (Corner Outer) (`gun_belt_corner_flat_reverse_xxl`)

*A bertha cannon ammo belt.*
Cannon ammo belts can store and transfer ammo shells. Spawned ammo type can be set in component properties window. Bertha shells are too large to be moved by hand.

- Größe 3x7x7 Blöcke (voxel [-1, -3, -3] .. [1, 3, 3]), Masse 138, Preis 100, Tags: weapon,cannon,belt,bertha
- Werte: cable_length=-431602080, weapon_ammo_capacity=1, weapon_class=6

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Contains Ammo | An/Aus | Ausgang | (0, 0, 0) | Returns true if the belt contains a shell. |

## Bertha Cannon Belt (Corner) (`gun_belt_corner_xxl`)

*A bertha cannon ammo belt.*
Cannon ammo belts can store and transfer ammo shells. Spawned ammo type can be set in component properties window. Bertha shells are too large to be moved by hand.

- Größe 3x3x7 Blöcke (voxel [-1, -1, -3] .. [1, 1, 3]), Masse 63, Preis 100, Tags: weapon,cannon,belt,bertha
- Werte: cable_length=-431602080, weapon_ammo_capacity=1, weapon_class=6

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Contains Ammo | An/Aus | Ausgang | (0, 0, 0) | Returns true if the belt contains a shell. |

## Bertha Cannon Belt (Feeder) (`gun_belt_loader_xxl`)

*A bertha cannon ammo belt.*
Cannon ammo belts can store and transfer ammo shells. Feedeer belts transfer ammo forwards using electric power. Spawned ammo type can be set in component properties window. Bertha shells are too large to be moved by hand.

- Größe 3x3x10 Blöcke (voxel [-1, -1, -6] .. [1, 1, 3]), Masse 90, Preis 100, Tags: weapon,cannon,belt,bertha
- Werte: cable_length=-431602080, weapon_ammo_capacity=1, weapon_belt_type=1, weapon_class=6

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Feed | An/Aus | Eingang | (0, 0, -5) | Transfer shells in the direction of the arrow. |
| Contains Ammo | An/Aus | Ausgang | (0, 0, 0) | Returns true if the belt contains a shell. |
| Electric | Strom | Eingang | (0, 0, -5) | Electrical power connection. |

## Bertha Cannon Belt (Flexible) (`gun_belt_flex_xxl`)

*A bertha cannon ammo belt.*
Flexible belts can be connected together by rope nodes to transfer ammo. Cannon ammo belts can store and transfer ammo shells. Spawned ammo type can be set in component properties window. Bertha shells are too large to be moved by hand.

- Größe 3x4x7 Blöcke (voxel [-1, -1, -3] .. [1, 2, 3]), Masse 63, Preis 100, Tags: weapon,cannon,belt,bertha
- Werte: cable_length=-431602080, logic_gate_subtype=11, weapon_ammo_capacity=1, weapon_belt_type=4, weapon_class=6

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Ammo | Seil/Munition | Eingang | (0, 2, 0) |  |

## Bertha Cannon Belt (Junction) (`gun_belt_junction_xxl`)

*A bertha cannon ammo belt.*
Cannon ammo belts can store and transfer ammo shells. Junction belts redirect the path of ammo transfer. Spawned ammo type can be set in component properties window. Bertha shells are too large to be moved by hand.

- Größe 3x3x7 Blöcke (voxel [-1, -1, -3] .. [1, 1, 3]), Masse 63, Preis 100, Tags: weapon,cannon,belt,bertha
- Werte: cable_length=-431602080, weapon_ammo_capacity=1, weapon_belt_type=3, weapon_class=6

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Contains Ammo | An/Aus | Ausgang | (0, 0, 1) | Returns true if the belt contains a shell. |
| Junction Switch | An/Aus | Eingang | (0, 0, 0) | Switches the ammo transfer T-junction between the left and right sides. |

## Bertha Cannon Belt (Straight) (`gun_belt_straight_xxl`)

*A bertha cannon ammo belt.*
Cannon ammo belts can store and transfer ammo shells. Spawned ammo type can be set in component properties window. Bertha shells are too large to be moved by hand.

- Größe 3x3x7 Blöcke (voxel [-1, -1, -3] .. [1, 1, 3]), Masse 63, Preis 100, Tags: weapon,cannon,belt,bertha
- Werte: cable_length=-431602080, weapon_ammo_capacity=1, weapon_class=6

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Contains Ammo | An/Aus | Ausgang | (0, 0, 0) | Returns true if the belt contains a shell. |

## Heavy Autocannon (`gun_m`)

*A heavy autocannon.*
Heavy autocannons bridge the gap between fast-firing autocannons and high-caliber cannons. Autocannons require electric power to load ammo from connected belts or drums.

- Größe 1x10x1 Blöcke (voxel [0, -2, 0] .. [0, 7, 0]), Masse 50, Preis 100, Tags: weapon,autocannon
- Werte: cable_length=-431602080, weapon_ammo_feed=true, weapon_barrel_length_voxels=7, weapon_class=3, weapon_type=2

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Trigger | An/Aus | Eingang | (0, 1, 0) | When true: feeds, loads, and fires cartridges from a connected belt or drum. |
| Loaded | An/Aus | Ausgang | (0, 0, 0) | Returns true when a cartridge is loaded and ready to fire. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |
| Fuse Timer | Zahl | Eingang | (0, -1, 0) | Sets the optional time-delay fuse in seconds for high-explosive and fragmentation ammo types. |

## Heavy Autocannon Barrel Extension (`gun_m_barrel`)

*A heavy autocannon barrel extension.*
Barrel extensions increase weapon accuracy, but add additional weight.

- Größe 1x3x1 Blöcke (voxel [0, -1, 0] .. [0, 1, 0]), Masse 20, Preis 50, Tags: weapon,autocannon
- Werte: cable_length=-431602080, weapon_barrel_length_voxels=3, weapon_class=3, weapon_type=4

## Heavy Autocannon Barrel Extension (`gun_m_barrel_1`)

*A heavy autocannon barrel extension.*
Barrel extensions increase weapon accuracy, but also produce more recoil force.

- Größe 1x3x1 Blöcke (voxel [0, -1, 0] .. [0, 1, 0]), Masse 20, Preis 50, Tags: weapon,autocannon
- Werte: cable_length=-431602080, weapon_barrel_length_voxels=3, weapon_class=3, weapon_type=4

## Heavy Autocannon Barrel Extension (`gun_m_barrel_2`)

*A heavy autocannon barrel extension.*
Barrel extensions increase weapon accuracy, but also produce more recoil force.

- Größe 1x3x2 Blöcke (voxel [0, -1, -1] .. [0, 1, 0]), Masse 20, Preis 50, Tags: weapon,autocannon
- Werte: cable_length=-431602080, weapon_barrel_length_voxels=3, weapon_class=3, weapon_type=4

## Heavy Autocannon Barrel Extension (`gun_m_barrel_3`)

*A heavy autocannon barrel extension.*
Barrel extensions increase weapon accuracy, but also produce more recoil force.

- Größe 1x3x2 Blöcke (voxel [0, -1, -1] .. [0, 1, 0]), Masse 20, Preis 50, Tags: weapon,autocannon
- Werte: cable_length=-431602080, weapon_barrel_length_voxels=3, weapon_class=3, weapon_type=4

## Heavy Autocannon Muzzle Brake (`gun_m_muzzle`)

*A heavy autocannon muzzle brake.*
A muzzle brake will reduce weapon recoil force when added to the end of a weapon barrel.

- Größe 1x4x1 Blöcke (voxel [0, -1, 0] .. [0, 2, 0]), Masse 20, Preis 50, Tags: weapon,autocannon
- Werte: cable_length=-431602080, weapon_barrel_length_voxels=3, weapon_class=3, weapon_type=7

## Heavy Autocannon Muzzle Brake (`gun_m_muzzle_1`)

*A heavy autocannon muzzle brake.*
A muzzle brake will reduce weapon recoil force when added to the end of a weapon barrel.

- Größe 1x4x1 Blöcke (voxel [0, -1, 0] .. [0, 2, 0]), Masse 20, Preis 50, Tags: weapon,autocannon
- Werte: cable_length=-431602080, weapon_barrel_length_voxels=3, weapon_class=3, weapon_type=7

## Heavy Autocannon Muzzle Brake (`gun_m_muzzle_2`)

*A heavy autocannon muzzle brake.*
A muzzle brake will reduce weapon recoil force when added to the end of a weapon barrel.

- Größe 1x4x1 Blöcke (voxel [0, -1, 0] .. [0, 2, 0]), Masse 20, Preis 50, Tags: weapon,autocannon
- Werte: cable_length=-431602080, weapon_barrel_length_voxels=3, weapon_class=3, weapon_type=7

## Light Autocannon (`gun_s`)

*A light autocannon.*
Light autocannons provide rapid fire and high ammo capacity. Autocannons require electric power to load ammo from connected belts or drums.

- Größe 2x6x1 Blöcke (voxel [0, 0, 0] .. [1, 5, 0]), Masse 25, Preis 100, Tags: weapon,autocannon
- Werte: cable_length=-431602080, weapon_ammo_feed=true, weapon_barrel_length_voxels=5, weapon_type=2

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Trigger | An/Aus | Eingang | (0, 1, 0) | When true: feeds, loads, and fires cartridges from a connected belt or drum. |
| Loaded | An/Aus | Ausgang | (0, 0, 0) | Returns true when a cartridge is loaded and ready to fire. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Light Autocannon Barrel Extension (`gun_s_barrel`)

*A light autocannon barrel extension.*
Barrel extensions increase weapon accuracy, but also produce more recoil force.

- Größe 1x3x1 Blöcke (voxel [0, -1, 0] .. [0, 1, 0]), Masse 10, Preis 50, Tags: weapon,autocannon
- Werte: cable_length=-431602080, weapon_barrel_length_voxels=3, weapon_type=4

## Light Autocannon Muzzle Brake (`gun_s_muzzle`)

*A light autocannon muzzle brake.*
A muzzle brake will reduce weapon recoil force when added to the end of a weapon barrel.

- Größe 1x2x1 Blöcke (voxel [0, 0, 0] .. [0, 1, 0]), Masse 3, Preis 50, Tags: weapon,autocannon
- Werte: cable_length=-431602080, weapon_barrel_length_voxels=1, weapon_type=7

## Light Autocannon Muzzle Brake (`gun_s_muzzle_1`)

*A light autocannon muzzle brake.*
A muzzle brake will reduce weapon recoil force when added to the end of a weapon barrel.

- Größe 1x2x1 Blöcke (voxel [0, 0, 0] .. [0, 1, 0]), Masse 3, Preis 50, Tags: weapon,autocannon
- Werte: cable_length=-431602080, weapon_barrel_length_voxels=1, weapon_type=7

## Light Autocannon Muzzle Brake (`gun_s_muzzle_2`)

*A light autocannon muzzle brake.*
A muzzle brake will reduce weapon recoil force when added to the end of a weapon barrel.

- Größe 1x2x1 Blöcke (voxel [0, 0, 0] .. [0, 1, 0]), Masse 3, Preis 50, Tags: weapon,autocannon
- Werte: cable_length=-431602080, weapon_barrel_length_voxels=1, weapon_type=7

## Light Autocannon Muzzle Brake (`gun_s_muzzle_3`)

*A light autocannon muzzle brake.*
A muzzle brake will reduce weapon recoil force when added to the end of a weapon barrel.

- Größe 1x2x1 Blöcke (voxel [0, 0, 0] .. [0, 1, 0]), Masse 3, Preis 50, Tags: weapon,autocannon
- Werte: cable_length=-431602080, weapon_barrel_length_voxels=1, weapon_type=7

## Machine Gun (`gun_xs`)

*A machine gun.*
Machine guns are lightweight and compact, but require ammo boxes to be reloaded by hand.

- Größe 1x4x1 Blöcke (voxel [0, -1, 0] .. [0, 2, 0]), Masse 10, Preis 50, Tags: weapon,machinegun
- Werte: cable_length=-431602080, weapon_ammo_feed=true, weapon_barrel_length_voxels=2, weapon_class=0, weapon_type=2

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Trigger | An/Aus | Eingang | (0, 0, 0) | When true: feeds, loads, and fires cartridges from a connected ammo box. |
| Loaded | An/Aus | Ausgang | (0, -1, 0) | Returns true when a cartridge is loaded and ready to fire. |

## Machine Gun Ammo Box (`gun_drum_xsmall`)

*A machine gun ammo box.*
Stores machine gun ammo, but can only be reloaded by hand. Machine guns are restricted to Kinetic, Armor-Piercing, and Incendiary ammo only.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 5, Preis 20, Tags: weapon,machinegun,belt
- Werte: cable_length=-431602080, weapon_ammo_capacity=100, weapon_class=0, weapon_type=5

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Ammo count | Zahl | Ausgang | (0, 0, 0) | Outputs the total ammo count stored in the box. |

## Machine Gun Ammo Box (Large) (`gun_drum_xsmall_2`)

*A machine gun ammo box with greater capacity.*
Stores machine gun ammo, but can only be reloaded by hand. Machine guns are restricted to Kinetic, Armor-Piercing, and Incendiary ammo only.

- Größe 1x2x2 Blöcke (voxel [0, 0, 0] .. [0, 1, 1]), Masse 20, Preis 30, Tags: weapon,machinegun,belt
- Werte: cable_length=-431602080, weapon_ammo_capacity=400, weapon_class=0, weapon_type=5

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Ammo count | Zahl | Ausgang | (0, 0, 0) | Outputs the total ammo count stored in the box. |

## Rocket Launcher (`gun_rocket_launcher`)

*A 4-shot rocket launcher.*
Rocket launchers fire powerful high explosive rockets, but cannot be reloaded once empty. Rockets are vulnerable to bullets while in flight.

- Größe 1x8x1 Blöcke (voxel [0, -3, 0] .. [0, 4, 0]), Masse 50, Preis 100, Tags: weapon,explosive
- Werte: cable_length=-431602080, weapon_ammo_capacity=4, weapon_barrel_length_voxels=3, weapon_class=3, weapon_type=6

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Trigger | An/Aus | Eingang | (0, 0, 0) | When true: fires a loaded rocket. |
| Loaded | An/Aus | Ausgang | (0, 1, 0) | Returns true when a rocket is loaded and ready to fire. |
| Trigger Passthrough | An/Aus | Ausgang | (0, -1, 0) | Outputs the trigger value once all rockets have been expended. |

## Rotary Autocannon (`gun_v`)

*A rotary autocannon.*
Rotary autocannons have a tremendous rate of fire, but can overheat quickly. Autocannons require electric power to load ammo from connected belts or drums.

- Größe 4x13x2 Blöcke (voxel [-1, -2, -1] .. [2, 10, 0]), Masse 400, Preis 100, Tags: weapon,autocannon
- Werte: cable_length=-431602080, weapon_ammo_feed=true, weapon_barrel_length_voxels=10, weapon_class=2, weapon_type=2

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Trigger | An/Aus | Eingang | (0, 1, 0) | When true: feeds, loads, and fires cartridges from a connected belt or drum. |
| Loaded | An/Aus | Ausgang | (0, 0, 0) | Returns true when a cartridge is loaded and ready to fire. |
| Electric | Strom | Eingang | (0, 0, 0) | Electrical power connection. |

## Rotary Autocannon Barrel Extension (`gun_v_barrel`)

*A rotary autocannon barrel extension.*
Barrel extensions increase weapon accuracy, but add additional weight.

- Größe 1x4x1 Blöcke (voxel [0, -1, 0] .. [0, 2, 0]), Masse 40, Preis 50, Tags: weapon,autocannon
- Werte: cable_length=-431602080, weapon_barrel_length_voxels=4, weapon_class=2, weapon_type=4

## Warhead (EMP) (`warhead_emp`)

*A electromagnetic-pulse warhead.*
Detonates from an impact, creating an EMP to temporarily shut down nearby electronic systems.

- Größe 5x13x5 Blöcke (voxel [-2, -6, -2] .. [2, 6, 2]), Masse 500, Preis 200, Tags: weapons,explosive
- Werte: cable_length=-431602080, weapon_barrel_length_voxels=8, weapon_type=0

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Arm | An/Aus | Eingang | (0, 0, 0) | Arm the EMP charge in the warhead to detonate when the internal impact sensor reaches its threshold. |

## Warhead (Large) (`warhead_large`)

*A large explosive warhead.*
Detonates from an impact, or when receiving damage. Be careful!

- Größe 5x9x5 Blöcke (voxel [-2, -4, -2] .. [2, 4, 2]), Masse 400, Preis 100, Tags: weapons,explosive
- Werte: cable_length=-431602080, weapon_class=4, weapon_type=1

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Arm | An/Aus | Eingang | (0, 0, 0) | Arm the explosives in the warhead to detonate when the internal impact sensor reaches its threshold. |

## Warhead (Medium) (`warhead_medium`)

*A medium explosive warhead.*
Detonates from an impact, or when receiving damage. Be careful!

- Größe 3x5x3 Blöcke (voxel [-1, -2, -1] .. [1, 2, 1]), Masse 80, Preis 50, Tags: weapons,explosive
- Werte: cable_length=-431602080, weapon_class=3, weapon_type=1

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Arm | An/Aus | Eingang | (0, 0, 0) | Arm the explosives in the warhead to detonate when the internal impact sensor reaches its threshold. |

## Warhead (Small) (`warhead_small`)

*A small explosive warhead.*
Detonates from an impact, or when receiving damage. Be careful!

- Größe 1x2x1 Blöcke (voxel [0, 0, 0] .. [0, 1, 0]), Masse 15, Preis 25, Tags: weapons,explosive
- Werte: cable_length=-431602080, weapon_barrel_length_voxels=8, weapon_type=1

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Arm | An/Aus | Eingang | (0, 0, 0) | Arm the explosives in the warhead to detonate when the internal impact sensor reaches its threshold. |

## Warhead Body (Large) (`warhead_body_large`)

*A large explosive warhead.*
Detonates from an impact, or when receiving damage. Be careful!

- Größe 5x9x5 Blöcke (voxel [-2, -4, -2] .. [2, 4, 2]), Masse 400, Preis 100, Tags: weapons,explosive
- Werte: cable_length=-431602080, weapon_barrel_length_voxels=8, weapon_class=4, weapon_type=1

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Arm | An/Aus | Eingang | (0, 0, 0) | Arm the explosives in the warhead to detonate when the internal impact sensor reaches its threshold. |

## Warhead Body (Medium) (`warhead_body_medium`)

*A medium explosive warhead.*
Detonates from an impact, or when receiving damage. Be careful!

- Größe 3x5x3 Blöcke (voxel [-1, -2, -1] .. [1, 2, 1]), Masse 80, Preis 50, Tags: weapons,explosive
- Werte: cable_length=-431602080, weapon_barrel_length_voxels=8, weapon_class=3, weapon_type=1

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Arm | An/Aus | Eingang | (0, 0, 0) | Arm the explosives in the warhead to detonate when the internal impact sensor reaches its threshold. |

## Warhead Body (Small) (`warhead_body_small`)

*A small explosive warhead.*
Detonates from an impact, or when receiving damage. Be careful!

- Größe 1x2x1 Blöcke (voxel [0, 0, 0] .. [0, 1, 0]), Masse 15, Preis 25, Tags: weapons,explosive
- Werte: cable_length=-431602080, weapon_barrel_length_voxels=8, weapon_type=1

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Arm | An/Aus | Eingang | (0, 0, 0) | Arm the explosives in the warhead to detonate when the internal impact sensor reaches its threshold. |
