# =========================================================
# Environment Validator
# Autonomous AI DBA Operations Platform
# =========================================================

import os

from app.common.config_manager import (
    SQL_SERVER,
    DATABASE_NAME,
    OPENROUTER_API_KEY,
    REPORT_FOLDER,
    AUDIT_FOLDER
)

from app.common.custom_exception import (
    MonitoringException
)


# =========================================================
# VALIDATE ENVIRONMENT
# =========================================================

def validate_environment():

    """
    Validate required environment settings.
    """

    print("\n========================================")

    print(" ENVIRONMENT VALIDATION ")

    print("========================================\n")


    # =====================================================
    # SQL SERVER
    # =====================================================

    if SQL_SERVER:

        print(f"SQL Server       : OK ({SQL_SERVER})")

    else:

        raise MonitoringException(
            "SQL Server configuration missing."
        )


    # =====================================================
    # DATABASE
    # =====================================================

    if DATABASE_NAME:

        print(f"Database         : OK ({DATABASE_NAME})")

    else:

        raise MonitoringException(
            "Database configuration missing."
        )


    # =====================================================
    # API KEY
    # =====================================================

    if OPENROUTER_API_KEY:

        print("OpenRouter API   : OK")

    else:

        raise MonitoringException(
            "OpenRouter API Key missing."
        )


    # =====================================================
    # REPORT FOLDER
    # =====================================================

    os.makedirs(
        REPORT_FOLDER,
        exist_ok=True
    )

    print(
        f"Reports Folder   : OK ({REPORT_FOLDER})"
    )


    # =====================================================
    # AUDIT FOLDER
    # =====================================================

    os.makedirs(
        AUDIT_FOLDER,
        exist_ok=True
    )

    print(
        f"Audit Folder     : OK ({AUDIT_FOLDER})"
    )


    print("\nEnvironment Validation Passed.\n")

    return True


# =========================================================
# TEST EXECUTION
# =========================================================

if __name__ == "__main__":

    validate_environment()