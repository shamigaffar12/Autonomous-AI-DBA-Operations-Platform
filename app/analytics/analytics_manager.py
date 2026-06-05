# =========================================================
# Analytics Manager
# Autonomous AI DBA Operations Platform
# =========================================================

from app.analytics.trend_analyzer import (
    get_total_incidents,
    get_healthy_incidents,
    get_attention_required_incidents,
    get_latest_incident
)


# =========================================================
# DISPLAY ANALYTICS SUMMARY
# =========================================================

def display_analytics_summary():

    """
    Display incident analytics summary.
    """

    latest_incident = get_latest_incident()

    print("\n========================================")

    print(" INCIDENT ANALYTICS ")

    print("========================================\n")

    print(
        f"Total Incidents           : "
        f"{get_total_incidents()}"
    )

    print(
        f"Healthy Incidents         : "
        f"{get_healthy_incidents()}"
    )

    print(
        f"Attention Required        : "
        f"{get_attention_required_incidents()}"
    )

    if latest_incident:

        print(
            f"Latest Incident Status    : "
            f"{latest_incident['overall_status']}"
        )

        print(
            f"Latest Report             : "
            f"{latest_incident['report_file']}"
        )

    else:

        print(
            "Latest Incident Status    : None"
        )


# =========================================================
# GET ANALYTICS STATUS
# =========================================================

def get_analytics_status():

    """
    Return analytics status.
    """

    return {

        "status": "ACTIVE",

        "total_incidents":
        get_total_incidents(),

        "healthy_incidents":
        get_healthy_incidents(),

        "attention_required":
        get_attention_required_incidents()

    }


# =========================================================
# TEST EXECUTION
# =========================================================

if __name__ == "__main__":

    display_analytics_summary()

    print("\nAnalytics Status:\n")

    print(
        get_analytics_status()
    )