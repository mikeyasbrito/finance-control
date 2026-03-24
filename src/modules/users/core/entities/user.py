from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional
from uuid import UUID, uuid4

from modules.users.core.entities.value_objects import Email, Password

@dataclass(kw_only=True)
class User:
    """
    A Entidade Rica do Usuário. Ela é a base de tudo no módulo 'users'.
    O kw_only=True obriga que sempre passemos os nomes (ex: name="Mikeyas") na criação,
    evitando inverter a ordem dos parâmetros sem querer.
    """
    name: str
    email: Email
    password: Password
    
    # ID gerado automaticamente. default_factory garante uma execução nova do uuid4() para todo novo User
    id: UUID = field(default_factory=uuid4)
    
    # Data de criação auto-gerada em UTC (Universal Time Coordinated)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    # O updated_at inicia nulo, pois na criação ainda não houve alteração
    updated_at: Optional[datetime] = None