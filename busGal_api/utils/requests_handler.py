import requests
import json

def make_get_request(url):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'}
    r = requests.get(url , headers=headers)
    if r.status_code == 200:
        return r.json()
    else:
        raise RequestException("There was an error in the request: Code " + str(r.status_code))
