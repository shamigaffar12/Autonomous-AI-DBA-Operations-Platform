# =========================================================
# Approval Manager
# Autonomous AI DBA Operations Platform
# =========================================================

import json
import os
import uuid

from datetime import datetime


APPROVAL_FOLDER = "approval_requests"

PENDING_APPROVAL_FILE = os.path.join(
    APPROVAL_FOLDER,
    "pending_approvals.json"
)

APPROVAL_HISTORY_FILE = os.path.join(
    APPROVAL_FOLDER,
    "approval_history.json"
)


def ensure_approval_storage():
    """
    Create approval folder and JSON files if not available.
    """

    os.makedirs(
        APPROVAL_FOLDER,
        exist_ok=True
    )

    if not os.path.exists(
        PENDING_APPROVAL_FILE
    ):

        with open(
            PENDING_APPROVAL_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                [],
                file,
                indent=4
            )

    if not os.path.exists(
        APPROVAL_HISTORY_FILE
    ):

        with open(
            APPROVAL_HISTORY_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                [],
                file,
                indent=4
            )


def load_json_data(
    file_path
):
    """
    Load JSON data from file.
    """

    ensure_approval_storage()

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(
            file
        )


def save_json_data(
    file_path,
    data
):
    """
    Save JSON data into file.
    """

    ensure_approval_storage()

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4,
            default=str
        )


def create_approval_request(
    action_name,
    target_name,
    risk_level,
    requested_by,
    reason,
    metadata=None
):
    """
    Create a real pending approval request.
    """

    try:

        ensure_approval_storage()

        pending_approvals = load_json_data(
            PENDING_APPROVAL_FILE
        )

        approval_id = str(
            uuid.uuid4()
        )

        approval_request = {
            "approval_id": approval_id,
            "action_name": action_name,
            "target_name": target_name,
            "risk_level": risk_level,
            "requested_by": requested_by,
            "reason": reason,
            "approval_status": "PENDING_APPROVAL",
            "approved_by": None,
            "rejected_by": None,
            "decision_reason": None,
            "created_at": str(
                datetime.now()
            ),
            "decision_at": None,
            "metadata": metadata or {}
        }

        pending_approvals.append(
            approval_request
        )

        save_json_data(
            PENDING_APPROVAL_FILE,
            pending_approvals
        )

        print("\n========================================")
        print(" Approval Request Created ")
        print("========================================\n")

        print(f"Approval ID : {approval_id}")
        print(f"Action      : {action_name}")
        print(f"Target      : {target_name}")
        print(f"Risk Level  : {risk_level}")
        print("Status      : PENDING_APPROVAL")

        return {
            "overall_status": "APPROVAL_REQUEST_CREATED",
            "approval_id": approval_id,
            "approval_status": "PENDING_APPROVAL",
            "message": "Approval request created successfully.",
            "approval_request": approval_request
        }

    except Exception as error:

        return {
            "overall_status": "ERROR",
            "approval_status": "ERROR",
            "message": str(
                error
            )
        }


def view_pending_approvals():
    """
    View all pending approval requests.
    """

    try:

        pending_approvals = load_json_data(
            PENDING_APPROVAL_FILE
        )

        print("\n========================================")
        print(" Pending Approval Requests ")
        print("========================================\n")

        if not pending_approvals:

            print("No pending approval requests found.")

        for approval in pending_approvals:

            print(f"Approval ID : {approval.get('approval_id')}")
            print(f"Action      : {approval.get('action_name')}")
            print(f"Target      : {approval.get('target_name')}")
            print(f"Risk Level  : {approval.get('risk_level')}")
            print(f"Requested By: {approval.get('requested_by')}")
            print(f"Status      : {approval.get('approval_status')}")
            print(f"Reason      : {approval.get('reason')}")
            print("----------------------------------------")

        return {
            "overall_status": "COMPLETED",
            "pending_count": len(
                pending_approvals
            ),
            "pending_approvals": pending_approvals
        }

    except Exception as error:

        return {
            "overall_status": "ERROR",
            "message": str(
                error
            ),
            "pending_count": 0,
            "pending_approvals": []
        }


def approve_request(
    approval_id,
    approved_by,
    decision_reason="Approved by Lead DBA."
):
    """
    Approve a pending approval request.
    """

    try:

        pending_approvals = load_json_data(
            PENDING_APPROVAL_FILE
        )

        approval_history = load_json_data(
            APPROVAL_HISTORY_FILE
        )

        selected_request = None
        remaining_requests = []

        for approval in pending_approvals:

            if approval.get(
                "approval_id"
            ) == approval_id:

                selected_request = approval

            else:

                remaining_requests.append(
                    approval
                )

        if selected_request is None:

            print("\nApproval request not found.")

            return {
                "overall_status": "NOT_FOUND",
                "approval_id": approval_id,
                "message": "Approval request not found."
            }

        selected_request["approval_status"] = "APPROVED"
        selected_request["approved_by"] = approved_by
        selected_request["decision_reason"] = decision_reason
        selected_request["decision_at"] = str(
            datetime.now()
        )

        approval_history.append(
            selected_request
        )

        save_json_data(
            PENDING_APPROVAL_FILE,
            remaining_requests
        )

        save_json_data(
            APPROVAL_HISTORY_FILE,
            approval_history
        )

        print("\n========================================")
        print(" Approval Request Approved ")
        print("========================================\n")

        print(f"Approval ID : {approval_id}")
        print("Status      : APPROVED")
        print(f"Approved By : {approved_by}")

        return {
            "overall_status": "APPROVED",
            "approval_status": "APPROVED",
            "message": "Approval request approved successfully.",
            "approval_request": selected_request
        }

    except Exception as error:

        return {
            "overall_status": "ERROR",
            "approval_id": approval_id,
            "message": str(
                error
            )
        }


