import logging
from pathlib import Path
from typing import Optional, List

from dotenv import load_dotenv

load_dotenv()

import os
from msgraph_api_auth import SharepointADHelper
from langchain_community.chains import PebbloRetrievalQA
from langchain_community.chains.pebblo_retrieval.models import (
    AuthContext,
    ChainInput,
    SemanticContext,
)
from langchain_community.document_loaders.pebblo import PebbloSafeLoader
from langchain_community.document_loaders import SharePointLoader
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_openai.llms import OpenAI
from langchain_postgres import PGVector
from utils import get_input_as_list, obfuscate, format_text

PEBBLO_API_KEY = os.getenv("PEBBLO_API_KEY")
PEBBLO_CLOUD_URL = os.getenv("PEBBLO_CLOUD_URL")
PG_CONNECTION_STRING = os.getenv("PG_CONNECTION_STRING")

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class PebbloSafeRAG:
    """
    Sample app to demonstrate the usage of PebbloSafeLoader, and PebbloRetrievalQA for Identity & Semantic enforcement
    using SharePointLoader and PostgreSQL VectorDB
    """

    def __init__(self, drive_id: str, folder_path: str, collection_name: str):
        self.loader_app_name = "pebblo-safe-loader"
        self.retrieval_app_name = "pebblo-safe-retriever"
        self.collection_name = collection_name
        self.drive_id = drive_id
        self.folder_path = folder_path

        print(120 * "-")
        # Load documents
        print("Loading RAG documents ...")
        token_path = Path.home() / ".credentials" / "o365_token.txt"
        self.loader = PebbloSafeLoader(
            SharePointLoader(
                document_library_id=self.drive_id,
                folder_path=self.folder_path or "/",
                auth_with_token=True if os.path.exists(token_path) else False,
                load_auth=True,
                recursive=True,
                load_extended_metadata=True,
            ),
            name=self.loader_app_name,  # App name (Mandatory)
            owner="Joe Smith",  # Owner (Optional)
            description="Identity & Semantic enabled SafeLoader and SafeRetrival app using Pebblo",  # Description (Optional)
            load_semantic=True,
            api_key=PEBBLO_API_KEY,
        )
        self.documents = self.loader.load()
        unique_identities = set()
        unique_topics = set()
        unique_entities = set()

        for doc in self.documents:
            if doc.metadata.get("authorized_identities"):
                unique_identities.update(doc.metadata.get("authorized_identities"))
            if doc.metadata.get("pebblo_semantic_topics"):
                unique_topics.update(doc.metadata.get("pebblo_semantic_topics"))
            if doc.metadata.get("pebblo_semantic_entities"):
                unique_entities.update(doc.metadata.get("pebblo_semantic_entities"))

        print(f"Loaded {len(self.documents)} documents with the following metadata:")
        print(f"Authorized Identities: {list(unique_identities)}")
        print(f"Semantic Topics: {list(unique_topics)}")
        print(f"Semantic Entities: {list(unique_entities)}")
        print(120 * "-")

        # Load documents into VectorDB
        print("Hydrating Vector DB ...")
        self.vectordb = self.init_vector_db()
        print("Finished hydrating Vector DB ...\n")

        # Prepare LLM
        self.llm = OpenAI()
        print("Initializing PebbloRetrievalQA ...")
        self.retrieval_chain = self.init_retrieval_chain()
        print("Finished initializing PebbloRetrievalQA ...")
        print(120 * "-")

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
        Initialize PostgreSQL VectorDB from documents
        """
        embeddings = OpenAIEmbeddings()
        vectordb = PGVector.from_documents(
            embedding=embeddings,
            documents=self.documents,
            collection_name=self.collection_name,
            connection=PG_CONNECTION_STRING,
            pre_delete_collection=True,
            use_jsonb=True,
        )
        print(f"Added {len(self.documents)} documents to PostgreSQL ...\n")
        return vectordb

    def ask(
        self,
        question: str,
        user_email: str,
        auth_identifiers: list,
        topics_to_deny: Optional[List[str]] = None,
        entities_to_deny: Optional[List[str]] = None,
    ):
        """
        Ask a question with identity and semantic context
        """
        auth_context = None
        if auth_identifiers:
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
        # Print chain input in formatted json
        print(f"\nchain_input: {chain_input.model_dump_json(indent=4)}")
        return self.retrieval_chain.invoke(chain_input.dict())


def select_drive(drives: list) -> tuple:
    """
    Select SharePoint drive from the available drives
    """
    if not drives:
        print("No drives found for the site. Exiting ...")
        exit(1)
    elif len(drives) == 1:
        _drive_id = drives[0].get("id")
        _drive_name = drives[0].get("name")
    else:
        # Select "Documents" as a default drive
        def_drive_idx = next(
            (
                idx
                for idx, drive in enumerate(drives)
                if drive.get("name") == "Documents"
            ),
            0,
        )
        # Select drive
        # print("Select a drive ...")
        print("Available drives on the site:")
        for idx, drive in enumerate(drives):
            print(f"\t{idx + 1}. {drive.get('name')}")

        # Prompt user for drive index
        _drive_idx = input(f"Enter drive index (default={def_drive_idx + 1}): ")
        _drive_idx = int(_drive_idx) - 1 if _drive_idx else def_drive_idx
        # Validate drive index and select default drive if invalid
        if _drive_idx < 0 or _drive_idx >= len(drives):
            print("Error. Invalid drive index! Selecting the default drive ...")
            _drive_idx = def_drive_idx

        # Get drive info
        _drive_id = drives[_drive_idx].get("id")
        _drive_name = drives[_drive_idx].get("name")
    return _drive_id, _drive_name


if __name__ == "__main__":
    input_collection_name = "identity-enabled-rag-sharepoint"
    _client_id = os.environ.get("O365_CLIENT_ID")
    _client_secret = os.environ.get("O365_CLIENT_SECRET")
    _tenant_id = os.environ.get("O365_TENANT_ID")
    _site_url = os.environ.get("SHAREPOINT_SITE_URL")

    print("Please enter the app details to authenticate with Microsoft Graph API ...")
    app_client_id = input(f"App client id ({_client_id}): ") or _client_id
    app_client_secret = (
        input(f"App client secret ({obfuscate(_client_secret)}): ") or _client_secret
    )
    tenant_id = input(f"Tenant id ({_tenant_id}): ") or _tenant_id

    print("\nInitializing SharepointADHelper ...")
    sharepoint_helper = SharepointADHelper(
        client_id=app_client_id,
        client_secret=app_client_secret,
        tenant_id=tenant_id,
    )
    print("SharepointADHelper initialized.\n")

    site_url = (
        input(f"Enter Sharepoint Site URL (default={_site_url}): ") or _site_url
    )
    if not site_url:
        print("\nSite URL is required. Exiting ...")
        exit(1)
    # remove white spaces from the site url
    site_url = site_url.strip()

    # Get SharePoint Site ID using URL
    site_id = sharepoint_helper.get_site_id(site_url)
    print(f"Derived Site Id: {site_id}\n")

    # Get drive info using site id
    print("Fetching drive info ...\n")
    drive_info = sharepoint_helper.get_drive_id(site_id)
    drive_id, drive_name = select_drive(drive_info)
    print(f"SharePoint Drive name: {drive_name}, Drive Id: {drive_id}\n")

    # Enter Folder path
    def_folder_path = "documents"
    folder_path = input(f"Enter folder path (default='{def_folder_path}'): ") or def_folder_path

    # Initialize PebbloSafeRAG app
    rag_app = PebbloSafeRAG(
        drive_id=drive_id,
        folder_path=folder_path,
        collection_name=input_collection_name,
    )

    while True:
        print("Please enter end user details below:")
        end_user_email_address = input("User email address: ")

        def_topics = None  # ["employee-agreement"]
        topic_to_deny = (
            get_input_as_list(
                f"Enter topics to deny (Optional, comma separated, no quotes needed): "
            )
            or def_topics
        )

        def_entities = None
        entity_to_deny = (
            get_input_as_list(
                f"Enter entities to deny (Optional, comma separated, no quotes needed): "
            )
            or def_entities
        )

        prompt = input("Please provide the prompt : ")

        authorized_identities = sharepoint_helper.get_authorized_identities(
            end_user_email_address
        )

        response = rag_app.ask(
            prompt,
            end_user_email_address,
            authorized_identities,
            topic_to_deny,
            entity_to_deny,
        )
        print(f"Result: {format_text(response['result'])}")
        print(120 * "-")

        try:
            continue_or_exist = int(input("\nType 1 to continue and 0 to exit : "))
        except ValueError:
            print("Please provide valid input")
            continue

        if not continue_or_exist:
            exit(0)

        print("\n")
