# =========================================================
# Dashboard Manager
# Autonomous AI DBA Operations Platform
# =========================================================

from app.dashboard.dashboard_data import (
    get_dashboard_metrics
)


# =========================================================
# DISPLAY DASHBOARD
# =========================================================

def display_dashboard():

    """
    Display operational dashboard.
    """

    metrics = get_dashboard_metrics()

    print("\n========================================")

    print(" DBA OPERATIONS DASHBOARD ")

    print("========================================\n")

    print(
        f"Platform Health      : "
        f"{metrics['platform_health']}"
    )

    print(
        f"Total Incidents      : "
        f"{metrics['total_incidents']}"
    )

    print(
        f"Healthy Incidents    : "
        f"{metrics['healthy_incidents']}"
    )

    print(
        f"Attention Required   : "
        f"{metrics['attention_required']}"
    )

    print(
        f"Latest Status        : "
        f"{metrics['latest_status']}"
    )

    print(
        f"Latest Report        : "
        f"{metrics['latest_report']}"
    )


# =========================================================
# TEST EXECUTION
# =========================================================

if __name__ == "__main__":

    display_dashboard()