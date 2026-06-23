# =========================================================
# Authentication Routes
# Autonomous AI DBA Operations Platform
# =========================================================

from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.security.auth_service import (
    authenticate_user,
    clear_auth_cookie,
    create_user_token,
    get_current_user,
    set_auth_cookie
)


# =========================================================
# ROUTER CONFIGURATION
# =========================================================

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

templates = Jinja2Templates(
    directory="templates"
)


# =========================================================
# ROUTES
# =========================================================

@router.get("/login")
def login_page(
    request: Request
):
    """
    Render login page.
    """

    current_user = get_current_user(
        request
    )

    if current_user:
        return RedirectResponse(
            url="/dashboard",
            status_code=302
        )

    return templates.TemplateResponse(
        request,
        "login.html",
        {
            "request": request,
            "error_message": None
        }
    )


@router.post("/login")
async def login_submit(
    request: Request
):
    """
    Handle login form submission.
    """

    form_data = await request.form()

    username = str(
        form_data.get("username", "")
    ).strip()

    password = str(
        form_data.get("password", "")
    )

    user = authenticate_user(
        username=username,
        password=password
    )

    if not user:
        return templates.TemplateResponse(
            request,
            "login.html",
            {
                "request": request,
                "error_message": "Invalid username or password."
            },
            status_code=401
        )

    token = create_user_token(
        user
    )

    response = RedirectResponse(
        url="/dashboard",
        status_code=302
    )

    set_auth_cookie(
        response=response,
        token=token
    )

    return response


@router.get("/logout")
def logout():
    """
    Logout current user.
    """

    response = RedirectResponse(
        url="/auth/login",
        status_code=302
    )

    clear_auth_cookie(
        response=response
    )

    return response