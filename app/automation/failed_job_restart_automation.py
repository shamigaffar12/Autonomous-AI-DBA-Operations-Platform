# =========================================================
# Failed Job Restart Automation
# Autonomous AI DBA Operations Platform
# =========================================================

from datetime import datetime


# =========================================================
# REQUEST FAILED JOB RESTART APPROVAL
# =========================================================

def request_failed_job_restart_approval(
    failed_job_result
):
    """
    Prepare approval-controlled restart recommendation
    for failed SQL Server Agent jobs.

    This module does not restart jobs directly.
    It creates an approval request for DBA review.
    """

    try:

        print("\n========================================")
        print(" Failed Job Restart Approval Workflow ")
        print("========================================\n")

        failed_jobs = failed_job_result.get(
            "failed_jobs",
            []
        )

        if not failed_jobs:

            print(
                "No failed jobs found for restart approval."
            )

            return {
                "overall_status": "NO_ACTION_REQUIRED",
                "automation_name": "FAILED_JOB_RESTART_APPROVAL",
                "message": "No failed jobs found for restart approval.",
                "approval_required": False,
                "restart_request_count": 0,
                "restart_requests": [],
                "created_at": str(
                    datetime.now()
                )
            }

        restart_requests = []

        for job in failed_jobs:

            job_name = job.get(
                "job_name"
            )

            restart_request = {
                "job_name": job_name,
                "action": "RESTART_SQL_AGENT_JOB",
                "approval_status": "PENDING_APPROVAL",
                "risk": "MEDIUM",
                "reason": (
                    "SQL Server Agent job failed and requires "
                    "DBA approval before restart."
                ),
                "created_at": str(
                    datetime.now()
                )
            }

            restart_requests.append(
                restart_request
            )

            print(f"Job Name        : {job_name}")
            print("Action          : Restart SQL Agent Job")
            print("Approval Status : PENDING_APPROVAL")
            print("Risk            : MEDIUM")
            print("----------------------------------------")

        return {
            "overall_status": "APPROVAL_REQUIRED",
            "automation_name": "FAILED_JOB_RESTART_APPROVAL",
            "message": "Failed job restart approval request created.",
            "approval_required": True,
            "restart_request_count": len(
                restart_requests
            ),
            "restart_requests": restart_requests,
            "created_at": str(
                datetime.now()
            )
        }

    except Exception as error:

        print("\nFailed Job Restart Automation Error:\n")
        print(error)

        return {
            "overall_status": "ERROR",
            "automation_name": "FAILED_JOB_RESTART_APPROVAL",
            "message": str(
                error
            ),
            "approval_required": True,
            "restart_request_count": 0,
            "restart_requests": [],
            "created_at": str(
                datetime.now()
            )
        }


# =========================================================
# TEST EXECUTION
# =========================================================

if __name__ == "__main__":

    sample_failed_job_result = {
        "overall_status": "ATTENTION REQUIRED",
        "check_name": "FAILED_JOBS",
        "message": "Failed SQL jobs detected.",
        "failed_jobs_count": 1,
        "failed_jobs": [
            {
                "job_name": "syspolicy_purge_history",
                "run_date": "2026-06-11",
                "run_time": "14:30:00",
                "run_status": "FAILED",
                "message": "Job execution failed."
            }
        ]
    }

    result = request_failed_job_restart_approval(
        sample_failed_job_result
    )

    print("\n========================================")
    print(" FAILED JOB RESTART APPROVAL RESULT ")
    print("========================================\n")

    print(
        result
    )