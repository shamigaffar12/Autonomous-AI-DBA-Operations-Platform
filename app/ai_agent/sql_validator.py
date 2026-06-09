# =========================================================
# SQL Validator
# =========================================================

def validate_sql_action(sql_action):

    """
    Validate generated SQL action.
    """

    sql = sql_action.get("sql")

    # =====================================================
    # NO ACTION
    # =====================================================

    if not sql:

        return {

            "approved": False,

            "reason": "No SQL generated"

        }

    sql_upper = sql.upper()

    # =====================================================
    # BLOCK DANGEROUS COMMANDS
    # =====================================================

    blocked_keywords = [

        "DROP ",
        "TRUNCATE ",
        "DELETE ",
        "SHUTDOWN ",
        "ALTER DATABASE "

    ]

    for keyword in blocked_keywords:

        if keyword in sql_upper:

            return {

                "approved": False,

                "reason": f"Blocked keyword detected: {keyword}"

            }

    # =====================================================
    # APPROVED
    # =====================================================

    return {

        "approved": True,

        "reason": "SQL validated successfully"

    }


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    print(

        validate_sql_action({

            "action_type": "NO_ACTION",

            "sql": None

        })

    )