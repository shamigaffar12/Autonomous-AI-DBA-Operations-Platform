# =========================================================
# MCP Tool Registry
# Autonomous AI DBA Operations Platform
# =========================================================


# =========================================================
# REGISTERED TOOLS
# =========================================================

REGISTERED_TOOLS = {

    "monitoring_tool":

        "Central SQL Monitoring Engine",


    "ai_analysis_tool":

        "AI DBA Agent",


    "report_tool":

        "Incident Report Generator",


    "notification_tool":

        "Notification Engine (Future)"
}


# =========================================================
# DISPLAY REGISTERED TOOLS
# =========================================================

def display_registered_tools():

    """
    Display registered MCP tools.
    """


    print("\n========================================")

    print(" MCP REGISTERED TOOLS ")

    print("========================================\n")


    for tool_name, description in (

        REGISTERED_TOOLS.items()

    ):

        print(

            f"{tool_name} -> {description}"

        )