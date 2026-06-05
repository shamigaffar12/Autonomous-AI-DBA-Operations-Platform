# =========================================================
# Workflow Scheduler
# Autonomous AI DBA Operations Platform
# =========================================================

import time

from app.mcp_server.workflow_manager import (
    execute_workflow
)

from app.audit.audit_logger import (
    write_audit_log
)

from app.common.error_handler import (
    handle_error
)

from app.scheduler.scheduler_manager import (
    get_scheduler_interval
)

from app.common.config_manager import (
    SCHEDULER_ENABLED
)


# =========================================================
# START SCHEDULER
# =========================================================

def start_scheduler():

    """
    Execute workflow continuously
    based on configured interval.
    """

    try:

        # =================================================
        # SCHEDULER ENABLED CHECK
        # =================================================

        if not SCHEDULER_ENABLED:

            print(
                "\nScheduler is disabled."
            )

            write_audit_log(
                "SCHEDULER DISABLED"
            )

            return

        # =================================================
        # SCHEDULER START
        # =================================================

        print("\n========================================")

        print(" WORKFLOW SCHEDULER STARTED ")

        print("========================================\n")

        write_audit_log(
            "SCHEDULER STARTED"
        )

        # =================================================
        # EXECUTION LOOP
        # =================================================

        while True:

            scheduler_interval = (
                get_scheduler_interval()
            )

            write_audit_log(
                "SCHEDULED WORKFLOW EXECUTION STARTED"
            )

            execute_workflow()

            write_audit_log(
                "SCHEDULED WORKFLOW EXECUTION COMPLETED"
            )

            print(
                f"\nNext execution in "
                f"{scheduler_interval} seconds...\n"
            )

            time.sleep(
                scheduler_interval
            )

    except KeyboardInterrupt:

        write_audit_log(
            "SCHEDULER STOPPED BY USER"
        )

        print(
            "\nScheduler stopped manually."
        )

    except Exception as error:

        handle_error(
            "WORKFLOW SCHEDULER",
            error
        )


# =========================================================
# TEST EXECUTION
# =========================================================

if __name__ == "__main__":

    start_scheduler()