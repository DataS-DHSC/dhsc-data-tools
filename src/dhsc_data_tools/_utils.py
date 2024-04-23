"""
These functions support underlying processes.
They are not meant to be called directly.
"""

import os
import hashlib
import json
import platformdirs
from pathlib import Path
from azure.identity import InteractiveBrowserCredential
from azure.identity import AuthenticationRecord
from azure.identity import TokenCachePersistenceOptions
from dhsc_data_tools import _constants


def _return_tenant_id():
    """
    Find DAC_TENANT (tenant name) environment variable.
    to define tenant_id
    """
    tenant_id = os.getenv("DAC_TENANT")
    if tenant_id is None:
        raise KeyError(
            """
            DAC_TENANT environment variable not found.
            Make sure DAC_TENANT is in your .env file
            and .env file is loaded.
            """
        )

    return tenant_id


def _get_authentication_record_filename(**kwargs):
    """
    Get auth record hashed filename.
    """
    kwargs.setdefault("version", "1.0")
    kwargs_hash = hashlib.sha1(
        json.dumps(kwargs, sort_keys=True).encode("utf-8")
    ).hexdigest()

    return kwargs_hash


def _get_authentication_record_path(**kwargs):
    """
    Get auth record path.
    """
    ar_base = Path(platformdirs.user_data_dir("dhsc_data_tools", "python"))
    if not ar_base.is_dir():
        print("Creating a user data folder to save credentials to it at", ar_base)
    ar_base.mkdir(parents=True, exist_ok=True)

    return ar_base / _get_authentication_record_filename(**kwargs)


def _read_authentication_record(authentication_record_path, use_cache=True):
    """
    Reads authentication record.
    """
    if (not use_cache) or (not authentication_record_path.is_file()):
        return None

    with open(authentication_record_path, "rt", encoding="utf-8") as infile:
        auth_rec = AuthenticationRecord.deserialize(infile.read())

    return auth_rec


def _write_authentication_record(
    authentication_record_path, authentication_record=None
):
    """
    Write auth record if authentication_record return is other than None type.
    """
    if authentication_record is None:
        pass

    with open(authentication_record_path, "wt", encoding="utf-8") as outfile:
        outfile.write(authentication_record.serialize())


def _return_credential(tenant_id: str, refresh_token: bool = False):
    """
    Returns an interactive browser credential object.
    """

    # Authentication process, attempts cached authentication first
    authentication_record_path = _get_authentication_record_path(
        authority=_constants._authority,
        clientId=_constants._client_id,
        tenantId=tenant_id,
    )

    authentication_record = _read_authentication_record(authentication_record_path)

    if refresh_token == True:
        authentication_record = None

    # Return credentia
    credential = InteractiveBrowserCredential(
        client_id=_constants._client_id,
        cache_persistence_options=TokenCachePersistenceOptions(),
        additionally_allowed_tenants=["*"],
        tenant_id=tenant_id,
        authentication_record=authentication_record,
    )

    if authentication_record is None:
        _write_authentication_record(
            authentication_record_path, credential.authenticate()
        )

    return credential
