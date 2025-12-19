from payments.paypal.interfaces import DTO
from .utils import resolve_link


class Token(DTO):
    token: str
    token_type: str
    expires_in: int

    def __str__(self):
        return f"{self.token_type} {self.token}"

    @classmethod
    def from_response(cls, response) -> "Token":
        return cls(
            token=response['access_token'],
            token_type=response['token_type'],
            expires_in=response['expires_in']
        )


class Order(DTO):
    id: str
    status: str
    self_link: str
    payer_action_link: str

    @classmethod
    def from_response(cls, response) -> "Order":
        links = response['links']

        return cls(
            id=response['id'],
            status=response['status'],
            self_link=resolve_link(links, 'self'),
            payer_action_link=resolve_link(links, 'payer-action')
        )


class CapturedOrder(DTO):
    id: str
    status: str
    capture_id: str

    @classmethod
    def from_response(cls, response) -> "CapturedOrder":
        return cls(
            id=response['id'],
            status=response['status'],
            capture_id=response['purchase_units'][0]['payments']['captures'][0]['id']
        )
