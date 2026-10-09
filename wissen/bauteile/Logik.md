# Logik (Kategorie 5)

Aus den Spieldaten erzeugt von `tools/bauteile_holen.py` - nicht von Hand ändern.

## Abs (`gate_float_abs`)

*Outputs the absolute value of a number input.*
Negative numbers are converted to positive numbers, whilst positive numbers are unchanged.

- Größe 1x1x2 Blöcke (voxel [0, 0, 0] .. [0, 0, 1]), Masse 1, Preis 20
- Werte: cable_radius=0, light_intensity=0, logic_gate_type=38, magnet_force=0, max_motor_speed=5, rudder_surface_area=0, type=16

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Absolute Value | Zahl | Ausgang | (0, 0, 0) | The absolute value of the input. |
| Input Number | Zahl | Eingang | (0, 0, 1) | The number to get the absolute value of. |

## Add (`gate_float_add`)

*Takes two number inputs, adds them together, and outputs the result.*

- Größe 2x1x2 Blöcke (voxel [0, 0, 0] .. [1, 0, 1]), Masse 1, Preis 20
- Werte: buoy_factor=1.000000, buoy_force=100.000000, buoy_radius=1.000000, constraint_range_of_motion=0.000000, door_lower_limit=-1.000000, door_upper_limit=1.000000, dynamic_min_rotation=0.000000, engine_max_force=1000.000000, force_emitter_max_force=1000.000000, force_emitter_max_vector=1.000000, light_fov=1.000000, light_intensity=0.000000, light_range=1.000000, logic_gate_type=6, magnet_force=0.000000, max_motor_force=100.000000, rudder_surface_area=0.000000, type=16, wheel_radius=0.250000

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| A | Zahl | Eingang | (1, 0, 1) | The first value to be added. |
| A + B | Zahl | Ausgang | (0, 0, 0) | Outputs the result of A + B. |
| B | Zahl | Eingang | (0, 0, 1) | The second value to be added. |

## And (`gate_bool_and`)

*A logic gate that outputs the logical AND of two input signals.*
The output will only be switched on if both inputs are on.

- Größe 2x1x2 Blöcke (voxel [0, 0, 0] .. [1, 0, 1]), Masse 1, Preis 20
- Werte: buoy_factor=1.000000, buoy_force=100.000000, buoy_radius=1.000000, constraint_range_of_motion=0.000000, door_lower_limit=-1.000000, door_upper_limit=1.000000, dynamic_min_rotation=0.000000, engine_max_force=1000.000000, force_emitter_max_force=1000.000000, force_emitter_max_vector=1.000000, light_fov=1.000000, light_intensity=0.000000, light_range=1.000000, magnet_force=0.000000, max_motor_force=100.000000, rudder_surface_area=0.000000, type=16, wheel_radius=0.250000

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| A | An/Aus | Eingang | (1, 0, 1) | The first value to perform the logical AND on. |
| B | An/Aus | Eingang | (0, 0, 1) | The second value to perform the logical AND on. |
| A AND B | An/Aus | Ausgang | (0, 0, 0) | Outputs an on signal when both A and B are on, and an off signal if either one is off. |

## Blinker (`gate_bool_blink`)

*The blinker outputs a value that blinks between on and off at a set rate.*
You can set the duration that the signal should stay on and off for by selecting it with the select tool. A control signal determines whether or not the blinker should output anything. If the control signal is off, the blinker's output will be off. The internal blink timer is reset every time the control signal is switched off.

- Größe 1x1x2 Blöcke (voxel [0, 0, 0] .. [0, 0, 1]), Masse 1, Preis 20
- Werte: buoy_factor=1.000000, buoy_force=100.000000, buoy_radius=1.000000, constraint_range_of_motion=0.000000, door_lower_limit=-1.000000, door_upper_limit=1.000000, dynamic_min_rotation=0.000000, engine_max_force=1000.000000, force_emitter_max_force=1000.000000, force_emitter_max_vector=1.000000, light_fov=1.000000, light_intensity=0.000000, light_range=1.000000, logic_gate_type=11, magnet_force=0.000000, max_motor_force=100.000000, rudder_surface_area=0.000000, type=16, wheel_radius=0.250000

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Control Signal | An/Aus | Eingang | (0, 0, 1) | Controls whether or not the blinker should output anything at all. |
| Blinking Signal | An/Aus | Ausgang | (0, 0, 0) | Outputs a signal that blinks between on and off at the set rate when the control signal is on. Outputs off if the control signal is off. |

## Capacitor (`gate_bool_capacitor`)

*Charges up when receiving an on signal, then discharges over a period of time.*
The charge and discharge times can be configured by selecting this component with the select tool. Once charged, inputting a new signal will reset the discharge timer.

