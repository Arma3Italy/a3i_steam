# Search for Italian Arma 3 servers on Steam

This script searches for all the arma 3 servers on steam that matches this regex:
| regex | exemple |
| --- | --- |
| (^ita\\s) | "ita superserver" |
| (\\sita\\s) | "super ita server" |
| (\\s?italia\\s?) | "super italia server" or "superitaliaserver" |
| (\[ita(\/[a-zA-Z]+)*\]) | "[ita]" or "[ita/eng]" or "[ITA/ENG/GER]" |

Those filters are case insensitive so "ita" and "Ita" are the same.

To add new filters you can:
- create a Issue with the filter you want to add
- fork the repo and create a pull request with the filter added to the source code

## install dependencies

dependencies:
- python 3.8
- requests
- pymongo
- dnspython

### linux
```bash
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

### windows
```bash
$ python -m venv .venv
$ .venv\Scripts\activate
$ pip install -r requirements.txt
```

## run
```bash
$ python main.py
```
