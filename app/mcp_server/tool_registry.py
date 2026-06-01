# =========================================================
# MCP Tool Registry
# Autonomous AI DBA Operations Platform
# =========================================================

# =========================================================
# REGISTERED TOOLS
# =========================================================

REGISTERED_TOOLS = {

    "monitoring_tool": {
        "description": "Central SQL Monitoring Engine",
        "status": "Implemented"
    },

    "ai_analysis_tool": {
        "description": "AI DBA Agent",
        "status": "Implemented"
    },

    "report_tool": {
        "description": "Incident Report Generator",
        "status": "Implemented"
    },

    "notification_tool": {
        "description": "Notification Engine",
        "status": "Planned"
    }
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

    for tool_name, tool_info in REGISTERED_TOOLS.items():

        print(
            f"{tool_name} -> "
            f"{tool_info['description']} "
            f"[{tool_info['status']}]"
        )


# =========================================================
# TEST EXECUTION
# =========================================================

if __name__ == "__main__":

    display_registered_tools()