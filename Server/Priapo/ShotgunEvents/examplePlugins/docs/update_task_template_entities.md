# update_task_template_entities.py

This trigger can be used instead of the "Update entities with new tasks..."
built-in Shotgun command; that built-in command is non-destructive and won't:

1. Update empty Task fields if new values are set in the TaskTemplate.
2. Update non-empty Task fields that have changed in the TaskTemplate.
3. Delete Tasks that aren't in the TaskTemplate.

This trigger will always do #1, and only do #2 and #3 if `overwrite_field_values`
and `trash_old_tasks` are `True`, respectively. The `exclude_fields` setting can
also be used to gain finer-grained control over which fields are destructively
updated and which are not.

## Notes

The default settings for this plugin are set to odd values. This is to work
around a limitation in sg-django-services. The following settings are better
defaults:

```
{
  "plugins_field": "sg_plugins",
  "trash_old_tasks": true,
  "project_ids": [
    70
  ],
  "exclude_fields": [
    "task_assignees",
    "start_date",
    "due_date",
    "duration"
  ],
  "overwrite_field_values": true,
  "plugins_field_value": "Update linked entities",
  "entity_types": [
    "Asset"
  ]
}
```

## Demo

![](images/update_task_template_entities1.gif?raw=true)

## Args

| Arg name               | Type            | Description                                                                           |
| :-                     | :-              | :-                                                                                    |
| project_ids            | list of ints    | The IDs of the Shotgun Projects this trigger acts on.                                 |
| entity_types           | list of strings | The entity types this trigger acts on.                                                |
| plugins_field          | str             | The field on TaskTemplate used to trigger this plugin.                                |
| plugins_field_value    | str             | The value `field` must be set to to trigger this plugin.                              |
| trash_old_tasks        | bool            | Whether or not to trash Tasks on entities that are not in the Task Template.          |
| overwrite_field_values | bool            | Whether or not to overwrite existing field values on Tasks.                           |
| exclude_fields         | list of strings | Task fields whose values will not be updated, even if overwrite_field_values is True. |
