import pytest
from uuid import UUID
from datetime import datetime

from modules.users.core.dtos.register_user_dto import RegisterUserInputDTO, RegisterUserOutputDTO
from modules.users.core.interfaces.repository import IUserRepository
from modules.users.core.interfaces.cryptography import IPasswordHasher
from modules.users.core.entities.user import User

# O Import abaixo vai falhar na Fase RED, pois o Use Case não existe
from modules.users.use_cases.register_user import RegisterUser

class MockUserRepository(IUserRepository):
    def __init__(self):
        self.saved_users = []

    def save(self, user: User) -> None:
        self.saved_users.append(user)

    def find_by_email(self, email: str) -> User | None:
        for u in self.saved_users:
            if u.email.value == email:
                return u
        return None

class MockPasswordHasher(IPasswordHasher):
    def hash(self, password: str) -> str:
        return f"hashed_{password}"
        
    def verify(self, plain: str, hashed: str) -> bool:
        return hashed == f"hashed_{plain}"

def test_should_register_new_user_successfully():
    # Arrange (Preparação das dependências e da entrada falsa)
    mock_repo = MockUserRepository()
    mock_hasher = MockPasswordHasher()
    
    use_case = RegisterUser(repository=mock_repo, hasher=mock_hasher)
    
    input_dto = RegisterUserInputDTO(
        name="Mikeyas",
        email="mikeyas@example.com",
        password="SenhaSecretaForte123!" # Senha forte pro zxcvbn não chorar
    )

    # Act (Ação: Mandamos o Caso de Uso registrar o usuário)
    output_dto = use_case.execute(input_dto)

    # Assert (A validação do que esperamos que o gerente tenha feito)
    assert isinstance(output_dto, RegisterUserOutputDTO)
    assert output_dto.name == "Mikeyas"
    assert output_dto.email == "mikeyas@example.com"
    
    # O Caso de uso fez a entidade salvar no "banco falso"?
    assert len(mock_repo.saved_users) == 1
    
    # O Caso de Uso chamou o Hasher para não deixar a senha pura?
    saved_user = mock_repo.saved_users[0]
    assert saved_user.password.value == "hashed_SenhaSecretaForte123!"

