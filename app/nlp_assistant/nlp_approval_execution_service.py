# =========================================================
# NLP Approval Execution Service
# Autonomous AI DBA Operations Platform
# =========================================================

import json
import os
import re
from datetime import datetime
from typing import Any, Dict, List, Optional

from app.automation.backup_execution_service import (
    execute_database_backup
)

from app.repository.reporting_event_repository import (
    log_agentic_workflow_history,
    log_nlp_action
)


# =========================================================
# CONFIGURATION
# =========================================================

APPROVAL_REQUEST_FOLDER = "approval_requests"

PENDING_APPROVALS_FILE = os.path.join(
    APPROVAL_REQUEST_FOLDER,
    "pending_approvals.json"
)

APPROVAL_HISTORY_FILE = os.path.join(
    APPROVAL_REQUEST_FOLDER,
    "approval_history.json"
)

EXECUTION_HISTORY_FILE = os.path.join(
    APPROVAL_REQUEST_FOLDER,
    "execution_history.json"
)

GOVERNANCE_AUDIT_FILE = os.path.join(
    APPROVAL_REQUEST_FOLDER,
    "governance_audit_log.json"
)


# =========================================================
# COMMON UTILITIES
# =========================================================

def ensure_approval_folder() -> None:
    """
    Ensure approval folder exists.
    """

    os.makedirs(
        APPROVAL_REQUEST_FOLDER,
        exist_ok=True
    )


def current_timestamp() -> str:
    """
    Return current timestamp.
    """

    return datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


def build_execution_id() -> str:
    """
    Build unique execution ID.
    """

    return "EXEC-" + datetime.now().strftime(
        "%Y%m%d%H%M%S%f"
    )


def load_json_list(
    file_path: str
) -> List[Dict[str, Any]]:
    """
    Load JSON list safely.
    """

    try:

        if not os.path.exists(
            file_path
        ):

            return []

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(
                file
            )

        if isinstance(
            data,
            list
        ):

            return data

        return []

    except Exception:

        return []


def save_json_list(
    file_path: str,
    records: List[Dict[str, Any]]
) -> None:
    """
    Save JSON list safely.
    """

    ensure_approval_folder()

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            records,
            file,
            indent=4,
            ensure_ascii=False
        )


def append_json_record(
    file_path: str,
    record: Dict[str, Any]
) -> None:
    """
    Append JSON record.
    """

    records = load_json_list(
        file_path
    )

    records.append(
        record
    )

    save_json_list(
        file_path,
        records
    )


def safe_get(
    data: Dict[str, Any],
    keys: List[str],
    default_value: Any = ""
) -> Any:
    """
    Get first available key value from dictionary.
    """

    for key in keys:

        value = data.get(
            key
        )

        if value not in [
            None,
            ""
        ]:

            return value

    return default_value


# =========================================================
# APPROVAL ID EXTRACTION
# =========================================================

def extract_approval_id_from_text(
    text: str
) -> Optional[str]:
    """
    Extract approval UUID from natural language text.
    """

    if not text:

        return None

    uuid_pattern = (
        r"[0-9a-fA-F]{8}-"
        r"[0-9a-fA-F]{4}-"
        r"[0-9a-fA-F]{4}-"
        r"[0-9a-fA-F]{4}-"
        r"[0-9a-fA-F]{12}"
    )

    match = re.search(
        uuid_pattern,
        text
    )

    if not match:

        return None

    return match.group(
        0
    )


def detect_nlp_approval_intent(
    text: str
) -> str:
    """
    Detect NLP approval command intent.
    """

    normalized_text = str(
        text or ""
    ).lower()

    if any(
        phrase in normalized_text
        for phrase in [
            "execute approval",
            "execute approved",
            "run approval",
            "run approved",
            "execute request",
            "run request",
            "perform approval",
            "start approval"
        ]
    ):

        return "EXECUTE_APPROVAL"

    if any(
        phrase in normalized_text
        for phrase in [
            "check approval",
            "approval status",
            "status of approval",
            "find approval"
        ]
    ):

        return "CHECK_APPROVAL_STATUS"

    return "UNKNOWN"


# =========================================================
# APPROVAL LOOKUP
# =========================================================

def find_approval_by_id(
    approval_id: str
) -> Dict[str, Any]:
    """
    Find approval by ID from pending approvals or approval history.
    """

    pending_approvals = load_json_list(
        PENDING_APPROVALS_FILE
    )

    approval_history = load_json_list(
        APPROVAL_HISTORY_FILE
    )

    for approval in pending_approvals:

        current_approval_id = safe_get(
            approval,
            [
                "approval_id",
                "request_id"
            ]
        )

        if current_approval_id == approval_id:

            return {
                "found": True,
                "source": "PENDING_APPROVALS",
                "approval": approval
            }

    for approval in approval_history:

        current_approval_id = safe_get(
            approval,
            [
                "approval_id",
                "request_id"
            ]
        )

        if current_approval_id == approval_id:

            return {
                "found": True,
                "source": "APPROVAL_HISTORY",
                "approval": approval
            }

    return {
        "found": False,
        "source": "NOT_FOUND",
        "approval": None
    }


