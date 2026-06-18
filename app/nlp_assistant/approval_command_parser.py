# =========================================================
# NLP Approval Command Parser
# Autonomous AI DBA Operations Platform
# =========================================================


# =========================================================
# PARSE APPROVAL COMMAND
# =========================================================

def parse_approval_command(
    user_query
):
    """
    Parse natural language approval command into approval request details.
    """

    query = user_query.lower().strip()

    approval_payload = {
        "action_name": "GENERAL_DBA_APPROVAL",
        "target_name": "SQL Server",
        "risk_level": "MEDIUM",
        "reason": user_query,
        "metadata": {
            "source": "NLP_DBA_ASSISTANT",
            "original_query": user_query
        }
    }

    if (
        "full backup" in query
        or "database backup" in query
        or "take backup" in query
    ):

        approval_payload.update(
            {
                "action_name": "FULL_DATABASE_BACKUP",
                "target_name": "AdventureWorks2019",
                "risk_level": "MEDIUM",
                "reason": "NLP request to create approval for full database backup."
            }
        )

        return approval_payload

    if (
        "differential backup" in query
        or "diff backup" in query
    ):

        approval_payload.update(
            {
                "action_name": "DIFFERENTIAL_DATABASE_BACKUP",
                "target_name": "AdventureWorks2019",
                "risk_level": "MEDIUM",
                "reason": "NLP request to create approval for differential database backup."
            }
        )

        return approval_payload

    if (
        "log backup" in query
        or "transaction log backup" in query
    ):

        approval_payload.update(
            {
                "action_name": "TRANSACTION_LOG_BACKUP",
                "target_name": "AdventureWorks2019",
                "risk_level": "MEDIUM",
                "reason": "NLP request to create approval for transaction log backup."
            }
        )

        return approval_payload

    if (
        "restart" in query
        and (
            "sql agent" in query
            or "job" in query
            or "failed job" in query
        )
    ):

        approval_payload.update(
            {
                "action_name": "RESTART_SQL_AGENT_JOB",
                "target_name": "Failed SQL Agent Job",
                "risk_level": "HIGH",
                "reason": "NLP request to create approval for restarting failed SQL Agent job."
            }
        )

        return approval_payload

    if (
        "remediation" in query
        or "fix issue" in query
        or "resolve issue" in query
    ):

        approval_payload.update(
            {
                "action_name": "DBA_REMEDIATION_ACTION",
                "target_name": "SQL Server",
                "risk_level": "HIGH",
                "reason": "NLP request to create approval for DBA remediation action."
            }
        )

        return approval_payload

    return approval_payload