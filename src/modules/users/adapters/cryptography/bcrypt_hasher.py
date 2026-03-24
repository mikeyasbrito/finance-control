import bcrypt
from modules.users.core.interfaces.cryptography import IPasswordHasher

class BcryptHasher(IPasswordHasher):
    """
    Este é o Adapter Concreto.
    Ele implementa a interface IPasswordHasher exigida pelo core/ e
    encapsula a lib externa 'bcrypt'.
    """

    def hash(self, password: str) -> str:
        # Pega a string plana e converte para bytes (que é como o bcrypt gosta)
        pwd_bytes = password.encode('utf-8')
        
        # Gera o tempero de criptografia
        salt = bcrypt.gensalt()
        
        # Gera o hash final
        hashed_bytes = bcrypt.hashpw(pwd_bytes, salt)
        
        # Retorna formatado em string para os nossos value objects e banco
        return hashed_bytes.decode('utf-8')

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        """
        Recebe a senha crua e o hash salvo no banco. 
        Retorna True caso a senha pertença ao hash.
        """
        return bcrypt.checkpw(
            plain_password.encode('utf-8'), 
            hashed_password.encode('utf-8')
        )
