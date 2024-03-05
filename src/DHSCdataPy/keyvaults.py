import os
from azure.keyvault.secrets import SecretClient
from azure.identity import InteractiveBrowserCredential
from pypac import pac_context_for_url

from dotenv import load_dotenv