- Größe 1x1x2 Blöcke (voxel [0, 0, 0] .. [0, 0, 1]), Masse 1, Preis 20
- Werte: cable_radius=0, light_intensity=0, logic_gate_type=36, magnet_force=0, max_motor_speed=5, rudder_surface_area=0, type=16

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Charge | An/Aus | Eingang | (0, 0, 1) | Charges the capacitor when on, discharges when off. |
| Stored Charge | An/Aus | Ausgang | (0, 0, 0) | The capacitor's stored charge. |

## Clamp (`gate_float_clamp`)

*The clamp takes a number input and clamps it to a set range.*
The upper and lower values to clamp to can be configured by selecting this component with the select tool.

- Größe 1x1x2 Blöcke (voxel [0, 0, 0] .. [0, 0, 1]), Masse 1, Preis 20
- Werte: buoy_factor=1.000000, buoy_force=100.000000, buoy_radius=1.000000, constraint_range_of_motion=0.000000, door_lower_limit=-1.000000, door_upper_limit=1.000000, dynamic_min_rotation=0.000000, engine_max_force=1000.000000, force_emitter_max_force=1000.000000, force_emitter_max_vector=1.000000, light_fov=1.000000, light_intensity=0.000000, light_range=1.000000, logic_gate_type=16, magnet_force=0.000000, max_motor_force=100.000000, rudder_surface_area=0.000000, type=16, wheel_radius=0.250000

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Clamped Number | Zahl | Ausgang | (0, 0, 0) | The input after being clamped within the upper and lower bounds. |
| Number to Clamp | Zahl | Eingang | (0, 0, 1) | The value to clamp within the upper and lower bounds. |

## Constant Number (`gate_float_constant`)

*Outputs a constant numerical value.*
The number that is being outputted can be configured by selecting this component with the select tool.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 20
- Werte: buoy_factor=1.000000, buoy_force=100.000000, buoy_radius=1.000000, constraint_range_of_motion=0.000000, door_lower_limit=-1.000000, door_upper_limit=1.000000, dynamic_min_rotation=0.000000, engine_max_force=1000.000000, force_emitter_max_force=1000.000000, force_emitter_max_vector=1.000000, light_fov=1.000000, light_intensity=0.000000, light_range=1.000000, logic_gate_type=14, magnet_force=0.000000, max_motor_force=100.000000, rudder_surface_area=0.000000, type=16, wheel_radius=0.250000

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Constant Number | Zahl | Ausgang | (0, 0, 0) | The selected output number. |

## Constant On Signal (`gate_bool_constant`)

*A simple logic component that continuously outputs an on signal.*
This is useful for creating logic circuits that are permanently switched on.

- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 20
- Werte: buoy_factor=1.000000, buoy_force=100.000000, buoy_radius=1.000000, constraint_range_of_motion=0.000000, door_lower_limit=-1.000000, door_upper_limit=1.000000, dynamic_min_rotation=0.000000, engine_max_force=1000.000000, force_emitter_max_force=1000.000000, force_emitter_max_vector=1.000000, light_fov=1.000000, light_intensity=0.000000, light_range=1.000000, logic_gate_type=17, magnet_force=0.000000, max_motor_force=100.000000, rudder_surface_area=0.000000, type=16, wheel_radius=0.250000

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| On | An/Aus | Ausgang | (0, 0, 0) | Outputs a constant on signal. |

## Counter (`gate_float_counter`)

*A counter which increases with a set speed.*
Stores and constantly outputs a value which increases by an input amount.

- Größe 1x1x2 Blöcke (voxel [0, 0, 0] .. [0, 0, 1]), Masse 1, Preis 20
- Werte: buoy_factor=1.000000, buoy_force=100.000000, buoy_radius=1.000000, constraint_range_of_motion=0.000000, door_lower_limit=-1.000000, door_upper_limit=1.000000, dynamic_min_rotation=0.000000, engine_max_force=1000.000000, force_emitter_max_force=1000.000000, force_emitter_max_vector=1.000000, light_fov=1.000000, light_intensity=0.000000, light_range=1.000000, logic_gate_type=27, magnet_force=0.000000, max_motor_force=100.000000, rudder_surface_area=0.000000, type=16, wheel_radius=0.250000

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Speed | Zahl | Eingang | (0, 0, 1) | The speed the count rises by. |
| Count | Zahl | Ausgang | (0, 0, 0) | The current count. |

## Counter (Ping Pong) (`gate_float_counter_ping_pong`)

*A counter which oscillates between -1 and +1 with a set speed.*

- Größe 1x1x2 Blöcke (voxel [0, 0, 0] .. [0, 0, 1]), Masse 1, Preis 20
- Werte: buoy_factor=1.000000, buoy_force=100.000000, buoy_radius=1.000000, constraint_range_of_motion=0.000000, door_lower_limit=-1.000000, door_upper_limit=1.000000, dynamic_min_rotation=0.000000, engine_max_force=1000.000000, force_emitter_max_force=1000.000000, force_emitter_max_vector=1.000000, light_fov=1.000000, light_intensity=0.000000, light_range=1.000000, logic_gate_type=28, magnet_force=0.000000, max_motor_force=100.000000, rudder_surface_area=0.000000, type=16, wheel_radius=0.250000

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Speed | Zahl | Eingang | (0, 0, 1) | The speed the count changes by. |
| Count | Zahl | Ausgang | (0, 0, 0) | The current count. |

