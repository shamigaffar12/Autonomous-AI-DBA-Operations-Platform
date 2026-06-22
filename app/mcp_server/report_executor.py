# =========================================================
# Report Executor
# Autonomous AI DBA Operations Platform
# =========================================================

from datetime import datetime

from app.reporting.excel_health_report_generator import (
    generate_monthly_excel_report
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
    Save AI incident report into the monthly Excel workbook.

    This function no longer creates .txt report files.
    It updates one monthly Excel file such as:
    excel_reports/dba_operations_report_june_2026.xlsx
    """

    print(
        "\nStarting Monthly Excel Report Update Workflow...\n"
    )

    current_datetime = datetime.now()

    current_incident = {
        "date": current_datetime.strftime(
            "%Y-%m-%d"
        ),
        "time": current_datetime.strftime(
            "%H:%M:%S"
        ),
        "incident_id": (
            "INC-"
            + current_datetime.strftime(
                "%Y%m%d%H%M%S"
            )
        ),
        "incident_type": "AI Incident Report",
        "severity": "MEDIUM"
        if str(
            overall_status
        ).upper() != "HEALTHY"
        else "LOW",
        "overall_status": overall_status,
        "incident_summary": incident_summary,
        "ai_analysis": ai_analysis,
        "report_path": "",
        "source": "MCP Report Executor"
    }

    current_recommendation = {
        "date": current_datetime.strftime(
            "%Y-%m-%d"
        ),
        "time": current_datetime.strftime(
            "%H:%M:%S"
        ),
        "area": "AI DBA Analysis",
        "recommendation": ai_analysis,
        "priority": "Medium",
        "source": "AI Analysis Engine"
    }

    report_result = generate_monthly_excel_report(
        current_incident=current_incident,
        current_recommendation=current_recommendation,
        notes="Incident analysis added to monthly Excel workbook."
    )

    if report_result.get(
        "overall_status"
    ) == "COMPLETED":

        report_file = report_result.get(
            "report_path"
        )

        print(
            "\n========================================"
        )

        print(
            " Monthly Excel Report Updated "
        )

        print(
            "========================================\n"
        )

        print(
            f"Report Path : {report_file}"
        )

        return report_file

    print(
        "\nMonthly Excel Report Update Failed:"
    )

    print(
        report_result.get(
            "message",
            "Unknown error"
        )
    )

    return None


# =========================================================
# TEST EXECUTION
# =========================================================

if __name__ == "__main__":

    result = save_report(
        "HEALTHY",
        "No incidents detected.",
        "AI analysis completed successfully."
    )

    print(
        result
    )