from __future__ import annotations

from sqlalchemy.orm import Session

from backend.audit.models import AuditEvent


def log_event(
    session: Session,
    event_type: str,
    actor: str,
    metadata: dict,
    record_type: str = "system",
    record_id: str = "n/a",
) -> AuditEvent:
    evt = AuditEvent(
        event_type=event_type,
        actor=actor,
        record_type=record_type,
        record_id=record_id,
        metadata=metadata,
    )
    session.add(evt)
    session.flush()
    return evt
