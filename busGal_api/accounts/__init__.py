from ..rest_adapter import RestAdapter as RestAdapter
from ..known_servers import XG_APP as BASE_URL

_rest_adapter = RestAdapter(BASE_URL)

from .accounts import *

__all__ = ["accounts"]
