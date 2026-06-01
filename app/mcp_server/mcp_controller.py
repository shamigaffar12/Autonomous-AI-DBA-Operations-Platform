# =========================================================
# MCP Controller
# Autonomous AI DBA Operations Platform
# =========================================================


# =========================================================
# IMPORT WORKFLOW MANAGER
# =========================================================

from app.mcp_server.workflow_manager import (

    display_workflow_steps,

    execute_workflow,

    workflow_summary
)


# =========================================================
# IMPORT TOOL REGISTRY
# =========================================================

from app.mcp_server.tool_registry import (

    display_registered_tools
)


# =========================================================
# MCP CONTROLLER CLASS
# =========================================================

class MCPController:


    # =====================================================
    # CONSTRUCTOR
    # =====================================================

    def __init__(self):

        self.name = (

            "MCP Orchestration Controller"
        )


    # =====================================================
    # START WORKFLOW
    # =====================================================

    def start_workflow(self):

        """
        Start MCP orchestration workflow.
        """

        print("\n========================================")

        print(" Autonomous AI DBA Operations Platform ")

        print(" MCP ORCHESTRATION CONTROLLER ")

        print("========================================\n")


        # =================================================
        # DISPLAY REGISTERED TOOLS
        # =================================================

        display_registered_tools()


        # =================================================
        # DISPLAY WORKFLOW
        # =================================================

        display_workflow_steps()


        # =================================================
        # EXECUTE WORKFLOW
        # =================================================

        execute_workflow()


        # =================================================
        # WORKFLOW SUMMARY
        # =================================================

        print("\n========================================")

        print(" WORKFLOW SUMMARY ")

        print("========================================")

        workflow_summary()


        # =================================================
        # COMPLETION MESSAGE
        # =================================================

        print("\n========================================")

        print(" MCP ORCHESTRATION SUCCESSFUL ")

        print("========================================\n")


# =========================================================
# MAIN EXECUTION
# =========================================================

if __name__ == "__main__":

    controller = MCPController()

    controller.start_workflow()