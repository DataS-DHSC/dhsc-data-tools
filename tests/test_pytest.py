import time
import pytest
from pypac import pac_context_for_url
from dhsc_data_tools.dac_odbc import connect
from dhsc_data_tools.keyvault import KVConnection
from dhsc_data_tools.remote_compute import connect_cluster

from dotenv import load_dotenv

load_dotenv(".env")

# Defining test cases


def test_keyvaultconnection():
    """
    Test Azure keyvault connection.
    """
    with pac_context_for_url("https://www.google.co.uk"):
        kvc = KVConnection("DEV")
        my_key = kvc.get_secret("dummy-example-key")
    assert my_key == "123456789"
    time.sleep(3)


def test_dac_odbc_connect():
    """
    Test ODBC driver connection.
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM samples.nyctaxi.trips LIMIT 10")
    columns = [column[0] for column in cursor.description]
    assert columns[0] == "tpep_pickup_datetime"
    conn.close()
    time.sleep(3)


def test_remote_compute_connect():
    """
    Test the running code on a dbricks compute cluster.
    """
    pass
