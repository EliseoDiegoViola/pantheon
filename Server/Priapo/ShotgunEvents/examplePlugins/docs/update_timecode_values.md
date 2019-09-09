# update_timecode_values.py

This trigger keeps timecode and frame values in sync across a variety of 
specified fields on an `entity_type`. This is a fairly complicated trigger. See
QA notes for more detail.

## Demo

![](images/update_timecode_values1.gif?raw=true)

Test here: https://studio-qa.shotgunstudio.com/page/2036?layout=update_timecode_values

Change settings here: <http://staging-sg-events.herokuapp.com/admin/sg_plugin/sgplugin/72/>

## JSON settings

| Setting name           | Type   | Description                                                                                |
| :-                     | :-     | :-                                                                                         |
| entity_type            | String | The type of entity this trigger acts on.                                                   |
| entity_name_field      | String | The field that stores an `entity_type`'s name, e.g., `code`.                               |
| head_duration_field    | String | The field on `entity_type` that stores the head duration value in frames.                  |
| tail_duration_field    | String | The field on `entity_type` that stores the tail duration value in frames.                  |
| timecode_cut_in_field  | String | The field on `entity_type` that stores the cut-in value in timecode, as a str in sg.       |
| timecode_cut_out_field | String | The field on `entity_type` that stores the cut-out value in timecode, as a str in sg.      |
| timecode_in_field      | String | The field on `entity_type` that stores the timecode-in value in timecode, as a str in sg.  |
| timecode_out_field     | String | The field on `entity_type` that stores the timecode-out value in timecode, as a str in sg. |
| first_frame_field      | String | The field on `entity_type` that stores the first frame value in frames.                    |
| last_frame_field       | String | The field on `entity_type` that stores the last frame value in frames.                     |
| frame_count_field      | String | The field on `entity_type` that stores the frame count value in frames.                    |
| fps                    | Float  | The frames-per-second value used to convert between timecode and frames.                   |

## Related tickets

* 40647
* 29483

## QA notes

To create a new test case for this trigger, create new Version and populate
these two Version fields with the following values (*Note*: typically the Import
 Scan app will populate these fields, as this trigger is used in conjunction
 with that app):

```
Timecode Cut In: 01:00:01:00
Timecode Cut Out: 01:00:02:00
```

Now, update the following fields, which should trigger cascading updates to the
remaining fields:

```
Head Duration: 24
Tail Duration: 24
First Frame: 1001
```

See attached image for reference and expected calculations:

![](images/update_timecode_values2.jpg?raw=true)

