# =========================================================
# NLP Intent Classifier
# Autonomous AI DBA Operations Platform
# =========================================================


# =========================================================
# CLASSIFY USER INTENT
# =========================================================

def classify_dba_intent(
    user_query
):
    """
    Classify natural language DBA request into platform intent.
    """

    query = user_query.lower().strip()

    # =====================================================
    # REMEDIATION REQUEST
    # Keep this before failed job check because restart
    # queries may also contain job keywords.
    # =====================================================

    if any(
        keyword in query
        for keyword in [
            "restart job",
            "restart sql job",
            "restart sql agent job",
            "restart agent job",
            "fix failed job",
            "remediate",
            "remediation",
            "execute remediation",
            "run automation",
            "trigger runbook"
        ]
    ):

        return {
            "intent": "REMEDIATION_REQUEST",
            "confidence": "HIGH",
            "risk_level": "MEDIUM"
        }

    # =====================================================
    # DATABASE HEALTH
    # =====================================================

    if any(
        keyword in query
        for keyword in [
            "health",
            "database health",
            "db health",
            "daily health",
            "overall status",
            "platform status",
            "system status"
        ]
    ):

        return {
            "intent": "DATABASE_HEALTH",
            "confidence": "HIGH",
            "risk_level": "LOW"
        }

    # =====================================================
    # FAILED JOB CHECK
    # =====================================================

    if any(
        keyword in query
        for keyword in [
            "failed job",
            "sql job",
            "agent job",
            "job failure",
            "failed sql job"
        ]
    ):

        return {
            "intent": "FAILED_JOB_CHECK",
            "confidence": "HIGH",
            "risk_level": "MEDIUM"
        }

    # =====================================================
    # APPROVAL STATUS
    # =====================================================

    if any(
        keyword in query
        for keyword in [
            "pending approval",
            "approval request",
            "approvals",
            "approval status",
            "governance"
        ]
    ):

        return {
            "intent": "APPROVAL_STATUS",
            "confidence": "HIGH",
            "risk_level": "LOW"
        }

    # =====================================================
    # AUDIT LOGS
    # =====================================================

    if any(
        keyword in query
        for keyword in [
            "audit",
            "audit log",
            "audit logs",
            "audit events",
            "governance audit",
            "tracking"
        ]
    ):

        return {
            "intent": "AUDIT_LOGS",
            "confidence": "HIGH",
            "risk_level": "LOW"
        }

    # =====================================================
    # EXECUTION HISTORY
    # =====================================================

    if any(
        keyword in query
        for keyword in [
            "execution",
            "executed",
            "runbook",
            "automation",
            "execution history",
            "runbook history"
        ]
    ):

        return {
            "intent": "EXECUTION_HISTORY",
            "confidence": "HIGH",
            "risk_level": "LOW"
        }

    # =====================================================
    # REPORT STATUS
    # =====================================================

    if any(
        keyword in query
        for keyword in [
            "report",
            "daily report",
            "health report",
            "excel report",
            "generate report"
        ]
    ):

        return {
            "intent": "REPORT_STATUS",
            "confidence": "HIGH",
            "risk_level": "LOW"
        }

    # =====================================================
    # GENERAL QUERY
    # =====================================================

    return {
        "intent": "GENERAL_DBA_QUERY",
        "confidence": "LOW",
        "risk_level": "LOW"
    }