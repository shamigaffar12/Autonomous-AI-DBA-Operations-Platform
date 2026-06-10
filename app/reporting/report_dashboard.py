# =========================================================
# Report Dashboard Data
# Autonomous AI DBA Operations Platform
# =========================================================

import os

from app.common.config_manager import (
    REPORT_FOLDER
)


# =========================================================
# GET REPORT DASHBOARD DATA
# =========================================================

def get_report_dashboard_data():

    """
    Return report dashboard data.
    """

    if not os.path.exists(

        REPORT_FOLDER

    ):

        return {

            "total_reports":
            0,

            "latest_report":
            None,

            "reports":
            []

        }

    reports = [

        file

        for file in os.listdir(

            REPORT_FOLDER

        )

        if file.endswith(

            ".txt"

        )

    ]

    reports.sort(

        reverse=True

    )

    latest_report = (

        reports[0]

        if reports

        else None

    )

    return {

        "total_reports":
        len(reports),

        "latest_report":
        latest_report,

        "reports":
        reports

    }


# =========================================================
# TEST EXECUTION
# =========================================================

if __name__ == "__main__":

    data = get_report_dashboard_data()

    print(

        f"\nTotal Reports: "
        f"{data['total_reports']}"

    )