# =========================================================
# Agent Planner
# Autonomous AI DBA Operations Platform
# =========================================================

def create_investigation_plan(
    intent_result
):
    """
    Create agentic DBA investigation plan based on detected intent.
    """

    intent = intent_result.get(
        "intent",
        "GENERAL_HEALTH_CHECK"
    )

    # =====================================================
    # DAILY DBA HEALTH CHECK
    # =====================================================

    if intent == "DAILY_HEALTH_CHECK":

        return [
            "CHECK_CPU",
            "CHECK_BLOCKING",
            "CHECK_LONG_RUNNING_QUERIES",
            "CHECK_FAILED_JOBS",
            "VALIDATE_RBAC_PERMISSION",
            "REQUEST_FAILED_JOB_RESTART_APPROVAL",
            "CHECK_BACKUP_STATUS",
            "CHECK_DATABASE_SPACE",
            "CHECK_INDEX_FRAGMENTATION",
            "CHECK_STATISTICS_HEALTH",
            "GENERATE_PERFORMANCE_TUNING_REPORT",
            "GENERATE_DAILY_HEALTH_REPORT",
            "SEND_TO_AZURE_MONITOR",
            "CREATE_AZURE_AUTOMATION_RUNBOOK_REQUEST"
        ]

    # =====================================================
    # FAILED SQL JOB CHECK
    # =====================================================

    if intent == "FAILED_JOB_CHECK":

        return [
            "CHECK_FAILED_JOBS",
            "VALIDATE_RBAC_PERMISSION",
            "REQUEST_FAILED_JOB_RESTART_APPROVAL",
            "CREATE_AZURE_AUTOMATION_RUNBOOK_REQUEST"
        ]

    # =====================================================
    # BACKUP HEALTH CHECK
    # =====================================================

    if intent == "BACKUP_HEALTH_CHECK":

        return [
            "CHECK_BACKUP_STATUS",
            "SEND_TO_AZURE_MONITOR"
        ]

    # =====================================================
    # BLOCKING ANALYSIS
    # =====================================================

    if intent == "BLOCKING_ANALYSIS":

        return [
            "CHECK_BLOCKING",
            "CHECK_LONG_RUNNING_QUERIES",
            "SEND_TO_AZURE_MONITOR"
        ]

    # =====================================================
    # PERFORMANCE ANALYSIS
    # =====================================================

    if intent == "PERFORMANCE_ANALYSIS":

        return [
            "CHECK_CPU",
            "CHECK_LONG_RUNNING_QUERIES",
            "CHECK_BLOCKING",
            "CHECK_INDEX_FRAGMENTATION",
            "CHECK_STATISTICS_HEALTH",
            "GENERATE_PERFORMANCE_TUNING_REPORT",
            "SEND_TO_AZURE_MONITOR"
        ]

    # =====================================================
    # SPACE ANALYSIS
    # =====================================================

    if intent == "SPACE_ANALYSIS":

        return [
            "CHECK_DATABASE_SPACE",
            "SEND_TO_AZURE_MONITOR"
        ]

    # =====================================================
    # DEFAULT GENERAL HEALTH CHECK
    # =====================================================

    return [
        "CHECK_CPU",
        "CHECK_BLOCKING",
        "CHECK_LONG_RUNNING_QUERIES",
        "CHECK_DATABASE_SPACE",
        "SEND_TO_AZURE_MONITOR"
    ]


# =========================================================
# TEST EXECUTION
# =========================================================

if __name__ == "__main__":

    sample_intent = {
        "intent": "DAILY_HEALTH_CHECK",
        "confidence": 95
    }

    plan = create_investigation_plan(
        sample_intent
    )

    print("\n========================================")
    print(" AGENT INVESTIGATION PLAN ")
    print("========================================\n")

    print(
        plan
    )