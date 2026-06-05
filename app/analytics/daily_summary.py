# =========================================================
# Daily Summary
# Autonomous AI DBA Operations Platform
# =========================================================

from datetime import datetime

from app.analytics.trend_analyzer import (
    get_total_incidents,
    get_healthy_incidents,
    get_attention_required_incidents,
    get_latest_incident
)


# =========================================================
# GENERATE DAILY SUMMARY
# =========================================================

def generate_daily_summary():

    """
    Generate daily operational summary.
    """

    latest_incident = get_latest_incident()

    platform_health = "STABLE"

    if get_attention_required_incidents() > 0:

        platform_health = "ATTENTION REQUIRED"

    summary = {

        "date":
        datetime.now().strftime(
            "%Y-%m-%d"
        ),

        "total_incidents":
        get_total_incidents(),

        "healthy_incidents":
        get_healthy_incidents(),

        "attention_required":
        get_attention_required_incidents(),

        "latest_status":
        latest_incident["overall_status"]
        if latest_incident else "N/A",

        "latest_report":
        latest_incident["report_file"]
        if latest_incident else "N/A",

        "platform_health":
        platform_health

    }

    return summary


# =========================================================
# DISPLAY DAILY SUMMARY
# =========================================================

def display_daily_summary():

    """
    Display operational summary.
    """

    summary = generate_daily_summary()

    print("\n========================================")

    print(" DAILY OPERATIONS SUMMARY ")

    print("========================================\n")

    print(
        f"Date                     : "
        f"{summary['date']}"
    )

    print(
        f"Total Incidents          : "
        f"{summary['total_incidents']}"
    )

    print(
        f"Healthy Incidents        : "
        f"{summary['healthy_incidents']}"
    )

    print(
        f"Attention Required       : "
        f"{summary['attention_required']}"
    )

    print(
        f"Latest Incident Status   : "
        f"{summary['latest_status']}"
    )

    print(
        f"Latest Report            : "
        f"{summary['latest_report']}"
    )

    print(
        f"Platform Health          : "
        f"{summary['platform_health']}"
    )


# =========================================================
# TEST EXECUTION
# =========================================================

if __name__ == "__main__":

    display_daily_summary()