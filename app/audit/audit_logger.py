# =========================================================
# Audit Logger
# Autonomous AI DBA Operations Platform
# =========================================================

from datetime import datetime
import os

from app.common.config_manager import (
    AUDIT_FOLDER
)


# =========================================================
# WRITE AUDIT LOG
# =========================================================

def write_audit_log(
    message
):
    """
    Write audit event to console and log file.
    """

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    # =====================================================
    # CREATE AUDIT FOLDER
    # =====================================================

    os.makedirs(
        AUDIT_FOLDER,
        exist_ok=True
    )

    # =====================================================
    # DAILY AUDIT FILE
    # =====================================================

    log_file = (
        f"{AUDIT_FOLDER}/audit_{datetime.now().strftime('%Y%m%d')}.log"
    )

    # =====================================================
    # AUDIT ENTRY
    # =====================================================

    audit_entry = (
        f"{timestamp} | {message}\n"
    )

    # =====================================================
    # WRITE LOG
    # =====================================================

    with open(
        log_file,
        "a",
        encoding="utf-8"
    ) as file:

        file.write(
            audit_entry
        )

    # =====================================================
    # CONSOLE OUTPUT
    # =====================================================

    print(
        f"AUDIT: {message}"
    )


# =========================================================
# TEST EXECUTION
# =========================================================

if __name__ == "__main__":

    write_audit_log(
        "Audit Logger Test"
    )