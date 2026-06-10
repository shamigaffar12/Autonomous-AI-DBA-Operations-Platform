# =========================================================
# Dashboard Data
# Autonomous AI DBA Operations Platform
# =========================================================

import os

from app.analytics.trend_analyzer import (
    get_total_incidents,
    get_healthy_incidents,
    get_attention_required_incidents,
    get_latest_incident
)

from app.repository.incident_repository import (
    get_incident_count
)

from app.repository.action_repository import (
    load_actions
)

from app.governance.approval_search import (
    get_all_approvals
)

from app.audit.audit_reader import (
    read_audit_log
)

from app.common.config_manager import (
    REPORT_FOLDER
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
# ACTION COUNT
# =========================================================

def get_action_count():

    """
    Return total action count.
    """

    actions = load_actions()

    return len(

        actions

    )


# =========================================================
# AUDIT EVENT COUNT
# =========================================================

def get_audit_event_count():

    """
    Return total audit events.
    """

    log_content = read_audit_log()

    if not log_content:

        return 0

    events = [

        line

        for line in log_content.splitlines()

        if line.strip()

    ]

    return len(

        events

    )


# =========================================================
# REPORT COUNT
# =========================================================

def get_report_count():

    """
    Return total report count.
    """

    if not os.path.exists(

        REPORT_FOLDER

    ):

        return 0

    reports = [

        file

        for file in os.listdir(

            REPORT_FOLDER

        )

        if file.endswith(

            ".txt"

        )

    ]

    return len(

        reports

    )


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

        "total_actions":
        get_action_count(),

        "total_audit_events":
        get_audit_event_count(),

        "total_reports":
        get_report_count(),

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