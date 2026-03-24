from abc import ABC, abstractmethod

class IPasswordHasher(ABC):
    @abstractmethod
    def hash(self, password: str) -> str:
        """Recebe a senha limpa e devolve o hash irreconhecível."""
        pass

    @abstractmethod
    def verify(self, plain_password: str, hashed_password: str) -> bool:
        """Recebe a senha limpa e o hash, e retorna True se coincidem."""
        pass
