# =========================================================
# Agentic DBA Workflow
# Autonomous AI DBA Operations Platform
# =========================================================

from app.ai_agent.intent_classifier import (
    classify_intent
)

from app.ai_agent.agent_planner import (
    create_investigation_plan
)

from app.mcp_server.tool_executor import (
    execute_tool_plan
)

from app.mcp_server.ai_executor import (
    run_ai_analysis
)

from app.audit.audit_logger import (
    write_audit_log
)

from app.common.error_handler import (
    handle_error
)


# =========================================================
# BUILD INCIDENT SUMMARY FROM TOOL RESULTS
# =========================================================

def build_incident_summary(
    user_command,
    intent_result,
    plan,
    tool_results
):
    """
    Build incident summary text for AI analysis.
    """

    summary = []

    summary.append(
        "Agentic DBA Workflow Execution Summary"
    )

    summary.append(
        f"User Command: {user_command}"
    )

    summary.append(
        f"Detected Intent: {intent_result['intent']}"
    )

    summary.append(
        f"Intent Confidence: {intent_result['confidence']}"
    )

    summary.append(
        "\nInvestigation Plan:"
    )

    for step in plan:

        summary.append(
            f"- {step}"
        )

    summary.append(
        "\nTool Execution Results:"
    )

    for result in tool_results.get(
        "results",
        []
    ):

        summary.append(
            f"- Tool: {result.get('tool')}"
        )

        summary.append(
            f"  Status: {result.get('status')}"
        )

        summary.append(
            f"  Result: {result.get('result')}"
        )

    return "\n".join(
        summary
    )


# =========================================================
# RUN AGENTIC DBA WORKFLOW
# =========================================================

def run_agentic_dba_workflow(
    user_command
):
    """
    Run complete agentic DBA workflow.
    """

    try:

        print("\n========================================")
        print(" AGENTIC DBA WORKFLOW STARTED ")
        print("========================================\n")

        write_audit_log(
            f"AGENTIC DBA WORKFLOW STARTED: {user_command}"
        )

        # =================================================
        # STEP 1: CLASSIFY INTENT
        # =================================================

        intent_result = classify_intent(
            user_command
        )

        # =================================================
        # STEP 2: CREATE INVESTIGATION PLAN
        # =================================================

        plan = create_investigation_plan(
            intent_result
        )

        # =================================================
        # STEP 3: EXECUTE DBA TOOLS
        # =================================================

        tool_results = execute_tool_plan(
            plan
        )

        # =================================================
        # STEP 4: BUILD INCIDENT SUMMARY
        # =================================================

        incident_summary = build_incident_summary(
            user_command,
            intent_result,
            plan,
            tool_results
        )

        # =================================================
        # STEP 5: RUN AI ANALYSIS
        # =================================================

        ai_result = run_ai_analysis(
            incident_summary
        )

        # =================================================
        # STEP 6: AUDIT COMPLETION
        # =================================================

        write_audit_log(
            f"AGENTIC DBA WORKFLOW COMPLETED: {intent_result['intent']}"
        )

        print("\n========================================")
        print(" AGENTIC DBA WORKFLOW COMPLETED ")
        print("========================================\n")

        return {
            "workflow_status": "COMPLETED",
            "user_command": user_command,
            "intent": intent_result,
            "plan": plan,
            "tool_results": tool_results,
            "incident_summary": incident_summary,
            "ai_result": ai_result
        }

    except Exception as error:

        return handle_error(
            "AGENTIC DBA WORKFLOW",
            error
        )


# =========================================================
# TEST EXECUTION
# =========================================================

if __name__ == "__main__":

    command = "Run daily DBA health check"

    result = run_agentic_dba_workflow(
        command
    )

    print("\n========================================")
    print(" FINAL AGENTIC WORKFLOW RESULT ")
    print("========================================\n")

    print(result)