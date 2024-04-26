# Fill-in OPENAI_API_KEY in .env file in this directory before proceeding
from dotenv import load_dotenv
from sharepoint_auth import get_authorized_identities
from langchain.chains import PebbloRetrievalQA
from langchain.chains.pebblo_retrieval.models import AuthContext, ChainInput
from langchain_community.document_loaders import UnstructuredFileIOLoader
from langchain_community.document_loaders.pebblo import PebbloSafeLoader
from langchain_community.vectorstores.qdrant import Qdrant
from langchain_community.document_loaders.sharepoint import SharePointLoader
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_openai.llms import OpenAI
import json
import os

load_dotenv()


class PebbloIdentityRAGSharePoint:
    def __init__(self, folder_id: str, folder_path: str, collection_name: str):
        self.app_name = "pebblo-identity-rag-1"
        self.folder_id = folder_id
        self.folder_path = folder_path
        self.collection_name = collection_name

        # Load documents
        print("\nLoading RAG documents ...")
        self.loader = PebbloSafeLoader(
            SharePointLoader(
                document_library_id=self.folder_id, 
                folder_path=self.folder_path, 
                auth_with_token=True
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
            "username": user_email,
            "authorized_identities": auth_identifiers,
        }
        auth_context = AuthContext(**auth_context)
        chain_input = ChainInput(query=question, auth_context=auth_context)

        return self.retrieval_chain.invoke(chain_input.dict())


if __name__ == "__main__":
    input_collection_name = "identity-enabled-rag"

    print("Please enter ingestion user details for loading data...")
    ingestion_user_email_address = input("email address : ")
    # ingestion_user_service_account_path = input("service-account.json path : ")
    input_folder_id = input("Folder id : ")
    imput_folder_path = input("Folder path : ")
    rag_app = PebbloIdentityRAGSharePoint(
        folder_id=input_folder_id, folder_path=imput_folder_path, collection_name=input_collection_name
    )

    while True:
        print("Please enter end user details below")
        end_user_email_address = input("User email address : ")
        prompt = input("Please provide the prompt : ")
        print(f"User: {end_user_email_address}.\nQuery:{prompt}\n")

        ingestion_user_service_account_path = os.path.expanduser('~') + '/.credentials/o365_token.txt'
        with open(ingestion_user_service_account_path) as f:
            s = f.read()
            data = json.loads(s)

        access_token = data.get("access_token")
        authorized_identities = get_authorized_identities(
            # admin_user_email_address=ingestion_user_email_address,
            access_token=access_token,
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
