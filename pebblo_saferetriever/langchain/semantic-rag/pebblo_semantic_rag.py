from typing import Optional, List

from dotenv import load_dotenv
from langchain.chains import PebbloRetrievalQA
from langchain.chains.pebblo_retrieval.models import SemanticContext
from langchain_community.document_loaders import (
    GoogleDriveLoader,
    UnstructuredFileIOLoader,
)
from langchain_community.document_loaders.pebblo import PebbloSafeLoader
from langchain_community.vectorstores.qdrant import Qdrant
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_openai.llms import OpenAI

from utils import format_text, get_input_as_list

load_dotenv()


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
            ),
            name=self.app_name,  # App name (Mandatory)
            owner="Joe Smith",  # Owner (Optional)
            description="Semantic filtering using PebbloSafeLoader and PebbloRetrievalQA ",  # Description (Optional)
            load_semantic=True,
        )
        self.documents = self.loader.load()
        unique_topics = set()
        unique_entities = set()

        for doc in self.documents:
            if doc.metadata.get("pebblo_semantic_topics"):
                unique_topics.update(doc.metadata.get("pebblo_semantic_topics"))
            if doc.metadata.get("pebblo_semantic_entities"):
                unique_entities.update(doc.metadata.get("pebblo_semantic_entities"))

        print(f"Semantic Topics: {list(unique_topics)}")
        print(f"Semantic Entities: {list(unique_entities)}")
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
            location=":memory:",
            collection_name=self.collection_name,
        )
        return vectordb

    def ask(
        self,
        question: str,
        topics_to_deny: Optional[List[str]] = None,
        entities_to_deny: Optional[List[str]] = None,
    ):
        semantic_context = dict()
        if topics_to_deny:
            semantic_context["pebblo_semantic_topics"] = {"deny": topics_to_deny}
        if entities_to_deny:
            semantic_context["pebblo_semantic_entities"] = {"deny": entities_to_deny}

        semantic_context = (
            SemanticContext(**semantic_context) if semantic_context else None
        )

        # Prepare retriever QA chain
        retriever = PebbloRetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vectordb.as_retriever(),
            verbose=True,
            semantic_context=semantic_context,
        )
        return retriever.invoke(question)


if __name__ == "__main__":
    input_collection_name = "semantic-enforcement-rag"
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

    rag_app = PebbloSemanticRAG(
        folder_id=input_folder_id, collection_name=input_collection_name
    )

    while True:
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

        prompt = input("Please provide the prompt : ")
        print(
            f"\nTopics to deny: {topic_to_deny}\n"
            f"Entities to deny: {entity_to_deny}\n"
            f"Query: {format_text(prompt)}"
        )
        response = rag_app.ask(prompt, topic_to_deny, entity_to_deny)

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
