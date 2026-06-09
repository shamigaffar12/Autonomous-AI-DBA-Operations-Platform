# =========================================================
# SQL Risk Analyzer
# Autonomous AI DBA Operations Platform
# =========================================================


# =========================================================
# ANALYZE SQL RISK
# =========================================================

def analyze_sql_risk(

    sql_action

):

    """
    Analyze generated SQL action
    and determine execution risk.
    """

    action_type = (

        sql_action.get(

            "action_type",

            "UNKNOWN"

        )

    )

    sql = (

        sql_action.get(

            "sql",

            ""

        )

    )

    # =====================================================
    # NO ACTION
    # =====================================================

    if action_type == "NO_ACTION":

        return {

            "risk":
            "NONE",

            "approval_required":
            False,

            "destructive":
            False,

            "rollback_required":
            False

        }

    # =====================================================
    # DANGEROUS SQL DETECTION
    # =====================================================

    sql_upper = sql.upper()

    dangerous_keywords = [

        "DROP ",

        "TRUNCATE ",

        "DELETE ",

        "ALTER DATABASE",

        "SHUTDOWN",

        "DROP TABLE",

        "DROP DATABASE",

        "DROP INDEX",

        "KILL ",

        "DBCC SHRINKDATABASE"

    ]

    for keyword in dangerous_keywords:

        if keyword in sql_upper:

            return {

                "risk":
                "HIGH",

                "approval_required":
                True,

                "destructive":
                True,

                "rollback_required":
                True

            }

    # =====================================================
    # LOW RISK ACTIONS
    # =====================================================

    low_risk_actions = [

        "BLOCKING_INVESTIGATION",

        "CPU_ANALYSIS",

        "DATABASE_HEALTH_CHECK",

        "QUERY_ANALYSIS",

        "CAPACITY_PLANNING"

    ]

    if action_type in low_risk_actions:

        return {

            "risk":
            "LOW",

            "approval_required":
            False,

            "destructive":
            False,

            "rollback_required":
            False

        }

    # =====================================================
    # MEDIUM RISK ACTIONS
    # =====================================================

    medium_risk_actions = [

        "UPDATE_STATISTICS",

        "INDEX_REBUILD",

        "INDEX_REORGANIZE",

        "INDEX_CREATION"

    ]

    if action_type in medium_risk_actions:

        return {

            "risk":
            "MEDIUM",

            "approval_required":
            True,

            "destructive":
            False,

            "rollback_required":
            False

        }

    # =====================================================
    # DEFAULT UNKNOWN ACTION
    # =====================================================

    return {

        "risk":
        "HIGH",

        "approval_required":
        True,

        "destructive":
        False,

        "rollback_required":
        False

    }


# =========================================================
# TEST EXECUTION
# =========================================================

if __name__ == "__main__":

    sample_action = {

        "action_type":
        "INDEX_REBUILD",

        "sql":
        """
        ALTER INDEX ALL
        ON Sales.SalesOrderHeader
        REBUILD;
        """

    }

    result = (

        analyze_sql_risk(

            sample_action

        )

    )

    print(

        "\nSQL Risk Analysis:\n"

    )

    print(

        result

    )