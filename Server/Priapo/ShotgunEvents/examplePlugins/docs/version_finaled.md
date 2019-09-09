# version_finaled.py

When a Version's `version_status_field` is set to a value in `query_statuses`,
do the following:

1. The `target_status_field` on `target_entity_type` is updated with the
`target_status`, or if no `target_status` is specified, with the same value as
the `version_status_field`.
2. The `target_date_field` is updated with the current date/timestamp.
3. The `linked_version_field` is set to the triggered Version.
4. Any other Versions that share the same `target_entity_type` and that are set
to any of the `query_statuses` are updated to have the `superseded_status`
value, if specified.

## Demo

![](images/version_finaled1.gif?raw=true)

## Args

| Arg name             | Type                 | Description                                                                               |
| :-                   | :-                   | :-                                                                                        |
| version_status_field | String               | The Status field on the Version this trigger acts on.                                     |
| query_statuses       | String               | A list of Statuses on the Version that are considered final.                              |
| target_entity_type   | String               | The Shotgun entity type that changes to the Version will target.                          |
| target_status_field  | String               | The Status field this trigger sets on `target_entity_type`.                               |
| target_status        | String               | The Status to set as a result of a `version_status_field` change.                         |
| superseded_status    | String               | The Status to set Versions to that are linked to the same `target_entity_type`.           |
| version_date_field   | String               | A date field on the Version to update. Note: timezone setting is required.                |
| target_date_field    | String               | The date field on the `target_entity_type` to update. Note: timezone setting is required. |
| linked_version_field | String               | A single entity field to update on the `target_entity_type`.                              |
| timezone             | pytz timezone String | A timezone used to calculate the date/time on Versions and `target_entity_type`s.         |
