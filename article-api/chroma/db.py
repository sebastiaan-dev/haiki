import os

from chroma import ChromaDocumentStore
from chromadb.config import Settings

"""
Configure the document store used to store and query papers.
"""
settings = Settings(
    chroma_client_auth_provider="chromadb.auth.token.TokenAuthClientProvider",
    chroma_client_auth_credentials=os.getenv("VECTOR_DB_TOKEN"),
)
store = ChromaDocumentStore(
    host=os.getenv("VECTOR_DB_HOST"), collection_name="papers_v1.2", settings=settings
)
