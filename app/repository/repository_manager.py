# =========================================================
# Repository Manager
# Autonomous AI DBA Operations Platform
# =========================================================

from app.repository.incident_repository import (
    load_incidents,
    get_incident_count
)


# =========================================================
# GET REPOSITORY STATUS
# =========================================================

def get_repository_status():

    """
    Return repository status.
    """

    return {

        "status": "ACTIVE",

        "total_incidents":
        get_incident_count()

    }


# =========================================================
# DISPLAY REPOSITORY SUMMARY
# =========================================================

def display_repository_summary():

    """
    Display repository summary.
    """

    incidents = load_incidents()

    print("\n========================================")

    print(" INCIDENT REPOSITORY ")

    print("========================================\n")

    print(

        f"Total Incidents : {len(incidents)}"

    )

    if incidents:

        latest_incident = incidents[-1]

        print(

            f"Latest Status   : "
            f"{latest_incident['overall_status']}"

        )

        print(

            f"Latest Report   : "
            f"{latest_incident['report_file']}"

        )


# =========================================================
# TEST EXECUTION
# =========================================================

if __name__ == "__main__":

    display_repository_summary()

    print("\nRepository Status:\n")

    print(
        get_repository_status()
    )