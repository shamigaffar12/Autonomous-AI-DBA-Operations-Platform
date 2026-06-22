# =========================================================
# Dashboard Routes
# Autonomous AI DBA Operations Platform
# =========================================================

import json
import os
from typing import Any, Dict, List

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


# =========================================================
# ROUTER AND TEMPLATE CONFIGURATION
# =========================================================

router = APIRouter()

templates = Jinja2Templates(
    directory="templates"
)


# =========================================================
# FILE PATH CONFIGURATION
# =========================================================

INCIDENTS_FILE = "repository/incidents.json"
ACTIONS_FILE = "repository/actions.json"
REPORTS_FILE = "repository/reports.json"

PENDING_APPROVALS_FILE = "approval_requests/pending_approvals.json"
APPROVAL_HISTORY_FILE = "approval_requests/approval_history.json"
EXECUTION_HISTORY_FILE = "approval_requests/execution_history.json"
GOVERNANCE_AUDIT_FILE = "approval_requests/governance_audit_log.json"

EXCEL_REPORTS_FOLDER = "excel_reports"


# =========================================================
# SAFE HELPERS
# =========================================================

def load_json_list(
    file_path: str
) -> List[Dict[str, Any]]:
    """
    Safely load JSON list data.
    """

    try:

        if not os.path.exists(
            file_path
        ):

            return []

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(
                file
            )

        if isinstance(
            data,
            list
        ):

            return data

        return []

    except Exception:

        return []


def safe_upper(
    value: Any
) -> str:
    """
    Convert value to uppercase string safely.
    """

    return str(
        value or ""
    ).strip().upper()


def safe_percentage(
    value: int,
    total: int
) -> int:
    """
    Calculate safe percentage for chart bars.
    """

    if total <= 0:

        return 0

    return round(
        (
            value / total
        ) * 100
    )


def count_excel_reports() -> int:
    """
    Count generated Excel report files.
    """

    if not os.path.exists(
        EXCEL_REPORTS_FOLDER
    ):

        return 0

    return len(
        [
            file_name
            for file_name in os.listdir(
                EXCEL_REPORTS_FOLDER
            )
            if file_name.lower().endswith(
                ".xlsx"
            )
        ]
    )


# =========================================================
# METRIC CALCULATION
# =========================================================

def calculate_incident_summary(
    incidents: List[Dict[str, Any]]
) -> Dict[str, int]:
    """
    Calculate incident health summary.
    """

    healthy_count = 0
    attention_count = 0

    for incident in incidents:

        status = safe_upper(
            incident.get(
                "status",
                incident.get(
                    "overall_status",
                    ""
                )
            )
        )

        if status == "HEALTHY":

            healthy_count += 1

        elif status in [
            "ATTENTION REQUIRED",
            "ATTENTION_REQUIRED",
            "WARNING",
            "CRITICAL",
            "FAILED",
            "ERROR"
        ]:

            attention_count += 1

    return {
        "healthy_count": healthy_count,
        "attention_count": attention_count
    }


def calculate_approval_summary(
    pending_approvals: List[Dict[str, Any]],
    approval_history: List[Dict[str, Any]]
) -> Dict[str, int]:
    """
    Calculate approval status summary.
    """

    approved_count = 0
    rejected_count = 0

    for approval in approval_history:

        approval_status = safe_upper(
            approval.get(
                "approval_status",
                approval.get(
                    "status",
                    ""
                )
            )
        )

        if approval_status == "APPROVED":

            approved_count += 1

        elif approval_status == "REJECTED":

            rejected_count += 1

    return {
        "pending_approvals": len(
            pending_approvals
        ),
        "approved_count": approved_count,
        "rejected_count": rejected_count
    }


def build_dashboard_metrics() -> Dict[str, Any]:
    """
    Build live dashboard metrics from repository JSON files.
    """

    incidents = load_json_list(
        INCIDENTS_FILE
    )

    actions = load_json_list(
        ACTIONS_FILE
    )

    reports = load_json_list(
        REPORTS_FILE
    )

    pending_approvals = load_json_list(
        PENDING_APPROVALS_FILE
    )

    approval_history = load_json_list(
        APPROVAL_HISTORY_FILE
    )

    execution_history = load_json_list(
        EXECUTION_HISTORY_FILE
    )

    governance_audit = load_json_list(
        GOVERNANCE_AUDIT_FILE
    )

    incident_summary = calculate_incident_summary(
        incidents
    )

    approval_summary = calculate_approval_summary(
        pending_approvals=pending_approvals,
        approval_history=approval_history
    )

    incidents_count = len(
        incidents
    )

    actions_count = len(
        actions
    )

    reports_count = len(
        reports
    )

    if reports_count == 0:

        reports_count = count_excel_reports()

    audit_count = len(
        governance_audit
    )

    execution_count = len(
        execution_history
    )

    healthy_count = incident_summary.get(
        "healthy_count",
        0
    )

    attention_count = incident_summary.get(
        "attention_count",
        0
    )

    pending_count = approval_summary.get(
        "pending_approvals",
        0
    )

    approved_count = approval_summary.get(
        "approved_count",
        0
    )

    rejected_count = approval_summary.get(
        "rejected_count",
        0
    )

    incident_total = healthy_count + attention_count

    approval_total = pending_count + approved_count + rejected_count

    max_activity = max(
        actions_count,
        reports_count,
        audit_count,
        execution_count,
        1
    )

    metrics = {
        "incidents_count": incidents_count,
        "actions_count": actions_count,
        "reports_count": reports_count,
        "audit_count": audit_count,
        "pending_approvals": pending_count,
        "approved_count": approved_count,
        "rejected_count": rejected_count,
        "execution_count": execution_count,
        "summary": {
            "healthy_count": healthy_count,
            "attention_count": attention_count
        },
        "charts": {
            "healthy_percentage": safe_percentage(
                healthy_count,
                incident_total
            ),
            "attention_percentage": safe_percentage(
                attention_count,
                incident_total
            ),
            "pending_percentage": safe_percentage(
                pending_count,
                approval_total
            ),
            "approved_percentage": safe_percentage(
                approved_count,
                approval_total
            ),
            "rejected_percentage": safe_percentage(
                rejected_count,
                approval_total
            ),
            "actions_percentage": safe_percentage(
                actions_count,
                max_activity
            ),
            "reports_percentage": safe_percentage(
                reports_count,
                max_activity
            ),
            "audit_percentage": safe_percentage(
                audit_count,
                max_activity
            ),
            "execution_percentage": safe_percentage(
                execution_count,
                max_activity
            )
        }
    }

    return metrics


# =========================================================
# ROUTES
# =========================================================

@router.get(
    "/dashboard"
)
def dashboard(
    request: Request
):
    """
    Dashboard page with live normalized data.
    """

    metrics = build_dashboard_metrics()

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "metrics": metrics
        }
    )


@router.get(
    "/debug/dashboard-data"
)
def debug_dashboard_data():
    """
    Debug dashboard live data.
    """

    return {
        "overall_status": "SUCCESS",
        "metrics": build_dashboard_metrics(),
        "source_files": {
            "incidents": INCIDENTS_FILE,
            "actions": ACTIONS_FILE,
            "reports": REPORTS_FILE,
            "pending_approvals": PENDING_APPROVALS_FILE,
            "approval_history": APPROVAL_HISTORY_FILE,
            "execution_history": EXECUTION_HISTORY_FILE,
            "governance_audit": GOVERNANCE_AUDIT_FILE,
            "excel_reports_folder": EXCEL_REPORTS_FOLDER
        }
    }