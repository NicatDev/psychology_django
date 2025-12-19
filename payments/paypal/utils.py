import hashlib
import json

from django.core.cache import cache

from payments import settings


def token_provider():
    from payments.paypal.commands import GetToken
    from payments.paypal.dto import Token

    cached_token = cache.get("paypal_access_token")
    if cached_token:
        return Token.from_json(cached_token)

    token_obj = GetToken.instance().execute()

    margin = 60  # in seconds - safety margin
    timeout = max(0, token_obj.expires_in - margin)

    cache.set(
        "paypal_access_token",
        token_obj.to_json(),
        timeout=timeout,
    )

    return token_obj


def gen_idempotency_key(peaces: tuple[str], prefix: str | None = None):
    key = "idempotent:"

    if prefix:
        key += prefix + ":"

    key += ":".join(map(str, peaces))
    key += ":" + settings.SECRET_KEY

    return hashlib.sha256(key.encode('utf-8')).hexdigest()


def resolve_link(links: list[dict], rel: str) -> str | None:
    for link in links:
        if link.get("rel") == rel:
            return link.get("href")

    return None
