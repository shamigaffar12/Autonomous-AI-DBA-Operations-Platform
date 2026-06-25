# =========================================================
# Application Database Helper
# Autonomous AI DBA Operations Platform
# =========================================================

import os
from contextlib import contextmanager
from typing import Iterator, Optional

import pyodbc


def get_app_db_connection_string() -> str:

    connection_string = os.getenv(
        "APP_DB_CONNECTION_STRING",
        ""
    ).strip()

    if connection_string:
        return connection_string

    server = os.getenv(
        "APP_DB_SERVER",
        "localhost"
    )

    database = os.getenv(
        "APP_DB_NAME",
        "AI_DBA_PLATFORM"
    )

    username = os.getenv(
        "APP_DB_USERNAME",
        ""
    )

    password = os.getenv(
        "APP_DB_PASSWORD",
        ""
    )

    driver = os.getenv(
        "APP_DB_DRIVER",
        "ODBC Driver 17 for SQL Server"
    )

    trust_cert = os.getenv(
        "APP_DB_TRUST_SERVER_CERTIFICATE",
        "yes"
    )

    if username and password:
        return (
            f"DRIVER={{{driver}}};"
            f"SERVER={server};"
            f"DATABASE={database};"
            f"UID={username};"
            f"PWD={password};"
            f"TrustServerCertificate={trust_cert};"
        )

    return (
        f"DRIVER={{{driver}}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"Trusted_Connection=yes;"
        f"TrustServerCertificate={trust_cert};"
    )


@contextmanager
def app_db_connection() -> Iterator[pyodbc.Connection]:

    connection: Optional[pyodbc.Connection] = None

    try:
        connection = pyodbc.connect(
            get_app_db_connection_string(),
            timeout=15
        )

        yield connection

        connection.commit()

    except Exception:

        if connection:
            connection.rollback()

        raise

    finally:

        if connection:
            connection.close()