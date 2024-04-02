"""
These functions support underlying authentication processes.
They are not meant to be called directly.
"""

import hashlib
import json
from pathlib import Path
import platformdirs
from azure.identity import InteractiveBrowserCredential
from azure.identity import AuthenticationRecord


def get_authentication_record_filename(**kwargs):
    """
    Get auth record hashed filename.
    """
    kwargs.setdefault("version", "1.0")
    kwargs_hash = hashlib.sha1(
        json.dumps(kwargs, sort_keys=True).encode("utf-8")
    ).hexdigest()

    return kwargs_hash + ".txt"


def get_authentication_record_path(**kwargs):
    """
    Get auth record path.
    """
    ar_base = Path(platformdirs.user_data_dir("dhsc_data_tools", "python"))
    if not ar_base.is_dir():
        print(
            "Creating a user data folder to save credentials to it at ",
            platformdirs.user_data_dir(),
        )
    ar_base.mkdir(parents=True, exist_ok=True)

    return ar_base / get_authentication_record_filename(**kwargs)


def read_authentication_record(authentication_record_path, use_cache=True):
    """
    Reads authentication record.
    """
    if (not use_cache) or (not authentication_record_path.is_file()):
        return None

    with open(authentication_record_path, "rt", encoding="utf-8") as infile:
        auth_rec = AuthenticationRecord.deserialize(infile.read())

    return auth_rec


def write_authentication_record(authentication_record_path, authentication_record=None):
    """
    Write auth record if authentication_record return is other than None type.
    """
    if authentication_record is None:
        pass

    with open(authentication_record_path, "wt", encoding="utf-8") as outfile:
        outfile.write(authentication_record.serialize())


def return_credential(client_id, tenant_id, cache_options, authentication_record):
    """
    Returns an interactive
    """
    credential = InteractiveBrowserCredential(
        client_id=client_id,
        cache_persistence_options=cache_options,
        additionally_allowed_tenants=["*"],
        tenant_id=tenant_id,
        authentication_record=authentication_record,
    )

    return credential


def check_auth_record(
    credential, authentication_record, authentication_record_path, scope
):
    """
    If there is no cached auth record, reauthenticate
    """
    if authentication_record is None:
        write_authentication_record(
            authentication_record_path, credential.authenticate(scopes=[scope])
        )
