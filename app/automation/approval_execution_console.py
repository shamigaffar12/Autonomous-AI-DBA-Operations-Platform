# =========================================================
# Approval Execution Console
# Autonomous AI DBA Operations Platform
# =========================================================

from datetime import datetime

from app.approvals.approval_manager import (
    get_approval_request,
    get_approval_status
)


# =========================================================
# EXECUTE APPROVED REQUEST
# =========================================================

def execute_approved_request(
    approval_id
):
    """
    Execute remediation only if approval status is APPROVED.
    """

    approval_request = get_approval_request(
        approval_id
    )

    if not approval_request:

        result = {
            "overall_status": "NOT_FOUND",
            "approval_id": approval_id,
            "message": "Approval request not found.",
            "executed": False,
            "executed_at": str(datetime.now())
        }

        print_execution_result(
            result
        )

        return result

    approval_status = get_approval_status(
        approval_id
    )

    if approval_status != "APPROVED":

        result = {
            "overall_status": "BLOCKED",
            "approval_id": approval_id,
            "approval_status": approval_status,
            "message": "Execution blocked. Approval is not completed.",
            "executed": False,
            "executed_at": str(datetime.now())
        }

        print_execution_result(
            result
        )

        return result

    action_name = approval_request.get(
        "action_name"
    )

    target_name = approval_request.get(
        "target_name"
    )

    # =====================================================
    # SIMULATED REMEDIATION EXECUTION
    # =====================================================

    if action_name == "RESTART_SQL_AGENT_JOB":

        result = {
            "overall_status": "RUNBOOK_REQUEST_CREATED",
            "approval_id": approval_id,
            "approval_status": approval_status,
            "action_name": action_name,
            "target_name": target_name,
            "runbook_name": "Restart-Failed-SQL-Agent-Job",
            "integration_mode": "SIMULATED",
            "message": "Azure Automation runbook request created after approval.",
            "runbook_request_created": True,
            "executed": True,
            "executed_at": str(datetime.now())
        }

        print_execution_result(
            result
        )

        return result

    result = {
        "overall_status": "UNSUPPORTED_ACTION",
        "approval_id": approval_id,
        "approval_status": approval_status,
        "action_name": action_name,
        "target_name": target_name,
        "message": "No execution handler found for this approved action.",
        "executed": False,
        "executed_at": str(datetime.now())
    }

    print_execution_result(
        result
    )

    return result


# =========================================================
# PRINT EXECUTION RESULT
# =========================================================

def print_execution_result(
    result
):
    """
    Print execution result in terminal.
    """

    print(
        "\n========================================"
    )
    print(
        " APPROVED REMEDIATION EXECUTION "
    )
    print(
        "========================================"
    )

    print(
        f"Overall Status  : {result.get('overall_status')}"
    )

    print(
        f"Approval ID     : {result.get('approval_id')}"
    )

    print(
        f"Approval Status : {result.get('approval_status')}"
    )

    print(
        f"Action Name     : {result.get('action_name')}"
    )

    print(
        f"Target Name     : {result.get('target_name')}"
    )

    print(
        f"Runbook Created : {result.get('runbook_request_created')}"
    )

    print(
        f"Message         : {result.get('message')}"
    )

    print(
        f"Executed At     : {result.get('executed_at')}"
    )