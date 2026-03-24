import uuid
from datetime import date
from pydantic import BaseModel, UUID4
from modules.transactions.core.interfaces.repository import ITransactionRepository
from modules.transactions.core.entities.transaction import Transaction
from modules.transactions.core.entities.value_objects import TransactionAmount, TransactionType, Category

class CreateTransactionInputDTO(BaseModel):
    user_id: UUID4
    title: str
    amount: float
    type: str
    category: str
    date: date

class CreateTransaction:
    """Orquestrador da criação de uma nova transação financeira no sistema."""
    
    def __init__(self, repo: ITransactionRepository):
        self.repo = repo

    def execute(self, dto: CreateTransactionInputDTO) -> None:
        # Desempacota o DTO da web e converte para a Entidade de Negócio segura
        # Erros como Strings inválidas ou valores negativos no DTO vão quebrar
        # O Pydantic já validou e transformou o UUID na porta de entrada!
        transaction = Transaction(
            user_id=dto.user_id,
            title=dto.title,
            amount=TransactionAmount(dto.amount),
            type=TransactionType(dto.type), 
            category=Category(dto.category),
            date=dto.date
        )
        
        # O Repositório cuida apenas de inserir a entidade impecável no banco.
        self.repo.save(transaction)
