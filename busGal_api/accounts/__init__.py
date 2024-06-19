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

Now, for the XenteNovaQr, here is the most typical use case, generating a QR to pay in the bus:

``` python
from busGal_api import accounts as api
import qrcode
from time import sleep

print("Please login to continue")
tpgal_account = api.Account(input("Email: "), input("Password: "))
xn_account = api.xentenovaqr.Account(tpgal_account.user_id) # This will only work if you have already registered for this service. You do so on the app or using the function for that purpose (not tested nor recommended)

qr_entity = xn_account.create_qr()
qr = qrcode.QRCode()
while True:
    qr.add_data(qr_entity.qr_string)
    print("Scan this code fast, it will refresh in 30s!")
    qr.print_ascii()
    sleep(30)
    qr_entity.refresh_qr_string() # This is done offline
    qr.clear()
```
"""

from ..rest_adapter import RestAdapter as RestAdapter
from ..known_servers import XG_APP as BASE_URL

_rest_adapter = RestAdapter(BASE_URL)

from .accounts import *
from . import xentenovaqr

__all__ = ["accounts", "xentenovaqr"]
