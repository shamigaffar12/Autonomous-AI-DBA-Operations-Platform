# =========================================================
# Authentication Service
# Autonomous AI DBA Operations Platform
# =========================================================

import base64
import hashlib
import hmac
import json
import os
import secrets
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import Request
from fastapi.responses import RedirectResponse, Response

from app.security.rbac_validator import (
    get_required_permission_for_request,
    get_role_permissions,
    has_permission,
    is_public_path,
    normalize_role,
)

AUTH_COOKIE_NAME = "ai_dba_auth_token"
CSRF_COOKIE_NAME = "ai_dba_csrf_token"
TOKEN_ALGORITHM = "HS256"
TOKEN_EXPIRY_SECONDS = int(
    os.getenv(
        "AUTH_TOKEN_EXPIRY_SECONDS",
        str(8 * 60 * 60)
    )
)
JWT_SECRET_KEY = os.getenv(
    "JWT_SECRET_KEY",
    "dev-change-this-secret-key-for-ai-dba-platform"
)
LOGIN_PATH = "/auth/login"
USER_STORE_PATH = Path(
    os.getenv(
        "USER_STORE_PATH",
        "data/users.json"
    )
)

MUTATING_METHODS = {
    "POST",
    "PUT",
    "PATCH",
    "DELETE"
}

CSRF_EXEMPT_PREFIXES = [
    "/auth/login",
    "/auth/logout",
    "/health"
]


@dataclass
class AuthUser:
    username: str
    display_name: str
    role: str
    permissions: Dict[str, bool]
    is_active: bool = True


def _utc_now() -> str:
    return datetime.utcnow().isoformat(
        timespec="seconds"
    ) + "Z"


def hash_password(
    password: str,
    salt: str
) -> str:

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        120000
    )

    return base64.urlsafe_b64encode(
        password_hash
    ).decode("utf-8")


def verify_password(
    password: str,
    stored_password_hash: str,
    salt: str
) -> bool:

    calculated_hash = hash_password(
        password=password,
        salt=salt
    )

    return hmac.compare_digest(
        calculated_hash,
        stored_password_hash
    )


def build_password_record(
    password: str,
    salt: Optional[str] = None
) -> Dict[str, str]:

    final_salt = salt or secrets.token_urlsafe(24)

    return {
        "salt": final_salt,
        "password_hash": hash_password(
            password=password,
            salt=final_salt
        )
    }


def _default_users() -> Dict[str, Dict[str, Any]]:
    return {
        "admin": {
            "username": "admin",
            "display_name": "Platform Admin",
            "role": "ADMIN",
            "is_active": True,
            **build_password_record(
                "admin@123",
                "admin-static-dev-salt"
            )
        },
        "dba": {
            "username": "dba",
            "display_name": "DBA User",
            "role": "DBA",
            "is_active": True,
            **build_password_record(
                "dba@123",
                "dba-static-dev-salt"
            )
        },
        "lead_dba": {
            "username": "lead_dba",
            "display_name": "Lead DBA",
            "role": "LEAD_DBA",
            "is_active": True,
            **build_password_record(
                "lead@123",
                "lead-dba-static-dev-salt"
            )
        },
        "manager": {
            "username": "manager",
            "display_name": "DBA Manager",
            "role": "DBA_MANAGER",
            "is_active": True,
            **build_password_record(
                "manager@123",
                "manager-static-dev-salt"
            )
        },
        "viewer": {
            "username": "viewer",
            "display_name": "Viewer User",
            "role": "VIEWER",
            "is_active": True,
            **build_password_record(
                "viewer@123",
                "viewer-static-dev-salt"
            )
        },
    }


def ensure_user_store() -> None:

    USER_STORE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    if not USER_STORE_PATH.exists():
        USER_STORE_PATH.write_text(
            json.dumps(
                {
                    "users": _default_users(),
                    "created_at": _utc_now(),
                    "updated_at": _utc_now()
                },
                indent=4
            ),
            encoding="utf-8"
        )


def load_user_store() -> Dict[str, Any]:

    ensure_user_store()

    try:
        return json.loads(
            USER_STORE_PATH.read_text(
                encoding="utf-8"
            )
        )

    except json.JSONDecodeError:

        backup_path = USER_STORE_PATH.with_suffix(
            ".corrupt.json"
        )

        USER_STORE_PATH.replace(
            backup_path
        )

        USER_STORE_PATH.write_text(
            json.dumps(
                {
                    "users": _default_users(),
                    "created_at": _utc_now(),
                    "updated_at": _utc_now()
                },
                indent=4
            ),
            encoding="utf-8"
        )

        return json.loads(
            USER_STORE_PATH.read_text(
                encoding="utf-8"
            )
        )


def save_user_store(
    store: Dict[str, Any]
) -> None:

    store["updated_at"] = _utc_now()

    USER_STORE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    USER_STORE_PATH.write_text(
        json.dumps(
            store,
            indent=4
        ),
        encoding="utf-8"
    )


