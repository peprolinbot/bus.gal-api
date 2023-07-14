from . import _rest_adapter
from .stops import Stop


## vvv Classes vvv ##

class Line():
    """
    A bus line
    """

    def __init__(self, id: int, name: str, origin: Stop = None, destination: Stop = None, code: str = None, number: str = None):
        self.id = id
        """
        Id of the line
        """

        self.name = name
        """
        Name of the line
        """

        self.origin = origin
        """
        Origin stop
        """

        self.destination = destination
        """
        Destination stop
        """

        self.code = code
        """
        Line's code the API gives only in expedition details. Again, no idea of its purpose
        """

        self.number = number
        """
        Line's number, only given in `busGal_api.transport.trips.get_expeditions_from_stop`
        """

    def __repr__(self):
        return self.name

## ^^^ Classes ^^^ ##


## vvv Methods vvv ##

def _parse_stop(data: dict) -> Stop:
    """
    Builds a stop based on the data given by the API. Nothe this is specific to the lines endpoints, e.g. the "nome" attribute
    """

    # Only busstops are posible as a line's origin or destination, kinda obvious
    return Stop(id=data["id"],
                type="busstop",
                name=data["nome"],
                lat=data.get("latitude"),
                long=data.get("longitude"))


def _parse_line(data: dict) -> Line:
    """
    Builds a line based on the data given by the API
    """

    origin = None
    destination = None
    origin_data = data.get("origin")
    destination_data = data.get("destination")
    if origin_data and destination_data:
        origin = _parse_stop(origin_data)
        destination = _parse_stop(destination_data)

    return Line(id=data["id"],
                name=data["line_name"],
                origin=origin,
                destination=destination)


def search_lines_from_stop(stop_id: int, page_number: int = 1, page_size: int = 2147483647) -> list[Line]:
    """
    Based on a stop id, obtains all the lines that go through it. **WARNING**: The API seems to have deprecated this, almost-always returns an empty list, again `15004` works, check `busGal_api.transport.stops.get_stop_name`

    :param page_number: The page number to retrieve. Defaults to the first one.

    :param page_size: Number of results per page. Defaults to the maximum integer value the API would accept, a.k.a. the maximum positive value for a 32-bit signed binary integer (Wikipedia), a.k.a. 2,147,483,647
    """

    data = _rest_adapter.get("/lines/search",
                            ep_params={"stop_id": stop_id,
                                       "page_number": page_number,
                                       "page_size": page_size})

    # Last element in list is total_results
    return [_parse_line(el) for el in data[:-1]]


def concession_search_lines(operator_id: int = None, contract_code: str = None, provincial_service: int = None) -> list[Line]:
    """
    Get lines filtering by operator, contract and provincial service id
    """

    data = _rest_adapter.get("/lines",
                            ep_params={"operator_id": operator_id,
                                       "contract_code": contract_code,
                                       "provincial_service": provincial_service})

    return [Line(id=el["id"],
                 name=el["line_name"])
            for el in data]


def get_all_lines():
    """
    Gets all the existing lines (calls `concession_search_lines` with no filters)
    """

    return concession_search_lines()


def get_line(line_id: int) -> Line:
    """
    Fetch a line with it's id. **WARNING**: The API seems to have deprecated this (kind-of), 
    it just keeps saying we're missing `X-CSRF-TOKEN` header, which hints to a form to check this somewhere, 
    but I'm tired and I don't want to play that game
    """

    return _parse_line(_rest_adapter.get("/lines/private/get",
                                        ep_params={"line_id": line_id}))

## ^^^ Methods ^^^ ##
