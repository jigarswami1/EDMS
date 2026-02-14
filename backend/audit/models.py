from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import DateTime, Integer, JSON, String, event
from sqlalchemy.orm import Mapped, mapped_column

from backend.db.base import Base


class AuditEvent(Base):
    __tablename__ = "audit_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_type: Mapped[str] = mapped_column(String(100), nullable=False)
    actor: Mapped[str] = mapped_column(String(100), nullable=False)
    record_type: Mapped[str] = mapped_column(String(100), nullable=False)
    record_id: Mapped[str] = mapped_column(String(100), nullable=False)
    metadata: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


@event.listens_for(AuditEvent, "before_update", propagate=True)
def _prevent_update(*_args, **_kwargs):
    raise ValueError("AuditEvent is append-only and immutable")


@event.listens_for(AuditEvent, "before_delete", propagate=True)
def _prevent_delete(*_args, **_kwargs):
    raise ValueError("AuditEvent cannot be deleted")
