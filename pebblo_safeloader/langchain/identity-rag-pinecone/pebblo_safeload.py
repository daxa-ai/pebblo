"""
Identity enabled SafeLoader app using Pebblo and Pinecone VectorDB.
This app loads documents from Google Drive and add them to Pinecone VectorDB.
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_community.document_loaders import UnstructuredFileIOLoader
from langchain_community.document_loaders.pebblo import PebbloSafeLoader
from langchain_community.vectorstores import Pinecone as PineconeVectorStore
from langchain_google_community import GoogleDriveLoader
from langchain_openai.embeddings import OpenAIEmbeddings
from pinecone_index import create_pinecone_index
from utils import describe_pebblo_semantic_stats

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")


class IdentityBasedDataLoader:
    """
    Identity enabled SafeLoader app using Pebblo and Pinecone VectorDB.
    This app loads documents from Google Drive and add them to Pinecone VectorDB.

    Args:
        folder_id (str): Google Drive folder id
        index_name (str): Index name for Pinecone
    """

    def __init__(self, folder_id: str, index_name: str):
        self.app_name = "pebblo-identity-sematic-loader-pinecone"
        self.folder_id = folder_id
        self.pinecone_index_name = index_name
        self.embeddings = OpenAIEmbeddings()

    def load_documents(self):
        """
        Load documents from Google Drive
        """
        print("\nLoading RAG documents ...")
        loader = PebbloSafeLoader(
            GoogleDriveLoader(
                folder_id=self.folder_id,
                credentials_path=Path("credentials/credentials.json"),
                token_path=Path("./google_token.json"),
                recursive=True,
                file_loader_cls=UnstructuredFileIOLoader,
                file_loader_kwargs={"mode": "elements"},
                load_auth=True,
            ),
            name=self.app_name,  # App name (Mandatory)
            owner="Joe Smith",  # Owner (Optional)
            description="Identity enabled SafeLoader app using Pebblo and Pinecone VectorDB",  # Description (Optional)
            load_semantic=True,
        )
        documents = loader.load()
        unique_identities = set()
        for doc in documents:
            unique_identities.update(doc.metadata.get("authorized_identities", []))
        print(f"Loaded {len(documents)} documents ...\n")
        describe_pebblo_semantic_stats(documents)
        return documents

    def add_docs_to_pinecone(self, documents) -> PineconeVectorStore:
        """
        Create a Pinecone index and load documents into it
        """
        # Create index
        create_pinecone_index(self.pinecone_index_name, recreate=True)

        print("Loading docs into index...")
        texts = [t.page_content for t in documents]
        metadatas = [t.metadata for t in documents]

        # pop "coordinates" from metadata(Nested JSONs are not supported in Pinecone)
        for metadata in metadatas:
            metadata.pop("coordinates", None)

        vector_store = PineconeVectorStore.from_texts(
            texts,
            self.embeddings,
            metadatas=metadatas,
            index_name=self.pinecone_index_name,
        )

        print("Done!")
        return vector_store


if __name__ == "__main__":
    print("Loading documents to Qdrant ...")
    folder_id = "<google-drive-folder-id>"
    input_index_name = "identity-semantic-enforcement-rag"
    pinecone_data_loader = IdentityBasedDataLoader(folder_id, input_index_name)

    result_documents = pinecone_data_loader.load_documents()

    vectordb_obj = pinecone_data_loader.add_docs_to_pinecone(result_documents)
    print(f"First document: {result_documents[0]}")
    print("Finished hydrating Vector DB ...\n")
