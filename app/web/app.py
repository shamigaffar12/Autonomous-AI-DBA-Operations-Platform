# =========================================================
# FastAPI Application
# Autonomous AI DBA Operations Platform
# =========================================================

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.web.routes import (
    router
)

from app.web.approval_routes import (
    router as approval_router
)


# =========================================================
# FASTAPI APP
# =========================================================

app = FastAPI(
    title="Autonomous AI DBA Operations Platform",
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
# ROUTERS
# =========================================================

# Main UI routes are loaded first.
app.include_router(
    router
)

# Approval POST action routes are loaded after main UI routes.
app.include_router(
    approval_router
)