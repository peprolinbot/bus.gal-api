from . import _rest_adapter

from .lines import Line, _parse_line

from datetime import date, datetime, timedelta

## vvv Classes vvv ##


class WarningAlert():
    """
    A warning
    """

    def __init__(self, id: int, line: Line, start: datetime, end: datetime, message_gl: str, message_es: str, important: bool):
        self.id = id
        """
        Id of the warning
        """

        self.line = line
        """
        The `busGal_api.transport.lines.Line` the warning refers to
        """

        self.start = start
        """
        The time at which the warning starts
        """

        self.end = end
        """
        The time at which the warning ends
        """

        self.message_gl = message_gl
        """
        The warning's message in galician
        """

        self.message_es = message_es
        """
        The warning's message in spanish
        """

        self.important = important
        """
        Whether the warning is classified as important
        """

    def __repr__(self):
        return self.message_gl

## ^^^ Classes ^^^ ##


## vvv Methods vvv ##

def _parse_warning(data: dict) -> WarningAlert:
    """
    Builds a `WarningAlert` based on the data given by the API
    """

    return WarningAlert(id=data["warning_id"],
                        line=[_parse_line(el) for el in data.get("line", [])],
                        start=datetime.strptime(
                            data["start_date"], "%Y-%m-%d %H:%M:%S") if data.get("start_date") else None,
                        end=datetime.strptime(
                            data["end_date"], "%Y-%m-%d %H:%M:%S") if data.get("end_date") else None,
                        message_gl=data["message_gl"],
                        message_es=data["message_es"],
                        important=data["important"])


def search_warnings(line_id: int = None, active: bool = True, date: date = date.today()+timedelta(1)) -> list[WarningAlert]:
    """
    Search warnings filtering by line, state and date. Set anything to None to disable that filter

    :param line_id: The line id to check

    :param active: Whether to fetch the active warnings, which is the default, or the non-active ones

    :param date: The date for which you want to check the warnings. Defaults to tomorrow
    """

    data = _rest_adapter.get("/warning/public/get-by-line",
                            ep_params={"line_id": line_id,
                                       "active": active,
                                       "date": date.strftime("%d/%m/%Y") if date else None})

    return [_parse_warning(el) for el in data]


def get_important_warnings() -> list[WarningAlert]:
    """
    Returns all the important warnings
    """

    data = _rest_adapter.get("/warning/public/get-important")

    return [_parse_warning(el) for el in data]

## ^^^ Methods ^^^ ##
