import jwt
from datetime import datetime, timedelta, timezone
from modules.users.core.interfaces.jwt_manager import IJwtManager
from modules.users.core.entities.value_objects import ExceptionDomain

class PyJwtAdapter(IJwtManager):
    def __init__(self, secret_key: str, algorithm: str = "HS256", expires_in_minutes: int = 60):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expires_in_minutes = expires_in_minutes

    def generate_token(self, user_id: str) -> str:
        # A carga pendurada no crachá (Identity + Quando o crachá vence)
        payload = {
            "sub": user_id,
            "exp": datetime.now(timezone.utc) + timedelta(minutes=self.expires_in_minutes)
        }
        
        # O chaveiro assinando nosso token
        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        return token
        
    def verify_token(self, token: str) -> dict:
        try:
            # Tenta decifrar o token. O 'decode' também checa o 'exp' automaticamente.
            decoded = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return decoded
        except jwt.ExpiredSignatureError:
            raise ExceptionDomain("Sessão expirada. Faça login novamente.")
        except jwt.InvalidTokenError:
            raise ExceptionDomain("Token de acesso inválido ou falsificado.")
