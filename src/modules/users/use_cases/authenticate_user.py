from modules.users.core.interfaces.repository import IUserRepository
from modules.users.core.interfaces.cryptography import IPasswordHasher
from modules.users.core.interfaces.jwt_manager import IJwtManager
from modules.users.core.dtos.login_dto import LoginInputDTO, LoginOutputDTO
from modules.users.core.entities.value_objects import ExceptionDomain

class AuthenticateUser:
    """
    Caso de Uso (Camada de Aplicação).
    Orquestra o processo de Login sem acoplamento.
    """
    def __init__(
        self, 
        repo: IUserRepository, 
        hasher: IPasswordHasher, 
        jwt_manager: IJwtManager
    ):
        self.repo = repo
        self.hasher = hasher
        self.jwt_manager = jwt_manager

    def execute(self, input_dto: LoginInputDTO) -> LoginOutputDTO:
        # 1. Pede ao Repositório para buscar o E-mail
        user = self.repo.find_by_email(input_dto.email)
        
        # 2. Segurança em Primeiro Lugar: Se não achou, diga apenas "Credenciais Inválidas"
        if not user:
            raise ExceptionDomain("Credenciais Inválidas.")
            
        # 3. Pede ao Especialista em Criptografia (Hashes) para comparar a senha fornecida
        is_password_correct = self.hasher.verify(
            plain_password=input_dto.password, 
            hashed_password=user.password.value
        )
        
        # 4. Se a senha for mentirosa, lance o mesmíssimo erro genérico
        if not is_password_correct:
            raise ExceptionDomain("Credenciais Inválidas.")
            
        # 5. E-mail e Senha batem! Peça ao Chaveiro (Manager) para fabricar o Crachá (JWT)
        token = self.jwt_manager.generate_token(user_id=str(user.id))
        
        # 6. Devolva o Token ao cliente no formato blindado
        return LoginOutputDTO(token=token, user_id=str(user.id))
