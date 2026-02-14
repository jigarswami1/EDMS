from __future__ import annotations

from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel

from backend.auth.models import Role
from backend.auth.service import AuthError, create_user, login, validate_token
from backend.db.base import Base
from backend.db.session import engine, get_session
from backend.documents.service import add_version, create_document, transition_document
from backend.signatures.service import sign_and_approve
from backend.workflow.state_machine import DocumentState

app = FastAPI(title="GxP EDMS")
Base.metadata.create_all(engine)


class UserIn(BaseModel):
    username: str
    password: str
    role: Role


class LoginIn(BaseModel):
    username: str
    password: str


class DocumentIn(BaseModel):
    doc_number: str
    title: str


class VersionIn(BaseModel):
    content: str


class SignIn(BaseModel):
    meaning: str


def _token_to_claims(authorization: str | None, session):
    if not authorization:
        raise HTTPException(401, "Missing Authorization header")
    token = authorization.replace("Bearer ", "")
    try:
        return validate_token(session, token)
    except AuthError as exc:
        raise HTTPException(401, str(exc)) from exc


@app.post("/users")
def create_user_route(payload: UserIn):
    with get_session() as session:
        create_user(session, payload.username, payload.password, payload.role)
    return {"status": "created"}


@app.post("/auth/login")
def login_route(payload: LoginIn):
    with get_session() as session:
        token = login(session, payload.username, payload.password)
    return {"access_token": token}


@app.post("/documents")
def create_document_route(payload: DocumentIn, authorization: str | None = Header(default=None)):
    with get_session() as session:
        claims = _token_to_claims(authorization, session)
        create_document(session, payload.doc_number, payload.title, claims["sub"])
    return {"status": "created"}


@app.post("/documents/{doc_number}/versions")
def add_version_route(doc_number: str, payload: VersionIn, authorization: str | None = Header(default=None)):
    with get_session() as session:
        claims = _token_to_claims(authorization, session)
        add_version(session, doc_number, payload.content, claims["sub"], Role(claims["role"]))
    return {"status": "versioned"}


@app.post("/documents/{doc_number}/submit-review")
def submit_review_route(doc_number: str, authorization: str | None = Header(default=None)):
    with get_session() as session:
        claims = _token_to_claims(authorization, session)
        transition_document(session, doc_number, DocumentState.REVIEW, claims["sub"], Role(claims["role"]))
    return {"status": "in_review"}


@app.post("/documents/{doc_number}/sign-approve")
def sign_approve_route(doc_number: str, payload: SignIn, authorization: str | None = Header(default=None)):
    with get_session() as session:
        claims = _token_to_claims(authorization, session)
        sign_and_approve(session, doc_number, claims["sub"], payload.meaning, Role(claims["role"]))
    return {"status": "approved"}
