import uuid
import datetime
from celery import shared_task
from azure.storage.blob import BlobServiceClient, BlobSasPermissions
from azure.cosmos import CosmosClient
from django.conf import settings

@shared_task
def generate_and_store_url(document_reference, expiration_in_minutes):
    # Generate a unique ID and expiration date
    unique_id = str(uuid.uuid4())
    expiration_date = datetime.datetime.utcnow() + datetime.timedelta(minutes=expiration_in_minutes)
    expiration_timestamp = expiration_date.isoformat()

    # Create a temporary SAS URL with the expiration date
    blob_service_client = BlobServiceClient.from_connection_string(settings.AZURE_BLOB_CONNECTION_STRING)
    blob_client = blob_service_client.get_blob_client(container=settings.AZURE_BLOB_CONTAINER_NAME, blob=document_reference)

    sas_token = blob_client.generate_shared_access_signature(
        permission=BlobSasPermissions(read=True),
        expiry=expiration_date
    )
    download_url = f"{blob_client.url}?{sas_token}"

    # Store URL and expiration details in Cosmos DB
    cosmos_client = CosmosClient(settings.AZURE_COSMOS_DB_ENDPOINT, settings.AZURE_COSMOS_DB_KEY)
    database = cosmos_client.get_database_client(settings.AZURE_COSMOS_DB_DATABASE)
    container = database.get_container_client(settings.AZURE_COSMOS_DB_CONTAINER)

    item = {
        "id": unique_id,
        "document_reference": document_reference,
        "download_url": download_url,
        "expiration_date": expiration_timestamp
    }
    container.create_item(item)

    return download_url
