import os
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

# Replace these variables with your Azure Cognitive Search details
source_endpoint = "source-endpoint"
source_index_name = "source-index"
source_key = ""

target_endpoint = "target-endpoint"
target_index_name = "target-index"
target_key = ""

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
