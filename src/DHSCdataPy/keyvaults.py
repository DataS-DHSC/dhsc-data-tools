import os
from azure.keyvault.secrets import SecretClient
from azure.identity import InteractiveBrowserCredential
from pypac import pac_context_for_url

from dotenv import load_dotenv

def find_secret(key_vault_name, secret_name):

    VAULT_NAME = os.environ["KEY_VAULT_NAME"]

    KVUri = f"https://{VAULT_NAME}.vault.azure.net"

    credential = InteractiveBrowserCredential(authority="https://login.microsoftonline.com/",
                                            tenant_id=os.environ["TENANT_ID"], 
                                            client_id=os.environ["CLIENT_ID"], 
                                            )

    client = SecretClient(vault_url=KVUri, credential=credential)

    with pac_context_for_url("https://www.google.co.uk/"):
        # get dummy-example-key
        this_secret = client.get_secret('dummy-example-key')

    return this_secret