## Delay (`gate_bool_delay`)

*This component stores an input on/off signal, and then outputs it after a delay.*
The delay time can be configured by selecting the component with the select tool. The internal delay timer is reset whenever the input signal changes.

- Größe 1x1x2 Blöcke (voxel [0, 0, 0] .. [0, 0, 1]), Masse 1, Preis 20
- Werte: buoy_factor=1.000000, buoy_force=100.000000, buoy_radius=1.000000, constraint_range_of_motion=0.000000, door_lower_limit=-1.000000, door_upper_limit=1.000000, dynamic_min_rotation=0.000000, engine_max_force=1000.000000, force_emitter_max_force=1000.000000, force_emitter_max_vector=1.000000, light_fov=1.000000, light_intensity=0.000000, light_range=1.000000, logic_gate_type=12, magnet_force=0.000000, max_motor_force=100.000000, rudder_surface_area=0.000000, type=16, wheel_radius=0.250000

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Signal to Delay | An/Aus | Eingang | (0, 0, 1) | Can be an on or off signal. Changing this will reset the delay's timer. |
| Delayed Signal | An/Aus | Ausgang | (0, 0, 0) | The input signal that has been delayed. |

## Divide (`gate_float_divide`)

*Takes two number inputs, divides one by the other, and outputs the result.*
If a division by 0 occurs, an on signal will be produced and the output number value will be set to 0.

- Größe 2x1x2 Blöcke (voxel [0, 0, 0] .. [1, 0, 1]), Masse 1, Preis 20
- Werte: cable_radius=0, light_intensity=0, logic_gate_type=37, magnet_force=0, max_motor_speed=5, rudder_surface_area=0, type=16

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| A | Zahl | Eingang | (1, 0, 1) | The number to divide. |
| B | Zahl | Eingang | (0, 0, 1) | The number to divide by. |
| Error | An/Aus | Ausgang | (1, 0, 0) | Outputs true when a division by 0 occurs. |
| A / B | Zahl | Ausgang | (0, 0, 0) | The result of A divided by B, or 0 attempting to divide by 0. |

## Exponent (`gate_float_exponent`)

*Outputs its input raised to the power of a selected exponent.*
The exponent can be changed by selecting this component with the select tool.

- Größe 1x1x2 Blöcke (voxel [0, 0, 0] .. [0, 0, 1]), Masse 1, Preis 20, Tags: square,cube,root,sqrt,pow
- Werte: cable_radius=0, light_intensity=0, logic_gate_type=44, magnet_force=0, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, type=16

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Powered Number | Zahl | Ausgang | (0, 0, 0) | The input raised to the power of the selected exponent. |
| Input Number | Zahl | Eingang | (0, 0, 1) | The number to exponentiate. |

## Function (1 input) (`gate_function_small`)

*Evaluates a mathematical function with 1 variable inputs*
The function can be entered by selecting this component with the select tool. A full list of valid operations are also visible in the component's selection menu.

- Größe 1x1x2 Blöcke (voxel [0, 0, 0] .. [0, 0, 1]), Masse 1, Preis 80
- Werte: cable_radius=0.02, light_intensity=0, logic_gate_type=45, magnet_force=0, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, type=16

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| f(x) | Zahl | Ausgang | (0, 0, 0) | Outputs the evaluation of the entered function. |
| Input 1 (x) | Zahl | Eingang | (0, 0, 1) | X input to the function. |

## Function (3 inputs) (`gate_function_large`)

*Evaluates a mathematical function with up to 3 variable inputs.*
The function can be entered by selecting this component with the select tool. A full list of valid operations are also visible in the component's selection menu.

- Größe 2x1x2 Blöcke (voxel [0, 0, 0] .. [1, 0, 1]), Masse 1, Preis 100
- Werte: cable_radius=0.02, light_intensity=0, logic_gate_type=45, magnet_force=0, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, type=16

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Input 1 (x) | Zahl | Eingang | (1, 0, 1) | X input to the function. |
| f(x,y,z) | Zahl | Ausgang | (0, 0, 0) | Outputs the evaluation of the entered function. |
| Input 2 (y) | Zahl | Eingang | (0, 0, 1) | Y input to the function. |
| Input 3 (z) | Zahl | Eingang | (1, 0, 0) | Z input to the function. |

## Greater-than (`gate_float_greater_than`)

*Compares two numerical values.*
Outputs an on signal if the first input is greater than the second, and outputs an off signal if the first input is less than or equal to the second.

