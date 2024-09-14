# uploader/azure_blob_service.py
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from django.conf import settings
import os

class AzureBlobService:
    def __init__(self):
        # Initialize the BlobServiceClient using the connection string or account details
        self.blob_service_client = BlobServiceClient(
            account_url=f"https://{settings.AZURE_STORAGE_ACCOUNT_NAME}.blob.core.windows.net",
            credential=settings.AZURE_STORAGE_ACCOUNT_KEY
        )
        self.container_client = self.blob_service_client.get_container_client(settings.AZURE_BLOB_CONTAINER)

    def upload_file(self, file, file_name):
        """
        Uploads a file to Azure Blob Storage.
        :param file: The file object to upload.
        :param file_name: The name of the file in Blob Storage.
        :return: URL of the uploaded file.
        """
        try:
            # Get a blob client
            blob_client = self.container_client.get_blob_client(file_name)
            # Upload the file to Azure Blob Storage
            blob_client.upload_blob(file)
            # Return the URL of the uploaded file
            return f"https://{settings.AZURE_CUSTOM_DOMAIN}/{settings.AZURE_BLOB_CONTAINER}/{file_name}"
        except Exception as e:
            print(f"Error uploading file: {e}")
            return None

    def delete_file(self, file_name):
        """
        Deletes a file from Azure Blob Storage.
        :param file_name: The name of the file to delete.
        """
        try:
            blob_client = self.container_client.get_blob_client(file_name)
            blob_client.delete_blob()
        except Exception as e:
            print(f"Error deleting file: {e}")
