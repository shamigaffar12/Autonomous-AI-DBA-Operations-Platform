# =========================================================
# Azure Monitor Adapter
# Autonomous AI DBA Operations Platform
# =========================================================

from datetime import datetime


# =========================================================
# SEND HEALTH SUMMARY TO AZURE MONITOR
# =========================================================

def send_health_summary_to_azure_monitor(
    health_summary
):
    """
    Simulate sending SQL Server DBA health summary
    to Azure Monitor / Log Analytics.

    This is a safe adapter for project review.
    No real Azure connection is executed here.
    """

    try:

        print("\n========================================")
        print(" Azure Monitor Adapter ")
        print("========================================\n")

        azure_payload = {
            "source": "Autonomous-AI-DBA-Operations-Platform",
            "target_service": "Azure Monitor / Log Analytics",
            "integration_mode": "SIMULATED",
            "status": "READY_FOR_AZURE_INTEGRATION",
            "health_summary": health_summary,
            "sent_at": str(
                datetime.now()
            )
        }

        print("Target Service : Azure Monitor / Log Analytics")
        print("Mode           : SIMULATED")
        print("Status         : READY_FOR_AZURE_INTEGRATION")
        print("Message        : Health summary prepared for Azure Monitor.")

        return {
            "overall_status": "READY_FOR_AZURE_INTEGRATION",
            "adapter_name": "AZURE_MONITOR_ADAPTER",
            "message": "Health summary prepared for Azure Monitor integration.",
            "integration_mode": "SIMULATED",
            "azure_payload": azure_payload,
            "created_at": str(
                datetime.now()
            )
        }

    except Exception as error:

        print("\nAzure Monitor Adapter Error:\n")
        print(error)

        return {
            "overall_status": "ERROR",
            "adapter_name": "AZURE_MONITOR_ADAPTER",
            "message": str(
                error
            ),
            "integration_mode": "SIMULATED",
            "azure_payload": None,
            "created_at": str(
                datetime.now()
            )
        }


# =========================================================
# TEST EXECUTION
# =========================================================

if __name__ == "__main__":

    sample_health_summary = {
        "database": "AdventureWorks2019",
        "overall_status": "ATTENTION REQUIRED",
        "issues_detected": [
            "Blocking session detected",
            "Long running query detected",
            "Old backup detected",
            "Failed SQL Agent job detected"
        ]
    }

    result = send_health_summary_to_azure_monitor(
        sample_health_summary
    )

    print("\n========================================")
    print(" AZURE MONITOR ADAPTER RESULT ")
    print("========================================\n")

    print(
        result
    )