- Größe 2x1x2 Blöcke (voxel [0, 0, 0] .. [1, 0, 1]), Masse 1, Preis 20
- Werte: cable_radius=0, light_intensity=0, logic_gate_type=33, magnet_force=0, max_motor_speed=5, rudder_surface_area=0, type=16

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| A | Zahl | Eingang | (1, 0, 1) | The value to compare. |
| B | Zahl | Eingang | (0, 0, 1) | The value to be compared to. |
| A GREATER THAN B | An/Aus | Ausgang | (0, 0, 0) | Outputs an on signal if A is greater than B. Outputs an off signal if A is less than or equal to B. |

## JK Flip-Flop (`gate_jk_flipflop`)

*A JK flip-flop that can be set and reset using two on/off inputs.*
When both inputs are off, there is no change in state. If both Set and Reset are set to on, the state will be toggled.

- Größe 2x1x2 Blöcke (voxel [0, 0, 0] .. [1, 0, 1]), Masse 1, Preis 20
- Werte: cable_radius=0, light_intensity=0, logic_gate_type=35, magnet_force=0, max_motor_speed=5, rudder_surface_area=0, type=16

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Set | An/Aus | Eingang | (1, 0, 1) | Sets the output to on. |
| Reset | An/Aus | Eingang | (0, 0, 1) | Sets the output to off. |
| Output | An/Aus | Ausgang | (1, 0, 0) | The internal state of the flip-flop. |
| NOT Output | An/Aus | Ausgang | (0, 0, 0) | The inverse of the internal state of the flip-flop. |

## Less-Than (`gate_float_less_than`)

*Compares two numerical values.*
Outputs an on signal if the first input is less than the second, and outputs an off signal if the first input is greater than or equal to the second.

- Größe 2x1x2 Blöcke (voxel [0, 0, 0] .. [1, 0, 1]), Masse 1, Preis 20
- Werte: buoy_factor=1.000000, buoy_force=100.000000, buoy_radius=1.000000, constraint_range_of_motion=0.000000, door_lower_limit=-1.000000, door_upper_limit=1.000000, dynamic_min_rotation=0.000000, engine_max_force=1000.000000, force_emitter_max_force=1000.000000, force_emitter_max_vector=1.000000, light_fov=1.000000, light_intensity=0.000000, light_range=1.000000, logic_gate_type=22, magnet_force=0.000000, max_motor_force=100.000000, rudder_surface_area=0.000000, type=16, wheel_radius=0.250000

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| A | Zahl | Eingang | (1, 0, 1) | The value to compare. |
| B | Zahl | Eingang | (0, 0, 1) | The value to be compared to. |
| A LESS THAN B | An/Aus | Ausgang | (0, 0, 0) | Outputs an on signal if A is less than B. Outputs an off signal if A is greater than or equal to B. |

## Memory Register (`gate_float_register`)

*A memory register that can store a number value.*
The number input will be stored when an on signal is received. A secondary on/off signal can be used to clear the stored value, resetting it to the configured value set using the select tool.

- Größe 2x1x2 Blöcke (voxel [0, 0, 0] .. [1, 0, 1]), Masse 1, Preis 20
- Werte: buoy_factor=1.000000, buoy_force=100.000000, buoy_radius=1.000000, constraint_range_of_motion=0.000000, door_lower_limit=-1.000000, door_upper_limit=1.000000, dynamic_min_rotation=0.000000, engine_max_force=1000.000000, force_emitter_max_force=1000.000000, force_emitter_max_vector=1.000000, light_fov=1.000000, light_intensity=0.000000, light_range=1.000000, logic_gate_type=32, magnet_force=0.000000, max_motor_force=100.000000, rudder_surface_area=0.000000, type=16, wheel_radius=0.250000

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Stored Value | Zahl | Ausgang | (0, 0, 1) | The value that is stored in the memory. |
| Value to Store | Zahl | Eingang | (1, 0, 1) | The value that will be stored when receiving an on signal. |
| Set | An/Aus | Eingang | (0, 0, 0) | Stores the input value when receiving an on signal. |
| Clear | An/Aus | Eingang | (1, 0, 0) | Resets the stored value to 0. |

## Microprocessor (`microprocessor`)


- Größe 1x1x1 Blöcke (voxel [0, 0, 0] .. [0, 0, 0]), Masse 1, Preis 100
- Werte: cable_length=-431602080, type=37

## Modulo (`gate_float_modulo`)

*Takes two number inputs, outputs the remainder after dividing the first by the second.*

