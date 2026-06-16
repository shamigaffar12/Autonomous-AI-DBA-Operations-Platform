# =========================================================
# Agent Planner
# Autonomous AI DBA Operations Platform
# =========================================================


# =========================================================
# FULL STANDARD TOOL PLAN
# =========================================================

def generate_agent_investigation_plan():
    """
    Standard full DBA investigation plan used by the MCP Tool Executor.

    Purpose:
    - Keeps Agent Planner, Tool Registry, and Tool Executor synchronized.
    - Ensures all currently implemented tools are included in the demo flow.
    - Supports monitoring, security validation, performance tuning,
      reporting, Azure Monitor, and Azure Automation request creation.

    Important:
    This planner only returns the tool plan.
    It does not execute any database operation.
    """

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
        "CREATE_AZURE_AUTOMATION_RUNBOOK_REQUEST",
    ]


# =========================================================
# INTENT-BASED INVESTIGATION PLAN
# =========================================================

def create_investigation_plan(intent_result):
    """
    Create agentic DBA investigation plan based on detected intent.

    Parameters:
        intent_result (dict): Intent classification output from AI agent.

    Returns:
        list: Ordered list of DBA tools to be executed by MCP Tool Executor.
    """

    intent = intent_result.get(
        "intent",
        "GENERAL_HEALTH_CHECK"
    )

    if intent == "DAILY_HEALTH_CHECK":

        return generate_agent_investigation_plan()

    if intent == "FAILED_JOB_CHECK":

        return [
            "CHECK_FAILED_JOBS",
            "VALIDATE_RBAC_PERMISSION",
            "REQUEST_FAILED_JOB_RESTART_APPROVAL",
            "CREATE_AZURE_AUTOMATION_RUNBOOK_REQUEST",
        ]

    if intent == "BACKUP_HEALTH_CHECK":

        return [
            "CHECK_BACKUP_STATUS",
            "SEND_TO_AZURE_MONITOR",
        ]

    if intent == "BLOCKING_ANALYSIS":

        return [
            "CHECK_BLOCKING",
            "CHECK_LONG_RUNNING_QUERIES",
            "SEND_TO_AZURE_MONITOR",
        ]

    if intent == "PERFORMANCE_ANALYSIS":

        return [
            "CHECK_CPU",
            "CHECK_LONG_RUNNING_QUERIES",
            "CHECK_BLOCKING",
            "CHECK_INDEX_FRAGMENTATION",
            "CHECK_STATISTICS_HEALTH",
            "GENERATE_PERFORMANCE_TUNING_REPORT",
            "SEND_TO_AZURE_MONITOR",
        ]

    if intent == "SPACE_ANALYSIS":

        return [
            "CHECK_DATABASE_SPACE",
            "SEND_TO_AZURE_MONITOR",
        ]

    if intent == "SECURITY_VALIDATION":

        return [
            "VALIDATE_RBAC_PERMISSION",
        ]

    if intent == "AZURE_MONITORING":

        return [
            "CHECK_CPU",
            "CHECK_BLOCKING",
            "CHECK_BACKUP_STATUS",
            "CHECK_DATABASE_SPACE",
            "SEND_TO_AZURE_MONITOR",
        ]

    if intent == "AZURE_AUTOMATION":

        return [
            "CHECK_FAILED_JOBS",
            "VALIDATE_RBAC_PERMISSION",
            "REQUEST_FAILED_JOB_RESTART_APPROVAL",
            "CREATE_AZURE_AUTOMATION_RUNBOOK_REQUEST",
        ]

    return [
        "CHECK_CPU",
        "CHECK_BLOCKING",
        "CHECK_LONG_RUNNING_QUERIES",
        "CHECK_FAILED_JOBS",
        "CHECK_BACKUP_STATUS",
        "CHECK_DATABASE_SPACE",
        "GENERATE_DAILY_HEALTH_REPORT",
        "SEND_TO_AZURE_MONITOR",
    ]


# =========================================================
# TEST EXECUTION
# =========================================================

if __name__ == "__main__":

    print("\n========================================")
    print(" AGENT INVESTIGATION PLAN ")
    print("========================================\n")

    sample_intent = {
        "intent": "DAILY_HEALTH_CHECK",
        "confidence": 95
    }

    plan = create_investigation_plan(
        sample_intent
    )

    print(plan)

    print("\n========================================")
    print(" TOOL COUNT ")
    print("========================================\n")

    print(f"Total Tools Planned: {len(plan)}")