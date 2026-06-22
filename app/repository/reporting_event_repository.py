# =========================================================
# Reporting Event Repository
# Autonomous AI DBA Operations Platform
# =========================================================

import argparse
import json
import os
from datetime import datetime
from typing import Any, Dict, List, Optional


# =========================================================
# CONFIGURATION
# =========================================================

REPOSITORY_FOLDER = "repository"

PERFORMANCE_METRICS_FILE = os.path.join(
    REPOSITORY_FOLDER,
    "performance_metrics.json"
)

NLP_ACTIONS_FILE = os.path.join(
    REPOSITORY_FOLDER,
    "nlp_actions.json"
)

BACKUP_MONITORING_FILE = os.path.join(
    REPOSITORY_FOLDER,
    "backup_monitoring.json"
)

WORKFLOW_HISTORY_FILE = os.path.join(
    REPOSITORY_FOLDER,
    "workflow_history.json"
)


# =========================================================
# COMMON UTILITIES
# =========================================================

def ensure_repository_folder() -> None:
    """
    Ensure repository folder exists.
    """

    os.makedirs(
        REPOSITORY_FOLDER,
        exist_ok=True
    )


def current_timestamp() -> str:
    """
    Return current timestamp.
    """

    return datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
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

    ensure_repository_folder()

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
    record: Dict[str, Any],
    unique_keys: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Append record into JSON list file.
    """

    records = load_json_list(
        file_path
    )

    if unique_keys:

        new_key = tuple(
            str(
                record.get(
                    key,
                    ""
                )
            )
            for key in unique_keys
        )

        for existing_record in records:

            existing_key = tuple(
                str(
                    existing_record.get(
                        key,
                        ""
                    )
                )
                for key in unique_keys
            )

            if existing_key == new_key:

                return {
                    "status": "SKIPPED",
                    "message": "Duplicate reporting event skipped.",
                    "file_path": file_path,
                    "record": existing_record
                }

    records.append(
        record
    )

    save_json_list(
        file_path,
        records
    )

    return {
        "status": "SAVED",
        "message": "Reporting event saved successfully.",
        "file_path": file_path,
        "record": record
    }


# =========================================================
# PERFORMANCE METRICS LOGGING
# =========================================================

def log_performance_metrics(
    cpu_percent: Any = "",
    memory_percent: Any = "",
    blocking_sessions: Any = "",
    deadlocks: Any = "",
    long_running_queries: Any = "",
    database_size_gb: Any = "",
    active_connections: Any = "",
    timestamp: Optional[str] = None
) -> Dict[str, Any]:
    """
    Log one monitoring cycle performance metric event.
    """

    event_timestamp = timestamp or current_timestamp()

    record = {
        "timestamp": event_timestamp,
        "cpu_percent": cpu_percent,
        "memory_percent": memory_percent,
        "blocking_sessions": blocking_sessions,
        "deadlocks": deadlocks,
        "long_running_queries": long_running_queries,
        "database_size_gb": database_size_gb,
        "active_connections": active_connections
    }

    return append_json_record(
        PERFORMANCE_METRICS_FILE,
        record,
        unique_keys=[
            "timestamp"
        ]
    )


# =========================================================
# NLP ACTION LOGGING
# =========================================================

def log_nlp_action(
    user: str,
    natural_language_query: str,
    generated_sql: str = "",
    risk_classification: str = "",
    approval_status: str = "",
    execution_status: str = "",
    timestamp: Optional[str] = None
) -> Dict[str, Any]:
    """
    Log one NLP DBA Assistant action.
    """

    event_timestamp = timestamp or current_timestamp()

    record = {
        "timestamp": event_timestamp,
        "user": user,
        "natural_language_query": natural_language_query,
        "generated_sql": generated_sql,
        "risk_classification": risk_classification,
        "approval_status": approval_status,
        "execution_status": execution_status
    }

    return append_json_record(
        NLP_ACTIONS_FILE,
        record,
        unique_keys=[
            "timestamp",
            "natural_language_query"
        ]
    )


# =========================================================
# BACKUP MONITORING LOGGING
# =========================================================

def log_backup_monitoring(
    database: str,
    last_backup_time: str = "",
    backup_type: str = "FULL",
    backup_status: str = "UNKNOWN",
    recovery_model: str = "",
    timestamp: Optional[str] = None
) -> Dict[str, Any]:
    """
    Log one backup monitoring event.
    """

    event_timestamp = timestamp or current_timestamp()

    record = {
        "timestamp": event_timestamp,
        "database": database,
        "last_backup_time": last_backup_time,
        "backup_type": backup_type,
        "backup_status": backup_status,
        "recovery_model": recovery_model
    }

    return append_json_record(
        BACKUP_MONITORING_FILE,
        record,
        unique_keys=[
            "timestamp",
            "database",
            "backup_type"
        ]
    )


# =========================================================
# AGENTIC WORKFLOW HISTORY LOGGING
# =========================================================

def log_agentic_workflow_history(
    workflow_name: str,
    trigger_source: str,
    status: str,
    duration: Any = "",
    result_summary: str = "",
    timestamp: Optional[str] = None
) -> Dict[str, Any]:
    """
    Log one agentic workflow execution event.
    """

    event_timestamp = timestamp or current_timestamp()

    record = {
        "timestamp": event_timestamp,
        "workflow_name": workflow_name,
        "trigger_source": trigger_source,
        "status": status,
        "duration": duration,
        "result_summary": result_summary
    }

    return append_json_record(
        WORKFLOW_HISTORY_FILE,
        record,
        unique_keys=[
            "timestamp",
            "workflow_name",
            "trigger_source"
        ]
    )


# =========================================================
# DEMO / INITIAL DATA SEEDING
# =========================================================

def seed_reporting_events_for_current_project() -> Dict[str, Any]:
    """
    Seed reporting events so Excel sheets are populated immediately.
    """

    timestamp = current_timestamp()

    performance_result = log_performance_metrics(
        cpu_percent="Normal",
        memory_percent="Normal",
        blocking_sessions=0,
        deadlocks=0,
        long_running_queries=0,
        database_size_gb="0.27",
        active_connections="Active",
        timestamp=timestamp
    )

    nlp_result = log_nlp_action(
        user="Lead DBA",
        natural_language_query="Generate monthly DBA report and validate approval workflow.",
        generated_sql="",
        risk_classification="LOW",
        approval_status="NOT_REQUIRED",
        execution_status="COMPLETED",
        timestamp=timestamp
    )

    backup_result = log_backup_monitoring(
        database="AdventureWorks2019",
        last_backup_time=timestamp,
        backup_type="FULL",
        backup_status="MONITORED",
        recovery_model="FULL",
        timestamp=timestamp
    )

    workflow_result = log_agentic_workflow_history(
        workflow_name="Monthly Excel Reporting Workflow",
        trigger_source="Manual Script Execution",
        status="COMPLETED",
        duration="",
        result_summary="Monthly DBA Excel workbook generated and reporting sheets populated.",
        timestamp=timestamp
    )

    return {
        "overall_status": "COMPLETED",
        "timestamp": timestamp,
        "performance_metrics": performance_result,
        "nlp_actions": nlp_result,
        "backup_monitoring": backup_result,
        "agentic_workflow_history": workflow_result
    }


# =========================================================
# DIRECT EXECUTION
# =========================================================

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Reporting event repository utility."
    )

    parser.add_argument(
        "--seed",
        action="store_true",
        help="Seed reporting event JSON files for current project."
    )

    args = parser.parse_args()

    if args.seed:

        result = seed_reporting_events_for_current_project()

    else:

        result = {
            "status": "READY",
            "message": "Use --seed to populate reporting event JSON files."
        }

    print(
        json.dumps(
            result,
            indent=4
        )
    )