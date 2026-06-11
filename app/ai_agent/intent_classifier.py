# =========================================================
# Intent Classifier
# Autonomous AI DBA Operations Platform
# =========================================================

def classify_intent(user_command):
    """
    Classify user command into DBA operational intent.
    """

    command = user_command.upper()

    if (
        "DAILY" in command
        or "HEALTH CHECK" in command
        or "DBA HEALTH" in command
        or "CHECK SQL SERVER HEALTH" in command
    ):
        return {
            "intent": "DAILY_HEALTH_CHECK",
            "confidence": 95,
            "description": "Run complete DBA daily health check"
        }

    if (
        "FAILED JOB" in command
        or "SQL JOB" in command
        or "JOB FAILURE" in command
    ):
        return {
            "intent": "FAILED_JOB_CHECK",
            "confidence": 90,
            "description": "Analyze failed SQL Server jobs"
        }

    if (
        "BACKUP" in command
        or "BACKUP STATUS" in command
        or "DATABASE BACKUP" in command
    ):
        return {
            "intent": "BACKUP_HEALTH_CHECK",
            "confidence": 90,
            "description": "Analyze database backup status"
        }

    if (
        "BLOCKING" in command
        or "BLOCKED SESSION" in command
        or "LOCK" in command
    ):
        return {
            "intent": "BLOCKING_ANALYSIS",
            "confidence": 90,
            "description": "Analyze blocking sessions"
        }

    if (
        "LONG RUNNING" in command
        or "SLOW QUERY" in command
        or "PERFORMANCE" in command
        or "QUERY PERFORMANCE" in command
    ):
        return {
            "intent": "PERFORMANCE_ANALYSIS",
            "confidence": 90,
            "description": "Analyze SQL Server performance issues"
        }

    if (
        "SPACE" in command
        or "DATABASE SIZE" in command
        or "DISK" in command
        or "GROWTH" in command
    ):
        return {
            "intent": "SPACE_ANALYSIS",
            "confidence": 90,
            "description": "Analyze database space usage"
        }

    return {
        "intent": "GENERAL_HEALTH_CHECK",
        "confidence": 70,
        "description": "Run general SQL Server health check"
    }


# =========================================================
# TEST EXECUTION
# =========================================================

if __name__ == "__main__":

    command = "Run daily DBA health check"

    result = classify_intent(command)

    print("\n========================================")
    print(" INTENT CLASSIFICATION RESULT ")
    print("========================================\n")

    print(result)