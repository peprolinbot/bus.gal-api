import requests
import json

def _make_get_request(url):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'}
    r = requests.get(url , headers=headers)
    if r.status_code == 200:
        return r.json()
    else:
        raise RequestException("There was an error in the request: Code " + str(r.status_code))

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
    json = _make_get_request(url)
    results = []
    for stop in json:
        results.append(_Stop(stop["id"], stop["value"], stop["type"], stop["group_type"]))
    return results

def search_stop(name):
    url = f"https://www.bus.gal/gl/service/autocomplete/busstop?text={name}"
    json = _make_get_request(url)
    results = []
    for stop in json:
        results.append(_Stop(stop["id"], stop["value"], stop["type"], stop["group_type"]))
    return results

def get_operators():
    url = "https://www.bus.gal/gl/service/autocomplete/operator"
    json = _make_get_request(url)
    results = []
    for operator in json:
        results.append(_Operator(operator["id"], operator["value"], operator["type"]))
    return results

def search_operator(name):
    url = f"https://www.bus.gal/gl/service/autocomplete/operator?text={name}"
    json = _make_get_request(url)
    results = []
    for operator in json:
        results.append(_Operator(operator["id"], operator["value"], operator["type"]))
    return results
