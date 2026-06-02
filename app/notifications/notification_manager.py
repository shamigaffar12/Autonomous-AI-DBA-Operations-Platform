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
# SEND NOTIFICATIONS
# =========================================================

def send_notifications(

    overall_status,

    incident_summary

):

    """
    Send notifications only when needed.
    """

    if overall_status == "HEALTHY":

        print(

            "\nSystem Healthy. No notifications required."

        )

        return


    subject = (

        f"SQL Alert - {overall_status}"
    )


    send_email_alert(

        subject,

        incident_summary
    )


    send_teams_alert(

        incident_summary
    )
"""""
if __name__ == "__main__":

    send_notifications(

        "HEALTHY",

        "SQL Monitoring Normal"
    )"""

if __name__ == "__main__":

    send_notifications(

        "ATTENTION REQUIRED",

        "Blocking Session Detected"
    )