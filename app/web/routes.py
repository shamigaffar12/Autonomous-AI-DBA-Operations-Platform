# =========================================================
# Web Routes
# Autonomous AI DBA Operations Platform
# =========================================================

from fastapi import (
    APIRouter,
    Request
)

from fastapi.templating import (
    Jinja2Templates
)

from fastapi.responses import (
    RedirectResponse
)

from app.dashboard.dashboard_data import (
    get_dashboard_metrics
)

from app.monitoring.monitoring_dashboard import (
    get_monitoring_dashboard_data
)

from app.analytics.analytics_manager import (
    get_analytics_status
)

from app.analytics.daily_summary import (
    get_daily_summary
)

from app.repository.incident_repository import (
    load_incidents
)

from app.repository.incident_search import (
    get_incident_by_index
)

from app.repository.action_dashboard import (
    get_action_dashboard_data
)

from app.governance.approval_search import (
    get_all_approvals
)

from app.governance.approval_actions import (
    approve_request,
    reject_request
)
from app.audit.audit_dashboard import (
    get_audit_dashboard_data
)
from app.reporting.report_dashboard import (
    get_report_dashboard_data
)
# =========================================================
# ROUTER
# =========================================================

router = APIRouter()

templates = Jinja2Templates(
    directory="templates"
)

# =========================================================
# HOME
# =========================================================

@router.get("/")
def home():

    """
    Home endpoint.
    """

    return {

        "platform":
        "Autonomous AI DBA Operations Platform",

        "status":
        "RUNNING"

    }


# =========================================================
# DASHBOARD
# =========================================================

@router.get("/dashboard")
def dashboard(

    request: Request

):

    metrics = (

        get_dashboard_metrics()

    )

    return templates.TemplateResponse(

        request=request,

        name="dashboard.html",

        context={

            "metrics":
            metrics

        }

    )


# =========================================================
# MONITORING
# =========================================================

@router.get("/monitoring")
def monitoring(

    request: Request

):

    monitoring_data = (

        get_monitoring_dashboard_data()

    )

    return templates.TemplateResponse(

        request=request,

        name="monitoring.html",

        context={

            "monitoring":
            monitoring_data

        }

    )


# =========================================================
# ANALYTICS
# =========================================================

@router.get("/analytics")
def analytics(

    request: Request

):

    analytics_data = (

        get_analytics_status()

    )

    daily_summary = (

        get_daily_summary()

    )

    return templates.TemplateResponse(

        request=request,

        name="analytics.html",

        context={

            "analytics":
            analytics_data,

            "summary":
            daily_summary

        }

    )


# =========================================================
# INCIDENT REPOSITORY
# =========================================================

@router.get("/incidents")
def incidents(

    request: Request

):

    incidents_data = (

        load_incidents()

    )

    return templates.TemplateResponse(

        request=request,

        name="incidents.html",

        context={

            "incidents":
            incidents_data

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

    incident = (

        get_incident_by_index(

            incident_index

        )

    )

    return templates.TemplateResponse(

        request=request,

        name="incident_details.html",

        context={

            "incident":
            incident

        }

    )


# =========================================================
# GOVERNANCE APPROVALS
# =========================================================

@router.get("/approvals")
def approvals(

    request: Request

):

    approvals_data = (

        get_all_approvals()

    )

    return templates.TemplateResponse(

        request=request,

        name="approvals.html",

        context={

            "approvals":
            approvals_data

        }

    )


# =========================================================
# APPROVE REQUEST
# =========================================================

@router.get("/approve/{request_id}")
def approve(

    request_id: str

):

    approve_request(

        request_id

    )

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

    reject_request(

        request_id

    )

    return RedirectResponse(

        url="/approvals",

        status_code=303

    )


# =========================================================
# ACTION REPOSITORY
# =========================================================

@router.get("/actions")
def actions(

    request: Request

):

    actions_data = (

        get_action_dashboard_data()

    )

    print(

        "\nACTIONS DATA:\n"

    )

    print(

        actions_data

    )

    return templates.TemplateResponse(

        request=request,

        name="actions.html",

        context={

            "actions":
            actions_data

        }

    )
    
    # =========================================================
# AUDIT DASHBOARD
# =========================================================

@router.get("/audit")
def audit(

    request: Request

):

    audit_data = (

        get_audit_dashboard_data()

    )

    return templates.TemplateResponse(

        request=request,

        name="audits.html",

        context={

            "audit":
            audit_data

        }

    )
    
    # =========================================================
# REPORTS CENTER
# =========================================================

@router.get("/reports")
def reports(

    request: Request

):

    reports_data = (

        get_report_dashboard_data()

    )

    return templates.TemplateResponse(

        request=request,

        name="reports.html",

        context={

            "reports":
            reports_data

        }

    )