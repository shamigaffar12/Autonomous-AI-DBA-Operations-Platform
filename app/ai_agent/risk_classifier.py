# =========================================================
# Risk Classifier
# Autonomous AI DBA Operations Platform
# =========================================================


# =========================================================
# CLASSIFY RISK
# =========================================================

def classify_risk(

    monitoring_result,

    ai_analysis

):

    """
    Classify incident risk using
    actual monitoring results.
    """

    overall_status = (

        monitoring_result.get(

            "overall_status",

            "UNKNOWN"

        ).upper()

    )

    incident_summary = (

        monitoring_result.get(

            "incident_summary",

            ""

        ).upper()

    )

    # =====================================================
    # HEALTHY
    # =====================================================

    if overall_status == "HEALTHY":

        return {

            "severity":
            "LOW",

            "confidence":
            95,

            "approval_required":
            False,

            "notify_email":
            False,

            "notify_teams":
            False

        }

    # =====================================================
    # CRITICAL CONDITIONS
    # =====================================================

    critical_keywords = [

        "DATABASE OFFLINE",

        "DATABASE UNAVAILABLE",

        "DATA CORRUPTION",

        "DISK FULL",

        "SEVERE OUTAGE"

    ]

    for keyword in critical_keywords:

        if keyword in incident_summary:

            return {

                "severity":
                "CRITICAL",

                "confidence":
                95,

                "approval_required":
                True,

                "notify_email":
                True,

                "notify_teams":
                True

            }

    # =====================================================
    # HIGH RISK CONDITIONS
    # =====================================================

    high_keywords = [

        "BLOCKING SESSION DETECTED",

        "DEADLOCK",

        "QUERY TIMEOUT",

        "HIGH CPU"

    ]

    for keyword in high_keywords:

        if keyword in incident_summary:

            return {

                "severity":
                "HIGH",

                "confidence":
                90,

                "approval_required":
                True,

                "notify_email":
                True,

                "notify_teams":
                True

            }

    # =====================================================
    # MEDIUM RISK CONDITIONS
    # =====================================================

    medium_keywords = [

        "LONG RUNNING QUERY",

        "FRAGMENTATION",

        "MISSING INDEX",

        "STATISTICS"

    ]

    for keyword in medium_keywords:

        if keyword in incident_summary:

            return {

                "severity":
                "MEDIUM",

                "confidence":
                85,

                "approval_required":
                True,

                "notify_email":
                True,

                "notify_teams":
                False

            }

    # =====================================================
    # DEFAULT ATTENTION REQUIRED
    # =====================================================

    return {

        "severity":
        "MEDIUM",

        "confidence":
        75,

        "approval_required":
        True,

        "notify_email":
        True,

        "notify_teams":
        False

    }


# =========================================================
# TEST EXECUTION
# =========================================================

if __name__ == "__main__":

    monitoring_result = {

        "overall_status":
        "HEALTHY",

        "incident_summary":
        """

        SQL Monitoring Summary

        No blocking sessions detected.

        No long running queries detected.

        Overall Status: HEALTHY

        """

    }

    result = classify_risk(

        monitoring_result,

        "AI Analysis"

    )

    print(

        "\nRisk Classification:\n"

    )

    print(

        result

    )