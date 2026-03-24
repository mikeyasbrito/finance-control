import uuid
from sqlalchemy.orm import Session
from modules.transactions.core.interfaces.credit_card_repository import ICreditCardRepository
from modules.transactions.core.entities.credit_card import CreditCard
from modules.transactions.core.entities.credit_card_transaction import CreditCardTransaction
from modules.transactions.adapters.repositories.models import CreditCardModel, CreditCardTransactionModel

class CreditCardRepository(ICreditCardRepository):
    def __init__(self, session: Session):
        self.session = session

    def save_card(self, card: CreditCard) -> None:
        model = CreditCardModel(
            id=str(card.id),
            user_id=str(card.user_id),
            name=card.name,
            institution=card.institution,
            limit=card.limit,
            closing_day=card.closing_day,
            due_day=card.due_day
        )
        self.session.add(model)
        self.session.commit()

    def find_card_by_id(self, card_id: str) -> CreditCard | None:
        model = self.session.query(CreditCardModel).filter_by(id=card_id).first()
        if not model:
            return None
            
        return CreditCard(
            id=uuid.UUID(model.id),
            user_id=uuid.UUID(model.user_id),
            name=model.name,
            institution=model.institution,
            limit=model.limit,
            closing_day=model.closing_day,
            due_day=model.due_day
        )

    def save_transactions(self, transactions: list[CreditCardTransaction]) -> None:
        # Padrão Bulk Insert para varrer a lista matemática de uma vez pesando muito menos o SQlite
        models = [
            CreditCardTransactionModel(
                id=str(tx.id),
                user_id=str(tx.user_id),
                credit_card_id=str(tx.credit_card_id),
                title=tx.title,
                amount=tx.amount,
                installment_number=tx.installment_number,
                total_installments=tx.total_installments,
                date=tx.date
            ) for tx in transactions
        ]
        self.session.add_all(models)
        self.session.commit()
