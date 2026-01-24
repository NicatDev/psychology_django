import requests, base64
from django.conf import settings

BASE_URL = "https://api-m.paypal.com"


def get_access_token():
    auth = base64.b64encode(
        f"{settings.PAYPAL_CLIENT_ID}:{settings.PAYPAL_CLIENT_SECRET}".encode()
    ).decode()

    r = requests.post(
        f"{BASE_URL}/v1/oauth2/token",
        headers={
            "Authorization": f"Basic {auth}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data={"grant_type": "client_credentials"},
    )
    r.raise_for_status()
    return r.json()["access_token"]


def create_order(amount):
    token = get_access_token()

    r = requests.post(
        f"{BASE_URL}/v2/checkout/orders",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        json={
            "intent": "CAPTURE",
            "purchase_units": [{
                "amount": {
                    "value": str(amount),
                    "currency_code": "USD"
                }
            }],
            "application_context": {
                "return_url": settings.PAYPAL_RETURN_URL,
                "cancel_url": settings.PAYPAL_CANCEL_URL,
            }
        }
    )
    r.raise_for_status()
    return r.json()


def capture_order(order_id):
    token = get_access_token()

    r = requests.post(
        f"{BASE_URL}/v2/checkout/orders/{order_id}/capture",
        headers={"Authorization": f"Bearer {token}","Content-Type": "application/json",}
    )
    r.raise_for_status()
    return r.json()
