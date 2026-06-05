# =========================================================
# Analytics Exporter
# Autonomous AI DBA Operations Platform
# =========================================================

from datetime import datetime
import os

from app.analytics.daily_summary import (
    generate_daily_summary
)

from app.audit.audit_logger import (
    write_audit_log
)

from app.common.error_handler import (
    handle_error
)


# =========================================================
# EXPORT DAILY SUMMARY
# =========================================================

def export_daily_summary():

    """
    Export daily operations summary
    to a report file.
    """

    try:

        summary = generate_daily_summary()

        output_folder = (

            "reports/daily_summaries"

        )

        os.makedirs(

            output_folder,

            exist_ok=True

        )

        report_file = (

            f"{output_folder}/"
            f"daily_summary_"
            f"{datetime.now().strftime('%Y%m%d')}.txt"

        )

        with open(

            report_file,

            "w",

            encoding="utf-8"

        ) as file:

            file.write(

                "========================================\n"
            )

            file.write(

                " DAILY OPERATIONS SUMMARY \n"

            )

            file.write(

                "========================================\n\n"

            )

            file.write(

                f"Date                     : "
                f"{summary['date']}\n"

            )

            file.write(

                f"Total Incidents          : "
                f"{summary['total_incidents']}\n"

            )

            file.write(

                f"Healthy Incidents        : "
                f"{summary['healthy_incidents']}\n"

            )

            file.write(

                f"Attention Required       : "
                f"{summary['attention_required']}\n"

            )

            file.write(

                f"Latest Incident Status   : "
                f"{summary['latest_status']}\n"

            )

            file.write(

                f"Latest Report            : "
                f"{summary['latest_report']}\n"

            )

            file.write(

                f"Platform Health          : "
                f"{summary['platform_health']}\n"

            )

        write_audit_log(

            f"DAILY SUMMARY EXPORTED: "
            f"{report_file}"

        )

        print(

            f"\nDaily Summary Exported: "
            f"{report_file}"

        )

        return report_file

    except Exception as error:

        return handle_error(

            "ANALYTICS EXPORTER",

            error

        )


# =========================================================
# TEST EXECUTION
# =========================================================

if __name__ == "__main__":

    export_daily_summary()