from datetime import date
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

# Conexão global
from modules.users.routes import get_db_session

# Componentes de Transação
from modules.transactions.adapters.repositories.transaction_repository import TransactionRepository
from modules.transactions.use_cases.create_transaction import CreateTransaction, CreateTransactionInputDTO
from modules.transactions.use_cases.get_transactions import GetTransactionsByDateRange, StatementOutputDTO
from modules.users.core.entities.value_objects import ExceptionDomain

transaction_router = APIRouter(prefix="/transactions", tags=["Transactions"])

@transaction_router.post("/", status_code=201)
def add_transaction(
    input_data: CreateTransactionInputDTO,
    session: Session = Depends(get_db_session)
):
    try:
        # Dependency Injection Manual
        repo = TransactionRepository(session)
        use_case = CreateTransaction(repo)
        
        use_case.execute(input_data)
        return {"message": "Transaction created successfully."}
    except ExceptionDomain as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ValueError as e:
        # Pydantic breaks se Enums/Tipos vierem errados
        raise HTTPException(status_code=400, detail="Valores inválidos (Ex: Type ou Categoria inexistente).")

@transaction_router.get("/{user_id}/statement", response_model=StatementOutputDTO)
def get_statement(
    user_id: str,
    start_date: date = Query(..., description="Data Inicial do Mapeamento"),
    end_date: date = Query(..., description="Data Final do Relatório"),
    session: Session = Depends(get_db_session)
):
    repo = TransactionRepository(session)
    use_case = GetTransactionsByDateRange(repo)
    return use_case.execute(user_id=user_id, start_date=start_date, end_date=end_date)
