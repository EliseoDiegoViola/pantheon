# init_entity.py

When an `entity_type` is created in Shotgun, use the key-value pairs from
`initial_data` to set values for the fields (keys), if the query `filters` don't
invalidate the entity instance.

Where providing data for an entity or multi-entity field, use the conventions of
the Shotgun Python API, for example:

```json
"initial_data": {
    "sg_vendor_groups": [
      {
        "type": "Group", 
        "id": 1
      }
    ]
}
```

By default the trigger won’t clobber any field data that’s already present in
Shotgun unless `force` is `true`.

## Demo

![](images/studio_trigger_init_entity.gif?raw=true)

## Args

| Arg name     | Type    | Description                                                                  |
| :-           | :-      | :-                                                                           |
| entity_type  | str     | The type of entity this trigger acts on.                                     |
| filters      | list    | Standard SG API list of lists used to limit query results.                   |
| initial_data | dict    | Key-value pairs (field_name: initial value) to use to initialise the entity. |
| force        | boolean | When true, will overwrite existing data (e.g. if the user provided it).      |

