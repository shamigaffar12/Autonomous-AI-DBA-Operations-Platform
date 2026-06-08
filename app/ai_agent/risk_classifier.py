# =========================================================
# Risk Classifier
# Autonomous AI DBA Operations Platform
# =========================================================


# =========================================================
# CLASSIFY RISK
# =========================================================

def classify_risk(

    ai_analysis

):

    """
    Classify incident risk level
    based on AI analysis.
    """

    analysis = ai_analysis.upper()

    # =====================================================
    # CRITICAL
    # =====================================================

    critical_keywords = [

        "DATABASE OFFLINE",
        "DATABASE UNAVAILABLE",
        "SEVERE OUTAGE",
        "DATA CORRUPTION",
        "DISK FULL"

    ]

    for keyword in critical_keywords:

        if keyword in analysis:

            return {

                "severity":
                "CRITICAL",

                "approval_required":
                True,

                "notify_email":
                True,

                "notify_teams":
                True

            }

    # =====================================================
    # HIGH
    # =====================================================

    high_keywords = [

        "DEADLOCK",
        "BLOCKING",
        "HIGH CPU",
        "LONG RUNNING QUERY",
        "QUERY TIMEOUT"

    ]

    for keyword in high_keywords:

        if keyword in analysis:

            return {

                "severity":
                "HIGH",

                "approval_required":
                True,

                "notify_email":
                True,

                "notify_teams":
                True

            }

    # =====================================================
    # MEDIUM
    # =====================================================

    medium_keywords = [

        "MISSING INDEX",
        "FRAGMENTATION",
        "STATISTICS",
        "PERFORMANCE DEGRADATION"

    ]

    for keyword in medium_keywords:

        if keyword in analysis:

            return {

                "severity":
                "MEDIUM",

                "approval_required":
                True,

                "notify_email":
                True,

                "notify_teams":
                False

            }

    # =====================================================
    # LOW
    # =====================================================

    return {

        "severity":
        "LOW",

        "approval_required":
        False,

        "notify_email":
        False,

        "notify_teams":
        False

    }


# =========================================================
# TEST EXECUTION
# =========================================================

if __name__ == "__main__":

    sample_analysis = """

    Blocking session detected.
    High CPU usage observed.
    Query timeout reported.

    """

    result = classify_risk(

        sample_analysis

    )

    print(

        "\nRisk Classification:\n"

    )

    print(

        result

    )