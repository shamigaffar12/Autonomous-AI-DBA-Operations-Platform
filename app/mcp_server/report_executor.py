# =========================================================
# Report Executor
# Autonomous AI DBA Operations Platform
# =========================================================

from datetime import datetime
import os

from app.reporting.report_formatter import (
    format_report
)

from app.common.config_manager import (
    REPORT_FOLDER
)


# =========================================================
# SAVE REPORT
# =========================================================

def save_report(
    overall_status,
    incident_summary,
    ai_analysis
):
    """
    Save formatted AI incident report.
    """

    print(
        "\nStarting Report Generation Workflow...\n"
    )

    # =====================================================
    # CREATE REPORT DIRECTORY
    # =====================================================

    os.makedirs(
        REPORT_FOLDER,
        exist_ok=True
    )

    # =====================================================
    # GENERATE REPORT FILE NAME
    # =====================================================

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    report_file = (
        f"{REPORT_FOLDER}/incident_report_{timestamp}.txt"
    )

    # =====================================================
    # FORMAT REPORT
    # =====================================================

    formatted_report = format_report(
        overall_status,
        incident_summary,
        ai_analysis
    )

    # =====================================================
    # SAVE REPORT
    # =====================================================

    with open(
        report_file,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            formatted_report
        )

    print(
        f"Report Saved: {report_file}"
    )

    return report_file


# =========================================================
# TEST EXECUTION
# =========================================================

if __name__ == "__main__":

    save_report(
        "HEALTHY",
        "No incidents detected.",
        "AI analysis completed successfully."
    )