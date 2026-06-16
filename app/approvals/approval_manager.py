# =========================================================
# Approval Manager
# Autonomous AI DBA Operations Platform
# =========================================================

import os
import json
import uuid

from datetime import datetime


# =========================================================
# APPROVAL STORAGE CONFIGURATION
# =========================================================

APPROVAL_REQUESTS_DIR = "approval_requests"

PENDING_APPROVALS_FILE = os.path.join(
    APPROVAL_REQUESTS_DIR,
    "pending_approvals.json"
)

APPROVAL_HISTORY_FILE = os.path.join(
    APPROVAL_REQUESTS_DIR,
    "approval_history.json"
)


# =========================================================
# STORAGE UTILITIES
# =========================================================

def ensure_approval_storage():
    """
    Ensure approval_requests folder and JSON files exist.
    """

    os.makedirs(
        APPROVAL_REQUESTS_DIR,
        exist_ok=True
    )

    if not os.path.exists(
        PENDING_APPROVALS_FILE
    ):

        with open(
            PENDING_APPROVALS_FILE,
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


def load_json_list(
    file_path
):
    """
    Load JSON list from file.
    """

    ensure_approval_storage()

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(
                file
            )

            if isinstance(
                data,
                list
            ):

                return data

            return []

    except json.JSONDecodeError:

        return []

    except FileNotFoundError:

        return []


def save_json_list(
    file_path,
    data
):
    """
    Save JSON list into file.
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


# =========================================================
# CREATE APPROVAL REQUEST
# =========================================================

def create_approval_request(
    action_name,
    target_name,
    risk_level,
    requested_by="DBA",
    reason="Approval required for controlled DBA remediation.",
    metadata=None
):
    """
    Create new approval request and store it in pending_approvals.json.
    """

    pending_approvals = load_json_list(
        PENDING_APPROVALS_FILE
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

    save_json_list(
        PENDING_APPROVALS_FILE,
        pending_approvals
    )

    print(
        "\n========================================"
    )
    print(
        " APPROVAL REQUEST CREATED "
    )
    print(
        "========================================"
    )
    print(
        f"Approval ID : {approval_id}"
    )
    print(
        f"Action      : {action_name}"
    )
    print(
        f"Target      : {target_name}"
    )
    print(
        f"Risk Level  : {risk_level}"
    )
    print(
        "Status      : PENDING_APPROVAL"
    )

    return approval_request


# =========================================================
# LIST APPROVALS
# =========================================================

def list_pending_approvals():
    """
    Return all pending approval requests.
    """

    return load_json_list(
        PENDING_APPROVALS_FILE
    )


def list_approval_history():
    """
    Return all completed approval requests.
    """

    return load_json_list(
        APPROVAL_HISTORY_FILE
    )


# =========================================================
# GET APPROVAL
# =========================================================

def get_approval_request(
    approval_id
):
    """
    Find approval request from pending or history.
    """

    pending_approvals = load_json_list(
        PENDING_APPROVALS_FILE
    )

    approval_history = load_json_list(
        APPROVAL_HISTORY_FILE
    )

    all_approvals = pending_approvals + approval_history

    for approval in all_approvals:

        if approval.get(
            "approval_id"
        ) == approval_id:

            return approval

    return None


def get_approval_status(
    approval_id
):
    """
    Get approval status by approval ID.
    """

    approval_request = get_approval_request(
        approval_id
    )

    if not approval_request:

        return "NOT_FOUND"

    return approval_request.get(
        "approval_status",
        "UNKNOWN"
    )


# =========================================================
# APPROVE REQUEST
# =========================================================

def approve_request(
    approval_id,
    approved_by="Lead DBA",
    comments="Approved."
):
    """
    Approve request.

    Move record from pending_approvals.json to approval_history.json.
    """

    pending_approvals = load_json_list(
        PENDING_APPROVALS_FILE
    )

    approval_history = load_json_list(
        APPROVAL_HISTORY_FILE
    )

    updated_pending_approvals = []
    approved_request = None

    for approval in pending_approvals:

        if approval.get(
            "approval_id"
        ) == approval_id:

            approval["approval_status"] = "APPROVED"
            approval["approved_by"] = approved_by
            approval["rejected_by"] = None
            approval["decision_reason"] = comments
            approval["decision_at"] = str(
                datetime.now()
            )

            approved_request = approval

            approval_history.append(
                approval
            )

        else:

            updated_pending_approvals.append(
                approval
            )

    save_json_list(
        PENDING_APPROVALS_FILE,
        updated_pending_approvals
    )

    save_json_list(
        APPROVAL_HISTORY_FILE,
        approval_history
    )

    return approved_request


# =========================================================
# REJECT REQUEST
# =========================================================

def reject_request(
    approval_id,
    rejected_by="Lead DBA",
    comments="Rejected."
):
    """
    Reject request.

    Move record from pending_approvals.json to approval_history.json.
    """

    pending_approvals = load_json_list(
        PENDING_APPROVALS_FILE
    )

    approval_history = load_json_list(
        APPROVAL_HISTORY_FILE
    )

    updated_pending_approvals = []
    rejected_request = None

    for approval in pending_approvals:

        if approval.get(
            "approval_id"
        ) == approval_id:

            approval["approval_status"] = "REJECTED"
            approval["approved_by"] = None
            approval["rejected_by"] = rejected_by
            approval["decision_reason"] = comments
            approval["decision_at"] = str(
                datetime.now()
            )

            rejected_request = approval

            approval_history.append(
                approval
            )

        else:

            updated_pending_approvals.append(
                approval
            )

    save_json_list(
        PENDING_APPROVALS_FILE,
        updated_pending_approvals
    )

    save_json_list(
        APPROVAL_HISTORY_FILE,
        approval_history
    )

    return rejected_request