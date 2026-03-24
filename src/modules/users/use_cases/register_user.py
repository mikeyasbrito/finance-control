from modules.users.core.entities.user import User
from modules.users.core.entities.value_objects import Email, Password, ExceptionDomain
from modules.users.core.interfaces.repository import IUserRepository
from modules.users.core.interfaces.cryptography import IPasswordHasher
from modules.users.core.dtos.register_user_dto import RegisterUserInputDTO, RegisterUserOutputDTO

class RegisterUser:
    """
    O Use Case (Camada de Aplicação). 
    Ele não sabe qual banco de dados usamos, nem qual lib de hash é usada.
    Ele confia cegamente nas Injeções de Dependências das Interfaces!
    """

    def __init__(self, repository: IUserRepository, hasher: IPasswordHasher):
        self.repository = repository
        self.hasher = hasher

    def execute(self, input_dto: RegisterUserInputDTO) -> RegisterUserOutputDTO:
        # 1. Regra de Negócio Pura: O e-mail não pode ser repetido
        user_already_exists = self.repository.find_by_email(email=input_dto.email)
        if user_already_exists:
            raise ExceptionDomain("This email is already in use.")
        
        # 2. Transforma as strings cruas do DTO nos Value Objects blindados
        email_vo = Email(value=input_dto.email)
        
        # 3. Valida a senha limpa gerando o Hash dentro do domínio do VO
        password_vo = Password.create(plain_password=input_dto.password, hasher=self.hasher)
        
        # 4. Instancia a Entidade User Rica (ID e Timestamp serão gerados por ela sozinha!)
        new_user = User(
            name=input_dto.name,
            email=email_vo,
            password=password_vo
        )
        
        # 5. Manda a interface do repositório salvar esse objeto rico
        self.repository.save(new_user)
        
        # 6. Retorna o DTO de saída, expondo apenas o que o frontend pode ver (nada de senha)
        return RegisterUserOutputDTO(
            id=new_user.id,
            name=new_user.name,
            email=new_user.email.value,
            created_at=new_user.created_at
        )
