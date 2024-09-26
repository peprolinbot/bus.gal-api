import requests
from json import JSONDecodeError
import logging
from typing import Callable

from .exceptions import *


class RestAdapter():
    """
    Trip class. Used for getting results as Expedition objects

    :param url: Base url of the rest service, e.g. https://tpgal-ws.xunta.gal/tpgal_ws/rest. The known ones are in known_servers.py

    :param token: The token used to authenticate to endpoints that are for logged in users

    :param token_type: The said token's type. In my tests it's always been `Bearer`, so that's the default

    :param logger: If your app has a logger, pass it in here

    :param authentication_function: A Callable which must return the token to be used. It will be called when 401 occurs to set the token to its returned value and try again the request

    :param max_auth_recursion_level: The maximum number of times an authentication using `authentication_function` can be tried
    """

    def __init__(self, url: str, token: str = None, token_type: str = "Bearer", logger: logging.Logger = None, authentication_function: Callable = None, max_auth_recursion_level: int = 1):
        self.url = url
        self.token = token
        self.token_type = token_type
        self._logger = logger or logging.getLogger(__name__)
        self._authentication_function = authentication_function
        self.max_auth_recursion_level = max_auth_recursion_level

    def _do(self, http_method: str, endpoint: str, ep_params: dict = None, data: dict = None, load_json: bool = True, results_only: bool = True, _auth_recursion_level: int = 0) -> dict:
        """
        Make an HTTP request

        :param http_method: The method to use for the request, e.g. GET or POST

        :param endpoint: The endpoint to which the request should be made. This will be appended to self.url

        :param ep_params: The request parameters

        :param data: The request data (It'll be parsed into json)

        :return: The results key from the JSON response of the api (already parsed)
        """

        full_url = self.url + endpoint
        headers = {"Authorization": f"{self.token_type} {self.token}"}

        def _escape_dict(data: dict) -> str:
            return str(data).replace("{", "{{").replace("}", "}}")

        log_line_pre = f"method={http_method}, url={full_url}, params={_escape_dict(ep_params)}, data={_escape_dict(data)}"
        log_line_post = ', '.join(
            (log_line_pre, "success={}, status_code={}, message={}"))

        try:
            self._logger.debug(msg=log_line_pre)
            response = requests.request(
                method=http_method, url=full_url, headers=headers, params=ep_params, json=data)
        except requests.exceptions.RequestException as e:
            self._logger.error(msg=(str(e)))
            raise e

        if response.status_code == 401 and self._authentication_function and (_auth_recursion_level < self.max_auth_recursion_level):
            self.token = self._authentication_function()
            self._logger.debug(msg="Retrying request after authentication")
            return self._do(http_method, endpoint, ep_params, data, _auth_recursion_level+1)
        if load_json:
            try:
                data_out = response.json()
            except (ValueError, JSONDecodeError) as e:
                if response.content == b'':
                    raise TPGalWSBlankResponse(response) from e
                raise TPGalWSBadJsonException(response) from e
        else:
            data_out = response
            results_only = False  # It is not a dict, so it wouldn't work

        is_success = 299 >= response.status_code >= 200  # 200 to 299 is OK
        log_line = log_line_post.format(
            is_success, response.status_code, response.reason)
        if is_success:
            self._logger.debug(msg=log_line)
            try:
                # In XenteNovaQr the results key doesn't exist
                return data_out.get("results", data_out) if results_only else data_out
            except AttributeError:
                return data_out  # For XenteNovaQR Account.get_qrs(), the API returns a list
        self._logger.error(msg=log_line)
        raise TPGalWSAppException(response)

    def get(self, endpoint: str, ep_params: dict = None, **kwargs) -> dict:
        """
        Make an HTTP GET request
        """

        return self._do(http_method='GET', endpoint=endpoint, ep_params=ep_params, **kwargs)

    def post(self, endpoint: str, ep_params: dict = None, data: dict = None, **kwargs) -> dict:
        """
        Make an HTTP POST request
        """

        return self._do(http_method='POST', endpoint=endpoint, ep_params=ep_params, data=data, **kwargs)

    def patch(self, endpoint: str, ep_params: dict = None, data: dict = None, **kwargs) -> dict:
        """
        Make an HTTP PATCH request
        """

        return self._do(http_method='PATCH', endpoint=endpoint, ep_params=ep_params, data=data, **kwargs)
