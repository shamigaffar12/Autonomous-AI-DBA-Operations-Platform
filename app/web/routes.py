# =========================================================
# Web Routes
# Autonomous AI DBA Operations Platform
# =========================================================

import os
import json

from fastapi import (
    APIRouter,
    Request,
    Form
)

from fastapi.responses import (
    HTMLResponse,
    RedirectResponse
)

from fastapi.templating import (
    Jinja2Templates
)


# =========================================================
# ROUTER CONFIGURATION
# =========================================================

router = APIRouter()

templates = Jinja2Templates(
    directory="templates"
)


# =========================================================
# SAFE JSON LOADER
# =========================================================

def load_json_file(
    file_path,
    default_value=None
):
    """
    Safely load JSON file data.
    """

    if default_value is None:

        default_value = []

    try:

        if not os.path.exists(
            file_path
        ):

            return default_value

        with open(
            file_path,
            "r"
        ) as file:

            return json.load(
                file
            )

    except Exception:

        return default_value


# =========================================================
# SAFE REPORT FILE LOADER
# =========================================================

def load_report_files():
    """
    Load available report files from reports folder.
    """

    reports = []

    report_folder = "reports"

    if not os.path.exists(
        report_folder
    ):

        return reports

    for file_name in os.listdir(
        report_folder
    ):

        reports.append(
            {
                "report_name": file_name,
                "report_type": "Generated Report",
                "status": "Available"
            }
        )

    return reports


# =========================================================
# COMMON LIVE DATA CONTEXT
# =========================================================

def get_common_context():
    """
    Load live platform data with safe fallback values.
    """

    incidents = load_json_file(
        "incidents.json",
        []
    )

    actions = load_json_file(
        "actions.json",
        []
    )

    pending_approvals = load_json_file(
        "approval_requests/pending_approvals.json",
        []
    )

    approval_history = load_json_file(
        "approval_requests/approval_history.json",
        []
    )

    execution_history = load_json_file(
        "approval_requests/execution_history.json",
        []
    )

    governance_audit_logs = load_json_file(
        "approval_requests/governance_audit_log.json",
        []
    )

    reports = load_report_files()

    approved_count = 0
    rejected_count = 0

    for approval in approval_history:

        if approval.get(
            "approval_status"
        ) == "APPROVED":

            approved_count = approved_count + 1

        elif approval.get(
            "approval_status"
        ) == "REJECTED":

            rejected_count = rejected_count + 1

    pending_count = len(
        pending_approvals
    )

    history_count = len(
        approval_history
    )

    total_requests = pending_count + history_count

    return {
        "platform_status": "Online",
        "monitoring_status": "Active",
        "governance_status": "Active",
        "audit_status": "ACTIVE",
        "automation_mode": "Simulated",

        "incidents": incidents,
        "actions": actions,
        "reports": reports,
        "pending_approvals": pending_approvals,
        "approval_history": approval_history,
        "execution_history": execution_history,
        "governance_audit_logs": governance_audit_logs,
        "audit_events": governance_audit_logs,

        "total_incidents": len(
            incidents
        ),
        "total_actions": len(
            actions
        ),
        "total_reports": len(
            reports
        ),
        "total_audit_events": len(
            governance_audit_logs
        ),
        "total_events": len(
            governance_audit_logs
        ),

        "pending_count": pending_count,
        "approved_count": approved_count,
        "rejected_count": rejected_count,
        "history_count": history_count,
        "execution_count": len(
            execution_history
        ),
        "audit_count": len(
            governance_audit_logs
        ),
        "total_requests": total_requests,

        "cpu_status": "Live Check Available",
        "blocking_status": "Live Check Available",
        "backup_status": "Live Check Available",
        "database_space_status": "Live Check Available",
        "failed_jobs_status": "Governed",

        "health_score": 85,
        "risk_level": "Medium",
        "last_updated": "Live repository data loaded"
    }


# =========================================================
# HOME PAGE
# =========================================================

