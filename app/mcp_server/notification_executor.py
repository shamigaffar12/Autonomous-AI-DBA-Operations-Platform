# =========================================================
# Notification Executor
# Autonomous AI DBA Operations Platform
# =========================================================

from app.notifications.notification_manager import (
    send_notifications
)

from app.audit.audit_logger import (
    write_audit_log
)

from app.common.error_handler import (
    handle_error
)

from app.common.custom_exception import (
    NotificationException
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

    try:

        write_audit_log(
            "NOTIFICATION WORKFLOW STARTED"
        )

        print(
            "\nStarting Notification Workflow...\n"
        )

        result = send_notifications(
            overall_status,
            incident_summary
        )

        if result is False:

            raise NotificationException(
                "Notification workflow failed."
            )

        print(
            "\nNotification Workflow Completed.\n"
        )

        write_audit_log(
            "NOTIFICATION WORKFLOW COMPLETED"
        )

        return True

    except Exception as error:

        write_audit_log(
            "NOTIFICATION WORKFLOW FAILED"
        )

        return handle_error(
            "NOTIFICATION EXECUTOR",
            error
        )


# =========================================================
# TEST EXECUTION
# =========================================================

if __name__ == "__main__":

    run_notifications(
        "ATTENTION REQUIRED",
        "Blocking Session Detected"
    )