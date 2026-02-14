from __future__ import annotations

from collections.abc import Callable
from functools import wraps

from backend.auth.models import Role


class PermissionDenied(Exception):
    pass


def require_roles(*allowed_roles: Role) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            role = kwargs.get("actor_role")
            if role not in allowed_roles:
                raise PermissionDenied(f"Role {role} not authorized")
            return func(*args, **kwargs)

        return wrapper

    return decorator
