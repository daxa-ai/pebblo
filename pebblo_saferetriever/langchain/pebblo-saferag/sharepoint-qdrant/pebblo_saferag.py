import os
from pathlib import Path
from typing import Optional, List

from dotenv import load_dotenv

load_dotenv()

from langchain_community.chains import PebbloRetrievalQA
from langchain_community.chains.pebblo_retrieval.models import (
    AuthContext,
    ChainInput,
    SemanticContext,
)
from langchain_community.document_loaders import SharePointLoader
from langchain_community.document_loaders.pebblo import PebbloSafeLoader
from langchain_community.vectorstores.qdrant import Qdrant
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_openai.llms import OpenAI
from msgraph_api_auth import SharepointADHelper
from utils import get_input_as_list, obfuscate, format_text


class PebbloSafeRAG:
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
        print(f"\nchain_input: {chain_input.json(indent=4)}")
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
    input_collection_name = "identity-enabled-rag"

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
    print("SharepointADHelper initialized.")

    site_url = (
        input(f"\nEnter Sharepoint Site URL (default={_site_url}): ") or _site_url
    )
    if not site_url:
        print("\nSite URL is required. Exiting ...")
        exit(1)

    # Get SharePoint Site ID using URL
    site_id = sharepoint_helper.get_site_id(site_url)
    print(f"Derived Site Id: {site_id}\n")

    # Get drive info using site id
    print("Fetching drive info ...")
    drive_info = sharepoint_helper.get_drive_id(site_id)
    drive_id, drive_name = select_drive(drive_info)
    print(f"\nSharePoint Drive name: {drive_name}, Drive Id: {drive_id}")

    # Enter Folder path
    folder_path = input("\nEnter folder path (default='/document'): ") or "/document"

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

        authorized_identities = SharepointADHelper(
            client_id=app_client_id,
            client_secret=app_client_secret,
            tenant_id=tenant_id,
        ).get_authorized_identities(end_user_email_address)

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
