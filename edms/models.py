from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import List


class Role(str, Enum):
    AUTHOR = "author"
    REVIEWER = "reviewer"
    APPROVER = "approver"


class DocumentState(str, Enum):
    DRAFT = "draft"
    REVIEW = "review"
    APPROVED = "approved"


@dataclass(frozen=True)
class User:
    user_id: str
    full_name: str
    role: Role


@dataclass
class AuditEvent:
    action: str
    actor: str
    timestamp: datetime
    comment: str = ""


@dataclass
class Document:
    document_id: str
    title: str
    content: str
    state: DocumentState = DocumentState.DRAFT
    audit_trail: List[AuditEvent] = field(default_factory=list)


def utc_now() -> datetime:
    return datetime.now(timezone.utc)
