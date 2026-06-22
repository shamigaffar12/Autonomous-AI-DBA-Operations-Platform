# =========================================================
# FastAPI Web Application
# Autonomous AI DBA Operations Platform
# =========================================================

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.web.report_routes import router as report_router
from app.web.dashboard_routes import router as dashboard_router
from app.web.nlp_execution_routes import router as nlp_execution_router
from app.web.routes import router as web_router
from app.web.approval_routes import router as approval_router


# =========================================================
# FASTAPI APPLICATION
# =========================================================

app = FastAPI(
    title="Autonomous AI DBA Operations Platform",
    description="AI-powered database operations, governance, monitoring, reporting, and automation center.",
    version="1.0.0"
)


# =========================================================
# STATIC FILES
# =========================================================

app.mount(
    "/static",
    StaticFiles(
        directory="static"
    ),
    name="static"
)


# =========================================================
# ROUTER REGISTRATION
# =========================================================
# Important:
# dashboard_router must be registered before web_router because
# an older /dashboard route may already exist inside routes.py.
#
# report_router must also be registered before web_router because
# old /reports routes may already exist in routes.py.
#
# nlp_execution_router is registered before web_router so
# approval execution APIs remain available.

app.include_router(
    report_router
)

app.include_router(
    dashboard_router
)

app.include_router(
    nlp_execution_router
)

app.include_router(
    web_router
)

app.include_router(
    approval_router
)


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get(
    "/health"
)
def health_check():
    """
    Application health check endpoint.
    """

    return {
        "application": "Autonomous AI DBA Operations Platform",
        "status": "RUNNING",
        "web": "ACTIVE",
        "dashboard": "LIVE_DATA_ACTIVE",
        "reporting": "MONTHLY_EXCEL_REPORTING_ACTIVE",
        "nlp_approval_execution": "ACTIVE"
    }