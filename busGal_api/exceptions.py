class AppError():
    """
    Represents error information returned by the server
    """
    def __init__(self, code, message):
        self.code = code
        """
        An integer which identifies an error
        """
        self.message = message
        """
        The actual error message
        """


class TPGalWSBaseResponseException(Exception):
    """
    Exception used for succesful connections to the server but that for some reason didn't provide any result
    """

    def __init__(self, message, response):

        super().__init__(
            f"HTTP --> {response.status_code}: {response.reason} || {message}")

        self.response = response
        """
        The `requests.response` object of the failed request
        """


class TPGalWSAppException(TPGalWSBaseResponseException):
    """
    Exception used when the server returns a JSON response with information about an error
    """

    def __init__(self, response, data_out=None):
        self.data_out = data_out or response.json()
        """
        `requests.response.json()`
        """

        self.app_error = AppError(self.data_out.get(
            'code'), self.data_out.get('message'))
        """
        `AppError` with more information about the cause of the error
        """

        super().__init__(
            f"App --> {self.app_error.code}: {self.app_error.message}", response)


class TPGalWSBlankResponse(TPGalWSBaseResponseException):
    """
    Exception used when the server returns nothing (really, just nothing, `b''` if you know what I mean😉)
    """

    def __init__(self, response):
        super().__init__("The API errored silently", response)


class TPGalWSBadJsonException(TPGalWSBaseResponseException):
    """
    Exception when the server returns something, but it isn't JSON-parseable
    """

    def __init__(self, response):
        super().__init__("Bad JSON in response", response)
