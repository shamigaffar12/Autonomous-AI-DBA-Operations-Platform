# =========================================================
# Workflow Manager
# Autonomous AI DBA Operations Platform
# =========================================================

# =========================================================
# IMPORTS
# =========================================================

from app.common.environment_validator import (
    validate_environment
)

from app.mcp_server.monitoring_executor import (
    execute_monitoring
)

from app.mcp_server.ai_executor import (
    run_ai_analysis
)

from app.mcp_server.report_executor import (
    save_report
)

from app.mcp_server.notification_executor import (
    run_notifications
)

from app.repository.incident_repository import (
    save_incident
)

from app.governance.governance_executor import (
    create_governance_request
)

from app.audit.audit_logger import (
    write_audit_log
)

from app.common.error_handler import (
    handle_error
)


# =========================================================
# WORKFLOW STEPS
# =========================================================

WORKFLOW_STEPS = [

    "Environment Validation",

    "Run Monitoring Engine",

    "Collect Monitoring Results",

    "Send Incident To AI Agent",

    "Governance Review",

    "Generate RCA Report",

    "Save Incident To Repository",

    "Send Notifications",

    "Save Incident Report"
]


# =========================================================
# DISPLAY WORKFLOW
# =========================================================

def display_workflow_steps():

    """
    Display workflow execution steps.
    """

    print("\n========================================")

    print(" MCP WORKFLOW EXECUTION ")

    print("========================================\n")

    for step_number, step in enumerate(

        WORKFLOW_STEPS,

        start=0

    ):

        print(
            f"{step_number}. {step}"
        )


# =========================================================
# EXECUTE WORKFLOW
# =========================================================

def execute_workflow():

    """
    Execute complete MCP workflow.
    """

    try:

        # =================================================
        # WORKFLOW START
        # =================================================

        write_audit_log(
            "WORKFLOW STARTED"
        )

        print("\n========================================")

        print(" EXECUTING MCP WORKFLOW ")

        print("========================================\n")

        approval_request = None

        # =================================================
        # STEP 0 - ENVIRONMENT VALIDATION
        # =================================================

        write_audit_log(
            "STEP 0 STARTED - Environment Validation"
        )

        print(
            "[STEP 0] Environment Validation"
        )

        validate_environment()

        write_audit_log(
            "STEP 0 COMPLETED - Environment Validation"
        )

        # =================================================
        # STEP 1 - MONITORING
        # =================================================

        write_audit_log(
            "STEP 1 STARTED - Monitoring Engine"
        )

        print(
            "\n[STEP 1] Run Monitoring Engine"
        )

        monitoring_result = execute_monitoring()

        write_audit_log(
            "STEP 1 COMPLETED - Monitoring Engine"
        )

        # =================================================
        # STEP 2 - COLLECT RESULTS
        # =================================================

        write_audit_log(
            "STEP 2 STARTED - Collect Monitoring Results"
        )

        print(
            "\n[STEP 2] Collect Monitoring Results"
        )

        print(
            "Monitoring results collected successfully."
        )

        write_audit_log(
            "STEP 2 COMPLETED - Collect Monitoring Results"
        )

        # =================================================
        # STEP 3 - AI ANALYSIS
        # =================================================

        write_audit_log(
            "STEP 3 STARTED - AI Analysis"
        )

        print(
            "\n[STEP 3] Send Incident To AI Agent"
        )

        ai_result = run_ai_analysis(

            monitoring_result[
                "incident_summary"
            ]

        )

        write_audit_log(
            "STEP 3 COMPLETED - AI Analysis"
        )

        # =================================================
        # STEP 4 - GOVERNANCE REVIEW
        # =================================================

        write_audit_log(
            "STEP 4 STARTED - Governance Review"
        )

        print(
            "\n[STEP 4] Governance Review"
        )

        if (

            monitoring_result[
                "overall_status"
            ].upper()

            !=

            "HEALTHY"

        ):

            approval_request = (

                create_governance_request(

                    ai_result[
                        "analysis"
                    ]

                )

            )

            write_audit_log(

                f"GOVERNANCE REQUEST ID: "
                f"{approval_request['request_id']}"

            )

        else:

            print(
                "No governance approval required."
            )

            write_audit_log(
                "GOVERNANCE REVIEW SKIPPED - HEALTHY"
            )

        write_audit_log(
            "STEP 4 COMPLETED - Governance Review"
        )

        # =================================================
        # STEP 5 - REPORT GENERATION
        # =================================================

        write_audit_log(
            "STEP 5 STARTED - Report Generation"
        )

        print(
            "\n[STEP 5] Generate RCA Report"
        )

        report_file = save_report(

            monitoring_result[
                "overall_status"
            ],

            monitoring_result[
                "incident_summary"
            ],

            ai_result[
                "analysis"
            ]

        )

        write_audit_log(
            "STEP 5 COMPLETED - Report Generation"
        )

        write_audit_log(
            f"REPORT FILE CREATED: {report_file}"
        )

        # =================================================
        # STEP 6 - INCIDENT REPOSITORY
        # =================================================

        write_audit_log(
            "STEP 6 STARTED - Incident Repository"
        )

        print(
            "\n[STEP 6] Save Incident To Repository"
        )

        save_incident(

            monitoring_result[
                "overall_status"
            ],

            monitoring_result[
                "incident_summary"
            ],

            ai_result[
                "analysis"
            ],

            report_file

        )

        write_audit_log(
            "STEP 6 COMPLETED - Incident Repository"
        )

        # =================================================
        # STEP 7 - NOTIFICATIONS
        # =================================================

        write_audit_log(
            "STEP 7 STARTED - Notifications"
        )

        print(
            "\n[STEP 7] Send Notifications"
        )

        run_notifications(

            monitoring_result[
                "overall_status"
            ],

            monitoring_result[
                "incident_summary"
            ]

        )

        write_audit_log(
            "STEP 7 COMPLETED - Notifications"
        )

        # =================================================
        # STEP 8 - SAVE REPORT
        # =================================================

        write_audit_log(
            "STEP 8 STARTED - Save Report"
        )

        print(
            "\n[STEP 8] Save Incident Report"
        )

        print(
            f"Report saved successfully: {report_file}"
        )

        write_audit_log(
            "STEP 8 COMPLETED - Save Report"
        )

        # =================================================
        # WORKFLOW COMPLETED
        # =================================================

        write_audit_log(
            "WORKFLOW COMPLETED"
        )

        print("\n========================================")

        print(" MCP WORKFLOW COMPLETED ")

        print("========================================\n")

        return {

            "status": "SUCCESS",

            "overall_status":
            monitoring_result[
                "overall_status"
            ],

            "report_file":
            report_file,

            "approval_request":
            approval_request

        }

    except Exception as error:

        return handle_error(

            "WORKFLOW MANAGER",

            error

        )


# =========================================================
# GET WORKFLOW STEPS
# =========================================================

def get_workflow_steps():

    """
    Return workflow steps.
    """

    return WORKFLOW_STEPS


# =========================================================
# WORKFLOW SUMMARY
# =========================================================

def workflow_summary():

    """
    Display workflow summary.
    """

    print("\n========================================")

    print(" WORKFLOW SUMMARY ")

    print("========================================\n")

    print(
        f"Total Workflow Steps : {len(WORKFLOW_STEPS)}"
    )

    print(
        "Workflow Status      : Active"
    )

    print(
        "Environment Check    : Enabled"
    )

    print(
        "Governance Layer     : Enabled"
    )


# =========================================================
# TEST EXECUTION
# =========================================================

if __name__ == "__main__":

    display_workflow_steps()

    execute_workflow()

    workflow_summary()