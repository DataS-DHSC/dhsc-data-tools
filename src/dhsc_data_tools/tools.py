"""Tooling to work with DAC data."""

import logging

import pandas as pd
import pyodbc
from tqdm import tqdm

from dhsc_data_tools import dac_odbc

_conn = None

logger = logging.getLogger(__name__)


def _handle_client(connection: pyodbc.Connection = None) -> None:
    """Handles connection to the DAC dac_odbc.connect. (Private method.)

    Args:
        connection [Optional] (pyodbc.Connection): ODBC connection object.
            Defaults to None, in which case creates own connection.
    Returns:
        None
    """
    global _conn
    if connection:
        logger.info("Using user defined DAC connection...")
        _conn = connection
    if not _conn:
        logger.info("Setting up DAC connection...")
        _conn = dac_odbc.connect()
    else:
        logger.info("Exisiting connection found...")


def _cursor_to_df(cursor: pyodbc.Connection) -> pd.DataFrame:
    """Low-level implementation to collect query to pd.DataFrame. (Private method.)

    Args:
        connection [Optional] (pyodbc.Connection): ODBC connection object.
            Defaults to None, in which case creates own connection.
    Returns:
        None
    """
    df = pd.DataFrame(
        [tuple(t) for t in tqdm(cursor.fetchall())],
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
    _handle_client(connection=connection)
    cursor = _conn.cursor()
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


def df_from_dataflow(
    dataflow: str, connection: pyodbc.Connection = None
) -> pd.DataFrame:
    """Get data into a pandas DataFrame. Either custom SQL query, or full dataflow path.

    Args:
        dataflow (str): full dataflow path. (Pass either dataflow or sql.)
        connection [Optional] (pyodbc.Connection): ODBC connection object.
            Defaults to None, in which case creates own connection.
    Returns:
        pd.DataFrame
    """
    query_string = f"""
        SELECT * 
        FROM {dataflow}
        """
    cursor = _query_databricks(sql_query=query_string, connection=connection)
    df = _cursor_to_df(cursor)

    return df


def df_from_sql(sql: str, connection: pyodbc.Connection = None) -> pd.DataFrame:
    """Get data into a pandas DataFrame. Either custom SQL query, or full dataflow path.

    Args:
        sql (str): sql query.
        connection [Optional] (pyodbc.Connection): ODBC connection object.
            Defaults to None, in which case creates own connection.
    Returns:
        pd.DataFrame
    """
    cursor = _query_databricks(sql_query=sql, connection=connection)
    df = _cursor_to_df(cursor)

    return df
