# =========================================================
# Performance Tuning Report Generator
# Autonomous AI DBA Operations Platform
# =========================================================

import os

from datetime import datetime


# =========================================================
# GENERATE PERFORMANCE TUNING REPORT
# =========================================================

def generate_performance_tuning_report(
    tool_results
):
    """
    Generate performance tuning report from fragmentation
    and statistics health results.
    """

    try:

        print("\n========================================")
        print(" Performance Tuning Report Generation ")
        print("========================================\n")

        report_folder = "reports/performance_tuning_reports"

        os.makedirs(
            report_folder,
            exist_ok=True
        )

        report_time = datetime.now()

        report_file_name = (
            f"performance_tuning_report_"
            f"{report_time.strftime('%Y%m%d_%H%M%S')}.txt"
        )

        report_path = os.path.join(
            report_folder,
            report_file_name
        )

        lines = []

        lines.append("========================================")
        lines.append(" PERFORMANCE TUNING REPORT")
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

            if tool not in [
                "CHECK_INDEX_FRAGMENTATION",
                "CHECK_STATISTICS_HEALTH"
            ]:

                continue

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

                # =========================================
                # FRAGMENTATION DETAILS
                # =========================================

                if tool == "CHECK_INDEX_FRAGMENTATION":

                    fragmented_indexes = result.get(
                        "fragmented_indexes",
                        []
                    )

                    lines.append("")
                    lines.append("Fragmented Index Details:")

                    if fragmented_indexes:

                        for index in fragmented_indexes:

                            lines.append(
                                f"- Database: {index.get('database_name')}, "
                                f"Table: {index.get('table_name')}, "
                                f"Index: {index.get('index_name')}, "
                                f"Fragmentation: {index.get('fragmentation_percent')}%, "
                                f"Pages: {index.get('page_count')}"
                            )

                    else:

                        lines.append(
                            "- No fragmented indexes found."
                        )

                # =========================================
                # STATISTICS DETAILS
                # =========================================

                if tool == "CHECK_STATISTICS_HEALTH":

                    stale_statistics = result.get(
                        "stale_statistics",
                        []
                    )

                    lines.append("")
                    lines.append("Statistics Health Details:")

                    if stale_statistics:

                        for stats in stale_statistics[:30]:

                            lines.append(
                                f"- Database: {stats.get('database_name')}, "
                                f"Table: {stats.get('table_name')}, "
                                f"Stats: {stats.get('statistics_name')}, "
                                f"Last Updated: {stats.get('last_updated')}, "
                                f"Rows: {stats.get('rows')}, "
                                f"Modification Counter: {stats.get('modification_counter')}"
                            )

                        if len(
                            stale_statistics
                        ) > 30:

                            lines.append(
                                f"...Additional stale statistics count: "
                                f"{len(stale_statistics) - 30}"
                            )

                    else:

                        lines.append(
                            "- No outdated statistics found."
                        )

            else:

                lines.append(
                    f"Result : {result}"
                )

            lines.append("")

        lines.append("========================================")
        lines.append(" PERFORMANCE RECOMMENDATIONS")
        lines.append("========================================")
        lines.append("")
        lines.append("- Review highly fragmented indexes.")
        lines.append("- Rebuild indexes when fragmentation is above 30%.")
        lines.append("- Reorganize indexes when fragmentation is between 10% and 30%.")
        lines.append("- Update outdated SQL Server statistics.")
        lines.append("- Review execution plans for long-running queries.")
        lines.append("- Monitor blocking sessions before running maintenance jobs.")
        lines.append("")

        lines.append("========================================")
        lines.append(f"OVERALL PERFORMANCE STATUS: {overall_status}")
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
            f"Performance Tuning Report Generated: {report_path}"
        )

        return {
            "overall_status": overall_status,
            "check_name": "PERFORMANCE_TUNING_REPORT",
            "message": "Performance tuning report generated successfully.",
            "report_path": report_path,
            "generated_at": str(
                report_time
            )
        }

    except Exception as error:

        print("\nPerformance Tuning Report Generation Error:\n")
        print(error)

        return {
            "overall_status": "ERROR",
            "check_name": "PERFORMANCE_TUNING_REPORT",
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
                "tool": "CHECK_INDEX_FRAGMENTATION",
                "status": "EXECUTED",
                "result": {
                    "overall_status": "HEALTHY",
                    "message": "No significant index fragmentation detected.",
                    "fragmented_indexes": []
                }
            },
            {
                "tool": "CHECK_STATISTICS_HEALTH",
                "status": "EXECUTED",
                "result": {
                    "overall_status": "ATTENTION REQUIRED",
                    "message": "Outdated statistics detected.",
                    "stale_statistics": [
                        {
                            "database_name": "AdventureWorks2019",
                            "table_name": "SalesOrderDetail",
                            "statistics_name": "IX_SalesOrderDetail_ProductID",
                            "last_updated": "2023-05-08",
                            "rows": 121317,
                            "modification_counter": 0
                        }
                    ]
                }
            }
        ]
    }

    result = generate_performance_tuning_report(
        sample_tool_results
    )

    print("\n========================================")
    print(" PERFORMANCE TUNING REPORT RESULT ")
    print("========================================\n")

    print(
        result
    )