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

    ai_analysis

):

    """
    Generate structured recommendation
    from AI analysis.
    """

    risk = classify_risk(

        ai_analysis

    )

    analysis = ai_analysis.upper()

    # =====================================================
    # BLOCKING
    # =====================================================

    if "BLOCKING" in analysis:

        return {

            "recommendation":
            "Investigate and resolve blocking session.",

            "action_type":
            "BLOCKING_INVESTIGATION",

            "risk":
            risk["severity"],

            "approval_required":
            risk["approval_required"]

        }

    # =====================================================
    # DEADLOCK
    # =====================================================

    if "DEADLOCK" in analysis:

        return {

            "recommendation":
            "Investigate deadlock and optimize transaction flow.",

            "action_type":
            "DEADLOCK_ANALYSIS",

            "risk":
            risk["severity"],

            "approval_required":
            risk["approval_required"]

        }

    # =====================================================
    # HIGH CPU
    # =====================================================

    if "HIGH CPU" in analysis:

        return {

            "recommendation":
            "Analyze high CPU queries and execution plans.",

            "action_type":
            "CPU_ANALYSIS",

            "risk":
            risk["severity"],

            "approval_required":
            risk["approval_required"]

        }

    # =====================================================
    # MISSING INDEX
    # =====================================================

    if "MISSING INDEX" in analysis:

        return {

            "recommendation":
            "Create recommended missing index after approval.",

            "action_type":
            "INDEX_CREATION",

            "risk":
            risk["severity"],

            "approval_required":
            risk["approval_required"]

        }

    # =====================================================
    # INDEX FRAGMENTATION
    # =====================================================

    if "FRAGMENTATION" in analysis:

        return {

            "recommendation":
            "Rebuild fragmented index.",

            "action_type":
            "INDEX_REBUILD",

            "risk":
            risk["severity"],

            "approval_required":
            risk["approval_required"]

        }

    # =====================================================
    # STATISTICS
    # =====================================================

    if "STATISTICS" in analysis:

        return {

            "recommendation":
            "Update database statistics.",

            "action_type":
            "UPDATE_STATISTICS",

            "risk":
            risk["severity"],

            "approval_required":
            risk["approval_required"]

        }

    # =====================================================
    # HEALTHY
    # =====================================================

    return {

        "recommendation":
        "Continue monitoring. No action required.",

        "action_type":
        "NO_ACTION",

        "risk":
        risk["severity"],

        "approval_required":
        False

    }


# =========================================================
# TEST EXECUTION
# =========================================================

if __name__ == "__main__":

    sample_analysis = """

    Blocking session detected.
    High CPU usage observed.

    """

    recommendation = (

        generate_recommendation(

            sample_analysis

        )

    )

    print(

        "\nRecommendation:\n"

    )

    print(

        recommendation

    )