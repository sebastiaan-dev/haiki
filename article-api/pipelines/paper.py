import os

from chroma import ChromaDocumentStore
from chromadb.config import Settings

from haystack import Pipeline
from haystack.components.converters import PyPDFToDocument
from haystack.components.preprocessors import DocumentCleaner, DocumentSplitter
from haystack.components.writers import DocumentWriter
from haystack_integrations.components.embedders.ollama import OllamaDocumentEmbedder

from utils.files import get_paths_from_dir
from logger import logger

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


def papers(path: str):
    logger.info(f"Processing papers from {path}")

    file_paths = get_paths_from_dir(path)
    if not file_paths:
        logger.error(f"No files found in {path}")
        return

    pipe = Pipeline()

    # Add components to the pipeline
    pipe.add_component(name="converter", instance=PyPDFToDocument())
    pipe.add_component(
        name="cleaner",
        instance=DocumentCleaner(
            remove_empty_lines=True,
            remove_extra_whitespaces=True,
            remove_repeated_substrings=False,
        ),
    )
    pipe.add_component(
        name="splitter", instance=DocumentSplitter(split_by="passage", split_length=1)
    )
    pipe.add_component(name="embedder", instance=OllamaDocumentEmbedder())
    pipe.add_component(name="writer", instance=DocumentWriter(store))

    # Connect components
    pipe.connect("converter", "cleaner")
    pipe.connect("cleaner", "splitter")
    pipe.connect("splitter", "embedder")
    pipe.connect("embedder", "writer")

    pipe.run({"converter": {"sources": file_paths}})
