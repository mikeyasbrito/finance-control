import uuid
from datetime import date, datetime, timezone
from dataclasses import dataclass, field
from modules.transactions.core.entities.value_objects import TransactionType, Category, TransactionAmount

@dataclass
class Transaction:
    user_id: uuid.UUID
    title: str
    amount: TransactionAmount
    type: TransactionType
    category: Category
    date: date
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
