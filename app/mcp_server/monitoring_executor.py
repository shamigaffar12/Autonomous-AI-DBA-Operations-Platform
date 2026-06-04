# =========================================================
# Monitoring Executor
# Autonomous AI DBA Operations Platform
# =========================================================

from app.monitoring.sql_monitor import (
    run_monitoring
)

from app.audit.audit_logger import (
    write_audit_log
)

from app.common.error_handler import (
    handle_error
)

from app.common.custom_exception import (
    MonitoringException
)


# =========================================================
# EXECUTE MONITORING WORKFLOW
# =========================================================

def execute_monitoring():

    """
    Execute SQL Monitoring Workflow.
    """

    try:

        write_audit_log(
            "MONITORING WORKFLOW STARTED"
        )

        print(
            "\nStarting SQL Monitoring Engine...\n"
        )

        monitoring_result = run_monitoring()

        if monitoring_result is None:

            raise MonitoringException(
                "Monitoring returned no results."
            )

        if not isinstance(
            monitoring_result,
            dict
        ):

            raise MonitoringException(
                "Invalid monitoring result format."
            )

        print(
            "\nSQL Monitoring Execution Completed.\n"
        )

        write_audit_log(
            "MONITORING WORKFLOW COMPLETED"
        )

        return monitoring_result

    except Exception as error:

        return handle_error(
            "MONITORING EXECUTOR",
            error
        )


# =========================================================
# TEST EXECUTION
# =========================================================

if __name__ == "__main__":

    result = execute_monitoring()

    print("\n========================================")
    print(" MONITORING RESULT ")
    print("========================================\n")

    print(result)