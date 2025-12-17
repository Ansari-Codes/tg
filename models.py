from typing import Dict, Any, Literal
from storage import getUserStorage, getThemeStorage

class Response:
    def __init__(self):
        self.data:dict = {}
        self.errors = {}
        self.meta = {}
    @property
    def success(self):
        return not self.errors
    def _kv_to_str(self, k, v):
        return f"{k}: {v}"
    def _dict_to_str(self, dct):
        if isinstance(dct, dict):
            data = [dct]
        else:
            data = dct
        return '\t\n'.join(
            self._kv_to_str(k, v)
            for d in data
            for k, v in d.items()
        )
    def __str__(self) -> str:
        return f"""
    META: \n\t{self._dict_to_str(self.meta)}
    SUCCESS: \n\t{self.success}
    DATA: \n\t{self._dict_to_str(self.data)}
    ERRORS: \n\t{self._dict_to_str(self.errors)}
    """

class Variable:
    def __init__(self, value="") -> None:
        self.value = value
    def set(self, value):
        self.value  = value
        return self.value
    def get(self):
        return self.value

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