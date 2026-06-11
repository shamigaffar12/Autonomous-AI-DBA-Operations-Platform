# =========================================================
# MCP Tool Registry
# Autonomous AI DBA Operations Platform
# =========================================================

DBA_TOOL_REGISTRY = {

    "CHECK_CPU": {
        "name": "CPU Health Monitor",
        "category": "MONITORING",
        "description": "Checks SQL Server CPU pressure and active workload.",
        "risk": "LOW",
        "approval_required": False
    },

    "CHECK_BLOCKING": {
        "name": "Blocking Session Monitor",
        "category": "MONITORING",
        "description": "Detects blocking sessions in SQL Server.",
        "risk": "LOW",
        "approval_required": False
    },

    "CHECK_LONG_RUNNING_QUERIES": {
        "name": "Long Running Query Monitor",
        "category": "PERFORMANCE",
        "description": "Detects long running SQL Server queries.",
        "risk": "LOW",
        "approval_required": False
    },

    "CHECK_FAILED_JOBS": {
        "name": "Failed SQL Job Monitor",
        "category": "MONITORING",
        "description": "Detects failed SQL Server Agent jobs.",
        "risk": "LOW",
        "approval_required": False
    },

    "VALIDATE_RBAC_PERMISSION": {
        "name": "RBAC Permission Validator",
        "category": "SECURITY",
        "description": (
            "Validates whether the current DBA role is allowed "
            "to perform medium or high-risk DBA actions."
        ),
        "risk": "LOW",
        "approval_required": False
    },

    "REQUEST_FAILED_JOB_RESTART_APPROVAL": {
        "name": "Failed Job Restart Approval Workflow",
        "category": "AUTOMATION",
        "description": (
            "Creates approval-controlled restart request "
            "for failed SQL Server Agent jobs."
        ),
        "risk": "MEDIUM",
        "approval_required": True
    },

    "CHECK_BACKUP_STATUS": {
        "name": "Backup Status Monitor",
        "category": "BACKUP",
        "description": "Checks latest database backup status.",
        "risk": "LOW",
        "approval_required": False
    },

    "CHECK_DATABASE_SPACE": {
        "name": "Database Space Monitor",
        "category": "CAPACITY",
        "description": "Checks database size and space usage.",
        "risk": "LOW",
        "approval_required": False
    },

    "CHECK_INDEX_FRAGMENTATION": {
        "name": "Index Fragmentation Monitor",
        "category": "PERFORMANCE",
        "description": (
            "Checks SQL Server index fragmentation and identifies "
            "indexes requiring maintenance."
        ),
        "risk": "LOW",
        "approval_required": False
    },

    "CHECK_STATISTICS_HEALTH": {
        "name": "Statistics Health Monitor",
        "category": "PERFORMANCE",
        "description": "Checks outdated or heavily modified SQL Server statistics.",
        "risk": "LOW",
        "approval_required": False
    },

    "GENERATE_PERFORMANCE_TUNING_REPORT": {
        "name": "Performance Tuning Report Generator",
        "category": "REPORTING",
        "description": (
            "Generates performance tuning report using fragmentation "
            "and statistics health results."
        ),
        "risk": "LOW",
        "approval_required": False
    },

    "GENERATE_DAILY_HEALTH_REPORT": {
        "name": "Daily DBA Health Report Generator",
        "category": "REPORTING",
        "description": "Generates daily DBA operational health report.",
        "risk": "LOW",
        "approval_required": False
    },

    "SEND_TO_AZURE_MONITOR": {
        "name": "Azure Monitor Adapter",
        "category": "AZURE_INTEGRATION",
        "description": (
            "Prepares DBA health summary for Azure Monitor "
            "and Log Analytics integration."
        ),
        "risk": "LOW",
        "approval_required": False
    },

    "CREATE_AZURE_AUTOMATION_RUNBOOK_REQUEST": {
        "name": "Azure Automation Runbook Adapter",
        "category": "AZURE_INTEGRATION",
        "description": (
            "Creates simulated Azure Automation runbook request "
            "for approval-based DBA remediation."
        ),
        "risk": "MEDIUM",
        "approval_required": True
    }
}


# =========================================================
# GET TOOL DETAILS
# =========================================================

def get_tool_details(
    tool_name
):
    """
    Return tool metadata from registry.
    """

    return DBA_TOOL_REGISTRY.get(
        tool_name,
        {
            "name": "Unknown Tool",
            "category": "UNKNOWN",
            "description": "Tool not registered.",
            "risk": "UNKNOWN",
            "approval_required": True
        }
    )


# =========================================================
# LIST TOOLS
# =========================================================

def list_registered_tools():
    """
    Return all registered DBA tools.
    """

    return DBA_TOOL_REGISTRY


# =========================================================
# TEST EXECUTION
# =========================================================

if __name__ == "__main__":

    print("\n========================================")
    print(" REGISTERED DBA TOOLS ")
    print("========================================\n")

    for tool, details in list_registered_tools().items():

        print(
            f"{tool} -> {details['name']}"
        )