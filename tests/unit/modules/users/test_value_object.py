import pytest
from modules.users.core.entities.value_objects import Email, Password, ExceptionDomain, InvalidEmailException
from modules.users.core.interfaces.cryptography import IPasswordHasher

class MockHasher(IPasswordHasher):
    def hash(self, password: str) -> str:
        return f"hashed_{password}"
        
    def verify(self, plain: str, hashed: str) -> bool:
        return hashed == f"hashed_{plain}"

"""
    TESTES DE SENHA
"""
def test_password_should_be_created_with_strong_data():
    """
    Objetivo: Garantir que a entidade Password possa ser instanciada com uma senha de alta entropia.
    """
    # Act & Assert
    password = Password.create(plain_password="MeuCachorroVesteAzul!", hasher=MockHasher())
    assert password.value == "hashed_MeuCachorroVesteAzul!"

def test_password_should_raise_error_when_password_is_too_short():
    """
    Objetivo: Garantir que a entidade Password não possa ser instanciada com uma senha muito curta.
    """
    with pytest.raises(ExceptionDomain, match="12 or more characters"):
        Password.create(plain_password="Senha123!", hasher=MockHasher())

def test_password_should_raise_error_when_password_is_weak():
    """
    Objetivo: Garantir que senhas longas, porém previsíveis, sejam bloqueadas pelo zxcvbn.
    """
    with pytest.raises(ExceptionDomain, match="Sua senha é muito fraca"):
        Password.create(plain_password="1234567890123", hasher=MockHasher())
    
    with pytest.raises(ExceptionDomain, match="Sua senha é muito fraca"):
        Password.create(plain_password="passwordpassword", hasher=MockHasher())



"""
    TESTES DE EMAIL
"""

def test_email_should_be_created_with_valid_data():
    email = Email(value="mikeyas@example.com")
    assert email.value == "mikeyas@example.com"

def test_email_should_raise_error_when_format_is_invalid():
    # Arrange & Act & Assert
    with pytest.raises(InvalidEmailException, match="Invalid email format"):
        Email(value="mikeyas.example.com") # E-mail inválido proposital (sem @)    