# =========================================================
# FastAPI Application
# Autonomous AI DBA Operations Platform
# =========================================================

from fastapi import FastAPI

from app.web.approval_routes import (
    router as approval_router
)

from app.web.routes import (
    router
)


app = FastAPI(
    title="Autonomous AI DBA Operations Platform",
    version="1.0.0"
)


# Approval router must be included first
app.include_router(
    approval_router
)

app.include_router(
    router
)