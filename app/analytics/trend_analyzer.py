# =========================================================
# Trend Analyzer
# Autonomous AI DBA Operations Platform
# =========================================================

from app.repository.incident_repository import (
    load_incidents
)


# =========================================================
# TOTAL INCIDENTS
# =========================================================

def get_total_incidents():

    """
    Return total incident count.
    """

    incidents = load_incidents()

    return len(
        incidents
    )


# =========================================================
# HEALTHY INCIDENTS
# =========================================================

def get_healthy_incidents():

    """
    Return healthy incident count.
    """

    incidents = load_incidents()

    return len(

        [

            incident

            for incident in incidents

            if incident[
                "overall_status"
            ] == "HEALTHY"

        ]

    )


# =========================================================
# ATTENTION REQUIRED INCIDENTS
# =========================================================

def get_attention_required_incidents():

    """
    Return attention required count.
    """

    incidents = load_incidents()

    return len(

        [

            incident

            for incident in incidents

            if incident[
                "overall_status"
            ] == "ATTENTION REQUIRED"

        ]

    )


# =========================================================
# INCIDENT DISTRIBUTION
# =========================================================

def get_incident_distribution():

    """
    Return incident distribution.
    """

    return {

        "healthy":
        get_healthy_incidents(),

        "attention_required":
        get_attention_required_incidents()

    }


# =========================================================
# LATEST INCIDENT
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
# TEST EXECUTION
# =========================================================

if __name__ == "__main__":

    print(

        f"Total Incidents : "
        f"{get_total_incidents()}"

    )

    print(

        f"Healthy Incidents : "
        f"{get_healthy_incidents()}"

    )

    print(

        f"Attention Required : "
        f"{get_attention_required_incidents()}"

    )

    print(

        "\nLatest Incident:\n"

    )

    print(

        get_latest_incident()

    )