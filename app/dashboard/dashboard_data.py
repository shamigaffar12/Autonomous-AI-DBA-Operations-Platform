# =========================================================
# Dashboard Data
# Autonomous AI DBA Operations Platform
# =========================================================

from app.analytics.trend_analyzer import (
    get_total_incidents,
    get_healthy_incidents,
    get_attention_required_incidents,
    get_latest_incident
)


# =========================================================
# PLATFORM HEALTH
# =========================================================

def get_platform_health():

    """
    Return overall platform health.
    """

    if get_attention_required_incidents() > 0:

        return "ATTENTION REQUIRED"

    return "STABLE"


# =========================================================
# DASHBOARD METRICS
# =========================================================

def get_dashboard_metrics():

    """
    Return dashboard metrics.
    """

    latest_incident = get_latest_incident()

    return {

        "platform_health":
        get_platform_health(),

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
        if latest_incident else "N/A"
    }


# =========================================================
# TEST EXECUTION
# =========================================================

if __name__ == "__main__":

    print(

        get_dashboard_metrics()

    )