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

from app.repository.incident_repository import (
    get_incident_count
)

from app.governance.approval_search import (
    get_all_approvals
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
# GOVERNANCE METRICS
# =========================================================

def get_governance_metrics():

    """
    Return governance statistics.
    """

    approvals = get_all_approvals()

    return {

        "total_requests":
        len(approvals),

        "approved_requests":
        len(

            [

                approval

                for approval in approvals

                if approval["status"] == "APPROVED"

            ]

        ),

        "rejected_requests":
        len(

            [

                approval

                for approval in approvals

                if approval["status"] == "REJECTED"

            ]

        ),

        "pending_requests":
        len(

            [

                approval

                for approval in approvals

                if approval["status"] == "PENDING"

            ]

        )

    }


# =========================================================
# DASHBOARD METRICS
# =========================================================

def get_dashboard_metrics():

    """
    Return dashboard metrics.
    """

    latest_incident = get_latest_incident()

    governance = get_governance_metrics()

    return {

        "platform_health":
        get_platform_health(),

        "total_incidents":
        get_total_incidents(),

        "healthy_incidents":
        get_healthy_incidents(),

        "attention_required":
        get_attention_required_incidents(),

        "repository_records":
        get_incident_count(),

        "total_requests":
        governance["total_requests"],

        "approved_requests":
        governance["approved_requests"],

        "rejected_requests":
        governance["rejected_requests"],

        "pending_requests":
        governance["pending_requests"],

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