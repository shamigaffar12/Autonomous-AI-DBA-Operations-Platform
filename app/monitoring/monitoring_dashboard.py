# =========================================================
# Monitoring Dashboard Data Adapter
# =========================================================

from datetime import datetime

from app.monitoring.sql_monitor import (
    run_monitoring
)


def get_monitoring_dashboard_data():

    monitoring = run_monitoring()

    cpu_count = len(
        monitoring["cpu_results"]
    ) if monitoring["cpu_results"] else 0

    blocking_count = len(
        monitoring["blocking_results"]
    ) if monitoring["blocking_results"] else 0

    long_query_count = len(
        monitoring["long_results"]
    ) if monitoring["long_results"] else 0

    return {

        "overall_status":
        monitoring["overall_status"],

        "cpu_sessions":
        cpu_count,

        "blocking_sessions":
        blocking_count,

        "long_queries":
        long_query_count,

        "last_check":
        datetime.now().strftime(
            "%d-%b-%Y %H:%M:%S"
        ),

        "incident_summary":
        monitoring["incident_summary"]

    }