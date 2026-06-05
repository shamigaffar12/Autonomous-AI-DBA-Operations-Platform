# =========================================================
# Incident Repository
# Autonomous AI DBA Operations Platform
# =========================================================

import json
import os

from datetime import datetime

from app.audit.audit_logger import (
    write_audit_log
)

from app.common.error_handler import (
    handle_error
)


# =========================================================
# REPOSITORY FILE
# =========================================================

REPOSITORY_FILE = (
    "repository/incidents.json"
)


# =========================================================
# SAVE INCIDENT
# =========================================================

def save_incident(

    overall_status,

    incident_summary,

    ai_analysis,

    report_file

):

    """
    Save incident to repository.
    """

    try:

        incident_record = {

            "timestamp":
            str(datetime.now()),

            "overall_status":
            overall_status,

            "incident_summary":
            incident_summary,

            "ai_analysis":
            ai_analysis,

            "report_file":
            report_file

        }

        if os.path.exists(

            REPOSITORY_FILE

        ):

            with open(

                REPOSITORY_FILE,

                "r",

                encoding="utf-8"

            ) as file:

                incidents = json.load(
                    file
                )

        else:

            incidents = []

        incidents.append(

            incident_record

        )

        with open(

            REPOSITORY_FILE,

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(

                incidents,

                file,

                indent=4

            )

        write_audit_log(

            "INCIDENT SAVED TO REPOSITORY"

        )

        return True

    except Exception as error:

        return handle_error(

            "INCIDENT REPOSITORY",

            error

        )


# =========================================================
# LOAD INCIDENTS
# =========================================================

def load_incidents():

    """
    Load all incidents.
    """

    try:

        if not os.path.exists(

            REPOSITORY_FILE

        ):

            return []

        with open(

            REPOSITORY_FILE,

            "r",

            encoding="utf-8"

        ) as file:

            return json.load(
                file
            )

    except Exception as error:

        return handle_error(

            "INCIDENT REPOSITORY",

            error

        )


# =========================================================
# GET INCIDENT COUNT
# =========================================================

def get_incident_count():

    """
    Return total incident count.
    """

    incidents = load_incidents()

    return len(
        incidents
    )


# =========================================================
# TEST EXECUTION
# =========================================================

if __name__ == "__main__":

    save_incident(

        "HEALTHY",

        "No incidents detected.",

        "AI analysis completed.",

        "reports/test_report.txt"

    )

    print(

        f"\nTotal Incidents: "
        f"{get_incident_count()}"

    )