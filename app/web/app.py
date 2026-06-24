# =========================================================
# FastAPI Application
# Autonomous AI DBA Operations Platform
# =========================================================

import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.security.auth_service import (
    auth_route_guard
)

from app.web.auth_routes import (
    router as auth_router
)

from app.web.report_routes import (
    router as report_router
)

from app.web.dashboard_routes import (
    router as dashboard_router
)

from app.web.nlp_execution_routes import (
    router as nlp_execution_router
)

from app.web.routes import (
    router as web_router
)

from app.web.approval_routes import (
    router as approval_router
)


# =========================================================
# APPLICATION CONFIGURATION
# =========================================================

app = FastAPI(
    title="Autonomous AI DBA Operations Platform",
    version="1.0.0"
)


# =========================================================
# AUTHENTICATION AND RBAC MIDDLEWARE
# =========================================================

@app.middleware("http")
async def authentication_and_rbac_middleware(
    request,
    call_next
):
    """
    Enforce authentication and route-level/method-level RBAC.
    """

    return await auth_route_guard(
        request=request,
        call_next=call_next
    )


# =========================================================
# ROUTER REGISTRATION
# =========================================================

app.include_router(
    auth_router
)

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
# STATIC FILES
# =========================================================

if os.path.exists("static"):

    app.mount(
        "/static",
        StaticFiles(directory="static"),
        name="static"
    )


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/health")
def health_check():
    """
    Application health check.
    """

    return {
        "status": "healthy",
        "service": "Autonomous AI DBA Operations Platform"
    }