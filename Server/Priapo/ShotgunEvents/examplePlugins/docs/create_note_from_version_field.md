# create_note_from_version_field.py

When a HumanUser or Script updates a Version's `content_field` field value, 
create a Note based on the value in that field.

## Demo

![](images/create_note_from_version_field1.gif?raw=true)

## Notes

The Django `Ignore non-human events` should be OFF for this trigger.

## Args

| Arg name         | Type   | Description                                                                        |
| :-               | :-     | :-                                                                                 |
| sg_note_type     | String | The Note type, as specified by the sg_note_type list field.                        |
| content_field    | String | The Version field to gather text from for the body of the Note.                    |
| author_is_artist | Bool   | Whether the author of the Note is the artist or the user that generated the event. |