def reject_request(
    approval_id,
    rejected_by,
    decision_reason="Rejected by Lead DBA."
):
    """
    Reject a pending approval request.
    """

    try:

        pending_approvals = load_json_data(
            PENDING_APPROVAL_FILE
        )

        approval_history = load_json_data(
            APPROVAL_HISTORY_FILE
        )

        selected_request = None
        remaining_requests = []

        for approval in pending_approvals:

            if approval.get(
                "approval_id"
            ) == approval_id:

                selected_request = approval

            else:

                remaining_requests.append(
                    approval
                )

        if selected_request is None:

            print("\nApproval request not found.")

            return {
                "overall_status": "NOT_FOUND",
                "approval_id": approval_id,
                "message": "Approval request not found."
            }

        selected_request["approval_status"] = "REJECTED"
        selected_request["rejected_by"] = rejected_by
        selected_request["decision_reason"] = decision_reason
        selected_request["decision_at"] = str(
            datetime.now()
        )

        approval_history.append(
            selected_request
        )

        save_json_data(
            PENDING_APPROVAL_FILE,
            remaining_requests
        )

        save_json_data(
            APPROVAL_HISTORY_FILE,
            approval_history
        )

        print("\n========================================")
        print(" Approval Request Rejected ")
        print("========================================\n")

        print(f"Approval ID : {approval_id}")
        print("Status      : REJECTED")
        print(f"Rejected By : {rejected_by}")

        return {
            "overall_status": "REJECTED",
            "approval_status": "REJECTED",
            "message": "Approval request rejected successfully.",
            "approval_request": selected_request
        }

    except Exception as error:

        return {
            "overall_status": "ERROR",
            "approval_id": approval_id,
            "message": str(
                error
            )
        }


def view_approval_history():
    """
    View approved and rejected approval requests.
    """

    try:

        approval_history = load_json_data(
            APPROVAL_HISTORY_FILE
        )

        print("\n========================================")
        print(" Approval History ")
        print("========================================\n")

        if not approval_history:

            print("No approval history found.")

        for approval in approval_history:

            print(f"Approval ID : {approval.get('approval_id')}")
            print(f"Action      : {approval.get('action_name')}")
            print(f"Target      : {approval.get('target_name')}")
            print(f"Status      : {approval.get('approval_status')}")
            print(f"Decision At : {approval.get('decision_at')}")
            print(f"Reason      : {approval.get('decision_reason')}")
            print("----------------------------------------")

        return {
            "overall_status": "COMPLETED",
            "history_count": len(
                approval_history
            ),
            "approval_history": approval_history
        }

    except Exception as error:

        return {
            "overall_status": "ERROR",
            "message": str(
                error
            ),
            "history_count": 0,
            "approval_history": []
        }


def approval_menu():
    """
    Simple CLI menu for testing approve/reject workflow.
    """

    while True:

        print("\n========================================")
        print(" Approval Workflow Menu ")
        print("========================================\n")

        print("1. Create Sample Approval Request")
        print("2. View Pending Approvals")
        print("3. Approve Request")
        print("4. Reject Request")
        print("5. View Approval History")
        print("6. Exit")

        choice = input(
            "\nEnter your choice: "
        ).strip()

        if choice == "1":

            create_approval_request(
                action_name="RESTART_SQL_AGENT_JOB",
                target_name="syspolicy_purge_history",
                risk_level="MEDIUM",
                requested_by="DBA",
                reason="SQL Server Agent job failed and requires Lead DBA approval before restart.",
                metadata={
                    "source": "FAILED_JOB_MONITOR"
                }
            )

        elif choice == "2":

            view_pending_approvals()

        elif choice == "3":

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

            approve_request(
                approval_id=approval_id,
                approved_by=approved_by,
                decision_reason=decision_reason
            )

        elif choice == "4":

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

            reject_request(
                approval_id=approval_id,
                rejected_by=rejected_by,
                decision_reason=decision_reason
            )

        elif choice == "5":

            view_approval_history()

        elif choice == "6":

            print("\nExiting approval workflow.")
            break

        else:

            print("\nInvalid choice. Please try again.")


if __name__ == "__main__":

    approval_menu()