from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional
from uuid import uuid4


class Role(str, Enum):
    AUTHOR = "author"
    REVIEWER = "reviewer"
    APPROVER = "approver"
    QA_ADMIN = "qa_admin"
    PRINT_CUSTODIAN = "print_custodian"
    SYSTEM_ADMIN = "system_admin"
    READ_ONLY = "read_only"


class DocumentState(str, Enum):
    DRAFT = "draft"
    REVIEW = "review"
    APPROVAL = "approval"
    EFFECTIVE = "effective"
    OBSOLETE = "obsolete"


@dataclass(frozen=True)
class User:
    user_id: str
    full_name: str
    role: Role
    password: str


@dataclass
class Signature:
    signed_by: str
    meaning: str
    comment: str
    timestamp: datetime


@dataclass
class AuditEvent:
    event_type: str
    actor: str
    timestamp: datetime
    details: Dict[str, str] = field(default_factory=dict)


@dataclass
class ControlledPrint:
    print_id: str
    copy_number: int
    printed_by: str
    printed_at: datetime
    source_version: str
    reconciled: bool = False
    reconciliation_note: Optional[str] = None


@dataclass
class DocumentVersion:
    version_id: str
    major: int
    minor: int
    content: str
    metadata: Dict[str, str]
    state: DocumentState = DocumentState.DRAFT
    signatures: List[Signature] = field(default_factory=list)
    audit_trail: List[AuditEvent] = field(default_factory=list)
    controlled_prints: List[ControlledPrint] = field(default_factory=list)


@dataclass
class Document:
    document_id: str
    title: str
    document_type: str
    department: str
    product_site: str
    versions: List[DocumentVersion] = field(default_factory=list)

    def current_version(self) -> DocumentVersion:
        if not self.versions:
            raise ValueError("Document has no versions.")
        return self.versions[-1]


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def new_identifier(prefix: str) -> str:
    return f"{prefix}-{uuid4().hex[:10]}"
