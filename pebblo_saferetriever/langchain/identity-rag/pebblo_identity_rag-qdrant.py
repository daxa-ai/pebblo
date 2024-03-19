import os

from dotenv import load_dotenv
from langchain.chains import PebbloRetrievalQA
from langchain_community.document_loaders import (
    GoogleDriveLoader,
    UnstructuredFileIOLoader,
)
from langchain_community.document_loaders.pebblo import PebbloSafeLoader
from langchain_community.vectorstores.qdrant import Qdrant
from langchain_openai import OpenAIEmbeddings
from langchain_openai.llms import OpenAI
from qdrant_client import QdrantClient

from google_auth import get_authorized_identities

load_dotenv()

# Get Qdrant API key from environment
QDRANT_API_KEY = os.environ.get("QDRANT_API_KEY", "your-qdrant-api-key")
#  Qdrant URL
QDRANT_URL = os.environ.get("QDRANT_URL")
#  Qdrant DB collection name
DEFAULT_COLLECTION_NAME = "identity-enabled-rag"

print(
    f"QDRANT Config: \n\tKey: {QDRANT_API_KEY[:10]}{'x' * len(QDRANT_API_KEY[10:])}, \n\tUrl: {QDRANT_URL}\n"
)


class PebbloIdentityRAG:
    def __init__(self, collection_name: str = DEFAULT_COLLECTION_NAME):
        self.app_name = "acme-corp-rag-1"
        self.qdrant_collection_name = collection_name
        self.llm = OpenAI()
        self.embeddings = OpenAIEmbeddings()
        self.vectordb = self.init_vector_db()

    def init_vector_db(self):
        """
        Load Vector DB
        """
        client = QdrantClient(
            url=QDRANT_URL,
            api_key=QDRANT_API_KEY,
        )
        vectordb = Qdrant(
            client=client,
            collection_name=self.qdrant_collection_name,
            embeddings=self.embeddings,
        )
        return vectordb

    def load_documents_to_vector_db(self, folder_id: str):
        """
        Load documents to Qdrant Vector DB
        """
        print("Loading documents...")

        loader = PebbloSafeLoader(
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
            description="Identity enabled SafeLoader and SafeRetrival app using Pebblo",  # Description (Optional)
        )
        documents = loader.load()
        print(f"Loaded {len(documents)} documents ...\n")
        print(f"First document: {documents[0]}")

        # Load documents into VectorDB
        print("Hydrating Vector DB ...")

        _vectordb = Qdrant.from_documents(
            documents,
            self.embeddings,
            url=QDRANT_URL,
            api_key=QDRANT_API_KEY,
            collection_name=self.qdrant_collection_name,
        )
        print("Finished hydrating Vector DB ...\n")

    def ask(self, question: str, auth_context: dict):
        # Prepare retriever QA chain
        retriever = PebbloRetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vectordb.as_retriever(),
            verbose=True,
            auth_context=auth_context,
        )
        return retriever.invoke(question)


if __name__ == "__main__":
    # TODO: pass the actual GoogleDrive folder id
    def_folder_id = "1sRvP0j6L6M_Ll0y_8Qp7cFWUOlpdbfN5"
    def_service_acc_path = "credentials/service-account.json"
    def_ingestion_user_email_address = "user@clouddefense.io"
    input_collection_name = "identity-enabled-rag"

    rag_app = PebbloIdentityRAG(input_collection_name)

    print("Please enter ingestion user details for loading data...")
    ingestion_user_email_address = (
        input(f"email address ({def_ingestion_user_email_address}) : ")
        or def_ingestion_user_email_address
    )
    ingestion_user_service_account_path = (
        input(f"service-account.json path ({def_service_acc_path}) : ")
        or def_service_acc_path
    )
    input_folder_id = input(f"Folder id ({def_folder_id}): ") or def_folder_id

    # Load documents to Qdrant Vector DB
    rag_app.load_documents_to_vector_db(input_folder_id)

    while True:
        print("Please enter end user details below")
        end_user_email_address = input("User email address : ")
        prompt = input("Please provide the prompt : ")
        print(f"User: {end_user_email_address}.\nQuery:{prompt}\n")

        auth = {
            "authorized_identities": get_authorized_identities(
                admin_user_email_address=ingestion_user_email_address,
                credentials_file_path=ingestion_user_service_account_path,
                user_email=end_user_email_address,
            )
        }
        response = rag_app.ask(prompt, auth)
        print(f"Response:\n{response}")
        try:
            continue_or_exist = int(input("\n\nType 1 to continue and 0 to exit : "))
        except ValueError:
            print("Please provide valid input")
            continue

        if not continue_or_exist:
            exit(0)

        print("\n\n")
