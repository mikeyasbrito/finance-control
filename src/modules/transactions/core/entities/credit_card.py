import uuid
from dataclasses import dataclass, field
from modules.users.core.entities.value_objects import ExceptionDomain

@dataclass
class CreditCard:
    user_id: uuid.UUID
    name: str
    institution: str
    limit: float
    closing_day: int
    due_day: int
    id: uuid.UUID = field(default_factory=uuid.uuid4)

    def __post_init__(self):
        if not (1 <= self.closing_day <= 31):
            raise ExceptionDomain("Dia de fechamento inválido.")
        if not (1 <= self.due_day <= 31):
            raise ExceptionDomain("Dia de vencimento inválido.")
