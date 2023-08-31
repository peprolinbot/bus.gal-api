from . import _rest_adapter
from ..rest_adapter import RestAdapter

## vvv Classes vvv ##


class Card():
    """
    A card
    """

    def __init__(self, account: 'Account', number: int, is_xente_nova: bool, alias: str = None, pending: float = None, cashed: float = None, expired: float = None, summary_movements: list[dict] = None, travels: int = None) -> None:
        self.account = account
        """
        The user account the card belongs to
        """

        self.number = number
        """
        Number of the card
        """

        self.is_xente_nova = is_xente_nova
        """
        Whether the card is Xente Nova (type 0 in the API) or not (type 1)
        """

        self.alias = alias
        """
        The alias of the card
        """

        self.pending = pending
        """
        Amount of money pending of return
        """

        self.cashed = cashed
        """
        Amount of money cashed
        """

        self.expired = expired
        """
        Amount of money expired because it wasn't cashed
        """

        self.summary_movements = summary_movements
        """
        The summary of the movemnts of the card
        """

        self.travels = travels
        """
        Number of travels done. Given in card summary (`Account.get_cards`)
        """

    def refresh_data(self, months: int = 12) -> None:
        """
        Obtains the card's details and sets them to the object

        :params months: How many months to get `summary_movements` for
        """

        card = self.account.get_card(number=self.number,
                                     months=months)

        self.is_xente_nova = card.is_xente_nova
        self.alias = card.alias
        self.pending = card.pending
        self.cashed = card.cashed
        self.expired = card.expired
        self.summary_movements = card.summary_movements

    def rename(self, alias: str) -> None:
        """
        Change the alias of the card

        :param alias: New alias for the card
        """
        self.account.rename_card(number=self.number,
                                 alias=alias)

    def __repr__(self) -> str:
        return f"{self.alias}: {self.number}"


class Account():
    """
    Class that represents a user account. Either both email and password or token must be specified

    :param email: Email address to login with

    :param password: Password to log in with

    :param token: Auth token to use for the requests. It will be auto-obtained if email and password are specified

    :param token_type: Usually `Bearer`, and that's the default
    """

    def __init__(self, email: str = None, password: str = None, token: str = None, token_type: str = "Bearer", user_id: int = None, name: str = None, last_name: str = None, identity_number: str = None, identity_type: int = None, phone_number: str = None) -> None:
        self.rest_adapter = RestAdapter(_rest_adapter.url)
        """
        The `busGal_api.rest_adapter.RestAdapter` this classe's methods use to do authenticated requests
        """

        if token:
            self.rest_adapter.token = token
            """
            The user token. It is a JWT
            """

            self.rest_adapter.token_type = token_type
            """
            The type of token
            """

            self.user_id = user_id
            """
            The user id
            """
        elif email and password:
            self.login(email, password)
        else:
            raise TypeError(
                "Account.__init__() expected either the 'token' or both the 'email' and 'password' arguments")

        self.email = None
        """
        Email of the user
        """

        self.name = None
        """
        First name of the user
        """

        self.last_name = None
        """
        Last name of the user
        """

        self.identity_number = None
        """
        Identity number of the user e.g. DNI
        """

        self.identity_type = None
        """
        Identity type. It can be:
        - 1: DNI
        - 2: Other
        """

        self.phone_number = None
        """
        The user's phone number
        """

    def _parse_token(self, data: dict) -> None:
        """
        Set token info obtained from an authenticated request or `login`
        """

        self.rest_adapter.token = data["token"]["user_token"]
        self.token_type = data["token"]["token_type"]

    def login(self, email: str, password: str) -> None:
        """
        Logins with the given email and password and returns a token, which is also set to self.token
        """

        data = _rest_adapter.post("/user/login",
                                  data={"email": email,
                                        "password": password})

        self.user_id = data["user_id"]

        self._parse_token(data)

    def refresh_data(self) -> None:
        """
        Obtains the user's details and sets them to the object
        """

        data = self.rest_adapter.get("/user/private/profile")

        self.name = data["name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.identity_number = data["identity_number"]
        self.identity_type = data["identity_type"]
        self.phone_number = data["phone_number"]

    def get_cards(self, months: int = 0) -> list[Card]:
        """
        Get all the user cards

        :param months: Something. Works well if set to 0
        """

        data = self.rest_adapter.post("/cards/summary",
                                      data={"months": 0})

        return [_parse_card(el, self) for el in data["cards"]]

    def get_card(self, number: int, months: int = 12) -> Card:
        """
        Get the object for the user's card with the specified number

        :params months: How many months to get `summary_movements` for
        """

        data = self.rest_adapter.post("/cards/get",
                                     data={"months": months,
                                           "number": number})

        return _parse_card(data, self)

    def add_card(self, number: int, alias: str) -> None:
        """
        Add a card to the user with the specified number and alias
        """

        self.rest_adapter.post("/cards/register",
                               data={"alias": alias,
                                     "number": str(number),
                                     "type": 0})  # The app sends  this as 0 for both Xente Nova and normal cards

    def rename_card(self, number: int, alias: str) -> None:
        """
        Change the alias of a card with the specified number

        :param alias: New alias for the card
        """

        self.rest_adapter.post("/cards/update",
                               data={"alias": alias,
                                     "number": str(number)})

    def delete_card(self, number: int) -> None:
        """
        Delete the card with the specified number
        """

        self.rest_adapter.post("/cards/unregister",
                               data={"number": str(number)})

    def __repr__(self) -> str:
        return self.email

## ^^^ Classes ^^^ ##

## vvv Methods vvv ##


def _parse_card(data: dict, account: Account) -> Card:
    """
    Build a `Card` from a dict of API data
    """

    return Card(account=account,
                number=data["number"],
                is_xente_nova=data["type"] == 0,
                travels=data.get("travels"),
                alias=data.get("alias"),
                pending=data.get("pending", data.get("total_pending")),
                cashed=data.get("total_cashed"),
                expired=data.get("expired"),
                summary_movements=data.get("summary_datas")
                )


def register_account(email: str, password: str, name: str, last_name: str, identity_type: str, identity_number: str, phone_number: str) -> None:
    """
    Register an user account

    :param email: Email address

    :param password: Password (Must be at least 6 character length, including a digit and an upper case letter)

    :param name: First name

    :param last_name: Last name

    :param identity_type: Identity type: "DNI" or "other"

    :param identity_number: Identity number e.g. your DNI

    :param phone_number: Phone number
    """

    if identity_type == "DNI":
        identity_type = 1
    elif identity_type == "other":
        identity_type = 2
    else:
        raise Exception("identity_type must be 'DNI' or 'other'")

    _rest_adapter.post("/user/register",
                       data={
                           "check_data_protection": 1,
                           "email": email,
                           "password": password,
                           "name": name,
                           "last_name": last_name,
                           "identity_type": identity_type,
                           "identity_number": identity_number,
                           "phone_number": str(phone_number)
                       })


def recover_password(email: str) -> None:
    """
    Recover an account's password (sends an email with a new temporal one)

    :param email: Email address
    """

    _rest_adapter.get("/user/password",
                      ep_params={"email": email})

## ^^^ Methods ^^^ ##
