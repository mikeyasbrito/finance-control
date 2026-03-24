import pytest
import uuid
from datetime import date
from modules.users.core.entities.value_objects import ExceptionDomain
from modules.transactions.core.entities.credit_card_transaction import CreditCardTransaction

def test_should_create_credit_card_transaction():
    tx = CreditCardTransaction(
        user_id=uuid.uuid4(),
        credit_card_id=uuid.uuid4(),
        title="TV OLED 55",
        amount=150.00,
        installment_number=1,
        total_installments=12,
        date=date(2026, 4, 5) # Vencimento da Fatura onde a Parcela será cobrada
    )
    assert tx.title == "TV OLED 55"
    assert tx.installment_number == 1
    assert tx.total_installments == 12
    assert getattr(tx, "id", None) is not None

def test_amount_cannot_be_negative():
     with pytest.raises(ExceptionDomain, match="Valor de transação do cartão não pode ser negativo."):
         CreditCardTransaction(
             user_id=uuid.uuid4(),
             credit_card_id=uuid.uuid4(),
             title="Bug",
             amount=-10.0, # Hacker tenta colocar desconto absurdo
             installment_number=1, 
             total_installments=1,
             date=date.today()
         )
