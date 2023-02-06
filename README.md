# Steam Trade Finder


[![Build status][build-image]][build]
[![Code coverage][codecov-image]][codecov]
[![Code Quality][codacy-image]][codacy]

This repository contains Python code to find Steam trades for a given appID.

## Introduction

Available automated tools ([STM](https://www.steamtradematcher.com/) and [ASF](https://github.com/JustArchiNET/ArchiSteamFarm/)) look for **good** trades for both sides.
However, you can be missing out on good trades from your perspective, which would be **neutral** for the other side.

The good news is that if you find such a trade (good for you, neutral for them), and if the other side is using ASF,
then the trade will be [automatically accepted](https://github.com/JustArchiNET/ArchiSteamFarm/wiki/Trading#steamtradematcher).

The objective of the tool provided in this repository is to ease the search for potentially **neutral** Steam trades.

## Requirements

-   Install the latest version of [Python 3.X](https://www.python.org/downloads/).
-   Install the required packages:

```bash
pip install -r requirements.txt
```

## Usage

### Download the list of userIDs of ASF bots

The objective is to obtain a list of userIDs of ASF bots, as found in [`data/asf_bots.json`](data/asf_bots.json).

#### Automatic process

Run the following script to download the list of userIDs of ASF bots:

```bash
python download_bot_listing.py
```

#### Manual process

#### HTML

Alternatively, one could manually download the HTML code from [a public listing of ASF bots](https://asf.justarchi.net/STM).
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

4. Replace the following with `\n`, in order to remove empty lines:
```regexp
\n+
```

#### JSON

Alternatively, one could manually download data as JSON from the [official API for the public listing ASF bots][api-for-asf-bots].

### Find Steam trades

Run the following script to find Steam trades:

```bash
python trade_finder.py
```

The default market appID is `448720` for [Puzzle Box](https://www.steamcardexchange.net/index.php?gamepage-appid-448720).

## References

-   [Wiki: **neutral** Steam trades](https://github.com/JustArchiNET/ArchiSteamFarm/wiki/Trading#steamtradematcher),
-   [Steam Trade Matcher (STM)](https://www.steamtradematcher.com/),
-   [Wiki: automated STM based on ArchiSteamFarm (ASF)](https://github.com/JustArchiNET/ArchiSteamFarm/wiki/Statistics#public-asf-stm-listing),
-   [A public listing of ASF bots](https://asf.justarchi.net/STM).
-   [Official API for the public listing ASF bots][api-for-asf-bots]

<!-- Definitions -->

[build]: <https://github.com/woctezuma/steam-trade-finder/actions>
[build-image]: <https://github.com/woctezuma/steam-trade-finder/workflows/Python package/badge.svg?branch=master>

[pyup]: <https://pyup.io/repos/github/woctezuma/steam-trade-finder/>
[dependency-image]: <https://pyup.io/repos/github/woctezuma/steam-trade-finder/shield.svg>
[python3-image]: <https://pyup.io/repos/github/woctezuma/steam-trade-finder/python-3-shield.svg>

[codecov]: <https://codecov.io/gh/woctezuma/steam-trade-finder>
[codecov-image]: <https://codecov.io/gh/woctezuma/steam-trade-finder/branch/master/graph/badge.svg>

[codacy]: <https://www.codacy.com/app/woctezuma/steam-trade-finder>
[codacy-image]: <https://api.codacy.com/project/badge/Grade/038afb64dd404f8f978ff8ba41b65aef>

[api-for-asf-bots]: <https://asf.justarchi.net/Api/Bots>
