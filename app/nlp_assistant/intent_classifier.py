# =========================================================
# NLP Intent Classifier
# Autonomous AI DBA Operations Platform
# =========================================================


# =========================================================
# CLASSIFY DBA INTENT
# =========================================================

def classify_dba_intent(
    user_query
):
    """
    Classify natural language DBA query into platform intent.
    """

    query = user_query.lower().strip()

    # =====================================================
    # EXECUTE APPROVED REMEDIATION
    # Must come before generic remediation checks
    # =====================================================

    if (
        "execute approved" in query
        or "run approved" in query
        or "execute approval" in query
        or "execute approved remediation" in query
        or "run approved remediation" in query
    ):

        return {
            "intent": "EXECUTE_APPROVED_REMEDIATION",
            "confidence": "HIGH",
            "risk_level": "HIGH"
        }

    # =====================================================
    # CREATE APPROVAL REQUEST
    # Must come before backup/remediation checks
    # =====================================================

    if (
        "create approval" in query
        or "raise approval" in query
        or "request approval" in query
        or "approval request" in query
        or "create request" in query
        or "raise request" in query
        or "submit approval" in query
        or "generate approval" in query
    ):

        return {
            "intent": "CREATE_APPROVAL_REQUEST",
            "confidence": "HIGH",
            "risk_level": "MEDIUM"
        }

    # =====================================================
    # REMEDIATION REQUEST
    # =====================================================

    if (
        "restart sql agent" in query
        or "restart failed job" in query
        or "restart job" in query
        or "fix failed job" in query
        or "remediate" in query
        or "remediation" in query
        or "fix issue" in query
        or "resolve issue" in query
        or "auto fix" in query
        or "execute remediation" in query
    ):

        return {
            "intent": "REMEDIATION_REQUEST",
            "confidence": "HIGH",
            "risk_level": "HIGH"
        }

    # =====================================================
    # DEADLOCK ANALYSIS
    # =====================================================

    if (
        "deadlock" in query
        or "dead lock" in query
        or "deadlocked" in query
        or "deadlock situation" in query
        or "check deadlock" in query
        or "deadlock analysis" in query
    ):

        return {
            "intent": "DEADLOCK_ANALYSIS",
            "confidence": "HIGH",
            "risk_level": "MEDIUM"
        }

    # =====================================================
    # BACKUP REQUESTS
    # =====================================================

    if (
        "full backup" in query
        or "take full backup" in query
        or "run full backup" in query
        or "create full backup" in query
    ):

        return {
            "intent": "FULL_BACKUP_REQUEST",
            "confidence": "HIGH",
            "risk_level": "MEDIUM"
        }

    if (
        "differential backup" in query
        or "diff backup" in query
        or "take differential backup" in query
        or "run differential backup" in query
    ):

        return {
            "intent": "DIFFERENTIAL_BACKUP_REQUEST",
            "confidence": "HIGH",
            "risk_level": "MEDIUM"
        }

    if (
        "log backup" in query
        or "transaction log backup" in query
        or "take log backup" in query
        or "run log backup" in query
    ):

        return {
            "intent": "LOG_BACKUP_REQUEST",
            "confidence": "HIGH",
            "risk_level": "MEDIUM"
        }

    if (
        "take backup" in query
        or "run backup" in query
        or "create backup" in query
        or "database backup" in query
        or "backup database" in query
    ):

        return {
            "intent": "BACKUP_REQUEST",
            "confidence": "HIGH",
            "risk_level": "MEDIUM"
        }

    # =====================================================
    # BACKUP STATUS
    # =====================================================

    if (
        "backup status" in query
        or "last backup" in query
        or "backup health" in query
        or "check backup" in query
        or "verify backup" in query
        or "backup failure" in query
    ):

        return {
            "intent": "BACKUP_STATUS",
            "confidence": "HIGH",
            "risk_level": "LOW"
        }

    # =====================================================
    # MONITORING CONTROL
    # =====================================================

    if (
        "start monitoring" in query
        or "run monitoring" in query
        or "begin monitoring" in query
        or "enable monitoring" in query
        or "start sql monitoring" in query
    ):

        return {
            "intent": "START_MONITORING",
            "confidence": "HIGH",
            "risk_level": "LOW"
        }

    if (
        "stop monitoring" in query
        or "disable monitoring" in query
        or "pause monitoring" in query
    ):

        return {
            "intent": "STOP_MONITORING",
            "confidence": "HIGH",
            "risk_level": "LOW"
        }

    # =====================================================
    # DAILY HEALTH CHECK
    # =====================================================

    if (
        "run health check" in query
        or "daily health check" in query
        or "run daily health" in query
        or "health check" in query
        or "database health check" in query
        or "dba health check" in query
    ):

        return {
            "intent": "RUN_HEALTH_CHECK",
            "confidence": "HIGH",
            "risk_level": "LOW"
        }

    # =====================================================
    # FULL DBA WORKFLOW
    # =====================================================

    if (
        "run full dba workflow" in query
        or "full dba workflow" in query
        or "execute full workflow" in query
        or "run complete workflow" in query
        or "complete dba workflow" in query
        or "run mcp workflow" in query
        or "execute mcp workflow" in query
    ):

        return {
            "intent": "RUN_FULL_DBA_WORKFLOW",
            "confidence": "HIGH",
            "risk_level": "LOW"
        }

    # =====================================================
    # DATABASE HEALTH
    # =====================================================

    if (
        "database health" in query
        or "db health" in query
        or "platform health" in query
        or "system health" in query
        or "show health" in query
        or "check database" in query
    ):

        return {
            "intent": "DATABASE_HEALTH",
            "confidence": "HIGH",
            "risk_level": "LOW"
        }

    # =====================================================
    # FAILED JOB CHECK
    # =====================================================

    if (
        "failed job" in query
        or "failed sql job" in query
        or "sql agent job" in query
        or "job failure" in query
        or "check failed jobs" in query
        or "show failed jobs" in query
    ):

        return {
            "intent": "FAILED_JOB_CHECK",
            "confidence": "HIGH",
            "risk_level": "MEDIUM"
        }

    # =====================================================
    # APPROVAL STATUS
    # =====================================================

    if (
        "pending approval" in query
        or "pending approvals" in query
        or "show approvals" in query
        or "approval status" in query
        or "governance status" in query
        or "show pending approvals" in query
        or "approval dashboard" in query
    ):

        return {
            "intent": "APPROVAL_STATUS",
            "confidence": "HIGH",
            "risk_level": "LOW"
        }

    # =====================================================
    # AUDIT LOGS
    # =====================================================

    if (
        "audit" in query
        or "audit log" in query
        or "audit logs" in query
        or "show audit" in query
        or "show audit events" in query
        or "governance audit" in query
    ):

        return {
            "intent": "AUDIT_LOGS",
            "confidence": "HIGH",
            "risk_level": "LOW"
        }

    # =====================================================
    # EXECUTION HISTORY
    # =====================================================

    if (
        "execution history" in query
        or "remediation history" in query
        or "show execution" in query
        or "show execution history" in query
        or "executed actions" in query
        or "automation history" in query
    ):

        return {
            "intent": "EXECUTION_HISTORY",
            "confidence": "HIGH",
            "risk_level": "LOW"
        }

    # =====================================================
    # REPORT STATUS
    # =====================================================

    if (
        "report" in query
        or "reports" in query
        or "show reports" in query
        or "generated reports" in query
        or "daily report" in query
        or "health report" in query
    ):

        return {
            "intent": "REPORT_STATUS",
            "confidence": "HIGH",
            "risk_level": "LOW"
        }

    # =====================================================
    # DEFAULT GENERAL DBA QUERY
    # =====================================================

    return {
        "intent": "GENERAL_DBA_QUERY",
        "confidence": "LOW",
        "risk_level": "LOW"
    }