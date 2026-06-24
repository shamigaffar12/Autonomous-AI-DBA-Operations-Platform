# =========================================================
# RBAC Validator
# Autonomous AI DBA Operations Platform
# =========================================================

from datetime import datetime
from typing import Any, Dict, Optional


# =========================================================
# WEB ROLE PERMISSION REGISTRY
# =========================================================

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
        "can_manage_users": True
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
        "can_manage_users": True
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
        "can_manage_users": False
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
        "can_manage_users": False
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
        "can_manage_users": False
    }
}


# =========================================================
# PUBLIC ROUTES
# =========================================================

PUBLIC_PATH_PREFIXES = [
    "/auth/login",
    "/auth/logout",
    "/static",
    "/favicon.ico",
    "/health",
    "/docs",
    "/redoc",
    "/openapi.json"
]


# =========================================================
# WEB RBAC HELPERS
# =========================================================

def normalize_role(
    user_role: Any
) -> str:
    """
    Normalize user role for consistent RBAC checks.
    """

    return str(
        user_role or ""
    ).strip().upper()


def normalize_method(
    method: Any
) -> str:
    """
    Normalize HTTP method.
    """

    return str(
        method or "GET"
    ).strip().upper()


def normalize_path(
    path: Any
) -> str:
    """
    Normalize request path.
    """

    return str(
        path or ""
    ).strip()


def get_role_permissions(
    user_role: Any
) -> Dict[str, bool]:
    """
    Return permission dictionary for a role.
    """

    role = normalize_role(
        user_role
    )

    return ROLE_PERMISSIONS.get(
        role,
        {}
    )


def has_permission(
    user_role: Any,
    permission_name: str
) -> bool:
    """
    Check whether a role has a specific permission.
    """

    permissions = get_role_permissions(
        user_role
    )

    return bool(
        permissions.get(
            permission_name,
            False
        )
    )


def is_public_path(
    path: str
) -> bool:
    """
    Check whether the requested path is public.
    """

    normalized_path = normalize_path(
        path
    )

    return any(
        normalized_path.startswith(public_path)
        for public_path in PUBLIC_PATH_PREFIXES
    )


def get_required_permission_for_request(
    path: str,
    method: str
) -> Optional[str]:
    """
    Resolve required permission using route path and HTTP method.

    This prevents Viewer users from submitting approval,
    execution, action, monitoring, or NLP workflow commands.
    """

    normalized_path = normalize_path(
        path
    )

    normalized_method = normalize_method(
        method
    )

    path_lower = normalized_path.lower()

    # -----------------------------------------------------
    # Authentication routes
    # -----------------------------------------------------

    if is_public_path(
        normalized_path
    ):
        return None

    # -----------------------------------------------------
    # Governance / Approval Routes
    # -----------------------------------------------------
    # GET  -> view governance
    # POST -> approve/reject/execute permissions
    # -----------------------------------------------------

    if path_lower.startswith("/approvals"):

        if normalized_method == "GET":
            return "can_view_governance"

        if (
            "execute" in path_lower
            or "run" in path_lower
            or "remediate" in path_lower
        ):
            return "can_execute"

        if (
            "approve" in path_lower
            or "reject" in path_lower
            or "decision" in path_lower
            or "status" in path_lower
        ):
            return "can_approve"

        return "can_approve"

    # -----------------------------------------------------
    # Actions Routes
    # -----------------------------------------------------

    if path_lower.startswith("/actions"):

        if normalized_method == "GET":
            return "can_manage_actions"

        if normalized_method in [
            "POST",
            "PUT",
            "PATCH",
            "DELETE"
        ]:
            return "can_execute"

        return "can_manage_actions"

    # -----------------------------------------------------
    # NLP DBA Assistant Routes
    # -----------------------------------------------------
    # Viewer can open Assistant page, but cannot submit
    # operational NLP workflow commands.
    # -----------------------------------------------------

    if path_lower.startswith("/assistant"):

        if normalized_method == "GET":
            return "can_use_assistant"

        if normalized_method in [
            "POST",
            "PUT",
            "PATCH",
            "DELETE"
        ]:
            return "can_submit_assistant_command"

        return "can_use_assistant"

    # -----------------------------------------------------
    # NLP execution routes
    # -----------------------------------------------------

    if path_lower.startswith("/nlp"):

        if normalized_method == "GET":
            return "can_use_assistant"

        return "can_submit_assistant_command"

    # -----------------------------------------------------
    # Monitoring Routes
    # -----------------------------------------------------

    if path_lower.startswith("/monitoring"):
        return "can_run_monitoring"

    # -----------------------------------------------------
    # Normal Page-Level Routes
    # -----------------------------------------------------

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
    """
    Backward-compatible route permission resolver.
    """

    return get_required_permission_for_request(
        path=path,
        method="GET"
    )


