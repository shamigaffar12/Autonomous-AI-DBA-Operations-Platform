# =========================================================
# Approval Repository
# Autonomous AI DBA Operations Platform
# =========================================================

import json
import os
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional


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


# =========================================================
# COMMON UTILITIES
# =========================================================

def ensure_approval_folder() -> None:
    """
    Ensure approval request folder exists.
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


def safe_get(
    data: Dict[str, Any],
    keys: List[str],
    default_value: Any = ""
) -> Any:
    """
    Return first available value from dictionary.
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


def normalize_value(
    value: Any
) -> str:
    """
    Normalize string values for duplicate comparison.
    """

    return str(
        value or ""
    ).strip().upper()


def build_approval_id() -> str:
    """
    Build approval UUID.
    """

    return str(
        uuid.uuid4()
    )


# =========================================================
# APPROVAL DATA NORMALIZATION
# =========================================================

def normalize_approval_request(
    approval_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Normalize approval request payload.

    Supports old and new keys:
    - approval_id / request_id
    - action_name / action_type
    - target_name / database / database_name / job_name
    - approval_status / status
    """

    timestamp = current_timestamp()

    approval_id = safe_get(
        approval_data,
        [
            "approval_id",
            "request_id"
        ],
        build_approval_id()
    )

    action_type = safe_get(
        approval_data,
        [
            "action_type",
            "action_name"
        ],
        "UNKNOWN_ACTION"
    )

    target_name = safe_get(
        approval_data,
        [
            "target_name",
            "database",
            "database_name",
            "job_name"
        ],
        "UNKNOWN_TARGET"
    )

    risk_level = safe_get(
        approval_data,
        [
            "risk_level"
        ],
        "MEDIUM"
    )

    requestor = safe_get(
        approval_data,
        [
            "requestor",
            "requested_by",
            "created_by",
            "user"
        ],
        "NLP DBA Assistant"
    )

    created_at = safe_get(
        approval_data,
        [
            "created_at",
            "timestamp",
            "requested_at"
        ],
        timestamp
    )

    approval_status = safe_get(
        approval_data,
        [
            "approval_status",
            "status"
        ],
        "PENDING_APPROVAL"
    )

    normalized_request = dict(
        approval_data
    )

    normalized_request.update(
        {
            "approval_id": approval_id,
            "request_id": approval_id,
            "action_type": action_type,
            "action_name": action_type,
            "target_name": target_name,
            "risk_level": risk_level,
            "requestor": requestor,
            "requested_by": requestor,
            "created_by": requestor,
            "created_at": created_at,
            "timestamp": created_at,
            "approval_status": approval_status,
            "status": approval_status
        }
    )

    if "database" not in normalized_request:

        normalized_request["database"] = target_name

    if "database_name" not in normalized_request:

        normalized_request["database_name"] = target_name

    return normalized_request


def build_duplicate_key(
    approval_data: Dict[str, Any]
) -> str:
    """
    Build duplicate prevention key.

    Duplicate means same:
    - action type
    - target
    - risk level
    """

    action_type = safe_get(
        approval_data,
        [
            "action_type",
            "action_name"
        ],
        "UNKNOWN_ACTION"
    )

    target_name = safe_get(
        approval_data,
        [
            "target_name",
            "database",
            "database_name",
            "job_name"
        ],
        "UNKNOWN_TARGET"
    )

    risk_level = safe_get(
        approval_data,
        [
            "risk_level"
        ],
        "MEDIUM"
    )

    return "|".join(
        [
            normalize_value(
                action_type
            ),
            normalize_value(
                target_name
            ),
            normalize_value(
                risk_level
            )
        ]
    )


# =========================================================
# READ FUNCTIONS
# =========================================================

def get_pending_approvals() -> List[Dict[str, Any]]:
    """
    Return all pending approvals.
    """

    return load_json_list(
        PENDING_APPROVALS_FILE
    )


def get_approval_history() -> List[Dict[str, Any]]:
    """
    Return approval history.
    """

    return load_json_list(
        APPROVAL_HISTORY_FILE
    )


def get_all_approvals() -> Dict[str, List[Dict[str, Any]]]:
    """
    Return pending and history approvals.
    """

    return {
        "pending_approvals": get_pending_approvals(),
        "approval_history": get_approval_history()
    }


def find_approval_by_id(
    approval_id: str
) -> Dict[str, Any]:
    """
    Find approval from pending approvals or approval history.
    """

    for approval in get_pending_approvals():

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

    for approval in get_approval_history():

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
# DUPLICATE PREVENTION
# =========================================================

def find_duplicate_pending_approval(
    approval_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Check whether same approval request is already pending.
    """

    incoming_request = normalize_approval_request(
        approval_data
    )

    incoming_duplicate_key = build_duplicate_key(
        incoming_request
    )

    pending_approvals = get_pending_approvals()

    for existing_approval in pending_approvals:

        existing_status = normalize_value(
            safe_get(
                existing_approval,
                [
                    "approval_status",
                    "status"
                ],
                "PENDING_APPROVAL"
            )
        )

        if existing_status != "PENDING_APPROVAL":

            continue

        existing_duplicate_key = build_duplicate_key(
            existing_approval
        )

        if existing_duplicate_key == incoming_duplicate_key:

            return {
                "duplicate_found": True,
                "message": "Duplicate pending approval request already exists.",
                "existing_approval": existing_approval,
                "duplicate_key": incoming_duplicate_key
            }

    return {
        "duplicate_found": False,
        "message": "No duplicate pending approval found.",
        "existing_approval": None,
        "duplicate_key": incoming_duplicate_key
    }


def is_duplicate_pending_approval(
    approval_data: Dict[str, Any]
) -> bool:
    """
    Boolean duplicate check helper.
    """

    duplicate_result = find_duplicate_pending_approval(
        approval_data
    )

    return bool(
        duplicate_result.get(
            "duplicate_found"
        )
    )


# =========================================================
# CREATE APPROVAL REQUEST
# =========================================================

def create_approval_request(
    approval_data: Dict[str, Any],
    prevent_duplicates: bool = True
) -> Dict[str, Any]:
    """
    Create approval request with duplicate prevention.

    If duplicate pending approval exists, existing approval is returned.
    """

    normalized_request = normalize_approval_request(
        approval_data
    )

    if prevent_duplicates:

        duplicate_result = find_duplicate_pending_approval(
            normalized_request
        )

        if duplicate_result.get(
            "duplicate_found"
        ):

            existing_approval = duplicate_result.get(
                "existing_approval"
            )

            return {
                "overall_status": "DUPLICATE_APPROVAL_FOUND",
                "created": False,
                "duplicate_prevention": "ACTIVE",
                "message": "Duplicate pending approval was not created. Existing approval returned.",
                "approval_id": safe_get(
                    existing_approval,
                    [
                        "approval_id",
                        "request_id"
                    ]
                ),
                "approval": existing_approval,
                "duplicate_key": duplicate_result.get(
                    "duplicate_key"
                )
            }

    pending_approvals = get_pending_approvals()

    pending_approvals.append(
        normalized_request
    )

    save_json_list(
        PENDING_APPROVALS_FILE,
        pending_approvals
    )

    return {
        "overall_status": "APPROVAL_CREATED",
        "created": True,
        "duplicate_prevention": "ACTIVE" if prevent_duplicates else "DISABLED",
        "message": "Approval request created successfully.",
        "approval_id": normalized_request.get(
            "approval_id"
        ),
        "approval": normalized_request,
        "duplicate_key": build_duplicate_key(
            normalized_request
        )
    }


# =========================================================
# COMPATIBILITY FUNCTIONS
# =========================================================


def save_approval(
    approval_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Backward-compatible function.

    Older MCP workflow modules may still import save_approval().
    This function now routes to create_approval_request()
    with duplicate prevention enabled.
    """

    return create_approval_request(
        approval_data=approval_data,
        prevent_duplicates=True
    )

def save_pending_approval(
    approval_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Backward-compatible function.

    Older modules can call save_pending_approval().
    Duplicate prevention remains active.
    """

    return create_approval_request(
        approval_data=approval_data,
        prevent_duplicates=True
    )


def add_pending_approval(
    approval_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Backward-compatible function.

    Older modules can call add_pending_approval().
    Duplicate prevention remains active.
    """

    return create_approval_request(
        approval_data=approval_data,
        prevent_duplicates=True
    )


def create_pending_approval(
    approval_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Backward-compatible function.

    Older modules can call create_pending_approval().
    Duplicate prevention remains active.
    """

    return create_approval_request(
        approval_data=approval_data,
        prevent_duplicates=True
    )


# =========================================================
# STATUS UPDATE HELPERS
# =========================================================

def remove_pending_approval(
    approval_id: str
) -> Dict[str, Any]:
    """
    Remove approval from pending list.
    """

    pending_approvals = get_pending_approvals()

    updated_pending_approvals = []
    removed_approval = None

    for approval in pending_approvals:

        current_approval_id = safe_get(
            approval,
            [
                "approval_id",
                "request_id"
            ]
        )

        if current_approval_id == approval_id:

            removed_approval = approval

        else:

            updated_pending_approvals.append(
                approval
            )

    save_json_list(
        PENDING_APPROVALS_FILE,
        updated_pending_approvals
    )

    if removed_approval:

        return {
            "overall_status": "REMOVED",
            "approval_id": approval_id,
            "approval": removed_approval
        }

    return {
        "overall_status": "NOT_FOUND",
        "approval_id": approval_id,
        "approval": None
    }


def move_approval_to_history(
    approval_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Move approval request into approval history.
    """

    approval_history = get_approval_history()

    normalized_request = normalize_approval_request(
        approval_data
    )

    approval_history.append(
        normalized_request
    )

    save_json_list(
        APPROVAL_HISTORY_FILE,
        approval_history
    )

    return {
        "overall_status": "MOVED_TO_HISTORY",
        "approval_id": normalized_request.get(
            "approval_id"
        ),
        "approval": normalized_request
    }


# =========================================================
# TEST / DIRECT EXECUTION
# =========================================================

if __name__ == "__main__":

    sample_request = {
        "action_type": "FULL_DATABASE_BACKUP",
        "target_name": "AdventureWorks2019",
        "database": "AdventureWorks2019",
        "risk_level": "MEDIUM",
        "requestor": "NLP DBA Assistant",
        "reason": "Testing duplicate approval prevention."
    }

    result = create_approval_request(
        sample_request
    )

    print(
        json.dumps(
            result,
            indent=4
        )
    )
