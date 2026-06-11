# =========================================================
# Daily DBA Health Report Generator
# Autonomous AI DBA Operations Platform
# =========================================================

import os

from datetime import datetime


# =========================================================
# GENERATE DAILY HEALTH REPORT
# =========================================================

def generate_daily_health_report(
    tool_results
):
    """
    Generate daily DBA health report from agentic tool execution results.
    """

    try:

        print("\n========================================")
        print(" Daily DBA Health Report Generation ")
        print("========================================\n")

        report_folder = "reports/daily_health_reports"

        os.makedirs(
            report_folder,
            exist_ok=True
        )

        report_time = datetime.now()

        report_file_name = (
            f"daily_dba_health_report_"
            f"{report_time.strftime('%Y%m%d_%H%M%S')}.txt"
        )

        report_path = os.path.join(
            report_folder,
            report_file_name
        )

        lines = []

        lines.append("========================================")
        lines.append(" DAILY DBA HEALTH REPORT")
        lines.append(" Autonomous AI DBA Operations Platform")
        lines.append("========================================")
        lines.append("")
        lines.append(f"Report Time: {report_time}")
        lines.append("")

        overall_status = "HEALTHY"

        results = tool_results.get(
            "results",
            []
        )

        for item in results:

            tool = item.get(
                "tool",
                "UNKNOWN"
            )

            status = item.get(
                "status",
                "UNKNOWN"
            )

            result = item.get(
                "result",
                {}
            )

            lines.append("----------------------------------------")
            lines.append(f"Tool   : {tool}")
            lines.append(f"Status : {status}")

            if isinstance(
                result,
                dict
            ):

                check_status = result.get(
                    "overall_status",
                    "UNKNOWN"
                )

                message = result.get(
                    "message",
                    "No message available."
                )

                lines.append(f"Health : {check_status}")
                lines.append(f"Message: {message}")

                if check_status in [
                    "ATTENTION REQUIRED",
                    "ERROR"
                ]:

                    overall_status = "ATTENTION REQUIRED"

            else:

                lines.append(f"Result : {result}")

            lines.append("")

        lines.append("========================================")
        lines.append(f"OVERALL DBA HEALTH STATUS: {overall_status}")
        lines.append("========================================")

        with open(
            report_path,
            "w",
            encoding="utf-8"
        ) as report_file:

            report_file.write(
                "\n".join(
                    lines
                )
            )

        print(
            f"Daily DBA Health Report Generated: {report_path}"
        )

        return {
            "overall_status": overall_status,
            "check_name": "DAILY_DBA_HEALTH_REPORT",
            "message": "Daily DBA health report generated successfully.",
            "report_path": report_path,
            "generated_at": str(
                report_time
            )
        }

    except Exception as error:

        print("\nDaily Health Report Generation Error:\n")
        print(error)

        return {
            "overall_status": "ERROR",
            "check_name": "DAILY_DBA_HEALTH_REPORT",
            "message": str(
                error
            ),
            "report_path": None,
            "generated_at": str(
                datetime.now()
            )
        }


# =========================================================
# TEST EXECUTION
# =========================================================

if __name__ == "__main__":

    sample_tool_results = {
        "results": [
            {
                "tool": "CHECK_CPU",
                "status": "EXECUTED",
                "result": {
                    "overall_status": "HEALTHY",
                    "message": "CPU usage is within normal range."
                }
            },
            {
                "tool": "CHECK_BLOCKING",
                "status": "EXECUTED",
                "result": {
                    "overall_status": "ATTENTION REQUIRED",
                    "message": "Blocking sessions detected."
                }
            },
            {
                "tool": "CHECK_FAILED_JOBS",
                "status": "EXECUTED",
                "result": {
                    "overall_status": "ATTENTION REQUIRED",
                    "message": "Failed SQL jobs detected."
                }
            },
            {
                "tool": "CHECK_BACKUP_STATUS",
                "status": "EXECUTED",
                "result": {
                    "overall_status": "HEALTHY",
                    "message": "Backup status check completed successfully."
                }
            },
            {
                "tool": "CHECK_DATABASE_SPACE",
                "status": "EXECUTED",
                "result": {
                    "overall_status": "HEALTHY",
                    "message": "Database space check completed successfully."
                }
            }
        ]
    }

    result = generate_daily_health_report(
        sample_tool_results
    )

    print("\n========================================")
    print(" DAILY HEALTH REPORT RESULT ")
    print("========================================\n")

    print(
        result
    )