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

def build_teams_summary(
    overall_status,
    incident_summary
):
    """
    Create a short Teams-friendly incident message.
    """

    lines = []

    lines.append(
        f"SQL Alert: {overall_status}"
    )

    if "Blocking Sessions Detected:" in incident_summary:

        lines.append(
            "Blocking session detected"
        )

    if "Long Running Query Analysis:" in incident_summary:

        lines.append(
            "Long running query detected"
        )

    if "High CPU Usage Detected" in incident_summary:

        lines.append(
            "High CPU usage detected"
        )

    return "\n".join(lines)


# =========================================================
# SEND NOTIFICATIONS
# =========================================================

def send_notifications(
    overall_status,
    incident_summary
):
    """
    Send notifications only when required.
    """

    # =====================================================
    # HEALTHY SYSTEM
    # =====================================================

    if overall_status.upper() == "HEALTHY":

        print(
            "\nSystem Healthy. No notifications required."
        )

        return True

    # =====================================================
    # EMAIL ALERT
    # =====================================================

    subject = (
        f"SQL Alert - {overall_status}"
    )

    send_email_alert(
        subject,
        incident_summary
    )

    # =====================================================
    # TEAMS ALERT
    # =====================================================

    teams_message = build_teams_summary(
        overall_status,
        incident_summary
    )

    send_teams_alert(
        teams_message
    )

    return True


# =========================================================
# TEST EXECUTION
# =========================================================

if __name__ == "__main__":

    sample_incident = """

    SQL Monitoring Summary

    Blocking Sessions Detected:

    Session ID: 52
    Blocking Session ID: 67

    Overall Status: ATTENTION REQUIRED

    """

    send_notifications(
        "ATTENTION REQUIRED",
        sample_incident
    )