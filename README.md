# Steam Trade Finder


[![Build status][build-image]][build]
[![Updates][dependency-image]][pyup]
[![Python 3][python3-image]][pyup]
[![Code coverage][codecov-image]][codecov]
[![Code Quality][codacy-image]][codacy]

This repository contains Python code to find Steam trades for a given appID.

## Requirements

-   Install the latest version of [Python 3.X](https://www.python.org/downloads/).
-   Install the required packages:

```bash
pip install -r requirements.txt
```

## Usage

### Download the list of userIDs of ASF bots

Download the HTML code from [a public listing of ASF bots](https://asf.justarchi.net/STM).
Then edit it as follows, using for instance Visual Studio Code, with regular expressions allowed: 

1. Remove HTML lines [which do not contain the word]((https://stackoverflow.com/a/7024359)) "steamtradematcher":
```regexp
^(?!.*steamtradematcher.*).+$
```

2. Trim the beginning of lines:
```regexp
^.*/specscan/
```

3. Trim the end of lines:
```regexp
" target.*$
```

4. Replace the following with `\n`:
```regexp
\n+
```

You should obtain a list of userIDs of ASF bots, similar to [`data/asf_bots.txt`](data/asf_bots.txt).

### Find Steam trades

Run the following script to find Steam trades:

```bash
python trade_finder.py
```

## References

-   [Steam Trade Matcher (STM)](https://www.steamtradematcher.com/),
-   [Wiki: automated STM based on ArchiSteamFarm (ASF)](https://github.com/JustArchiNET/ArchiSteamFarm/wiki/Statistics#public-asf-stm-listing),
-   [A public listing of ASF bots](https://asf.justarchi.net/STM).


<!-- Definitions -->

[build]: <https://travis-ci.org/woctezuma/steam-trade-finder>
[build-image]: <https://travis-ci.org/woctezuma/steam-trade-finder.svg?branch=master>

[pyup]: <https://pyup.io/repos/github/woctezuma/steam-trade-finder/>
[dependency-image]: <https://pyup.io/repos/github/woctezuma/steam-trade-finder/shield.svg>
[python3-image]: <https://pyup.io/repos/github/woctezuma/steam-trade-finder/python-3-shield.svg>

[codecov]: <https://codecov.io/gh/woctezuma/steam-trade-finder>
[codecov-image]: <https://codecov.io/gh/woctezuma/steam-trade-finder/branch/master/graph/badge.svg>

[codacy]: <https://www.codacy.com/app/woctezuma/steam-trade-finder>
[codacy-image]: <https://api.codacy.com/project/badge/Grade/038afb64dd404f8f978ff8ba41b65aef>

