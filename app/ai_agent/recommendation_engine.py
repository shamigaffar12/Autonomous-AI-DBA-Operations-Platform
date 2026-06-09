# =========================================================
# Recommendation Engine
# Autonomous AI DBA Operations Platform
# =========================================================

from app.ai_agent.risk_classifier import (
    classify_risk
)


# =========================================================
# GENERATE RECOMMENDATION
# =========================================================

def generate_recommendation(

    monitoring_result,

    ai_analysis

):

    """
    Generate recommendation
    using actual monitoring results.
    """

    risk = classify_risk(

        monitoring_result,

        ai_analysis

    )

    overall_status = (

        monitoring_result[
            "overall_status"
        ]
        .upper()
    )

    incident_summary = (

        monitoring_result[
            "incident_summary"
        ]
        .upper()
    )

    # =====================================================
    # HEALTHY
    # =====================================================

    if overall_status == "HEALTHY":

        return {

            "recommendation":
            "System healthy. Continue monitoring.",

            "action_type":
            "NO_ACTION",

            "risk":
            risk["severity"],

            "approval_required":
            False

        }

    # =====================================================
    # BLOCKING
    # =====================================================

    if "BLOCKING SESSION DETECTED" in incident_summary:

        return {

            "recommendation":
            "Investigate blocking sessions and identify root blocking process.",

            "action_type":
            "BLOCKING_INVESTIGATION",

            "risk":
            risk["severity"],

            "approval_required":
            risk["approval_required"]

        }

    # =====================================================
    # LONG RUNNING QUERY
    # =====================================================

    if "LONG RUNNING QUERY" in incident_summary:

        return {

            "recommendation":
            "Analyze execution plan and optimize long running query.",

            "action_type":
            "QUERY_TUNING",

            "risk":
            risk["severity"],

            "approval_required":
            risk["approval_required"]

        }

    # =====================================================
    # HIGH CPU
    # =====================================================

    if "HIGH CPU" in incident_summary:

        return {

            "recommendation":
            "Identify top CPU consuming queries and review execution plans.",

            "action_type":
            "CPU_ANALYSIS",

            "risk":
            risk["severity"],

            "approval_required":
            risk["approval_required"]

        }

    # =====================================================
    # DATABASE SIZE
    # =====================================================

    if "DATABASE SIZE" in incident_summary:

        return {

            "recommendation":
            "Review database growth trend and perform capacity planning.",

            "action_type":
            "CAPACITY_PLANNING",

            "risk":
            risk["severity"],

            "approval_required":
            False

        }

    # =====================================================
    # DEFAULT
    # =====================================================

    return {

        "recommendation":
        "Review incident manually and perform further investigation.",

        "action_type":
        "MANUAL_REVIEW",

        "risk":
        risk["severity"],

        "approval_required":
        risk["approval_required"]

    }


# =========================================================
# TEST EXECUTION
# =========================================================

if __name__ == "__main__":

    sample_monitoring = {

        "overall_status":
        "HEALTHY",

        "incident_summary":
        "No blocking sessions detected."
    }

    result = generate_recommendation(

        sample_monitoring,

        "System operating normally."

    )

    print(result)