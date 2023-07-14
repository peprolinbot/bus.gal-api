"""
# Introduction

This submodule takes care of accounts and other stuff which requires logging in. This is all reverse-engineered using [mitmproxy](https://mitmproxy.org) and other techniques on the [Android app](https://play.google.com/store/apps/details?id=gal.xunta.transportepublico).

# Quick example

This is just a simple command-line "client" which shows your cards and makes you rename them:

``` python
from busGal_api import accounts as api

print("Please login to continue")
account=api.Account(input("Email: "), input("Password: "))

print("Here are your cards. You are going to rename each of them")
cards=account.get_cards()
for card in cards:
    print(card)
    card.rename(input("New name: "))
```
"""

from ..rest_adapter import RestAdapter as RestAdapter
from ..known_servers import XG_APP as BASE_URL

_rest_adapter = RestAdapter(BASE_URL)

from .accounts import *

__all__ = ["accounts"]