- Größe 2x1x2 Blöcke (voxel [0, 0, 0] .. [1, 0, 1]), Masse 1, Preis 20
- Werte: buoy_factor=1.000000, buoy_force=100.000000, buoy_radius=1.000000, constraint_range_of_motion=0.000000, door_lower_limit=-1.000000, door_upper_limit=1.000000, dynamic_min_rotation=0.000000, engine_max_force=1000.000000, force_emitter_max_force=1000.000000, force_emitter_max_vector=1.000000, light_fov=1.000000, light_intensity=0.000000, light_range=1.000000, logic_gate_type=26, magnet_force=0.000000, max_motor_force=100.000000, rudder_surface_area=0.000000, type=16, wheel_radius=0.250000

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| A | Zahl | Eingang | (1, 0, 1) | The value to modulo. |
| A % B | Zahl | Ausgang | (0, 0, 0) | Outputs the remainder when A is divided by B. |
| B | Zahl | Eingang | (0, 0, 1) | The value to modulo A by. |

## Multiply (`gate_float_multiply`)

*Takes two number inputs, multiplies them together, and outputs the result.*

- Größe 2x1x2 Blöcke (voxel [0, 0, 0] .. [1, 0, 1]), Masse 1, Preis 20
- Werte: buoy_factor=1.000000, buoy_force=100.000000, buoy_radius=1.000000, constraint_range_of_motion=0.000000, door_lower_limit=-1.000000, door_upper_limit=1.000000, dynamic_min_rotation=0.000000, engine_max_force=1000.000000, force_emitter_max_force=1000.000000, force_emitter_max_vector=1.000000, light_fov=1.000000, light_intensity=0.000000, light_range=1.000000, logic_gate_type=15, magnet_force=0.000000, max_motor_force=100.000000, rudder_surface_area=0.000000, type=16, wheel_radius=0.250000

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| A | Zahl | Eingang | (1, 0, 1) | The value to be multiplied. |
| A x B | Zahl | Ausgang | (0, 0, 0) | Outputs the result of multiplying A by B. |
| B | Zahl | Eingang | (0, 0, 1) | The value to multiply by. |

## Not (`gate_bool_not`)

*A logic gate that outputs the logical NOT of its input signal.*
The output will always be the opposite of the input.

- Größe 1x1x2 Blöcke (voxel [0, 0, 0] .. [0, 0, 1]), Masse 1, Preis 20
- Werte: buoy_factor=1.000000, buoy_force=100.000000, buoy_radius=1.000000, constraint_range_of_motion=0.000000, door_lower_limit=-1.000000, door_upper_limit=1.000000, dynamic_min_rotation=0.000000, engine_max_force=1000.000000, force_emitter_max_force=1000.000000, force_emitter_max_vector=1.000000, light_fov=1.000000, light_intensity=0.000000, light_range=1.000000, logic_gate_type=3, magnet_force=0.000000, max_motor_force=100.000000, rudder_surface_area=0.000000, type=16, wheel_radius=0.250000

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| A | An/Aus | Eingang | (0, 0, 1) | The signal to invert. |
| NOT A | An/Aus | Ausgang | (0, 0, 0) | The logical NOT of input A. This output will always be the opposite of the input. |

## Numerical Inverter (`gate_float_invert`)

*The inverter takes a number as input, multiplies it by -1, and outputs the result.*

- Größe 1x1x2 Blöcke (voxel [0, 0, 0] .. [0, 0, 1]), Masse 1, Preis 20
- Werte: buoy_factor=1.000000, buoy_force=100.000000, buoy_radius=1.000000, constraint_range_of_motion=0.000000, door_lower_limit=-1.000000, door_upper_limit=1.000000, dynamic_min_rotation=0.000000, engine_max_force=1000.000000, force_emitter_max_force=1000.000000, force_emitter_max_vector=1.000000, light_fov=1.000000, light_intensity=0.000000, light_range=1.000000, logic_gate_type=8, magnet_force=0.000000, max_motor_force=100.000000, rudder_surface_area=0.000000, type=16, wheel_radius=0.250000

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Number to Invert | Zahl | Eingang | (0, 0, 1) | The number that will be inverted. |
| Inverted Number | Zahl | Ausgang | (0, 0, 0) | The inverse of the input. This is equivalent to multiplying the input by -1. |

## Numerical Junction (`gate_float_switch`)

*Acts as a junction for two number signals.*
The junction can be switched using an on/off signal. When the signal is on, the number is passed through to the first output and a value of 0 is passed to the second. When the signal is off, the number is passed through to the second output with the first being set to 0.

- Größe 2x1x2 Blöcke (voxel [0, 0, 0] .. [1, 0, 1]), Masse 1, Preis 20
- Werte: buoy_factor=1.000000, buoy_force=100.000000, buoy_radius=1.000000, constraint_range_of_motion=0.000000, door_lower_limit=-1.000000, door_upper_limit=1.000000, dynamic_min_rotation=0.000000, engine_max_force=1000.000000, force_emitter_max_force=1000.000000, force_emitter_max_vector=1.000000, light_fov=1.000000, light_intensity=0.000000, light_range=1.000000, logic_gate_type=5, magnet_force=0.000000, max_motor_force=100.000000, rudder_surface_area=0.000000, type=16, wheel_radius=0.250000

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Switch Signal | An/Aus | Eingang | (0, 0, 1) | Controls which of the two output paths the input value will be sent to. |
| Value to Pass Through | Zahl | Eingang | (1, 0, 1) | The value to pass through the junction. |
| On Path | Zahl | Ausgang | (0, 0, 0) | Receives the input value when the switch signal is set to on. |
| Off Path | Zahl | Ausgang | (1, 0, 0) | Receives the input value when the switch signal is set to off. |

