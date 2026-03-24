from sqlalchemy.orm import Session

from modules.users.core.interfaces.repository import IUserRepository
from modules.users.core.entities.user import User
from modules.users.core.entities.value_objects import Email, Password
from modules.users.adapters.repositories.models import UserModel

class UserRepository(IUserRepository):
    """
    O Adapter Concreto.
    Assina o contrato da IUserRepository e se conecta ao SQLAlchemy.
    """
    def __init__(self, session: Session):
        self.session = session

    def save(self, user: User) -> None:
        # 1. Tradução (Descer pra Infraestrutura): Entidade Rica -> Modelo Burro de Tabela
        user_model = UserModel(
            id=user.id,
            name=user.name,
            email=user.email.value,       # Desempacota o String puro de lá de dentro
            password=user.password.value, # Desempacota o String puro da senha
            created_at=user.created_at,
            updated_at=user.updated_at
        )
        self.session.add(user_model)
        self.session.commit()

    def find_by_email(self, email: str) -> User | None:
        # Busca a linha no banco
        user_model = self.session.query(UserModel).filter_by(email=email).first()
        
        if not user_model:
            return None
            
        # 2. Tradução (Subir para o Domínio): Modelo Burro Tabela -> Entidade Rica
        return User(
            id=user_model.id,
            name=user_model.name,
            email=Email(value=user_model.email),       # Reconstrói e valida na Entidade Rica
            password=Password(value=user_model.password), 
            created_at=user_model.created_at,
            updated_at=user_model.updated_at
        )

