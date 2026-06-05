# =========================================================
# Scheduler Manager
# Autonomous AI DBA Operations Platform
# =========================================================

from app.common.config_manager import (
    SCHEDULER_ENABLED,
    SCHEDULER_INTERVAL_SECONDS
)


# =========================================================
# GET SCHEDULER INTERVAL
# =========================================================

def get_scheduler_interval():

    """
    Return scheduler interval.
    """

    return SCHEDULER_INTERVAL_SECONDS


# =========================================================
# DISPLAY SCHEDULER CONFIGURATION
# =========================================================

def display_scheduler_config():

    """
    Display scheduler configuration.
    """

    print("\n========================================")

    print(" SCHEDULER CONFIGURATION ")

    print("========================================\n")

    print(
        f"Scheduler Enabled : {SCHEDULER_ENABLED}"
    )

    print(
        f"Execution Interval : "
        f"{SCHEDULER_INTERVAL_SECONDS} Seconds"
    )


# =========================================================
# GET SCHEDULER STATUS
# =========================================================

def get_scheduler_status():

    """
    Return scheduler status.
    """

    return {

        "status": (
            "ACTIVE"
            if SCHEDULER_ENABLED
            else "DISABLED"
        ),

        "interval_seconds":
        SCHEDULER_INTERVAL_SECONDS

    }


# =========================================================
# TEST EXECUTION
# =========================================================

if __name__ == "__main__":

    display_scheduler_config()

    print("\nScheduler Status:\n")

    print(
        get_scheduler_status()
    )