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

from app.governance.approval_search import (
    get_all_approvals
)

from app.governance.approval_actions import (
    approve_request,
    reject_request
)
from app.repository.incident_repository import (
    load_incidents
)
from app.repository.incident_search import (
    get_incident_by_index
)

from app.analytics.analytics_manager import (
    get_analytics_status
)

from app.analytics.daily_summary import (
    get_daily_summary
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

    """
    Dashboard page.
    """

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
# INCIDENTS
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

@router.get(
    "/incidents/{incident_index}"
)
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

    """
    Governance approvals page.
    """

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

@router.get(
    "/approve/{request_id}"
)
def approve(

    request_id: str

):

    """
    Approve governance request.
    """

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

@router.get(
    "/reject/{request_id}"
)
def reject(

    request_id: str

):

    """
    Reject governance request.
    """

    reject_request(

        request_id

    )

    return RedirectResponse(

        url="/approvals",

        status_code=303

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