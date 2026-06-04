# =========================================================
# Report Formatter
# Autonomous AI DBA Operations Platform
# =========================================================


# =========================================================
# FORMAT INCIDENT REPORT
# =========================================================

def format_report(

    overall_status,

    incident_summary,

    ai_analysis

):

    """
    Generate formatted incident report.
    """

    report = f"""

========================================
 INCIDENT REPORT
========================================

Overall Status
--------------
{overall_status}


Monitoring Summary
------------------
{incident_summary}


AI Analysis
-----------
{ai_analysis}

========================================
 END OF REPORT
========================================

"""

    return report