def list_users() -> List[Dict[str, Any]]:

    store = load_user_store()
    users = []

    for record in store.get("users", {}).values():
        users.append(
            {
                "username": record.get("username", ""),
                "display_name": record.get("display_name", ""),
                "role": normalize_role(
                    record.get("role", "")
                ),
                "is_active": bool(
                    record.get("is_active", True)
                ),
                "created_at": record.get("created_at", ""),
                "updated_at": record.get("updated_at", ""),
            }
        )

    return sorted(
        users,
        key=lambda item: item["username"]
    )


def create_or_update_user(
    username: str,
    display_name: str,
    role: str,
    password: Optional[str] = None,
    is_active: bool = True
) -> Dict[str, Any]:

    normalized_username = str(
        username or ""
    ).strip().lower()

    if not normalized_username:
        raise ValueError(
            "Username is required."
        )

    normalized_role = normalize_role(
        role
    )

    if normalized_role not in [
        "ADMIN",
        "DBA_MANAGER",
        "LEAD_DBA",
        "DBA",
        "VIEWER"
    ]:
        raise ValueError(
            "Invalid role."
        )

    store = load_user_store()
    users = store.setdefault(
        "users",
        {}
    )

    existing = users.get(
        normalized_username,
        {}
    )

    record = {
        "username": normalized_username,
        "display_name": str(
            display_name or normalized_username
        ).strip(),
        "role": normalized_role,
        "is_active": bool(is_active),
        "created_at": existing.get(
            "created_at",
            _utc_now()
        ),
        "updated_at": _utc_now(),
    }

    if password:
        record.update(
            build_password_record(
                password
            )
        )
    else:
        fallback_record = build_password_record(
            "ChangeMe@123"
        )

        record["salt"] = existing.get(
            "salt",
            fallback_record["salt"]
        )

        record["password_hash"] = existing.get(
            "password_hash",
            build_password_record(
                "ChangeMe@123",
                record["salt"]
            )["password_hash"]
        )

    users[normalized_username] = record

    save_user_store(
        store
    )

    return record


def set_user_active(
    username: str,
    is_active: bool
) -> bool:

    store = load_user_store()

    normalized_username = str(
        username or ""
    ).strip().lower()

    user = store.get(
        "users",
        {}
    ).get(
        normalized_username
    )

    if not user:
        return False

    user["is_active"] = bool(
        is_active
    )

    user["updated_at"] = _utc_now()

    save_user_store(
        store
    )

    return True


def base64url_encode(
    data: bytes
) -> str:

    return base64.urlsafe_b64encode(
        data
    ).decode("utf-8").rstrip("=")


def base64url_decode(
    data: str
) -> bytes:

    padding = "=" * (-len(data) % 4)

    return base64.urlsafe_b64decode(
        data + padding
    )


def create_signed_token(
    payload: Dict[str, Any]
) -> str:

    header = {
        "alg": TOKEN_ALGORITHM,
        "typ": "JWT"
    }

    header_encoded = base64url_encode(
        json.dumps(
            header,
            separators=(",", ":")
        ).encode("utf-8")
    )

    payload_encoded = base64url_encode(
        json.dumps(
            payload,
            separators=(",", ":")
        ).encode("utf-8")
    )

    signing_input = f"{header_encoded}.{payload_encoded}".encode(
        "utf-8"
    )

    signature = hmac.new(
        JWT_SECRET_KEY.encode("utf-8"),
        signing_input,
        hashlib.sha256
    ).digest()

    return f"{header_encoded}.{payload_encoded}.{base64url_encode(signature)}"


def decode_signed_token(
    token: str
) -> Optional[Dict[str, Any]]:

    try:
        parts = token.split(".")

        if len(parts) != 3:
            return None

        header_encoded, payload_encoded, signature_encoded = parts

        signing_input = f"{header_encoded}.{payload_encoded}".encode(
            "utf-8"
        )

        expected_signature = hmac.new(
            JWT_SECRET_KEY.encode("utf-8"),
            signing_input,
            hashlib.sha256
        ).digest()

        if not hmac.compare_digest(
            expected_signature,
            base64url_decode(signature_encoded)
        ):
            return None

        payload = json.loads(
            base64url_decode(
                payload_encoded
            ).decode("utf-8")
        )

        if int(
            payload.get("exp", 0)
        ) < int(
            time.time()
        ):
            return None

        return payload

    except Exception:
        return None


