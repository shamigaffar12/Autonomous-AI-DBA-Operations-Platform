# =========================================================
# NLP Execution Routes
# Autonomous AI DBA Operations Platform
# =========================================================

from fastapi import APIRouter, Form, Request
from fastapi.responses import JSONResponse

from app.nlp_assistant.nlp_approval_execution_service import (
    handle_nlp_approval_request
)


# =========================================================
# ROUTER
# =========================================================

router = APIRouter()


# =========================================================
# CHECK APPROVAL STATUS FROM NLP
# =========================================================

@router.post("/assistant/check-approval")
def check_approval_from_nlp(
    request: Request,
    query: str = Form(...),
    user: str = Form("Lead DBA")
):
    """
    Check approval status using NLP approval ID.
    """

    result = handle_nlp_approval_request(
        natural_language_query=query,
        user=user
    )

    return JSONResponse(
        content=result
    )


# =========================================================
# EXECUTE APPROVAL FROM NLP
# =========================================================

@router.post("/assistant/execute-approval")
def execute_approval_from_nlp(
    request: Request,
    query: str = Form(...),
    user: str = Form("Lead DBA")
):
    """
    Execute approved governance request using NLP approval ID.
    """

    result = handle_nlp_approval_request(
        natural_language_query=query,
        user=user
    )

    return JSONResponse(
        content=result
    )