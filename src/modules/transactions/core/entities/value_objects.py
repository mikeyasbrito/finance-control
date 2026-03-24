from enum import Enum
from dataclasses import dataclass
from modules.users.core.entities.value_objects import ExceptionDomain

class TransactionType(Enum):
    INCOME = "INCOME"
    EXPENSE = "EXPENSE"

class Category(Enum):
    SALARY = "SALARY"
    FOOD = "FOOD"
    TRANSPORT = "TRANSPORT"
    LEISURE = "LEISURE"
    HEALTH = "HEALTH"
    OTHER = "OTHER"

@dataclass
class TransactionAmount:
    value: float

    def __post_init__(self):
        if self.value < 0:
            raise ExceptionDomain("O valor da transação não pode ser nulo ou negativo.")
