# =========================================================
# Statistics Health Monitor
# Autonomous AI DBA Operations Platform
# =========================================================

from datetime import datetime

from app.monitoring.sql_collector import (
    execute_monitoring_query
)


# =========================================================
# CHECK STATISTICS HEALTH
# =========================================================

def check_statistics_health():
    """
    Check SQL Server statistics freshness and modification count.
    """

    try:

        print("\n========================================")
        print(" Statistics Health Monitoring ")
        print("========================================\n")

        query = """
        SELECT
            DB_NAME() AS database_name,
            OBJECT_NAME(s.object_id) AS table_name,
            s.name AS statistics_name,
            sp.last_updated,
            sp.rows,
            sp.modification_counter
        FROM sys.stats s
        CROSS APPLY sys.dm_db_stats_properties(
            s.object_id,
            s.stats_id
        ) sp
        WHERE
            sp.modification_counter > 100
            OR sp.last_updated < DATEADD(DAY, -7, GETDATE())
        ORDER BY
            sp.modification_counter DESC;
        """

        statistics_results = execute_monitoring_query(
            query
        )

        stale_statistics = []

        if statistics_results:

            for row in statistics_results:

                stats_data = {
                    "database_name": row[0] if len(row) > 0 else None,
                    "table_name": row[1] if len(row) > 1 else None,
                    "statistics_name": row[2] if len(row) > 2 else None,
                    "last_updated": row[3] if len(row) > 3 else None,
                    "rows": row[4] if len(row) > 4 else 0,
                    "modification_counter": row[5] if len(row) > 5 else 0
                }

                stale_statistics.append(
                    stats_data
                )

                print(f"Database              : {stats_data['database_name']}")
                print(f"Table                 : {stats_data['table_name']}")
                print(f"Statistics            : {stats_data['statistics_name']}")
                print(f"Last Updated          : {stats_data['last_updated']}")
                print(f"Rows                  : {stats_data['rows']}")
                print(f"Modification Counter  : {stats_data['modification_counter']}")
                print("----------------------------------------")

            return {
                "overall_status": "ATTENTION REQUIRED",
                "check_name": "STATISTICS_HEALTH",
                "message": "Outdated or heavily modified statistics detected.",
                "stale_statistics_count": len(
                    stale_statistics
                ),
                "stale_statistics": stale_statistics,
                "checked_at": str(
                    datetime.now()
                )
            }

        print("No outdated statistics detected.")

        return {
            "overall_status": "HEALTHY",
            "check_name": "STATISTICS_HEALTH",
            "message": "No outdated statistics detected.",
            "stale_statistics_count": 0,
            "stale_statistics": [],
            "checked_at": str(
                datetime.now()
            )
        }

    except Exception as error:

        print("\nStatistics Health Monitoring Error:\n")
        print(error)

        return {
            "overall_status": "ERROR",
            "check_name": "STATISTICS_HEALTH",
            "message": str(
                error
            ),
            "stale_statistics_count": 0,
            "stale_statistics": [],
            "checked_at": str(
                datetime.now()
            )
        }


# =========================================================
# TEST EXECUTION
# =========================================================

if __name__ == "__main__":

    result = check_statistics_health()

    print("\n========================================")
    print(" STATISTICS HEALTH RESULT ")
    print("========================================\n")

    print(
        result
    )