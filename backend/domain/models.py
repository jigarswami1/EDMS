"""Initial EDMS domain entities used by application modules."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class DocumentState(str, Enum):
    DRAFT = "draft"
    IN_REVIEW = "in_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    EFFECTIVE = "effective"
    ARCHIVED = "archived"


@dataclass(slots=True)
class Document:
    document_id: str
    title: str
    owner_id: str
    state: DocumentState = DocumentState.DRAFT
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass(slots=True)
class DocumentVersion:
    version_id: str
    document_id: str
    version_number: int
    content_ref: str
    checksum: str
    created_by: str
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass(slots=True)
class WorkflowInstance:
    workflow_id: str
    document_id: str
    current_step: str
    reviewers: list[str] = field(default_factory=list)
    status: str = "pending"
    updated_at: datetime = field(default_factory=datetime.utcnow)


@dataclass(slots=True)
class SignatureEvent:
    event_id: str
    document_id: str
    version_id: str
    signer_id: str
    outcome: str
    signature_provider: str
    occurred_at: datetime = field(default_factory=datetime.utcnow)


@dataclass(slots=True)
class PrintEvent:
    event_id: str
    document_id: str
    version_id: str
    requested_by: str
    quantity: int
    issued_quantity: int = 0
    reconciled: bool = False
    occurred_at: datetime = field(default_factory=datetime.utcnow)


@dataclass(slots=True)
class AuditEntry:
    entry_id: str
    document_id: str
    actor_id: str
    action: str
    metadata: dict[str, Any] = field(default_factory=dict)
    occurred_at: datetime = field(default_factory=datetime.utcnow)


@dataclass(slots=True)
class RoleAssignment:
    assignment_id: str
    principal_id: str
    role: str
    scope: str
    granted_by: str
    granted_at: datetime = field(default_factory=datetime.utcnow)
