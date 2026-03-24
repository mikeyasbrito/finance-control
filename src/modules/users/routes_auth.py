from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from modules.users.core.dtos.login_dto import LoginInputDTO, LoginOutputDTO
from modules.users.adapters.repositories.user_repository import UserRepository
from modules.users.adapters.cryptography.bcrypt_hasher import BcryptHasher
from modules.users.adapters.cryptography.jwt_adapter import PyJwtAdapter
from modules.users.use_cases.authenticate_user import AuthenticateUser
from modules.users.core.entities.value_objects import ExceptionDomain

from modules.users.routes import get_db_session

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

SECRET_KEY = "vitralis_super_secreta_chave_indescritivel"

@auth_router.post("/login", response_model=LoginOutputDTO, status_code=200)
def login_endpoint(
    input_data: LoginInputDTO,
    session: Session = Depends(get_db_session)
):
    try:
        repository = UserRepository(session)
        hasher = BcryptHasher()
        jwt_manager = PyJwtAdapter(secret_key=SECRET_KEY, expires_in_minutes=120)
        
        use_case = AuthenticateUser(repo=repository, hasher=hasher, jwt_manager=jwt_manager)
        
        output_dto = use_case.execute(input_data)
        
        return output_dto

    except ExceptionDomain as e:
        raise HTTPException(status_code=401, detail=str(e))
