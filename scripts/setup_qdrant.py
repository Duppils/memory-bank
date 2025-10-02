# scripts/setup_qdrant.py
from qdrant_client import QdrantClient, models
import os

QDRANT_URL = os.environ.get("QDRANT_URL", "http://qdrant:6333")
COLLECTION_NAME = "user_memories"
# Nomic-embed-text uses 768 dimensions
VECTOR_SIZE = 768 

print(f"Qdrant URL: {QDRANT_URL}")

try:
    client = QdrantClient(url=QDRANT_URL)

    collections = client.get_collections().collections
    if any(c.name == COLLECTION_NAME for c in collections):
        print(f"Collection '{COLLECTION_NAME}' already exists. Skipping creation.")
    else:
        print(f"Creating collection '{COLLECTION_NAME}'...")
        client.recreate_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=models.VectorParams(
                size=VECTOR_SIZE,
                distance=models.Distance.COSINE
            )
        )
        print(f"Collection '{COLLECTION_NAME}' created successfully.")

except Exception as e:
    print(f"Error during Qdrant setup: {e}")

print("Qdrant setup script finished.")