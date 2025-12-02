"""Tooling to work with DAC data."""

import logging
import warnings

import pandas as pd
import pyodbc

from dhsc_data_tools import dac_odbc
from dhsc_data_tools._backend_utils import _Sentinel

_conn = None

_sentinel = _Sentinel()

logger = logging.getLogger(__name__)


def _get_client(connection: pyodbc.Connection = None) -> None:
    """Handles connection to the DAC dac_odbc.connect. (Private method.)

    Args:
        connection [Optional] (pyodbc.Connection): ODBC connection object.
            Defaults to None, in which case creates own connection.
    Returns:
        None
    """
    global _conn
    if connection:
        _conn = connection
    if not _conn:
        _conn = dac_odbc.connect()

    return _conn


def _cursor_to_df(cursor: pyodbc.Connection) -> pd.DataFrame:
    """Low-level implementation to collect query to pd.DataFrame. (Private method.)

    Args:
        connection [Optional] (pyodbc.Connection): ODBC connection object.
            Defaults to None, in which case creates own connection.
    Returns:
        None
    """
    df = pd.DataFrame(
        [tuple(t) for t in cursor.fetchall()],
        columns=[i[0] for i in cursor.description],
    )

    return df


def _query_databricks(
    sql_query: str, connection: pyodbc.Connection = None
) -> pyodbc.Cursor:
    """Sends SQL query to the DAC over a connection. (Private method.)

    Args:
        sql_query (str): and sql query as string.
        connection [Optional] (pyodbc.Connection): ODBC connection object.
            Defaults to None, in which case creates own connection.
    Returns:
        pyodbc.Cursor
    """
    conn = _get_client(connection=connection)
    cursor = conn.cursor()
    cursor.execute(sql_query)

    return cursor


def get_catalogs(connection: pyodbc.Connection = None) -> pd.DataFrame:
    """Gets catalogs on the DAC.

    Args:
        connection [Optional] (pyodbc.Connection): ODBC connection object.
            Defaults to None, in which case creates own connection.
    Returns:
        pd.DataFrame
    """
    cursor = _query_databricks(sql_query="SHOW CATALOGS", connection=connection)
    df = _cursor_to_df(cursor)

    return df


def get_schemas(catalog: str, connection: pyodbc.Connection = None) -> pd.DataFrame:
    """Gets all schemas within the catalog.

    Args:
        catalog (str): catalog name.
        connection [Optional] (pyodbc.Connection): ODBC connection object.
            Defaults to None, in which case creates own connection.
    Returns:
        pd.DataFrame
    """
    cursor = _query_databricks(
        sql_query=f"SHOW SCHEMAS IN {catalog}", connection=connection
    )
    df = _cursor_to_df(cursor)

    return df


def get_tables(
    catalog: str, schema: str, connection: pyodbc.Connection = None
) -> pd.DataFrame:
    """Gets all tables within a given schema.

    Args:
        catalog (str): catalog name.
        schema (str): schema name.
        connection [Optional] (pyodbc.Connection): ODBC connection object.
            Defaults to None, in which case creates own connection.
    Returns:
        pd.DataFrame
    """
    cursor = _query_databricks(
        f"SHOW TABLES IN {catalog}.{schema}", connection=connection
    )
    df = _cursor_to_df(cursor)

    return df


def get_table_info(
    catalog: str, schema: str, table: str, connection: pyodbc.Connection = None
) -> pd.DataFrame:
    """Gets table description of a given table.

    Args:
        catalog (str): catalog name.
        schema (str): schema name.
        table (str): table name.
        connection [Optional] (pyodbc.Connection): ODBC connection object.
            Defaults to None, in which case creates own connection.
    Returns:
        pd.DataFrame
    """
    cursor = _query_databricks(
        f"DESCRIBE TABLE EXTENDED {catalog}.{schema}.{table}", connection=connection
    )
    df = _cursor_to_df(cursor)

    return df


def df_from_sql(sql: str, connection: pyodbc.Connection = None) -> pd.DataFrame:
    """Load data as pandas.DataFrame from a custom SQL query.

    Args:
        sql (str): SQL query.
        connection [Optional] (pyodbc.Connection): ODBC connection object.
            Defaults to None, in which case creates own connection.
    Returns:
        pd.DataFrame
    """
    cursor = _query_databricks(sql_query=sql, connection=connection)
    df = _cursor_to_df(cursor)

    return df


def df_from_dataflow(
    dataflow: str,
    limit: int | _Sentinel | None = _sentinel,
    columns: list[str] | None = None,
    connection: pyodbc.Connection = None,
) -> pd.DataFrame:
    """Load data as pandas.DataFrame from a dataflow path.

    Args:
        dataflow (str): Full dataflow path.
        limit (int | None | _SentinelType):
            - `_sentinel` → argument not passed (defaults to 10)
            - `None` → load full dataset
            - `int` → limit rows
        columns (list[str] | None): Columns to select.
        connection (pyodbc.Connection | None): ODBC connection object.
            Defaults to None, creates its own connection.

    Returns:
        pd.DataFrame
    """
    # Validate limit
    if limit not in (_sentinel, None) and not isinstance(limit, int):
        raise ValueError("`limit` must be int or None.")

    # Validate columns
    if columns is not None:
        if not (isinstance(columns, list) and all(isinstance(c, str) for c in columns)):
            raise ValueError("`columns` must be a list of strings.")
        cols_string = ", ".join(columns)
    else:
        warnings.warn("Consider passing `columns` to load only what you need.")
        cols_string = "*"

    # Build query
    if limit is _sentinel:
        warnings.warn(
            "No `limit` provided. Defaulting to 10 rows to avoid performance issues."
        )
        query = f"SELECT {cols_string} FROM {dataflow} LIMIT 10;"
    elif limit is None:
        warnings.warn("Loading the entire dataset. This may impact performance.")
        query = f"SELECT {cols_string} FROM {dataflow};"
    else:
        query = f"SELECT {cols_string} FROM {dataflow} LIMIT {limit};"

    # Execute query
    df = df_from_sql(sql=query, connection=connection)

    return df
