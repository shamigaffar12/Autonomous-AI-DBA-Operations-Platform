# =========================================================
# Monitoring Executor
# Autonomous AI DBA Operations Platform
# =========================================================

import subprocess


# =========================================================
# EXECUTE MONITORING ENGINE
# =========================================================

def run_monitoring():

    """
    Execute SQL Monitoring Engine.
    """

    print("\nStarting SQL Monitoring Engine...\n")

    subprocess.run(

        [

            "python",

            "-m",

            "app.monitoring.sql_monitor"

        ]

    )

    print("\nSQL Monitoring Execution Completed.\n")