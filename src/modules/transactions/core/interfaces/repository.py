from abc import ABC, abstractmethod
from datetime import date
from modules.transactions.core.entities.transaction import Transaction

class ITransactionRepository(ABC):
    @abstractmethod
    def save(self, transaction: Transaction) -> None:
        """Persiste uma transação da conta do usuário no banco."""
        pass
        
    @abstractmethod
    def find_by_user_and_date_range(self, user_id: str, start_date: date, end_date: date) -> list[Transaction]:
        """Busca todas as transações de um usuário dentro de um intervalo de datas."""
        pass
