# =========================================================
# AI Executor
# Autonomous AI DBA Operations Platform
# =========================================================

from app.ai_agent.agent import AIDBAgent

from app.common.error_handler import (
    handle_error
)

from app.common.custom_exception import (
    AIAnalysisException
)


# =========================================================
# EXECUTE AI ANALYSIS WORKFLOW
# =========================================================

def run_ai_analysis(
    incident_summary
):

    """
    Execute AI Analysis Workflow.
    """

    try:

        print(
            "\nStarting AI Analysis Workflow...\n"
        )

        agent = AIDBAgent()

        ai_result = agent.analyze_incident(
            incident_summary
        )

        if ai_result is None:

            raise AIAnalysisException(
                "AI analysis returned no response."
            )

        print(
            "\nAI Analysis Completed.\n"
        )

        return ai_result

    except Exception as error:

        return handle_error(
            "AI EXECUTOR",
            error
        )


# =========================================================
# TEST EXECUTION
# =========================================================

if __name__ == "__main__":

    sample_incident = """

    SQL Monitoring Summary

    Blocking Sessions Detected

    Session ID: 52
    Blocking Session ID: 67

    Overall Status: ATTENTION REQUIRED

    """

    result = run_ai_analysis(
        sample_incident
    )

    print("\n========================================")
    print(" AI ANALYSIS RESULT ")
    print("========================================\n")

    print(result)