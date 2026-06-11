# =========================================================
# Backup Status Monitor
# Autonomous AI DBA Operations Platform
# =========================================================

from datetime import datetime

from app.monitoring.sql_collector import (
    execute_monitoring_query
)


# =========================================================
# CHECK BACKUP STATUS
# =========================================================

def check_backup_status():
    """
    Check latest SQL Server database backup status from msdb.
    """

    try:

        print("\n========================================")
        print(" Backup Status Monitoring ")
        print("========================================\n")

        query = """
        SELECT
            database_name,
            MAX(backup_finish_date) AS last_backup_time,
            CASE
                WHEN MAX(backup_finish_date) IS NULL THEN 'NO BACKUP FOUND'
                WHEN MAX(backup_finish_date) < DATEADD(DAY, -1, GETDATE()) THEN 'BACKUP OLD'
                ELSE 'BACKUP HEALTHY'
            END AS backup_status
        FROM msdb.dbo.backupset
        WHERE type = 'D'
        GROUP BY database_name
        ORDER BY last_backup_time DESC;
        """

        backup_results = execute_monitoring_query(
            query
        )

        backups = []

        if backup_results:

            for row in backup_results:

                backup_data = {
                    "database_name": row[0] if len(row) > 0 else None,
                    "last_backup_time": row[1] if len(row) > 1 else None,
                    "backup_status": row[2] if len(row) > 2 else None
                }

                backups.append(
                    backup_data
                )

                print(f"Database Name    : {backup_data['database_name']}")
                print(f"Last Backup Time : {backup_data['last_backup_time']}")
                print(f"Backup Status    : {backup_data['backup_status']}")
                print("----------------------------------------")

            unhealthy_backups = [
                backup for backup in backups
                if backup["backup_status"] != "BACKUP HEALTHY"
            ]

            if unhealthy_backups:

                return {
                    "overall_status": "ATTENTION REQUIRED",
                    "check_name": "BACKUP_STATUS",
                    "message": "One or more databases have old or missing backups.",
                    "backup_count": len(backups),
                    "unhealthy_backup_count": len(unhealthy_backups),
                    "backups": backups,
                    "checked_at": str(datetime.now())
                }

            return {
                "overall_status": "HEALTHY",
                "check_name": "BACKUP_STATUS",
                "message": "All checked databases have healthy backups.",
                "backup_count": len(backups),
                "unhealthy_backup_count": 0,
                "backups": backups,
                "checked_at": str(datetime.now())
            }

        print("No backup records found.")

        return {
            "overall_status": "ATTENTION REQUIRED",
            "check_name": "BACKUP_STATUS",
            "message": "No backup records found in msdb.",
            "backup_count": 0,
            "unhealthy_backup_count": 0,
            "backups": [],
            "checked_at": str(datetime.now())
        }

    except Exception as error:

        print("\nBackup Status Monitoring Error:\n")
        print(error)

        return {
            "overall_status": "ERROR",
            "check_name": "BACKUP_STATUS",
            "message": str(error),
            "backup_count": 0,
            "unhealthy_backup_count": 0,
            "backups": [],
            "checked_at": str(datetime.now())
        }


# =========================================================
# TEST EXECUTION
# =========================================================

if __name__ == "__main__":

    result = check_backup_status()

    print("\n========================================")
    print(" BACKUP STATUS MONITOR RESULT ")
    print("========================================\n")

    print(result)