from . import _rest_adapter

from datetime import date

## vvv Classes vvv ##


class SpecialRate():
    """
    A special rate (a discount)
    """

    def __init__(self, id: int, text: str, type_id: int, type_name: str):
        self.id = id
        """
        The special rate id
        """

        self.text = text
        """
        The text of the discount
        """

        self.type_id = type_id
        """
        The id of the type of discount
        """

        self.type_name = type_name
        """
        The name of the type of discount
        """

    def __repr__(self):
        return f"{self.type_name}: {self.text}"


class Rate():
    """
    A rate (the cost of a trip)
    """

    def __init__(self, effective: float, credit_card: float, special_rates: list[SpecialRate] = None):
        self.effective = effective
        """
        The cost of the trip if payed with physical money
        """

        self.credit_card = credit_card
        """
        The cost of the trip if payed with the public transport card
        """

        self.special_rates = special_rates
        """
        The applicable special rates
        """

    def __repr__(self):
        return f"Effective: {self.effective}€ || Card: {self.credit_card}€"

## ^^^ Classes ^^^ ##


## vvv Methods vvv ##

def _parse_special_rate(data: dict) -> SpecialRate:
    return SpecialRate(id=data["special_rate_id"],
                       text=data["special_rate_text"],
                       type_id=data["special_rate_type_id"],
                       type_name=data["special_rate_type_name"])


def _parse_rate(data: dict) -> Rate:
    return Rate(effective=data["effective"],
                credit_card=data["credit_card"],
                special_rates=[_parse_special_rate(sr) for sr in data["special_rates"]] if data.get("special_rates") else None)


def get_rate(origin_id: int, destination_id: int, expedition_id: int, date: date) -> Rate:
    """
    Fetches the rate of an expedition, including special rates
    """

    return _parse_rate(_rest_adapter.get("/rate/search",
                                        ep_params={"origin_id": origin_id,
                                                   "destination_id": destination_id,
                                                   "expedition_id": expedition_id,
                                                   "date": date.strftime("%d/%m/%Y")}))

## ^^^ Methods ^^^ ##
