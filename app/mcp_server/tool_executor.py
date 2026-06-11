# =========================================================
# DBA Tool Executor
# Autonomous AI DBA Operations Platform
# =========================================================

from app.common.error_handler import (
    handle_error
)

from app.mcp_server.tool_registry import (
    get_tool_details
)

from app.monitoring.sql_monitor import (
    run_monitoring
)


# =========================================================
# EXECUTE SINGLE DBA TOOL
# =========================================================

def execute_tool(
    tool_name
):
    """
    Execute one DBA tool selected by the AI Agent.

    This executor does not decide what to run.
    The AI Agent Planner decides the plan.
    This executor only executes the approved registered DBA tool.
    """

    try:

        tool_details = get_tool_details(
            tool_name
        )

        print("\n========================================")
        print(" DBA TOOL EXECUTOR ")
        print("========================================\n")

        print(
            f"Tool Selected : {tool_name}"
        )

        print(
            f"Tool Name     : {tool_details['name']}"
        )

        print(
            f"Category      : {tool_details['category']}"
        )

        # =================================================
        # EXISTING SQL MONITORING ENGINE TOOLS
        # =================================================

        if tool_name in [
            "CHECK_CPU",
            "CHECK_BLOCKING",
            "CHECK_LONG_RUNNING_QUERIES"
        ]:

            result = run_monitoring()

            return {
                "tool": tool_name,
                "tool_name": tool_details["name"],
                "category": tool_details["category"],
                "risk": tool_details["risk"],
                "approval_required": tool_details[
                    "approval_required"
                ],
                "status": "EXECUTED",
                "result": result
            }

        # =================================================
        # DAY 16 REGISTERED TOOLS
        # These tools are registered now and will be
        # connected to dedicated monitoring modules next.
        # =================================================

        if tool_name == "CHECK_FAILED_JOBS":

            return {
                "tool": tool_name,
                "tool_name": tool_details["name"],
                "category": tool_details["category"],
                "risk": tool_details["risk"],
                "approval_required": tool_details[
                    "approval_required"
                ],
                "status": "PENDING_IMPLEMENTATION",
                "result": (
                    "Failed SQL job monitoring tool is registered "
                    "and ready for dedicated monitor integration."
                )
            }

        if tool_name == "CHECK_BACKUP_STATUS":

            return {
                "tool": tool_name,
                "tool_name": tool_details["name"],
                "category": tool_details["category"],
                "risk": tool_details["risk"],
                "approval_required": tool_details[
                    "approval_required"
                ],
                "status": "PENDING_IMPLEMENTATION",
                "result": (
                    "Backup status monitoring tool is registered "
                    "and ready for dedicated monitor integration."
                )
            }

        if tool_name == "CHECK_DATABASE_SPACE":

            return {
                "tool": tool_name,
                "tool_name": tool_details["name"],
                "category": tool_details["category"],
                "risk": tool_details["risk"],
                "approval_required": tool_details[
                    "approval_required"
                ],
                "status": "PENDING_IMPLEMENTATION",
                "result": (
                    "Database space monitoring tool is registered "
                    "and ready for dedicated monitor integration."
                )
            }

        if tool_name == "GENERATE_DAILY_HEALTH_REPORT":

            return {
                "tool": tool_name,
                "tool_name": tool_details["name"],
                "category": tool_details["category"],
                "risk": tool_details["risk"],
                "approval_required": tool_details[
                    "approval_required"
                ],
                "status": "PENDING_IMPLEMENTATION",
                "result": (
                    "Daily DBA health report generation will be "
                    "executed after all agentic tool results are collected."
                )
            }

        # =================================================
        # UNKNOWN TOOL
        # =================================================

        return {
            "tool": tool_name,
            "tool_name": tool_details["name"],
            "category": tool_details["category"],
            "risk": tool_details["risk"],
            "approval_required": tool_details[
                "approval_required"
            ],
            "status": "UNKNOWN_TOOL",
            "result": None
        }

    except Exception as error:

        return handle_error(
            "DBA TOOL EXECUTOR",
            error
        )


# =========================================================
# EXECUTE TOOL PLAN
# =========================================================

def execute_tool_plan(
    plan
):
    """
    Execute all DBA tools selected by the AI Agent Planner.
    """

    results = []

    print("\n========================================")
    print(" DBA TOOL PLAN EXECUTION STARTED ")
    print("========================================\n")

    for tool_name in plan:

        result = execute_tool(
            tool_name
        )

        results.append(
            result
        )

    print("\n========================================")
    print(" DBA TOOL PLAN EXECUTION COMPLETED ")
    print("========================================\n")

    return {
        "execution_status": "COMPLETED",
        "tools_requested": len(
            plan
        ),
        "tools_executed": len(
            results
        ),
        "results": results
    }


# =========================================================
# TEST EXECUTION
# =========================================================

if __name__ == "__main__":

    sample_plan = [
        "CHECK_CPU",
        "CHECK_BLOCKING",
        "CHECK_LONG_RUNNING_QUERIES",
        "CHECK_FAILED_JOBS",
        "CHECK_BACKUP_STATUS",
        "CHECK_DATABASE_SPACE",
        "GENERATE_DAILY_HEALTH_REPORT"
    ]

    result = execute_tool_plan(
        sample_plan
    )

    print("\n========================================")
    print(" DBA TOOL EXECUTION RESULT ")
    print("========================================\n")

    print(
        result
    )