# =========================================================
# Approval Repository
# Autonomous AI DBA Operations Platform
# =========================================================

import json
import os

from app.audit.audit_logger import (
    write_audit_log
)

from app.common.error_handler import (
    handle_error
)


# =========================================================
# REPOSITORY CONFIGURATION
# =========================================================

APPROVAL_REPOSITORY_FILE = (

    "repository/approvals.json"

)


# =========================================================
# LOAD APPROVALS
# =========================================================

def load_approvals():

    """
    Load all approval requests.
    """

    try:

        if not os.path.exists(

            APPROVAL_REPOSITORY_FILE

        ):

            return []

        with open(

            APPROVAL_REPOSITORY_FILE,

            "r",

            encoding="utf-8"

        ) as file:

            content = file.read().strip()

            if not content:

                return []

            return json.loads(

                content

            )

    except Exception as error:

        handle_error(

            "APPROVAL REPOSITORY",

            error

        )

        return []


# =========================================================
# SAVE ALL APPROVALS
# =========================================================

def save_approvals(

    approvals

):

    """
    Persist complete approval list.
    """

    try:

        os.makedirs(

            "repository",

            exist_ok=True

        )

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

        write_audit_log(

            "APPROVAL REPOSITORY UPDATED"

        )

    except Exception as error:

        handle_error(

            "APPROVAL REPOSITORY",

            error

        )


# =========================================================
# SAVE APPROVAL REQUEST
# =========================================================

def save_approval(

    approval_request

):

    """
    Save single approval request.
    """

    try:

        approvals = load_approvals()

        approvals.append(

            approval_request

        )

        save_approvals(

            approvals

        )

        write_audit_log(

            "APPROVAL REQUEST SAVED"

        )

    except Exception as error:

        handle_error(

            "APPROVAL REPOSITORY",

            error

        )


# =========================================================
# GET APPROVAL BY ID
# =========================================================

def get_approval_by_id(

    request_id

):

    """
    Return approval request
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
# GET APPROVAL COUNT
# =========================================================

def get_approval_count():

    """
    Return total approval count.
    """

    approvals = load_approvals()

    return len(

        approvals

    )


# =========================================================
# TEST EXECUTION
# =========================================================

if __name__ == "__main__":

    from app.governance.approval_request import (
        create_approval_request
    )

    approval = create_approval_request(

        "INDEX REBUILD",

        "Rebuild fragmented index."

    )

    save_approval(

        approval

    )

    print(

        f"Total Approvals: "
        f"{get_approval_count()}"

    )

    print(

        "\nApproval Lookup:\n"

    )

    print(

        get_approval_by_id(

            approval[
                "request_id"
            ]

        )

    )
    
    