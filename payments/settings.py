import os

import environ

from core.settings import SECRET_KEY

env = environ.Env(
    SECRET_KEY=(str, SECRET_KEY),
    PAYPAL_MODE=(str, "sandbox"),
    PAYPAL_SANDBOX_URL=(str, ""),
    PAYPAL_LIVE_URL=(str, ""),
    PAYPAL_SANDBOX_CLIENT_ID=(str, ""),
    PAYPAL_LIVE_CLIENT_ID=(str, ""),
    PAYPAL_SANDBOX_CLIENT_SECRET=(str, ""),
    PAYPAL_LIVE_CANCEL_URL=(str, ""),
    PAYPAL_WEBHOOK_ID=(str, ""),
    PAYPAL_CLIENT_PROXY_ENABLED=(bool, False),
    PAYPAL_RETURN_URL=(str, ""),
    PAYPAL_CANCEL_URL=(str, ""),
)

environ.Env.read_env(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

PAYPAL_MODE = env("PAYPAL_MODE", default="sandbox")
PAYPAL_WEBHOOK_ID = env("PAYPAL_WEBHOOK_ID")
PAYPAL_RETURN_URL = env("PAYPAL_RETURN_URL", default="http://localhost:8000/payment/success")
PAYPAL_CANCEL_URL = env("PAYPAL_CANCEL_URL", default="http://localhost:8000/payment/cancel")
PAYPAL_CLIENT_PROXIES = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}

if PAYPAL_MODE == "sandbox":
    PAYPAL_URL = env("PAYPAL_SANDBOX_URL", default="https://api-m.sandbox.paypal.com")
    PAYPAL_CLIENT_ID = env("PAYPAL_SANDBOX_CLIENT_ID")
    PAYPAL_CLIENT_SECRET = env("PAYPAL_SANDBOX_CLIENT_SECRET")
    PAYPAL_CLIENT_PROXY_ENABLED = env("PAYPAL_CLIENT_PROXY_ENABLED", default=True)
else:
    PAYPAL_URL = env("PAYPAL_LIVE_URL", default="https://api-m.paypal.com")
    PAYPAL_CLIENT_ID = env("PAYPAL_LIVE_CLIENT_ID")
    PAYPAL_CLIENT_SECRET = env("PAYPAL_LIVE_CLIENT_SECRET")
    PAYPAL_CLIENT_PROXY_ENABLED = env("PAYPAL_CLIENT_PROXY_ENABLED", default=False)
