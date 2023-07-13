# bus.gal-api

[![GitHub license](https://img.shields.io/github/license/peprolinbot/bus.gal-api)](https://github.com/peprolinbot/bus.gal-api)

[![PyPI version](https://img.shields.io/pypi/v/busGal-api?label=pypi%20package)](https://pypi.org/project/busGal-api)

[![Upload Python Package](https://github.com/peprolinbot/bus.gal-api/actions/workflows/python-publish.yml/badge.svg)](https://github.com/peprolinbot/bus.gal-api/actions/workflows/python-publish.yml)

Python API wrapper for [bus.gal](https://www.bus.gal/) which uses the
associated
[app](https://play.google.com/store/apps/details?id=gal.xunta.transportepublico)'s
http API to get the inforamtion about buses, your card and your user
account. I got the endpoints using [mitmproxy](https://mitmproxy.org/).

## Documentation

Documentation can be found [here](CHANGEMEYOUMORON). There are two main submodules: transport and accounts, the first one has all the functions related to transportation and the second one allows you to manage cards and accounts, as the name implies.

## Installation

Just run:

``` bash
pip install busGal_api
```

## Quick example

This is just a simple command-line "client" which shows the transport submodule in action

``` python
from busGal_api import buses as api
from datetime import date

NUM_RESULTS=8

def stop_search_menu(prompt):
    query = input(prompt)
    results = api.search_stops(query=query, num_results=NUM_RESULTS)

    for i, result in enumerate(results):
        print(f"{i} -- {result.name}")

    selection = int(input("Which number do you want? >>>"))

    return results[selection]

origin = stop_search_menu("Where do you want to start your trip? >>> ")
destination = stop_search_menu("And where do you want to go? >>> ")

expeditions = api.search_expeditions(origin=origin, destination=destination, date=date.today())

if expeditions == None:
    print("No results")
    exit()

print("\nORIGIN  |  DEPARTURE  |  DESTINATION  |  ARRIVAL\n")
for expedition in expeditions:
    print(expedition)
```

## Disclaimer

This project is not endorsed by, directly affiliated with, maintained
by, sponsored by or in any way officially related with la Xunta de
Galicia, the bus operators or any of the companies involved in the
[bus.gal](https://www.bus.gal/) website and the
[app](https://play.google.com/store/apps/details?id=gal.xunta.transportepublico).
