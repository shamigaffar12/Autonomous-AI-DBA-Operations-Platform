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
        "approval_required": tool_details["approval_required"],
        "status": status,
        "result": result
    }


# =========================================================
# BUILD HEALTH SUMMARY FOR AZURE MONITOR
# =========================================================

def build_azure_health_summary(results):
    """
    Build DBA health summary payload for Azure Monitor adapter.
    """

    issues_detected = []
    overall_status = "HEALTHY"

    for item in results:

        result = item.get(
            "result",
            {}
        )

        if not isinstance(result, dict):
            continue

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
            "ACCESS_DENIED",
            "WAITING_FOR_APPROVAL",
            "REMEDIATION_BLOCKED",
            "NO_FAILED_JOB_DATA",
            "NO_RBAC_DATA"
        ]:

            overall_status = "ATTENTION REQUIRED"

            if message:
                issues_detected.append(message)

    return {
        "source": "Autonomous-AI-DBA-Operations-Platform",
        "database": "AdventureWorks2019",
        "overall_status": overall_status,
        "issues_detected": issues_detected,
        "tools_executed": len(results)
    }


# =========================================================
# GET PREVIOUS TOOL RESULT
# =========================================================

def get_previous_tool_result(results, tool_name):
    """
    Return previous result from already executed tool list.
    """

    for item in results:

        if item.get("tool") == tool_name:

            return item.get("result")

    return None


# =========================================================
# GET AUTOMATION ACTION FOR AZURE RUNBOOK
# =========================================================

def get_automation_action_from_results(results):
    """
    Get failed job restart approval action from previous results.

    Important:
    Azure Automation must not create a runbook request while approval is pending.
    """

    for item in results:

        if item.get("tool") == "REQUEST_FAILED_JOB_RESTART_APPROVAL":

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
        "approval_status": "NOT_AVAILABLE",
        "message": "No automation approval action found.",
        "risk": "LOW"
    }


# =========================================================
# CHECK APPROVAL STATUS FOR AUTOMATION
# =========================================================

def evaluate_automation_approval_status(automation_action):
    """
    Decide whether Azure Automation is allowed to proceed.

    Rules:
    - APPROVED: allow runbook request creation
    - PENDING_APPROVAL: block and wait
    - REJECTED: block remediation
    - Anything else: block safely
    """

    approval_status = str(
        automation_action.get(
            "approval_status",
            "NOT_AVAILABLE"
        )
    ).upper()

    if approval_status == "APPROVED":

        return {
            "can_create_runbook": True,
            "overall_status": "APPROVED_FOR_AUTOMATION",
            "message": "Approval completed. Azure Automation runbook request can be created."
        }

    if approval_status == "PENDING_APPROVAL":

        return {
            "can_create_runbook": False,
            "overall_status": "WAITING_FOR_APPROVAL",
            "message": "Azure Automation runbook request is blocked until approval is completed."
        }

    if approval_status == "REJECTED":

        return {
            "can_create_runbook": False,
            "overall_status": "REMEDIATION_BLOCKED",
            "message": "Azure Automation runbook request blocked because remediation was rejected."
        }

    return {
        "can_create_runbook": False,
        "overall_status": "AUTOMATION_BLOCKED",
        "message": "Azure Automation runbook request blocked because approval status is unavailable or invalid."
    }


# =========================================================
# EXECUTE SINGLE DBA TOOL
# =========================================================

