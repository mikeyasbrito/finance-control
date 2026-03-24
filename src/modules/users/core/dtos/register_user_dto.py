from pydantic import BaseModel, EmailStr
from datetime import datetime
from uuid import UUID

# DTO de Entrada (O que o usuário vai enviar no JSON do POST)
class RegisterUserInputDTO(BaseModel):
    name: str
    email: EmailStr
    password: str
    
# DTO de Saída (O que vamos devolver na requisição, escondendo a senha!)
class RegisterUserOutputDTO(BaseModel):
    id: UUID
    name: str
    email: str
    created_at: datetime