# =========================================================
# SQL Action Executor
# =========================================================

def generate_sql_action(

    recommendation

):

    action_type = (

        recommendation[
            "action_type"
        ]
    )

    if action_type == "UPDATE_STATISTICS":

        return {

            "action_type":
            action_type,

            "sql":
            """
            UPDATE STATISTICS
            Sales.SalesOrderHeader;
            """
        }

    if action_type == "INDEX_REBUILD":

        return {

            "action_type":
            action_type,

            "sql":
            """
            ALTER INDEX ALL
            ON Sales.SalesOrderHeader
            REBUILD;
            """
        }

    if action_type == "BLOCKING_INVESTIGATION":

        return {

            "action_type":
            action_type,

            "sql":
            """
            SELECT
                blocking_session_id,
                session_id
            FROM sys.dm_exec_requests
            WHERE blocking_session_id <> 0;
            """
        }

    return {

        "action_type":
        "NO_ACTION",

        "sql":
        None

    }