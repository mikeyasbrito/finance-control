import pytest
from modules.users.core.entities.value_objects import Email, Password, ExceptionDomain, InvalidEmailException

"""
    TESTES DE SENHA
"""
def test_password_should_be_created_with_valid_data():
    """
    Objetivo: Garantir que a entidade Password possa ser instanciada com dados válidos.
    """
    # Act & Assert (Se não lançar exceção, o teste passa)
    password = Password(value="Senha@Forte123")
    assert password.value == "Senha@Forte123"

def test_password_should_raise_error_when_password_is_too_short():
    """
    Objetivo: Garantir que a entidade Password não possa ser instanciada com uma senha muito curta.
    """
    with pytest.raises(ExceptionDomain, match="12 or more charactere"):
        Password(value="curta@1B")

def test_password_should_raise_error_when_password_does_not_contain_uppercase_letter():
    """
    Objetivo: Garantir que a entidade Password não possa ser instanciada com uma senha que não contém uma letra maiúscula.
    """
    with pytest.raises(ExceptionDomain, match="uppercase letter"):
        Password(value="senasem_maiuscula@123")

def test_password_should_raise_error_when_password_does_not_contain_lowercase_letter():
    """
    Objetivo: Garantir que a entidade Password não possa ser instanciada com uma senha que não contém uma letra minúscula.
    """
    with pytest.raises(ExceptionDomain, match="lowercase letter"):
        Password(value="SENHASEM_MINUSCULA@123")

def test_password_should_raise_error_when_password_does_not_contain_number():
    """
    Objetivo: Garantir que a entidade Password não possa ser instanciada com uma senha que não contém um número.
    """
    with pytest.raises(ExceptionDomain, match="at least one number"):
        Password(value="SenhaSemNumero@Aqui")

def test_password_should_raise_error_when_password_does_not_contain_special_character():
    """
    Objetivo: Garantir que a entidade Password não possa ser instanciada com uma senha que não contém um caractere especial.
    """
    with pytest.raises(ExceptionDomain, match="special charactere"):
        Password(value="SenhaSemEspecial123")


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