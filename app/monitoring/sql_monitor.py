# =========================================================
# Central SQL Monitoring Engine
# Autonomous AI DBA Operations Platform
# =========================================================

# Import monitoring collector functions
from app.monitoring.sql_collector import (

    execute_monitoring_query,

    read_sql_file
)


# Import AI DBA Agent
from app.ai_agent.agent import AIDBAgent


# Import incident formatter
from app.monitoring.incident_formatter import (

    format_incident_data
)


# Import datetime
from datetime import datetime


# Import OS
import os


# =========================================================
# CPU MONITORING
# =========================================================

print("\n========================================")

print(" CPU Monitoring Results ")

print("========================================\n")


# Read CPU monitoring query
cpu_query = read_sql_file(

    "sql/health_queries/cpu_monitor.sql"
)


# Execute CPU monitoring query
cpu_results = execute_monitoring_query(

    cpu_query
)


# Display CPU results
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


# =========================================================
# BLOCKING SESSION MONITORING
# =========================================================

print("\n========================================")

print(" Blocking Session Monitoring ")

print("========================================\n")


# Read blocking session query
blocking_query = read_sql_file(

    "sql/health_queries/blocking_sessions.sql"
)


# Execute blocking monitoring query
blocking_results = execute_monitoring_query(

    blocking_query
)


# Display blocking monitoring results
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


# =========================================================
# LONG RUNNING QUERY MONITORING
# =========================================================

print("\n========================================")

print(" Long Running Query Monitoring ")

print("========================================\n")


# Read long running query monitoring query
long_query = read_sql_file(

    "sql/health_queries/long_running_queries.sql"
)


# Execute long running query monitoring
long_results = execute_monitoring_query(

    long_query
)


# Display long running query results
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


# =========================================================
# DATABASE SIZE MONITORING
# =========================================================

print("\n========================================")

print(" Database Size Monitoring ")

print("========================================\n")


# Read database size query
database_query = read_sql_file(

    "sql/health_queries/database_size.sql"
)


# Execute database size query
# Execute database size query
database_results = execute_monitoring_query(

    database_query
)

# =========================================================
# DEBUG DATABASE RESULTS
# =========================================================

print("\nDEBUG DATABASE RESULTS:")
print(database_results)
print(f"TYPE: {type(database_results)}")

# Display database size results
if database_results:

    for row in database_results:

        print(f"Database Name : {row[0]}")
        print(f"Database Size : {row[1]} MB")

        print("----------------------------------------")

else:

    print("No database size data found.")


# =========================================================
# INCIDENT FORMATTING
# =========================================================

incident_summary = format_incident_data(

    cpu_results,

    blocking_results,

    long_results
)


print("\n========================================")

print(" INCIDENT SUMMARY ")

print("========================================\n")


print(incident_summary)


# =========================================================
# AI INCIDENT ANALYSIS
# =========================================================

print("\n========================================")

print(" AI INCIDENT ANALYSIS ")

print("========================================\n")


# Create AI DBA Agent
agent = AIDBAgent()


# Send monitoring results to AI
ai_result = agent.analyze_incident(

    incident_summary
)


# Display AI RCA result
print(

    ai_result["analysis"]

)


# =========================================================
# SAVE INCIDENT REPORT
# =========================================================

# Create reports folder
os.makedirs(

    "reports",

    exist_ok=True
)


# Generate timestamp
timestamp = datetime.now().strftime(

    "%Y%m%d_%H%M%S"
)


# Dynamic report filename
report_file = (

    f"reports/incident_report_{timestamp}.txt"
)


# Save report
with open(

    report_file,

    "w",

    encoding="utf-8"

) as file:


    file.write(

        ai_result["analysis"]

    )


print(

    f"\nIncident report saved: {report_file}"
)


# =========================================================
# MONITORING COMPLETED
# =========================================================

print("\n========================================")

print(" SQL Monitoring Completed Successfully ")

print("========================================\n")