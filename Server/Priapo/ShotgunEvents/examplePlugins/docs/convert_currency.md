# convert_currency.py

This plugin sets an `entity_type`'s `to_currency_field`'s based on its
`from_currency_field`'s value and `exchange_rate_field`'s value when either:

1. `status_field` is updated to any Status, excluding those in `ignore_statuses`.
2. `exchange_rate_field`'s value is changed.
3. `from_currency_field`'s value is changed.

## Demo

![](images/convert_currency1.gif?raw=true)

## Args

| Arg name            | Type            | Description                                                                               |
| :-                  | :-              | :-                                                                                        |
| entity_type         | String          | The type of `entity this` plugin acts on.                                                 |
| from_currency_field | String          | The field on `entity_type` to convert currency from.                                      |
| to_currency_field   | String          | The field on `entity_type` to convert currency to.                                        |
| exchange_rate_field | String          | The field on `entity_type` that stores the exchange rate used in the currency conversion. |
| status_field        | String          | The field on `entity_type` that activates this plugin.                                    |
| ignore_statuses     | List of Strings | A list of Status values on `status_field` that will be ignored.                           |
