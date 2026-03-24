from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from modules.users.routes import get_db_session
from modules.transactions.adapters.repositories.credit_card_repository import CreditCardRepository
from modules.transactions.use_cases.register_credit_card import RegisterCreditCard, RegisterCreditCardInputDTO
from modules.transactions.use_cases.add_credit_card_expense import AddCreditCardExpense, AddCreditCardExpenseInputDTO
from modules.users.core.entities.value_objects import ExceptionDomain

credit_card_router = APIRouter(prefix="/credit-cards", tags=["Credit Cards"])

@credit_card_router.post("/", status_code=201)
def register_card(
    input_data: RegisterCreditCardInputDTO,
    session: Session = Depends(get_db_session)
):
    try:
        repo = CreditCardRepository(session)
        use_case = RegisterCreditCard(repo)
        
        use_case.execute(input_data)
        
        return {"message": "Credit Card registered successfully."}
    except ExceptionDomain as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato Pydantic UUID, float numérico ou Date inválido.")

@credit_card_router.post("/expenses", status_code=201)
def add_expense(
    input_data: AddCreditCardExpenseInputDTO,
    session: Session = Depends(get_db_session)
):
    try:
        repo = CreditCardRepository(session)
        use_case = AddCreditCardExpense(repo)
        
        use_case.execute(input_data)
        
        return {
            "message": f"Expense divided into {input_data.total_installments} installments successfully."
        }
    except ExceptionDomain as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ValueError:
        raise HTTPException(status_code=400, detail="Formatos de Data (YYYY-MM-DD), UUID ou Float incorretos no JSON.")
