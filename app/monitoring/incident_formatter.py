# =========================================================
# Incident Formatter
# Autonomous AI DBA Operations Platform
# =========================================================


# =========================================================
# FORMAT INCIDENT DATA
# =========================================================

def format_incident_data(

    cpu_results,

    blocking_results,

    long_query_results

):

    """
    Convert monitoring results into
    AI-readable incident summary.
    """


    incident_summary = "\nSQL Monitoring Alert:\n"


    # =====================================================
    # CPU MONITORING
    # =====================================================

    if cpu_results:

        incident_summary += (

            "\n- High CPU usage detected"

        )


    # =====================================================
    # BLOCKING SESSION
    # =====================================================

    if blocking_results:

        incident_summary += (

            "\n- Blocking session identified"

        )


    # =====================================================
    # LONG RUNNING QUERIES
    # =====================================================

    if long_query_results:

        incident_summary += (

            "\n- Long running query detected"

        )


    # =====================================================
    # DEFAULT MESSAGE
    # =====================================================

    if (

        not cpu_results and

        not blocking_results and

        not long_query_results

    ):

        incident_summary += (

            "\n- No critical issues detected"

        )


    return incident_summary