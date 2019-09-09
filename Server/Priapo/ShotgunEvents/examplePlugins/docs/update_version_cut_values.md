# update_version_cut_values.py

This trigger maintains the relationship between different cut fields on a
Version. See QA notes for more details.

## Demo

![](images/update_version_cut_values1.gif?raw=true)

## Args

| Arg name            | Type   | Description                                            |
| :-                  | :-     | :-                                                     |
| first_frame_field   | String | The Version field that stores the first frame value.   |
| last_frame_field    | String | The Version field that stores the last frame value.    |
| cut_in_field        | String | The Version field that stores the cut in value.        |
| cut_out_field       | String | The Version field that stores the cut out value.       |
| cut_length_field    | String | The Version field that stores the cut length value.    |
| head_duration_field | String | The Version field that stores the head duration value. |
| tail_duration_field | String | The Version field that stores the tail duration value. |
| frame_count_field   | String | The Version field that stores the frame count value.   |
| default_head_in     | String | The head_in_field's default value in frames.           |
| default_tail_out    | Int    | The tail_out_field's default value in frames.          |

## QA notes

To get this trigger tested, create a new Version with the following values
populated:

```
Head Duration: 0
Tail Duration: 0

First Frame: 1001
Last Frame: 1025
Frame Count: 24

Cut In: 1001
Cut Out: 1025
Cut Length: 24
```