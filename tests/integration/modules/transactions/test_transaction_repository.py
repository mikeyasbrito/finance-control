import pytest
import uuid
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from modules.users.adapters.repositories.models import Base
from modules.transactions.adapters.repositories.transaction_repository import TransactionRepository
from modules.transactions.core.entities.transaction import Transaction
from modules.transactions.core.entities.value_objects import TransactionAmount, TransactionType, Category

@pytest.fixture
def sqlite_session():
    # Banco Volátil Fresquinho
    engine = create_engine("sqlite:///:memory:")
    # Importante pro Base recriar a tabela transações em memória:
    from modules.transactions.adapters.repositories.models import TransactionModel 
    Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_repository_should_save_and_find_by_date_range(sqlite_session):
    repo = TransactionRepository(sqlite_session)
    user_id = uuid.uuid4()
    
    # 1. Transação Fora do Range (Antiga - Fevereiro)
    tx_old = Transaction(
        user_id=user_id,
        title="Restaurante",
        amount=TransactionAmount(100.0),
        type=TransactionType.EXPENSE,
        category=Category.OTHER,
        date=date(2026, 2, 1) # Fevereiro
    )
    repo.save(tx_old)
    
    # 2. Transação Dentro do Range (Março)
    tx_target = Transaction(
        user_id=user_id,
        title="Salário",
        amount=TransactionAmount(5000.0),
        type=TransactionType.INCOME,
        category=Category.SALARY,
        date=date(2026, 3, 10) # Março
    )
    repo.save(tx_target)
    
    # Busca de Dia 03 de Março a Dia 02 de Abril (O fechamento vitralis)
    start_date = date(2026, 3, 3)
    end_date = date(2026, 4, 2)
    
    results = repo.find_by_user_and_date_range(str(user_id), start_date, end_date)
    
    # O Banco deve ter filtrado e ignorado a transação de fevereiro!
    assert len(results) == 1
    assert results[0].title == "Salário"
    assert results[0].amount.value == 5000.0
    assert results[0].type == TransactionType.INCOME
