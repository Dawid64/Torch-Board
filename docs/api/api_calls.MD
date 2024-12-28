## - ```/get_changes``` : GET
Returns JSON of all changed variables (since last request) in the form:
```javascript
{
    "name_0": [ val_0, val_1...,val_n],
    ...
    "name_n": [ val_0, val_1...,val_n],
}
```
At least one value is present in each list, else the variable is not included in the response 