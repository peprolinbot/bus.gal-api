"""
# Introduction

This submodule takes care of transport. The endpoints used here have an official documentation [here](https://ficheiros-web.xunta.gal/abertos/manuais/TPGAL-WS-Externos-MU-guiaConsumoServizos.pdf), altough it's a really poor one. Keep in mind some names and structures have been modified to be more comprehensible (at least in my opinion).

# Quick example

This is just a simple command-line "client" which shows the transport submodule in action by showing a simple timetable for the buses of the trip you specify:

``` python
.. include:: __main__.py
```

This is also this submodule's `__main__.py`, therefore you can `python -m busGal_api.transport` to try it out
"""

from ..rest_adapter import RestAdapter as RestAdapter
from ..known_servers import XG_APP as BASE_URL

_rest_adapter = RestAdapter(BASE_URL)


from . import lines
from . import stops
from . import operators
from . import expeditions
from . import warning_alerts
from . import rates

__all__ = ["lines", "stops", "operators", "expeditions", "warning_alerts", "rates"]
