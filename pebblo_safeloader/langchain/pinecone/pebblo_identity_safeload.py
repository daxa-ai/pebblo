import os
import time

from dotenv import load_dotenv
from langchain_community.document_loaders import (
    GoogleDriveLoader,
    UnstructuredFileIOLoader,
)
from langchain_community.document_loaders.pebblo import PebbloSafeLoader
from langchain_community.vectorstores import Pinecone as PineconeVectorStore
from langchain_openai.embeddings import OpenAIEmbeddings
from pinecone import Pinecone, PodSpec, ServerlessSpec

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

INDEX_NAME = "identity-enabled-rag"


class IdentityBasedDataLoader:
    def __init__(self, folder_id: str, index_name: str = INDEX_NAME):
        self.app_name = "acme-corp-rag-1"
        self.folder_id = folder_id
        self.pinecone_index_name = index_name
        self.embeddings = OpenAIEmbeddings()

    def load_documents(self):
        print("\nLoading RAG documents ...")
        loader = PebbloSafeLoader(
            GoogleDriveLoader(
                folder_id=self.folder_id,
                credentials_path="credentials/credentials.json",
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
        documents = loader.load()
        unique_identities = set()
        for doc in documents:
            unique_identities.update(doc.metadata.get("authorized_identities"))

        print(f"Authorized Identities: {list(unique_identities)}")
        print(f"Loaded {len(documents)} documents ...\n")
        return documents

    def add_docs_to_pinecone(self, documents) -> PineconeVectorStore:
        """
        Create a Pinecone index and load documents into it
        """
        # configure client
        pc = Pinecone(api_key=PINECONE_API_KEY)

        use_serverless = True
        if use_serverless:
            spec = ServerlessSpec(cloud="aws", region="us-west-2")
        else:
            environment = "gcp-starter"
            # if not using a starter index, you should specify a pod_type too
            spec = PodSpec(environment=environment)

        # check for and delete index if already exists
        if self.pinecone_index_name in pc.list_indexes().names():
            print(f"Index {self.pinecone_index_name} already exists. ")
            #  Delete and create a new index
            # pc.delete_index(self.pinecone_index_name)
            print(f"Deleted index {self.pinecone_index_name}.")
        else:
            print(f"Creating index {self.pinecone_index_name}...")
            # create a new index
            pc.create_index(
                self.pinecone_index_name,
                dimension=1536,  # dimensionality of text-embedding-ada-002
                metric="dotproduct",
                spec=spec,
            )

        # wait for index to be initialized
        while not pc.describe_index(self.pinecone_index_name).status["ready"]:
            time.sleep(1)

        index = pc.Index(self.pinecone_index_name)
        index.describe_index_stats()

        print("Creating embeddings and Loading docs into index...")
        texts = [t.page_content for t in documents]
        metadatas = [t.metadata for t in documents]
        # pop "coordinates" from metadata
        for metadata in metadatas:
            metadata.pop("coordinates", None)

        vector_store = PineconeVectorStore.from_texts(
            texts,
            self.embeddings,
            metadatas=metadatas,
            index_name=self.pinecone_index_name,
        )
        # vector_store = PineconeVectorStore.from_documents(
        #     documents, self.embeddings, index_name=self.pinecone_index_name
        # )
        # wait for index to be initialized
        print("Waiting for index to be ready...")
        time.sleep(0)

        print("Done!")
        return vector_store


if __name__ == "__main__":
    print("Loading documents to Qdrant ...")
    def_folder_id = "<google_drive_folder_id>"
    input_index_name = "identity-enabled-rag"

    pinecone_data_loader = IdentityBasedDataLoader(def_folder_id, input_index_name)

    result_documents = pinecone_data_loader.load_documents()

    vectordb_obj = pinecone_data_loader.add_docs_to_pinecone(result_documents)
    print(f"First document: {result_documents[0]}")
    print("Finished hydrating Vector DB ...\n")
