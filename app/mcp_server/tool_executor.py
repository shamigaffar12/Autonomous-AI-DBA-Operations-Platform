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

from app.security.rbac_validator import (
    validate_action_permission
)

from app.automation.failed_job_restart_automation import (
    request_failed_job_restart_approval
)

from app.reporting.performance_tuning_report_generator import (
    generate_performance_tuning_report
)

from app.reporting.daily_health_report_generator import (
    generate_daily_health_report
)

from app.azure_integration.azure_monitor_adapter import (
    send_health_summary_to_azure_monitor
)

from app.azure_integration.azure_automation_adapter import (
    create_azure_automation_runbook_request
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
# BUILD HEALTH SUMMARY FOR AZURE MONITOR
# =========================================================

def build_azure_health_summary(
    results
):
    """
    Build simple DBA health summary for Azure Monitor adapter.
    """

    issues_detected = []

    overall_status = "HEALTHY"

    for item in results:

        result = item.get(
            "result",
            {}
        )

        if isinstance(
            result,
            dict
        ):

            result_status = result.get(
                "overall_status"
            )

            message = result.get(
                "message"
            )

            if result_status in [
                "ATTENTION REQUIRED",
                "ERROR",
                "APPROVAL_REQUIRED",
                "ACCESS_DENIED"
            ]:

                overall_status = "ATTENTION REQUIRED"

                if message:

                    issues_detected.append(
                        message
                    )

    return {
        "source": "Autonomous-AI-DBA-Operations-Platform",
        "database": "AdventureWorks2019",
        "overall_status": overall_status,
        "issues_detected": issues_detected,
        "tools_executed": len(
            results
        )
    }


# =========================================================
# GET AUTOMATION ACTION FOR AZURE RUNBOOK
# =========================================================

def get_automation_action_from_results(
    results
):
    """
    Get failed job restart approval action from previous results.
    """

    for item in results:

        if item.get(
            "tool"
        ) == "REQUEST_FAILED_JOB_RESTART_APPROVAL":

            automation_result = item.get(
                "result",
                {}
            )

            restart_requests = automation_result.get(
                "restart_requests",
                []
            )

            if restart_requests:

                return restart_requests[0]

    return {
        "action": "NO_AUTOMATION_ACTION",
        "message": "No approved or pending automation action found.",
        "risk": "LOW"
    }


# =========================================================
# EXECUTE SINGLE DBA TOOL
# =========================================================

def execute_tool(
    tool_name
):
    """
    Execute one DBA tool selected by the AI Agent.
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

        if tool_name == "CHECK_FAILED_JOBS":

            result = check_failed_jobs()

            return build_tool_response(
                tool_name,
                tool_details,
                "EXECUTED",
                result
            )

        if tool_name == "VALIDATE_RBAC_PERMISSION":

            result = validate_action_permission(
                user_role="DBA",
                action_name="RESTART_SQL_AGENT_JOB",
                risk_level="MEDIUM"
            )

            return build_tool_response(
                tool_name,
                tool_details,
                "EXECUTED",
                result
            )

        if tool_name == "REQUEST_FAILED_JOB_RESTART_APPROVAL":

            return build_tool_response(
                tool_name,
                tool_details,
                "WAITING_FOR_FAILED_JOB_AND_RBAC_RESULTS",
                (
                    "Failed job restart approval will be created "
                    "after failed job monitoring and RBAC validation "
                    "results are collected."
                )
            )

        if tool_name == "CHECK_BACKUP_STATUS":

            result = check_backup_status()

            return build_tool_response(
                tool_name,
                tool_details,
                "EXECUTED",
                result
            )

        if tool_name == "CHECK_DATABASE_SPACE":

            result = check_database_space()

            return build_tool_response(
                tool_name,
                tool_details,
                "EXECUTED",
                result
            )

        if tool_name == "CHECK_INDEX_FRAGMENTATION":

            result = check_index_fragmentation()

            return build_tool_response(
                tool_name,
                tool_details,
                "EXECUTED",
                result
            )

        if tool_name == "CHECK_STATISTICS_HEALTH":

            result = check_statistics_health()

            return build_tool_response(
                tool_name,
                tool_details,
                "EXECUTED",
                result
            )

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

        if tool_name == "SEND_TO_AZURE_MONITOR":

            return build_tool_response(
                tool_name,
                tool_details,
                "WAITING_FOR_HEALTH_SUMMARY",
                (
                    "Azure Monitor payload will be prepared "
                    "after health results are collected."
                )
            )

        if tool_name == "CREATE_AZURE_AUTOMATION_RUNBOOK_REQUEST":

            return build_tool_response(
                tool_name,
                tool_details,
                "WAITING_FOR_AUTOMATION_ACTION",
                (
                    "Azure Automation runbook request will be created "
                    "after automation action is prepared."
                )
            )

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
        # RBAC VALIDATION
        # =================================================

        if tool_name == "VALIDATE_RBAC_PERMISSION":

            tool_details = get_tool_details(
                tool_name
            )

            rbac_result = validate_action_permission(
                user_role="DBA",
                action_name="RESTART_SQL_AGENT_JOB",
                risk_level="MEDIUM"
            )

            results.append(
                build_tool_response(
                    tool_name,
                    tool_details,
                    "EXECUTED",
                    rbac_result
                )
            )

            continue

        # =================================================
        # FAILED JOB RESTART APPROVAL
        # =================================================

        if tool_name == "REQUEST_FAILED_JOB_RESTART_APPROVAL":

            tool_details = get_tool_details(
                tool_name
            )

            failed_job_result = None
            rbac_result = None

            for item in results:

                if item.get(
                    "tool"
                ) == "CHECK_FAILED_JOBS":

                    failed_job_result = item.get(
                        "result"
                    )

                if item.get(
                    "tool"
                ) == "VALIDATE_RBAC_PERMISSION":

                    rbac_result = item.get(
                        "result"
                    )

            if failed_job_result is None:

                automation_result = {
                    "overall_status": "NO_FAILED_JOB_DATA",
                    "automation_name": "FAILED_JOB_RESTART_APPROVAL",
                    "message": "Failed job monitoring result not found.",
                    "approval_required": False,
                    "restart_request_count": 0,
                    "restart_requests": []
                }

            elif rbac_result is None:

                automation_result = {
                    "overall_status": "NO_RBAC_DATA",
                    "automation_name": "FAILED_JOB_RESTART_APPROVAL",
                    "message": "RBAC validation result not found.",
                    "approval_required": True,
                    "restart_request_count": 0,
                    "restart_requests": []
                }

            elif rbac_result.get(
                "overall_status"
            ) == "ACCESS_DENIED":

                automation_result = {
                    "overall_status": "ACCESS_DENIED",
                    "automation_name": "FAILED_JOB_RESTART_APPROVAL",
                    "message": "Automation blocked due to RBAC access denial.",
                    "approval_required": True,
                    "restart_request_count": 0,
                    "restart_requests": []
                }

            else:

                automation_result = request_failed_job_restart_approval(
                    failed_job_result
                )

                automation_result[
                    "rbac_status"
                ] = rbac_result.get(
                    "overall_status"
                )

                automation_result[
                    "rbac_message"
                ] = rbac_result.get(
                    "message"
                )

            results.append(
                build_tool_response(
                    tool_name,
                    tool_details,
                    "EXECUTED",
                    automation_result
                )
            )

            continue

        # =================================================
        # PERFORMANCE TUNING REPORT
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

        # =================================================
        # AZURE MONITOR ADAPTER
        # =================================================

        if tool_name == "SEND_TO_AZURE_MONITOR":

            tool_details = get_tool_details(
                tool_name
            )

            health_summary = build_azure_health_summary(
                results
            )

            azure_monitor_result = send_health_summary_to_azure_monitor(
                health_summary
            )

            results.append(
                build_tool_response(
                    tool_name,
                    tool_details,
                    "EXECUTED",
                    azure_monitor_result
                )
            )

            continue

        # =================================================
        # AZURE AUTOMATION RUNBOOK REQUEST
        # =================================================

        if tool_name == "CREATE_AZURE_AUTOMATION_RUNBOOK_REQUEST":

            tool_details = get_tool_details(
                tool_name
            )

            automation_action = get_automation_action_from_results(
                results
            )

            azure_automation_result = create_azure_automation_runbook_request(
                automation_action
            )

            results.append(
                build_tool_response(
                    tool_name,
                    tool_details,
                    "EXECUTED",
                    azure_automation_result
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

    result = execute_tool_plan(
        sample_plan
    )

    print("\n========================================")
    print(" DBA TOOL EXECUTION RESULT ")
    print("========================================\n")

    print(
        result
    )