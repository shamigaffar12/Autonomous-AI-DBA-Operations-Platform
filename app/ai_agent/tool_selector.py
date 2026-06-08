# =========================================================
# Tool Selector
# =========================================================

def select_tool(

    task

):

    tool_map = {

        "CHECK_CPU":
        "SQL_MONITORING",

        "CHECK_BLOCKING":
        "SQL_MONITORING",

        "CHECK_LONG_RUNNING_QUERIES":
        "SQL_MONITORING",

        "GENERAL_HEALTH_CHECK":
        "SQL_MONITORING"

    }

    return {

        "task": task,

        "tool":
        tool_map.get(

            task,

            "UNKNOWN"

        )

    }