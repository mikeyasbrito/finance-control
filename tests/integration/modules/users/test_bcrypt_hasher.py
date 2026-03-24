from modules.users.adapters.cryptography.bcrypt_hasher import BcryptHasher

def test_should_hash_password_successfully():
    # Arrange
    hasher = BcryptHasher()
    plain_password = "MinhaSenha123"
    
    # Act
    hashed_password = hasher.hash(plain_password)
    
    # Assert
    # O hash nunca pode ser igual à senha original
    assert hashed_password != plain_password
    # O formato padrão do Bcrypt sempre começa com $2b$
    assert hashed_password.startswith("$2b$")
