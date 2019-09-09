# datestamp.py

This trigger sets `entity_types`' `date_field`s to the current date/time for a
specified `timezone` when either:

1. `status_field` field is set to a value in `statuses`.
2. A new entity of type `entity_types` is created.

Both of these are optional, see notes and args.

It is also possible—with the `allow_date_overwrite` arg—to control whether
or not an existing value in `date_field` is overwritten.

## Demo

![](images/datestamp1.gif?raw=true)

## Notes

If you'd like the plugin to only fire on entity creation, set either the 
`status_field` or `statuses` arg to `""` or `[]` respectively.

## Args

| Arg name                    | Type                 | Description                                                            |
| :-                          | :-                   | :-                                                                     |
| entity_types                | List of Strings      | The types of entities this trigger acts on.                            |
| status_field                | String               | The List or Status List field on `entity_types` this trigger acts on.  |
| statuses                    | List of Strings      | The list of Status value(s) this trigger acts on.                      |
| date_field                  | String               | The Date or Date and Time field to update, relative to `entity_types`. |
| timezone                    | pytz timezone String | The local timezone used in datetime conversions (e.g., "US/Pacific").  |
| allow_date_overwrite        | Boolean              | Determines whether existing date values are overwritten.               |
| set_date_on_entity_creation | Boolean              | Determines whether or not the date is set on entity creation.          |
