# Fill-in OPENAI_API_KEY in .env file in this directory before proceeding
from typing import Optional, List

from dotenv import load_dotenv
from langchain.chains import PebbloRetrievalQA
from langchain.chains.pebblo_retrieval.models import AuthContext, SemanticContext
from langchain_community.document_loaders import (
    GoogleDriveLoader,
    UnstructuredFileIOLoader,
)
from langchain_community.document_loaders.pebblo import PebbloSafeLoader
from langchain_community.vectorstores.qdrant import Qdrant
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_openai.llms import OpenAI

from google_auth import get_authorized_identities
from utils import format_text, get_input_as_list

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

    def embeddings(self):
        embeddings = OpenAIEmbeddings()
        vectordb = Qdrant.from_documents(
            self.documents,
            embeddings,
            location=":memory:",
            collection_name=self.collection_name,
        )
        return vectordb

    def ask(
        self,
        question: str,
        auth_identifiers: Optional[List[str]] = None,
        topics_to_deny: Optional[List[str]] = None,
        entities_to_deny: Optional[List[str]] = None,
    ):
        auth_context = dict()
        if auth_identifiers:
            auth_context["authorized_identities"] = auth_identifiers
        semantic_context = dict()
        if topics_to_deny:
            semantic_context["pebblo_semantic_topics"] = {"deny": topics_to_deny}
        if entities_to_deny:
            semantic_context["pebblo_semantic_entities"] = {"deny": entities_to_deny}

        auth_context = AuthContext(**auth_context) if auth_context else None
        semantic_context = (
            SemanticContext(**semantic_context) if semantic_context else None
        )
        # Prepare retriever QA chain
        retriever = PebbloRetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vectordb.as_retriever(),
            verbose=True,
            auth_context=auth_context,
            semantic_context=semantic_context,
        )
        return retriever.invoke(question)


if __name__ == "__main__":
    input_collection_name = "identity-enabled-rag"
    service_acc_def = "credentials/service-account.json"
    in_folder_id_def = "<google-drive-folder-id>"
    ing_user_email_def = "<ingestion-user-email-id>"

    print("Please enter ingestion user details for loading data...")
    ingestion_user_email_address = (
        input(f"email address ({ing_user_email_def}): ") or ing_user_email_def
    )
    ingestion_user_service_account_path = (
        input(f"service-account.json path ({service_acc_def}): ") or service_acc_def
    )
    input_folder_id = input(f"Folder id ({in_folder_id_def}): ") or in_folder_id_def

    rag_app = PebbloIdentityRAG(
        folder_id=input_folder_id, collection_name=input_collection_name
    )

    while True:
        print(
            "Please enter end user details and semantic filters below...\n"
            "(Leave empty if you don't want to enforce any identity or semantic filters)"
        )
        end_user_email_address = input("User email address (Optional): ") or None
        # topic_to_deny = input("Topics to deny, comma separated (Optional): ") or None
        # entity_to_deny = input("Entities to deny, comma separated (Optional): ") or None
        topic_to_deny = get_input_as_list(
            "Topics to deny, comma separated (Optional): "
        )
        entity_to_deny = get_input_as_list(
            "Entities to deny, comma separated (Optional): "
        )

        authorized_identities = None
        if end_user_email_address:
            authorized_identities = get_authorized_identities(
                admin_user_email_address=ingestion_user_email_address,
                credentials_file_path=ingestion_user_service_account_path,
                user_email=end_user_email_address,
            )

        prompt = input("Please provide the prompt : ")
        print(
            f"\nUser: {end_user_email_address}\n"
            f"Topics to deny: {topic_to_deny}\n"
            f"Entities to deny: {entity_to_deny}\n"
            f"Query: {format_text(prompt)}"
        )
        response = rag_app.ask(
            prompt, authorized_identities, topic_to_deny, entity_to_deny
        )

        print(f"Response:\n" f"{format_text(response['result'])}")

        try:
            continue_or_exist = int(
                input("\n\nType 1 to continue and 0 to exit (1): ") or 1
            )
        except ValueError:
            print("Please provide valid input")
            continue

        if not continue_or_exist:
            exit(0)

        print("\n\n")
