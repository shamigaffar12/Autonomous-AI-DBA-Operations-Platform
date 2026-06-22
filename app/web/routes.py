# =========================================================
# Web Routes
# Autonomous AI DBA Operations Platform
# =========================================================

from typing import Optional
from datetime import date
import os
import json

from fastapi import (
    APIRouter,
    Request,
    Form
)

from fastapi.templating import (
    Jinja2Templates
)

from fastapi.responses import (
    RedirectResponse,
    FileResponse,
    HTMLResponse
)


# =========================================================
# ROUTER AND TEMPLATES
# =========================================================

router = APIRouter()

templates = Jinja2Templates(
    directory="templates"
)


# =========================================================
# COMPATIBILITY OBJECTS
# =========================================================

class ReportItem(dict):
    """
    Report object compatible with both dictionary access
    and old template split usage.
    """

    def split(
        self,
        separator=None
    ):
        """
        Support template usage: report.split('/')[-1]
        """

        file_path = self.get(
            "file_path",
            self.get(
                "report_name",
                ""
            )
        )

        return str(
            file_path
        ).split(
            separator
        )


# =========================================================
# SAFE JSON LOADER
# =========================================================

def load_json_file(
    file_path,
    default_value=None
):
    """
    Safely load JSON file.
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
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(
                file
            )

    except Exception:

        return default_value


# =========================================================
# ENSURE LIST
# =========================================================

def ensure_list(
    value
):
    """
    Ensure value is list.
    """

    if isinstance(
        value,
        list
    ):

        return value

    return []


# =========================================================
# LIVE APPROVAL / GOVERNANCE DATA
# =========================================================

def load_live_approval_data():
    """
    Load live approval, execution, and governance audit data.
    """

    pending_approvals = ensure_list(
        load_json_file(
            "approval_requests/pending_approvals.json",
            []
        )
    )

    approval_history = ensure_list(
        load_json_file(
            "approval_requests/approval_history.json",
            []
        )
    )

    execution_history = ensure_list(
        load_json_file(
            "approval_requests/execution_history.json",
            []
        )
    )

    governance_audit_logs = ensure_list(
        load_json_file(
            "approval_requests/governance_audit_log.json",
            []
        )
    )

    approved_count = len(
        [
            approval for approval in approval_history
            if approval.get(
                "approval_status"
            ) == "APPROVED"
        ]
    )

    rejected_count = len(
        [
            approval for approval in approval_history
            if approval.get(
                "approval_status"
            ) == "REJECTED"
        ]
    )

    return {
        "pending_approvals": pending_approvals,
        "approval_history": approval_history,
        "execution_history": execution_history,
        "governance_audit_logs": governance_audit_logs,
        "pending_count": len(
            pending_approvals
        ),
        "approved_count": approved_count,
        "rejected_count": rejected_count,
        "total_count": len(
            pending_approvals
        ) + len(
            approval_history
        ),
        "execution_count": len(
            execution_history
        ),
        "audit_count": len(
            governance_audit_logs
        )
    }


# =========================================================
# LIVE INCIDENT DATA
# =========================================================

def load_live_incidents():
    """
    Load live incidents from repository.
    """

    incidents = ensure_list(
        load_json_file(
            "repository/incidents.json",
            []
        )
    )

    if not incidents:

        incidents = ensure_list(
            load_json_file(
                "incidents.json",
                []
            )
        )

    normalized_incidents = []

    for index, incident in enumerate(
        incidents
    ):

        overall_status = incident.get(
            "overall_status",
            incident.get(
                "status",
                "TRACKED"
            )
        )

        if not overall_status:

            overall_status = "TRACKED"

        severity = incident.get(
            "severity",
            "LOW"
        )

        if str(
            overall_status
        ).upper() in [
            "ATTENTION REQUIRED",
            "INCIDENT",
            "FAILED",
            "BLOCKED"
        ]:

            severity = "HIGH"

        timestamp = incident.get(
            "timestamp",
            incident.get(
                "created_at",
                "-"
            )
        )

        report_file = incident.get(
            "report_file",
            incident.get(
                "report_path",
                "-"
            )
        )

        normalized_incidents.append(
            {
                "incident_id": incident.get(
                    "incident_id",
                    f"INC-{index + 1:04d}"
                ),
                "type": incident.get(
                    "type",
                    incident.get(
                        "incident_type",
                        "DBA Monitoring"
                    )
                ),
                "severity": severity,
                "status": overall_status,
                "overall_status": overall_status,
                "created_at": incident.get(
                    "created_at",
                    timestamp
                ),
                "timestamp": timestamp,
                "report_file": report_file,
                "report_path": report_file,
                "incident_summary": incident.get(
                    "incident_summary",
                    incident.get(
                        "summary",
                        "-"
                    )
                ),
                "summary": incident.get(
                    "summary",
                    incident.get(
                        "incident_summary",
                        "-"
                    )
                ),
                "ai_analysis": incident.get(
                    "ai_analysis",
                    incident.get(
                        "analysis",
                        "-"
                    )
                ),
                "analysis": incident.get(
                    "analysis",
                    incident.get(
                        "ai_analysis",
                        "-"
                    )
                )
            }
        )

    return normalized_incidents


# =========================================================
# LIVE ACTION DATA
# =========================================================

def load_live_actions():
    """
    Load live action repository data.
    """

    actions = ensure_list(
        load_json_file(
            "repository/actions.json",
            []
        )
    )

    if not actions:

        actions = ensure_list(
            load_json_file(
                "actions.json",
                []
            )
        )

    normalized_actions = []

    for index, action in enumerate(
        actions
    ):

        action_type = action.get(
            "action_type",
            action.get(
                "action_name",
                f"ACTION-{index + 1:04d}"
            )
        )

        component = action.get(
            "component",
            action.get(
                "category",
                "DBA Automation"
            )
        )

        normalized_actions.append(
            {
                "timestamp": action.get(
                    "timestamp",
                    action.get(
                        "created_at",
                        "-"
                    )
                ),
                "action_type": action_type,
                "action_name": action.get(
                    "action_name",
                    action_type
                ),
                "component": component,
                "category": action.get(
                    "category",
                    component
                ),
                "risk_level": action.get(
                    "risk_level",
                    "LOW"
                ),
                "status": action.get(
                    "status",
                    "Available"
                ),
                "details": action.get(
                    "details",
                    action.get(
                        "message",
                        "-"
                    )
                )
            }
        )

    return {
        "total_actions": len(
            normalized_actions
        ),
        "actions": list(
            reversed(
                normalized_actions
            )
        )
    }


# =========================================================
# REPORT TYPE HELPER
# =========================================================

def get_report_type(
    report_file
):
    """
    Return report type from file name.
    """

    file_name = str(
        report_file
    ).lower()

    if file_name.endswith(
        ".xlsx"
    ):

        return "Excel Report"

    if "performance" in file_name:

        return "Performance Report"

    if "health" in file_name:

        return "Health Report"

    if "incident" in file_name:

        return "Incident Report"

    if "daily" in file_name:

        return "Daily Health Report"

    return "Generated Report"


# =========================================================
# LIVE REPORT DATA
# =========================================================

def load_live_reports():
    """
    Load live reports from reports folder and subfolders.
    """

    report_items = []
    report_folders = [
        "reports",
        "excel_reports"
    ]

    try:

        for report_folder in report_folders:

            if os.path.exists(
                report_folder
            ):

                for root, directories, files in os.walk(
                    report_folder
                ):

                    for report_file in files:

                        if report_file.endswith(
                            (
                                ".txt",
                                ".xlsx",
                                ".csv",
                                ".json",
                                ".log",
                                ".md"
                            )
                        ):

                            file_path = os.path.join(
                                root,
                                report_file
                            ).replace(
                                "\\",
                                "/"
                            )

                            report_items.append(
                                ReportItem(
                                    {
                                        "report_name": report_file,
                                        "name": report_file,
                                        "report_type": get_report_type(
                                            report_file
                                        ),
                                        "type": get_report_type(
                                            report_file
                                        ),
                                        "status": "Available",
                                        "file_path": file_path,
                                        "path": file_path
                                    }
                                )
                            )

    except Exception:

        report_items = []

    report_items.sort(
        key=lambda item: item.get(
            "file_path",
            ""
        ),
        reverse=True
    )

    latest_report = "-"

    if report_items:

        latest_report = report_items[
            0
        ].get(
            "file_path",
            "-"
        )

    return {
        "total_reports": len(
            report_items
        ),
        "latest_report": latest_report,
        "reports": report_items,
        "report_files": report_items
    }


# =========================================================
# REPORT FILE SAFETY HELPER
# =========================================================

def resolve_safe_report_path(
    report_path
):
    """
    Resolve and validate report file path safely.
    Prevents access outside allowed report folders.
    """

    if not report_path:

        return None

    normalized_path = str(
        report_path
    ).replace(
        "\\",
        "/"
    ).strip()

    allowed_prefixes = [
        "reports/",
        "excel_reports/"
    ]

    is_allowed = False

    for prefix in allowed_prefixes:

        if normalized_path.startswith(
            prefix
        ):

            is_allowed = True
            break

    if not is_allowed:

        return None

    absolute_path = os.path.abspath(
        normalized_path
    )

    project_root = os.path.abspath(
        "."
    )

    if not absolute_path.startswith(
        project_root
    ):

        return None

    if not os.path.exists(
        absolute_path
    ):

        return None

    if not os.path.isfile(
        absolute_path
    ):

        return None

    return absolute_path


# =========================================================
# REPORT CONTENT READER
# =========================================================

def read_report_preview_content(
    file_path
):
    """
    Read preview content for supported text-based report files.
    """

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            content = file.read()

        return content

    except UnicodeDecodeError:

        try:

            with open(
                file_path,
                "r",
                encoding="latin-1"
            ) as file:

                content = file.read()

            return content

        except Exception:

            return "Unable to preview this file content."

    except Exception as error:

        return f"Unable to read report file. Error: {str(error)}"


# =========================================================
# LIVE AUDIT DATA
# =========================================================

def load_live_audit_data():
    """
    Load live governance audit events.
    """

    approvals = load_live_approval_data()

    governance_audit_logs = approvals.get(
        "governance_audit_logs",
        []
    )

    normalized_events = []

    for event in governance_audit_logs:

        event_type = event.get(
            "event_type",
            event.get(
                "event",
                "-"
            )
        )

        created_at = event.get(
            "created_at",
            event.get(
                "timestamp",
                "-"
            )
        )

        normalized_events.append(
            {
                "event_type": event_type,
                "event": event_type,
                "approval_id": event.get(
                    "approval_id",
                    "-"
                ),
                "action_name": event.get(
                    "action_name",
                    "-"
                ),
                "target_name": event.get(
                    "target_name",
                    "-"
                ),
                "status": event.get(
                    "status",
                    "-"
                ),
                "performed_by": event.get(
                    "performed_by",
                    "System"
                ),
                "message": event.get(
                    "message",
                    "-"
                ),
                "created_at": created_at,
                "timestamp": created_at
            }
        )

    reversed_events = list(
        reversed(
            normalized_events
        )
    )

    return {
        "total_events": len(
            normalized_events
        ),
        "events": reversed_events,
        "audit_events": reversed_events,
        "audit_logs": reversed_events
    }


# =========================================================
# DASHBOARD METRICS BUILDER
# =========================================================

def build_live_dashboard_metrics():
    """
    Build dashboard metrics from live repositories.
    """

    incidents = load_live_incidents()
    approvals = load_live_approval_data()
    actions = load_live_actions()
    reports = load_live_reports()
    audit = load_live_audit_data()

    healthy_incidents = len(
        [
            incident for incident in incidents
            if str(
                incident.get(
                    "overall_status",
                    ""
                )
            ).upper() == "HEALTHY"
        ]
    )

    attention_required = len(
        incidents
    ) - healthy_incidents

    platform_health = "STABLE"

    if attention_required > 0:

        platform_health = "ATTENTION REQUIRED"

    latest_status = "N/A"
    latest_report = reports.get(
        "latest_report",
        "-"
    )

    if incidents:

        latest_status = incidents[
            -1
        ].get(
            "overall_status",
            "N/A"
        )

    return {
        "platform_status": "ONLINE",
        "overall_status": "HEALTHY"
        if platform_health == "STABLE"
        else "ATTENTION REQUIRED",
        "platform_health": platform_health,

        "total_incidents": len(
            incidents
        ),
        "incident_count": len(
            incidents
        ),
        "incidents": len(
            incidents
        ),

        "healthy_incidents": healthy_incidents,
        "attention_required": attention_required,

        "total_actions": actions.get(
            "total_actions",
            0
        ),
        "actions": actions.get(
            "total_actions",
            0
        ),
        "action_count": actions.get(
            "total_actions",
            0
        ),

        "total_reports": reports.get(
            "total_reports",
            0
        ),
        "reports": reports.get(
            "total_reports",
            0
        ),
        "report_count": reports.get(
            "total_reports",
            0
        ),

        "total_audit_events": audit.get(
            "total_events",
            0
        ),
        "audit_events": audit.get(
            "total_events",
            0
        ),
        "audit_count": audit.get(
            "total_events",
            0
        ),

        "pending_requests": approvals.get(
            "pending_count",
            0
        ),
        "pending_approvals": approvals.get(
            "pending_count",
            0
        ),

        "approved_requests": approvals.get(
            "approved_count",
            0
        ),
        "approved": approvals.get(
            "approved_count",
            0
        ),

        "rejected_requests": approvals.get(
            "rejected_count",
            0
        ),
        "rejected": approvals.get(
            "rejected_count",
            0
        ),

        "total_requests": approvals.get(
            "total_count",
            0
        ),

        "execution_records": approvals.get(
            "execution_count",
            0
        ),
        "executions": approvals.get(
            "execution_count",
            0
        ),

        "latest_status": latest_status,
        "latest_report": latest_report,
        "repository_records": len(
            incidents
        ),
        "recent_governance_activity": audit.get(
            "audit_events",
            []
        )[:5]
    }


# =========================================================
# LIVE MONITORING DATA
# =========================================================

def load_live_monitoring_data():
    """
    Load monitoring dashboard data safely.
    """

    try:

        from app.monitoring.monitoring_dashboard import (
            get_monitoring_dashboard_data
        )

        monitoring_data = get_monitoring_dashboard_data()

        if monitoring_data:

            return monitoring_data

    except Exception:

        pass

    incidents = load_live_incidents()

    if incidents:

        latest_incident = incidents[
            -1
        ]

        return {
            "overall_status": latest_incident.get(
                "overall_status",
                "UNKNOWN"
            ),
            "cpu_sessions": 0,
            "blocking_sessions": 0,
            "long_queries": 0,
            "last_check": latest_incident.get(
                "timestamp",
                "Not available"
            ),
            "incident_summary": latest_incident.get(
                "incident_summary",
                "No monitoring summary available."
            )
        }

    return {
        "overall_status": "UNKNOWN",
        "cpu_sessions": 0,
        "blocking_sessions": 0,
        "long_queries": 0,
        "last_check": "Not available",
        "incident_summary": "Monitoring dashboard data is not available."
    }


# =========================================================
# HOME
# =========================================================

@router.get("/")
def home():
    """
    Home endpoint.
    """

    return {
        "platform": "Autonomous AI DBA Operations Platform",
        "status": "RUNNING"
    }


# =========================================================
# DEBUG LIVE DATA
# =========================================================

@router.get("/debug/live-data")
def debug_live_data():
    """
    Debug route to verify live repository data loading.
    """

    debug_result = {
        "status": "DEBUG_STARTED",
        "errors": [],
        "checked_files": {
            "pending_approvals": os.path.exists(
                "approval_requests/pending_approvals.json"
            ),
            "approval_history": os.path.exists(
                "approval_requests/approval_history.json"
            ),
            "execution_history": os.path.exists(
                "approval_requests/execution_history.json"
            ),
            "governance_audit_log": os.path.exists(
                "approval_requests/governance_audit_log.json"
            ),
            "repository_incidents": os.path.exists(
                "repository/incidents.json"
            ),
            "root_incidents": os.path.exists(
                "incidents.json"
            ),
            "repository_actions": os.path.exists(
                "repository/actions.json"
            ),
            "root_actions": os.path.exists(
                "actions.json"
            ),
            "reports_folder": os.path.exists(
                "reports"
            ),
            "excel_reports_folder": os.path.exists(
                "excel_reports"
            )
        }
    }

    try:

        incidents = load_live_incidents()

        debug_result[
            "incidents_count"
        ] = len(
            incidents
        )

        debug_result[
            "incidents_sample"
        ] = incidents[:3]

    except Exception as error:

        debug_result[
            "errors"
        ].append(
            {
                "section": "incidents",
                "error": str(
                    error
                )
            }
        )

    try:

        actions = load_live_actions()

        debug_result[
            "actions_count"
        ] = actions.get(
            "total_actions",
            0
        )

        debug_result[
            "actions_sample"
        ] = actions.get(
            "actions",
            []
        )[:3]

    except Exception as error:

        debug_result[
            "errors"
        ].append(
            {
                "section": "actions",
                "error": str(
                    error
                )
            }
        )

    try:

        reports = load_live_reports()

        debug_result[
            "reports_count"
        ] = reports.get(
            "total_reports",
            0
        )

        debug_result[
            "reports_sample"
        ] = reports.get(
            "reports",
            []
        )[:5]

    except Exception as error:

        debug_result[
            "errors"
        ].append(
            {
                "section": "reports",
                "error": str(
                    error
                )
            }
        )

    try:

        approvals = load_live_approval_data()

        debug_result[
            "pending_approvals"
        ] = approvals.get(
            "pending_count",
            0
        )

        debug_result[
            "approved_count"
        ] = approvals.get(
            "approved_count",
            0
        )

        debug_result[
            "rejected_count"
        ] = approvals.get(
            "rejected_count",
            0
        )

        debug_result[
            "execution_count"
        ] = approvals.get(
            "execution_count",
            0
        )

        debug_result[
            "audit_count"
        ] = approvals.get(
            "audit_count",
            0
        )

        debug_result[
            "audit_sample"
        ] = approvals.get(
            "governance_audit_logs",
            []
        )[:3]

    except Exception as error:

        debug_result[
            "errors"
        ].append(
            {
                "section": "approvals_audit",
                "error": str(
                    error
                )
            }
        )

    try:

        dashboard = build_live_dashboard_metrics()

        debug_result[
            "dashboard"
        ] = dashboard

    except Exception as error:

        debug_result[
            "errors"
        ].append(
            {
                "section": "dashboard",
                "error": str(
                    error
                )
            }
        )

    if debug_result[
        "errors"
    ]:

        debug_result[
            "status"
        ] = "DEBUG_COMPLETED_WITH_ERRORS"

    else:

        debug_result[
            "status"
        ] = "DEBUG_COMPLETED_SUCCESSFULLY"

    return debug_result


# =========================================================
# DASHBOARD
# =========================================================

@router.get("/dashboard")
def dashboard(
    request: Request
):
    """
    Render Dashboard page with live repository data.
    """

    metrics = build_live_dashboard_metrics()

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "metrics": metrics,
            "dashboard": metrics,
            "dashboard_data": metrics,
            "data": metrics,

            "total_incidents": metrics.get(
                "total_incidents",
                0
            ),
            "incident_count": metrics.get(
                "incident_count",
                0
            ),
            "incidents": metrics.get(
                "incidents",
                0
            ),

            "total_actions": metrics.get(
                "total_actions",
                0
            ),
            "actions_count": metrics.get(
                "total_actions",
                0
            ),
            "actions": metrics.get(
                "actions",
                0
            ),

            "total_reports": metrics.get(
                "total_reports",
                0
            ),
            "reports_count": metrics.get(
                "total_reports",
                0
            ),
            "reports": metrics.get(
                "reports",
                0
            ),

            "total_audit_events": metrics.get(
                "total_audit_events",
                0
            ),
            "audit_events": metrics.get(
                "audit_events",
                0
            ),

            "pending_approvals": metrics.get(
                "pending_approvals",
                0
            ),
            "pending_requests": metrics.get(
                "pending_requests",
                0
            ),

            "approved_requests": metrics.get(
                "approved_requests",
                0
            ),
            "approved": metrics.get(
                "approved",
                0
            ),

            "rejected_requests": metrics.get(
                "rejected_requests",
                0
            ),
            "rejected": metrics.get(
                "rejected",
                0
            ),

            "execution_records": metrics.get(
                "execution_records",
                0
            ),
            "executions": metrics.get(
                "executions",
                0
            ),

            "recent_governance_activity": metrics.get(
                "recent_governance_activity",
                []
            )
        }
    )


# =========================================================
# MONITORING
# =========================================================

@router.get("/monitoring")
def monitoring(
    request: Request
):
    """
    Render Monitoring page.
    """

    monitoring_data = load_live_monitoring_data()

    return templates.TemplateResponse(
        request=request,
        name="monitoring.html",
        context={
            "monitoring": monitoring_data,
            "monitoring_data": monitoring_data,
            "monitoring_start_result": None
        }
    )


# =========================================================
# START MONITORING FROM UI
# =========================================================

@router.post("/monitoring/start")
def start_monitoring_from_ui(
    request: Request
):
    """
    Start MCP monitoring workflow from Monitoring UI.
    """

    try:

        from app.mcp_server.workflow_manager import (
            execute_workflow
        )

        from app.automation.governance_audit_manager import (
            add_governance_audit_log
        )

        workflow_result = execute_workflow()

        add_governance_audit_log(
            event_type="MONITORING_STARTED_FROM_UI",
            approval_id=None,
            action_name="START_MONITORING",
            target_name="SQL Server Monitoring Workflow",
            status=workflow_result.get(
                "status",
                "UNKNOWN"
            ),
            performed_by="Lead DBA",
            message="Monitoring workflow started from FastAPI Monitoring UI."
        )

        monitoring_start_result = {
            "status": workflow_result.get(
                "status",
                "UNKNOWN"
            ),
            "overall_status": workflow_result.get(
                "overall_status",
                "UNKNOWN"
            ),
            "execution_mode": "MCP_WORKFLOW",
            "message": "Monitoring workflow executed successfully from UI.",
            "report_file": workflow_result.get(
                "report_file"
            ),
            "sql_action": workflow_result.get(
                "sql_action_result",
                workflow_result.get(
                    "sql_action"
                )
            ),
            "sql_risk": workflow_result.get(
                "sql_risk_result",
                workflow_result.get(
                    "sql_risk"
                )
            ),
            "validation_result": workflow_result.get(
                "validation_result"
            ),
            "execution_result": workflow_result.get(
                "execution_result"
            ),
            "verification_result": workflow_result.get(
                "verification_result"
            ),
            "remediation_result": workflow_result.get(
                "remediation_result"
            )
        }

    except Exception as error:

        monitoring_start_result = {
            "status": "FAILED",
            "overall_status": "FAILED",
            "execution_mode": "MCP_WORKFLOW",
            "message": str(
                error
            ),
            "report_file": None,
            "sql_action": None,
            "sql_risk": None,
            "validation_result": None,
            "execution_result": None,
            "verification_result": None,
            "remediation_result": None
        }

    monitoring_data = load_live_monitoring_data()

    return templates.TemplateResponse(
        request=request,
        name="monitoring.html",
        context={
            "monitoring": monitoring_data,
            "monitoring_data": monitoring_data,
            "monitoring_start_result": monitoring_start_result
        }
    )


# =========================================================
# ANALYTICS
# =========================================================

@router.get("/analytics")
def analytics(
    request: Request
):
    """
    Render Analytics page with live incident and governance data.
    """

    incidents = load_live_incidents()
    approvals = load_live_approval_data()

    total_incidents = len(
        incidents
    )

    healthy_incidents = len(
        [
            incident for incident in incidents
            if str(
                incident.get(
                    "overall_status",
                    ""
                )
            ).upper() == "HEALTHY"
        ]
    )

    attention_required = total_incidents - healthy_incidents

    health_score = 100

    if total_incidents > 0:

        health_score = round(
            (
                healthy_incidents / total_incidents
            ) * 100,
            2
        )

    risk_level = "LOW"

    if attention_required > 0:

        risk_level = "MEDIUM"

    if attention_required >= 3:

        risk_level = "HIGH"

    analytics_data = {
        "status": "ACTIVE",
        "total_incidents": total_incidents,
        "healthy_incidents": healthy_incidents,
        "attention_required": attention_required,
        "health_score": health_score,
        "risk_level": risk_level,
        "automation_mode": "SIMULATED",
        "pending_approvals": approvals.get(
            "pending_count",
            0
        ),
        "execution_records": approvals.get(
            "execution_count",
            0
        ),
        "audit_events": approvals.get(
            "audit_count",
            0
        )
    }

    daily_summary = {
        "date": str(
            date.today()
        ),
        "summary": (
            "Live analytics data loaded successfully from repository."
            if total_incidents > 0
            else "No incident data found yet. Run monitoring workflow to generate analytics data."
        ),
        "platform_health": "STABLE"
        if attention_required == 0
        else "ATTENTION REQUIRED"
    }

    return templates.TemplateResponse(
        request=request,
        name="analytics.html",
        context={
            "analytics": analytics_data,
            "analytics_data": analytics_data,
            "summary": daily_summary,
            "daily_summary": daily_summary,

            "health_score": health_score,
            "risk_level": risk_level,
            "automation_mode": analytics_data.get(
                "automation_mode",
                "SIMULATED"
            ),
            "total_incidents": total_incidents,
            "healthy_incidents": healthy_incidents,
            "attention_required": attention_required
        }
    )


# =========================================================
# INCIDENT REPOSITORY
# =========================================================

@router.get("/incidents")
def incidents(
    request: Request,
    status: Optional[str] = None,
    q: Optional[str] = None
):
    """
    Render Incidents page with live repository data.
    """

    incidents_data = load_live_incidents()

    if status:

        incidents_data = [
            item for item in incidents_data
            if str(
                item.get(
                    "overall_status",
                    ""
                )
            ).upper() == status.upper()
            or str(
                item.get(
                    "status",
                    ""
                )
            ).upper() == status.upper()
        ]

    if q:

        query = q.lower()

        incidents_data = [
            item for item in incidents_data
            if query in str(
                item
            ).lower()
        ]

    return templates.TemplateResponse(
        request=request,
        name="incidents.html",
        context={
            "incidents": incidents_data,
            "incident_records": incidents_data,
            "incident_data": incidents_data,
            "total_incidents": len(
                incidents_data
            ),
            "selected_status": status or "",
            "search_query": q or ""
        }
    )


# =========================================================
# INCIDENT DETAILS
# =========================================================

@router.get("/incidents/{incident_index}")
def incident_details(
    request: Request,
    incident_index: int
):
    """
    Render Incident Details page.
    """

    incidents_data = load_live_incidents()

    if 0 <= incident_index < len(
        incidents_data
    ):

        incident = incidents_data[
            incident_index
        ]

    else:

        incident = None

    return templates.TemplateResponse(
        request=request,
        name="incident_details.html",
        context={
            "incident": incident
        }
    )


# =========================================================
# ACTION REPOSITORY
# =========================================================

@router.get("/actions")
def actions(
    request: Request
):
    """
    Render Actions page with live action data.
    """

    actions_data = load_live_actions()

    action_records = actions_data.get(
        "actions",
        []
    )

    return templates.TemplateResponse(
        request=request,
        name="actions.html",
        context={
            "actions": actions_data,
            "actions_data": actions_data,
            "action_records": action_records,
            "total_actions": actions_data.get(
                "total_actions",
                0
            )
        }
    )


# =========================================================
# REPORTS CENTER
# =========================================================

@router.get("/reports")
def reports(
    request: Request
):
    """
    Render Reports page with live reports folder data.
    """

    reports_data = load_live_reports()

    report_files = reports_data.get(
        "reports",
        []
    )

    return templates.TemplateResponse(
        request=request,
        name="reports.html",
        context={
            "reports": reports_data,
            "reports_data": reports_data,
            "report_files": report_files,
            "total_reports": reports_data.get(
                "total_reports",
                0
            ),
            "latest_report": reports_data.get(
                "latest_report",
                "-"
            )
        }
    )


# =========================================================
# REPORT VIEW
# =========================================================

@router.get("/reports/view")
def view_report(
    request: Request,
    file_path: str
):
    """
    View supported report file content in browser.
    """

    safe_path = resolve_safe_report_path(
        file_path
    )

    if not safe_path:

        return HTMLResponse(
            content="""
            <html>
                <body style="font-family: Arial; padding: 30px;">
                    <h3>Invalid or missing report file.</h3>
                    <p>The selected report file could not be found or is not allowed.</p>
                    <a href="/reports">Back to Reports</a>
                </body>
            </html>
            """,
            status_code=404
        )

    file_name = os.path.basename(
        safe_path
    )

    file_extension = os.path.splitext(
        file_name
    )[1].lower()

    preview_supported_extensions = [
        ".txt",
        ".json",
        ".csv",
        ".log",
        ".md"
    ]

    if file_extension not in preview_supported_extensions:

        return templates.TemplateResponse(
            request=request,
            name="report_view.html",
            context={
                "report_name": file_name,
                "report_path": file_path,
                "report_content": "Preview is not available for this file type. Please use the Download button.",
                "preview_supported": False,
                "file_extension": file_extension
            }
        )

    report_content = read_report_preview_content(
        safe_path
    )

    return templates.TemplateResponse(
        request=request,
        name="report_view.html",
        context={
            "report_name": file_name,
            "report_path": file_path,
            "report_content": report_content,
            "preview_supported": True,
            "file_extension": file_extension
        }
    )


# =========================================================
# REPORT DOWNLOAD
# =========================================================

@router.get("/reports/download")
def download_report(
    file_path: str
):
    """
    Download selected report file.
    """

    safe_path = resolve_safe_report_path(
        file_path
    )

    if not safe_path:

        return HTMLResponse(
            content="""
            <html>
                <body style="font-family: Arial; padding: 30px;">
                    <h3>Invalid or missing report file.</h3>
                    <p>The selected report file could not be found or is not allowed.</p>
                    <a href="/reports">Back to Reports</a>
                </body>
            </html>
            """,
            status_code=404
        )

    file_name = os.path.basename(
        safe_path
    )

    return FileResponse(
        path=safe_path,
        filename=file_name,
        media_type="application/octet-stream"
    )


# =========================================================
# AUDIT LOGS
# =========================================================

@router.get("/audit")
def audit(
    request: Request
):
    """
    Render Audit Logs page with governance audit data.
    """

    audit_data = load_live_audit_data()

    audit_events = audit_data.get(
        "audit_events",
        []
    )

    return templates.TemplateResponse(
        request=request,
        name="audits.html",
        context={
            "audit": audit_data,
            "audit_data": audit_data,
            "audit_events": audit_events,
            "events": audit_events,
            "audit_logs": audit_events,
            "total_events": audit_data.get(
                "total_events",
                0
            ),
            "total_audit_events": audit_data.get(
                "total_events",
                0
            )
        }
    )


# =========================================================
# GOVERNANCE APPROVALS
# =========================================================

@router.get("/approvals")
def approvals(
    request: Request
):
    """
    Render Governance Approval page.
    """

    approvals_data = load_live_approval_data()

    return templates.TemplateResponse(
        request=request,
        name="approvals.html",
        context={
            "approvals": approvals_data,
            "approval_data": approvals_data,
            "pending_approvals": approvals_data.get(
                "pending_approvals",
                []
            ),
            "approval_history": approvals_data.get(
                "approval_history",
                []
            ),
            "execution_history": approvals_data.get(
                "execution_history",
                []
            ),
            "governance_audit_logs": approvals_data.get(
                "governance_audit_logs",
                []
            ),
            "pending_count": approvals_data.get(
                "pending_count",
                0
            ),
            "approved_count": approvals_data.get(
                "approved_count",
                0
            ),
            "rejected_count": approvals_data.get(
                "rejected_count",
                0
            ),
            "execution_count": approvals_data.get(
                "execution_count",
                0
            ),
            "audit_count": approvals_data.get(
                "audit_count",
                0
            ),
            "total_requests": approvals_data.get(
                "total_count",
                0
            )
        }
    )


# =========================================================
# APPROVE REQUEST
# =========================================================

@router.get("/approve/{request_id}")
def approve(
    request_id: str
):
    """
    Approve governance request.
    """

    try:

        from app.approvals.approval_manager import (
            approve_approval_request
        )

        approve_approval_request(
            approval_id=request_id,
            approved_by="Lead DBA",
            decision_reason="Approved from FastAPI Governance dashboard."
        )

    except Exception:

        try:

            from app.governance.approval_actions import (
                approve_request
            )

            approve_request(
                request_id
            )

        except Exception:

            pass

    return RedirectResponse(
        url="/approvals",
        status_code=303
    )


# =========================================================
# REJECT REQUEST
# =========================================================

@router.get("/reject/{request_id}")
def reject(
    request_id: str
):
    """
    Reject governance request.
    """

    try:

        from app.approvals.approval_manager import (
            reject_approval_request
        )

        reject_approval_request(
            approval_id=request_id,
            rejected_by="Lead DBA",
            decision_reason="Rejected from FastAPI Governance dashboard."
        )

    except Exception:

        try:

            from app.governance.approval_actions import (
                reject_request
            )

            reject_request(
                request_id
            )

        except Exception:

            pass

    return RedirectResponse(
        url="/approvals",
        status_code=303
    )


# =========================================================
# EXECUTE APPROVED REQUEST
# =========================================================

@router.get("/execute/{request_id}")
def execute_approved(
    request_id: str
):
    """
    Execute approved remediation request.
    """

    try:

        from app.automation.approval_execution_console import (
            execute_approved_request
        )

        execute_approved_request(
            request_id
        )

    except Exception:

        pass

    return RedirectResponse(
        url="/approvals",
        status_code=303
    )


# =========================================================
# NLP DBA ASSISTANT - GET
# =========================================================

@router.get("/assistant")
def assistant_page(
    request: Request
):
    """
    Render NLP DBA Assistant page.
    """

    return templates.TemplateResponse(
        request=request,
        name="assistant.html",
        context={
            "assistant_result": None,
            "user_query": ""
        }
    )


# =========================================================
# NLP DBA ASSISTANT - POST
# =========================================================

@router.post("/assistant")
def assistant_query(
    request: Request,
    user_query: str = Form(...)
):
    """
    Handle NLP DBA Assistant query.
    """

    try:

        from app.nlp_assistant.dba_assistant import (
            handle_dba_query
        )

        assistant_result = handle_dba_query(
            user_query
        )

    except Exception as error:

        assistant_result = {
            "user_query": user_query,
            "intent": "ERROR",
            "confidence": "LOW",
            "risk_level": "LOW",
            "assistant_response": "Failed to process DBA assistant query.",
            "summary": {
                "error": str(
                    error
                )
            },
            "recommended_next_action": "Check NLP DBA Assistant backend logs and module imports.",
            "workflow_result": {
                "workflow_status": "FAILED",
                "message": str(
                    error
                )
            }
        }

    return templates.TemplateResponse(
        request=request,
        name="assistant.html",
        context={
            "assistant_result": assistant_result,
            "user_query": user_query
        }
    )