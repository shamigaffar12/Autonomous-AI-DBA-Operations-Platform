# =========================================================
# Agent Planner
# =========================================================

def create_investigation_plan(

    incident_summary

):

    plan = []

    summary = incident_summary.upper()

    if "CPU" in summary:

        plan.append(

            "CHECK_CPU"

        )

    if "BLOCKING" in summary:

        plan.append(

            "CHECK_BLOCKING"

        )

    if "LONG RUNNING" in summary:

        plan.append(

            "CHECK_LONG_RUNNING_QUERIES"

        )

    if not plan:

        plan.append(

            "GENERAL_HEALTH_CHECK"

        )

    return plan