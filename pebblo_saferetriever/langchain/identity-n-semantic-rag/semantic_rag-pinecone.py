from typing import List, Optional

from dotenv import load_dotenv
from google_auth import get_authorized_identities
from langchain.chains import PebbloRetrievalQA
from langchain.chains.pebblo_retrieval.models import (
    AuthContext,
    ChainInput,
    SemanticContext,
)
from langchain_community.vectorstores.pinecone import Pinecone as PineconeVectorStore
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_openai.llms import OpenAI
from utils import format_text, get_input_as_list

load_dotenv()


class SafeRetrieverSemanticRAG:
    """
    Sample app to demonstrate the usage of PebbloSafeLoader, and PebbloRetrievalQA
    for semantic enforcement in RAG.

    Args:
        folder_id (str): Google Drive folder id
        collection_name (str): Collection name for Qdrant
    """

    def __init__(self, index_name: str):
        self.app_name = "pebblo-sematic-rag"
        self.index_name = index_name
        self.vectordb = self.init_vector_db()
        # Prepare LLM
        self.llm = OpenAI()

        print("Initializing PebbloRetrievalQA ...")
        self.retrieval_chain = self.init_retrieval_chain()

    def init_vector_db(self):
        """
        Create embeddings from documents
        """
        embeddings = OpenAIEmbeddings()
        vectordb = PineconeVectorStore.from_existing_index(
            self.index_name, embedding=embeddings
        )
        return vectordb

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

    def ask(
        self,
        question: str,
        user_email: str,
        auth_identifiers: List[str],
        topics_to_deny: Optional[List[str]] = None,
        entities_to_deny: Optional[List[str]] = None,
    ):
        auth_context = {
            "name": "Name here",
            "username": user_email,
            "authorized_identities": auth_identifiers,
        }
        auth_context = AuthContext(**auth_context)
        semantic_context = dict()
        if topics_to_deny:
            semantic_context["pebblo_semantic_topics"] = {"deny": topics_to_deny}
        if entities_to_deny:
            semantic_context["pebblo_semantic_entities"] = {"deny": entities_to_deny}

        semantic_context = (
            SemanticContext(**semantic_context) if semantic_context else None
        )

        chain_input = ChainInput(
            query=question, auth_context=auth_context, semantic_context=semantic_context
        )

        return self.retrieval_chain.invoke(chain_input.dict())


if __name__ == "__main__":
    input_index_name = "semantic-enforcement-rag"
    service_acc_def = "credentials/service-account.json"
    in_folder_id_def = "<google-drive-folder-id>"
    ing_user_email_def = "<ingestion-user-email-id>"

    print("Please enter ingestion user details for loading data...")
    print("Please enter admin user details...")
    ingestion_user_email_address = (
        input(f"email address ({ing_user_email_def}): ") or ing_user_email_def
    )
    ingestion_user_service_account_path = (
        input(f"service-account.json path ({service_acc_def}): ") or service_acc_def
    )
    rag_app = SafeRetrieverSemanticRAG(index_name=input_index_name)

    while True:
        print("Please enter end user details below")
        end_user_email_address = input("User email address : ")

        auth_identifiers = get_authorized_identities(
            admin_user_email_address=ingestion_user_email_address,
            credentials_file_path=ingestion_user_service_account_path,
            user_email=end_user_email_address,
        )

        print(
            "Please enter semantic filters below...\n"
            "(Leave these fields empty if you do not wish to enforce any semantic filters)"
        )
        topic_to_deny = get_input_as_list(
            "Topics to deny, comma separated (Optional): "
        )
        entity_to_deny = get_input_as_list(
            "Entities to deny, comma separated (Optional): "
        )

        prompt = input("Please provide the prompt: ")
        print(
            f"User: {end_user_email_address}.\n"
            f"\nTopics to deny: {topic_to_deny}\n"
            f"Entities to deny: {entity_to_deny}\n"
            f"Query: {format_text(prompt)}"
        )
        response = rag_app.ask(
            prompt,
            end_user_email_address,
            auth_identifiers,
            topic_to_deny,
            entity_to_deny,
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
