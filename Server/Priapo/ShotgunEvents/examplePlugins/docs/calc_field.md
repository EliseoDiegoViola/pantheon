# calc_field.py

When either `field_a` or `field_b` are changed on an `entity_type` in Shotgun,
`field_to_update` is set to the result of `field_a` and `field_b` as modified by
the math `operator`, i.e.:

`field_a` * `field_b` = `field_to_update`

... where `*` is determined by `operator`.

Either `field_a` or `field_b` can be set to a static value instead of referring
to a field on the Shotgun `entity_type`. Both cannot be set to static values
because then there would be nothing to trigger off of.

`field_a` and `field_b` can refer to `Float`, `Number`, `Currency`, or `Percent`
field types in Shotgun. `field_to_update` can be set to those same types, and
also `Text`.

## Demo

![](images/calc_field1.gif?raw=true)

## Args

| Arg name        | Type                   | Description                                                                |
| :-              | :-                     | :-                                                                         |
| entity_type     | str                    | The type of entity this trigger acts on.                                   |
| field_a         | str, int, float        | The field on entity_type that stores the first value, or an int or float.  |
| field_b         | str, int, float        | The field on entity_type that stores the second value, or an int or float. |
| operator        | str "+", "-", "*", "/" | The math operator to use in the calculation.                               |
| field_to_update | str                    | The field on entity_type that stores the result of the calculation.        |
