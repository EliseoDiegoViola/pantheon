# task_status_update_version_status.py

When a HumanUser updates a Task's Status, find the latest Version in Shotgun
whose Task matches the relevant Task, and update that Version's Status to the
value defined defined by the Status' `status_mapping_field`. If the
`status_mapping_field` value is blank or not present on the Version, do not
update the Version Status field.

## Demo

![](images/task_status_update_version_status1.gif?raw=true)

## Notes:

This trigger's args are effectively split between Django and the
`status_mapping_field` field on the Status entity. Go to the Status entity's
page in Shotgun and reveal the `status_mapping_field` field to control Status
mappings.

Note: This trigger will need to play nicely with #39294.

## Args

| Arg name             | Type   | Description                                                                                 |
| :-                   | :-     | :-                                                                                          |
| status_mapping_field | String | The Status entity field that determines what values this trigger maps existing Statuses to. |
