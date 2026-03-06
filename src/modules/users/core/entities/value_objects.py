from dataclasses import dataclass
from pydantic import validate_email


special_characters_set = set("!@#$%^&*()_+-=[]{}|;:,.<>?")

class ExceptionDomain(Exception):
    pass

class InvalidEmailException(ExceptionDomain):
    pass


@dataclass
class Password:
    value: str

    def __post_init__(self):

        self._validate_complexity()

    def _validate_complexity(self):

        if len(self.value) < 12:
            raise ExceptionDomain("Password must contain 12 or more charactere")

        if not any(char.islower() for char in self.value):
            raise ExceptionDomain("Password must contain at least one lowercase letter")

        if not any(char.isdigit() for char in self.value):
            raise ExceptionDomain("Password must contain at least one number")

        if not any(char in special_characters_set for char in self.value):
            raise ExceptionDomain("Password must contain at least one special charactere")

        if not any(char.isupper() for char in self.value):
            raise ExceptionDomain("Password must contain at least one uppercase letter")
        



@dataclass
class Email:
    value: str

    def __post_init__(self):
        try:
            validate_email(self.value)
        except Exception:
            raise InvalidEmailException("Invalid email format")