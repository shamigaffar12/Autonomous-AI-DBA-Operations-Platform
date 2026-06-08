# =========================================================
# Agent Executor
# =========================================================

from app.ai_agent.agent_planner import (
    create_investigation_plan
)

from app.ai_agent.tool_selector import (
    select_tool
)

from app.ai_agent.query_generator import (
    generate_query
)

from app.ai_agent.risk_classifier import (
    classify_risk
)

from app.ai_agent.recommendation_engine import (
    generate_recommendation
)


def execute_agent_workflow(

    incident_summary,

    ai_analysis

):

    plan = (

        create_investigation_plan(

            incident_summary

        )

    )

    tasks = []

    for step in plan:

        tool = (

            select_tool(

                step

            )

        )

        query = (

            generate_query(

                step

            )

        )

        tasks.append({

            "task":
            step,

            "tool":
            tool,

            "query":
            query

        })

    risk = (

        classify_risk(

            ai_analysis

        )

    )

    recommendation = (

        generate_recommendation(

            ai_analysis

        )

    )

    return {

        "plan":
        plan,

        "tasks":
        tasks,

        "risk":
        risk,

        "recommendation":
        recommendation

    }