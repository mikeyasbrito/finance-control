from dataclasses import dataclass
from pydantic import validate_email
from zxcvbn import zxcvbn
from modules.users.core.interfaces.cryptography import IPasswordHasher

special_characters_set = set("!@#$%^&*()_+-=[]{}|;:,.<>?")

class ExceptionDomain(Exception):
    pass

class InvalidEmailException(ExceptionDomain):
    pass


@dataclass
class Password:
    value: str

    @classmethod
    def create(cls, plain_password: str, hasher: IPasswordHasher) -> "Password":
        # Mantemos o limite mínimo de 12 como camada extra de segurança
        if len(plain_password) < 12:
            raise ExceptionDomain("Password must contain 12 or more characters")
            
        resultado = zxcvbn(plain_password)
        score = resultado.get('score', 0)
        
        # Um score 3 ou 4 é considerado forte/muito forte
        if score < 3:
            raise ExceptionDomain("Sua senha é muito fraca. Tente uma frase ou palavras aleatórias.")        
            
        hashed_value = hasher.hash(plain_password)
        return cls(value=hashed_value)        



@dataclass
class Email:
    value: str

    def __post_init__(self):
        try:
            validate_email(self.value)
        except Exception:
            raise InvalidEmailException("Invalid email format")