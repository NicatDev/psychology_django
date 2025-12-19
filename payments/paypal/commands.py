import base64
from decimal import Decimal, ROUND_HALF_UP

from payments import settings
from payments.paypal.dto import Token, Order, CapturedOrder
from payments.paypal.enums import Method, Currency, Locale
from payments.paypal.exceptions import TokenObtainingError, OrderCreationFailed, CaptureOrderFailed
from payments.paypal.executor import Executor
from payments.paypal.interfaces import Command, HasHeaders, HasBody, Idempotent, NeedsAuthorization


class GetToken(Command, HasHeaders, HasBody):

    def __init__(self, executor: Executor, client_id: str, client_secret: str):
        self.__client_id = client_id
        self.__client_secret = client_secret
        self.__executor = executor

    def execute(self) -> Token:
        response = self.__executor.execute(self)

        if response.ok:
            data = response.json()
            return Token.from_response(response.json())

        raise TokenObtainingError(message=response.text, status_code=response.status_code)

    def path(self) -> str:
        return "/v1/oauth2/token"

    def method(self) -> Method:
        return Method.POST

    def headers(self):
        return {
            "Authorization": f"Basic {self.__token()}",
            "Content-Type": "application/x-www-form-urlencoded"
        }

    def data(self):
        return {"grant_type": "client_credentials"}

    def __token(self):
        return base64.b64encode(f"{self.__client_id}:{self.__client_secret}".encode()).decode()

    @classmethod
    def instance(cls, client_id: str | None = None, client_secret: str | None = None, executor: Executor | None = None):
        executor = executor or Executor()
        client_id = client_id or settings.PAYPAL_CLIENT_ID
        client_secret = client_secret or settings.PAYPAL_CLIENT_SECRET

        return cls(
            executor=executor,
            client_id=client_id,
            client_secret=client_secret,
        )


class CreateOrder(Command, Idempotent, NeedsAuthorization, HasBody):
    def __init__(
            self,
            executor: Executor,
            amount: int | float,
            currency: Currency = Currency.USD,
            locale: Locale = Locale.EN_US,
            idempotency_key: str | None = None,
    ):
        self.__idempotency_key = idempotency_key
        self.__amount = amount
        self.__currency = currency
        self.__locale = locale
        self.__executor = executor

    def path(self) -> str:
        return "/v2/checkout/orders"

    def method(self) -> Method:
        return Method.POST

    def data(self) -> dict:
        return {
            "intent": "CAPTURE",
            "purchase_units": [{
                "amount": {
                    "value": float(Decimal(self.__amount).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)),
                    "currency_code": self.__currency.value
                }
            }],
            "payment_source": {
                "paypal": {
                    "experience_context": {
                        "locale": self.__locale.value,
                        "shipping_reference": "NO_SHIPPING",
                        "brand_name": "Octopus",
                        "return_url": settings.PAYPAL_RETURN_URL,
                        "cancel_url": settings.PAYPAL_CANCEL_URL,
                    }
                }
            }
        }

    def idempotency_key(self) -> str:
        return self.__idempotency_key

    def execute(self) -> Order:
        response = self.__executor.execute(self)

        if response.ok:
            return Order.from_response(response.json())

        raise OrderCreationFailed(message=response.text, status_code=response.status_code)

    @classmethod
    def instance(
            cls,
            amount: int | float,
            currency: Currency = Currency.USD,
            locale: Locale = Locale.EN_US,
            idempotency_key: str | None = None,
            executor: Executor | None = None
    ):
        executor = executor or Executor()

        return cls(
            executor=executor,
            amount=amount,
            currency=currency,
            locale=locale,
            idempotency_key=idempotency_key
        )


class CaptureOrder(Command, NeedsAuthorization):
    def __init__(self, executor: Executor, order_id: str):
        self.__executor = executor
        self.__order_id = order_id

    def path(self) -> str:
        return f"/v2/checkout/orders/{self.__order_id}/capture"

    def method(self) -> Method:
        return Method.POST

    def execute(self) -> CapturedOrder:
        response = self.__executor.execute(self)

        if response.ok:
            return CapturedOrder.from_response(response.json())

        raise CaptureOrderFailed(message=response.text, status_code=response.status_code)

    @classmethod
    def instance(cls, order_id: str, executor: Executor | None = None):
        return cls(executor=executor or Executor(), order_id=order_id)
