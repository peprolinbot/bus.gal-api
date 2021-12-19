from ..requests import *
from urllib.parse import quote_plus as urlencode

def register_account(email, password, name, last_name, identity_type, identity_number, phone_number):
    """
    Register an user account

    :param email: Email address
    :type email: str

    :param password: Password (Must be at least 6 character length, including a digit and an upper case letter)
    :type email: str

    :param name: First name
    :type name: str

    :param last_name: Last name
    :type last_name: str

    :param identity_type: Identity type: "DNI" or "other"
    :type identity_type: str

    :param identity_number: Identity number e.g. your DNI
    :type identity_number: str

    :param phone_number: Phone number
    :type phone_number: str
    """
    if identity_type == "DNI":
        identity_type = 1
    elif identity_type == "other":
        identity_type = 2
    else:
        raise Exception("identity_type must be 'DNI' or 'other'")

    data = {
        "check_data_protection": 1,
        "email": email,
        "password": password,
        "name": name,
        "last_name": last_name,
        "identity_type": identity_type,
        "identity_number": identity_number,
        "phone_number": str(phone_number)
    }
    url = "https://tpgal-ws.xunta.gal/tpgal_ws/rest/user/register"
    make_post_request(url, data)

def recover_password(email):
    """
    Recover an account's password (sends an email with a new temporal one)

    :param email: Email address
    :type email: str
    """
    url = f"https://tpgal-ws.xunta.gal/tpgal_ws/rest/user/password?email={urlencode(email)}"
    make_get_request(url)

class _Card():
    """
    Class that represents a card. If an object of this class is deleted, so will be the card, it's in the destructor (__del__)
    """
    def __init__(self, account, number):
        self.account = account
        """
        The user account the card belongs to

        :type: Account
        """

        self.number = number
        """
        Number of the card

        :type: int
        """

        self.is_xente_nova = None
        """
        Whether the card is Xente Nova or no

        :type: bool
        """

        self.alias = None
        """
        The alias of the card

        :type: str
        """

        self.pending = None
        """
        Amount of money pending of return from the Xunta (cantos cartos débeche o pirolas)

        :type: float
        """

        self.cashed = None
        """
        Amount of money cashed from the Xunta (cantos cartos lle roubaches ó pirolas)

        :type: float
        """

        self.expired = None
        """
        Amount of money expired from the Xunta (cantos cartos quedouse o pirolas)

        :type: float
        """
        self.refresh_data()

    def refresh_data(self):
        """
        Obtains the card's details and sets them to the object
        """
        url = "https://tpgal-ws.xunta.gal/tpgal_ws/rest/cards/get"
        data = {
            "months": 12,
            "number": self.number
        }
        json = self.account._make_post_request(url, data)
        json_data = json["results"]

        self.is_xente_nova = json_data["type"] == 0
        self.alias = json_data["alias"]
        self.pending = json_data["total_pending"]
        self.cashed = json_data["total_cashed"]
        self.expired = json_data["total_expired"]

    def rename(self, alias):
        """
        Change the alias of the card

        :param alias: New alias for the card
        :type alias: str
        """
        self.account.rename_card(self.number, alias)

    def __del__(self):
        self.account.delete_card(self.number)

