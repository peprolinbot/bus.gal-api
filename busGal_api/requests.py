import requests

def make_post_request(url, data, token=None):
    """
    Makes a post request with the given dict of data data using the app's headers (okhttp) and authorize if token is set. Not intended to be used by clients

    :param url: Full url to make the request to
    :type url: str

    :param data: Data to send, it will be sent as application/json
    :type data: dict

    :param token: Bearer token to use for authentication, it is a JWT
    :type token: str

    :return: Dictionary made from the request's json
    :rtype: dict
    """
    headers = {'User-Agent': 'okhttp/3.10.0', 'Content-type': 'application/json;charset=UTF-8'}
    if token != None:
        headers["Authorization"] = f"Bearer {token}"
    r = requests.post(url , headers=headers, json=data)
    if r.status_code == 200:
        return r.json()
    else:
        raise Exception(f"There was an error in the request: Code {r.status_code}")

def make_get_request(url, token=None):
    """
    Makes a get request using the app's headers (okhttp) and authorize if token is set. Not intended to be used by clients

    :param url: Full url to make the request to
    :type url: str

    :param token: Bearer token to use for authentication, it is a JWT
    :type token: str

    :return: Dictionary made from the request's json
    :rtype: dict
    """
    headers = {'User-Agent': 'okhttp/3.10.0'}
    if token != None:
        headers["Authorization"] = f"Bearer {token}"
    r = requests.get(url , headers=headers)
    if r.status_code == 200:
        return r.json()
    else:
        raise Exception(f"There was an error in the request: Code {r.status_code}")
