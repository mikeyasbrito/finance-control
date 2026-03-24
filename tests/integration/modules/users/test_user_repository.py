import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# Importaremos os modelos reais na Fase Green
from modules.users.adapters.repositories.models import Base, UserModel
from modules.users.adapters.repositories.user_repository import UserRepository
from modules.users.core.entities.user import User
from modules.users.core.entities.value_objects import Email, Password

# Fixture: Cria um banco SQLite na memória RAM toda vez que rodar! Rápido e Descartável.
@pytest.fixture
def db_session() -> Session:
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine) # Cria as tabelas
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    
    yield session
    
    session.close()
    Base.metadata.drop_all(engine)

def test_user_repository_should_save_and_find_user(db_session):
    # Arrange: Preparando a nossa Entidade rica
    repo = UserRepository(session=db_session)
    user = User(
        name="Teste Banco",
        email=Email("banco@example.com"),
        password=Password("SenhaMuitoF0rt3!")
    )
    
    # Act: Salvando no banco de dados e buscando de volta
    repo.save(user)
    found_user = repo.find_by_email("banco@example.com")
    
    # Assert: Se achou, não pode ser nulo e precisa ser igual ao salvo
    assert found_user is not None
    assert found_user.id == user.id
    assert found_user.email.value == "banco@example.com"
