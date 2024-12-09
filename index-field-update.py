import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

# Load environment variables
load_dotenv()
source_endpoint = os.getenv("TARGET_ENDPOINT")
source_index_name = os.getenv("TARGET_INDEX_NAME")
api_key = os.getenv("TARGET_KEY")

if api_key:
    credential = AzureKeyCredential(api_key)
else:
    credential = DefaultAzureCredential()

# Create a client to connect to the search service
search_client = SearchClient(
    endpoint=source_endpoint,
    index_name=source_index_name,
    credential=credential
)

# The field to search and update
search_field = "source"
search_value = "https://strchysn5ma5ssya.blob.core.windows.net/documents/DOM-part-1.pdf_SAS_TOKEN_PLACEHOLDER_"
update_field = "source"
new_value = "https://strchysn5ma5ssya.blob.core.windows.net/documents/DOM-part-1.pdf"

# Search for documents
results = search_client.search(search_text=f"{search_field}:{search_value}")

# Update documents
documents_to_update = []
for result in results:
    doc_id = result["id"]
    documents_to_update.append({
        "id": doc_id,
        update_field: new_value
    })

# Upload the updated documents
result = search_client.merge_or_upload_documents(documents=documents_to_update)
if all(r.succeeded for r in result):
    print("Documents updated successfully!")
else:
    print("Failed to update some documents.")
    for r in result:
        if not r.succeeded:
            print(f"Failed document key: {r.key}")

print("Operation completed.")
