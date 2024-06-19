# bus.gal-api 🚍

[![GitHub license](https://img.shields.io/github/license/peprolinbot/bus.gal-api)](https://github.com/peprolinbot/bus.gal-api)
[![PyPI version](https://img.shields.io/pypi/v/busGal-api?label=pypi%20package)](https://pypi.org/project/busGal-api)
[![Upload Python Package](https://github.com/peprolinbot/bus.gal-api/actions/workflows/python-publish.yml/badge.svg)](https://github.com/peprolinbot/bus.gal-api/actions/workflows/python-publish.yml)

Python API wrapper for [the galician public transport](https://www.bus.gal/) which uses the
associated
[app](https://play.google.com/store/apps/details?id=gal.xunta.transportepublico)'s
http API to get the inforamtion about buses, your card and your user
account. I got the endpoints using [mitmproxy](https://mitmproxy.org/).

## 📜 Documentation

Documentation can be found [here](https://peprolinbot.github.io/bus.gal-api). There are two main submodules: `busGal_api.transport` and `busGal_api.accounts`, the first one has all the functions related to transportation and the second one allows you to manage cards and accounts, as the name implies.

## 🔧 Installation

Just run:

``` bash
pip install busGal_api
```

## ✅ Quick examples

There are quick examples for both the submodules mentioned above in their `__main__.py` and their docs.

## ⚠️ Disclaimer

This project is not endorsed by, directly affiliated with, maintained
by, sponsored by or in any way officially related with la Xunta de
Galicia, the bus operators or any of the companies involved in the
[bus.gal](https://www.bus.gal/) website and the
[app](https://play.google.com/store/apps/details?id=gal.xunta.transportepublico).

This software is provided 'as is' without any warranty of any kind. The user of this software assumes all responsibility and risk for its use. I shall not be liable for any damages or misuse of this software. Please use the code and information in this repo responsibly.
