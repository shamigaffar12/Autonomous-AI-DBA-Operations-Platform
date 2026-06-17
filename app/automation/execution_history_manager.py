# =========================================================
# Execution History Manager
# Autonomous AI DBA Operations Platform
# =========================================================

import os
import json

from datetime import datetime


# =========================================================
# FILE CONFIGURATION
# =========================================================

EXECUTION_HISTORY_DIR = "approval_requests"

EXECUTION_HISTORY_FILE = os.path.join(
    EXECUTION_HISTORY_DIR,
    "execution_history.json"
)


# =========================================================
# ENSURE STORAGE
# =========================================================

def ensure_execution_history_storage():
    """
    Ensure execution history folder and JSON file exist.
    """

    if not os.path.exists(
        EXECUTION_HISTORY_DIR
    ):

        os.makedirs(
            EXECUTION_HISTORY_DIR
        )

    if not os.path.exists(
        EXECUTION_HISTORY_FILE
    ):

        with open(
            EXECUTION_HISTORY_FILE,
            "w"
        ) as file:

            json.dump(
                [],
                file,
                indent=4
            )


# =========================================================
# LOAD EXECUTION HISTORY
# =========================================================

def load_execution_history():
    """
    Load execution history records.
    """

    ensure_execution_history_storage()

    with open(
        EXECUTION_HISTORY_FILE,
        "r"
    ) as file:

        return json.load(
            file
        )


# =========================================================
# SAVE EXECUTION HISTORY
# =========================================================

def save_execution_history(
    history
):
    """
    Save execution history records.
    """

    ensure_execution_history_storage()

    with open(
        EXECUTION_HISTORY_FILE,
        "w"
    ) as file:

        json.dump(
            history,
            file,
            indent=4
        )


# =========================================================
# ADD EXECUTION HISTORY
# =========================================================

def add_execution_history(
    execution_result
):
    """
    Add execution result into execution history.
    """

    history = load_execution_history()

    execution_record = {
        "execution_id": f"EXEC-{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
        "approval_id": execution_result.get(
            "approval_id"
        ),
        "approval_status": execution_result.get(
            "approval_status"
        ),
        "action_name": execution_result.get(
            "action_name"
        ),
        "target_name": execution_result.get(
            "target_name"
        ),
        "overall_status": execution_result.get(
            "overall_status"
        ),
        "runbook_name": execution_result.get(
            "runbook_name"
        ),
        "integration_mode": execution_result.get(
            "integration_mode"
        ),
        "runbook_request_created": execution_result.get(
            "runbook_request_created"
        ),
        "executed": execution_result.get(
            "executed"
        ),
        "message": execution_result.get(
            "message"
        ),
        "executed_at": execution_result.get(
            "executed_at",
            str(datetime.now())
        )
    }

    history.append(
        execution_record
    )

    save_execution_history(
        history
    )

    return execution_record


# =========================================================
# LIST EXECUTION HISTORY
# =========================================================

def list_execution_history():
    """
    Return all execution history records.
    """

    return load_execution_history()


# =========================================================
# GET EXECUTION BY APPROVAL ID
# =========================================================

def get_execution_by_approval_id(
    approval_id
):
    """
    Return latest execution record for a given approval ID.
    """

    history = load_execution_history()

    matched_records = []

    for record in history:

        if record.get(
            "approval_id"
        ) == approval_id:

            matched_records.append(
                record
            )

    if not matched_records:

        return None

    return matched_records[
        -1
    ]