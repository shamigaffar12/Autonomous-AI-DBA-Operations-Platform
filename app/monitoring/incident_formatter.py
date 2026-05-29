# =========================================================
# Incident Formatter
# Autonomous AI DBA Operations Platform
# =========================================================

from datetime import datetime


# =========================================================
# ALERT THRESHOLDS
# =========================================================

CPU_THRESHOLD = 1000

LONG_QUERY_THRESHOLD = 30000


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

    incident_summary = (
        "\nSQL Monitoring Summary\n"
    )

    incident_summary += (
        f"\nMonitoring Time: {datetime.now()}"
    )

    incident_summary += (
        "\nDatabase: AdventureWorks2019\n"
    )

    critical_issue_found = False


    # =====================================================
    # CPU MONITORING
    # =====================================================

    if cpu_results:

        incident_summary += (
            "\n\nCPU Monitoring:"
        )

        for row in cpu_results:

            cpu_time = row[2]

            incident_summary += (

                f"\nSession ID: {row[0]}"
                f"\nStatus: {row[1]}"
                f"\nCPU Time: {row[2]}"
                f"\nElapsed Time: {row[3]}"
                f"\nReads: {row[4]}"
                f"\nWrites: {row[5]}"
                f"\nLogical Reads: {row[6]}"
            )

            if cpu_time > CPU_THRESHOLD:

                critical_issue_found = True

                incident_summary += (

                    "\nAlert: High CPU Usage Detected"
                )

            else:

                incident_summary += (

                    "\nAlert: CPU Usage Within Normal Range"
                )

            incident_summary += (
                "\n--------------------------"
            )

    else:

        incident_summary += (
            "\n\nNo CPU monitoring data found."
        )


    # =====================================================
    # BLOCKING SESSION MONITORING
    # =====================================================

    if blocking_results:

        critical_issue_found = True

        incident_summary += (
            "\n\nBlocking Sessions Detected:"
        )

        for row in blocking_results:

            incident_summary += (

                f"\nSession ID: {row[0]}"
                f"\nBlocking Session ID: {row[1]}"
                f"\nWait Type: {row[2]}"
                f"\nWait Time: {row[3]}"
                f"\nStatus: {row[4]}"
                "\n--------------------------"
            )

    else:

        incident_summary += (
            "\n\nNo blocking sessions detected."
        )


    # =====================================================
    # LONG RUNNING QUERY MONITORING
    # =====================================================

    if long_query_results:

        incident_summary += (
            "\n\nLong Running Query Analysis:"
        )

        for row in long_query_results:

            elapsed_time = row[4]

            incident_summary += (

                f"\nSession ID: {row[0]}"
                f"\nStatus: {row[1]}"
                f"\nCommand: {row[2]}"
                f"\nCPU Time: {row[3]}"
                f"\nElapsed Time: {row[4]}"
                f"\nBlocking Session: {row[5]}"
                f"\nWait Type: {row[6]}"
            )

            if elapsed_time > LONG_QUERY_THRESHOLD:

                critical_issue_found = True

                incident_summary += (

                    "\nAlert: Long Running Query Detected"
                )

            else:

                incident_summary += (

                    "\nAlert: Query Duration Within Normal Range"
                )

            incident_summary += (
                "\n--------------------------"
            )

    else:

        incident_summary += (
            "\n\nNo long running queries detected."
        )


    # =====================================================
    # OVERALL HEALTH STATUS
    # =====================================================

    if critical_issue_found:

        incident_summary += (

            "\n\nOverall Status: ATTENTION REQUIRED"
        )

    else:

        incident_summary += (

            "\n\nOverall Status: HEALTHY"
        )


    return incident_summary