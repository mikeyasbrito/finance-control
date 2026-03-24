from abc import ABC, abstractmethod

class IJwtManager(ABC):
    @abstractmethod
    def generate_token(self, user_id: str) -> str:
        """
        Recebe o UUID do usuário (em string) e devolve a string contendo o Token JWT assinado.
        """
        pass
    
    @abstractmethod
    def verify_token(self, token: str) -> dict:
        """
        Recebe um Token JWT e devolve as informações decodificadas (payload).
        Deve levantar uma Exceção se o token for inválido ou estiver expirado.
        """
        pass
