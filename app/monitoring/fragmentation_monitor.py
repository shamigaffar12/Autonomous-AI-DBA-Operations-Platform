# =========================================================
# Index Fragmentation Monitor
# Autonomous AI DBA Operations Platform
# =========================================================

from datetime import datetime

from app.monitoring.sql_collector import (
    execute_monitoring_query
)


# =========================================================
# CHECK INDEX FRAGMENTATION
# =========================================================

def check_index_fragmentation():
    """
    Check SQL Server index fragmentation.
    """

    try:

        print("\n========================================")
        print(" Index Fragmentation Monitoring ")
        print("========================================\n")

        query = """
        SELECT
            DB_NAME() AS database_name,
            OBJECT_NAME(ips.object_id) AS table_name,
            i.name AS index_name,
            ips.avg_fragmentation_in_percent,
            ips.page_count
        FROM sys.dm_db_index_physical_stats(
            DB_ID(),
            NULL,
            NULL,
            NULL,
            'LIMITED'
        ) ips
        INNER JOIN sys.indexes i
            ON ips.object_id = i.object_id
            AND ips.index_id = i.index_id
        WHERE
            ips.page_count > 100
            AND ips.avg_fragmentation_in_percent > 10
        ORDER BY
            ips.avg_fragmentation_in_percent DESC;
        """

        fragmentation_results = execute_monitoring_query(
            query
        )

        fragmented_indexes = []

        if fragmentation_results:

            for row in fragmentation_results:

                index_data = {
                    "database_name": row[0] if len(row) > 0 else None,
                    "table_name": row[1] if len(row) > 1 else None,
                    "index_name": row[2] if len(row) > 2 else None,
                    "fragmentation_percent": float(row[3]) if len(row) > 3 and row[3] is not None else 0,
                    "page_count": row[4] if len(row) > 4 else 0
                }

                fragmented_indexes.append(
                    index_data
                )

                print(f"Database      : {index_data['database_name']}")
                print(f"Table         : {index_data['table_name']}")
                print(f"Index         : {index_data['index_name']}")
                print(f"Fragmentation : {index_data['fragmentation_percent']}%")
                print(f"Page Count    : {index_data['page_count']}")
                print("----------------------------------------")

            return {
                "overall_status": "ATTENTION REQUIRED",
                "check_name": "INDEX_FRAGMENTATION",
                "message": "Fragmented indexes detected.",
                "fragmented_index_count": len(fragmented_indexes),
                "fragmented_indexes": fragmented_indexes,
                "checked_at": str(datetime.now())
            }

        print("No significant index fragmentation detected.")

        return {
            "overall_status": "HEALTHY",
            "check_name": "INDEX_FRAGMENTATION",
            "message": "No significant index fragmentation detected.",
            "fragmented_index_count": 0,
            "fragmented_indexes": [],
            "checked_at": str(datetime.now())
        }

    except Exception as error:

        print("\nIndex Fragmentation Monitoring Error:\n")
        print(error)

        return {
            "overall_status": "ERROR",
            "check_name": "INDEX_FRAGMENTATION",
            "message": str(error),
            "fragmented_index_count": 0,
            "fragmented_indexes": [],
            "checked_at": str(datetime.now())
        }


# =========================================================
# TEST EXECUTION
# =========================================================

if __name__ == "__main__":

    result = check_index_fragmentation()

    print("\n========================================")
    print(" INDEX FRAGMENTATION RESULT ")
    print("========================================\n")

    print(result)