# calculate_cut_length.py

This trigger sets an `entity_type`'s `cut_duration_field` and
`cut_length_rt_field` to the difference between `cut_in_field` and
`cut_out_field`, if either the `cut_in_field` or `cut_out_field` values change.
The `fps` setting is used to convert frames to timecode. Additionally,
`cut_length_rt_field`'s value is updated if the `cut_duration_field`'s value is
changed.

## Demo

![](images/calculate_cut_length1.gif?raw=true)

## Args

| Arg name            | Type   | Description                                                              |
| :-                  | :-     | :-                                                                       |
| entity_type         | String | The entity type this trigger acts on.                                    |
| cut_in_field        | String | The field on `entity_type` that stores the cut in number.                |
| cut_out_field       | String | The field on `entity_type` that stores the cut out number.               |
| cut_duration_field  | String | The field on `entity_type` that stores the cut duration number.          |
| cut_length_rt_field | String | The field on `entity_type` that stores the cut length timecode.          |
| fps                 | Float  | The frames-per-second value used to convert between frames and timecode. |
