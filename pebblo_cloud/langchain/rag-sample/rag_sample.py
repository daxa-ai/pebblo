import os
from typing import List

from dotenv import load_dotenv
from langchain.schema import Document
from langchain_community.document_loaders import (
    GoogleDriveLoader,
    UnstructuredFileIOLoader,
)
from langchain_community.document_loaders.pebblo import PebbloSafeLoader
from langchain_community.vectorstores.qdrant import Qdrant
from langchain_openai.embeddings import OpenAIEmbeddings

load_dotenv()

#  Qdrant DB path
QDRANT_PATH = "qdrant.db"
#  Qdrant DB collection name
COLLECTION_NAME = "identity-enabled-rag"


class DataLoader:
    def __init__(self, folder_id: str, collection_name: str = COLLECTION_NAME):
        self.app_name = "pebblo-cloud-sample-app"
        self.folder_id = folder_id
        self.qdrant_collection_name = collection_name

    def load_documents(self):
        print("\nLoading RAG documents ...")
        loader = PebbloSafeLoader(
            GoogleDriveLoader(
                folder_id=self.folder_id,
                credentials_path="credentials/credentials.json",
                token_path="./google_token.json",
                recursive=True,
                file_loader_cls=UnstructuredFileIOLoader,
                file_loader_kwargs={"mode": "elements"},
                load_auth=True,
            ),
            name=self.app_name,  # App name (Mandatory)
            owner="Joe Smith",  # Owner (Optional)
            description="SafeLoader and SafeRetrival app using Pebblo",  # Description (Optional)
            api_key=os.environ.get("PEBBLO_API_KEY"),  # Pebblo cloud API key
        )
        documents = loader.load()
        unique_identities = set()
        for doc in documents:
            unique_identities.update(doc.metadata.get("authorized_identities"))

        print(f"Authorized Identities: {list(unique_identities)}")
        print(f"Loaded {len(documents)} documents ...\n")
        return documents

    def add_docs_to_qdrant(self, documents: List[Document]):
        """
        Load documents into Qdrant
        """
        print("\nAdding documents to Qdrant ...")
        embeddings = OpenAIEmbeddings()
        vectordb = Qdrant.from_documents(
            documents,
            embeddings,
            path=QDRANT_PATH,
            collection_name=self.qdrant_collection_name,
        )
        print(f"Added {len(documents)} documents to Qdrant ...\n")
        return vectordb


if __name__ == "__main__":
    print("Loading documents to Qdrant ...")
    def_folder_id = "<google_drive_folder_id>"
    input_collection_name = "identity-enabled-rag"

    qloader = DataLoader(def_folder_id, input_collection_name)

    result_documents = qloader.load_documents()

    vectordb_obj = qloader.add_docs_to_qdrant(result_documents)