# =========================================================
# DUPLICATE EXECUTION CHECK
# =========================================================

def is_already_executed(
    approval_id: str
) -> bool:
    """
    Check if approval was already executed successfully.
    """

    execution_history = load_json_list(
        EXECUTION_HISTORY_FILE
    )

    for execution in execution_history:

        existing_approval_id = safe_get(
            execution,
            [
                "approval_id"
            ]
        )

        execution_status = str(
            safe_get(
                execution,
                [
                    "execution_status",
                    "overall_status",
                    "status"
                ],
                ""
            )
        ).upper()

        if existing_approval_id == approval_id and execution_status in [
            "COMPLETED",
            "SUCCESS",
            "RUNBOOK_REQUEST_CREATED",
            "BACKUP_REQUEST_CREATED",
            "BACKUP_COMPLETED",
            "ACTION_REQUEST_CREATED"
        ]:

            return True

    return False


# =========================================================
# APPROVED ACTION EXECUTION
# =========================================================

def execute_approved_action(
    approval: Dict[str, Any],
    performed_by: str = "Lead DBA"
) -> Dict[str, Any]:
    """
    Execute approved action in governed safe mode.
    """

    approval_id = safe_get(
        approval,
        [
            "approval_id",
            "request_id"
        ]
    )

    action_name = safe_get(
        approval,
        [
            "action_name",
            "action_type"
        ],
        "UNKNOWN_ACTION"
    )

    target_name = safe_get(
        approval,
        [
            "target_name",
            "database",
            "database_name"
        ],
        "UNKNOWN_TARGET"
    )

    action_name_upper = str(
        action_name
    ).upper()

    if action_name_upper == "RESTART_SQL_AGENT_JOB":

        return {
            "approval_id": approval_id,
            "action_name": action_name,
            "target_name": target_name,
            "execution_status": "RUNBOOK_REQUEST_CREATED",
            "result": "Azure Automation runbook request created after approval.",
            "runbook_status": "REQUEST_CREATED",
            "message": "SQL Agent job restart request prepared for governed automation."
        }

    if action_name_upper == "FULL_DATABASE_BACKUP":

        backup_result = execute_database_backup(
            database_name=target_name,
            approval_id=approval_id,
            requested_by=performed_by,
            backup_type="FULL",
            execution_mode="SIMULATED"
        )

        return {
            "approval_id": approval_id,
            "action_name": action_name,
            "target_name": target_name,
            "execution_status": backup_result.get(
                "execution_status",
                "BACKUP_COMPLETED"
            ),
            "result": backup_result.get(
                "message"
            ),
            "runbook_status": "NOT_REQUIRED",
            "message": backup_result.get(
                "message"
            ),
            "backup_result": backup_result
        }

    return {
        "approval_id": approval_id,
        "action_name": action_name,
        "target_name": target_name,
        "execution_status": "ACTION_REQUEST_CREATED",
        "result": "Approved action request created.",
        "runbook_status": "REQUEST_CREATED",
        "message": "Approved action request prepared for governed automation."
    }


# =========================================================
# EXECUTION HISTORY
# =========================================================

def save_execution_history(
    execution_result: Dict[str, Any],
    performed_by: str = "NLP DBA Assistant"
) -> Dict[str, Any]:
    """
    Save execution history for non-backup actions.

    Backup actions are already recorded by backup_execution_service.
    """

    if execution_result.get(
        "action_name"
    ) == "FULL_DATABASE_BACKUP" and execution_result.get(
        "backup_result"
    ):

        return execution_result.get(
            "backup_result"
        )

    timestamp = current_timestamp()

    execution_record = {
        "execution_id": build_execution_id(),
        "executed_at": timestamp,
        "timestamp": timestamp,
        "approval_id": execution_result.get(
            "approval_id"
        ),
        "action_name": execution_result.get(
            "action_name"
        ),
        "action_executed": execution_result.get(
            "action_name"
        ),
        "target_name": execution_result.get(
            "target_name"
        ),
        "database": execution_result.get(
            "target_name"
        ),
        "execution_status": execution_result.get(
            "execution_status"
        ),
        "overall_status": execution_result.get(
            "execution_status"
        ),
        "result": execution_result.get(
            "result"
        ),
        "message": execution_result.get(
            "message"
        ),
        "runbook_status": execution_result.get(
            "runbook_status"
        ),
        "performed_by": performed_by
    }

    append_json_record(
        EXECUTION_HISTORY_FILE,
        execution_record
    )

    return execution_record


