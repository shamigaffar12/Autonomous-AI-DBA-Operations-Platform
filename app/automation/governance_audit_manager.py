# =========================================================
# Governance Audit Manager
# Autonomous AI DBA Operations Platform
# =========================================================

import os
import json

from datetime import datetime


# =========================================================
# FILE CONFIGURATION
# =========================================================

GOVERNANCE_AUDIT_DIR = "approval_requests"

GOVERNANCE_AUDIT_FILE = os.path.join(
    GOVERNANCE_AUDIT_DIR,
    "governance_audit_log.json"
)


# =========================================================
# ENSURE STORAGE
# =========================================================

def ensure_governance_audit_storage():
    """
    Ensure governance audit JSON file exists.
    """

    if not os.path.exists(
        GOVERNANCE_AUDIT_DIR
    ):

        os.makedirs(
            GOVERNANCE_AUDIT_DIR
        )

    if not os.path.exists(
        GOVERNANCE_AUDIT_FILE
    ):

        with open(
            GOVERNANCE_AUDIT_FILE,
            "w"
        ) as file:

            json.dump(
                [],
                file,
                indent=4
            )


# =========================================================
# LOAD GOVERNANCE AUDIT LOGS
# =========================================================

def load_governance_audit_logs():
    """
    Load governance audit logs.
    """

    ensure_governance_audit_storage()

    with open(
        GOVERNANCE_AUDIT_FILE,
        "r"
    ) as file:

        return json.load(
            file
        )


# =========================================================
# SAVE GOVERNANCE AUDIT LOGS
# =========================================================

def save_governance_audit_logs(
    logs
):
    """
    Save governance audit logs.
    """

    ensure_governance_audit_storage()

    with open(
        GOVERNANCE_AUDIT_FILE,
        "w"
    ) as file:

        json.dump(
            logs,
            file,
            indent=4
        )


# =========================================================
# ADD GOVERNANCE AUDIT LOG
# =========================================================

def add_governance_audit_log(
    event_type,
    approval_id,
    action_name=None,
    target_name=None,
    status=None,
    performed_by="Lead DBA",
    message=None
):
    """
    Add governance audit log entry.
    """

    logs = load_governance_audit_logs()

    audit_record = {
        "audit_id": f"AUDIT-{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
        "event_type": event_type,
        "approval_id": approval_id,
        "action_name": action_name,
        "target_name": target_name,
        "status": status,
        "performed_by": performed_by,
        "message": message,
        "created_at": str(datetime.now())
    }

    logs.append(
        audit_record
    )

    save_governance_audit_logs(
        logs
    )

    return audit_record


# =========================================================
# LIST GOVERNANCE AUDIT LOGS
# =========================================================

def list_governance_audit_logs():
    """
    Return governance audit logs.
    """

    return load_governance_audit_logs()