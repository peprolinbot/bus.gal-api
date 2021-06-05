import requests
import json

def _make_get_request(url):
    """
    Makes a get request using normal browser headers

    :return: Dictionary made from the request's json
    :rtype: dict
    """
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'}
    r = requests.get(url , headers=headers)
    if r.status_code == 200:
        return r.json()
    else:
        raise Exception("There was an error in the request: Code " + str(r.status_code))

class _Stop():
    """
    Class that represents a bus stop
    """
    def __init__(self, id, name, type, type_id):
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

def get_stops():
    """
    Gets all the existing stops

    :return: List of all stops
    :rtype: list[_Stop]
    """
    url = "https://www.bus.gal/gl/service/autocomplete/busstop"
    json = _make_get_request(url)
    results = []
    for stop in json:
        results.append(_Stop(stop["id"], stop["value"], stop["type"], stop["group_type"]))
    return results

def search_stop(name):
    """
    Searchs for stops with the specified name, using bus.gal's search api
    
    :param name: Search query
    :type name: str

    :return: List of stop results
    :rtype: list[_Stop]
    """
    url = f"https://www.bus.gal/gl/service/autocomplete/busstop?text={name}"
    json = _make_get_request(url)
    results = []
    for stop in json:
        results.append(_Stop(stop["id"], stop["value"], stop["type"], stop["group_type"]))
    
    return results

def get_operators():
    """
    Gets all the existing operators

    :return: List of all operators
    :rtype: list[_Operator]
    """
    url = "https://www.bus.gal/gl/service/autocomplete/operator"
    json = _make_get_request(url)
    results = []
    for operator in json:
        results.append(_Operator(operator["id"], operator["value"], operator["type"]))
    return results

def search_operator(name):
    """
    Searchs for operators with the specified name, using bus.gal's search api
        
    :param name: Search query
    :type name: str

    :return: List of operator results
    :rtype: list[_Operator]
    """
    url = f"https://www.bus.gal/gl/service/autocomplete/operator?text={name}"
    json = _make_get_request(url)
    results = []
    for operator in json:
        results.append(_Operator(operator["id"], operator["value"], operator["type"]))
    return results
