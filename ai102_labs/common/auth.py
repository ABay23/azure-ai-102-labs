import os
from azure.identity import DefaultAzureCredential
from azure.core.credentials import AzureKeyCredential

def token_credential():
    # Uses az login locally, or managed identity in Azure
    return DefaultAzureCredential()

def key_credential(env_key_name: str):
    return AzureKeyCredential(os.environ[env_key_name])
