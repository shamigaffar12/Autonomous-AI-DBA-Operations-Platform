# =========================================================
# Audit Dashboard Data
# Autonomous AI DBA Operations Platform
# =========================================================

from app.audit.audit_reader import (
    read_audit_log,
    get_today_audit_file
)


# =========================================================
# GET AUDIT DASHBOARD DATA
# =========================================================

def get_audit_dashboard_data():

    """
    Return audit dashboard data.
    """

    log_content = read_audit_log()

    if not log_content:

        return {

            "total_events":
            0,

            "log_file":
            get_today_audit_file(),

            "events":
            []

        }

    events = [

        line

        for line in log_content.splitlines()

        if line.strip()

    ]

    events.reverse()

    return {

        "total_events":
        len(events),

        "log_file":
        get_today_audit_file(),

        "events":
        events

    }


# =========================================================
# TEST EXECUTION
# =========================================================

if __name__ == "__main__":

    data = get_audit_dashboard_data()

    print(

        f"\nTotal Events: "
        f"{data['total_events']}"

    )