@router.get(
    "/"
)
def home_page():
    """
    Redirect home page to dashboard.
    """

    return RedirectResponse(
        url="/dashboard",
        status_code=303
    )


# =========================================================
# DASHBOARD PAGE
# =========================================================

@router.get(
    "/dashboard",
    response_class=HTMLResponse
)
def dashboard_page(
    request: Request
):
    """
    Display main operations dashboard with live repository data.
    """

    context = get_common_context()

    context.update(
        {
            "page_title": "Dashboard",
            "dashboard_title": "Operations Dashboard"
        }
    )

    return templates.TemplateResponse(
        name="dashboard.html",
        request=request,
        context=context
    )


# =========================================================
# MONITORING PAGE
# =========================================================

@router.get(
    "/monitoring",
    response_class=HTMLResponse
)
def monitoring_page(
    request: Request
):
    """
    Display monitoring center.
    """

    context = get_common_context()

    monitoring_results = [
        {
            "check_name": "CPU Health Monitor",
            "status": context.get(
                "cpu_status"
            ),
            "details": "CPU health monitor is connected with the monitoring workflow."
        },
        {
            "check_name": "Blocking Session Monitor",
            "status": context.get(
                "blocking_status"
            ),
            "details": "Blocking session monitor is available for SQL workload analysis."
        },
        {
            "check_name": "Failed SQL Job Monitor",
            "status": context.get(
                "failed_jobs_status"
            ),
            "details": "Failed SQL job remediation is connected with approval workflow."
        },
        {
            "check_name": "Backup Status Monitor",
            "status": context.get(
                "backup_status"
            ),
            "details": "Backup status monitoring is available."
        },
        {
            "check_name": "Database Space Monitor",
            "status": context.get(
                "database_space_status"
            ),
            "details": "Database space monitoring is available."
        }
    ]

    context.update(
        {
            "page_title": "Monitoring",
            "monitoring_title": "Monitoring Center",
            "monitoring_results": monitoring_results
        }
    )

    return templates.TemplateResponse(
        name="monitoring.html",
        request=request,
        context=context
    )


# =========================================================
# ANALYTICS PAGE
# =========================================================

@router.get(
    "/analytics",
    response_class=HTMLResponse
)
def analytics_page(
    request: Request
):
    """
    Display analytics center using live repository counts.
    """

    context = get_common_context()

    analytics_results = [
        {
            "metric": "Total Incidents",
            "value": context.get(
                "total_incidents"
            ),
            "status": "Tracked"
        },
        {
            "metric": "Approval Requests",
            "value": context.get(
                "total_requests"
            ),
            "status": "Governed"
        },
        {
            "metric": "Execution Records",
            "value": context.get(
                "execution_count"
            ),
            "status": "Tracked"
        },
        {
            "metric": "Audit Events",
            "value": context.get(
                "audit_count"
            ),
            "status": "Active"
        },
        {
            "metric": "Automation Mode",
            "value": context.get(
                "automation_mode"
            ),
            "status": "Controlled"
        }
    ]

    context.update(
        {
            "page_title": "Analytics",
            "analytics_title": "Analytics Center",
            "analytics_results": analytics_results
        }
    )

    return templates.TemplateResponse(
        name="analytics.html",
        request=request,
        context=context
    )


# =========================================================
# INCIDENTS PAGE
# =========================================================

@router.get(
    "/incidents",
    response_class=HTMLResponse
)
def incidents_page(
    request: Request
):
    """
    Display incident investigation center using live incident data.
    """

    context = get_common_context()

    context.update(
        {
            "page_title": "Incidents"
        }
    )

    return templates.TemplateResponse(
        name="incidents.html",
        request=request,
        context=context
    )


# =========================================================
# ACTIONS PAGE
# =========================================================

