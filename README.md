JSON Explorer
=============

Tools to get data only some specific field from a JSON File

CLI Usage
---------

```
usage: jsonexplorer [-h] [-v] [--input INPUT | --input-file INPUT_FILE] key

positional arguments:
  key                   Key to parse

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Verbose
  --input INPUT         Raw JSON data
  --input-file INPUT_FILE
                        Path to JSON File
```

Example:

`jsonexplorer --input-file example.json "object.*.name"`

Python usage
------------

```
import jsonexplorer

obj = JsonExplorer()
result = obj.parse_and_explore(key, python_dict)
```

Key Name Rules
--------------

**Atom** : 

    - C Name Like (no whitespace only alphanumeric chars + underscore)
    - double quoted string
    - INT corresponding to one index of a list
    - wildcard "*" corresponding to every index of a list

**List separated by dots** :

Using atoms, list separated by dots and list separated by colon, you can create a list separated by dots ".". It will enter in the object or list of the specified data.

**List separated by colon with braces**:

Using atoms, list separated by dots and list separated by colon, you can create a list separated by colon "," with braces around it. It will go in each expression

Examples
--------

Let's take
```
{
  "object": [
    {
        "name": "a",
        "extra": {
            "value": 0,
            "date": "01/01"
        }
    },
    {
        "name": "b",
        "extra": {
            "value": 1,
            "date": "06/06"
        }
    },
    {
        "name": "c",
        "extra": {
            "value": 2,
            "date": "12/12"
        }
    }
  ]
}
```

With the key `object.*.{name,extra.data}`

The result is:
```
a  0
b  1
c  2
```

You can also use multiple times those lists:

With the key `object.*.{name,extra.{value,date}}`

The result is:
```
a  0  01/01
b  1  06/06
c  2  12/12
```