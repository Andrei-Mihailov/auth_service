# models/entity.py
import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID

from db.postgres_db import Base
from services.utils import hash_password, validate_password


class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True),
                primary_key=True,
                default=uuid.uuid4,
                unique=True,
                nullable=False)
    login = Column(String(255),
                   unique=True,
                   nullable=False)
    password = Column(String(255),
                      nullable=False)
    first_name = Column(String(50))
    last_name = Column(String(50))
    created_at = Column(DateTime,
                        default=datetime.now)
    active = Column(Boolean,
                    default=True)

    def __init__(self,
                 login: str,
                 password: str,
                 first_name: str,
                 last_name: str) -> None:
        self.login = login
        self.password = hash_password(password)
        self.first_name = first_name
        self.last_name = last_name

    def check_password(self, password: str) -> bool:
        return validate_password(self.password, password)

    def __repr__(self) -> str:
        return f'<User {self.login}>'
