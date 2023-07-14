from busGal_api import transport as api
from datetime import date, datetime

NUM_RESULTS=8

def stop_search_menu(prompt):
    query = input(prompt)
    results = api.stops.search_stops(query=query, num_results=NUM_RESULTS)

    for i, result in enumerate(results):
        print(f"{i} -- {result.name}")

    selection = int(input("Which number do you want? >>> "))

    return results[selection]

origin = stop_search_menu("Where do you want to start your trip? >>> ")
destination = stop_search_menu("And where do you want to go? >>> ")

date_str = input("And when? (dd-mm-yy) (defaults to today) >>> ")
date = datetime.strptime(date_str, "%d-%m-%Y") if date_str else date.today()

expeditions = api.expeditions.search_expeditions(origin=origin, destination=destination, date=date)

if expeditions == None:
    print("No results")
    exit()

print("\nORIGIN  |  DEPARTURE  |  DESTINATION  |  ARRIVAL\n")
for expedition in expeditions:
    print(expedition)