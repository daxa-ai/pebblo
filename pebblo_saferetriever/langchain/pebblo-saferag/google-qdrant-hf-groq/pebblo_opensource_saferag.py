from typing import List, Optional

from google_auth import get_authorized_identities
from langchain_community.chains import PebbloRetrievalQA
from langchain_community.chains.pebblo_retrieval.models import (
    AuthContext,
    ChainInput,
    SemanticContext,
)
from langchain_community.document_loaders import UnstructuredFileIOLoader
from langchain_community.document_loaders.pebblo import PebbloSafeLoader
from langchain_community.vectorstores.qdrant import Qdrant
from langchain_google_community import GoogleDriveLoader
from langchain_groq import ChatGroq
from sentence_transformers import SentenceTransformer
from langchain.embeddings.base import Embeddings
from utils import format_text, get_input_as_list
from constant import (
    LLM_NAME,
    GROQ_API_KEY,
    SERVICE_ACCOUNT_PATH,
    INPUT_FOLDER_ID,
    EMBEDDING_MODEL,
    INGESTION_USER_EMAIL_ADDRESS,
    TOKEN_PATH,
    LOADER_APP_NAME,
    RETRIEVAL_APP_NAME,
    COLLECTION_NAME,
    VECTOR_DB_URL,
)


class LocalHuggingFaceEmbeddings(Embeddings):
    """
    Wrapper for HuggingFace SentenceTransformer embeddings to be used with LangChain.

    Args:
        model_name (str): Name of the HuggingFace model to use for embeddings.
    """

    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """
        Initialize the embedding model.

        Args:
            model_name (str): HuggingFace model name.
        """
        self.model = SentenceTransformer(model_name)

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Embed a list of documents.

        Args:
            texts (List[str]): List of document texts.
        Returns:
            List[List[float]]: List of embedding vectors.
        """
        embeddings = self.model.encode(texts)
        return embeddings.tolist()

    def embed_query(self, text: str) -> List[float]:
        """
        Embed a single query string.

        Args:
            text (str): Query text.
        Returns:
            List[float]: Embedding vector.
        """
        embedding = self.model.encode(text)
        return embedding.tolist()


class SafeRetrieverSemanticRAG:
    """
    Main class for secure, semantic RAG using PebbloSafeLoader, Qdrant, and Groq LLM.

    Args:
        folder_id (str): Google Drive folder ID to ingest documents from.
        collection_name (str): Qdrant collection name.
    """

    def __init__(self, folder_id: str, collection_name: str):
        """
        Initialize the RAG pipeline (models, config, but not indexing).

        Args:
            folder_id (str): Google Drive folder ID.
            collection_name (str): Qdrant collection name.
        """
        self.folder_id = folder_id
        self.collection_name = collection_name
        self.loader_app_name = LOADER_APP_NAME
        self.retrieval_app_name = RETRIEVAL_APP_NAME
        self.owner = "Joe Smith"
        self.description = (
            "Semantic filtering using PebbloSafeLoader, and PebbloRetrievalQA "
        )
        self.embedding_model = LocalHuggingFaceEmbeddings(EMBEDDING_MODEL)
        self.llm = ChatGroq(
            model_name=LLM_NAME, temperature=0.1, groq_api_key=GROQ_API_KEY
        )
        self.documents = []
        self.vectordb = None
        self.retrieval_chain = None

    def load_documents(self) -> PebbloSafeLoader:
        """
        Create and return a PebbloSafeLoader for the configured Google Drive folder.

        Returns:
            PebbloSafeLoader: Configured loader instance.
        """
        # https://python.langchain.com/api_reference/community/document_loaders/langchain_community.document_loaders.pebblo.PebbloSafeLoader.html
        return PebbloSafeLoader(
            GoogleDriveLoader(
                folder_id=self.folder_id,
                token_path=TOKEN_PATH,
                recursive=True,  # required if we are giving folder id
                file_loader_cls=UnstructuredFileIOLoader,  # document processing using unstructured
                # https://python.langchain.com/docs/integrations/document_loaders/ visit this link for more document loaders
                file_loader_kwargs={"mode": "single"},
                load_auth=True,
            ),
            name=self.loader_app_name,  # App name (Mandatory)
            owner=self.owner,  # Owner (Optional)
            description=self.description,  # Description (Optional)
            load_semantic=True,
        )

    def index(self):
        """
        Load documents, extract unique topics/entities, and hydrate the vector DB.
        Must be called before querying.
        """
        print("\nLoading RAG documents ...")
        self.loader = self.load_documents()
        self.documents = (
            self.loader.load()
        )  # load_and_split if you want to split the documents into chunks

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
        try:
            # Initialize Qdrant vector database with documents
            # documents: List of documents to be stored in the vector database
            # embedding_model: Model used to generate embeddings for the documents
            # url: URL of the Qdrant server (default: http://localhost:6333)
            # collection_name: Name of the collection in Qdrant where documents will be stored
            self.vectordb = Qdrant.from_documents(
                self.documents,  # List of documents to be stored
                self.embedding_model,  # Embedding model for vector generation
                url=VECTOR_DB_URL,  # Qdrant server URL
                collection_name=self.collection_name,  # Collection name in Qdrant
            )

        except Exception:
            print("\nError: Could not connect to Qdrant server.")
            print("Please make sure Qdrant server is running.")
            print("\nTo start Qdrant server, run this command in your terminal:")
            print("docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant")
            print("\nAfter starting the server, run this script again.")
            exit(1)
        print("Finished hydrating Vector DB ...\n")
        print("Initializing PebbloRetrievalQA ...")

    def init_retrieval_chain(self) -> PebbloRetrievalQA:
        """
        Initialize the PebbloRetrievalQA chain for querying.

        Returns:
            PebbloRetrievalQA: Configured retrieval QA chain.

        """
        # factory method for creating different types of retrieval chains.
        # there are other classes likeRetrievalQA,  RetrievalQAWithSourcesChain
        return PebbloRetrievalQA.from_chain_type(
            llm=self.llm,
            app_name=self.retrieval_app_name,
            owner="Nishan Jain",
            description="Identity and Semantic filtering using PebbloSafeLoader, and PebbloRetrievalQA",
            chain_type="stuff",  # other options are map_reduce, map_rerank, stuff, refine, map_rerank_and_stuff
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
    ) -> dict:
        """
        Query the RAG system with semantic and identity filtering.

        Args:
            question (str): The user's question.
            user_email (str): The user's email address.
            auth_identifiers (List[str]): List of user authorization identifiers.
            topics_to_deny (Optional[List[str]]): Topics to deny in results.
            entities_to_deny (Optional[List[str]]): Entities to deny in results.
        Returns:
            dict: The result from the retrieval chain.
        """
        print("topics_to_deny", topics_to_deny)
        print("entities_to_deny", entities_to_deny)
        print("auth_identifiers", auth_identifiers)
        print("question", question)
        print("user_email", user_email)
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
    """
    Entrypoint for the Pebblo Open Source SafeRAG demo.
    Loads and indexes documents, then enters a query loop for user interaction.
    """
    rag_app = SafeRetrieverSemanticRAG(
        folder_id=INPUT_FOLDER_ID, collection_name=COLLECTION_NAME
    )
    rag_app.index()

    rag_app.retrieval_chain = rag_app.init_retrieval_chain()

    while True:
        print("Please enter end user details below")
        end_user_email_address = input("User email address : ")

        auth_identifiers = get_authorized_identities(
            admin_user_email_address=INGESTION_USER_EMAIL_ADDRESS,
            credentials_file_path=SERVICE_ACCOUNT_PATH,
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

        print(f"Response:\n{format_text(response['result'])}")

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
