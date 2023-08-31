import requests
from json import JSONDecodeError
import logging

from .exceptions import *


class RestAdapter():
    """
    Trip class. Used for getting results as Expedition objects

    :param url: Base url of the rest service, e.g. https://tpgal-ws.xunta.gal/tpgal_ws/rest. The known ones are in known_servers.py

    :param token: The token used to authenticate to endpoints that are for logged in users

    :param token_type: The said token's type. In my tests it's always been `Bearer`, so that's the default

    :param logger: If your app has a logger, pass it in here
    """

    def __init__(self, url: str, token: str = None, token_type: str = "Bearer", logger: logging.Logger = None):
        self.url = url
        self.token = token
        self.token_type = token_type
        self._logger = logger or logging.getLogger(__name__)

    def _do(self, http_method: str, endpoint: str, ep_params: dict = None, data: dict = None) -> dict:
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
        print(log_line_pre)
        log_line_post = ', '.join(
            (log_line_pre, "success={}, status_code={}, message={}"))

        try:
            self._logger.debug(msg=log_line_pre)
            response = requests.request(
                method=http_method, url=full_url, headers=headers, params=ep_params, json=data)
        except requests.exceptions.RequestException as e:
            self._logger.error(msg=(str(e)))
            raise e

        try:
            data_out = response.json()
        except (ValueError, JSONDecodeError) as e:
            if response.content == b'':
                raise TPGalWSBlankResponse(response) from e
            raise TPGalWSBadJsonException(response) from e

        is_success = 299 >= response.status_code >= 200  # 200 to 299 is OK
        log_line = log_line_post.format(
            is_success, response.status_code, response.reason)
        if is_success:
            self._logger.debug(msg=log_line)
            return data_out.get("results")
        self._logger.error(msg=log_line)
        raise TPGalWSAppException(response)

    def get(self, endpoint: str, ep_params: dict = None) -> dict:
        """
        Make an HTTP GET request
        """

        return self._do(http_method='GET', endpoint=endpoint, ep_params=ep_params)

    def post(self, endpoint: str, ep_params: dict = None, data: dict = None) -> dict:
        """
        Make an HTTP POST request
        """

        return self._do(http_method='POST', endpoint=endpoint, ep_params=ep_params, data=data)
