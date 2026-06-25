# =========================================================
# Notification Manager
# Autonomous AI DBA Operations Platform
# =========================================================

from app.notifications.email_notifier import send_email_alert
from app.notifications.teams_notifier import send_teams_alert


def build_teams_summary(
    overall_status,
    incident_summary
):
    lines = [
        f"SQL Alert: {overall_status}"
    ]

    summary = str(
        incident_summary or ""
    )

    if "Blocking Sessions Detected:" in summary:
        lines.append(
            "Blocking session detected"
        )

    if "Long Running Query Analysis:" in summary:
        lines.append(
            "Long running query detected"
        )

    if "High CPU Usage Detected" in summary:
        lines.append(
            "High CPU usage detected"
        )

    if len(lines) == 1:
        lines.append(
            summary[:800]
        )

    return "\n".join(
        lines
    )


def send_notifications(
    overall_status,
    incident_summary
):

    if str(
        overall_status
    ).upper() == "HEALTHY":

        print(
            "\nSystem Healthy. No notifications required."
        )

        return True

    subject = f"SQL Alert - {overall_status}"

    email_sent = send_email_alert(
        subject,
        incident_summary
    )

    teams_message = build_teams_summary(
        overall_status,
        incident_summary
    )

    teams_sent = send_teams_alert(
        teams_message,
        title=subject
    )

    return bool(
        email_sent or teams_sent
    )


if __name__ == "__main__":

    send_notifications(
        "ATTENTION REQUIRED",
        "SQL Monitoring Summary\nBlocking Sessions Detected:\nSession ID: 52"
    )