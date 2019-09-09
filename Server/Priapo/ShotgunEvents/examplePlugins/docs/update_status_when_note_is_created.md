# update_status_when_note_is_created.py

This trigger sets `status_field` to `new_status` on an `entity_type` when a Note
is created, if the entity is already set to a Status in `trigger_statuses`.

## Demo

![](images/update_status_when_note_is_created1.gif?raw=true)

## Args

| Arg name         | Type            | Description                                        |
| :-               | :-              | :-                                                 |
| entity_type      | String          | The type of entity this trigger acts on.           |
| status_field     | String          | The field on entity_type that stores its status.   |
| trigger_statuses | List of Strings | The statuses in status_field this trigger acts on. |
| new_status       | String          | The status value set on status_field on success.   |
