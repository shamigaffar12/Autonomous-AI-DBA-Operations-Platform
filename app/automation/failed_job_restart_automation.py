# =========================================================
# Failed Job Restart Automation
# Autonomous AI DBA Operations Platform
# =========================================================

from datetime import datetime

from app.approvals.approval_manager import (
    create_approval_request
)


# =========================================================
# REQUEST FAILED JOB RESTART APPROVAL
# =========================================================

def request_failed_job_restart_approval(
    failed_job_result
):
    """
    Create approval request for failed SQL Agent job restart.

    Important:
    This function does not restart SQL Agent jobs.
    It only creates approval requests.
    """

    print("\n========================================")
    print(" Failed Job Restart Approval Workflow ")
    print("========================================\n")

    failed_jobs = failed_job_result.get(
        "failed_jobs",
        []
    )

    if not failed_jobs:

        return {
            "overall_status": "NO_FAILED_JOBS",
            "automation_name": "FAILED_JOB_RESTART_APPROVAL",
            "message": "No failed SQL jobs found. No restart approval required.",
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

        approval_request = create_approval_request(
            action_name="RESTART_SQL_AGENT_JOB",
            target_name=job_name,
            risk_level="MEDIUM",
            requested_by="AI_AGENT",
            reason=(
                "SQL Server Agent job failed and requires Lead DBA approval "
                "before restart automation can be triggered."
            ),
            metadata={
                "source": "FAILED_JOB_RESTART_AUTOMATION",
                "job_name": job_name,
                "failed_job_details": job
            }
        )

        restart_request = {
            "approval_id": approval_request.get(
                "approval_id"
            ),
            "job_name": job_name,
            "action": "RESTART_SQL_AGENT_JOB",
            "approval_status": approval_request.get(
                "approval_status",
                "PENDING_APPROVAL"
            ),
            "risk": "MEDIUM",
            "created_at": approval_request.get(
                "created_at"
            )
        }

        restart_requests.append(
            restart_request
        )

        print(f"Job Name        : {job_name}")
        print("Action          : Restart SQL Agent Job")
        print("Approval Status : PENDING_APPROVAL")
        print("Risk            : MEDIUM")
        print(f"Approval ID     : {approval_request.get('approval_id')}")
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


# =========================================================
# TEST EXECUTION
# =========================================================

if __name__ == "__main__":

    sample_failed_job_result = {
        "overall_status": "ATTENTION REQUIRED",
        "failed_jobs": [
            {
                "job_name": "syspolicy_purge_history",
                "run_status": "FAILED",
                "message": "Job failed during last execution."
            }
        ]
    }

    result = request_failed_job_restart_approval(
        sample_failed_job_result
    )

    print("\n========================================")
    print(" FAILED JOB RESTART APPROVAL RESULT ")
    print("========================================\n")

    print(result)