@router.get(
    "/actions",
    response_class=HTMLResponse
)
def actions_page(
    request: Request
):
    """
    Display action repository using live action data.
    """

    context = get_common_context()

    if not context.get(
        "actions"
    ):

        context["actions"] = [
            {
                "action_name": "RESTART_SQL_AGENT_JOB",
                "category": "Remediation",
                "risk_level": "Medium",
                "status": "Approval Required"
            },
            {
                "action_name": "GENERATE_DAILY_HEALTH_REPORT",
                "category": "Reporting",
                "risk_level": "Low",
                "status": "Available"
            },
            {
                "action_name": "CHECK_BLOCKING_SESSIONS",
                "category": "Monitoring",
                "risk_level": "Low",
                "status": "Available"
            }
        ]

        context["total_actions"] = len(
            context["actions"]
        )

    context.update(
        {
            "page_title": "Actions"
        }
    )

    return templates.TemplateResponse(
        name="actions.html",
        request=request,
        context=context
    )


# =========================================================
# REPORTS PAGE
# =========================================================

@router.get(
    "/reports",
    response_class=HTMLResponse
)
def reports_page(
    request: Request
):
    """
    Display reports center using generated report files.
    """

    context = get_common_context()

    if not context.get(
        "reports"
    ):

        context["reports"] = [
            {
                "report_name": "Daily DBA Health Report",
                "report_type": "Health Report",
                "status": "Available"
            },
            {
                "report_name": "Performance Tuning Report",
                "report_type": "Performance Report",
                "status": "Available"
            },
            {
                "report_name": "Excel Health Analytics Report",
                "report_type": "Excel Report",
                "status": "Available"
            }
        ]

        context["total_reports"] = len(
            context["reports"]
        )

    context.update(
        {
            "page_title": "Reports"
        }
    )

    return templates.TemplateResponse(
        name="reports.html",
        request=request,
        context=context
    )


# =========================================================
# AUDIT DASHBOARD PAGE
# =========================================================

@router.get(
    "/audit",
    response_class=HTMLResponse
)
def audit_page(
    request: Request
):
    """
    Display audit logs and governance audit events.
    """

    try:

        context = get_common_context()

        context.update(
            {
                "page_title": "Audit Logs",
                "audit_events": context.get(
                    "governance_audit_logs"
                ),
                "total_events": context.get(
                    "audit_count"
                ),
                "total_audit_events": context.get(
                    "audit_count"
                ),
                "audit_status": "ACTIVE",
                "governance_tracking": "ENABLED",
                "log_file": "approval_requests/governance_audit_log.json"
            }
        )

        return templates.TemplateResponse(
            name="audits.html",
            request=request,
            context=context
        )

    except Exception as error:

        return HTMLResponse(
            content=f"""
            <html>
                <body style="font-family: Arial; padding: 30px;">
                    <h2>Audit Dashboard Error</h2>
                    <p><b>Error:</b></p>
                    <pre>{str(error)}</pre>
                    <p>Please verify that governance audit manager and audit JSON files are available.</p>
                </body>
            </html>
            """,
            status_code=500
        )


# =========================================================
# NLP DBA ASSISTANT PAGE
# =========================================================

@router.get(
    "/assistant",
    response_class=HTMLResponse
)
def assistant_page(
    request: Request
):
    """
    Display NLP DBA Assistant page.
    """

    return templates.TemplateResponse(
        name="assistant.html",
        request=request,
        context={
            "page_title": "NLP DBA Assistant",
            "user_query": "",
            "assistant_result": None
        }
    )


# =========================================================
# NLP DBA ASSISTANT QUERY
# =========================================================

@router.post(
    "/assistant",
    response_class=HTMLResponse
)
def assistant_query(
    request: Request,
    user_query: str = Form(...)
):
    """
    Handle NLP DBA Assistant query.
    """

    from app.nlp_assistant.dba_assistant import (
        handle_dba_query
    )

    assistant_result = handle_dba_query(
        user_query
    )

    return templates.TemplateResponse(
        name="assistant.html",
        request=request,
        context={
            "page_title": "NLP DBA Assistant",
            "user_query": user_query,
            "assistant_result": assistant_result
        }
    )