# =========================================================
# GOVERNANCE AUDIT
# =========================================================

def save_governance_audit(
    execution_result: Dict[str, Any],
    event_type: str,
    status: str,
    message: str,
    performed_by: str = "NLP DBA Assistant"
) -> Dict[str, Any]:
    """
    Save governance audit event for non-backup actions.

    Backup actions are already audited by backup_execution_service.
    """

    if execution_result.get(
        "action_name"
    ) == "FULL_DATABASE_BACKUP" and execution_result.get(
        "backup_result"
    ):

        return execution_result.get(
            "backup_result"
        )

    timestamp = current_timestamp()

    audit_record = {
        "created_at": timestamp,
        "timestamp": timestamp,
        "event_type": event_type,
        "activity_type": event_type,
        "approval_id": execution_result.get(
            "approval_id"
        ),
        "action_name": execution_result.get(
            "action_name"
        ),
        "target_name": execution_result.get(
            "target_name"
        ),
        "object_affected": execution_result.get(
            "target_name"
        ),
        "status": status,
        "result": status,
        "performed_by": performed_by,
        "user": performed_by,
        "message": message,
        "comments": message
    }

    append_json_record(
        GOVERNANCE_AUDIT_FILE,
        audit_record
    )

    return audit_record


# =========================================================
# MAIN NLP HANDLER
# =========================================================

