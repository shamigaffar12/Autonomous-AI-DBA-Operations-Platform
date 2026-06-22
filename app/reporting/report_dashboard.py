# =========================================================
# Report Dashboard Data
# Autonomous AI DBA Operations Platform
# =========================================================

import os

from datetime import datetime


# =========================================================
# REPORT FOLDER CONFIGURATION
# =========================================================

EXCEL_REPORT_FOLDER = "excel_reports"


# =========================================================
# GET REPORT TYPE
# =========================================================

def get_report_type(
    file_name
):
    """
    Identify report type from Excel file name.
    """

    lower_name = str(
        file_name
    ).lower()

    if "operations" in lower_name:

        return "Monthly DBA Operations Report"

    if "health" in lower_name:

        return "Excel Health Report"

    if "approval" in lower_name:

        return "Excel Approval Report"

    if "governance" in lower_name:

        return "Excel Governance Report"

    if "performance" in lower_name:

        return "Excel Performance Report"

    return "Excel Report"


# =========================================================
# GET REPORT DASHBOARD DATA
# =========================================================

def get_report_dashboard_data():
    """
    Return Excel-only report dashboard data.

    Text reports are intentionally ignored.
    """

    if not os.path.exists(
        EXCEL_REPORT_FOLDER
    ):

        return {
            "total_reports": 0,
            "latest_report": None,
            "reports": []
        }

    report_items = []

    for root, directories, files in os.walk(
        EXCEL_REPORT_FOLDER
    ):

        for file_name in files:

            if not file_name.endswith(
                ".xlsx"
            ):

                continue

            file_path = os.path.join(
                root,
                file_name
            ).replace(
                "\\",
                "/"
            )

            try:

                modified_timestamp = os.path.getmtime(
                    file_path
                )

                modified_at = datetime.fromtimestamp(
                    modified_timestamp
                ).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

                file_size_kb = round(
                    os.path.getsize(
                        file_path
                    ) / 1024,
                    2
                )

            except Exception:

                modified_timestamp = 0
                modified_at = "-"
                file_size_kb = 0

            report_items.append(
                {
                    "report_name": file_name,
                    "report_type": get_report_type(
                        file_name
                    ),
                    "file_path": file_path,
                    "status": "Available",
                    "modified_at": modified_at,
                    "modified_timestamp": modified_timestamp,
                    "file_size_kb": file_size_kb
                }
            )

    report_items.sort(
        key=lambda item: item.get(
            "modified_timestamp",
            0
        ),
        reverse=True
    )

    latest_report = None

    if report_items:

        latest_report = report_items[
            0
        ].get(
            "report_name"
        )

    return {
        "total_reports": len(
            report_items
        ),
        "latest_report": latest_report,
        "reports": report_items
    }


# =========================================================
# TEST EXECUTION
# =========================================================

if __name__ == "__main__":

    data = get_report_dashboard_data()

    print(
        f"\nTotal Excel Reports: {data['total_reports']}"
    )

    print(
        f"Latest Excel Report: {data['latest_report']}"
    )