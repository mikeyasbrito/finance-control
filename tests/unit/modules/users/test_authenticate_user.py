import pytest
from modules.users.core.dtos.login_dto import LoginInputDTO, LoginOutputDTO
from modules.users.core.entities.user import User
from modules.users.core.entities.value_objects import Email, Password, ExceptionDomain
from modules.users.core.interfaces.repository import IUserRepository
from modules.users.core.interfaces.jwt_manager import IJwtManager
from modules.users.core.interfaces.cryptography import IPasswordHasher

# O Nosso Import da Fase Red:
from modules.users.use_cases.authenticate_user import AuthenticateUser

# Criando "Atores Falsos" Rápidos
class MockHasher(IPasswordHasher):
    # Hasher só devolve string fixa
    def hash(self, password: str) -> str: return f"hashed_{password}"
    # NOVO MÉTODO (Importante p/ o login): verificar se a senha bate com o banco
    def verify(self, plain_password: str, hashed_password: str) -> bool: return f"hashed_{plain_password}" == hashed_password

class MockJwt(IJwtManager):
    def generate_token(self, user_id: str) -> str: return f"fake_token_for_{user_id}"
    def verify_token(self, token: str) -> dict: return {}

class MockRepo(IUserRepository):
    def save(self, user: User) -> None: pass
    def find_by_email(self, email: str) -> User | None:
        if email == "existente@example.com":
            return User(name="Teste", email=Email("existente@example.com"), password=Password.create("SenhaReal123!", MockHasher()))
        return None

def test_should_authenticate_and_return_token_when_credentials_are_valid():
    # Arrange
    use_case = AuthenticateUser(repo=MockRepo(), hasher=MockHasher(), jwt_manager=MockJwt())
    input_dto = LoginInputDTO(email="existente@example.com", password="SenhaReal123!")

    # Act
    output = use_case.execute(input_dto)

    # Assert
    assert isinstance(output, LoginOutputDTO)
    assert output.token.startswith("fake_token_for_")
    assert output.user_id is not None

def test_should_raise_error_when_email_not_found_or_wrong_password():
    use_case = AuthenticateUser(repo=MockRepo(), hasher=MockHasher(), jwt_manager=MockJwt())

    # Se a senha for fraca, forte ou errada, o erro é genérico p/ não dar dicas ao hacker!
    with pytest.raises(ExceptionDomain, match="Credenciais Inválidas."):
        use_case.execute(LoginInputDTO(email="existente@example.com", password="SenhaIncorreta99"))

    with pytest.raises(ExceptionDomain, match="Credenciais Inválidas."):
        use_case.execute(LoginInputDTO(email="naoexiste@example.com", password="QualquerSenha123!"))