def handle_nlp_approval_request(
    natural_language_query: str,
    user: str = "Lead DBA"
) -> Dict[str, Any]:
    """
    Handle NLP approval status check or execution request.
    """

    timestamp = current_timestamp()

    approval_id = extract_approval_id_from_text(
        natural_language_query
    )

    intent = detect_nlp_approval_intent(
        natural_language_query
    )

    if not approval_id:

        log_nlp_action(
            user=user,
            natural_language_query=natural_language_query,
            generated_sql="",
            risk_classification="UNKNOWN",
            approval_status="APPROVAL_ID_MISSING",
            execution_status="FAILED",
            timestamp=timestamp
        )

        log_agentic_workflow_history(
            workflow_name="NLP Approval Execution Workflow",
            trigger_source="NLP DBA Assistant",
            status="FAILED",
            duration="",
            result_summary="Approval ID was not found in the natural language query.",
            timestamp=timestamp
        )

        return {
            "overall_status": "FAILED",
            "intent": intent,
            "approval_id": None,
            "message": "Approval ID was not found in the NLP request."
        }

    lookup_result = find_approval_by_id(
        approval_id
    )

    if not lookup_result.get(
        "found"
    ):

        log_nlp_action(
            user=user,
            natural_language_query=natural_language_query,
            generated_sql="",
            risk_classification="UNKNOWN",
            approval_status="NOT_FOUND",
            execution_status="FAILED",
            timestamp=timestamp
        )

        log_agentic_workflow_history(
            workflow_name="NLP Approval Execution Workflow",
            trigger_source="NLP DBA Assistant",
            status="FAILED",
            duration="",
            result_summary=f"Approval ID not found: {approval_id}",
            timestamp=timestamp
        )

        return {
            "overall_status": "FAILED",
            "intent": intent,
            "approval_id": approval_id,
            "message": "Approval ID was not found in pending approvals or approval history."
        }

    approval = lookup_result.get(
        "approval"
    )

    approval_status = str(
        safe_get(
            approval,
            [
                "approval_status",
                "status"
            ],
            "UNKNOWN"
        )
    ).upper()

    risk_level = safe_get(
        approval,
        [
            "risk_level"
        ],
        "UNKNOWN"
    )

    action_name = safe_get(
        approval,
        [
            "action_name",
            "action_type"
        ],
        "UNKNOWN_ACTION"
    )

    target_name = safe_get(
        approval,
        [
            "target_name",
            "database",
            "database_name"
        ],
        "UNKNOWN_TARGET"
    )

    if intent == "CHECK_APPROVAL_STATUS":

        log_nlp_action(
            user=user,
            natural_language_query=natural_language_query,
            generated_sql="",
            risk_classification=risk_level,
            approval_status=approval_status,
            execution_status="STATUS_CHECKED",
            timestamp=timestamp
        )

        log_agentic_workflow_history(
            workflow_name="NLP Approval Status Workflow",
            trigger_source="NLP DBA Assistant",
            status="COMPLETED",
            duration="",
            result_summary=f"Approval status checked for {approval_id}: {approval_status}",
            timestamp=timestamp
        )

        return {
            "overall_status": "COMPLETED",
            "intent": intent,
            "approval_id": approval_id,
            "approval_status": approval_status,
            "action_name": action_name,
            "target_name": target_name,
            "risk_level": risk_level,
            "message": f"Approval status is {approval_status}."
        }

    if intent != "EXECUTE_APPROVAL":

        log_nlp_action(
            user=user,
            natural_language_query=natural_language_query,
            generated_sql="",
            risk_classification=risk_level,
            approval_status=approval_status,
            execution_status="UNKNOWN_INTENT",
            timestamp=timestamp
        )

        return {
            "overall_status": "FAILED",
            "intent": intent,
            "approval_id": approval_id,
            "approval_status": approval_status,
            "message": "NLP intent is not supported for approval execution."
        }

    if approval_status != "APPROVED":

        blocked_result = {
            "approval_id": approval_id,
            "action_name": action_name,
            "target_name": target_name,
            "execution_status": "BLOCKED",
            "result": "Execution blocked because approval is not approved.",
            "message": f"Approval status is {approval_status}. Execution requires APPROVED status.",
            "runbook_status": "NOT_CREATED"
        }

        save_governance_audit(
            execution_result=blocked_result,
            event_type="NLP_REMEDIATION_EXECUTION_BLOCKED",
            status="BLOCKED",
            message=blocked_result.get(
                "message"
            ),
            performed_by=user
        )

        log_nlp_action(
            user=user,
            natural_language_query=natural_language_query,
            generated_sql="",
            risk_classification=risk_level,
            approval_status=approval_status,
            execution_status="BLOCKED",
            timestamp=timestamp
        )

        log_agentic_workflow_history(
            workflow_name="NLP Approval Execution Workflow",
            trigger_source="NLP DBA Assistant",
            status="BLOCKED",
            duration="",
            result_summary=blocked_result.get(
                "message"
            ),
            timestamp=timestamp
        )

        return {
            "overall_status": "BLOCKED",
            "intent": intent,
            "approval_id": approval_id,
            "approval_status": approval_status,
            "action_name": action_name,
            "target_name": target_name,
            "risk_level": risk_level,
            "message": blocked_result.get(
                "message"
            )
        }

    if is_already_executed(
        approval_id
    ):

        log_nlp_action(
            user=user,
            natural_language_query=natural_language_query,
            generated_sql="",
            risk_classification=risk_level,
            approval_status=approval_status,
            execution_status="ALREADY_EXECUTED",
            timestamp=timestamp
        )

        log_agentic_workflow_history(
            workflow_name="NLP Approval Execution Workflow",
            trigger_source="NLP DBA Assistant",
            status="SKIPPED",
            duration="",
            result_summary=f"Approval ID already executed: {approval_id}",
            timestamp=timestamp
        )

        return {
            "overall_status": "SKIPPED",
            "intent": intent,
            "approval_id": approval_id,
            "approval_status": approval_status,
            "action_name": action_name,
            "target_name": target_name,
            "risk_level": risk_level,
            "message": "This approval request has already been executed."
        }

    execution_result = execute_approved_action(
        approval=approval,
        performed_by=user
    )

    execution_record = save_execution_history(
        execution_result=execution_result,
        performed_by=user
    )

    audit_record = save_governance_audit(
        execution_result=execution_result,
        event_type="NLP_REMEDIATION_EXECUTED",
        status=execution_result.get(
            "execution_status"
        ),
        message=execution_result.get(
            "message"
        ),
        performed_by=user
    )

    log_nlp_action(
        user=user,
        natural_language_query=natural_language_query,
        generated_sql="",
        risk_classification=risk_level,
        approval_status=approval_status,
        execution_status=execution_result.get(
            "execution_status"
        ),
        timestamp=timestamp
    )

    log_agentic_workflow_history(
        workflow_name="NLP Approval Execution Workflow",
        trigger_source="NLP DBA Assistant",
        status=execution_result.get(
            "execution_status"
        ),
        duration="",
        result_summary=execution_result.get(
            "message"
        ),
        timestamp=timestamp
    )

    return {
        "overall_status": execution_result.get(
            "execution_status"
        ),
        "intent": intent,
        "approval_id": approval_id,
        "approval_status": approval_status,
        "action_name": action_name,
        "target_name": target_name,
        "risk_level": risk_level,
        "execution_record": execution_record,
        "audit_record": audit_record,
        "message": execution_result.get(
            "message"
        )
    }


# =========================================================
# DIRECT EXECUTION
# =========================================================

if __name__ == "__main__":

    sample_query = (
        "check approval status for "
        "4ddc91f1-066f-4487-a04f-f114bd2d3383"
    )

    result = handle_nlp_approval_request(
        natural_language_query=sample_query,
        user="Lead DBA"
    )

    print(
        json.dumps(
            result,
            indent=4
        )
    )