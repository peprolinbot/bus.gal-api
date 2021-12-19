from ..requests import *
from datetime import datetime

class _Stop():
    """
    Class that represents a bus stop
    """
    def __init__(self, id, name, type, type_id, bus_stop_id=None):
        self.id = id
        """
        Id of the stop

        :type: int
        """

        self.name = name
        """
        name of the stop

        :type: str
        """

        self.type = type
        """
        Type string of the stop . Ex: 'municipality', 'busstop'

        :type: str
        """

        self.type_id = type_id
        """
        Type id of the stop

        :type: int
        """

        self.bus_stop_id = bus_stop_id
        """
        Id the API gives just in expedition details. Idk what it is. It's used to obtain _Expedition.url

        :type: int
        """

class _Operator():
    """
    Class that represents an operator enterprise
    """
    def __init__(self, id, name, type):
        self.id = id
        """
        Id of the operator

        :type: int
        """

        self.name = name
        """
        Name of the operator

        :type: str
        """

        self.type = type
        """
        Type of the operator. Ex: 'group', 'operator'

        :type: str
        """

class _Line():
    """
    Class that represents a bus line
    """

    def __init__(self, id, name):
        self.id = id
        """
        Id of the line

        :type: int
        """

        self.name = name
        """
        Name of the line

        :type: str
        """

class _Expedition():
    """
    Represents any of the expeditions of a Trip. Get's it's own data from dictionary of the json response of api

    :param data: Dictionary corresponding to the expedition in the json response of the API
    :type data: dict

    :param date: Date when the expedition takes place. Just the day matters
    :type date: datetime.datetime

    :param operator: Operator object to make sure the operator property has the right type. If not given will use "operator" type
    :type operator: _Operator
    """

    def __init__(self, data, date, operator=None):

        self.id = data["id"]
        """
        Id of the expedition

        :type: int
        """

        self.code = data["contract_code"]
        """
        Code-name of the expedition

        :type: str
        """

        self.origin = _Stop(data["origin"]["id"], data["origin"]["busstop"], "busstop", 4, data["origin"]["bus_stop_id"])
        """
        Origin stop object

        :type: _Stop
        """

        self.destination = _Stop(data["destination"]["id"], data["destination"]["busstop"], "busstop", 4, data["destination"]["bus_stop_id"])
        """
        Destination stop object

        :type: _Stop
        """

        time = datetime.strptime(data["origin"]["time"], "%H:%M")
        self.departure = datetime(date.year, date.month, date.day, time.hour, time.minute)
        """
        Deaparture time

        :type: datetime.datetime
        """

        time = datetime.strptime(data["destination"]["time"], "%H:%M")
        self.arrival = datetime(date.year, date.month, date.day, time.hour, time.minute)
        """
        Arrival time

        :type: datetime.datetime
        """

        self.line = _Line(id=data["line_id"], name=data["line_name"])
        """
        Bus line object

        :type: _Line
        """

        if operator != None:
            operator_type = operator.type
        else:
            operator_type = "operator"
        self.operator = _Operator(data["operator_id"], data["operator"], operator_type)
        """
        Operator object. Note that if no operator argument was given the type of this will default to "operator"

        :type: _Operator
        """

        self.on_demand = not bool(data["on_demand"])
        """
        Whether th stop works under demand

        :type: bool
        """

        self.url = f"https://www.bus.gal/gl/service/expedition/{self.id}/nojs?ori={self.origin.bus_stop_id}&des={self.destination.bus_stop_id}&date={date.strftime('%Y-%m-%d')}"
        """
        Url on bus.gal for the expedition page

        :type: str
        """


class Trip():
    """
    Trip class. Used for getting results as Expedition objects

    :param origin: Origin stop
    :type origin: _Stop

    :param destination: Destination stop
    :type destination: _Stop

    :param date: The date the trip will take place. Just the day matters
    :type date: datetime.datetime

    :param operator: The operator that you would like to own the buses
    :type operator: _Operator
    """

    def __init__(self, origin, destination, date, operator=None):
        self.origin = origin
        """
        Origin stop

        :type: _Stop
        """

        self.destination = destination
        """
        Destination stop

        :type: _Stop
        """
        self.date = date

        self.expeditions = self._get_expeditions_from_api(origin, destination, date, operator)
        """
        List of avaliable expeditions

        :type: list[_Expedition]
        """


    def _get_expeditions_from_api(self, origin, destination, date, operator):
        """
        Obtains all the expeditions from the app API. Called on creation

        :return: List of avaliable expeditions
        :rtype: list[_Expedition]
        """
        date_timestamp = int(datetime(date.year, date.month, date.day).timestamp()) * 1000 #It's multiplied by 1000 to add extra precision the API needs

        url = f"https://tpgal-ws.xunta.gal/tpgal_ws/rest/service/search?origin_id={origin.id}&destination_id={destination.id}&origin_type={origin.type}&destination_type={destination.type}&date={date_timestamp}&departure_time={date_timestamp}&page_number=1&page_size=2147483647"
        json = make_get_request(url)["results"]

        expeditions = []
        for expedition in json:
            if operator != None:
                expeditions.append(_Expedition(expedition, date, operator))
            else:
                expeditions.append(_Expedition(expedition, date))

        return expeditions

def get_stops():
    """
    Gets all the existing stops

    :return: List of all stops
    :rtype: list[_Stop]
    """
    url = "https://tpgal-ws.xunta.gal/tpgal_ws/rest/busstops/autocomplete?text&num_results=2147483647"
    json = make_get_request(url)["results"]
    results = []
    for stop in json:
        results.append(_Stop(stop["id"], stop["text"], stop["type"], stop["group_type"]))

    return results

def search_stop(name):
    """
    Searchs for stops with the specified name, using the app's search api

    :param name: Search query
    :type name: str

    :return: List of stop results
    :rtype: list[_Stop]
    """
    url = f"https://tpgal-ws.xunta.gal/tpgal_ws/rest/busstops/autocomplete?text={name}&num_results=2147483647"
    json = make_get_request(url)["results"]
    results = []
    for stop in json:
        results.append(_Stop(stop["id"], stop["text"], stop["type"], stop["group_type"]))

    return results

def get_operators():
    """
    Gets all the existing operators

    :return: List of all operators
    :rtype: list[_Operator]
    """
    url = "https://tpgal-ws.xunta.gal/tpgal_ws/rest/operators/autocomplete?text&num_results=2147483647"
    json = make_get_request(url)["results"]
    results = []
    for operator in json:
        results.append(_Operator(operator["id"], operator["text"], operator["type"]))
    return results

def search_operator(name):
    """
    Searchs for operators with the specified name, using the app's search api

    :param name: Search query
    :type name: str

    :return: List of operator results
    :rtype: list[_Operator]
    """
    url = f"https://tpgal-ws.xunta.gal/tpgal_ws/rest/operators/autocomplete?text={name}&num_results=2147483647"
    json = make_get_request(url)["results"]
    results = []
    for operator in json:
        results.append(_Operator(operator["id"], operator["text"], operator["type"]))
    return results
