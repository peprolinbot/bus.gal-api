from . import _rest_adapter

from .stops import Stop
from .lines import Line
from .operators import Operator, Contract, _parse_operator
from .warning_alerts import WarningAlert, _parse_warning
from .rates import SpecialRate, _parse_special_rate

from datetime import date, datetime
from time import mktime


## vvv Classes vvv ##

class Route():
    """
    An expedition's route
    """

    def __init__(self, code: str, name: str):
        self.code = code
        """
        The code for the route
        """

        self.name = name
        """
        The name of the route
        """

    def __repr__(self):
        return f"{self.code} - {self.name}"


class Expedition():
    """
    An expedition
    """

    def __init__(self, id: int, name: str, origin: Stop, destination: Stop, line: Line, operator: Operator, week_frequency: str, anual_frequency: str, on_demand: bool, school_integration: bool, code: str = None, passing_stop: Stop = None, passing_time: datetime = None, contract: Contract = None, warnings: list[WarningAlert] = None, special_rates: list[SpecialRate] = None, route: Route = None, direction: str = None, school_seats: int = None, on_demand_seats: int = None, reservable_seats: int = None, duration: int = None, bus_stops: list[Stop] = None, polyline: dict = None):

        self.id = id
        """
        Id of the expedition
        """

        self.name = name
        """
        Name of the expedition
        """

        self.origin = origin
        """
        Origin stop
        """

        self.destination = destination
        """
        Destination stop
        """

        self.line = line
        """
        The `busGal_api.transport.lines.Line` this expedition uses
        """

        self.operator = operator
        """
        The `busGal_api.transport.operators.Operator` which owns this expedition
        """

        self.week_frequency = week_frequency
        """
        The weekly frequency of this expedition
        """

        self.anual_frequency = anual_frequency
        """
        The anual frequency of this expedition
        """

        self.on_demand = bool(on_demand)
        """
        Whether the stop works under demand
        """

        self.school_integration = bool(school_integration)
        """
        Whether the stop has school integration
        """

        self.code = code
        """
        Code-name of the expedition
        """

        self.passing_stop = passing_stop
        """
        Passing stop at the stop given in `get_expeditions_from_stop`
        """

        self.passing_time = passing_time
        """
        Passing time at the stop given in `get_expeditions_from_stop`
        """

        self.contract = contract
        """
        `busGal_api.transport.operators.Contract` for the expedition
        """

        self.warnings = warnings
        """
        `busGal_api.transport.warning_alerts.WarningAlert`s for this expedition
        """

        self.special_rates = special_rates
        """
        `SpecialRate`s for this expedition
        """

        self.route = route
        """
        `Route` for this expedition
        """

        self.direction = direction
        """
        Direction of the expedition. Only given in `get_expeditions_from_stop`
        """

        self.school_seats = school_seats
        """
        The amount of seats reserved for scholars
        """

        self.ondemand_seats = on_demand_seats
        """
        The amount of seats that work on demand
        """

        self.reservable_seats = reservable_seats
        """
        The amount of seats that are reservable
        """

        self.duration = duration
        """
        Duration of the expedition
        """

        self.bus_stops = bus_stops
        """
        The stops the expedition goes trough. Only given in `get_expedition_details`
        """

        self.polyline = polyline
        """
        It represents stops the expedition goes trough in a special format. Only given in `get_expedition_details`
        """

        self.bus_dot_gal_url = f"https://www.bus.gal/gl/service/expedition/{self.id}/nojs?ori={self.origin.bus_stop_id}&des={self.destination.bus_stop_id}&date={self.origin.time.strftime('%Y-%m-%d')}"
        """
        Url on bus.gal for the expedition's details page. Shows it's itinerary and looks good, so I put it in here
        """

    def __repr__(self):
        return f"{self.origin}  |  {self.origin.time.strftime('%H:%M')}  --->  {self.destination}  |  {self.destination.time.strftime('%H:%M')}"

## ^^^ Classes ^^^ ##


## vvv Methods vvv ##

def _parse_stop(data: dict) -> Stop:
    # Only busstops are posible
    return Stop(id=data["id"],
                type="busstop",
                name=data["busstop"],
                bus_stop_id=data["bus_stop_id"],
                bus_stop_code=data.get("bus_stop_code"),
                on_demand=data["on_demand"],
                school_integration=data["school_integration"],
                ordinal=data["ordinal"],
                lat=data.get("latitude"),
                long=data.get("longitude"),
                time=datetime.strptime(data["time"], "%H:%M"))


