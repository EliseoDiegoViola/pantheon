# update_version_task_field.py

This trigger links a Task to a Version if all of the following conditions are
met:

1. The Version and Task are linked to the same entity.
2. The Version's `matched_version_field` value matches a value in the Task's
`matched_task_field` (this can be a multi-entity field).
3. The Task's `Task.step.Step.code` field matches the `matched_task_step_value`.

If more than one Task fulfills these criteria, one is arbitrarily chosen by the
Python API's `find_one` method.

## Demo

![](images/update_version_task_field1.gif?raw=true)

## Notes

This is critical to the split Shots workflow.

## Args

| Arg name                | Type            | Description                                                                |
| :-                      | :-              | :-                                                                         |
| matched_version_field   | String          | The Version field whose value is compared to `matched_task_field`'s value. |
| matched_task_field      | String          | The Task field whose value is compared to `matched_version_field`'s value. |
| matched_task_step_value | List of Strings | The value to use when matching Task Steps.                                 |
