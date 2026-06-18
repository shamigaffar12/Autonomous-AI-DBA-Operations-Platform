# =========================================================
# NLP Workflow Router
# Autonomous AI DBA Operations Platform
# =========================================================

from datetime import datetime


# =========================================================
# ROUTE NLP INTENT TO PLATFORM WORKFLOW
# =========================================================

def route_nlp_workflow(
    user_query,
    intent,
    risk_level
):
    """
    Route NLP DBA intent to controlled platform workflow.

    This router connects natural language commands with
    existing MCP workflow and governance capabilities.
    """

    # =====================================================
    # START MONITORING
    # =====================================================

    if intent == "START_MONITORING":

        return build_workflow_result(
            user_query=user_query,
            intent=intent,
            workflow_name="SQL Monitoring Workflow",
            workflow_status="SIMULATED_EXECUTION_COMPLETED",
            risk_level=risk_level,
            execution_mode="SIMULATED",
            executed_steps=[
                "CPU health check prepared",
                "Blocking session check prepared",
                "Long running query check prepared",
                "Failed SQL job check prepared",
                "Backup status check prepared",
                "Database space check prepared"
            ],
            message="Monitoring workflow routed successfully in simulated mode.",
            next_action="Next enhancement: connect this route directly with the existing monitoring executor."
        )

    # =====================================================
    # STOP MONITORING
    # =====================================================

    if intent == "STOP_MONITORING":

        return build_workflow_result(
            user_query=user_query,
            intent=intent,
            workflow_name="SQL Monitoring Control Workflow",
            workflow_status="SIMULATED_STOP_PREPARED",
            risk_level=risk_level,
            execution_mode="SIMULATED",
            executed_steps=[
                "Stop monitoring command received",
                "Monitoring control request prepared",
                "No live scheduler stop executed in current phase"
            ],
            message="Stop monitoring workflow prepared in simulated mode.",
            next_action="Next enhancement: connect this route with scheduler or monitoring state control."
        )

    # =====================================================
    # RUN DAILY HEALTH CHECK
    # =====================================================

    if intent == "RUN_HEALTH_CHECK":

        return build_workflow_result(
            user_query=user_query,
            intent=intent,
            workflow_name="Daily DBA Health Check Workflow",
            workflow_status="SIMULATED_EXECUTION_COMPLETED",
            risk_level=risk_level,
            execution_mode="SIMULATED",
            executed_steps=[
                "Environment validation prepared",
                "CPU health check prepared",
                "Blocking session check prepared",
                "Long running query check prepared",
                "Failed SQL job check prepared",
                "Backup status check prepared",
                "Database space check prepared",
                "Health report generation prepared"
            ],
            message="Daily DBA health check workflow routed successfully in simulated mode.",
            next_action="Next enhancement: connect this command with MCP workflow execution or monthly report generation."
        )

    # =====================================================
    # RUN FULL DBA WORKFLOW
    # =====================================================

    if intent == "RUN_FULL_DBA_WORKFLOW":

        return run_existing_mcp_workflow(
            user_query=user_query,
            intent=intent,
            risk_level=risk_level
        )

    # =====================================================
    # DEADLOCK ANALYSIS
    # =====================================================

    if intent == "DEADLOCK_ANALYSIS":

        return build_workflow_result(
            user_query=user_query,
            intent=intent,
            workflow_name="Deadlock Analysis Workflow",
            workflow_status="SIMULATED_ANALYSIS_PREPARED",
            risk_level=risk_level,
            execution_mode="SIMULATED",
            executed_steps=[
                "Blocking session review prepared",
                "Deadlock symptom check prepared",
                "Long running transaction review prepared",
                "Query pattern review prepared",
                "RCA generation prepared"
            ],
            message="Deadlock analysis workflow prepared in simulated mode.",
            next_action="Next enhancement: add real deadlock monitoring query and connect it with RCA engine."
        )

    # =====================================================
    # BACKUP STATUS
    # =====================================================

    if intent == "BACKUP_STATUS":

        return build_workflow_result(
            user_query=user_query,
            intent=intent,
            workflow_name="Backup Status Monitoring Workflow",
            workflow_status="SIMULATED_CHECK_PREPARED",
            risk_level=risk_level,
            execution_mode="SIMULATED",
            executed_steps=[
                "Last full backup check prepared",
                "Last differential backup check prepared",
                "Last log backup check prepared",
                "Backup age validation prepared",
                "Backup health summary prepared"
            ],
            message="Backup status workflow prepared in simulated mode.",
            next_action="Next enhancement: connect this command with the real backup status SQL monitoring query."
        )

    # =====================================================
    # BACKUP REQUESTS
    # =====================================================

    if intent in [
        "BACKUP_REQUEST",
        "FULL_BACKUP_REQUEST",
        "DIFFERENTIAL_BACKUP_REQUEST",
        "LOG_BACKUP_REQUEST"
    ]:

        backup_type = get_backup_type(
            intent
        )

        return build_workflow_result(
            user_query=user_query,
            intent=intent,
            workflow_name="Governed Backup Workflow",
            workflow_status="APPROVAL_REQUIRED",
            risk_level=risk_level,
            execution_mode="SIMULATED",
            executed_steps=[
                "Backup request identified",
                f"Backup type detected: {backup_type}",
                "Approval requirement evaluated",
                "Audit tracking prepared",
                "Execution blocked until approval"
            ],
            message="Backup execution is a governed DBA operation and requires approval before execution.",
            next_action="Use 'create approval for full backup' to create a pending approval request."
        )

    # =====================================================
    # CREATE APPROVAL REQUEST
    # =====================================================

    if intent == "CREATE_APPROVAL_REQUEST":

        return create_nlp_approval_request(
            user_query=user_query,
            intent=intent,
            risk_level=risk_level
        )

    # =====================================================
    # EXECUTE APPROVED REMEDIATION
    # =====================================================

    if intent == "EXECUTE_APPROVED_REMEDIATION":

        return build_workflow_result(
            user_query=user_query,
            intent=intent,
            workflow_name="Approved Remediation Execution Workflow",
            workflow_status="APPROVAL_VALIDATION_REQUIRED",
            risk_level=risk_level,
            execution_mode="SIMULATED",
            executed_steps=[
                "Execution request identified",
                "Approval validation required",
                "Execution history target identified",
                "Governance audit target identified"
            ],
            message="Approved remediation execution requires approval ID validation before automation trigger.",
            next_action="Next enhancement: connect this route with approval execution console."
        )

    # =====================================================
    # DEFAULT ROUTE
    # =====================================================

    return build_workflow_result(
        user_query=user_query,
        intent=intent,
        workflow_name="No Workflow Route",
        workflow_status="NO_WORKFLOW_EXECUTED",
        risk_level=risk_level,
        execution_mode="SIMULATED",
        executed_steps=[],
        message="No workflow routing is configured for this intent.",
        next_action="Use supported commands such as start monitoring, run health check, run full DBA workflow, check deadlock situation, take full backup, or create approval for full backup."
    )


