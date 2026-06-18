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
# LOAD REPORT FILES
# =========================================================

def load_report_files():
    """
    Load generated report files.
    """

    reports = []
    report_folder = "reports"

    try:
        if os.path.exists(
            report_folder
        ):
            reports = os.listdir(
                report_folder
            )

    except Exception:
        reports = []

    return reports


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

    reports = load_report_files()

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

    # =====================================================
    # DATABASE HEALTH
    # =====================================================

    if intent == "DATABASE_HEALTH":

        return {
            "assistant_response": "The platform is operational. Monitoring, governance, audit tracking, reporting, NLP assistant, and simulated automation are active.",
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
            "recommended_next_action": "Open the Dashboard or Monitoring page for detailed platform health status.",
            "risk_level": risk_level
        }

    # =====================================================
    # DEADLOCK ANALYSIS
    # =====================================================

    if intent == "DEADLOCK_ANALYSIS":

        return {
            "assistant_response": "Deadlock analysis request identified. The platform can review blocking and deadlock-related symptoms, generate RCA, and recommend safe DBA actions.",
            "summary": {
                "analysis_type": "Deadlock Analysis",
                "risk_level": "Medium",
                "recommended_checks": [
                    "blocking sessions",
                    "long running queries",
                    "deadlock graph review",
                    "transaction isolation review",
                    "index and query pattern review"
                ],
                "automation_mode": "Simulated"
            },
            "recommended_next_action": "Review the workflow execution result. Deadlock analysis is currently prepared in simulated mode and can be connected with real SQL deadlock monitoring queries in the next phase.",
            "risk_level": risk_level
        }

    # =====================================================
    # FAILED JOB CHECK
    # =====================================================

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

    # =====================================================
    # BACKUP STATUS
    # =====================================================

    if intent == "BACKUP_STATUS":

        return {
            "assistant_response": "Backup status monitoring request identified. The assistant can help review backup health, backup age, and backup-related risk.",
            "summary": {
                "backup_monitoring": "Available",
                "supported_backup_checks": [
                    "last full backup",
                    "last differential backup",
                    "last log backup",
                    "backup age",
                    "backup failure risk"
                ],
                "automation_mode": "Simulated",
                "audit_events": len(
                    governance_audit_logs
                )
            },
            "recommended_next_action": "Review the workflow execution result. Backup status routing is prepared and can be connected with real SQL backup monitoring queries.",
            "risk_level": risk_level
        }

    # =====================================================
    # BACKUP REQUEST
    # =====================================================

    if intent == "BACKUP_REQUEST":

        return {
            "assistant_response": "Backup request identified. A database backup is an operational DBA action and should be handled through a governed workflow.",
            "summary": {
                "requested_action": "Database Backup",
                "backup_type": "Not specified",
                "approval_required": "Recommended",
                "execution_mode": "Simulated",
                "pending_approvals": len(
                    pending_approvals
                )
            },
            "recommended_next_action": "Specify backup type such as full backup, differential backup, or log backup before creating a governed backup request.",
            "risk_level": risk_level
        }

    # =====================================================
    # FULL BACKUP REQUEST
    # =====================================================

    if intent == "FULL_BACKUP_REQUEST":

        return {
            "assistant_response": "Full backup request identified. This request has been routed through the governed backup workflow in controlled mode.",
            "summary": {
                "requested_action": "Database Backup",
                "backup_type": "Full Backup",
                "approval_required": "Recommended",
                "execution_mode": "Simulated",
                "pending_approvals": len(
                    pending_approvals
                )
            },
            "recommended_next_action": "Review the workflow result. Use 'create approval for full backup' to create a pending Governance approval request.",
            "risk_level": risk_level
        }

    # =====================================================
    # DIFFERENTIAL BACKUP REQUEST
    # =====================================================

    if intent == "DIFFERENTIAL_BACKUP_REQUEST":

        return {
            "assistant_response": "Differential backup request identified. This backup depends on the latest full backup and should be validated before execution.",
            "summary": {
                "requested_action": "Database Backup",
                "backup_type": "Differential Backup",
                "approval_required": "Recommended",
                "execution_mode": "Simulated",
                "pending_approvals": len(
                    pending_approvals
                )
            },
            "recommended_next_action": "Validate latest full backup availability before creating a governed differential backup request.",
            "risk_level": risk_level
        }

    # =====================================================
    # LOG BACKUP REQUEST
    # =====================================================

    if intent == "LOG_BACKUP_REQUEST":

        return {
            "assistant_response": "Transaction log backup request identified. Log backup execution should be validated based on database recovery model and backup chain.",
            "summary": {
                "requested_action": "Database Backup",
                "backup_type": "Transaction Log Backup",
                "approval_required": "Recommended",
                "execution_mode": "Simulated",
                "pending_approvals": len(
                    pending_approvals
                )
            },
            "recommended_next_action": "Validate database recovery model and backup chain before creating a governed log backup request.",
            "risk_level": risk_level
        }

    # =====================================================
    # START MONITORING
    # =====================================================

    if intent == "START_MONITORING":

        return {
            "assistant_response": "Monitoring start command identified. The request has been routed through the NLP workflow router in controlled mode.",
            "summary": {
                "workflow": "Monitoring Workflow",
                "checks": [
                    "CPU health",
                    "blocking sessions",
                    "long running queries",
                    "failed SQL jobs",
                    "backup status",
                    "database space"
                ],
                "execution_mode": "Simulated",
                "risk_level": "Low"
            },
            "recommended_next_action": "Review the workflow execution result. The next enhancement is to connect this route directly with the monitoring executor.",
            "risk_level": risk_level
        }

    # =====================================================
    # STOP MONITORING
    # =====================================================

    if intent == "STOP_MONITORING":

        return {
            "assistant_response": "Stop monitoring command identified. In the current phase, monitoring stop is treated as a controlled simulated platform operation.",
            "summary": {
                "workflow": "Monitoring Control",
                "requested_action": "Stop Monitoring",
                "execution_mode": "Simulated",
                "risk_level": "Low"
            },
            "recommended_next_action": "Add monitoring state control before enabling stop monitoring from NLP.",
            "risk_level": risk_level
        }

    # =====================================================
    # RUN DAILY HEALTH CHECK
    # =====================================================

    if intent == "RUN_HEALTH_CHECK":

        return {
            "assistant_response": "Daily health check command identified. The platform can run core health checks and prepare a DBA health summary.",
            "summary": {
                "workflow": "Daily DBA Health Check",
                "planned_checks": [
                    "CPU health",
                    "blocking sessions",
                    "long running queries",
                    "failed jobs",
                    "backup status",
                    "database space",
                    "health report"
                ],
                "execution_mode": "Simulated"
            },
            "recommended_next_action": "Review the workflow execution result. The next enhancement is to connect this command with monthly report generation.",
            "risk_level": risk_level
        }

    # =====================================================
    # RUN FULL DBA WORKFLOW
    # =====================================================

    if intent == "RUN_FULL_DBA_WORKFLOW":

        return {
            "assistant_response": "Full DBA workflow command identified. The request has been routed through the NLP workflow router and executed through the MCP workflow manager.",
            "summary": {
                "workflow": "Full DBA Workflow",
                "planned_steps": [
                    "environment validation",
                    "monitoring",
                    "AI analysis",
                    "RCA generation",
                    "risk classification",
                    "recommendation generation",
                    "governance review",
                    "reporting",
                    "audit logging"
                ],
                "execution_mode": "MCP Workflow"
            },
            "recommended_next_action": "Review the workflow execution result, generated report, audit logs, and governance status.",
            "risk_level": risk_level
        }

    # =====================================================
    # APPROVAL STATUS
    # =====================================================

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

    # =====================================================
    # CREATE APPROVAL REQUEST
    # =====================================================

    if intent == "CREATE_APPROVAL_REQUEST":

        return {
            "assistant_response": "Approval request creation command identified. The request has been routed through the NLP workflow router and created in the Governance approval queue.",
            "summary": {
                "workflow": "Approval Request Creation",
                "approval_required": True,
                "pending_approvals": len(
                    pending_approvals
                ),
                "supported_actions": [
                    "restart SQL Agent job",
                    "backup execution",
                    "remediation execution"
                ]
            },
            "recommended_next_action": "Open the Governance page to review, approve, or reject the newly created approval request.",
            "risk_level": risk_level
        }

    # =====================================================
    # AUDIT LOGS
    # =====================================================

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

    # =====================================================
    # EXECUTION HISTORY
    # =====================================================

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

    # =====================================================
    # EXECUTE APPROVED REMEDIATION
    # =====================================================

    if intent == "EXECUTE_APPROVED_REMEDIATION":

        return {
            "assistant_response": "Approved remediation execution command identified. The assistant must verify approval status before executing any automation.",
            "summary": {
                "workflow": "Approved Remediation Execution",
                "approval_validation_required": True,
                "execution_mode": "Simulated",
                "execution_records": len(
                    execution_history
                )
            },
            "recommended_next_action": "Connect this intent to the execution console so only approved requests can be executed.",
            "risk_level": risk_level
        }

    # =====================================================
    # REPORT STATUS
    # =====================================================

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

    # =====================================================
    # REMEDIATION REQUEST
    # =====================================================

    if intent == "REMEDIATION_REQUEST":

        return {
            "assistant_response": "This is a governed remediation request. The assistant cannot directly execute SQL Agent job restart or other remediation without approval.",
            "summary": {
                "pending_approvals": len(
                    pending_approvals
                ),
                "approved_requests": approved_count,
                "approval_required": True
            },
            "recommended_next_action": "Create or review an approval request in the Governance page before executing remediation.",
            "risk_level": risk_level
        }

    # =====================================================
    # GENERAL DBA QUERY
    # =====================================================

    return {
        "assistant_response": "I understood this as a general DBA query. Currently I can help with health status, failed jobs, approvals, audit logs, execution history, reports, backup, deadlock, and monitoring-related commands.",
        "summary": {
            "supported_topics": [
                "database health",
                "failed jobs",
                "approval status",
                "audit logs",
                "execution history",
                "reports",
                "backup",
                "deadlock",
                "monitoring",
                "daily health workflow",
                "full DBA workflow",
                "approval creation"
            ]
        },
        "recommended_next_action": "Ask a DBA operations question such as 'run full dba workflow', 'start monitoring', 'check deadlock situation', or 'create approval for full backup'.",
        "risk_level": risk_level
    }