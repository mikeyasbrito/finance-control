import uuid
from sqlalchemy import Column, String, Float, Integer, Date, DateTime, Enum as SQLEnum
from modules.users.adapters.repositories.models import Base
from modules.transactions.core.entities.value_objects import TransactionType, Category

class TransactionModel(Base):
    __tablename__ = "transactions"

    # UUIDs no SQLite são salvos como String nativamente
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, index=True, nullable=False) # Chave estrangeira conceitual
    title = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    type = Column(SQLEnum(TransactionType), nullable=False)
    category = Column(SQLEnum(Category), nullable=False)
    date = Column(Date, nullable=False)
    created_at = Column(DateTime, nullable=False)

class CreditCardModel(Base):
    __tablename__ = "credit_cards"

    id = Column(String, primary_key=True)
    user_id = Column(String, index=True, nullable=False)
    name = Column(String, nullable=False)
    institution = Column(String, nullable=False)
    limit = Column(Float, nullable=False)
    closing_day = Column(Integer, nullable=False)
    due_day = Column(Integer, nullable=False)

class CreditCardTransactionModel(Base):
    __tablename__ = "credit_card_transactions"
    
    id = Column(String, primary_key=True)
    user_id = Column(String, index=True, nullable=False)
    credit_card_id = Column(String, index=True, nullable=False)
    title = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    installment_number = Column(Integer, nullable=False)
    total_installments = Column(Integer, nullable=False)
    date = Column(Date, index=True, nullable=False)
