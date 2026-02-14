from __future__ import annotations

from datetime import datetime
from enum import Enum
import secrets

from sqlalchemy import Enum as SQLEnum, Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from backend.db.base import Base
from backend.db.types import UTCDateTime, utcnow


class Role(str, Enum):
    AUTHOR = "Author"
    REVIEWER = "Reviewer"
    APPROVER = "Approver"
    ADMIN = "Admin"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(500), nullable=False)
    role: Mapped[Role] = mapped_column(SQLEnum(Role), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(UTCDateTime(), default=utcnow, nullable=False)


class UserSession(Base):
    __tablename__ = "user_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    session_id: Mapped[str] = mapped_column(String(64), unique=True, default=lambda: secrets.token_hex(16), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    issued_at: Mapped[datetime] = mapped_column(UTCDateTime(), default=utcnow, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(UTCDateTime(), nullable=False)
    revoked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
