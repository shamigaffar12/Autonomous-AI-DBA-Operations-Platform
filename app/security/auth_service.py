# =========================================================
# Authentication Service
# Autonomous AI DBA Operations Platform
# =========================================================

import base64
import hashlib
import hmac
import json
import os
import time
from dataclasses import dataclass
from typing import Any, Dict, Optional

from fastapi import Request
from fastapi.responses import RedirectResponse, Response

from app.security.rbac_validator import (
    get_required_permission_for_request,
    get_role_permissions,
    has_permission,
    is_public_path,
    normalize_role
)


# =========================================================
# SECURITY CONFIGURATION
# =========================================================

AUTH_COOKIE_NAME = "ai_dba_auth_token"
TOKEN_ALGORITHM = "HS256"
TOKEN_EXPIRY_SECONDS = 8 * 60 * 60

JWT_SECRET_KEY = os.getenv(
    "JWT_SECRET_KEY",
    "dev-change-this-secret-key-for-ai-dba-platform"
)

LOGIN_PATH = "/auth/login"


# =========================================================
# USER MODEL
# =========================================================

@dataclass
class AuthUser:
    username: str
    display_name: str
    role: str
    permissions: Dict[str, bool]


# =========================================================
# PASSWORD HASHING
# =========================================================

def hash_password(
    password: str,
    salt: str
) -> str:
    """
    Hash password using PBKDF2-HMAC-SHA256.
    """

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        100000
    )

    return base64.urlsafe_b64encode(
        password_hash
    ).decode("utf-8")


def verify_password(
    password: str,
    stored_password_hash: str,
    salt: str
) -> bool:
    """
    Verify password using constant-time comparison.
    """

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
    salt: str
) -> Dict[str, str]:
    """
    Build password hash record.
    """

    return {
        "salt": salt,
        "password_hash": hash_password(
            password=password,
            salt=salt
        )
    }


# =========================================================
# LOCAL DEMO USER STORE
# =========================================================

DEMO_USERS: Dict[str, Dict[str, Any]] = {
    "admin": {
        "username": "admin",
        "display_name": "Platform Admin",
        "role": "ADMIN",
        **build_password_record(
            password="admin@123",
            salt="admin-static-dev-salt"
        )
    },
    "dba": {
        "username": "dba",
        "display_name": "DBA User",
        "role": "DBA",
        **build_password_record(
            password="dba@123",
            salt="dba-static-dev-salt"
        )
    },
    "lead_dba": {
        "username": "lead_dba",
        "display_name": "Lead DBA",
        "role": "LEAD_DBA",
        **build_password_record(
            password="lead@123",
            salt="lead-dba-static-dev-salt"
        )
    },
    "manager": {
        "username": "manager",
        "display_name": "DBA Manager",
        "role": "DBA_MANAGER",
        **build_password_record(
            password="manager@123",
            salt="manager-static-dev-salt"
        )
    },
    "viewer": {
        "username": "viewer",
        "display_name": "Viewer User",
        "role": "VIEWER",
        **build_password_record(
            password="viewer@123",
            salt="viewer-static-dev-salt"
        )
    }
}


# =========================================================
# BASE64 URL HELPERS
# =========================================================

def base64url_encode(
    data: bytes
) -> str:
    """
    Base64 URL-safe encode without padding.
    """

    return base64.urlsafe_b64encode(
        data
    ).decode("utf-8").rstrip("=")


def base64url_decode(
    data: str
) -> bytes:
    """
    Base64 URL-safe decode with padding recovery.
    """

    padding = "=" * (-len(data) % 4)

    return base64.urlsafe_b64decode(
        data + padding
    )


# =========================================================
# TOKEN HELPERS
# =========================================================

