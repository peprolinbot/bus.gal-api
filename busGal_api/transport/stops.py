from . import _rest_adapter

from datetime import datetime


## vvv Classes vvv ##

class Location():
    """
    A location (latitude and longitude)
    """

    def __init__(self, lat: float, long: float):
        self.lat = float(lat)
        """
        Latitude
        """

        self.long = float(long)
        """
        Longitude
        """

    def __repr__(self):
        return f"Lat: {self.lat}, Long: {self.long}"


class Stop():
    """
    A bus stop (municipalities are also considered stops)
    """

    def __init__(self, id: int, type: str, name: str = None, group_type: int = None, location: Location = None, lat: float = None, long: float = None, on_demand: bool = None, school_integration: bool = None, ordinal: int = None, bus_stop_id: int = None, bus_stop_code: str = None, sitme_id: int = None, town_name: str = None, time: datetime = None):
        self.id = id
        """
        Id of the stop. These aren't actually unique, as i've found them changing from time to time
        """

        self.type = type
        """
        What kind of stop this is (`busstop`/`municipality`)
        """

        self.name = name
        """
        Name of the stop
        """

        self.group_type = group_type
        """
        Group of results to which the stop belongs: 
        - 1: City council
        - 2: Main stops of the city council/s that coincide with the text of search
        - 3: Non-main stops of the city council
        - 4: Stops matching the text entered, but from other city councils.
        """

        self.location = location or (
            Location(lat, long) if lat and long else None)
        """
        Location of the stop
        """

        self.on_demand = bool(on_demand)
        """
        Whether the stop works on demand
        """

        self.school_integration = bool(school_integration)
        """
        Whether the stop has school integration
        """

        self.ordinal = ordinal
        """
        Not sure, I guess it indicates some kind of order
        """

        self.bus_stop_id = bus_stop_id
        """
        Id the API gives only in expedition details. Idk what it represents, but it's not the same across expeditions (of different lines)
        """

        self.bus_stop_code = bus_stop_code
        """
        Code the API gives only in expedition details. Again, no idea of its purpose
        """

        self.sitme_id = sitme_id
        """
        Given in `location_search_stops`. Used for real-time
        """

        self.town_name = town_name
        """
        Given in `busGal_api.transport.trips.get_expeditions_from_stop`
        """

        self.time = time
        """
        Indicates the time at wich the bus goes trough the stop during an expedition
        """

    def fetch_name(self) -> str:
        """
        Fetch the name (and set it) for this stop id from the API
        """

        self.name = get_stop_name(self.id)

        return self.name

    def fetch_location(self) -> Location:
        """
        Fetch the location (and set it) for this stop id from the API
        """

        self.location = get_stop_location(self.id)

        return self.location

    def __repr__(self):
        return self.name

## ^^^ Classes ^^^ ##


## vvv Methods vvv ##

def _parse_stop_search_results(data: dict, type: str = "busstop") -> list[Stop]:
    """
    Helper function to parse the JSON data (already parsed into a Python dict) returned by the API from either `location_searc_stop` or `search_stop` into a list of Stop objects

    :param data: API results, parsed from JSON

    :param type: Type to assign to stops which don't have it in the results. Defaults to busstop
    """

    stops = []
    for el in data:
        stop = Stop(id=el["id"], type=el.get("type", type),
                    name=el["text"], group_type=el.get("group_type"))  # group_type not specified in location-based search results, neither when getting all councils
        try:
            location = el["location"]
            stop.location = Location(
                location["latitude"], location["longitude"])
        except KeyError:
            pass

        stops.append(stop)

    return stops


def search_stops(query: str, councils: bool = True, num_results: int = 2147483647) -> list[Stop]:
    """
    Searchs for stops with the specified name, using the app's search API, which is actually meant for autocomplete

    :param query: Search query

    :param councils: Whether to show council/municipality stops. By default, it does. Note that disabling this queries a different endpoint

    :param num_results: Number of results to return. Defaults to the maximum integer value the API would accept, a.k.a. the maximum positive value for a 32-bit signed binary integer, a.k.a. 2,147,483,647
    """

    if councils:
        endpoint = "/busstops/autocomplete"
    else:
        endpoint = "/busstops/autocomplete-only-busstops"

    return _parse_stop_search_results(_rest_adapter.get(endpoint,
                                                        ep_params={"text": query,
                                                                   "num_results": num_results}))


def get_all_stops(councils: bool = True) -> list[Stop]:
    """
    Gets all the existing stops (calls `search_stops` with an empty query)

    :param councils: Whether to show council/municipality stops. By default, it does. Note that disabling this queries a different endpoint
    """

    return search_stops(query='', councils=councils)


def get_all_councils() -> list[Stop]:
    """
    Gets all the existing councils
    """
    return _parse_stop_search_results(_rest_adapter.get("/municipalities"))


def location_search_stops(location: Location = None, lat: float = None, long: float = None, radius=5) -> list[Stop]:
    """
    Searchs for stops within a given radius of a geographic point. You must either provide `location` or both `lat` & `long`. Note that if you give a `Location` object, it will be unpacked anyway.

    :param radius: Radius (in kilometers) for the search. Defaults to `5`
    """

    # Required arguments logic (either location or both lat & long)
    if location:
        lat = location.lat
        long = location.long
    else:
        if not (lat and long):
            raise TypeError(
                "location_search_stops() expected either the 'location' or both the 'lat' and 'long' arguments")

    return _parse_stop_search_results(_rest_adapter.get("/busstops/in-range",
                                                        ep_params={"latitude": lat,
                                                                   "longitude": long,
                                                                   "range": radius}))


def get_stop_name(stop_id: int, alternative: bool = True) -> str:
    """
    Fetch the name of a stop. **WARNING**: The API seems to have deprecated this somehow; altough I got it to work when trying random ids with `15004`, but the returned name is wrong; therefore I made a hacky alternative to fetch a stop's name, based on `busGal_api.transport.trips.get_expeditions_from_stop`

    :param alternative: Whether to use the alternative, hacky, but working ;) method (it does by default)
    """

    if alternative:
        data = _rest_adapter.get("/public/expedition/from",
                                 ep_params={"stopId": stop_id,
                                            "tripDate": datetime.now().strftime("%d/%m/%Y %H:%M")})

        return data[0]["stop_name"]

    return _rest_adapter.get("/busstops/get",
                             ep_params={"stop_id": stop_id})


def get_stop_location(stop_id: int) -> Location:
    """
    Fetch the location of a stop. **WARNING**: The API seems to have deprecated this. Same problem as `get_stop_name`
    """

    data = _rest_adapter.get("/busstops/busstop-location",
                             ep_params={"id": stop_id})

    return Location(data["latitude"], data["longitude"])

## ^^^ Methods ^^^ ##
