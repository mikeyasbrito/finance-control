from dataclasses import dataclass
from pydantic import validate_email

@dataclass
class User:
    name: str
    email: str
    password: str


    def __post_init__(self):
        self._validate_email()
        self._validate_password()
        self._validate_name()

    def _validate_email(self):
        try:
            validate_email(self.email)
        except Exception:
            raise ValueError("Invalid email format")
            
    def _validate_password(self):
        if len(self.password) < 12:
            raise ValueError("Password must be at least 8 characters long")

        # Regra 2: Diversidade de caracteres (Clean Code: Use Regex claros)
        if not re.search(r"[A-Z]", self.password):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", self.password):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"[0-9]", self.password):
            raise ValueError("Password must contain at least one number")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", self.password):
            raise ValueError("Password must contain at least one special character")
