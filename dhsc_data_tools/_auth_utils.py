"""Authentication utilities.

These functions support underlying processes.
They are not meant to be called directly.
"""

import hashlib
import json
import os
import warnings
from pathlib import Path
from typing import TypedDict

import platformdirs
from azure.identity import (
    AuthenticationRecord,
    InteractiveBrowserCredential,
    TokenCachePersistenceOptions,
)

from dhsc_data_tools import _constants


class AuthRecordHashParams(TypedDict):
    authority: str
    client_id: str
    tenant_id: str


def _return_tenant_id() -> str:
    """Find DAC_TENANT (tenant name) environment variable."""
    tenant_id = os.getenv("DAC_TENANT")
    if tenant_id is None:
        raise KeyError(
            """
            DAC_TENANT environment variable not found.
            Make sure DAC_TENANT is in your .env file
            and .env file is loaded.
            """,
        )

    return tenant_id


def _get_authentication_record_filename(params: AuthRecordHashParams) -> str:
    """Get auth record hashed filename."""
    params.setdefault("version", "1.0")  # type: ignore
    return hashlib.sha256(
        json.dumps(params, sort_keys=True).encode("utf-8"),
    ).hexdigest()


def _get_authentication_record_path(params: AuthRecordHashParams) -> Path:
    """Get auth record path."""
    ar_base = Path(platformdirs.user_data_dir("dhsc_data_tools", "python"))
    if not ar_base.is_dir():
        warnings.warn(
            (
                f"Creating a user data folder to save credentials to at"
                f"{ar_base}"
            ),
            stacklevel=2,
        )
    ar_base.mkdir(parents=True, exist_ok=True)

    return ar_base / _get_authentication_record_filename(params)


def _read_authentication_record(
    authentication_record_path: Path,
    use_cache: bool = True,
) -> AuthenticationRecord | None:
    """Read authentication record."""
    if (not use_cache) or (not authentication_record_path.is_file()):
        return None

    with authentication_record_path.open(encoding="utf-8") as infile:
        return AuthenticationRecord.deserialize(infile.read())


def _write_authentication_record(
    authentication_record_path: Path,
    authentication_record: AuthenticationRecord | None = None,
) -> None:
    """Write auth record if authentication_record else return None."""
    if authentication_record is None:
        return

    with authentication_record_path.open("w", encoding="utf-8") as outfile:
        outfile.write(authentication_record.serialize())


def _return_credential(
    refresh_token: bool = False,
) -> InteractiveBrowserCredential:
    """Return an interactive browser credential object."""
    tenant_id = _return_tenant_id()

    # Authentication process, attempts cached authentication first
    authentication_record_path = _get_authentication_record_path(
        AuthRecordHashParams(
            authority=_constants._AUTHORITY,
            client_id=_constants._CLIENT_ID,
            tenant_id=tenant_id,
        ),
    )

    if refresh_token:
        authentication_record = None
    else:
        authentication_record = _read_authentication_record(
            authentication_record_path,
        )

    # Return credentia
    credential = InteractiveBrowserCredential(
        client_id=_constants._CLIENT_ID,
        cache_persistence_options=TokenCachePersistenceOptions(),
        additionally_allowed_tenants=["*"],
        tenant_id=tenant_id,
        authentication_record=authentication_record,
    )

    if authentication_record is None:
        _write_authentication_record(
            authentication_record_path,
            credential.authenticate(),
        )

    return credential
