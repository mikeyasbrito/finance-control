import pytest
import uuid
from datetime import date
from modules.transactions.core.services.installment_generator import InstallmentGenerator

def test_should_generate_installments_correctly():
    installments = InstallmentGenerator.generate(
        user_id=uuid.uuid4(),
        credit_card_id=uuid.uuid4(),
        title="TV OLED",
        total_amount=300.00,
        total_installments=3,
        first_due_date=date(2026, 4, 15)
    )
    
    assert len(installments) == 3
    assert installments[0].amount == 100.00
    assert installments[0].date == date(2026, 4, 15)
    assert installments[0].title == "TV OLED (1/3)"
    
    assert installments[1].amount == 100.00
    assert installments[1].date == date(2026, 5, 15)
    
    assert installments[2].amount == 100.00
    assert installments[2].date == date(2026, 6, 15)

def test_should_adjust_cent_rounding_in_last_installment_to_prevent_money_loss():
    # R$ 100.0 / 3 parcelas = 33.33333... O Financeiro não pode perder o último centavo de R$ 99,99!
    installments = InstallmentGenerator.generate(
        user_id=uuid.uuid4(),
        credit_card_id=uuid.uuid4(),
        title="Camisa",
        total_amount=100.00,
        total_installments=3,
        first_due_date=date(2026, 4, 1)
    )
    
    assert installments[0].amount == 33.33
    assert installments[1].amount == 33.33
    assert installments[2].amount == 33.34 # Fatura final engole o 1 centavo extra

def test_should_calculate_leap_years_and_shorter_months_correctly():
    # Fevereiro tem 28 dias. Compra fechada no dia 31 de Janeiro deve cair no último dia de Fevereiro.
    installments = InstallmentGenerator.generate(
        user_id=uuid.uuid4(),
        credit_card_id=uuid.uuid4(),
        title="Iphone",
        total_amount=100.00,
        total_installments=2,
        first_due_date=date(2026, 1, 31)
    )
    # Parcela 1: 31 de Janeiro
    assert installments[0].date == date(2026, 1, 31)
    # Parcela 2: Pula magicamente para dia 28 de Fevereiro de 2026!
    assert installments[1].date == date(2026, 2, 28)
