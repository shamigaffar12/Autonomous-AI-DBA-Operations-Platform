# =========================================================
# Governance Executor
# Autonomous AI DBA Operations Platform
# =========================================================

from app.governance.approval_request import (
    create_approval_request
)

from app.governance.approval_repository import (
    save_approval
)

from app.audit.audit_logger import (
    write_audit_log
)

from app.common.error_handler import (
    handle_error
)


# =========================================================
# CREATE GOVERNANCE REQUEST
# =========================================================

def create_governance_request(

    ai_analysis

):

    """
    Create approval request from
    AI recommendation.
    """

    try:

        approval_request = (

            create_approval_request(

                "AI RECOMMENDATION",

                ai_analysis

            )

        )

        save_approval(

            approval_request

        )

        write_audit_log(

            "GOVERNANCE REQUEST CREATED"

        )

        return approval_request

    except Exception as error:

        return handle_error(

            "GOVERNANCE EXECUTOR",

            error

        )


# =========================================================
# TEST EXECUTION
# =========================================================

if __name__ == "__main__":

    request = create_governance_request(

        "Create missing index recommendation."

    )

    print(

        request

    )