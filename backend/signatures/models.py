from __future__ import annotations

from datetime import datetime


from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.db.base import Base
from backend.db.types import UTCDateTime, utcnow


class ElectronicSignature(Base):
    __tablename__ = "electronic_signatures"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    document_id: Mapped[int] = mapped_column(ForeignKey("documents.id"), nullable=False)
    version_id: Mapped[int] = mapped_column(ForeignKey("document_versions.id"), nullable=False)
    signer_username: Mapped[str] = mapped_column(String(100), nullable=False)
    meaning: Mapped[str] = mapped_column(String(255), nullable=False)
    signature_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    created_at: Mapped[datetime] = mapped_column(UTCDateTime(), default=utcnow, nullable=False)
