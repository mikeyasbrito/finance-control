from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Importamos a nossa rota modular isolada e a Base das nossas tabelas
from modules.users.routes import router as users_router
from modules.users.adapters.repositories.models import Base
from modules.users.adapters.repositories.models import UserModel
from modules.transactions.adapters.repositories.models import TransactionModel, CreditCardModel, CreditCardTransactionModel

# Para fins didáticos e práticos, usaremos um SQLite em arquivo local
# Num ambiente real, puxaremos a string de conexão (ex: "postgresql://...") das variáveis de ambiente na pasta config/!
SQLALCHEMY_DATABASE_URL = "sqlite:///./finance_system.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Fabrica as tabelas no arquivo gerado
Base.metadata.create_all(bind=engine)

# Inicia o Servidor FastAPI mestre
app = FastAPI(
    title="Finance System API",
    description="Primeira Fatia Vertical com Clean Architecture",
    version="1.0.0"
)

# Conecta os roteadores na aplicação mestre
app.include_router(users_router)

from modules.users.routes_auth import auth_router
app.include_router(auth_router)

from modules.transactions.routes import transaction_router
app.include_router(transaction_router)

from modules.transactions.routes_credit_cards import credit_card_router
app.include_router(credit_card_router)

# Lembra da função get_db_session vazia lá na rota? 
# Nós interceptamos (Dependency Override) a injeção do FastAPI e mandamos a do nosso banco de verdade
def get_real_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from modules.users.routes import get_db_session
app.dependency_overrides[get_db_session] = get_real_db_session
