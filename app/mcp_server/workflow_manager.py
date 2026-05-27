# =========================================================
# Workflow Manager
# Autonomous AI DBA Operations Platform
# =========================================================


# =========================================================
# WORKFLOW STEPS
# =========================================================

WORKFLOW_STEPS = [

    "Run Monitoring Engine",

    "Collect Monitoring Results",

    "Format Incident Data",

    "Send Incident To AI Agent",

    "Generate RCA Report",

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

        start=1
    ):

        print(

            f"{step_number}. {step}"

        )