from abc import ABC, abstractmethod
from modules.transactions.core.entities.credit_card import CreditCard
from modules.transactions.core.entities.credit_card_transaction import CreditCardTransaction

class ICreditCardRepository(ABC):
    @abstractmethod
    def save_card(self, card: CreditCard) -> None:
        """Salva a entidade de controle isolada do cartão no sistema."""
        pass
        
    @abstractmethod
    def find_card_by_id(self, card_id: str) -> CreditCard | None:
        pass

    @abstractmethod
    def save_transactions(self, transactions: list[CreditCardTransaction]) -> None:
        """Salva múltiplas parcelas geradas pelo motor matemático de uma vez só! (Bulk Insert)"""
        pass
