from pydantic import BaseModel

class LoginInputDTO(BaseModel):
    email: str
    password: str

class LoginOutputDTO(BaseModel):
    token: str
    user_id: str
