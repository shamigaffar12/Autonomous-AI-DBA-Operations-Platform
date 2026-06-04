# =========================================================
# MCP Tool Registry
# Autonomous AI DBA Operations Platform
# =========================================================

from app.mcp_server.monitoring_executor import (
    run_monitoring
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

# =========================================================
# REGISTERED TOOLS
# =========================================================

REGISTERED_TOOLS = {

    "monitoring_tool": {

        "description": "Central SQL Monitoring Engine",

        "status": "Implemented",

        "executor": run_monitoring
    },

    "ai_analysis_tool": {

        "description": "AI DBA Agent",

        "status": "Implemented",

        "executor": run_ai_analysis
    },

    "report_tool": {

        "description": "Incident Report Generator",

        "status": "Implemented",

        "executor": save_report
    },

    "notification_tool": {

        "description": "Notification Engine",

        "status": "Implemented",

        "executor": run_notifications
    }
}


# =========================================================
# GET TOOL
# =========================================================

def get_tool(tool_name):

    return REGISTERED_TOOLS.get(tool_name)


# =========================================================
# DISPLAY REGISTERED TOOLS
# =========================================================

def display_registered_tools():

    print("\n========================================")

    print(" MCP REGISTERED TOOLS ")

    print("========================================\n")

    for tool_name, tool_info in REGISTERED_TOOLS.items():

        print(
            f"{tool_name} -> "
            f"{tool_info['description']} "
            f"[{tool_info['status']}]"
        )


# =========================================================
# TEST TOOL LOADING
# =========================================================

def test_tool_loading():

    print("\n========================================")

    print(" TOOL LOADING TEST ")

    print("========================================\n")

    for tool_name in REGISTERED_TOOLS:

        tool = get_tool(tool_name)

        print(
            f"Loaded Tool : {tool['description']}"
        )


# =========================================================
# TEST EXECUTION
# =========================================================

if __name__ == "__main__":

    display_registered_tools()

    test_tool_loading()