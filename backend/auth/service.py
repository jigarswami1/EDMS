from __future__ import annotations

import base64
from datetime import datetime, timedelta, timezone
import hashlib
import hmac
import json
import os
import secrets

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.auth.models import Role, User, UserSession
from backend.audit.service import log_event

JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret-change-me")
JWT_TTL_MINUTES = int(os.getenv("JWT_TTL_MINUTES", "30"))


class AuthError(Exception):
    pass


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("utf-8")


def _b64url_decode(data: str) -> bytes:
    pad = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + pad)


def hash_password(password: str, salt: bytes | None = None) -> str:
    if len(password) < 12:
        raise AuthError("Password policy violation: minimum length is 12")
    salt = salt or secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 200_000)
    return f"{salt.hex()}:{digest.hex()}"


def verify_password(password: str, encoded: str) -> bool:
    salt_hex, digest_hex = encoded.split(":", 1)
    expected = hash_password(password, bytes.fromhex(salt_hex)).split(":", 1)[1]
    return hmac.compare_digest(expected, digest_hex)


def _jwt_encode(payload: dict) -> str:
    header = {"alg": "HS256", "typ": "JWT"}
    header_b64 = _b64url(json.dumps(header, separators=(",", ":")).encode("utf-8"))
    payload_b64 = _b64url(json.dumps(payload, separators=(",", ":")).encode("utf-8"))
    signing_input = f"{header_b64}.{payload_b64}".encode("utf-8")
    sig = hmac.new(JWT_SECRET.encode("utf-8"), signing_input, hashlib.sha256).digest()
    return f"{header_b64}.{payload_b64}.{_b64url(sig)}"


def _jwt_decode(token: str) -> dict:
    try:
        h_b64, p_b64, s_b64 = token.split(".")
    except ValueError as exc:
        raise AuthError("Invalid token format") from exc
    signing_input = f"{h_b64}.{p_b64}".encode("utf-8")
    expected = hmac.new(JWT_SECRET.encode("utf-8"), signing_input, hashlib.sha256).digest()
    if not hmac.compare_digest(_b64url(expected), s_b64):
        raise AuthError("Invalid token signature")
    payload = json.loads(_b64url_decode(p_b64))
    now = datetime.now(timezone.utc).timestamp()
    if payload["exp"] < now:
        raise AuthError("Token expired")
    return payload


def create_user(session: Session, username: str, password: str, role: Role) -> User:
    user = User(username=username, password_hash=hash_password(password), role=role)
    session.add(user)
    session.flush()
    log_event(session, "USER_CREATE", actor=username, metadata={"role": role.value})
    return user


def login(session: Session, username: str, password: str) -> str:
    user = session.scalar(select(User).where(User.username == username))
    if not user or not verify_password(password, user.password_hash):
        log_event(session, "LOGIN_FAILED", actor=username, metadata={})
        raise AuthError("Invalid username or password")
    now = datetime.now(timezone.utc)
    expires = now + timedelta(minutes=JWT_TTL_MINUTES)
    usr_session = UserSession(user_id=user.id, expires_at=expires)
    session.add(usr_session)
    session.flush()
    payload = {
        "sub": user.username,
        "role": user.role.value,
        "sid": usr_session.session_id,
        "iat": now.timestamp(),
        "exp": expires.timestamp(),
    }
    token = _jwt_encode(payload)
    log_event(session, "LOGIN_SUCCESS", actor=username, metadata={"session": usr_session.session_id})
    return token


def validate_token(session: Session, token: str) -> dict:
    payload = _jwt_decode(token)
    user = session.scalar(select(User).where(User.username == payload["sub"], User.is_active.is_(True)))
    if not user:
        raise AuthError("Unknown user")
    sess = session.scalar(select(UserSession).where(UserSession.session_id == payload["sid"], UserSession.revoked.is_(False)))
    if not sess:
        raise AuthError("Session revoked")
    return payload


def logout(session: Session, session_id: str, actor: str) -> None:
    db_sess = session.scalar(select(UserSession).where(UserSession.session_id == session_id))
    if db_sess:
        db_sess.revoked = True
        log_event(session, "LOGOUT", actor=actor, metadata={"session": session_id})
