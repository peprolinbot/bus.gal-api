from . import _rest_adapter


## vvv Classes vvv ##

class Operator():
    """
    An operator firm
    """

    def __init__(self, id: int, type: str = None, name: str = None, address: str = None, phone: str = None, emails: list[str] = None, web: str = None):
        self.id = id
        """
        Id of the operator
        """

        self.type = type
        """
        Type of operator, either `group` or `operator`
        """

        self.name = name
        """
        Name of the operator
        """

        self.address = address
        """
        Real-life address of the operator
        """

        self.phone = phone
        """
        Phone number of the operator
        """

        self.emails = emails
        """
        E-Mail addresses of the operator
        """

        self.web = web
        """
        Website of the operator
        """

    def fetch_api(self) -> tuple[str, str, str]:
        """
        Fetch the API for it's own data. Calls `get_operator`, therefore updates name, emails and type

        :return: Name, emails and type, in that order
        """

        o = get_operator(self.id)
        self.name = o.name
        self.emails+o.emails
        self.type=o.type

        return o.name, o.emails, o.type

    def __repr__(self):
        return self.name


class Contract():
    """
    A contract with an operator
    """

    def __init__(self, code: str, name: str = None, consolidated: bool = None, operator: Operator = None, xg_code: str = None):
        self.code = code
        """
        Code of the contract
        """

        self.name = name
        """
        Name of the contract
        """

        self.consolidated = consolidated
        """
        Consolidation state of the contract
        """

        self.operator = operator
        """
        The `Operator` wich owns the contract
        """

        self.xg_code = xg_code
        """
        Code of the XG contract. Yeah, i'm not sure what it is either
        """

    def __repr__(self):
        return self.name

## ^^^ Classes ^^^ ##


## vvv Methods vvv ##

def _parse_operator(data: dict) -> Operator:
    """
    Builds an operator based on the data given by the API

    :param data: The dict
    """

    return Operator(id=data.get("id"),
                    type=data.get("type"),
                    name=data.get("text"),
                    address=data.get("text"),
                    phone=data.get("phone"),
                    emails=list(data.get("emails", data.get("email", ''))),
                    web=data.get("web"))


def search_operators(query: str, num_results: int = 2147483647) -> list[Operator]:
    """
    Searchs for operators with the specified name, using the app's search API, which is actually meant for autocomplete

    :param query: Search query

    :param num_results: Number of results to return. Defaults to the maximum integer value the API would accept, a.k.a. the maximum positive value for a 32-bit signed binary integer (Wikipedia), a.k.a. 2,147,483,647
    """

    data = _rest_adapter.get("/operators/autocomplete",
                            ep_params={"text": query,
                                       "numresults": num_results})

    return [Operator(id=el["id"],
                     type=el["type"],
                     name=el["text"]) for el in data]


def get_all_operators() -> list[Operator]:
    """
    Gets all the existing operators
    """

    data = _rest_adapter.get("/operators/autocomplete",
                            ep_params={"text": '',  # The API doesn't respond for some reason if the text argument isn't given
                                       "show_all": True})

    return [Operator(id=el["id"],
                     type=el["type"],
                     name=el["text"]) for el in data]


def search_contracts(operator_id: int = None, provincial_service: int = None) -> list[Contract]:
    """
    Searchs for contracts, filtering by operator and/or provincial service id 

    :param operator_id: The id of an operator

    :param provincial_service: A provincial service id
    """

    data = _rest_adapter.get("/operators/contracts",
                            ep_params={"operator_id": operator_id,
                                       "provincial_service": provincial_service})

    return [Contract(code=el["code"],
                     xg_code=el.get("xg_code"),
                     name=el["name"],
                     consolidated=el["consolidated"],
                     operator=_parse_operator(el["operator"])) for el in data]


def get_all_contracts() -> list[Contract]:
    """
    Gets all the existing contracts
    """

    return search_contracts()


def get_operator(operator_id: int) -> Operator:
    """
    Fetch an operator with it's id. You'll get it's name, type and email addresses

    :param operator_id: The the operator id to fetch the data for
    """

    return _parse_operator(_rest_adapter.get("/operators/get",
                                            ep_params={"operator_id": operator_id,
                                                       "operator_type": "operator"}))  # Turns out the API doesn't give a damn about which type you specify, but you can't just skip it

## ^^^ Methods ^^^ ##
