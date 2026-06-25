# =========================================================
# RBAC Validator
# Autonomous AI DBA Operations Platform
# =========================================================

from datetime import datetime
from typing import Any, Dict, Optional


ROLE_PERMISSIONS: Dict[str, Dict[str, bool]] = {
    "ADMIN": {
        "can_view_dashboard": True,
        "can_run_monitoring": True,
        "can_view_analytics": True,
        "can_view_incidents": True,
        "can_manage_actions": True,
        "can_view_reports": True,
        "can_view_audit": True,
        "can_view_governance": True,
        "can_approve": True,
        "can_execute": True,
        "can_use_assistant": True,
        "can_submit_assistant_command": True,
        "can_manage_users": True,
        "can_manage_notifications": True,
    },
    "DBA_MANAGER": {
        "can_view_dashboard": True,
        "can_run_monitoring": True,
        "can_view_analytics": True,
        "can_view_incidents": True,
        "can_manage_actions": True,
        "can_view_reports": True,
        "can_view_audit": True,
        "can_view_governance": True,
        "can_approve": True,
        "can_execute": True,
        "can_use_assistant": True,
        "can_submit_assistant_command": True,
        "can_manage_users": True,
        "can_manage_notifications": True,
    },
    "LEAD_DBA": {
        "can_view_dashboard": True,
        "can_run_monitoring": True,
        "can_view_analytics": True,
        "can_view_incidents": True,
        "can_manage_actions": True,
        "can_view_reports": True,
        "can_view_audit": True,
        "can_view_governance": True,
        "can_approve": True,
        "can_execute": True,
        "can_use_assistant": True,
        "can_submit_assistant_command": True,
        "can_manage_users": False,
        "can_manage_notifications": True,
    },
    "DBA": {
        "can_view_dashboard": True,
        "can_run_monitoring": True,
        "can_view_analytics": True,
        "can_view_incidents": True,
        "can_manage_actions": True,
        "can_view_reports": True,
        "can_view_audit": True,
        "can_view_governance": True,
        "can_approve": True,
        "can_execute": True,
        "can_use_assistant": True,
        "can_submit_assistant_command": True,
        "can_manage_users": False,
        "can_manage_notifications": False,
    },
    "VIEWER": {
        "can_view_dashboard": True,
        "can_run_monitoring": False,
        "can_view_analytics": True,
        "can_view_incidents": True,
        "can_manage_actions": False,
        "can_view_reports": True,
        "can_view_audit": True,
        "can_view_governance": True,
        "can_approve": False,
        "can_execute": False,
        "can_use_assistant": True,
        "can_submit_assistant_command": False,
        "can_manage_users": False,
        "can_manage_notifications": False,
    },
}

PUBLIC_PATH_PREFIXES = [
    "/auth/login",
    "/auth/logout",
    "/static",
    "/favicon.ico",
    "/health",
    "/docs",
    "/redoc",
    "/openapi.json",
]


def normalize_role(user_role: Any) -> str:
    return str(user_role or "").strip().upper()


def normalize_method(method: Any) -> str:
    return str(method or "GET").strip().upper()


def normalize_path(path: Any) -> str:
    normalized_path = str(path or "").strip()

    if normalized_path and not normalized_path.startswith("/"):
        normalized_path = f"/{normalized_path}"

    return normalized_path


def get_role_permissions(user_role: Any) -> Dict[str, bool]:
    return ROLE_PERMISSIONS.get(
        normalize_role(user_role),
        {}
    )


def has_permission(
    user_role: Any,
    permission_name: str
) -> bool:
    return bool(
        get_role_permissions(user_role).get(
            permission_name,
            False
        )
    )


def is_public_path(path: str) -> bool:
    normalized_path = normalize_path(path)

    return any(
        normalized_path.startswith(public_path)
        for public_path in PUBLIC_PATH_PREFIXES
    )


def get_required_permission_for_request(
    path: str,
    method: str
) -> Optional[str]:

    normalized_path = normalize_path(path)
    normalized_method = normalize_method(method)
    path_lower = normalized_path.lower()

    if is_public_path(normalized_path):
        return None

    if path_lower.startswith("/approvals"):

        if normalized_method == "GET":
            return "can_view_governance"

        if any(
            word in path_lower
            for word in ["execute", "run", "remediate"]
        ):
            return "can_execute"

        if any(
            word in path_lower
            for word in ["approve", "reject", "decision", "status"]
        ):
            return "can_approve"

        return "can_approve"

    if path_lower.startswith("/actions"):

        if normalized_method == "GET":
            return "can_manage_actions"

        if normalized_method in ["POST", "PUT", "PATCH", "DELETE"]:
            return "can_execute"

        return "can_manage_actions"

    if path_lower.startswith("/assistant") or path_lower.startswith("/nlp"):

        if normalized_method == "GET":
            return "can_use_assistant"

        return "can_submit_assistant_command"

    if path_lower.startswith("/monitoring"):
        return "can_run_monitoring"

    if path_lower.startswith("/users"):
        return "can_manage_users"

    if path_lower.startswith("/notifications"):
        return "can_manage_notifications"

    if path_lower.startswith("/dashboard"):
        return "can_view_dashboard"

    if path_lower.startswith("/analytics"):
        return "can_view_analytics"

    if path_lower.startswith("/incidents"):
        return "can_view_incidents"

    if path_lower.startswith("/reports"):
        return "can_view_reports"

    if path_lower.startswith("/audit"):
        return "can_view_audit"

    if path_lower.startswith("/debug"):
        return "can_view_dashboard"

    return "can_view_dashboard"


