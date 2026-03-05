import pytest
from modules.users.entities.user import User

def test_user_should_be_created_with_valid_data():
    """
    Objetivo: Garantir que a entidade User possa ser instanciada com dados válidos.
    Este é o teste mais simples possível para iniciar o domínio.
    """
    # Arrange
    name = "Mikeyas Brito"
    email = "mikeyas@example.com"
    password = "securepassword123"

    # Act
    user = User(name=name, email=email, password=password)

    # Assert
    assert user.name == name
    assert user.email == email
    assert user.password == password


def test_user_should_raise_error_when_email_is_invalid():
    """
    Objetivo: Garantir que a entidade User não possa ser instanciada com um e-mail inválido.
    """
    # Arrange
    name = "Mikeyas Brito"
    email = "mikeyasexample.com"
    password = "securepassword123"

    # act
    with pytest.raises(ValueError, match="Invalid email format"):
        user = User(name=name, email=email, password=password)
        
@pytest.mark.parametrize("invalid_email", [
    "mikeyas@",             # Falta o domínio
    "@example.com",         # Falta o nome
    "mikeyas@domain",       # Falta a extensão (.com, .com.br)
    "mikeyas @example.com", # Tem espaço interno
    "mikeyas..@example.com",
    "mikeyas+@example.com",     # Pontos duplicados
    "mikeyas@dom-ain.com.br",   # Domínio com hífen
    "Mikeyas@example@gmail.@com"
])
def test_user_should_raise_error_when_email_is_invalid(invalid_email):
    """
    Objetivo: Garantir que a entidade User não possa ser instanciada com um e-mail inválido.
    """
    # Arrange
    name = "Mikeyas Brito"
    email = invalid_email
    password = "securepassword123"

    # act
    with pytest.raises(ValueError, match="Invalid email format"):
        user = User(name=name, email=email, password=password)