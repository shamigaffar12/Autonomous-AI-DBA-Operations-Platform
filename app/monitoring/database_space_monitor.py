# =========================================================
# Database Space Monitor
# Autonomous AI DBA Operations Platform
# =========================================================

from datetime import datetime

from app.monitoring.sql_collector import (
    execute_monitoring_query,
    read_sql_file
)


# =========================================================
# CHECK DATABASE SPACE
# =========================================================

def check_database_space():
    """
    Check SQL Server database size and space usage.
    """

    try:

        print("\n========================================")
        print(" Database Space Monitoring ")
        print("========================================\n")

        query = read_sql_file(
            "sql/health_queries/database_size.sql"
        )

        if query is None:

            return {
                "overall_status": "ERROR",
                "check_name": "DATABASE_SPACE",
                "message": "Database size SQL file could not be loaded.",
                "databases": [],
                "checked_at": str(datetime.now())
            }

        space_results = execute_monitoring_query(
            query
        )

        databases = []

        if space_results:

            for row in space_results:

                database_data = {
                    "database_name": row[0] if len(row) > 0 else None,
                    "database_size_mb": row[1] if len(row) > 1 else None
                }

                databases.append(
                    database_data
                )

                print(f"Database Name : {database_data['database_name']}")
                print(f"Size MB       : {database_data['database_size_mb']}")
                print("----------------------------------------")

            return {
                "overall_status": "HEALTHY",
                "check_name": "DATABASE_SPACE",
                "message": "Database space check completed successfully.",
                "database_count": len(databases),
                "databases": databases,
                "checked_at": str(datetime.now())
            }

        print("No database space data found.")

        return {
            "overall_status": "ATTENTION REQUIRED",
            "check_name": "DATABASE_SPACE",
            "message": "No database space data found.",
            "database_count": 0,
            "databases": [],
            "checked_at": str(datetime.now())
        }

    except Exception as error:

        print("\nDatabase Space Monitoring Error:\n")
        print(error)

        return {
            "overall_status": "ERROR",
            "check_name": "DATABASE_SPACE",
            "message": str(error),
            "database_count": 0,
            "databases": [],
            "checked_at": str(datetime.now())
        }


# =========================================================
# TEST EXECUTION
# =========================================================

if __name__ == "__main__":

    result = check_database_space()

    print("\n========================================")
    print(" DATABASE SPACE MONITOR RESULT ")
    print("========================================\n")

    print(result)