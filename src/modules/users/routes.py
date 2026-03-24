from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from modules.users.core.dtos.register_user_dto import RegisterUserInputDTO, RegisterUserOutputDTO
from modules.users.adapters.repositories.user_repository import UserRepository
from modules.users.adapters.cryptography.bcrypt_hasher import BcryptHasher
from modules.users.use_cases.register_user import RegisterUser
from modules.users.core.entities.value_objects import ExceptionDomain

def get_db_session():
    # Isso será sobreescrito no "main" para repassar uma sessão real do banco
    pass

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=RegisterUserOutputDTO, status_code=201)
def register_user_endpoint(
    input_data: RegisterUserInputDTO,
    session: Session = Depends(get_db_session)
):
    try:
        repository = UserRepository(session)
        hasher = BcryptHasher()
        
        use_case = RegisterUser(repository=repository, hasher=hasher)
        output_dto = use_case.execute(input_data)
        
        return output_dto

    except ExceptionDomain as e:
        raise HTTPException(status_code=400, detail=str(e))
