# =========================================================
# RBAC Validator
# Autonomous AI DBA Operations Platform
# =========================================================

from datetime import datetime


# =========================================================
# VALIDATE ACTION PERMISSION
# =========================================================

def validate_action_permission(
    user_role,
    action_name,
    risk_level
):
    """
    Validate whether a user role is allowed to execute
    or request a DBA action.

    LOW risk actions are allowed for DBA and Lead DBA.
    MEDIUM risk actions require Lead DBA or approval workflow.
    HIGH risk actions require Lead DBA and explicit approval.
    """

    try:

        print("\n========================================")
        print(" RBAC Security Validation ")
        print("========================================\n")

        role = str(
            user_role
        ).upper()

        action = str(
            action_name
        ).upper()

        risk = str(
            risk_level
        ).upper()

        allowed_roles = [
            "DBA",
            "LEAD_DBA",
            "DBA_MANAGER"
        ]

        privileged_roles = [
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
                "validated_at": str(
                    datetime.now()
                )
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
                "validated_at": str(
                    datetime.now()
                )
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
                    "validated_at": str(
                        datetime.now()
                    )
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
                "validated_at": str(
                    datetime.now()
                )
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
                    "validated_at": str(
                        datetime.now()
                    )
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
                "validated_at": str(
                    datetime.now()
                )
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
            "validated_at": str(
                datetime.now()
            )
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
            "message": str(
                error
            ),
            "validated_at": str(
                datetime.now()
            )
        }


# =========================================================
# TEST EXECUTION
# =========================================================

if __name__ == "__main__":

    result = validate_action_permission(
        user_role="DBA",
        action_name="RESTART_SQL_AGENT_JOB",
        risk_level="MEDIUM"
    )

    print("\n========================================")
    print(" RBAC VALIDATION RESULT ")
    print("========================================\n")

    print(
        result
    )