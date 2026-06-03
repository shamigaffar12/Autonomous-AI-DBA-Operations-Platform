# =========================================================
# Notification Executor
# Autonomous AI DBA Operations Platform
# =========================================================

from app.notifications.notification_manager import (
    send_notifications
)


# =========================================================
# EXECUTE NOTIFICATION WORKFLOW
# =========================================================

def run_notifications(

    overall_status,

    incident_summary

):

    """
    Execute notification workflow.
    """

    print(

        "\nStarting Notification Workflow...\n"
    )

    send_notifications(

        overall_status,

        incident_summary
    )

    print(

        "\nNotification Workflow Completed.\n"
    )