## Numerical Switchbox (`gate_float_switch_input`)

*Acts as a switchbox for two number signals.*
Which of the two inputs is sent to the output is determined by the on/off switch signal. When the signal is on, the first value is sent to the output. When it is off, the second output is sent.

- Größe 2x1x2 Blöcke (voxel [0, 0, 0] .. [1, 0, 1]), Masse 1, Preis 20
- Werte: buoy_factor=1.000000, buoy_force=100.000000, buoy_radius=1.000000, constraint_range_of_motion=0.000000, door_lower_limit=-1.000000, door_upper_limit=1.000000, dynamic_min_rotation=0.000000, engine_max_force=1000.000000, force_emitter_max_force=1000.000000, force_emitter_max_vector=1.000000, light_fov=1.000000, light_intensity=0.000000, light_range=1.000000, logic_gate_type=10, magnet_force=0.000000, max_motor_force=100.000000, rudder_surface_area=0.000000, type=16, wheel_radius=0.250000

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Switch Signal | An/Aus | Eingang | (0, 0, 0) | Controls which of the two input values will be sent to the output. |
| First Value (On) | Zahl | Eingang | (1, 0, 1) | The value to output when the switch signal is on. |
| Switched Value | Zahl | Ausgang | (1, 0, 0) | Outputs the first value when the switch signal is on, and the second value when it is off. |
| Second Value (Off) | Zahl | Eingang | (0, 0, 1) | The value to output when the switch signal is off. |

## Or (`gate_bool_or`)

*A logic gate that outputs the logical OR of two input signals.*
The output will be switched on if either of the inputs is on, and off if neither are on.

- Größe 2x1x2 Blöcke (voxel [0, 0, 0] .. [1, 0, 1]), Masse 1, Preis 20
- Werte: buoy_factor=1.000000, buoy_force=100.000000, buoy_radius=1.000000, constraint_range_of_motion=0.000000, door_lower_limit=-1.000000, door_upper_limit=1.000000, dynamic_min_rotation=0.000000, engine_max_force=1000.000000, force_emitter_max_force=1000.000000, force_emitter_max_vector=1.000000, light_fov=1.000000, light_intensity=0.000000, light_range=1.000000, logic_gate_type=1, magnet_force=0.000000, max_motor_force=100.000000, rudder_surface_area=0.000000, type=16, wheel_radius=0.250000

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| A | An/Aus | Eingang | (1, 0, 1) | The first value to perform the logical OR on. |
| B | An/Aus | Eingang | (0, 0, 1) | The second value to perform the logical OR on. |
| A OR B | An/Aus | Ausgang | (0, 0, 0) | Outputs an on signal when either A or B are on, and an off signal if neither are on. |

## PID Controller (`gate_pid_controller`)

*A control loop feedback mechanism that measures and corrects the error in a system over time.*
It takes the current measured output of a system or sensor, and a desired target measurement. It outputs a value that can be used as an input to the system to gradually correct its error. For example, the controller could input to an engine's throttle to maintain a desired speed or altitude. The control terms (proportional, integral and derivative) can be set by selecting the component with the select tool. The control terms must be carefully tuned for optimal output.

- Größe 2x1x2 Blöcke (voxel [0, 0, 0] .. [1, 0, 1]), Masse 1, Preis 100
- Werte: buoy_factor=1.000000, buoy_force=100.000000, buoy_radius=1.000000, constraint_range_of_motion=0.000000, door_lower_limit=-1.000000, door_upper_limit=1.000000, dynamic_min_rotation=0.000000, engine_max_force=1000.000000, force_emitter_max_force=1000.000000, force_emitter_max_vector=1.000000, light_fov=1.000000, light_intensity=0.000000, light_range=1.000000, logic_gate_type=29, magnet_force=0.000000, max_motor_force=100.000000, rudder_surface_area=0.000000, type=16, wheel_radius=0.250000

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Active | An/Aus | Eingang | (0, 0, 0) | Sets whether or not the controller is active. When inactive, stored values are reset. |
| Control Output | Zahl | Ausgang | (1, 0, 0) | The output computed by the controller. |
| Process Variable | Zahl | Eingang | (0, 0, 1) | The current measured value of the system. |
| Setpoint | Zahl | Eingang | (1, 0, 1) | The desired value to correct the process variable to. |

## Power Add (`gate_torque_add`)

