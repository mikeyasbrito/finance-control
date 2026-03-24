import uuid
from datetime import date
from sqlalchemy.orm import Session
from modules.transactions.core.interfaces.repository import ITransactionRepository
from modules.transactions.core.entities.transaction import Transaction
from modules.transactions.core.entities.value_objects import TransactionAmount, TransactionType, Category
from modules.transactions.adapters.repositories.models import TransactionModel

class TransactionRepository(ITransactionRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, transaction: Transaction) -> None:
        # Desempacota o Value Object Puro -> Banco Burro
        model = TransactionModel(
            id=str(transaction.id),
            user_id=str(transaction.user_id),
            title=transaction.title,
            amount=transaction.amount.value,
            type=transaction.type,
            category=transaction.category,
            date=transaction.date,
            created_at=transaction.created_at
        )
        self.session.add(model)
        self.session.commit()

    def find_by_user_and_date_range(self, user_id: str, start_date: date, end_date: date) -> list[Transaction]:
        # ORM filtra os dados dinamicamente com as métricas do DTO de busca
        models = self.session.query(TransactionModel).filter(
            TransactionModel.user_id == user_id,
            TransactionModel.date >= start_date,
            TransactionModel.date <= end_date
        ).all()
        
        transactions = []
        for m in models:
            # Reempacota as proteções com Value Objects para devolver à aplicação
            tx = Transaction(
                id=uuid.UUID(m.id),
                user_id=uuid.UUID(m.user_id),
                title=m.title,
                amount=TransactionAmount(m.amount),
                type=m.type,
                category=m.category,
                date=m.date,
                created_at=m.created_at
            )
            transactions.append(tx)
            
        return transactions
