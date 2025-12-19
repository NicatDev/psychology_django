import requests

from payments import settings
from payments.paypal.enums import Mode, Method
from payments.paypal.interfaces import Command, HasBody, HasHeaders, NeedsAuthorization, Idempotent


class Executor:
    def __init__(self, mode: Mode = Mode.SANDBOX, proxies: dict | None = None):
        self.__mode = mode
        self.__session = requests.Session()

        proxies = proxies or settings.PAYPAL_CLIENT_PROXIES
        if settings.PAYPAL_CLIENT_PROXY_ENABLED and proxies:
            self.__session.proxies.update(proxies)

        if mode == Mode.SANDBOX:
            self.__session.verify = False

    def execute(self, command: Command):
        url = self.__url(command)
        method = self.__method(command)
        _headers = self.__headers(command)
        data = self.__data(command)

        if _headers['Content-Type'] == 'application/x-www-form-urlencoded':
            response = self.__session.request(method.value, url, headers=_headers, data=data)
        else:
            response = self.__session.request(method.value, url, headers=_headers, json=data)

        return response

    @classmethod
    def __url(cls, command: Command):
        url = settings.PAYPAL_URL.rstrip("/")
        path = command.path().strip("/")

        return f"{url}/{path}"

    @classmethod
    def __method(cls, command: Command) -> Method:
        return command.method()

    @classmethod
    def __headers(cls, command: Command) -> dict:
        _headers = {
            "Accept": "application/json",
        }

        if isinstance(command, HasHeaders):
            _headers.update(command.headers())

        if isinstance(command, NeedsAuthorization):
            from .utils import token_provider # to avoid circular dependency
            _headers["Authorization"] = str(token_provider())

        if isinstance(command, Idempotent) and command.idempotency_key():
            _headers['PayPal-Request-Id'] = command.idempotency_key()

        _headers.setdefault("Content-Type", "application/json")

        return _headers

    @classmethod
    def __data(cls, command: Command) -> dict:
        if isinstance(command, HasBody):
            return command.data()

        return {}
