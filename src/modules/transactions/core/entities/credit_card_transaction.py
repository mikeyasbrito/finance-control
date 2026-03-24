import uuid
from datetime import date
from dataclasses import dataclass, field
from modules.users.core.entities.value_objects import ExceptionDomain

@dataclass
class CreditCardTransaction:
    """Entidade Core que representa UMA parcela individual de uma fatura de cartão."""
    user_id: uuid.UUID
    credit_card_id: uuid.UUID
    title: str
    amount: float
    installment_number: int
    total_installments: int
    date: date # A data da Fatura de cobrança exata
    id: uuid.UUID = field(default_factory=uuid.uuid4)

    def __post_init__(self):
        # Proteção TDD contra saldos negativos inseridos via API
        if self.amount < 0:
            raise ExceptionDomain("Valor de transação do cartão não pode ser negativo.")
