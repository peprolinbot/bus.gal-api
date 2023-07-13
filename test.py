from busGal_api import transport as api
from datetime import date

NUM_RESULTS=8

def stop_search_menu(prompt):
    query = input(prompt)
    results = api.stops.search_stops(query=query, num_results=NUM_RESULTS)

    for i, result in enumerate(results):
        print(f"{i} -- {result.name}")

    selection = int(input("Which number do you want? >>>"))

    return results[selection]

origin = api.stops.search_stops(query="Ferrol", num_results=2)[1]#stop_search_menu("Where do you want to start your trip? >>> ")
destination = api.stops.search_stops(query="ares", num_results=2)[1]#stop_search_menu("And where do you want to go? >>> ")

expeditions = api.trips.search_expeditions(origin=origin, destination=destination, date=date.today())

if expeditions == None:
    print("No results")
    exit()

print("\nORIGIN  |  DEPARTURE  |  DESTINATION  |  ARRIVAL\n")
for expedition in expeditions:
    print(expedition)