def validate_route_permission(
    user_role: Any,
    path: str,
    method: str = "GET"
) -> Dict[str, Any]:
    """
    Validate route-level and method-level RBAC permission.
    """

    role = normalize_role(
        user_role
    )

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
            "validated_at": str(datetime.now())
        }

    permission_granted = has_permission(
        user_role=role,
        permission_name=required_permission
    )

    if permission_granted:
        return {
            "overall_status": "ACCESS_GRANTED",
            "validator_name": "ROUTE_RBAC_VALIDATOR",
            "user_role": role,
            "path": path,
            "method": normalize_method(method),
            "required_permission": required_permission,
            "permission_granted": True,
            "message": "Route access granted.",
            "validated_at": str(datetime.now())
        }

    return {
        "overall_status": "ACCESS_DENIED",
        "validator_name": "ROUTE_RBAC_VALIDATOR",
        "user_role": role,
        "path": path,
        "method": normalize_method(method),
        "required_permission": required_permission,
        "permission_granted": False,
        "message": "User role is not authorized to access this route or action.",
        "validated_at": str(datetime.now())
    }


# =========================================================
# EXISTING WORKFLOW RBAC VALIDATOR
# =========================================================

def validate_action_permission(
    user_role,
    action_name,
    risk_level
):
    """
    Validate whether a user role is allowed to execute
    or request a DBA action.

    LOW risk actions are allowed for DBA and privileged roles.
    MEDIUM risk actions require privileged role or approval workflow.
    HIGH risk actions require privileged role and explicit approval.
    """

    try:

        print("\n========================================")
        print(" RBAC Security Validation ")
        print("========================================\n")

        role = normalize_role(
            user_role
        )

        action = str(
            action_name
        ).upper()

        risk = str(
            risk_level
        ).upper()

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

            return {
                "overall_status": "ACCESS_DENIED",
                "validator_name": "RBAC_VALIDATOR",
                "user_role": role,
                "action_name": action,
                "risk_level": risk,
                "permission_granted": False,
                "approval_required": False,
                "message": "User role is not authorized for DBA operations.",
                "validated_at": str(datetime.now())
            }

        if risk == "LOW":

            print("Access Status : GRANTED")

            return {
                "overall_status": "ACCESS_GRANTED",
                "validator_name": "RBAC_VALIDATOR",
                "user_role": role,
                "action_name": action,
                "risk_level": risk,
                "permission_granted": True,
                "approval_required": False,
                "message": "Low-risk DBA action is allowed for this role.",
                "validated_at": str(datetime.now())
            }

        if risk == "MEDIUM":

            if role in privileged_roles:

                print("Access Status : GRANTED")

                return {
                    "overall_status": "ACCESS_GRANTED",
                    "validator_name": "RBAC_VALIDATOR",
                    "user_role": role,
                    "action_name": action,
                    "risk_level": risk,
                    "permission_granted": True,
                    "approval_required": False,
                    "message": "Medium-risk DBA action is allowed for privileged DBA role.",
                    "validated_at": str(datetime.now())
                }

            print("Access Status : APPROVAL_REQUIRED")

            return {
                "overall_status": "APPROVAL_REQUIRED",
                "validator_name": "RBAC_VALIDATOR",
                "user_role": role,
                "action_name": action,
                "risk_level": risk,
                "permission_granted": False,
                "approval_required": True,
                "message": "Medium-risk DBA action requires Lead DBA approval.",
                "validated_at": str(datetime.now())
            }

        if risk == "HIGH":

            if role in privileged_roles:

                print("Access Status : APPROVAL_REQUIRED")

                return {
                    "overall_status": "APPROVAL_REQUIRED",
                    "validator_name": "RBAC_VALIDATOR",
                    "user_role": role,
                    "action_name": action,
                    "risk_level": risk,
                    "permission_granted": False,
                    "approval_required": True,
                    "message": "High-risk DBA action requires explicit approval even for privileged role.",
                    "validated_at": str(datetime.now())
                }

            print("Access Status : DENIED")

            return {
                "overall_status": "ACCESS_DENIED",
                "validator_name": "RBAC_VALIDATOR",
                "user_role": role,
                "action_name": action,
                "risk_level": risk,
                "permission_granted": False,
                "approval_required": True,
                "message": "High-risk DBA action is denied for non-privileged role.",
                "validated_at": str(datetime.now())
            }

        print("Access Status : UNKNOWN_RISK")

        return {
            "overall_status": "UNKNOWN_RISK",
            "validator_name": "RBAC_VALIDATOR",
            "user_role": role,
            "action_name": action,
            "risk_level": risk,
            "permission_granted": False,
            "approval_required": True,
            "message": "Unknown risk level. Approval required by default.",
            "validated_at": str(datetime.now())
        }

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
            "validated_at": str(datetime.now())
        }


# =========================================================
# TEST EXECUTION
# =========================================================

if __name__ == "__main__":

    print("\n========================================")
    print(" RBAC ROUTE TESTS ")
    print("========================================\n")

    print(
        validate_route_permission(
            user_role="VIEWER",
            path="/approvals",
            method="GET"
        )
    )

    print(
        validate_route_permission(
            user_role="VIEWER",
            path="/approvals/approve/123",
            method="POST"
        )
    )

    print(
        validate_route_permission(
            user_role="VIEWER",
            path="/approvals/execute/123",
            method="POST"
        )
    )

    print(
        validate_route_permission(
            user_role="VIEWER",
            path="/assistant",
            method="POST"
        )
    )

    print(
        validate_route_permission(
            user_role="DBA",
            path="/assistant",
            method="POST"
        )
    )