# =========================================================
# Notification Manager
# Autonomous AI DBA Operations Platform
# =========================================================

from app.notifications.email_notifier import (
    send_email_alert
)

from app.notifications.teams_notifier import (
    send_teams_alert
)


# =========================================================
# BUILD TEAMS SUMMARY
# =========================================================

def build_teams_summary(overall_status, incident_summary):

    """
    Create a short Teams-friendly incident message.
    """

    lines = []

    lines.append(f"SQL Alert: {overall_status}")

    if "Blocking Sessions Detected:" in incident_summary:
        lines.append("Blocking session detected")

    if "Long Running Query Analysis:" in incident_summary:
        lines.append("Long running query detected")

    if "High CPU Usage Detected" in incident_summary:
        lines.append("High CPU usage detected")

    return "\n".join(lines)


# =========================================================
# SEND NOTIFICATIONS
# =========================================================

def send_notifications(overall_status, incident_summary):

    """
    Send notifications only when needed.
    """

    if overall_status.upper() == "HEALTHY":

        print("\nSystem Healthy. No notifications required.")
        return

    subject = f"SQL Alert - {overall_status}"

    # Full detail to Email
    send_email_alert(
        subject,
        incident_summary
    )

    # Short summary to Teams
    teams_message = build_teams_summary(
        overall_status,
        incident_summary
    )

    send_teams_alert(
        teams_message
    )


# =========================================================
# TEST EXECUTION
# =========================================================

if __name__ == "__main__":

    send_notifications(
        "ATTENTION REQUIRED",
        "SQL Monitoring Summary\n\nBlocking Sessions Detected:\nSession ID: 52\nBlocking Session ID: 67"
    )