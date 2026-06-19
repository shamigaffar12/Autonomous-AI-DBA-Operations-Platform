# =========================================================
# Approval Workflow Routes
# Autonomous AI DBA Operations Platform
# =========================================================

from fastapi import (
    APIRouter,
    Request,
    Form
)

from fastapi.responses import (
    HTMLResponse,
    RedirectResponse,
    PlainTextResponse
)

from fastapi.templating import (
    Jinja2Templates
)

from app.approvals.approval_manager import (
    list_pending_approvals,
    list_approval_history,
    approve_request,
    reject_request
)

from app.automation.execution_history_manager import (
    list_execution_history
)

from app.automation.governance_audit_manager import (
    add_governance_audit_log,
    list_governance_audit_logs
)


# =========================================================
# ROUTER CONFIGURATION
# =========================================================

router = APIRouter()

templates = Jinja2Templates(
    directory="templates"
)


# =========================================================
# DEBUG ROUTE
# =========================================================

@router.get(
    "/approvals/debug",
    response_class=PlainTextResponse
)
def approvals_debug():
    """
    Debug approval data loading.
    """

    try:

        pending_approvals = list_pending_approvals()
        approval_history = list_approval_history()
        execution_history = list_execution_history()
        governance_audit_logs = list_governance_audit_logs()

        output = ""
        output += "Approval Debug OK\n"
        output += "=================\n"
        output += f"Pending Count: {len(pending_approvals)}\n"
        output += f"History Count: {len(approval_history)}\n"
        output += f"Execution Count: {len(execution_history)}\n"
        output += f"Audit Count: {len(governance_audit_logs)}\n\n"

        output += "First Pending Approval:\n"

        if pending_approvals:

            output += str(
                pending_approvals[0]
            )

        else:

            output += "No pending approvals"

        return output

    except Exception as error:

        return f"Approval Debug Error:\n{str(error)}"


# =========================================================
# APPROVAL DASHBOARD PAGE
# =========================================================

@router.get(
    "/approvals",
    response_class=HTMLResponse
)
def approvals_page(
    request: Request
):
    """
    Display approval workflow dashboard.
    """

    try:

        pending_approvals = list_pending_approvals()
        approval_history = list_approval_history()
        execution_history = list_execution_history()
        governance_audit_logs = list_governance_audit_logs()

        approved_count = 0
        rejected_count = 0

        for approval in approval_history:

            if approval.get(
                "approval_status"
            ) == "APPROVED":

                approved_count = approved_count + 1

            elif approval.get(
                "approval_status"
            ) == "REJECTED":

                rejected_count = rejected_count + 1

        pending_count = len(
            pending_approvals
        )

        history_count = len(
            approval_history
        )

        execution_count = len(
            execution_history
        )

        audit_count = len(
            governance_audit_logs
        )

        total_requests = pending_count + history_count

        approvals_data = {
            "pending_approvals": pending_approvals,
            "approval_history": approval_history,
            "execution_history": execution_history,
            "governance_audit_logs": governance_audit_logs,
            "pending_count": pending_count,
            "approved_count": approved_count,
            "rejected_count": rejected_count,
            "history_count": history_count,
            "execution_count": execution_count,
            "audit_count": audit_count,
            "total_requests": total_requests,
            "total_count": total_requests
        }

        return templates.TemplateResponse(
            request=request,
            name="approvals.html",
            context={
                "approvals": approvals_data,
                "approval_data": approvals_data,
                "pending_approvals": pending_approvals,
                "approval_history": approval_history,
                "execution_history": execution_history,
                "governance_audit_logs": governance_audit_logs,
                "pending_count": pending_count,
                "approved_count": approved_count,
                "rejected_count": rejected_count,
                "history_count": history_count,
                "execution_count": execution_count,
                "audit_count": audit_count,
                "total_requests": total_requests
            }
        )

    except Exception as error:

        return HTMLResponse(
            content=f"""
            <html>
                <body style="font-family: Arial; padding: 30px;">
                    <h2>Approval Dashboard Error</h2>
                    <p><b>Error:</b></p>
                    <pre>{str(error)}</pre>
                    <p>Open /approvals/debug to test JSON loading.</p>
                </body>
            </html>
            """,
            status_code=500
        )


# =========================================================
# APPROVE REQUEST
# =========================================================

@router.post(
    "/approvals/approve"
)
def approve_approval_request(
    approval_id: str = Form(...)
):
    """
    Approve selected approval request.
    """

    approve_request(
        approval_id=approval_id,
        approved_by="Lead DBA",
        comments="Approved from FastAPI approval dashboard."
    )

    add_governance_audit_log(
        event_type="APPROVAL_APPROVED",
        approval_id=approval_id,
        action_name="APPROVE_REQUEST",
        target_name="Governance Approval",
        status="APPROVED",
        performed_by="Lead DBA",
        message="Approval request approved from FastAPI Governance dashboard."
    )

    return RedirectResponse(
        url="/approvals",
        status_code=303
    )


# =========================================================
# REJECT REQUEST
# =========================================================

@router.post(
    "/approvals/reject"
)
def reject_approval_request(
    approval_id: str = Form(...)
):
    """
    Reject selected approval request.
    """

    reject_request(
        approval_id=approval_id,
        rejected_by="Lead DBA",
        comments="Rejected from FastAPI approval dashboard."
    )

    add_governance_audit_log(
        event_type="APPROVAL_REJECTED",
        approval_id=approval_id,
        action_name="REJECT_REQUEST",
        target_name="Governance Approval",
        status="REJECTED",
        performed_by="Lead DBA",
        message="Approval request rejected from FastAPI Governance dashboard."
    )

    return RedirectResponse(
        url="/approvals",
        status_code=303
    )


# =========================================================
# EXECUTE APPROVED REQUEST
# =========================================================

@router.post(
    "/approvals/execute"
)
def execute_approval_request(
    approval_id: str = Form(...)
):
    """
    Execute approved remediation request.
    """

    from app.automation.approval_execution_console import (
        execute_approved_request
    )

    result = execute_approved_request(
        approval_id
    )

    print(
        "\n========================================"
    )
    print(
        " DASHBOARD EXECUTION RESULT "
    )
    print(
        "========================================"
    )
    print(
        result
    )

    return RedirectResponse(
        url="/approvals",
        status_code=303
    )