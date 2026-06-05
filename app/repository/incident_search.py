# =========================================================
# Incident Search
# Autonomous AI DBA Operations Platform
# =========================================================

from app.repository.incident_repository import (
    load_incidents
)


# =========================================================
# SEARCH BY STATUS
# =========================================================

def search_by_status(

    status

):

    """
    Search incidents by status.
    """

    incidents = load_incidents()

    results = [

        incident

        for incident in incidents

        if incident["overall_status"].upper()
        == status.upper()

    ]

    return results


# =========================================================
# GET LATEST INCIDENT
# =========================================================

def get_latest_incident():

    """
    Return latest incident.
    """

    incidents = load_incidents()

    if not incidents:

        return None

    return incidents[-1]


# =========================================================
# SEARCH BY REPORT FILE
# =========================================================

def search_by_report_file(

    report_file

):

    """
    Search incident by report file.
    """

    incidents = load_incidents()

    for incident in incidents:

        if incident["report_file"] == report_file:

            return incident

    return None


# =========================================================
# DISPLAY INCIDENTS
# =========================================================

def display_incidents(

    incidents

):

    """
    Display incident results.
    """

    print("\n========================================")

    print(" INCIDENT SEARCH RESULTS ")

    print("========================================\n")

    if not incidents:

        print("No incidents found.")

        return

    for incident in incidents:

        print(

            f"Timestamp      : "
            f"{incident['timestamp']}"

        )

        print(

            f"Status         : "
            f"{incident['overall_status']}"

        )

        print(

            f"Report File    : "
            f"{incident['report_file']}"

        )

        print(

            "----------------------------------------"

        )


# =========================================================
# TEST EXECUTION
# =========================================================

if __name__ == "__main__":

    healthy_incidents = search_by_status(

        "HEALTHY"

    )

    display_incidents(

        healthy_incidents

    )

    print("\nLatest Incident:\n")

    print(

        get_latest_incident()

    )