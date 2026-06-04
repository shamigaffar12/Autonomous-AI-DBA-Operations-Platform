# =========================================================
# Central SQL Monitoring Engine
# Autonomous AI DBA Operations Platform
# =========================================================

from app.monitoring.sql_collector import (
    execute_monitoring_query,
    read_sql_file
)

from app.monitoring.incident_formatter import (
    format_incident_data
)


# =========================================================
# RUN MONITORING
# =========================================================

def run_monitoring():

    # =====================================================
    # CPU MONITORING
    # =====================================================

    print("\n========================================")
    print(" CPU Monitoring Results ")
    print("========================================\n")

    cpu_query = read_sql_file(
        "sql/health_queries/cpu_monitor.sql"
    )

    cpu_results = execute_monitoring_query(
        cpu_query
    )

    if cpu_results:

        for row in cpu_results:

            print(f"Session ID          : {row[0]}")
            print(f"Status              : {row[1]}")
            print(f"CPU Time            : {row[2]}")
            print(f"Elapsed Time        : {row[3]}")
            print(f"Reads               : {row[4]}")
            print(f"Writes              : {row[5]}")
            print(f"Logical Reads       : {row[6]}")

            print("----------------------------------------")

    else:

        print("No CPU monitoring data found.")


    # =====================================================
    # BLOCKING SESSION MONITORING
    # =====================================================

    print("\n========================================")
    print(" Blocking Session Monitoring ")
    print("========================================\n")

    blocking_query = read_sql_file(
        "sql/health_queries/blocking_sessions.sql"
    )

    blocking_results = execute_monitoring_query(
        blocking_query
    )

    if blocking_results:

        for row in blocking_results:

            print(f"Session ID          : {row[0]}")
            print(f"Blocking Session ID : {row[1]}")
            print(f"Wait Type           : {row[2]}")
            print(f"Wait Time           : {row[3]}")
            print(f"Status              : {row[4]}")

            print("----------------------------------------")

    else:

        print("No blocking sessions detected.")


    # =====================================================
    # LONG RUNNING QUERY MONITORING
    # =====================================================

    print("\n========================================")
    print(" Long Running Query Monitoring ")
    print("========================================\n")

    long_query = read_sql_file(
        "sql/health_queries/long_running_queries.sql"
    )

    long_results = execute_monitoring_query(
        long_query
    )

    if long_results:

        for row in long_results:

            print(f"Session ID         : {row[0]}")
            print(f"Status             : {row[1]}")
            print(f"Command            : {row[2]}")
            print(f"CPU Time           : {row[3]}")
            print(f"Elapsed Time       : {row[4]}")
            print(f"Blocking Session   : {row[5]}")
            print(f"Wait Type          : {row[6]}")

            print("----------------------------------------")

    else:

        print("No long running queries detected.")


    # =====================================================
    # DATABASE SIZE MONITORING
    # =====================================================

    print("\n========================================")
    print(" Database Size Monitoring ")
    print("========================================\n")

    database_query = read_sql_file(
        "sql/health_queries/database_size.sql"
    )

    database_results = execute_monitoring_query(
        database_query
    )

    if database_results:

        for row in database_results:

            print(f"Database Name : {row[0]}")
            print(f"Database Size : {row[1]} MB")

            print("----------------------------------------")

    else:

        print("No database size data found.")


    # =====================================================
    # INCIDENT FORMATTING
    # =====================================================

    incident_summary = format_incident_data(

        cpu_results,

        blocking_results,

        long_results
    )

    print("\n========================================")
    print(" INCIDENT SUMMARY ")
    print("========================================\n")

    print(incident_summary)


    # =====================================================
    # OVERALL STATUS
    # =====================================================

    if "ATTENTION REQUIRED" in incident_summary:

        overall_status = "ATTENTION REQUIRED"

    else:

        overall_status = "HEALTHY"


    print("\n========================================")
    print(" SQL Monitoring Completed Successfully ")
    print("========================================\n")


    # =====================================================
    # RETURN RESULTS TO MCP
    # =====================================================

    return {

        "overall_status": overall_status,

        "incident_summary": incident_summary,

        "cpu_results": cpu_results,

        "blocking_results": blocking_results,

        "long_results": long_results
    }


# =========================================================
# MAIN EXECUTION
# =========================================================

if __name__ == "__main__":

    run_monitoring()