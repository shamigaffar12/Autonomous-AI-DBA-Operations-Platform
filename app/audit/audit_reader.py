# =========================================================
# Audit Reader
# Autonomous AI DBA Operations Platform
# =========================================================

from datetime import datetime
import os


# =========================================================
# AUDIT LOG DIRECTORY
# =========================================================

AUDIT_LOG_DIRECTORY = "audit_logs"


# =========================================================
# GET TODAY LOG FILE
# =========================================================

def get_today_audit_file():

    """
    Return today's audit log path.
    """

    today = datetime.now().strftime(

        "%Y%m%d"

    )

    return (

        f"{AUDIT_LOG_DIRECTORY}/audit_{today}.log"

    )


# =========================================================
# READ AUDIT LOG
# =========================================================

def read_audit_log(

    log_file=None

):

    """
    Read audit log contents.
    """

    if log_file is None:

        log_file = get_today_audit_file()

    if not os.path.exists(

        log_file

    ):

        print(

            "\nAudit log not found."

        )

        return None

    with open(

        log_file,

        "r",

        encoding="utf-8"

    ) as file:

        return file.read()


# =========================================================
# DISPLAY AUDIT LOG
# =========================================================

def display_audit_log():

    """
    Display audit log contents.
    """

    print("\n========================================")

    print(" AUDIT LOG ")

    print("========================================\n")

    log_content = read_audit_log()

    if log_content:

        print(

            log_content

        )


# =========================================================
# AUDIT SUMMARY
# =========================================================

def audit_summary():

    """
    Display audit summary.
    """

    log_content = read_audit_log()

    if not log_content:

        return

    events = [

        line

        for line in log_content.splitlines()

        if line.strip()
    ]

    print("\n========================================")

    print(" AUDIT SUMMARY ")

    print("========================================\n")

    print(

        f"Total Events : {len(events)}"

    )

    print(

        f"Log File     : {get_today_audit_file()}"

    )

    print(

        f"Latest Event : {events[-1]}"

    )


# =========================================================
# TEST EXECUTION
# =========================================================

if __name__ == "__main__":

    display_audit_log()

    audit_summary()
