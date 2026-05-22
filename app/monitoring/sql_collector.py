# =========================================================
# SQL Monitoring Collector Engine
# Autonomous AI DBA Operations Platform
# =========================================================

# Import shared SQL connection
from app.database.connection import get_sql_connection


# =========================================================
# READ SQL QUERY FROM FILE
# =========================================================

def read_sql_file(file_path):

    # Read SQL query from file

    try:

        with open(file_path, "r") as file:

            query = file.read()
            print(f"\nLoaded SQL File: {file_path}")

        return query


    except Exception as error:

        print("\nSQL File Read Error:\n")

        print(error)

        return None


# =========================================================
# EXECUTE SQL MONITORING QUERY
# =========================================================

def execute_monitoring_query(query):

    # Execute monitoring query and return results

    try:

        # Get SQL connection
        connection = get_sql_connection()


        # Create cursor
        cursor = connection.cursor()


        # Execute query
        cursor.execute(query)


        # Fetch results
        rows = cursor.fetchall()


        # Close connections
        cursor.close()

        connection.close()


        return rows


    except Exception as error:

        print("\nMonitoring Query Error:\n")

        print(error)

        return None