def authenticate_user(
    username: str,
    password: str
) -> Optional[AuthUser]:

    normalized_username = str(
        username or ""
    ).strip().lower()

    user_record = load_user_store().get(
        "users",
        {}
    ).get(
        normalized_username
    )

    if not user_record or not bool(
        user_record.get("is_active", True)
    ):
        return None

    if not verify_password(
        password=password,
        stored_password_hash=user_record["password_hash"],
        salt=user_record["salt"]
    ):
        return None

    role = normalize_role(
        user_record["role"]
    )

    return AuthUser(
        username=user_record["username"],
        display_name=user_record.get(
            "display_name",
            user_record["username"]
        ),
        role=role,
        permissions=get_role_permissions(role),
        is_active=True
    )


def create_user_token(
    user: AuthUser
) -> str:

    now = int(
        time.time()
    )

    payload = {
        "sub": user.username,
        "name": user.display_name,
        "role": normalize_role(user.role),
        "permissions": user.permissions,
        "iat": now,
        "exp": now + TOKEN_EXPIRY_SECONDS
    }

    return create_signed_token(
        payload
    )


def get_current_user(
    request: Request
) -> Optional[AuthUser]:

    token = request.cookies.get(
        AUTH_COOKIE_NAME
    )

    if not token:
        return None

    payload = decode_signed_token(
        token
    )

    if not payload:
        return None

    username = str(
        payload.get("sub", "")
    )

    role = normalize_role(
        payload.get("role", "")
    )

    if not username or not role:
        return None

    user_record = load_user_store().get(
        "users",
        {}
    ).get(
        username.lower()
    )

    if not user_record or not bool(
        user_record.get("is_active", True)
    ):
        return None

    return AuthUser(
        username=username,
        display_name=str(
            payload.get("name", username)
        ),
        role=role,
        permissions=get_role_permissions(role),
        is_active=True
    )


def set_auth_cookie(
    response: Response,
    token: str
) -> None:

    secure_cookie = os.getenv(
        "AUTH_COOKIE_SECURE",
        "false"
    ).lower() == "true"

    response.set_cookie(
        key=AUTH_COOKIE_NAME,
        value=token,
        max_age=TOKEN_EXPIRY_SECONDS,
        httponly=True,
        samesite="lax",
        secure=secure_cookie
    )


def clear_auth_cookie(
    response: Response
) -> None:

    response.delete_cookie(
        key=AUTH_COOKIE_NAME
    )

    response.delete_cookie(
        key=CSRF_COOKIE_NAME
    )


def get_or_create_csrf_token(
    request: Request,
    response: Response
) -> str:

    csrf_token = request.cookies.get(
        CSRF_COOKIE_NAME
    ) or secrets.token_urlsafe(32)

    secure_cookie = os.getenv(
        "AUTH_COOKIE_SECURE",
        "false"
    ).lower() == "true"

    response.set_cookie(
        key=CSRF_COOKIE_NAME,
        value=csrf_token,
        max_age=TOKEN_EXPIRY_SECONDS,
        httponly=False,
        samesite="lax",
        secure=secure_cookie
    )

    return csrf_token


def set_anonymous_request_state(
    request: Request
) -> None:

    request.state.current_user = None
    request.state.permissions = {}


def set_authenticated_request_state(
    request: Request,
    current_user: AuthUser
) -> None:

    request.state.current_user = current_user
    request.state.permissions = current_user.permissions


def _is_csrf_exempt(
    path: str
) -> bool:

    return any(
        path.startswith(prefix)
        for prefix in CSRF_EXEMPT_PREFIXES
    )


def _csrf_valid(
    request: Request
) -> bool:

    if request.method.upper() not in MUTATING_METHODS:
        return True

    if _is_csrf_exempt(
        request.url.path
    ):
        return True

    cookie_token = request.cookies.get(
        CSRF_COOKIE_NAME
    )

    header_token = request.headers.get(
        "x-csrf-token"
    )

    form_token = None

    return bool(
        cookie_token and (
            header_token == cookie_token
            or form_token == cookie_token
        )
    )


async def auth_route_guard(
    request: Request,
    call_next
):

    path = request.url.path
    method = request.method

    if is_public_path(path):

        set_anonymous_request_state(
            request
        )

        return await call_next(
            request
        )

    current_user = get_current_user(
        request
    )

    if not current_user:
        return RedirectResponse(
            url=LOGIN_PATH,
            status_code=302
        )

    required_permission = get_required_permission_for_request(
        path=path,
        method=method
    )

    if required_permission and not has_permission(
        user_role=current_user.role,
        permission_name=required_permission
    ):
        return Response(
            content=(
                "<h2>403 Forbidden</h2>"
                "<p>You do not have permission to perform this action.</p>"
                "<p><strong>Required Permission:</strong> "
                f"{required_permission}</p>"
                "<p><a href='/dashboard'>Back to Dashboard</a></p>"
            ),
            status_code=403,
            media_type="text/html"
        )

    set_authenticated_request_state(
        request=request,
        current_user=current_user
    )

    response = await call_next(
        request
    )

    if request.method.upper() == "GET":
        get_or_create_csrf_token(
            request,
            response
        )

    return response