# field_to_field.py

If `from_field` is set to `from_value` on an `entity_type`, `to_field` is set to
`to_value` on that same `entity_type`.

## Demo

![](images/field_to_field1.gif?raw=true)

## Args

| Arg name     | Type     | Description                                       |
| :-           | :-       | :-                                                |
| entity_type  | String   | The type of entity this trigger acts on.          |
| from_field   | String   | The field on entity_type this trigger acts on.    |
| from_value   | Any type | The value on from_field this trigger acts on.     |
| to_field     | String   | The file on entity_type this trigger targets.     |
| to_value     | Any type | The value set on to_field when this trigger runs. |
