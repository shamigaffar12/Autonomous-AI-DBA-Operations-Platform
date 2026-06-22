# =========================================================
# Backup Execution Service
# Autonomous AI DBA Operations Platform
# =========================================================

import json
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

from app.repository.reporting_event_repository import (
    log_agentic_workflow_history,
    log_backup_monitoring
)


# =========================================================
# CONFIGURATION
# =========================================================

BACKUP_FOLDER = "database_backups"

APPROVAL_REQUEST_FOLDER = "approval_requests"

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

def current_timestamp() -> str:
    """
    Return current timestamp.
    """

    return datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


def backup_file_timestamp() -> str:
    """
    Return timestamp safe for backup file name.
    """

    return datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )


def ensure_folder(
    folder_path: str
) -> None:
    """
    Ensure folder exists.
    """

    os.makedirs(
        folder_path,
        exist_ok=True
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

    ensure_folder(
        os.path.dirname(
            file_path
        )
    )

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
    Append record into JSON list.
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


def build_execution_id() -> str:
    """
    Build unique backup execution ID.
    """

    return "BKP-EXEC-" + datetime.now().strftime(
        "%Y%m%d%H%M%S%f"
    )


def normalize_value(
    value: Any
) -> str:
    """
    Normalize text value.
    """

    return str(
        value or ""
    ).strip()


# =========================================================
# BACKUP SCRIPT GENERATION
# =========================================================

def build_backup_file_path(
    database_name: str,
    backup_type: str = "FULL"
) -> str:
    """
    Build backup file path for simulated backup execution.
    """

    safe_database_name = normalize_value(
        database_name
    ).replace(
        " ",
        "_"
    )

    safe_backup_type = normalize_value(
        backup_type
    ).upper()

    file_name = (
        f"{safe_database_name}_{safe_backup_type}_"
        f"{backup_file_timestamp()}.bak"
    )

    return os.path.join(
        BACKUP_FOLDER,
        file_name
    )


def build_backup_sql_command(
    database_name: str,
    backup_file_path: str,
    backup_type: str = "FULL"
) -> str:
    """
    Build SQL Server backup command.
    """

    safe_backup_path = backup_file_path.replace(
        "\\",
        "\\\\"
    )

    backup_type_upper = normalize_value(
        backup_type
    ).upper()

    if backup_type_upper == "LOG":

        return (
            f"BACKUP LOG [{database_name}] "
            f"TO DISK = N'{safe_backup_path}' "
            f"WITH INIT, COMPRESSION, STATS = 10;"
        )

    if backup_type_upper == "DIFFERENTIAL":

        return (
            f"BACKUP DATABASE [{database_name}] "
            f"TO DISK = N'{safe_backup_path}' "
            f"WITH DIFFERENTIAL, INIT, COMPRESSION, STATS = 10;"
        )

    return (
        f"BACKUP DATABASE [{database_name}] "
        f"TO DISK = N'{safe_backup_path}' "
        f"WITH INIT, COMPRESSION, STATS = 10;"
    )


# =========================================================
# BACKUP EXECUTION
# =========================================================

def execute_database_backup(
    database_name: str,
    approval_id: str,
    requested_by: str = "Lead DBA",
    backup_type: str = "FULL",
    execution_mode: str = "SIMULATED"
) -> Dict[str, Any]:
    """
    Execute database backup in governed mode.

    Default mode is SIMULATED to keep the platform safe.
    It generates execution records, audit records, backup monitoring data,
    and SQL command details without directly modifying production systems.

    Real SQL execution can be connected later through the existing database
    connection layer after environment validation and secure backup path setup.
    """

    timestamp = current_timestamp()

    ensure_folder(
        BACKUP_FOLDER
    )

    backup_file_path = build_backup_file_path(
        database_name=database_name,
        backup_type=backup_type
    )

    backup_sql_command = build_backup_sql_command(
        database_name=database_name,
        backup_file_path=backup_file_path,
        backup_type=backup_type
    )

    execution_id = build_execution_id()

    backup_result = {
        "execution_id": execution_id,
        "timestamp": timestamp,
        "approval_id": approval_id,
        "database": database_name,
        "backup_type": normalize_value(
            backup_type
        ).upper(),
        "backup_file_path": backup_file_path,
        "backup_sql_command": backup_sql_command,
        "execution_mode": execution_mode,
        "backup_status": "BACKUP_COMPLETED",
        "execution_status": "BACKUP_COMPLETED",
        "overall_status": "BACKUP_COMPLETED",
        "requested_by": requested_by,
        "message": "Database backup completed in governed simulated mode.",
        "output_summary": "Backup command prepared and backup audit trail recorded successfully."
    }

    save_backup_execution_history(
        backup_result
    )

    save_backup_governance_audit(
        backup_result
    )

    log_backup_monitoring(
        database=database_name,
        last_backup_time=timestamp,
        backup_type=normalize_value(
            backup_type
        ).upper(),
        backup_status="BACKUP_COMPLETED",
        recovery_model="FULL",
        timestamp=timestamp
    )

    log_agentic_workflow_history(
        workflow_name="Governed Database Backup Workflow",
        trigger_source="NLP DBA Assistant",
        status="BACKUP_COMPLETED",
        duration="",
        result_summary=(
            "Database backup workflow completed and audit trail recorded "
            f"for {database_name}."
        ),
        timestamp=timestamp
    )

    return backup_result


# =========================================================
# EXECUTION HISTORY
# =========================================================

def save_backup_execution_history(
    backup_result: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Save backup execution history.
    """

    execution_record = {
        "execution_id": backup_result.get(
            "execution_id"
        ),
        "executed_at": backup_result.get(
            "timestamp"
        ),
        "timestamp": backup_result.get(
            "timestamp"
        ),
        "approval_id": backup_result.get(
            "approval_id"
        ),
        "action_name": "FULL_DATABASE_BACKUP",
        "action_executed": "FULL_DATABASE_BACKUP",
        "target_name": backup_result.get(
            "database"
        ),
        "database": backup_result.get(
            "database"
        ),
        "execution_status": backup_result.get(
            "execution_status"
        ),
        "overall_status": backup_result.get(
            "overall_status"
        ),
        "duration": "",
        "result": backup_result.get(
            "message"
        ),
        "message": backup_result.get(
            "message"
        ),
        "output_summary": backup_result.get(
            "output_summary"
        ),
        "backup_file_path": backup_result.get(
            "backup_file_path"
        ),
        "backup_sql_command": backup_result.get(
            "backup_sql_command"
        ),
        "performed_by": backup_result.get(
            "requested_by"
        )
    }

    append_json_record(
        EXECUTION_HISTORY_FILE,
        execution_record
    )

    return execution_record


# =========================================================
# GOVERNANCE AUDIT
# =========================================================

def save_backup_governance_audit(
    backup_result: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Save backup governance audit event.
    """

    audit_record = {
        "created_at": backup_result.get(
            "timestamp"
        ),
        "timestamp": backup_result.get(
            "timestamp"
        ),
        "event_type": "BACKUP_EXECUTED",
        "activity_type": "BACKUP_EXECUTED",
        "approval_id": backup_result.get(
            "approval_id"
        ),
        "action_name": "FULL_DATABASE_BACKUP",
        "target_name": backup_result.get(
            "database"
        ),
        "object_affected": backup_result.get(
            "database"
        ),
        "status": backup_result.get(
            "backup_status"
        ),
        "result": backup_result.get(
            "backup_status"
        ),
        "performed_by": backup_result.get(
            "requested_by"
        ),
        "user": backup_result.get(
            "requested_by"
        ),
        "message": backup_result.get(
            "message"
        ),
        "comments": backup_result.get(
            "output_summary"
        )
    }

    append_json_record(
        GOVERNANCE_AUDIT_FILE,
        audit_record
    )

    return audit_record


# =========================================================
# DIRECT TEST EXECUTION
# =========================================================

if __name__ == "__main__":

    result = execute_database_backup(
        database_name="AdventureWorks2019",
        approval_id="MANUAL-BACKUP-TEST",
        requested_by="Lead DBA",
        backup_type="FULL",
        execution_mode="SIMULATED"
    )

    print(
        json.dumps(
            result,
            indent=4
        )
    )
    