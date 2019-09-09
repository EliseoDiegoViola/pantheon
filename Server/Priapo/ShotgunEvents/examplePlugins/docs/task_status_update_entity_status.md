# task_status_update_entity_status.py

1. When a Task's `task_status_field` is changed to `task_fin_status`, check to
see if all Tasks linked to the parent entity have `task_status_field` values's
also set to `task_fin_status`. If so, set the parent entity's
`target_status_field` to `target_fin_status`, as long as it is not currently set
 to `target_disable_status`.

2. If a Task's `task_status_field` is changed from `task_fin_status` to any
other Status except `task_na_status`, check if the parent entity's
`target_status_field` is currently `target_fin_status`. If so, set that parent
entity's `target_status_field` to`target_ip_status`, as long as it is not
currently set to `target_disable_status`.

## Demo

![](images/task_status_update_entity_status1.gif?raw=true)

## Args

| Arg name               | Type   | Description                                                                        |
| :-                     | :-     | :-                                                                                 |
| task_status_field      | String | The Task entity field this trigger acts on.                                        |
| task_fin_status"       | String | The `task_status_field` value meaning finished/complete.                           |
| task_ip_status"        | String | The `task_status_field` value meaning in progress.                                 |
| task_na_status"        | String | The `task_status_field` value meaning not applicable                               |
| target_status_field"   | String | The parent entity's Status field this trigger targets.                             |
| target_fin_status"     | String | The `target_status_field` value meaning finished/complete.                         |
| target_ip_status"      | String | The `target_status_field` value meaning in progress.                               |
| target_disable_status" | String | The status value on `target_status_field` that disables this trigger for the Task. |
