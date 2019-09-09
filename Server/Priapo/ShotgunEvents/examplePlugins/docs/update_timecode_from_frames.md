# update_timecode_from_frames.py

This trigger sets `target_tc_field` on an `entity_type` to a timecode value 
derived by converting frames stored in `source_frames_field` to timecode via the 
`fps` setting.

## Demo

![](images/update_timecode_from_frames1.gif?raw=true)

## Notes

It is possible to kill this plugin by setting the `source_frames_field` to a
huge value. In that case the Shotgun Python API will return a CRUD error that
looks like this:

`Fault: API update() CRUD ERROR #5: Update failed for [Shot.sg_cut_length_r_t]: PG::NumericValueOutOfRange: ERROR:  value "3062050417" is out of range for type integer`

## Args

| Arg name            | Type    | Description                                                                      |
| :-                  | :-      | :-                                                                               |
| entity_type         | String  | The type of entity this trigger acts on.                                         |
| source_frames_field | String  | The field whose frame value is used to calculate the timecode value.             |
| target_tc_field     | String  | The field relative to entity_type to set timecode on.                            |
| fps                 | Float   | The float fps value used to convert the `source_frames_field` value to timecode. |
