# =========================================================
# FastAPI Application
# Autonomous AI DBA Operations Platform
# =========================================================

from fastapi import FastAPI

from app.web.routes import (
    router
)



app = FastAPI(

    title=
    "Autonomous AI DBA Operations Platform",

    version=
    "1.0.0"

)

app.include_router(
    router
)

