# =========================================================
# Email Notifier
# Autonomous AI DBA Operations Platform
# =========================================================

import os
import smtplib
from email.message import EmailMessage
from typing import Iterable, List, Optional


def _split_recipients(
    value: str
) -> List[str]:

    return [
        item.strip()
        for item in str(value or "").replace(";", ",").split(",")
        if item.strip()
    ]


def send_email_alert(
    subject: str,
    message: str,
    recipients: Optional[Iterable[str]] = None
) -> bool:

    smtp_host = os.getenv(
        "SMTP_HOST",
        ""
    ).strip()

    smtp_port = int(
        os.getenv(
            "SMTP_PORT",
            "587"
        )
    )

    smtp_username = os.getenv(
        "SMTP_USERNAME",
        ""
    ).strip()

    smtp_password = os.getenv(
        "SMTP_PASSWORD",
        ""
    ).strip()

    smtp_from = os.getenv(
        "SMTP_FROM",
        smtp_username or "ai-dba-platform@example.com"
    ).strip()

    smtp_tls = os.getenv(
        "SMTP_USE_TLS",
        "true"
    ).lower() == "true"

    configured_recipients = list(
        recipients or _split_recipients(
            os.getenv(
                "SMTP_TO",
                ""
            )
        )
    )

    if not smtp_host or not configured_recipients:

        print("\n========================================")
        print(" EMAIL ALERT - SIMULATION MODE ")
        print("========================================")
        print(f"Subject: {subject}")
        print(f"Message:\n{message}")
        print("Reason: SMTP_HOST or SMTP_TO is not configured.")

        return False

    email = EmailMessage()
    email["Subject"] = subject
    email["From"] = smtp_from
    email["To"] = ", ".join(
        configured_recipients
    )
    email.set_content(
        message
    )

    try:
        with smtplib.SMTP(
            smtp_host,
            smtp_port,
            timeout=20
        ) as server:

            if smtp_tls:
                server.starttls()

            if smtp_username and smtp_password:
                server.login(
                    smtp_username,
                    smtp_password
                )

            server.send_message(
                email
            )

        print(
            "Email notification sent successfully."
        )

        return True

    except Exception as error:

        print(
            f"Email notification failed: {error}"
        )

        return False