*Combines the outputs of two engines, allowing you to connect multiple engines to the same input.*

- Größe 2x1x2 Blöcke (voxel [0, 0, 0] .. [1, 0, 1]), Masse 1, Preis 20
- Werte: cable_radius=0.02, light_intensity=0, logic_gate_type=24, magnet_force=0, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, type=16

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Combined Power | Drehmoment | Ausgang | (0, 0, 0) | Outputs the combined power of engine 1 and 2. |

## Power Meter (`gate_torque_multimeter`)

*The power meter allows you to take a measurement of how much power is being output from an engine to a specific component.*
To prevent a loss of power, it should be connected in series between the engine and its receiving component.

- Größe 2x1x2 Blöcke (voxel [0, 0, 0] .. [1, 0, 1]), Masse 1, Preis 20
- Werte: cable_radius=0.02, light_intensity=0, logic_gate_type=25, magnet_force=0, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, type=16

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Relay | Drehmoment | Ausgang | (0, 0, 0) | Relays the power received from an engine. |

## Push to Toggle (`gate_push_to_toggle`)

*This component has an internal on/off switch that is toggled every time a new on signal is sent to its input.*
This can allow regular push buttons to act as toggle buttons.

- Größe 1x1x2 Blöcke (voxel [0, 0, 0] .. [0, 0, 1]), Masse 1, Preis 20
- Werte: buoy_factor=1.000000, buoy_force=100.000000, buoy_radius=1.000000, constraint_range_of_motion=0.000000, door_lower_limit=-1.000000, door_upper_limit=1.000000, dynamic_min_rotation=0.000000, engine_max_force=1000.000000, force_emitter_max_force=1000.000000, force_emitter_max_vector=1.000000, light_fov=1.000000, light_intensity=0.000000, light_range=1.000000, logic_gate_type=9, magnet_force=0.000000, max_motor_force=100.000000, rudder_surface_area=0.000000, type=16, wheel_radius=0.250000

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Toggle Signal | An/Aus | Eingang | (0, 0, 1) | An on signal toggles the internal on/off switch. |
| Internal State | An/Aus | Ausgang | (0, 0, 0) | The output of the internal on/off switch. |

## SR Latch (`gate_sr_latch`)

*An SR latch that can be set and reset using two on/off inputs.*
When both inputs are off, there is no change in state. If both Set and Reset are set to on, Reset will take precedence.

- Größe 2x1x2 Blöcke (voxel [0, 0, 0] .. [1, 0, 1]), Masse 1, Preis 20
- Werte: cable_radius=0, light_intensity=0, logic_gate_type=34, magnet_force=0, max_motor_speed=5, rudder_surface_area=0, type=16

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Set | An/Aus | Eingang | (1, 0, 1) | Sets the output to on. |
| Reset | An/Aus | Eingang | (0, 0, 1) | Sets the output to off. |
| Output | An/Aus | Ausgang | (1, 0, 0) | The internal state of the latch. |
| NOT Output | An/Aus | Ausgang | (0, 0, 0) | The inverse of the internal state of the latch. |

## Subtract (`gate_float_subtract`)

*Takes two number inputs, subtracts the second from first, and outputs the result.*

- Größe 2x1x2 Blöcke (voxel [0, 0, 0] .. [1, 0, 1]), Masse 1, Preis 20
- Werte: buoy_factor=1.000000, buoy_force=100.000000, buoy_radius=1.000000, constraint_range_of_motion=0.000000, door_lower_limit=-1.000000, door_upper_limit=1.000000, dynamic_min_rotation=0.000000, engine_max_force=1000.000000, force_emitter_max_force=1000.000000, force_emitter_max_vector=1.000000, light_fov=1.000000, light_intensity=0.000000, light_range=1.000000, logic_gate_type=7, magnet_force=0.000000, max_motor_force=100.000000, rudder_surface_area=0.000000, type=16, wheel_radius=0.250000

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| A | Zahl | Eingang | (1, 0, 1) | The value to subtract from. |
| A - B | Zahl | Ausgang | (0, 0, 0) | Outputs the result of subtracting B from A. |
| B | Zahl | Eingang | (0, 0, 1) | The value to subtract. |

## Threshold Gate (`gate_float_threshold`)

*Takes a value and compares it to a set threshold.*
A lower and upper bound to the threshold must be set. The output is set to on if the input value is less than or equal to the upper bound, and greater than or equal to the lower bound. If it is outside this range, the output is set to off. The threshold bounds can be configured by selecting this component with the select tool.