def execute_tool(tool_name):
    """
    Execute one DBA tool selected by the AI Agent.

    This function handles independent tools.
    Tools that depend on previous results are handled inside execute_tool_plan().
    """

    try:

        tool_details = get_tool_details(
            tool_name
        )

        print("\n========================================")
        print(" DBA TOOL EXECUTOR ")
        print("========================================\n")

        print(f"Tool Selected : {tool_name}")
        print(f"Tool Name     : {tool_details['name']}")
        print(f"Category      : {tool_details['category']}")

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

        if tool_name == "REQUEST_FAILED_JOB_RESTART_APPROVAL":

            return build_tool_response(
                tool_name,
                tool_details,
                "WAITING_FOR_FAILED_JOB_AND_RBAC_RESULTS",
                {
                    "overall_status": "WAITING",
                    "message": (
                        "Failed job restart approval requires failed job "
                        "monitoring result and RBAC validation result."
                    )
                }
            )

        if tool_name == "GENERATE_PERFORMANCE_TUNING_REPORT":

            return build_tool_response(
                tool_name,
                tool_details,
                "WAITING_FOR_TOOL_RESULTS",
                {
                    "overall_status": "WAITING",
                    "message": (
                        "Performance tuning report will be generated after "
                        "performance tool results are collected."
                    )
                }
            )

        if tool_name == "GENERATE_DAILY_HEALTH_REPORT":

            return build_tool_response(
                tool_name,
                tool_details,
                "WAITING_FOR_TOOL_RESULTS",
                {
                    "overall_status": "WAITING",
                    "message": (
                        "Daily DBA health report will be generated after "
                        "all tool results are collected."
                    )
                }
            )

        if tool_name == "SEND_TO_AZURE_MONITOR":

            return build_tool_response(
                tool_name,
                tool_details,
                "WAITING_FOR_HEALTH_SUMMARY",
                {
                    "overall_status": "WAITING",
                    "message": (
                        "Azure Monitor payload will be prepared after "
                        "health results are collected."
                    )
                }
            )

        if tool_name == "CREATE_AZURE_AUTOMATION_RUNBOOK_REQUEST":

            return build_tool_response(
                tool_name,
                tool_details,
                "WAITING_FOR_APPROVAL_STATUS",
                {
                    "overall_status": "WAITING",
                    "message": (
                        "Azure Automation request will be evaluated after "
                        "approval status is checked."
                    )
                }
            )

        return build_tool_response(
            tool_name,
            tool_details,
            "UNKNOWN_TOOL",
            {
                "overall_status": "UNKNOWN_TOOL",
                "message": f"Tool {tool_name} is not mapped in Tool Executor."
            }
        )

    except Exception as error:

        return handle_error(
            "DBA TOOL EXECUTOR",
            error
        )


# =========================================================
# EXECUTE FAILED JOB APPROVAL WORKFLOW
# =========================================================

