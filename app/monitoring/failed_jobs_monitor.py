# =========================================================
# Failed SQL Jobs Monitor
# Autonomous AI DBA Operations Platform
# =========================================================

from datetime import datetime

from app.monitoring.sql_collector import (
    execute_monitoring_query,
    read_sql_file
)


# =========================================================
# CHECK FAILED SQL JOBS
# =========================================================

def check_failed_jobs():
    """
    Check failed SQL Server Agent jobs using approved SQL health query.
    """

    try:

        print("\n========================================")
        print(" Failed SQL Jobs Monitoring ")
        print("========================================\n")

        query = read_sql_file(
            "sql/health_queries/failed_jobs.sql"
        )

        if query is None:

            return {
                "overall_status": "ERROR",
                "check_name": "FAILED_JOBS",
                "message": "Failed jobs SQL file could not be loaded.",
                "failed_jobs": [],
                "checked_at": str(datetime.now())
            }

        failed_job_results = execute_monitoring_query(
            query
        )

        failed_jobs = []

        if failed_job_results:

            for row in failed_job_results:

                job_data = {
                    "job_name": row[0] if len(row) > 0 else None,
                    "run_date": row[1] if len(row) > 1 else None,
                    "run_time": row[2] if len(row) > 2 else None,
                    "run_status": row[3] if len(row) > 3 else None,
                    "message": row[4] if len(row) > 4 else None
                }

                failed_jobs.append(
                    job_data
                )

                print(f"Job Name   : {job_data['job_name']}")
                print(f"Run Date   : {job_data['run_date']}")
                print(f"Run Time   : {job_data['run_time']}")
                print(f"Status     : {job_data['run_status']}")
                print(f"Message    : {job_data['message']}")
                print("----------------------------------------")

            return {
                "overall_status": "ATTENTION REQUIRED",
                "check_name": "FAILED_JOBS",
                "message": "Failed SQL jobs detected.",
                "failed_jobs_count": len(failed_jobs),
                "failed_jobs": failed_jobs,
                "checked_at": str(datetime.now())
            }

        print("No failed SQL jobs detected.")

        return {
            "overall_status": "HEALTHY",
            "check_name": "FAILED_JOBS",
            "message": "No failed SQL jobs detected.",
            "failed_jobs_count": 0,
            "failed_jobs": [],
            "checked_at": str(datetime.now())
        }

    except Exception as error:

        print("\nFailed Jobs Monitoring Error:\n")
        print(error)

        return {
            "overall_status": "ERROR",
            "check_name": "FAILED_JOBS",
            "message": str(error),
            "failed_jobs_count": 0,
            "failed_jobs": [],
            "checked_at": str(datetime.now())
        }


# =========================================================
# TEST EXECUTION
# =========================================================

if __name__ == "__main__":

    result = check_failed_jobs()

    print("\n========================================")
    print(" FAILED JOBS MONITOR RESULT ")
    print("========================================\n")

    print(result)