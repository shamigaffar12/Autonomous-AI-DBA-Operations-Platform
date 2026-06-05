# =========================================================
# Configuration Manager
# Autonomous AI DBA Operations Platform
# =========================================================


# =========================================================
# DATABASE CONFIGURATION
# =========================================================

SQL_SERVER = "localhost"

DATABASE_NAME = "AdventureWorks2019"


# =========================================================
# AI CONFIGURATION
# =========================================================

OPENROUTER_API_KEY = "YOUR_API_KEY"

AI_MODEL = "openrouter"


# =========================================================
# STORAGE CONFIGURATION
# =========================================================

REPORT_FOLDER = "reports"

AUDIT_FOLDER = "audit_logs"


# =========================================================
# MONITORING THRESHOLDS
# =========================================================

CPU_THRESHOLD = 10000

LONG_QUERY_THRESHOLD = 30000


# =========================================================
# NOTIFICATION CONFIGURATION
# =========================================================

EMAIL_ENABLED = True

TEAMS_ENABLED = True


# =========================================================
# SCHEDULER CONFIGURATION
# =========================================================

SCHEDULER_ENABLED = True

SCHEDULER_INTERVAL_SECONDS = 30