# calc_summaries.py

When the `field` value of an `entity_type` in the `summarize` list changes,
`field_to_update` is updated on the summarize entity (determined by
`link_fields` values) with the result of all summaries defined in the
`summarize` list, calculated in the order they are defined. The `sum_or_count`
and `operator` args determine how `summarize` list items are combined,
according to PEMDAS math rules. The `filters` list can be used to limit summary
results to entities with specific field values.

## Demo

![](images/calc_summaries1.gif?raw=true)

## Notes

Here is a practical example of real-world args a client might use; the
`sg_bid` fields on the entity types `Asset` and `Shot` are summed, and the
result is stored on the `sg_project_bid_budget` field on the Project entity.
`Shot` records that don't contain the string `sh` are excluded.

```
{
  "summarize": [
    {
      "operator": "+",
      "field": "sg_bid",
      "entity_type": "Asset",
      "filters": [],
      "sum_or_count": "sum",
    },
    {
      "operator": "+",
      "field": "sg_bid",
      "entity_type": "Shot",
      "filters": [
        [
          "code",
          "contains",
          "sh"
        ]
      ],
      "sum_or_count": "sum",
    }
  ],
  "field_to_update": "sg_project_bid_budget",
  "link_fields": {
    "Shot": "project",
    "Asset": "project",
  }
}
```

Note that any entity type referenced in the `summarize` list must have a link
field defined in the `link_fields` dict.

## Args

| Arg name        | Type                   | Description                                                                                              |
| :-              | :-                     | :-                                                                                                       |
| field_to_update | str                    | The field that stores the summary result on the summarize entity, as determined by `link_fields` values. |
| link_fields     | dict                   | Key/value pairs; keys are entity types, values are fields that link to the summarize entity.             |
| summarize       | list of dicts          | A list of summary item dicts.                                                                            |
| entity_type     | str                    | The type of entity to summarize field values on.                                                         |
| field           | str                    | The field on `entity_type` to summarize.                                                                 |
| sum_or_count    | str "sum", "count"     | Whether the `field` on `entity_type` should be summed or counted.                                        |
| operator        | str "+", "-", "*", "/" | The math operation to use when factoring the current summary result into the final result.               |
| filters         | list of lists, standard sg filter | A standard Shotgun Python API filters list used to limit `entity_type` results.               |
