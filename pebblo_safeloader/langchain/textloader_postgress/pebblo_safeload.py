import logging
import os

from dotenv import load_dotenv
from langchain_community.document_loaders.pebblo import (
    PebbloSafeLoader,
    PebbloTextLoader,
)
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_postgres import PGVector
from util import get_data

load_dotenv()

PEBBLO_API_KEY = os.getenv("PEBBLO_API_KEY")
PEBBLO_CLOUD_URL = os.getenv("PEBBLO_CLOUD_URL")
PG_CONNECTION_STRING = os.getenv("PG_CONNECTION_STRING")

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class PebbloSafeRAG:
    """
    Sample app to demonstrate the usage of PebbloSafeLoader
    using PebbloTextLoader and PostgreSQL VectorDB
    """

    def __init__(self, collection_name: str):
        self.loader_app_name = "pebblo-safe-loader-text-loader"
        self.collection_name = collection_name

        print(120 * "-")
        # Load documents
        print("Loading RAG documents ...")
        texts, metadata, metadatas, ids = get_data(
            metadata=True, ids=True, metadatas=True
        )
        self.loader = PebbloSafeLoader(
            PebbloTextLoader(
                texts=texts,
                metadata=metadata,
                metadatas=metadatas,
                ids=ids,
            ),
            name=self.loader_app_name,  # App name (Mandatory)
            owner="Joe Smith",  # Owner (Optional)
            description="Identity & Semantic enabled SafeLoader app using Pebblo",  # Description (Optional)
            load_semantic=True,
            api_key=PEBBLO_API_KEY,
            anonymize_snippets=True,
        )
        self.documents = self.loader.load()
        unique_identities = set()
        unique_topics = set()
        unique_entities = set()

        for doc in self.documents:
            if doc.metadata.get("authorized_identities"):
                unique_identities.update(doc.metadata.get("authorized_identities"))
            if doc.metadata.get("pebblo_semantic_topics"):
                unique_topics.update(doc.metadata.get("pebblo_semantic_topics"))
            if doc.metadata.get("pebblo_semantic_entities"):
                unique_entities.update(doc.metadata.get("pebblo_semantic_entities"))

        print(f"Loaded {len(self.documents)} documents with the following metadata:")
        print(f"Authorized Identities: {list(unique_identities)}")
        print(f"Semantic Topics: {list(unique_topics)}")
        print(f"Semantic Entities: {list(unique_entities)}")
        print(120 * "-")

        # Load documents into VectorDB
        print("Hydrating Vector DB ...")
        self.vectordb = self.init_vector_db()
        print("Finished hydrating Vector DB ...\n")
        print(120 * "-")

    def init_vector_db(self):
        """
        Initialize PostgreSQL VectorDB from documents
        """
        embeddings = OpenAIEmbeddings()
        vectordb = PGVector.from_documents(
            embedding=embeddings,
            documents=self.documents,
            collection_name=self.collection_name,
            connection=PG_CONNECTION_STRING,
            pre_delete_collection=True,
            use_jsonb=True,
        )
        print(f"Added {len(self.documents)} documents to PostgreSQL ...\n")
        return vectordb


if __name__ == "__main__":
    input_collection_name = "identity-enabled-text-loader"
    rag_app = PebbloSafeRAG(
        collection_name=input_collection_name,
    )