# =========================================================
# RUN EXISTING MCP WORKFLOW
# =========================================================

def run_existing_mcp_workflow(
    user_query,
    intent,
    risk_level
):
    """
    Run existing MCP workflow manager safely.

    This uses:
    app/mcp_server/workflow_manager.py
    """

    try:

        from app.mcp_server.workflow_manager import (
            execute_workflow,
            get_workflow_steps
        )

        workflow_steps = get_workflow_steps()

        workflow_result = execute_workflow()

        return {
            "workflow_id": f"NLP-WF-{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
            "user_query": user_query,
            "intent": intent,
            "workflow_name": "Full MCP DBA Workflow",
            "workflow_status": workflow_result.get(
                "status",
                "UNKNOWN"
            ),
            "risk_level": risk_level,
            "execution_mode": "MCP_WORKFLOW",
            "executed_steps": workflow_steps,
            "message": "Full MCP workflow executed through NLP workflow router.",
            "next_action": "Review workflow output, report file, audit logs, and governance result.",
            "mcp_result": workflow_result,
            "created_at": str(
                datetime.now()
            )
        }

    except Exception as error:

        return {
            "workflow_id": f"NLP-WF-{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
            "user_query": user_query,
            "intent": intent,
            "workflow_name": "Full MCP DBA Workflow",
            "workflow_status": "FAILED",
            "risk_level": risk_level,
            "execution_mode": "MCP_WORKFLOW",
            "executed_steps": [],
            "message": "Failed to execute MCP workflow from NLP router.",
            "next_action": "Check MCP workflow manager error and validate imports/configuration.",
            "error": str(
                error
            ),
            "created_at": str(
                datetime.now()
            )
        }


# =========================================================
# CREATE NLP APPROVAL REQUEST
# =========================================================

