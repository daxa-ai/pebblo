from dotenv import load_dotenv
from langchain.chains import PebbloRetrievalQA
from langchain_community.vectorstores.qdrant import Qdrant
from langchain_openai import OpenAIEmbeddings
from langchain_openai.llms import OpenAI
from qdrant_client import QdrantClient

from google_auth import get_authorized_identities

load_dotenv()

#  Qdrant DB path
QDRANT_PATH = "qdrant.db"
#  Qdrant DB collection name
DEFAULT_COLLECTION_NAME = "identity-enabled-rag"


class PebbloIdentityRAG:
    def __init__(self, collection_name: str = DEFAULT_COLLECTION_NAME):
        self.app_name = "acme-corp-rag-1"
        self.qdrant_collection_name = collection_name
        self.llm = OpenAI()
        self.embeddings = OpenAIEmbeddings()
        self.vectordb = self.init_vector_db()

    def init_vector_db(self):
        """
        Load Vector DB from file
        """
        client = QdrantClient(
            path=QDRANT_PATH,
        )
        vectordb = Qdrant(
            client=client,
            collection_name=self.qdrant_collection_name,
            embeddings=self.embeddings,
        )
        return vectordb

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
    def_service_acc_path = "credentials/service-account.json"
    def_ingestion_user_email_address = "admin@clouddefense.io"
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

    def_end_user = "demo-user-hr@daxa.ai"

    while True:
        print("Please enter end user details below")
        end_user_email_address = (
            input(f"User email address ({def_end_user}): ") or def_end_user
        )
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
