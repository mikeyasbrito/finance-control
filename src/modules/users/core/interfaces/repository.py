from abc import ABC, abstractmethod
from modules.users.core.entities.user import User
class IUserRepository(ABC):
    @abstractmethod
    def save(self, user: User) -> None:
        pass
    
    @abstractmethod
    def find_by_email(self, email: str) -> User | None:
        pass