def create_nlp_approval_request(
    user_query,
    intent,
    risk_level
):
    """
    Create approval request from NLP command.
    """

    try:

        from app.nlp_assistant.approval_command_parser import (
            parse_approval_command
        )

        from app.approvals.approval_manager import (
            create_approval_request
        )

        from app.automation.governance_audit_manager import (
            add_governance_audit_log
        )

        approval_payload = parse_approval_command(
            user_query
        )

        approval_result = create_approval_request(
            action_name=approval_payload.get(
                "action_name"
            ),
            target_name=approval_payload.get(
                "target_name"
            ),
            risk_level=approval_payload.get(
                "risk_level"
            ),
            requested_by="NLP DBA Assistant",
            reason=approval_payload.get(
                "reason"
            ),
            metadata=approval_payload.get(
                "metadata"
            )
        )

        approval_id = approval_result.get(
            "approval_id"
        )

        if approval_result.get(
            "approval_status"
        ) == "PENDING_APPROVAL":

            add_governance_audit_log(
                event_type="NLP_APPROVAL_REQUEST_CREATED",
                approval_id=approval_id,
                action_name=approval_payload.get(
                    "action_name"
                ),
                target_name=approval_payload.get(
                    "target_name"
                ),
                status="PENDING_APPROVAL",
                performed_by="NLP DBA Assistant",
                message="Approval request created from NLP DBA Assistant."
            )

            return {
                "workflow_id": f"NLP-WF-{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
                "user_query": user_query,
                "intent": intent,
                "workflow_name": "NLP Approval Request Workflow",
                "workflow_status": "PENDING_APPROVAL",
                "risk_level": approval_payload.get(
                    "risk_level"
                ),
                "execution_mode": "GOVERNANCE",
                "executed_steps": [
                    "User command parsed",
                    "Approval action identified",
                    "Approval request payload created",
                    "Pending approval saved",
                    "Governance audit log created"
                ],
                "message": "Approval request created successfully from NLP command.",
                "next_action": "Open the Governance page and approve or reject the request.",
                "approval_result": approval_result,
                "created_at": str(
                    datetime.now()
                )
            }

        return {
            "workflow_id": f"NLP-WF-{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
            "user_query": user_query,
            "intent": intent,
            "workflow_name": "NLP Approval Request Workflow",
            "workflow_status": "FAILED",
            "risk_level": risk_level,
            "execution_mode": "GOVERNANCE",
            "executed_steps": [
                "User command parsed",
                "Approval creation attempted"
            ],
            "message": "Approval request creation failed.",
            "next_action": "Check approval manager and pending approval storage.",
            "approval_result": approval_result,
            "created_at": str(
                datetime.now()
            )
        }

    except Exception as error:

        return {
            "workflow_id": f"NLP-WF-{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
            "user_query": user_query,
            "intent": intent,
            "workflow_name": "NLP Approval Request Workflow",
            "workflow_status": "FAILED",
            "risk_level": risk_level,
            "execution_mode": "GOVERNANCE",
            "executed_steps": [],
            "message": "Failed to create approval request from NLP command.",
            "next_action": "Check NLP approval parser, approval manager, and governance audit manager.",
            "error": str(
                error
            ),
            "created_at": str(
                datetime.now()
            )
        }


# =========================================================
# BUILD WORKFLOW RESULT
# =========================================================

def build_workflow_result(
    user_query,
    intent,
    workflow_name,
    workflow_status,
    risk_level,
    execution_mode,
    executed_steps,
    message,
    next_action
):
    """
    Build standard workflow routing result.
    """

    return {
        "workflow_id": f"NLP-WF-{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
        "user_query": user_query,
        "intent": intent,
        "workflow_name": workflow_name,
        "workflow_status": workflow_status,
        "risk_level": risk_level,
        "execution_mode": execution_mode,
        "executed_steps": executed_steps,
        "message": message,
        "next_action": next_action,
        "created_at": str(
            datetime.now()
        )
    }


# =========================================================
# BACKUP TYPE HELPER
# =========================================================

def get_backup_type(
    intent
):
    """
    Return backup type from intent.
    """

    if intent == "FULL_BACKUP_REQUEST":

        return "Full Backup"

    if intent == "DIFFERENTIAL_BACKUP_REQUEST":

        return "Differential Backup"

    if intent == "LOG_BACKUP_REQUEST":

        return "Transaction Log Backup"

    return "Not specified"