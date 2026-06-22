# =========================================================
# Excel Health Report Generator - Compatibility Wrapper
# Autonomous AI DBA Operations Platform
# =========================================================

"""
This file is kept for backward compatibility.

Older modules may still import:
- generate_excel_health_report
- generate_monthly_excel_report

The actual monthly Excel report logic is now implemented in:
app.reporting.monthly_excel_report_generator

Do not delete this file until final cleanup/refactoring.
"""

from app.reporting.monthly_excel_report_generator import (
    generate_monthly_dba_excel_report,
    get_monthly_report_file_path
)


# =========================================================
# BACKWARD-COMPATIBLE HEALTH REPORT FUNCTION
# =========================================================

def generate_excel_health_report():
    """
    Backward-compatible function for old Excel health report calls.

    New behavior:
    Updates the monthly DBA Excel workbook instead of creating
    separate timestamp-based Excel files.

    Output file example:
    excel_reports/DBA_Monthly_Report_2026_06.xlsx
    """

    return generate_monthly_dba_excel_report(
        trigger_source="Legacy Excel Health Report Generator",
        notes="Monthly DBA Excel workbook updated from legacy health report function."
    )


# =========================================================
# BACKWARD-COMPATIBLE MONTHLY REPORT FUNCTION
# =========================================================

def generate_monthly_excel_report(
    current_incident=None,
    current_recommendation=None,
    notes="Monthly DBA Excel workbook updated successfully."
):
    """
    Backward-compatible function for previous monthly Excel calls.

    Parameters are accepted for compatibility, but the new generator
    reads live data from repository JSON files and updates the monthly workbook.
    """

    return generate_monthly_dba_excel_report(
        trigger_source="Legacy Monthly Excel Report Generator",
        notes=notes
    )


# =========================================================
# GET CURRENT MONTHLY REPORT PATH
# =========================================================

def get_excel_health_report_path():
    """
    Return current monthly DBA Excel report path.
    """

    return get_monthly_report_file_path()


# =========================================================
# DIRECT EXECUTION
# =========================================================

if __name__ == "__main__":

    result = generate_excel_health_report()

    print(
        result
    )