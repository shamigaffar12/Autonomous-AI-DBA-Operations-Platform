# =========================================================
# NLP Response Engine
# Autonomous AI DBA Operations Platform
# =========================================================

import os
import json


# =========================================================
# SAFE JSON LOADER
# =========================================================

def load_json_file(
    file_path,
    default_value=None
):
    """
    Safely load JSON file.
    """

    if default_value is None:

        default_value = []

    try:

        if not os.path.exists(
            file_path
        ):

            return default_value

        with open(
            file_path,
            "r"
        ) as file:

            return json.load(
                file
            )

    except Exception:

        return default_value


# =========================================================
# BUILD RESPONSE FOR INTENT
# =========================================================

def build_nlp_response(
    user_query,
    intent_result
):
    """
    Build DBA assistant response based on classified intent.
    """

    intent = intent_result.get(
        "intent"
    )

    risk_level = intent_result.get(
        "risk_level"
    )

    pending_approvals = load_json_file(
        "approval_requests/pending_approvals.json",
        []
    )

    approval_history = load_json_file(
        "approval_requests/approval_history.json",
        []
    )

    execution_history = load_json_file(
        "approval_requests/execution_history.json",
        []
    )

    governance_audit_logs = load_json_file(
        "approval_requests/governance_audit_log.json",
        []
    )

    incidents = load_json_file(
        "incidents.json",
        []
    )

    reports = []

    if os.path.exists(
        "reports"
    ):

        reports = os.listdir(
            "reports"
        )

    approved_count = 0
    rejected_count = 0

    for approval in approval_history:

        if approval.get(
            "approval_status"
        ) == "APPROVED":

            approved_count = approved_count + 1

        elif approval.get(
            "approval_status"
        ) == "REJECTED":

            rejected_count = rejected_count + 1

    if intent == "DATABASE_HEALTH":

        return {
            "assistant_response": "The platform is operational. Monitoring, governance, audit tracking, reporting, and simulated automation are active.",
            "summary": {
                "incidents": len(
                    incidents
                ),
                "pending_approvals": len(
                    pending_approvals
                ),
                "approved_requests": approved_count,
                "rejected_requests": rejected_count,
                "execution_records": len(
                    execution_history
                ),
                "audit_events": len(
                    governance_audit_logs
                )
            },
            "recommended_next_action": "Open the Dashboard or Monitoring page for detailed health status.",
            "risk_level": risk_level
        }

    if intent == "FAILED_JOB_CHECK":

        return {
            "assistant_response": "Failed SQL Agent job monitoring is connected with the approval workflow. Any restart action requires approval before automation execution.",
            "summary": {
                "pending_approvals": len(
                    pending_approvals
                ),
                "approval_history": len(
                    approval_history
                )
            },
            "recommended_next_action": "Open the Governance page and review pending failed job restart approvals.",
            "risk_level": risk_level
        }

    if intent == "APPROVAL_STATUS":

        return {
            "assistant_response": "Approval workflow is active and tracking pending, approved, and rejected requests.",
            "summary": {
                "pending_approvals": len(
                    pending_approvals
                ),
                "approved_requests": approved_count,
                "rejected_requests": rejected_count,
                "total_requests": len(
                    pending_approvals
                ) + len(
                    approval_history
                )
            },
            "recommended_next_action": "Open the Governance page to approve, reject, or execute approved requests.",
            "risk_level": risk_level
        }

    if intent == "AUDIT_LOGS":

        return {
            "assistant_response": "Governance audit logging is active. Approval and remediation execution events are being recorded.",
            "summary": {
                "audit_events": len(
                    governance_audit_logs
                )
            },
            "recommended_next_action": "Open the Audit Logs page to review approval and remediation events.",
            "risk_level": risk_level
        }

    if intent == "EXECUTION_HISTORY":

        latest_execution = None

        if execution_history:

            latest_execution = execution_history[
                -1
            ]

        return {
            "assistant_response": "Remediation execution history is available. Approved remediation actions are tracked after execution.",
            "summary": {
                "execution_records": len(
                    execution_history
                ),
                "latest_execution": latest_execution
            },
            "recommended_next_action": "Open the Governance page and review Remediation Execution History.",
            "risk_level": risk_level
        }

    if intent == "REPORT_STATUS":

        return {
            "assistant_response": "Reporting module is available. Generated reports are tracked from the reports folder.",
            "summary": {
                "available_reports": len(
                    reports
                ),
                "reports": reports
            },
            "recommended_next_action": "Open the Reports page to review available reports.",
            "risk_level": risk_level
        }

    if intent == "REMEDIATION_REQUEST":

        return {
            "assistant_response": "This is a governed remediation request. The assistant cannot directly restart SQL Agent jobs without approval.",
            "summary": {
                "pending_approvals": len(
                    pending_approvals
                ),
                "approved_requests": approved_count
            },
            "recommended_next_action": "Create or review an approval request in the Governance page before executing remediation.",
            "risk_level": risk_level
        }

    return {
        "assistant_response": "I understood this as a general DBA query. Currently I can help with health status, failed jobs, approvals, audit logs, execution history, and reports.",
        "summary": {
            "supported_topics": [
                "database health",
                "failed jobs",
                "approval status",
                "audit logs",
                "execution history",
                "reports"
            ]
        },
        "recommended_next_action": "Ask a DBA operations question such as 'show pending approvals' or 'check failed SQL jobs'.",
        "risk_level": risk_level
    }