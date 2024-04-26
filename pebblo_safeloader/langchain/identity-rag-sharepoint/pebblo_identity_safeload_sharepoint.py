from typing import List

from dotenv import load_dotenv
from langchain.schema import Document
from langchain_community.document_loaders import UnstructuredFileIOLoader
from langchain_community.document_loaders.pebblo import PebbloSafeLoader
from langchain_community.vectorstores.qdrant import Qdrant
from langchain_community.document_loaders.sharepoint import SharePointLoader
from langchain_openai.embeddings import OpenAIEmbeddings

load_dotenv()

#  Qdrant DB path
QDRANT_PATH = "qdrant.db"
#  Qdrant DB collection name
COLLECTION_NAME = "identity-enabled-rag"


class IdentityBasedSharePointDataLoader:
    def __init__(self, folder_id: str, folder_path: str, collection_name: str = COLLECTION_NAME):
        self.app_name = "acme-corp-rag-1"
        self.folder_id = folder_id
        self.folder_path = folder_path
        self.qdrant_collection_name = collection_name

    def load_documents(self):
        print("\nLoading RAG documents ...")
        loader = PebbloSafeLoader(
            SharePointLoader(
                document_library_id=self.folder_id, 
                folder_path=self.folder_path, 
                auth_with_token=True
            ),
            name=self.app_name,  # App name (Mandatory)
            owner="Joe Smith",  # Owner (Optional)
            description="Identity enabled SafeLoader and SafeRetrival app using Pebblo",  # Description (Optional)
        )
        documents = loader.load()
        # unique_identities = set()
        # for doc in documents:
        #     unique_identities.update(doc.metadata.get("authorized_identities"))

        # print(f"Authorized Identities: {list(unique_identities)}")
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
    def_folder_id = "<sharepoint_folder_id>"
    def_folder_path = "<sharepoint_folder_path>"
    input_collection_name = "identity-enabled-rag"

    qloader = IdentityBasedSharePointDataLoader(def_folder_id, def_folder_path, input_collection_name)

    result_documents = qloader.load_documents()

    vectordb_obj = qloader.add_docs_to_qdrant(result_documents)
