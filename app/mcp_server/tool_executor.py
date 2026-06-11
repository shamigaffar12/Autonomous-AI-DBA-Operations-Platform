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

from app.monitoring.failed_jobs_monitor import (
    check_failed_jobs
)

from app.monitoring.backup_status_monitor import (
    check_backup_status
)

from app.monitoring.database_space_monitor import (
    check_database_space
)

from app.monitoring.fragmentation_monitor import (
    check_index_fragmentation
)

from app.monitoring.statistics_monitor import (
    check_statistics_health
)

from app.reporting.performance_tuning_report_generator import (
    generate_performance_tuning_report
)

from app.reporting.daily_health_report_generator import (
    generate_daily_health_report
)


# =========================================================
# BUILD EXECUTION RESPONSE
# =========================================================

def build_tool_response(
    tool_name,
    tool_details,
    status,
    result
):
    """
    Build common tool execution response.
    """

    return {
        "tool": tool_name,
        "tool_name": tool_details["name"],
        "category": tool_details["category"],
        "risk": tool_details["risk"],
        "approval_required": tool_details[
            "approval_required"
        ],
        "status": status,
        "result": result
    }


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

            return build_tool_response(
                tool_name,
                tool_details,
                "EXECUTED",
                result
            )

        # =================================================
        # FAILED SQL JOB MONITOR
        # =================================================

        if tool_name == "CHECK_FAILED_JOBS":

            result = check_failed_jobs()

            return build_tool_response(
                tool_name,
                tool_details,
                "EXECUTED",
                result
            )

        # =================================================
        # BACKUP STATUS MONITOR
        # =================================================

        if tool_name == "CHECK_BACKUP_STATUS":

            result = check_backup_status()

            return build_tool_response(
                tool_name,
                tool_details,
                "EXECUTED",
                result
            )

        # =================================================
        # DATABASE SPACE MONITOR
        # =================================================

        if tool_name == "CHECK_DATABASE_SPACE":

            result = check_database_space()

            return build_tool_response(
                tool_name,
                tool_details,
                "EXECUTED",
                result
            )

        # =================================================
        # INDEX FRAGMENTATION MONITOR
        # =================================================

        if tool_name == "CHECK_INDEX_FRAGMENTATION":

            result = check_index_fragmentation()

            return build_tool_response(
                tool_name,
                tool_details,
                "EXECUTED",
                result
            )

        # =================================================
        # STATISTICS HEALTH MONITOR
        # =================================================

        if tool_name == "CHECK_STATISTICS_HEALTH":

            result = check_statistics_health()

            return build_tool_response(
                tool_name,
                tool_details,
                "EXECUTED",
                result
            )

        # =================================================
        # PERFORMANCE TUNING REPORT
        # Report generation is handled inside execute_tool_plan()
        # after performance tool results are collected.
        # =================================================

        if tool_name == "GENERATE_PERFORMANCE_TUNING_REPORT":

            return build_tool_response(
                tool_name,
                tool_details,
                "WAITING_FOR_TOOL_RESULTS",
                (
                    "Performance tuning report will be generated "
                    "after performance tool results are collected."
                )
            )

        # =================================================
        # DAILY HEALTH REPORT
        # Report generation is handled inside execute_tool_plan()
        # after all previous tool results are collected.
        # =================================================

        if tool_name == "GENERATE_DAILY_HEALTH_REPORT":

            return build_tool_response(
                tool_name,
                tool_details,
                "WAITING_FOR_TOOL_RESULTS",
                (
                    "Daily DBA health report will be generated "
                    "after all tool results are collected."
                )
            )

        # =================================================
        # UNKNOWN TOOL
        # =================================================

        return build_tool_response(
            tool_name,
            tool_details,
            "UNKNOWN_TOOL",
            None
        )

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

        # =================================================
        # PERFORMANCE TUNING REPORT
        # Must run after fragmentation/statistics results.
        # =================================================

        if tool_name == "GENERATE_PERFORMANCE_TUNING_REPORT":

            tool_details = get_tool_details(
                tool_name
            )

            report_result = generate_performance_tuning_report(
                {
                    "results": results
                }
            )

            results.append(
                build_tool_response(
                    tool_name,
                    tool_details,
                    "EXECUTED",
                    report_result
                )
            )

            continue

        # =================================================
        # DAILY HEALTH REPORT
        # Must run after all previous tool results.
        # =================================================

        if tool_name == "GENERATE_DAILY_HEALTH_REPORT":

            tool_details = get_tool_details(
                tool_name
            )

            report_result = generate_daily_health_report(
                {
                    "results": results
                }
            )

            results.append(
                build_tool_response(
                    tool_name,
                    tool_details,
                    "EXECUTED",
                    report_result
                )
            )

            continue

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
        "CHECK_INDEX_FRAGMENTATION",
        "CHECK_STATISTICS_HEALTH",
        "GENERATE_PERFORMANCE_TUNING_REPORT",
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