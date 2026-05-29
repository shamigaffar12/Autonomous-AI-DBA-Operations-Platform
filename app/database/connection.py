# =========================================================
# Database Connection Module
# Autonomous AI DBA Operations Platform
# =========================================================

# Import required libraries
import pyodbc
import os

from dotenv import load_dotenv


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()


# =========================================================
# SQL SERVER CONFIGURATION
# =========================================================

server = os.getenv(
    "DB_SERVER"
)

database = os.getenv(
    "DB_DATABASE"
)

username = os.getenv(
    "DB_USERNAME"
)

password = os.getenv(
    "DB_PASSWORD"
)


# =========================================================
# CREATE DATABASE CONNECTION FUNCTION
# =========================================================

def get_sql_connection():

    """
    Create and return SQL Server connection.
    """

    try:

        connection = pyodbc.connect(

            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={server};"
            f"DATABASE={database};"
            f"UID={username};"
            f"PWD={password};"
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

    print(f"DB_SERVER   : {server}")
    print(f"DB_DATABASE : {database}")

    connection = get_sql_connection()

    if connection:

        print("\nSQL Server connection successful.")

        try:

            cursor = connection.cursor()

            cursor.execute(
                "SELECT DB_NAME()"
            )

            current_db = cursor.fetchone()[0]

            print(
                f"Connected Database : {current_db}"
            )

            cursor.close()

        except Exception as error:

            print(
                "\nDatabase Verification Error:\n"
            )

            print(error)

        connection.close()

    else:

        print(
            "\nSQL Server connection failed."
        )