# version_status_update_task_status.py

When a script or HumanUser updates a Version's `sg_status_list` field, the
linked Task's `sg_status_list` field is also updated, based on the value defined
in the Status's `sg_task_status_mapping` field. If the `sg_task_status_mapping`
field is blank or if the Status defined in the `sg_task_status_mapping` field is
not present on the Task, do not update the Task Status field.

Additionally, when a script or HumanUser updates the Version's `sg_status_list`
to the `approved_status_code`, update the Version's `date_approved_field`, based
on the `date_approved_timezone` value.

## Demo

![](images/version_status_update_task_status1.gif?raw=true)

Test here: https://studio-qa.shotgunstudio.com/page/2036?layout=version_status_update_task_status

Change settings here: <http://staging-sg-events.herokuapp.com/admin/sg_plugin/sgplugin/84/>

## Notes

Settings for this trigger are effectively split between Django and the
`sg_task_status_mapping` field on the Status entity. Go to the Status entity's
page in Shotgun and reveal the `sg_task_status_mapping` field to control Status
mappings.

Django setting "Ignore non-human events" should be *OFF*.

## JSON settings

| Setting name           | Type                 | Description                                               |
| :-                     | :-                   | :-                                                        |
| date_approved_field    | String               | The field on Version that stores the approved date.       |
| date_approved_timezone | pytz timezone String | The timezone to use when calculating the date.            |
| approved_status_code   | String               | The `date_approved_field` is set when this Status is set. |

## Related tickets

* 41784
* 39294