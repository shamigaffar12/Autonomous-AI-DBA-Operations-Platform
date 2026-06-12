# =========================================================
# Main Application Entry Point
# Autonomous AI DBA Operations Platform
# =========================================================

from app.approvals.approval_manager import (
    view_pending_approvals,
    approve_request,
    reject_request,
    view_approval_history
)

from app.azure_integration.azure_automation_adapter import (
    create_azure_automation_runbook_request
)


try:

    from app.mcp_server.agentic_workflow import (
        run_agentic_workflow
    )

except ImportError:

    from app.mcp_server.agentic_workflow import (
        run_agentic_dba_workflow as run_agentic_workflow
    )


def run_daily_health_check():
    """
    Run Agentic AI DBA workflow.
    Approval request will be automatically created
    if failed SQL job remediation is recommended.
    """

    print("\n========================================")
    print(" Running Agentic AI DBA Workflow ")
    print("========================================\n")

    run_agentic_workflow(
        "Run daily DBA health check"
    )


def approve_and_trigger_automation():
    """
    Lead DBA approves request.
    Azure Automation request is created only after approval.
    """

    pending_result = view_pending_approvals()

    if pending_result.get(
        "pending_count",
        0
    ) == 0:

        return

    approval_id = input(
        "\nEnter Approval ID to approve: "
    ).strip()

    approved_by = input(
        "Approved By: "
    ).strip()

    if not approved_by:

        approved_by = "LEAD_DBA"

    decision_reason = input(
        "Approval Reason: "
    ).strip()

    if not decision_reason:

        decision_reason = "Approved by Lead DBA."

    approval_result = approve_request(
        approval_id=approval_id,
        approved_by=approved_by,
        decision_reason=decision_reason
    )

    if approval_result.get(
        "overall_status"
    ) == "APPROVED":

        approval_request = approval_result.get(
            "approval_request",
            {}
        )

        automation_request = {
            "approval_id": approval_request.get(
                "approval_id"
            ),
            "action": approval_request.get(
                "action_name"
            ),
            "job_name": approval_request.get(
                "target_name"
            ),
            "approval_status": "APPROVED",
            "approved_by": approved_by,
            "risk": approval_request.get(
                "risk_level"
            ),
            "reason": approval_request.get(
                "decision_reason"
            )
        }

        print("\n========================================")
        print(" Triggering Azure Automation Request ")
        print("========================================\n")

        create_azure_automation_runbook_request(
            automation_request
        )


def reject_automation_request():
    """
    Lead DBA rejects request.
    Remediation is blocked.
    """

    pending_result = view_pending_approvals()

    if pending_result.get(
        "pending_count",
        0
    ) == 0:

        return

    approval_id = input(
        "\nEnter Approval ID to reject: "
    ).strip()

    rejected_by = input(
        "Rejected By: "
    ).strip()

    if not rejected_by:

        rejected_by = "LEAD_DBA"

    decision_reason = input(
        "Rejection Reason: "
    ).strip()

    if not decision_reason:

        decision_reason = "Rejected by Lead DBA."

    reject_result = reject_request(
        approval_id=approval_id,
        rejected_by=rejected_by,
        decision_reason=decision_reason
    )

    if reject_result.get(
        "overall_status"
    ) == "REJECTED":

        print("\n========================================")
        print(" Remediation Blocked ")
        print("========================================\n")

        print("Status : REJECTED")
        print("Action : Automation request will not be triggered.")


def show_menu():
    """
    Display Operations Console menu.
    """

    print("\n========================================")
    print(" Autonomous AI DBA Operations Platform ")
    print("========================================\n")

    print("1. Run Agentic DBA Health Check")
    print("2. View Pending Approvals")
    print("3. Approve Request and Trigger Azure Automation")
    print("4. Reject Request")
    print("5. View Approval History")
    print("6. Exit")


def main():
    """
    Main Operations Console.
    """

    while True:

        show_menu()

        choice = input(
            "\nEnter your choice: "
        ).strip()

        if choice == "1":

            run_daily_health_check()

        elif choice == "2":

            view_pending_approvals()

        elif choice == "3":

            approve_and_trigger_automation()

        elif choice == "4":

            reject_automation_request()

        elif choice == "5":

            view_approval_history()

        elif choice == "6":

            print("\nExiting platform...")
            break

        else:

            print("\nInvalid choice. Please try again.")


if __name__ == "__main__":

    main()