def _parse_expedition(data: dict) -> Expedition:
    return Expedition(id=data["id"],
                      name=data["expedition_name"],
                      origin=_parse_stop(data["origin"]),
                      destination=_parse_stop(data["destination"]),
                      line=Line(id=data.get("line_id"),
                                name=data.get("line_name"),
                                code=data.get("line_code")),
                      operator=Operator(id=data["operator_id"],
                                        name=data["operator"],
                                        emails=data.get("emails")),
                      week_frequency=data.get("week_frequency"),
                      anual_frequency=data.get("anual_frequency"),
                      on_demand=data.get("on_demand"),
                      school_integration=data.get("school_integration"),
                      code=data.get("expedition_code"),
                      warnings=[_parse_warning(
                          w) for w in data["warnings"]] if data.get("warnings") else None,
                      special_rates=[_parse_special_rate(
                          sr) for sr in data["special_rates"]] if data.get("special_rates") else None,
                      contract=Contract(
                          code=data.get("contract_code"),
                          name=data.get("contract_name")) if data.get("contract_code") or data.get("contract_name") else None,
                      route=Route(code=data.get("route_code"),
                                  name=data.get("route_name")) if data.get(
                          "route_name") or data.get("route_code") else None,
                      duration=data.get("duration"),
                      school_seats=data.get("school_seats"),
                      on_demand_seats=data.get("ondemand_seats"),
                      reservable_seats=data.get("reservable_seats"),
                      bus_stops=[_parse_stop(s) for s in data["busstops"]] if data.get(
                          "busstops") else None,
                      polyline=data.get("saepolyline"))


def search_expeditions(origin: Stop, destination: Stop, date: date, on_demand: bool = None, operator: Operator = None, expedition_id: int = None, page_number: int = 1, page_size: int = 2147483647, departure_time: datetime = None, discount_id: int = None) -> list[Expedition]:
    """
    Obtains all the expeditions from the app API. Called on creation

    :param origin: Origin stop

    :param destination: Destination stop

    :param date: The date for the trip

    :param on_demand: If `True`, shows only on demand services; if `False`, only regular ones

    :param operator: The operator that you would like to own the expeditions

    :param expedition_id: Id of an expedition

    :param page_number: The number of the page to return

    :param page_size: How many expeditions to return per page. The default is the maximum integer the api would accept (2147483647)

    :param departure_time: The time at wich the trip should start

    :param discount_id: Id of a discount you'd want to apply
    """

    # Timestamps are multiplied by 1000 because the API wants miliseconds
    data = _rest_adapter.get("/service/search",
                             ep_params={'origin_id': origin.id,
                                        'origin_type': origin.type,
                                        'destination_id': destination.id,
                                        'destination_type': destination.type,
                                        'date': int(mktime(date.timetuple())) * 1000,
                                        'type_service': int(on_demand)+1 if on_demand else None,
                                        'operator_id': operator.id if operator else None,
                                        'operator_id': operator.type if operator else None,
                                        'expedition_id': expedition_id,
                                        'page_number': page_number,
                                        'page_size': page_size,
                                        'departure_time': departure_time.timestamp()*1000 if departure_time else None,
                                        'discount_id': discount_id})

    return [_parse_expedition(el) for el in data]


def get_expedition(expedition_id: int) -> Expedition:
    """
    Obtains the details of an expedition.

    :param expedition_id: The expedition id
    """

    data = _rest_adapter.get("/service/detail",
                             ep_params={"id": expedition_id})

    return _parse_expedition(data)


def get_expeditions_from_stop(stop_id: int, departure_time: datetime) -> list[Expedition]:
    """
    Based on a stop id, obtains all the expeditions that go through it

    :param stop_id: The stop id

    :param datetime: The date and time for the trip
    """

    data = _rest_adapter.get("/public/expedition/from",
                             ep_params={"stopId": stop_id,
                                        "tripDate": departure_time.strftime("%d/%m/%Y %H:%M")})

    def _parse_stop(data: dict) -> Stop:
        # Only busstops are posible
        return Stop(id=data["stop_id"],
                    type="busstop",
                    name=data["stop_name"],
                    town_name=data["town_name"],
                    bus_stop_id=data.get("line_stop_id"),
                    sitme_id=data.get("id_sitme"),
                    on_demand=data["on_demand"],
                    school_integration=data["scholar"],
                    time=datetime.strptime(data["departure_time"], "%H:%M"))

    def _parse_expedition(data: dict) -> Expedition:
        return Expedition(id=data["expedition_id"],
                          name=data["expedition_name"],
                          origin=_parse_stop(data["origin_line_stop"]),
                          destination=_parse_stop(
                              data["destination_line_stop"]),
                          line=Line(id=data.get("line_id"),
                                    name=data.get("line_name"),
                                    number=data.get("line_number")),
                          operator=_parse_operator(data["operator"]),
                          contract=Contract(
                              code=data.get("contract_code")),
                          week_frequency=data.get("week_frecuency"),
                          anual_frequency=data.get("week_frecuency"),
                          on_demand=data.get("on_demand"),
                          school_integration=data.get("scholar"),
                          passing_stop=Stop(id=data["stop_id"],
                                            type="busstop",  # Obviously
                                            name=data.get("stop_name")),
                          passing_time=datetime.strptime(
                              data["passing_time"], "%H:%M"),
                          direction=data.get("direction"))

    return [_parse_expedition(el) for el in data]

## ^^^ Methods ^^^ ##
