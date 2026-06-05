# =========================================================
# Approval Manager
# Autonomous AI DBA Operations Platform
# =========================================================

from app.governance.approval_repository import (
    load_approvals,
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

        if approval["status"] == "PENDING"

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

        if approval["status"] == "APPROVED"

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

        if approval["status"] == "REJECTED"

    ]


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

        "status": "ACTIVE",

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

    print("\nGovernance Status:\n")

    print(

        get_governance_status()

    )