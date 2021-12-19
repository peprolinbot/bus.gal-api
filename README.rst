bus.gal-api
===========


.. image:: https://img.shields.io/github/license/peprolinbot/bus.gal-api
   :target: https://github.com/peprolinbot/bus.gal-api
   :alt: GitHub license

.. image:: https://img.shields.io/pypi/v/busGal-api?label=pypi%20package
   :target: https://pypi.org/project/busGal-api
   :alt: PyPI version

.. image:: https://github.com/peprolinbot/bus.gal-api/actions/workflows/python-publish.yml/badge.svg
   :target: https://github.com/peprolinbot/bus.gal-api/actions/workflows/python-publish.yml
   :alt: Upload Python Package


Python API wrapper for bus.gal_ which uses the associated app_'s http API to get the inforamtion about buses, your card and your user account. I got the endpoints using mitmproxy_

.. _bus.gal: https://www.bus.gal/
.. _app: https://play.google.com/store/apps/details?id=gal.xunta.transportepublico
.. _mitmproxy: https://mitmproxy.org/

Documentation
-------------
Documentation can be found `here <https://busgal-api.readthedocs.io/en/latest/>`_

Installation
------------

Just run:

.. code-block:: bash

   pip install busGal_api

Quick example
-------------

This is just a simple command-line "client"

.. code-block:: python

   import busGal_api as api
   from datetime import datetime

   def menu(results):
       for i, result in enumerate(results):
           print(f"{i} -- {result.name}")

       return int(input("Which number you want? >>>"))

   origin = input("Where do you want to start your trip? >>>")
   results = api.search_stop(origin)
   selection = menu(results)
   origin = results[selection]

   destination = input("Where do you want to go? >>>")
   results = api.search_stop(destination)
   selection = menu(results)
   destination = results[selection]

   trip = api.Trip(origin, destination, datetime.now())

   if trip.expeditions == None:
       print("No results")
       exit()

   print("\nORIGIN  |  DEPARTURE  |  DESTINATION  |  ARRIVAL\n")
   for expedition in trip.expeditions:
       print(f"{expedition.origin.name}  |  {expedition.departure.strftime('%H:%M')}  |  {expedition.destination.name}  |  {expedition.arrival.strftime('%H:%M')}")


Disclaimer
----------

This project is not endorsed by, directly affiliated with, maintained by, sponsored by or in any way officially related with la Xunta de Galicia, the bus operators or any of the companies involved in the bus.gal_ website and the app_.
