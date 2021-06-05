bus.gal-api
===========


.. image:: https://img.shields.io/pypi/l/busgal-api
   :target: https://pypi.org/project/busGal-api
   :alt: PyPi License
 
.. image:: https://img.shields.io/pypi/v/busGal-api?label=pypi%20package
   :target: https://pypi.org/project/busGal-api
   :alt: PyPI version


Python API wrapper for bus.gal which uses the associated app's http API to get the inforamtion. I got the endpoints using mitmproxy

There is also included an old implementation using selenium, which isn't included in the package, it's in busdotg

Documentation
-------------
Documentation can be found in https://busgal-api.readthedocs.io/en/latest/

Installation
------------

Just run:

.. code-block::

   pip install busGal_api

Quick example
-------------

This is just a simple command-line "client"

.. code-block::

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

Free **TechTip** for you: Set the ``MOZ_HEADLESS`` env bar to anything for this to run Firefox in headless mode.
