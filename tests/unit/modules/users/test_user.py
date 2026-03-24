import pytest
from uuid import UUID
from datetime import datetime

# Importamos os Value Objects que já estão prontos
from modules.users.core.entities.value_objects import Email, Password

# Este import vai falhar, pois a classe User ainda não existe (Isso é esperado no TDD!)
from modules.users.core.entities.user import User

def test_user_should_be_created_with_valid_data():
    """
    Objetivo: Garantir que a entidade User possa ser instanciada via construtor com os dados válidos,
    e que ela mesma seja responsável por gerar o seu UUID e Timestamp de criação.
    """
    # Arrange
    email = Email(value="mikeyas@example.com")
    password = Password(value="Senha@Forte123")
    
    # Act
    user = User(
        name="Mikeyas Brito",
        email=email,
        password=password
    )
    
    # Assert
    assert isinstance(user.id, UUID)  # O ID deve ser auto-gerado como um UUID
    assert user.name == "Mikeyas Brito"
    assert user.email == email
    assert user.password == password
    assert isinstance(user.created_at, datetime)  # A data de criação deve ser instanciada automaticamente
    assert user.updated_at is None  # Não houve atualização ainda, então deve ser nulo
