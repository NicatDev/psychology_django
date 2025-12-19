from __future__ import annotations

from typing import TypeVar, Dict, Any, Type

from pydantic import BaseModel

from payments.paypal.enums import Method


class DTO(BaseModel):
    @classmethod
    def from_response(cls: Type[T], response: Dict[str, Any]) -> T:
        raise NotImplementedError

    def to_json(self) -> str:
        return self.model_dump_json()

    @classmethod
    def from_json(cls, json_string: str) -> T:
        """Create Token from cached JSON (uses Pydantic field names)"""
        return cls.model_validate_json(json_string)


T = TypeVar("T", bound=DTO)


class Command:
    def execute(self) -> DTO:
        pass

    def path(self) -> str:
        pass

    def method(self) -> Method:
        pass


class NeedsAuthorization:
    pass


class HasHeaders:
    def headers(self) -> dict:
        pass


class Idempotent:
    def idempotency_key(self) -> str:
        raise NotImplementedError


class HasBody:
    def data(self) -> dict:
        pass
