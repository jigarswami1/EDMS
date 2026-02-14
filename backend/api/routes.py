"""Core EDMS API route stubs.

These handlers are intentionally skeletal and serve as integration points for
future HTTP framework wiring.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class RouteStub:
    method: str
    path: str
    action: str


ROUTES: tuple[RouteStub, ...] = (
    RouteStub("POST", "/documents/drafts", "create_draft"),
    RouteStub("POST", "/documents/{document_id}/review", "submit_review"),
    RouteStub("POST", "/documents/{document_id}/decisions", "approve_reject"),
    RouteStub("POST", "/documents/{document_id}/effective", "make_effective"),
    RouteStub("POST", "/prints/requests", "request_print"),
    RouteStub("POST", "/prints/issues", "issue_print"),
    RouteStub("POST", "/prints/{print_event_id}/reconcile", "reconcile_print"),
    RouteStub("GET", "/documents/{document_id}/audit-trail", "retrieve_audit_trail"),
)


def create_draft(payload: dict[str, Any]) -> dict[str, Any]:
    return {"status": "not_implemented", "action": "create_draft", "payload": payload}


def submit_review(document_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "status": "not_implemented",
        "action": "submit_review",
        "document_id": document_id,
        "payload": payload,
    }


def approve_reject(document_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "status": "not_implemented",
        "action": "approve_reject",
        "document_id": document_id,
        "payload": payload,
    }


def make_effective(document_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "status": "not_implemented",
        "action": "make_effective",
        "document_id": document_id,
        "payload": payload,
    }


def request_print(payload: dict[str, Any]) -> dict[str, Any]:
    return {"status": "not_implemented", "action": "request_print", "payload": payload}


def issue_print(payload: dict[str, Any]) -> dict[str, Any]:
    return {"status": "not_implemented", "action": "issue_print", "payload": payload}


def reconcile_print(print_event_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "status": "not_implemented",
        "action": "reconcile_print",
        "print_event_id": print_event_id,
        "payload": payload,
    }


def retrieve_audit_trail(document_id: str) -> dict[str, Any]:
    return {
        "status": "not_implemented",
        "action": "retrieve_audit_trail",
        "document_id": document_id,
    }
