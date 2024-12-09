import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

def upload_documents_batch(client, documents):
    results = client.upload_documents(documents)
    if all(result.succeeded for result in results):
        print(f"Batch of {len(documents)} documents copied successfully!")
    else:
        print("Some documents failed to copy.")
        for result in results:
            if not result.succeeded:
                print(f"Failed document key: {result.key}")

# Put these values in a local .env file (or in your environment variables)
load_dotenv()

source_endpoint = os.getenv("SOURCE_ENDPOINT") # full URL
source_index_name = os.getenv("SOURCE_INDEX_NAME")
source_key = os.getenv("SOURCE_KEY")

target_endpoint = os.getenv("TARGET_ENDPOINT") # full URL
target_index_name = os.getenv("TARGET_INDEX_NAME")
target_key = os.getenv("TARGET_KEY")

print(f"Copying data from source (Endpoint: {source_endpoint}, Index: {source_index_name}) to target (Endpoint: {target_endpoint}, Index: {target_index_name})")

if source_key:
    source_credential = AzureKeyCredential(source_key)
else:
    source_credential = DefaultAzureCredential()

if target_key:
    target_credential = AzureKeyCredential(target_key)
else:
    target_credential = DefaultAzureCredential()

# Create a client to connect to the source search service
source_client = SearchClient(
    endpoint=source_endpoint,
    index_name=source_index_name,
    credential=source_credential
)

# Create a client to connect to the target search service
target_client = SearchClient(
    endpoint=target_endpoint,
    index_name=target_index_name,
    credential=target_credential
)

# Read and upload documents in batches of 500
batch_size = 500
current_skip = 0

while True:
    results = source_client.search(
        search_text="*",
        top=batch_size,
        skip=current_skip,
        include_total_count=True
    )

    documents = [result for result in results]
    upload_documents_batch(target_client, documents)
    
    current_skip += batch_size

    # Break if no more results
    if current_skip >= results.get_count():
        break

print("Documents copied successfully!")