class Account():
    """
    Class that represents a user account. Either email and password or token and user_id (not really necessary) must be specified

    :param email: Email address to login with
    :type email: str

    :param password: Password to log in with
    :type password: str

    :param token: Auth token to use for the requests. It will be auto-obtained if email and password are specified
    :type token: str

    :param user_id: The user account's id. Not really needed for anything unless you are doing weird shit with the JWTs
    :type user_id: int
    """
    def __init__(self, email=None, password=None, token=None, user_id=None):
        if token is None:
            self.token = token
            self.login(email, password)
        else:
            self.token = token
            """
            The user token. It is a JWT.

            :type: str
            """

            self.user_id = user_id
            """
            The user id. You won't probably need this

            :type: int
            """

        self.name = None
        """
        First name of the user

        :type: str
        """

        self.last_name = None
        """
        Last name of the user

        :type: str
        """

        self.email  = None
        """
        Email of the user

        :type: str
        """

        self.identity_number = None
        """
        Identity number of the user e.g. DNI

        :type: str
        """

        self.identity_type = None
        """
        Identity type. It can be "DNI" or "other"

        :type: str
        """

        self.phone_number = None
        """
        The user's phone number

        :type: str
        """

        self.refresh_data()

    def _make_post_request(self, url, data):
        """
        Calls make_post_request using the object's token, which is updated after every request. Not intended to be used by clients

        :param url: Full url to make the request to
        :type url: str

        :param data: Data to send, it will be sent as application/json
        :type data: dict

        :return: Dictionary made from the request's json
        :rtype: dict
        """
        json = make_post_request(url, data, self.token)
        self.token = json["results"]["token"]["user_token"] # A new token is returned in every request, tokens don't seem to expire, but just in case we'll do as in the app.
        return json

    def _make_get_request(self, url):
        """
        Calls make_get_request using the object's token, which is updated after every request. Not intended to be used by clients

        :param url: Full url to make the request to
        :type url: str

        :return: Dictionary made from the request's json
        :rtype: dict
        """
        json = make_get_request(url, self.token)
        self.token = json["results"]["token"]["user_token"] # A new token is returned in every request, tokens don't seem to expire, but just in case we'll do as in the app.
        return json

    def login(self, email, password):
        """
        Logins with the given email and password and returns a token, which is also set to self.token

        :param email: Email address to login with
        :type email: str

        :param password: Password to login with
        :type password: str

        :return: User token
        :rtype: str
        """
        url = "https://tpgal-ws.xunta.gal/tpgal_ws/rest/user/login"
        data = {
         "email": email,
         "password": password
        }
        json = self._make_post_request(url, data) # This function already sets self.token to the returned token

        self.user_id = json["results"]["user_id"]

        return self.token

    def refresh_data(self):
        """
        Obtains the user's details and sets them to the object
        """
        url = "https://tpgal-ws.xunta.gal/tpgal_ws/rest/user/private/profile"
        json = self._make_get_request(url)
        user_data = json["results"]

        self.name = user_data["name"]
        self.last_name = user_data["last_name"]
        self.email  = user_data["email"]
        self.identity_number = user_data["identity_number"]
        self.identity_type = "DNI" if user_data["identity_type"] == 1 else "other" # else is used here, "other" is 2
        self.phone_number = user_data["phone_number"]

    def get_cards(self):
        """
        Get all the user cards

        :return: List with all the obtained cards' objects
        :rtype: list(_Card)
        """

        url = "https://tpgal-ws.xunta.gal/tpgal_ws/rest/cards/summary"
        data = {"months": 0}
        json = self._make_post_request(url, data)

        cards_data = json["results"]["cards"]
        cards = []
        for card in cards_data:
            card = self.get_card(int(card["number"]))
            cards.append(card)

        return cards

    def get_card(self, number):
        """
        Get the object for the user's card with the specified number

        :param number: Number of the card
        :type number: str

        :return: Card object
        :rtype: _Card
        """
        card = _Card(self, number)

        return card

    def add_card(self, number, alias):
        """
        Add a card to the user with the specified number and alias

        :param number: Number of the card
        :type number: str

        :param alias: Alias for the card
        :type alias: str
        """
        url = "https://tpgal-ws.xunta.gal/tpgal_ws/rest/cards/register"
        data = {
            "alias": alias,
            "number": str(number),
            "type": 0 # Idk what this is for, it is 0 for both Xente Nova and normal cards
        }
        self._make_post_request(url, data)

    def rename_card(self, number, alias):
        """
        Change the alias of a card with the specified number

        :param number: Number of the card
        :type number: str

        :param alias: New alias for the card
        :type alias: str
        """
        url = "https://tpgal-ws.xunta.gal/tpgal_ws/rest/cards/update"
        data = {
            "alias": alias,
            "number": str(number)
        }
        self._make_post_request(url, data)

    def delete_card(self, number):
        """
        Delete the card with the specified number

        :param number: Number of the card
        :type number: str
        """
        url = "https://tpgal-ws.xunta.gal/tpgal_ws/rest/cards/unregister"
        data = {"number": str(number)}
        self._make_post_request(url, data)
