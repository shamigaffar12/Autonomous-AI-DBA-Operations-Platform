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
    Load approval requests.
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
# SAVE APPROVAL REQUEST
# =========================================================

def save_approval(

    approval_request

):

    """
    Save approval request.
    """

    try:

        os.makedirs(

            "repository",

            exist_ok=True

        )

        approvals = load_approvals()

        approvals.append(

            approval_request

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

            "APPROVAL REQUEST SAVED"

        )

    except Exception as error:

        handle_error(

            "APPROVAL REPOSITORY",

            error

        )


# =========================================================
# GET APPROVAL COUNT
# =========================================================

def get_approval_count():

    """
    Return approval count.
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