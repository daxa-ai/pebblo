import os

from dotenv import load_dotenv

load_dotenv()

from langchain_community.chains import PebbloRetrievalQA
from langchain_community.chains.pebblo_retrieval.models import (
    AuthContext,
    ChainInput,
)
from langchain_community.document_loaders import SharePointLoader
from langchain_community.document_loaders.pebblo import PebbloSafeLoader
from langchain_community.vectorstores.qdrant import Qdrant
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_openai.llms import OpenAI
from msgraph_api_auth import SharepointADHelper


class PebbloIdentityRAG:
    """
    Sample app to demonstrate the usage of PebbloSafeLoader, and PebbloRetrievalQA
    for Identity enforcement using Qdrant VectorDB
    """

    def __init__(self, drive_id: str, folder_path: str, collection_name: str):
        self.loader_app_name = "pebblo-identity-loader"
        self.retrieval_app_name = "pebblo-identity-retriever"
        self.collection_name = collection_name
        self.drive_id = drive_id
        self.folder_path = folder_path

        # Load documents
        print("\nLoading RAG documents ...")
        self.loader = PebbloSafeLoader(
            SharePointLoader(
                document_library_id=self.drive_id,
                folder_path=self.folder_path or "/",
                auth_with_token=True,
                load_auth=True,
                recursive=True,
                load_extended_metadata=True,
            ),
            name=self.loader_app_name,  # App name (Mandatory)
            owner="Joe Smith",  # Owner (Optional)
            description="Identity enabled SafeLoader and SafeRetrival app using Pebblo",  # Description (Optional)
            load_semantic=True,
        )
        self.documents = self.loader.load()
        print(self.documents[-1].metadata.get("authorized_identities"))
        print(f"Loaded {len(self.documents)} documents ...\n")

        # Load documents into VectorDB
        print("Hydrating Vector DB ...")
        self.vectordb = self.init_vector_db()
        print("Finished hydrating Vector DB ...\n")

        # Prepare LLM
        self.llm = OpenAI()
        print("Initializing PebbloRetrievalQA ...")
        self.retrieval_chain = self.init_retrieval_chain()

    def init_retrieval_chain(self):
        """
        Initialize PebbloRetrievalQA chain
        """
        return PebbloRetrievalQA.from_chain_type(
            llm=self.llm,
            app_name=self.retrieval_app_name,
            owner="Joe Smith",
            description="Identity enabled filtering using PebbloSafeLoader, and PebbloRetrievalQA",
            chain_type="stuff",
            retriever=self.vectordb.as_retriever(),
            verbose=True,
        )

    def init_vector_db(self):
        """
        Initialize Qdrant VectorDB from documents
        """
        embeddings = OpenAIEmbeddings()
        vectordb = Qdrant.from_documents(
            self.documents,
            embeddings,
            location=":memory:",
            collection_name=self.collection_name,
        )
        return vectordb

    def ask(self, question: str, user_email: str, auth_identifiers: list):
        """
        Ask a question
        """
        auth_context = {
            "user_id": user_email,
            "user_auth": auth_identifiers,
        }
        auth_context = AuthContext(**auth_context)
        chain_input = ChainInput(query=question, auth_context=auth_context)

        return self.retrieval_chain.invoke(chain_input.dict())


if __name__ == "__main__":
    input_collection_name = "identity-enabled-rag"

    print("Please enter ingestion user details for loading data...")
    app_client_id = input("App client id : ") or os.environ.get("O365_CLIENT_ID")
    app_client_secret = input("App client secret : ") or os.environ.get(
        "O365_CLIENT_SECRET"
    )
    tenant_id = input("Tenant id : ") or os.environ.get("O365_TENANT_ID")

    drive_id = input("Drive id : ")

    rag_app = PebbloIdentityRAG(
        drive_id=drive_id,
        folder_path="/document",
        collection_name=input_collection_name,
    )

    while True:
        print("Please enter end user details below")
        end_user_email_address = input("User email address : ")
        prompt = input("Please provide the prompt : ")
        print(f"User: {end_user_email_address}.\nQuery:{prompt}\n")

        authorized_identities = SharepointADHelper(
            client_id=app_client_id,
            client_secret=app_client_secret,
            tenant_id=tenant_id,
        ).get_authorized_identities(end_user_email_address)

        response = rag_app.ask(prompt, end_user_email_address, authorized_identities)
        print(
            f"auth_context: {response['auth_context']}\n"
            f"semantic_context: {response['semantic_context']}\n"
            f"Result: \n{response['result']}\n"
        )

        try:
            continue_or_exist = int(input("\n\nType 1 to continue and 0 to exit : "))
        except ValueError:
            print("Please provide valid input")
            continue

        if not continue_or_exist:
            exit(0)
