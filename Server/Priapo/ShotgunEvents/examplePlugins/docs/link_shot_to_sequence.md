# link_shot_to_sequence.py

This plugin links a Sequence to a Shot when the Shot's `code` value is changed—
based on a regrex match on the Shot `code`. Note that this will happen on Shot
creation.

## Demo

![](images/link_shot_to_sequence1.gif?raw=true)

## Args

| Arg name                  | Type            | Description                                                                                                     |
| :-                        | :-              | :-                                                                                                              |
| shot_code_regex           | String          | How to match Shot codes with Sequences. Eg. `^([A-Za-z]{2})([0-9]{4})`                                          |
| sequence_code_regex_group | Int             | Matching group number in the shot_code_regex identifying the Sequence code.                                     |
| sequence_code_field       | String          | Which field to search for matching Sequence codes. Eg. `sg_sequence_code`.                                      |
| sequence_filters          | List of Strings | List of additional filters used to search for the matching Sequence. Eg. `[["sg_status_list", "is_not", "na"]]` |

