# =========================================================
# Approval Search
# Autonomous AI DBA Operations Platform
# =========================================================

from app.governance.approval_repository import (
    load_approvals
)


# =========================================================
# GET ALL APPROVALS
# =========================================================

def get_all_approvals():

    """
    Return all approval requests.
    """

    return load_approvals()


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
# TEST EXECUTION
# =========================================================

if __name__ == "__main__":

    print(

        get_all_approvals()

    )