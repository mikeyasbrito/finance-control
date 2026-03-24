from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy import String
from uuid import UUID
from datetime import datetime

# Essa é a classe base do SQLAlchemy (nossa fábrica de tabelas)
Base = declarative_base()

class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(150), unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(String(200), nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False)
    updated_at: Mapped[datetime] = mapped_column(nullable=True)