- Größe 1x1x2 Blöcke (voxel [0, 0, 0] .. [0, 0, 1]), Masse 1, Preis 20
- Werte: buoy_factor=1.000000, buoy_force=100.000000, buoy_radius=1.000000, constraint_range_of_motion=0.000000, door_lower_limit=-1.000000, door_upper_limit=1.000000, dynamic_min_rotation=0.000000, engine_max_force=1000.000000, force_emitter_max_force=1000.000000, force_emitter_max_vector=1.000000, light_fov=1.000000, light_intensity=0.000000, light_range=1.000000, logic_gate_type=13, magnet_force=1.000000, max_motor_force=100.000000, rudder_surface_area=0.000000, type=16, wheel_radius=0.250000

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Value to Test | Zahl | Eingang | (0, 0, 1) | The value to test within the threshold. |
| Within Threshold | An/Aus | Ausgang | (0, 0, 0) | Outputs an on signal when the input value is within the set threshold. |

## Train Junction Controller (`gate_train_junction`)

*This component has an internal on/off switch that is toggled every time a new on signal is sent to its input.*
This can allow regular push buttons to act as toggle buttons.

- Größe 1x1x2 Blöcke (voxel [0, 0, 0] .. [0, 0, 1]), Masse 1, Preis 20
- Werte: cable_radius=0.02, light_intensity=0, logic_gate_type=46, magnet_force=0, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, type=16

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Toggle Signal | An/Aus | Eingang | (0, 0, 1) | An on signal toggles the internal on/off switch. |
| Internal State | An/Aus | Ausgang | (0, 0, 0) | The output of the internal on/off switch. |

## Trigonometry (`gate_float_sin`)

*Provides a set of basic trigonometry functions.*
The available functions are sin, cos, tan, asin, acos and atan. If an invalid number is input, the output will be 0. Sin, cos and tan accept inputs measured in turns. Asin, acos and atan output values measured in turns. The function can be set by selecting this component with the select tool.

- Größe 1x1x2 Blöcke (voxel [0, 0, 0] .. [0, 0, 1]), Masse 1, Preis 20, Tags: sine,cosine,tangent,asin,atan,acos,inverse,function
- Werte: cable_radius=0, light_intensity=0, logic_gate_type=43, magnet_force=0, max_motor_speed=5, pump_pressure=0, rudder_surface_area=0, type=16

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| f(x) | Zahl | Ausgang | (0, 0, 0) | f(x), where f is the selected function and x is the input. |
| Input Number | Zahl | Eingang | (0, 0, 1) | The input to the function. |

## Up/Down (`gate_up_down`)

*This component uses two on/off signals to move an internal value between -1 and 1.*
The up input moves the value towards 1, and the down input moves it towards -1. This component can be used for converting on/off button presses into a standard number value that can be used to control any mechanical components that accept a standard number input.

- Größe 2x1x2 Blöcke (voxel [0, 0, 0] .. [1, 0, 1]), Masse 1, Preis 20
- Werte: buoy_factor=1.000000, buoy_force=100.000000, buoy_radius=1.000000, constraint_range_of_motion=0.000000, door_lower_limit=-1.000000, door_upper_limit=1.000000, dynamic_min_rotation=0.000000, engine_max_force=1000.000000, force_emitter_max_force=1000.000000, force_emitter_max_vector=1.000000, light_fov=1.000000, light_intensity=0.000000, light_range=1.000000, logic_gate_type=4, magnet_force=0.000000, max_motor_force=100.000000, rudder_surface_area=0.000000, type=16, wheel_radius=0.250000

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| Up | An/Aus | Eingang | (1, 0, 1) | Moves the internal value towards 1. |
| Down | An/Aus | Eingang | (0, 0, 1) | Moves the internal value towards -1. |
| Up/Down Value | Zahl | Ausgang | (0, 0, 0) | The internally stored value between -1 an 1. |

## Xor (`gate_bool_xor`)

*A logic gate that outputs the logical XOR of two input signals.*
The output will be switched on if only one of the signals are on. The output will be switched off if the two signals are the same.

- Größe 2x1x2 Blöcke (voxel [0, 0, 0] .. [1, 0, 1]), Masse 1, Preis 20
- Werte: buoy_factor=1.000000, buoy_force=100.000000, buoy_radius=1.000000, constraint_range_of_motion=0.000000, door_lower_limit=-1.000000, door_upper_limit=1.000000, dynamic_min_rotation=0.000000, engine_max_force=1000.000000, force_emitter_max_force=1000.000000, force_emitter_max_vector=1.000000, light_fov=1.000000, light_intensity=0.000000, light_range=1.000000, logic_gate_type=2, magnet_force=0.000000, max_motor_force=100.000000, rudder_surface_area=0.000000, type=16, wheel_radius=0.250000

| Anschluss | Art | Richtung | Lage (x,y,z) | Beschreibung |
|---|---|---|---|---|
| A | An/Aus | Eingang | (1, 0, 1) | The first value to perform the logical XOR on. |
| B | An/Aus | Eingang | (0, 0, 1) | The first value to perform the logical XOR on. |
| A XOR B | An/Aus | Ausgang | (0, 0, 0) | Outputs an on signal if only A is on, or only B is on. The output is off if A and B are both on or off. |
