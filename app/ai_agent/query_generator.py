# =========================================================
# Query Generator
# =========================================================

def generate_query(

    task

):

    query_map = {

        "CHECK_CPU":

        """
        SELECT TOP 10 *
        FROM sys.dm_exec_requests
        ORDER BY cpu_time DESC
        """,

        "CHECK_BLOCKING":

        """
        SELECT *
        FROM sys.dm_exec_requests
        WHERE blocking_session_id <> 0
        """,

        "CHECK_LONG_RUNNING_QUERIES":

        """
        SELECT *
        FROM sys.dm_exec_requests
        WHERE total_elapsed_time > 60000
        """

    }

    return query_map.get(

        task,

        None

    )