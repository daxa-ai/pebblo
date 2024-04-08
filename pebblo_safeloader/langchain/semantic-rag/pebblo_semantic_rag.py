from dotenv import load_dotenv
from langchain_community.document_loaders import (
    GoogleDriveLoader,
    UnstructuredFileIOLoader,
)
from langchain_community.document_loaders.pebblo import PebbloSafeLoader
from langchain_community.vectorstores.qdrant import Qdrant
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_openai.llms import OpenAI

load_dotenv()

QDRANT_PATH = "qdrant.db"


class PebbloSemanticRAG:
    """
    Sample app to demonstrate the usage of PebbloSafeLoader and PebbloRetrievalQA
    for semantic enforcement in RAG.

    Args:
        folder_id (str): Google Drive folder id
        collection_name (str): Collection name for Qdrant
    """

    def __init__(self, folder_id: str, collection_name: str):
        self.app_name = "pebblo-sematic-rag"
        self.collection_name = collection_name

        # Load documents
        print("\nLoading RAG documents ...")
        self.loader = PebbloSafeLoader(
            GoogleDriveLoader(
                folder_id=folder_id,
                token_path="./google_token.json",
                recursive=True,
                file_loader_cls=UnstructuredFileIOLoader,
                file_loader_kwargs={"mode": "elements"},
                load_auth=True,
            ),
            name=self.app_name,  # App name (Mandatory)
            owner="Joe Smith",  # Owner (Optional)
            description="Semantic filtering using PebbloSafeLoader and PebbloRetrievalQA ",  # Description (Optional)
            load_semantic=True,
        )
        self.documents = self.loader.load()
        unique_topics = set()
        unique_entities = set()
        unique_identities = set()

        for doc in self.documents:
            if doc.metadata.get("pebblo_semantic_topics"):
                unique_topics.update(doc.metadata.get("pebblo_semantic_topics"))
            if doc.metadata.get("pebblo_semantic_entities"):
                unique_entities.update(doc.metadata.get("pebblo_semantic_entities"))

            if doc.metadata.get("authorized_identities"):
                unique_identities.update(doc.metadata.get("authorized_identities"))

        print(f"Semantic Topics: {list(unique_topics)}")
        print(f"Semantic Entities: {list(unique_entities)}")
        print(f"Authorized Identities: {list(unique_identities)}")
        print(f"Loaded {len(self.documents)} documents ...\n")

        # Load documents into VectorDB
        print("Hydrating Vector DB ...")
        self.vectordb = self.embeddings()
        print("Finished hydrating Vector DB ...\n")

        # Prepare LLM
        self.llm = OpenAI()

    def embeddings(self):
        """
        Create embeddings from documents and load into Qdrant
        """
        embeddings = OpenAIEmbeddings()
        vectordb = Qdrant.from_documents(
            self.documents,
            embeddings,
            path=QDRANT_PATH,
            collection_name=self.collection_name,
        )
        return vectordb


if __name__ == "__main__":
    input_collection_name = "identity-semantic-enforcement-rag"
    service_acc_def = "credentials/service-account.json"
    in_folder_id_def = "1sR3wRgX9hGCdjtD1Vkl-b3hZuzGUP2EU"
    ing_user_email_def = "sridhar@clouddefense.io"

    rag_app = PebbloSemanticRAG(
        folder_id=in_folder_id_def, collection_name=input_collection_name
    )
