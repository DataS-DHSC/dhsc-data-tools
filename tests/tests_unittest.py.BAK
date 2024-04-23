import os
import time
from pypac import pac_context_for_url
import unittest
from dhsc_data_tools.dac_odbc import connect
from dhsc_data_tools.keyvault import KVConnection
from dhsc_data_tools.remote_compute import connect_cluster

from dotenv import load_dotenv
load_dotenv("../../dhsc_data_tools_dumps/.env")

class Tests(unittest.TestCase):
    '''
    Test case, currently tests:
    - dhsc_data_tools.keyvault.kvConnection
    - dhsc_data_tools.dac_odbc.connect

    Later will add:
    - dhsc_data_tools.remote_compute.connect_cluster
    '''

    def test_keyvaultconnection(self):
        with pac_context_for_url("https://www.google.co.uk"):
            kvc = KVConnection("DEV")
            my_key = kvc.get_secret('dummy-example-key')
        self.assertEqual(my_key, '123456789')
        time.sleep(3)

    def test_dac_odbc_connect(self):
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM samples.nyctaxi.trips LIMIT 10")
        columns = [column[0] for column in cursor.description]
        self.assertEqual(columns[0], "tpep_pickup_datetime")
        conn.close()
        #time.sleep(3)

    def test_remote_compute_connect_cluster(self):
        pass

if __name__ == '__main__':
    unittest.main()