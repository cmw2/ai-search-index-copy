import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import SearchIndex

# Put these values in a local .env file (or in your environment variables)
load_dotenv()

source_endpoint = os.getenv("SOURCE_ENDPOINT") # full URL
source_index_name = os.getenv("SOURCE_INDEX_NAME")
source_key = os.getenv("SOURCE_KEY")

target_endpoint = os.getenv("TARGET_ENDPOINT") # full URL
target_index_name = os.getenv("TARGET_INDEX_NAME")
target_key = os.getenv("TARGET_KEY")

print(f"Copying index schema from source (Endpoint: {source_endpoint}, Index: {source_index_name}) to target (Endpoint: {target_endpoint}, Index: {target_index_name})")

if source_key:
    source_credential = AzureKeyCredential(source_key)
else:
    source_credential = DefaultAzureCredential()

if target_key:
    target_credential = AzureKeyCredential(target_key)
else:
    target_credential = DefaultAzureCredential()

# Create a client to connect to the source search service
source_client = SearchIndexClient(
    endpoint=source_endpoint,
    index_name=source_index_name,
    credential=source_credential
)

# Create a client to connect to the target search service
target_client = SearchIndexClient(
    endpoint=target_endpoint,
    index_name=target_index_name,
    credential=target_credential
)

source_index_definition = source_client.get_index(source_index_name)
source_index_definition.name = target_index_name
target_client.create_or_update_index(source_index_definition)
print("Index schema copied successfully!")
