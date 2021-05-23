from utils.requests_handler import *

class _Stop():
    def __init__(self, id, name, type, type_id):
        self.id = id
        self.name = name
        self.type = type
        self.type_id = type_id

class _Operator():
    def __init__(self, id, name, type):
        self.id = id
        self.name = name
        self.type = type

def get_stops():
    url = "https://www.bus.gal/gl/service/autocomplete/busstop"
    json = make_get_request(url)
    results = []
    for stop in json:
        results.append(_Stop(stop["id"], stop["value"], stop["type"], stop["group_type"]))
    return results

def search_stop(name):
    url = f"https://www.bus.gal/gl/service/autocomplete/busstop?text={name}"
    json = make_get_request(url)
    results = []
    for stop in json:
        results.append(_Stop(stop["id"], stop["value"], stop["type"], stop["group_type"]))
    return results

def get_operators():
    url = "https://www.bus.gal/gl/service/autocomplete/operator"
    json = make_get_request(url)
    results = []
    for operator in json:
        results.append(_Operator(operator["id"], operator["value"], operator["type"]))
    return results

def search_operator(name):
    url = f"https://www.bus.gal/gl/service/autocomplete/operator?text={name}"
    json = make_get_request(url)
    results = []
    for operator in json:
        results.append(_Operator(operator["id"], operator["value"], operator["type"]))
    return results
