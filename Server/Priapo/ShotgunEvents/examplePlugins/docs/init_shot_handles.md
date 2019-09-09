# init_shot_handles.py

This trigger initializes Smart Cut fields by pre-populating default values for 
the `smart_head_in`, `smart_head_duration`, and `smart_tail_duration` fields.

## Demo

![](images/init_shot_handles1.gif?raw=true)

## Args

| Arg name            | Type | Description                                    |
| :-                  | :-   | :-                                             |
| smart_head_in       | Int  | The type of entity this trigger acts on.       |
| smart_head_duration | Int  | The field on entity_type this trigger acts on. |
| smart_tail_duration | Int  | The value on from_field this trigger acts on.  |
