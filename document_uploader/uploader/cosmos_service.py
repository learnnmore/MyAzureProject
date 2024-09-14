# uploader/cosmos_service.py
import uuid  # For generating unique ids
from azure.cosmos import CosmosClient, PartitionKey, exceptions
from django.conf import settings
from datetime import datetime


class CosmosDBService:
    def __init__(self):
        # Initialize the CosmosClient using the endpoint and key
        self.client = CosmosClient(settings.AZURE_COSMOS_DB_ENDPOINT, settings.AZURE_COSMOS_DB_KEY)

        # Try to get the database, create if it doesn't exist
        self.database = self.client.create_database_if_not_exists(settings.AZURE_COSMOS_DB_DATABASE)

        # Try to get the container, create if it doesn't exist
        self.container = self.database.create_container_if_not_exists(
            id=settings.AZURE_COSMOS_DB_CONTAINER,
            partition_key=PartitionKey(path="/user_id"),  # Define the partition key, adjust as needed
            offer_throughput=400
        )

    def store_metadata(self, metadata):
        """
        Store document metadata in Azure Cosmos DB.
        :param metadata: A dictionary containing document metadata (e.g., upload date, type, user ID, tags).
        :return: The inserted document if successful, or None.
        """
        try:
            # Add a unique 'id' field to metadata
            metadata['id'] = str(uuid.uuid4())  # Generate a unique UUID for each document

            # Add upload timestamp to metadata
            metadata['upload_date'] = datetime.utcnow().isoformat()

            # Insert the metadata into the Cosmos DB container
            self.container.create_item(metadata)
            return metadata
        except exceptions.CosmosHttpResponseError as e:
            print(f"Failed to store metadata: {e}")
            return None
