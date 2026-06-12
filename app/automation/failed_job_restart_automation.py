# =========================================================
# Failed Job Restart Automation
# Autonomous AI DBA Operations Platform
# =========================================================

from datetime import datetime

from app.approvals.approval_manager import (
    create_approval_request
)


def request_failed_job_restart_approval(
    failed_job_result
):
    """
    Automatically create approval request when failed SQL job is detected.
    This does not restart the job directly.
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

            print("No failed jobs found. No approval required.")

            return {
                "overall_status": "NO_ACTION_REQUIRED",
                "automation_name": "FAILED_JOB_RESTART_APPROVAL",
                "message": "No failed SQL Agent jobs found.",
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
                "job_name",
                "UNKNOWN_JOB"
            )

            approval_result = create_approval_request(
                action_name="RESTART_SQL_AGENT_JOB",
                target_name=job_name,
                risk_level="MEDIUM",
                requested_by="DBA",
                reason=(
                    "AI Agent detected failed SQL Server Agent job. "
                    "Restart recommendation requires Lead DBA approval."
                ),
                metadata={
                    "source": "AI_AGENT_FAILED_JOB_RECOMMENDATION",
                    "job_details": job
                }
            )

            restart_request = {
                "approval_id": approval_result.get(
                    "approval_id"
                ),
                "job_name": job_name,
                "action": "RESTART_SQL_AGENT_JOB",
                "approval_status": "PENDING_APPROVAL",
                "risk": "MEDIUM",
                "created_at": str(
                    datetime.now()
                )
            }

            restart_requests.append(
                restart_request
            )

            print(f"Job Name        : {job_name}")
            print(f"Approval ID     : {restart_request['approval_id']}")
            print("Action          : RESTART_SQL_AGENT_JOB")
            print("Approval Status : PENDING_APPROVAL")
            print("Risk            : MEDIUM")
            print("----------------------------------------")

        return {
            "overall_status": "APPROVAL_REQUIRED",
            "automation_name": "FAILED_JOB_RESTART_APPROVAL",
            "message": "Approval request created automatically by AI Agent workflow.",
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

        print("\nFailed Job Restart Automation Error:")
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


if __name__ == "__main__":

    sample_failed_job_result = {
        "failed_jobs": [
            {
                "job_name": "syspolicy_purge_history",
                "run_status": "FAILED",
                "message": "Job failed during execution."
            }
        ]
    }

    result = request_failed_job_restart_approval(
        sample_failed_job_result
    )

    print(
        result
    )