# Fill-in OPENAI_API_KEY in .env file in this directory before proceeding
from dotenv import load_dotenv
from google_auth import get_authorized_identities
from langchain_community.chains import PebbloRetrievalQA
from langchain_community.chains.pebblo_retrieval.models import (
    AuthContext,
    ChainInput,
)
from langchain_community.document_loaders import UnstructuredFileIOLoader
from langchain_community.document_loaders.pebblo import PebbloSafeLoader
from langchain_community.vectorstores.qdrant import Qdrant
from langchain_google_community import GoogleDriveLoader
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_openai.llms import OpenAI

load_dotenv()


class PebbloIdentityRAG:
    def __init__(self, folder_id: str, collection_name: str):
        self.app_name = "pebblo-identity-rag-1"
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
            description="Identity enabled SafeLoader and SafeRetrival app using Pebblo",  # Description (Optional)
        )
        self.documents = self.loader.load()
        print(self.documents[-1].metadata.get("authorized_identities"))
        print(f"Loaded {len(self.documents)} documents ...\n")

        # Load documents into VectorDB

        print("Hydrating Vector DB ...")
        self.vectordb = self.embeddings()
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
            chain_type="stuff",
            retriever=self.vectordb.as_retriever(),
            verbose=True,
        )

    def embeddings(self):
        embeddings = OpenAIEmbeddings()
        vectordb = Qdrant.from_documents(
            self.documents,
            embeddings,
            location=":memory:",
            collection_name=self.collection_name,
        )
        return vectordb

    def ask(self, question: str, user_email: str, auth_identifiers: list):
        auth_context = {
            "user_id": user_email,
            "authorized_identities": auth_identifiers,
        }
        auth_context = AuthContext(**auth_context)
        chain_input = ChainInput(query=question, auth_context=auth_context)

        return self.retrieval_chain.invoke(chain_input.dict())


if __name__ == "__main__":
    input_collection_name = "identity-enabled-rag"

    print("Please enter ingestion user details for loading data...")
    ingestion_user_email_address = input("email address : ")
    ingestion_user_service_account_path = input("service-account.json path : ")
    input_folder_id = input("Folder id : ")

    rag_app = PebbloIdentityRAG(
        folder_id=input_folder_id, collection_name=input_collection_name
    )

    while True:
        print("Please enter end user details below")
        end_user_email_address = input("User email address : ")
        prompt = input("Please provide the prompt : ")
        print(f"User: {end_user_email_address}.\nQuery:{prompt}\n")

        authorized_identities = get_authorized_identities(
            admin_user_email_address=ingestion_user_email_address,
            credentials_file_path=ingestion_user_service_account_path,
            user_email=end_user_email_address,
        )
        response = rag_app.ask(prompt, end_user_email_address, authorized_identities)
        print(f"Response:\n{response}")
        try:
            continue_or_exist = int(input("\n\nType 1 to continue and 0 to exit : "))
        except ValueError:
            print("Please provide valid input")
            continue

        if not continue_or_exist:
            exit(0)

        print("\n\n")
