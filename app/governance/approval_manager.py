# =========================================================
# Approval Manager
# Autonomous AI DBA Operations Platform
# =========================================================

from datetime import datetime

from app.governance.approval_repository import (
    load_approvals,
    save_approvals,
    get_approval_count
)


# =========================================================
# GET PENDING APPROVALS
# =========================================================

def get_pending_approvals():

    """
    Return pending approvals.
    """

    approvals = load_approvals()

    return [

        approval

        for approval in approvals

        if approval.get(
            "status"
        ) == "PENDING"

    ]


# =========================================================
# GET APPROVED REQUESTS
# =========================================================

def get_approved_requests():

    """
    Return approved requests.
    """

    approvals = load_approvals()

    return [

        approval

        for approval in approvals

        if approval.get(
            "status"
        ) == "APPROVED"

    ]


# =========================================================
# GET REJECTED REQUESTS
# =========================================================

def get_rejected_requests():

    """
    Return rejected requests.
    """

    approvals = load_approvals()

    return [

        approval

        for approval in approvals

        if approval.get(
            "status"
        ) == "REJECTED"

    ]


# =========================================================
# GET REQUEST BY ID
# =========================================================

def get_request_by_id(

    request_id

):

    """
    Return governance request
    by request id.
    """

    approvals = load_approvals()

    for approval in approvals:

        if (

            approval.get(
                "request_id"
            )

            ==

            request_id

        ):

            return approval

    return None


# =========================================================
# GET REQUEST STATUS
# =========================================================

def get_request_status(

    request_id

):

    """
    Return request status.
    """

    approval = get_request_by_id(

        request_id

    )

    if approval:

        return approval.get(

            "status",

            "UNKNOWN"

        )

    return "NOT_FOUND"


# =========================================================
# APPROVE REQUEST
# =========================================================

def approve_request(

    request_id,

    approved_by="SYSTEM"

):

    """
    Approve governance request.
    """

    approvals = load_approvals()

    for approval in approvals:

        if (

            approval.get(
                "request_id"
            )

            ==

            request_id

        ):

            approval[
                "status"
            ] = "APPROVED"

            approval[
                "approved_by"
            ] = approved_by

            approval[
                "approved_timestamp"
            ] = str(

                datetime.now()

            )

            save_approvals(

                approvals

            )

            return approval

    return None


# =========================================================
# REJECT REQUEST
# =========================================================

def reject_request(

    request_id,

    reason,

    rejected_by="SYSTEM"

):

    """
    Reject governance request.
    """

    approvals = load_approvals()

    for approval in approvals:

        if (

            approval.get(
                "request_id"
            )

            ==

            request_id

        ):

            approval[
                "status"
            ] = "REJECTED"

            approval[
                "rejected_by"
            ] = rejected_by

            approval[
                "rejection_reason"
            ] = reason

            approval[
                "rejected_timestamp"
            ] = str(

                datetime.now()

            )

            save_approvals(

                approvals

            )

            return approval

    return None


# =========================================================
# DISPLAY APPROVAL SUMMARY
# =========================================================

def display_approval_summary():

    """
    Display approval statistics.
    """

    print("\n========================================")

    print(" APPROVAL GOVERNANCE DASHBOARD ")

    print("========================================\n")

    print(

        f"Total Requests      : "
        f"{get_approval_count()}"

    )

    print(

        f"Pending Requests    : "
        f"{len(get_pending_approvals())}"

    )

    print(

        f"Approved Requests   : "
        f"{len(get_approved_requests())}"

    )

    print(

        f"Rejected Requests   : "
        f"{len(get_rejected_requests())}"

    )


# =========================================================
# GET GOVERNANCE STATUS
# =========================================================

def get_governance_status():

    """
    Return governance statistics.
    """

    return {

        "status":
        "ACTIVE",

        "total_requests":
        get_approval_count(),

        "pending_requests":
        len(
            get_pending_approvals()
        ),

        "approved_requests":
        len(
            get_approved_requests()
        ),

        "rejected_requests":
        len(
            get_rejected_requests()
        )

    }


# =========================================================
# TEST EXECUTION
# =========================================================

if __name__ == "__main__":

    display_approval_summary()

    print(
        "\nGovernance Status:\n"
    )

    print(

        get_governance_status()

    )

    print(
        "\nPending Requests:\n"
    )

    print(

        get_pending_approvals()

    )

    print(
        "\nApproved Requests:\n"
    )

    print(

        get_approved_requests()

    )

    print(
        "\nRejected Requests:\n"
    )

    print(

        get_rejected_requests()

    )