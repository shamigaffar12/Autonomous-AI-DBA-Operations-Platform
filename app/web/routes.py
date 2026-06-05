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