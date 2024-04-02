'''
These functions support underlying authentication processes.
They are not meant to be called directly.
'''

import hashlib
import json
from pathlib import Path
from azure.identity import AuthenticationRecord
import platformdirs


def get_authentication_record_filename(**kwargs):
    kwargs.setdefault("version", "1.0")
    kwargs_hash = hashlib.sha1(
        json.dumps(kwargs, sort_keys=True).encode("utf-8")
    ).hexdigest()

    return kwargs_hash + '.txt'


def get_authentication_record_path(**kwargs):
    print("Creating a user data folder and storing credentials in it...")
    ar_base = Path(platformdirs.user_data_dir("dhsc_data_tools", "python"))
    ar_base.mkdir(parents=True, exist_ok=True)

    return ar_base / get_authentication_record_filename(**kwargs)


def read_authentication_record(authentication_record_path, use_cache=True):
    if (not use_cache) or (not authentication_record_path.is_file()):
        return None

    with open(authentication_record_path, "rt", encoding="utf-8") as infile:
        ar = AuthenticationRecord.deserialize(infile.read())

    return ar


def write_authentication_record(authentication_record_path, authentication_record=None):
    if authentication_record is None:
        return None

    with open(authentication_record_path, "wt", encoding="utf-8") as outfile:
        outfile.write(authentication_record.serialize())
