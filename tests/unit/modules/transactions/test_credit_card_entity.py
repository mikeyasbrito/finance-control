import pytest
import uuid
from modules.users.core.entities.value_objects import ExceptionDomain
# Importação na fase Red: A classe sequer existe ainda!
from modules.transactions.core.entities.credit_card import CreditCard

def test_should_create_valid_credit_card():
    user_id = uuid.uuid4()
    
    card = CreditCard(
        user_id=user_id,
        name="Clonado Black Platinum",
        institution="Nubank",
        limit=15000.00,
        closing_day=25, # Dia que a fatura fecha
        due_day=5       # Dia que a fatura vence
    )
    
    assert card.name == "Clonado Black Platinum"
    assert card.institution == "Nubank"
    assert card.limit == 15000.00
    assert card.closing_day == 25
    assert card.id is not None

def test_should_raise_error_when_closing_day_is_invalid():
    # Garantia de domínio: O dia de fechamento deve ser válido num calendário!
    with pytest.raises(ExceptionDomain, match="Dia de fechamento inválido."):
        CreditCard(user_id=uuid.uuid4(), name="Black", institution="Inter", limit=100.0, closing_day=35, due_day=5)
        
    with pytest.raises(ExceptionDomain, match="Dia de vencimento inválido."):
        CreditCard(user_id=uuid.uuid4(), name="Black", institution="Inter", limit=100.0, closing_day=25, due_day=0)