def execute_failed_job_restart_approval(results, tool_name):
    """
    Create failed job restart approval only after:
    1. Failed job result is available
    2. RBAC validation result is available
    3. RBAC is not denied
    """

    tool_details = get_tool_details(
        tool_name
    )

    failed_job_result = get_previous_tool_result(
        results,
        "CHECK_FAILED_JOBS"
    )

    rbac_result = get_previous_tool_result(
        results,
        "VALIDATE_RBAC_PERMISSION"
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

    elif rbac_result.get("overall_status") == "ACCESS_DENIED":

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

        automation_result["rbac_status"] = rbac_result.get(
            "overall_status"
        )

        automation_result["rbac_message"] = rbac_result.get(
            "message"
        )

    return build_tool_response(
        tool_name,
        tool_details,
        "EXECUTED",
        automation_result
    )


# =========================================================
# EXECUTE PERFORMANCE TUNING REPORT
# =========================================================

def execute_performance_report(results, tool_name):
    """
    Generate performance tuning report using all previous monitoring results.
    """

    tool_details = get_tool_details(
        tool_name
    )

    report_result = generate_performance_tuning_report(
        {
            "results": results
        }
    )

    return build_tool_response(
        tool_name,
        tool_details,
        "EXECUTED",
        report_result
    )


# =========================================================
# EXECUTE DAILY HEALTH REPORT
# =========================================================

def execute_daily_health_report(results, tool_name):
    """
    Generate daily DBA health report using all previous tool results.
    """

    tool_details = get_tool_details(
        tool_name
    )

    report_result = generate_daily_health_report(
        {
            "results": results
        }
    )

    return build_tool_response(
        tool_name,
        tool_details,
        "EXECUTED",
        report_result
    )


# =========================================================
# EXECUTE AZURE MONITOR ADAPTER
# =========================================================

def execute_azure_monitor(results, tool_name):
    """
    Send simulated DBA health payload to Azure Monitor adapter.
    """

    tool_details = get_tool_details(
        tool_name
    )

    health_summary = build_azure_health_summary(
        results
    )

    azure_monitor_result = send_health_summary_to_azure_monitor(
        health_summary
    )

    return build_tool_response(
        tool_name,
        tool_details,
        "EXECUTED",
        azure_monitor_result
    )


# =========================================================
# EXECUTE AZURE AUTOMATION ADAPTER
# =========================================================

def execute_azure_automation(results, tool_name):
    """
    Create Azure Automation runbook request only after approval.

    Security rule:
    - If approval is pending, do not create runbook request.
    - If approval is rejected, block remediation.
    - If approval is approved, create runbook request.
    """

    tool_details = get_tool_details(
        tool_name
    )

    automation_action = get_automation_action_from_results(
        results
    )

    approval_decision = evaluate_automation_approval_status(
        automation_action
    )

    if not approval_decision["can_create_runbook"]:

        blocked_result = {
            "overall_status": approval_decision["overall_status"],
            "adapter_name": "AZURE_AUTOMATION_ADAPTER",
            "message": approval_decision["message"],
            "integration_mode": "SIMULATED",
            "approval_required": True,
            "runbook_request_created": False,
            "automation_action": automation_action
        }

        print("\n========================================")
        print(" Azure Automation Adapter ")
        print("========================================\n")
        print("Target Service    : Azure Automation")
        print("Mode              : SIMULATED")
        print("Approval Required : True")
        print(f"Status            : {approval_decision['overall_status']}")
        print(f"Message           : {approval_decision['message']}")

        return build_tool_response(
            tool_name,
            tool_details,
            "BLOCKED",
            blocked_result
        )

    azure_automation_result = create_azure_automation_runbook_request(
        automation_action
    )

    azure_automation_result["approval_status"] = automation_action.get(
        "approval_status"
    )

    azure_automation_result["runbook_request_created"] = True

    return build_tool_response(
        tool_name,
        tool_details,
        "EXECUTED",
        azure_automation_result
    )


# =========================================================
# EXECUTE TOOL PLAN
# =========================================================

def execute_tool_plan(plan):
    """
    Execute all DBA tools selected by the AI Agent Planner.

    This function is responsible for:
    - Executing independent monitoring tools
    - Enforcing RBAC before remediation approval
    - Creating approval request before automation
    - Blocking Azure Automation until approval is approved
    - Generating reports after monitoring tools complete
    - Sending summary to Azure Monitor adapter
    """

    results = []

    print("\n========================================")
    print(" DBA TOOL PLAN EXECUTION STARTED ")
    print("========================================\n")

    for tool_name in plan:

        if tool_name == "REQUEST_FAILED_JOB_RESTART_APPROVAL":

            result = execute_failed_job_restart_approval(
                results,
                tool_name
            )

            results.append(result)
            continue

        if tool_name == "GENERATE_PERFORMANCE_TUNING_REPORT":

            result = execute_performance_report(
                results,
                tool_name
            )

            results.append(result)
            continue

        if tool_name == "GENERATE_DAILY_HEALTH_REPORT":

            result = execute_daily_health_report(
                results,
                tool_name
            )

            results.append(result)
            continue

        if tool_name == "SEND_TO_AZURE_MONITOR":

            result = execute_azure_monitor(
                results,
                tool_name
            )

            results.append(result)
            continue

        if tool_name == "CREATE_AZURE_AUTOMATION_RUNBOOK_REQUEST":

            result = execute_azure_automation(
                results,
                tool_name
            )

            results.append(result)
            continue

        result = execute_tool(
            tool_name
        )

        results.append(result)

    print("\n========================================")
    print(" DBA TOOL PLAN EXECUTION COMPLETED ")
    print("========================================\n")

    return {
        "execution_status": "COMPLETED",
        "tools_requested": len(plan),
        "tools_executed": len(results),
        "results": results
    }


# =========================================================
# TEST EXECUTION
# =========================================================

if __name__ == "__main__":

    from app.ai_agent.agent_planner import (
        generate_agent_investigation_plan
    )

    sample_plan = generate_agent_investigation_plan()

    print("\n========================================")
    print(" AGENT GENERATED TOOL PLAN ")
    print("========================================\n")

    for tool in sample_plan:
        print(f"- {tool}")

    result = execute_tool_plan(
        sample_plan
    )

    print("\n========================================")
    print(" DBA TOOL EXECUTION RESULT ")
    print("========================================\n")

    print(result)