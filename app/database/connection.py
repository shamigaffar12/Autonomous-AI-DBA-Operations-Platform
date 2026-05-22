# =========================================================
# Database Connection Module
# Autonomous AI DBA Operations Platform
# =========================================================

# Import required library
import pyodbc


# =========================================================
# SQL SERVER CONFIGURATION
# =========================================================

# SQL Server name
server = "ICS-LT-4V2CJ84\\SQLEXPRESS"


# Database name
database = "master"


# =========================================================
# CREATE DATABASE CONNECTION FUNCTION
# =========================================================

def get_sql_connection():

    """
    Create and return SQL Server connection.
    """

    try:

        # Create SQL connection
        connection = pyodbc.connect(

            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={server};"
            f"DATABASE={database};"
            "Trusted_Connection=yes;"
        )

        return connection


    except Exception as error:

        print("\nDatabase Connection Error:\n")

        print(error)

        return None
    
    # =========================================================
# CONNECTION TEST
# =========================================================

if __name__ == "__main__":

    print("\nTesting SQL Connection...\n")

    connection = get_sql_connection()

    if connection:

        print("SQL Server connection successful.")

        connection.close()

    else:

        print("SQL Server connection failed.")