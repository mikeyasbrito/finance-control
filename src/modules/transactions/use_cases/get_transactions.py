from datetime import date
from typing import List
from pydantic import BaseModel
from modules.transactions.core.interfaces.repository import ITransactionRepository
from modules.transactions.core.entities.value_objects import TransactionType

# O Formato visual de cada transação de volta pro FrontEnd
class TransactionOutputDTO(BaseModel):
    id: str
    title: str
    amount: float
    type: str
    category: str
    date: date

# O Formato Final do Relatório
class StatementOutputDTO(BaseModel):
    transactions: List[TransactionOutputDTO]
    total_incomes: float
    total_expenses: float
    balance: float

class GetTransactionsByDateRange:
    """Orquestrador do Relatório de Fechamento de Ciclo."""
    
    def __init__(self, repo: ITransactionRepository):
        self.repo = repo

    def execute(self, user_id: str, start_date: date, end_date: date) -> StatementOutputDTO:
        # 1. Busca os blocos puros
        domain_transactions = self.repo.find_by_user_and_date_range(user_id, start_date, end_date)
        
        dtos = []
        total_incomes = 0.0
        total_expenses = 0.0
        
        # 2. Converte os Blocos puros de volta para DTOs (Formato Serializável) e calcula métricas
        for tx in domain_transactions:
            dtos.append(
                TransactionOutputDTO(
                    id=str(tx.id),
                    title=tx.title,
                    amount=tx.amount.value,
                    type=tx.type.value,
                    category=tx.category.value,
                    date=tx.date
                )
            )
            # Acumuladores lógicos de negócio
            if tx.type == TransactionType.INCOME:
                total_incomes += tx.amount.value
            else:
                total_expenses += tx.amount.value
                
        # Rentabilidade Fria
        balance = total_incomes - total_expenses
        
        # Retorna a Fotografia Pronta para Exibir no Streamlit
        return StatementOutputDTO(
            transactions=dtos,
            total_incomes=total_incomes,
            total_expenses=total_expenses,
            balance=balance
        )
