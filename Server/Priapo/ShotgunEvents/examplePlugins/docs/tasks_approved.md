# tasks_approved.py

This plugin sets a Task's `task_status_field` to `downstream_task_status_active`
when an upstream Task's `task_status_field` is set to a valid `task_status`. If the
target Task's `task_status_field` is currently set to a valid `downstream_task_recurse` status
(e.g., "na"), the plugin will recurse the dependency graph until it finds a
Task to update. The plugin can also optionally close open Notes linked to the
Task. See the QA images below for more details.

## Demo

![](images/tasks_approved1.gif?raw=true)

## Args

| Arg name                        | Type    | Description                                                                              |
| :------------------------------ | :-----  | :--------------------------------------------------------------------------------------- |
| task_status_field               | String  | The status field on Task entities this plugin acts on.                                   |
| task_status                     | List    | The task_status_field values this plugin acts on.                                        |
| downstream_tasks_field          | String  | The Task field used to query downstream Tasks.                                           |
| downstream_task_status_activate | List    | The downstream Task statuses that identifies a Task as needing activation.               |
| downstream_task_status_active   | String  | The downstream Task status that should be set on activation.                             |
| downstream_task_status_recurse  | List    | The downstream Task statuses that triggers recursion of the downstream dependency graph. |
| note_status_field               | String  | The field on Note entities used to set and query statuses.                               |
| close_notes                     | Boolean | A boolean that determines whether or not Notes are closed.                               |
| closed_note_status              | String  | The Status to set closed Notes to.                                                       |

## QA images

![](images/tasks_approved2.png?raw=true)