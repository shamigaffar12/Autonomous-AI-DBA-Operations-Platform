# =========================================================
# Error Handler
# Autonomous AI DBA Operations Platform
# =========================================================

from datetime import datetime

from app.audit.audit_logger import (
    write_audit_log
)


# =========================================================
# HANDLE ERROR
# =========================================================

def handle_error(

    component,

    error

):

    """
    Centralized error handling.
    """

    error_message = (

        f"[ERROR] {component}: {str(error)}"
    )

    print(

        f"\n{error_message}\n"
    )

    write_audit_log(

        error_message
    )

    return {

        "status": "FAILED",

        "component": component,

        "error": str(error),

        "timestamp": datetime.now().isoformat()
    }

# =========================================================
# TEST EXECUTION
# =========================================================

if __name__ == "__main__":

    try:

        10 / 0

    except Exception as error:

        handle_error(

            "TEST MODULE",

            error
        )