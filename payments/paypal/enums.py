from enum import Enum

class Mode(Enum):
    SANDBOX = "sandbox"
    LIVE = "live"


class Method(Enum):
    POST = "post"
    GET = "get"

class Currency(Enum):
    USD = "USD"
    EUR = "EUR"

class Locale(Enum):
    EN_US = "en-US"
