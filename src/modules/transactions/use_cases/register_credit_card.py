import uuid
from pydantic import BaseModel, UUID4
from modules.transactions.core.interfaces.credit_card_repository import ICreditCardRepository
from modules.transactions.core.entities.credit_card import CreditCard

class RegisterCreditCardInputDTO(BaseModel):
    user_id: UUID4 # Pydantic Shield
    name: str
    institution: str
    limit: float
    closing_day: int
    due_day: int

class RegisterCreditCard:
    def __init__(self, repo: ICreditCardRepository):
        self.repo = repo

    def execute(self, dto: RegisterCreditCardInputDTO) -> None:
        card = CreditCard(
            user_id=dto.user_id,
            name=dto.name,
            institution=dto.institution,
            limit=dto.limit,
            closing_day=dto.closing_day, # Validações falham aqui se dia = 35
            due_day=dto.due_day
        )
        self.repo.save_card(card)
