import busGal_api as api
import difflib

stops = api.search_stop("ferrol")
names = [stop.name.split("(")[0][:-1] for stop in stops]

equivalent_stops={}
for i, name in enumerate(names):
    current_stop = stops[i]
    print(f"\n---- {current_stop.name} ----")

    _stops = []
    for i, name in enumerate(difflib.get_close_matches(name, names, 6)[1:]):
        stop = stops[names.index(name)]
        _stops.append(stop)

        print(f"{i} -- {stop.name}")

    if _stops != []:
        selection = input("Select if similar >>> ")
        try:
            selection = int(selection)
            equivalent_stops[current_stop.id] = _stops[int(selection)].id
        except ValueError:
            pass
        print(equivalent_stops)
    

    


