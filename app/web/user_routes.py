# =========================================================
# User Management Routes
# Autonomous AI DBA Operations Platform
# =========================================================

from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.security.auth_service import (
    create_or_update_user,
    list_users,
    set_user_active
)

router = APIRouter(
    prefix="/users",
    tags=["User Management"]
)

templates = Jinja2Templates(
    directory="templates"
)


@router.get("")
def users_page(
    request: Request
):
    return templates.TemplateResponse(
        request,
        "users.html",
        {
            "request": request,
            "users": list_users(),
            "message": None,
            "error_message": None,
        },
    )


@router.post("/save")
async def save_user(
    request: Request
):
    form = await request.form()

    try:
        username = str(
            form.get("username", "")
        ).strip()

        display_name = str(
            form.get("display_name", "")
        ).strip()

        role = str(
            form.get("role", "VIEWER")
        ).strip()

        password = str(
            form.get("password", "")
        ).strip() or None

        is_active = str(
            form.get("is_active", "false")
        ).lower() == "true"

        create_or_update_user(
            username=username,
            display_name=display_name,
            role=role,
            password=password,
            is_active=is_active,
        )

        return RedirectResponse(
            url="/users",
            status_code=302
        )

    except Exception as error:

        return templates.TemplateResponse(
            request,
            "users.html",
            {
                "request": request,
                "users": list_users(),
                "message": None,
                "error_message": str(error),
            },
            status_code=400,
        )


@router.post("/activate")
async def activate_user(
    request: Request
):
    form = await request.form()

    username = str(
        form.get("username", "")
    ).strip()

    set_user_active(
        username,
        True
    )

    return RedirectResponse(
        url="/users",
        status_code=302
    )


@router.post("/deactivate")
async def deactivate_user(
    request: Request
):
    form = await request.form()

    username = str(
        form.get("username", "")
    ).strip()

    set_user_active(
        username,
        False
    )

    return RedirectResponse(
        url="/users",
        status_code=302
    )