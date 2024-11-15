"""
Sample app to demonstrate the usage of PebbloSafeLoader, and PebbloRetrievalQA
for semantic enforcement using Pinecone VectorDB in RAG.
"""

import time
from pathlib import Path
from typing import List, Optional

from dotenv import load_dotenv
from google_auth import get_authorized_identities
from langchain_community.chains import PebbloRetrievalQA
from langchain_community.chains.pebblo_retrieval.models import (
    AuthContext,
    ChainInput,
    SemanticContext,
)
from langchain_community.document_loaders import UnstructuredFileIOLoader
from langchain_community.document_loaders.pebblo import PebbloSafeLoader
from langchain_community.vectorstores.pinecone import Pinecone as PineconeVectorStore
from langchain_google_community import GoogleDriveLoader
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_openai.llms import OpenAI
from pinecone_index import create_pinecone_index
from utils import describe_pebblo_semantic_stats, format_text, get_input_as_list

load_dotenv()


class SafeRetrieverSemanticRAG:
    """
    Sample app to demonstrate the usage of PebbloSafeLoader, and PebbloRetrievalQA
    for semantic enforcement using Pinecone VectorDB in RAG.


    Args:
        folder_id (str): Google Drive folder id
        index_name (str): Index name for Pinecone
    """

    def __init__(self, folder_id: str, index_name: str):
        self.loader_app_name = "pebblo-identity-n-semantic-loader-pinecone"
        self.retrieval_app_name = "pebblo-identity-n-semantic-retriever-pinecone"
        self.folder_id = folder_id
        self.pinecone_index_name = index_name
        # Prepare LLM
        self.llm = OpenAI()
        self.embeddings = OpenAIEmbeddings()
        # Load documents from Google Drive
        self.documents = self.load_documents()
        # Initialize VectorDB
        self.vectordb = self.init_vector_db()
        # Initialize PebbloRetrievalQA
        self.retrieval_chain = self.init_retrieval_chain()

    def load_documents(self):
        """
        Load documents from Google Drive
        """
        print("\nLoading RAG documents ...")
        loader = PebbloSafeLoader(
            GoogleDriveLoader(
                folder_id=self.folder_id,
                credentials_path=Path("credentials/credentials.json"),
                token_path=Path("./google_token.json"),
                recursive=True,
                file_loader_cls=UnstructuredFileIOLoader,
                file_loader_kwargs={"mode": "elements"},
                load_auth=True,
            ),
            name=self.loader_app_name,  # App name (Mandatory)
            owner="Joe Smith",  # Owner (Optional)
            description="Identity enabled SafeLoader app using Pebblo and Pinecone VectorDB",  # Description (Optional)
            load_semantic=True,
        )
        documents = loader.load()
        print(f"Loaded {len(documents)} documents ...\n")
        describe_pebblo_semantic_stats(documents)
        return documents

    def init_vector_db(self) -> PineconeVectorStore:
        """
        Create a Pinecone index and load documents into it
        """
        # Create index
        create_pinecone_index(self.pinecone_index_name, recreate=True)

        print("Loading docs into index...")
        texts = [t.page_content for t in self.documents]
        metadatas = [t.metadata for t in self.documents]

        # pop "coordinates" from metadata(Nested JSONs are not supported in Pinecone)
        for metadata in metadatas:
            metadata.pop("coordinates", None)

        vector_store = PineconeVectorStore.from_texts(
            texts,
            self.embeddings,
            metadatas=metadatas,
            index_name=self.pinecone_index_name,
        )

        # wait for index to be initialized
        print("Waiting for index to be ready...")
        time.sleep(5)

        print("Done!")
        return vector_store

    def init_retrieval_chain(self):
        """
        Initialize PebbloRetrievalQA chain
        """
        return PebbloRetrievalQA.from_chain_type(
            llm=self.llm,
            app_name=self.retrieval_app_name,
            owner="Joe Smith",
            description="Identity enabled SafeLoader and SafeRetrival app using "
            "Pebblo and Pinecone VectorDB",
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
        """
        Ask a question
        """
        auth_context = {
            "user_id": user_email,
            "user_auth": auth_identifiers,
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
    input_index_name = "identity-semantic-enforcement-rag"
    folder_id = "<google-drive-folder-id>"
    service_acc_def = "credentials/service-account.json"
    ing_user_email_def = "<ingestion-user-email-id>"

    print("Please enter ingestion user details for loading data...")
    print("Please enter admin user details...")
    ingestion_user_email_address = (
        input(f"email address ({ing_user_email_def}): ") or ing_user_email_def
    )
    ingestion_user_service_account_path = (
        input(f"service-account.json path ({service_acc_def}): ") or service_acc_def
    )
    rag_app = SafeRetrieverSemanticRAG(folder_id, input_index_name)

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