def create_signed_token(
    payload: Dict[str, Any]
) -> str:
    """
    Create HS256 signed token using Python standard library.
    """

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

    signing_input = f"{header_encoded}.{payload_encoded}".encode("utf-8")

    signature = hmac.new(
        JWT_SECRET_KEY.encode("utf-8"),
        signing_input,
        hashlib.sha256
    ).digest()

    signature_encoded = base64url_encode(
        signature
    )

    return f"{header_encoded}.{payload_encoded}.{signature_encoded}"


def decode_signed_token(
    token: str
) -> Optional[Dict[str, Any]]:
    """
    Decode and validate signed token.
    """

    try:
        parts = token.split(".")

        if len(parts) != 3:
            return None

        header_encoded, payload_encoded, signature_encoded = parts

        signing_input = f"{header_encoded}.{payload_encoded}".encode("utf-8")

        expected_signature = hmac.new(
            JWT_SECRET_KEY.encode("utf-8"),
            signing_input,
            hashlib.sha256
        ).digest()

        received_signature = base64url_decode(
            signature_encoded
        )

        if not hmac.compare_digest(
            expected_signature,
            received_signature
        ):
            return None

        payload = json.loads(
            base64url_decode(
                payload_encoded
            ).decode("utf-8")
        )

        expires_at = int(
            payload.get("exp", 0)
        )

        if expires_at < int(time.time()):
            return None

        return payload

    except Exception:
        return None


# =========================================================
# AUTHENTICATION
# =========================================================

def authenticate_user(
    username: str,
    password: str
) -> Optional[AuthUser]:
    """
    Authenticate user from local demo user store.
    """

    normalized_username = str(
        username or ""
    ).strip().lower()

    user_record = DEMO_USERS.get(
        normalized_username
    )

    if not user_record:
        return None

    password_valid = verify_password(
        password=password,
        stored_password_hash=user_record["password_hash"],
        salt=user_record["salt"]
    )

    if not password_valid:
        return None

    role = normalize_role(
        user_record["role"]
    )

    return AuthUser(
        username=user_record["username"],
        display_name=user_record["display_name"],
        role=role,
        permissions=get_role_permissions(role)
    )


def create_user_token(
    user: AuthUser
) -> str:
    """
    Create signed authentication token for user.
    """

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
    """
    Get current authenticated user from request cookie.
    """

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

    display_name = str(
        payload.get("name", username)
    )

    role = normalize_role(
        payload.get("role", "")
    )

    if not username or not role:
        return None

    permissions = payload.get(
        "permissions",
        get_role_permissions(role)
    )

    return AuthUser(
        username=username,
        display_name=display_name,
        role=role,
        permissions=permissions
    )


# =========================================================
# COOKIE HELPERS
# =========================================================

def set_auth_cookie(
    response: Response,
    token: str
) -> None:
    """
    Set authentication cookie.
    """

    response.set_cookie(
        key=AUTH_COOKIE_NAME,
        value=token,
        max_age=TOKEN_EXPIRY_SECONDS,
        httponly=True,
        samesite="lax",
        secure=False
    )


def clear_auth_cookie(
    response: Response
) -> None:
    """
    Clear authentication cookie.
    """

    response.delete_cookie(
        key=AUTH_COOKIE_NAME
    )


# =========================================================
# REQUEST STATE HELPERS
# =========================================================

def set_anonymous_request_state(
    request: Request
) -> None:
    """
    Set safe anonymous request state.
    """

    request.state.current_user = None
    request.state.permissions = {}


def set_authenticated_request_state(
    request: Request,
    current_user: AuthUser
) -> None:
    """
    Set authenticated user request state.
    """

    request.state.current_user = current_user
    request.state.permissions = current_user.permissions


# =========================================================
# MIDDLEWARE
# =========================================================

async def auth_route_guard(
    request: Request,
    call_next
):
    """
    Enforce login and route-level RBAC.

    Uses path + HTTP method so Viewer users cannot
    approve, reject, execute, manage actions, run monitoring,
    or submit operational NLP commands.
    """

    path = request.url.path
    method = request.method

    if is_public_path(
        path
    ):
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

    return await call_next(
        request
    )