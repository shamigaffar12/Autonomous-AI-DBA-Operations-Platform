# =========================================================
# Approval Actions
# Autonomous AI DBA Operations Platform
# =========================================================

from app.governance.approval_repository import (
    load_approvals,
    APPROVAL_REPOSITORY_FILE
)

from app.audit.audit_logger import (
    write_audit_log
)

from app.common.error_handler import (
    handle_error
)

import json


# =========================================================
# SAVE APPROVALS
# =========================================================

def save_approvals(approvals):

    """
    Persist approval requests.
    """

    with open(

        APPROVAL_REPOSITORY_FILE,

        "w",

        encoding="utf-8"

    ) as file:

        json.dump(

            approvals,

            file,

            indent=4

        )


# =========================================================
# UPDATE REQUEST STATUS
# =========================================================

def update_request_status(

    request_id,

    status

):

    """
    Update approval request status.
    """

    try:

        approvals = load_approvals()

        for approval in approvals:

            if (

                approval["request_id"]

                ==

                request_id

            ):

                approval["status"] = (

                    status.upper()

                )

                save_approvals(

                    approvals

                )

                write_audit_log(

                    f"APPROVAL REQUEST "
                    f"{request_id} "
                    f"UPDATED TO "
                    f"{status.upper()}"

                )

                return True

        print(

            f"Approval Request "
            f"{request_id} "
            f"not found."

        )

        return False

    except Exception as error:

        return handle_error(

            "APPROVAL ACTIONS",

            error

        )


# =========================================================
# APPROVE REQUEST
# =========================================================

def approve_request(

    request_id

):

    """
    Approve request.
    """

    return update_request_status(

        request_id,

        "APPROVED"

    )


# =========================================================
# REJECT REQUEST
# =========================================================

def reject_request(

    request_id

):

    """
    Reject request.
    """

    return update_request_status(

        request_id,

        "REJECTED"

    )


# =========================================================
# TEST EXECUTION
# =========================================================

if __name__ == "__main__":

    approvals = load_approvals()

    if approvals:

        request_id = (

            approvals[-1][

                "request_id"

            ]

        )

        approve_request(

            request_id

        )

        print(

            f"Approved Request: "
            f"{request_id}"

        )

    else:

        print(

            "No approval requests found."

        )