def get_required_permission_for_path(
    path: str
) -> Optional[str]:
    return get_required_permission_for_request(
        path=path,
        method="GET"
    )


def validate_route_permission(
    user_role: Any,
    path: str,
    method: str = "GET"
) -> Dict[str, Any]:

    role = normalize_role(user_role)

    required_permission = get_required_permission_for_request(
        path=path,
        method=method
    )

    if required_permission is None:
        return {
            "overall_status": "PUBLIC_ROUTE",
            "validator_name": "ROUTE_RBAC_VALIDATOR",
            "user_role": role,
            "path": path,
            "method": normalize_method(method),
            "required_permission": None,
            "permission_granted": True,
            "message": "Public route access granted.",
            "validated_at": str(datetime.now()),
        }

    granted = has_permission(
        role,
        required_permission
    )

    return {
        "overall_status": "ACCESS_GRANTED" if granted else "ACCESS_DENIED",
        "validator_name": "ROUTE_RBAC_VALIDATOR",
        "user_role": role,
        "path": path,
        "method": normalize_method(method),
        "required_permission": required_permission,
        "permission_granted": granted,
        "message": "Route access granted." if granted else "User role is not authorized to access this route or action.",
        "validated_at": str(datetime.now()),
    }


def validate_action_permission(
    user_role,
    action_name,
    risk_level
):
    try:

        print("\n========================================")
        print(" RBAC Security Validation ")
        print("========================================\n")

        role = normalize_role(user_role)
        action = str(action_name).upper()
        risk = str(risk_level).upper()

        allowed_roles = [
            "ADMIN",
            "DBA",
            "LEAD_DBA",
            "DBA_MANAGER"
        ]

        privileged_roles = [
            "ADMIN",
            "LEAD_DBA",
            "DBA_MANAGER"
        ]

        print(f"User Role   : {role}")
        print(f"Action Name : {action}")
        print(f"Risk Level  : {risk}")

        if role not in allowed_roles:
            print("Access Status : DENIED")

            return _action_result(
                "ACCESS_DENIED",
                role,
                action,
                risk,
                False,
                False,
                "User role is not authorized for DBA operations."
            )

        if risk == "LOW":
            print("Access Status : GRANTED")

            return _action_result(
                "ACCESS_GRANTED",
                role,
                action,
                risk,
                True,
                False,
                "Low-risk DBA action is allowed for this role."
            )

        if risk == "MEDIUM":

            if role in privileged_roles:
                print("Access Status : GRANTED")

                return _action_result(
                    "ACCESS_GRANTED",
                    role,
                    action,
                    risk,
                    True,
                    False,
                    "Medium-risk DBA action is allowed for privileged DBA role."
                )

            print("Access Status : APPROVAL_REQUIRED")

            return _action_result(
                "APPROVAL_REQUIRED",
                role,
                action,
                risk,
                False,
                True,
                "Medium-risk DBA action requires Lead DBA approval."
            )

        if risk == "HIGH":

            if role in privileged_roles:
                print("Access Status : APPROVAL_REQUIRED")

                return _action_result(
                    "APPROVAL_REQUIRED",
                    role,
                    action,
                    risk,
                    False,
                    True,
                    "High-risk DBA action requires explicit approval even for privileged role."
                )

            print("Access Status : DENIED")

            return _action_result(
                "ACCESS_DENIED",
                role,
                action,
                risk,
                False,
                True,
                "High-risk DBA action is denied for non-privileged role."
            )

        print("Access Status : UNKNOWN_RISK")

        return _action_result(
            "UNKNOWN_RISK",
            role,
            action,
            risk,
            False,
            True,
            "Unknown risk level. Approval required by default."
        )

    except Exception as error:

        print("\nRBAC Validation Error:\n")
        print(error)

        return {
            "overall_status": "ERROR",
            "validator_name": "RBAC_VALIDATOR",
            "user_role": user_role,
            "action_name": action_name,
            "risk_level": risk_level,
            "permission_granted": False,
            "approval_required": True,
            "message": str(error),
            "validated_at": str(datetime.now()),
        }


def _action_result(
    status: str,
    role: str,
    action: str,
    risk: str,
    granted: bool,
    approval_required: bool,
    message: str
) -> Dict[str, Any]:

    return {
        "overall_status": status,
        "validator_name": "RBAC_VALIDATOR",
        "user_role": role,
        "action_name": action,
        "risk_level": risk,
        "permission_granted": granted,
        "approval_required": approval_required,
        "message": message,
        "validated_at": str(datetime.now()),
    }


if __name__ == "__main__":

    tests = [
        ("VIEWER", "/approvals", "GET"),
        ("VIEWER", "/approvals/approve/123", "POST"),
        ("VIEWER", "/approvals/execute/123", "POST"),
        ("VIEWER", "/assistant", "POST"),
        ("DBA", "/assistant", "POST"),
    ]

    for role, path, method in tests:
        print(
            validate_route_permission(
                role,
                path,
                method
            )
        )