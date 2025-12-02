from typing import Dict, Any, Literal
from storage import getUserStorage, getThemeStorage

class Response:
    data: Dict[Any, Any] = {}
    errors: Dict[str, str] = {}
    success: bool = not errors

class Variable:
    def __init__(self, value="") -> None:
        self.value = value

class Auth:
    @property
    def name(self) -> str | None:
        return getUserStorage().get("name")
    @property
    def mail(self) -> str | None:
        return getUserStorage().get("mail")
    @property
    def avatar(self) -> str | None:
        return getUserStorage().get("avatar")
    @property
    def theme(self) -> dict | None:
        return getThemeStorage()
    @property
    def authenticated(self) -> bool:
        return getUserStorage().get("auth", False)