import os

# Fill-in OPENAI_API_KEY in .env file
# in this directory before proceeding
from dotenv import load_dotenv
from langchain.chains import PebbloRetrievalQA
from langchain_community.document_loaders import (
    GoogleDriveLoader,
    UnstructuredFileIOLoader,
)
from langchain_community.document_loaders.pebblo import PebbloSafeLoader
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_openai.llms import OpenAI

from google_auth import get_authorized_identities
from pinecone_data_loader import create_pinecone_index

load_dotenv()


class PebbloIdentityRAG:
    def __init__(self, folder_id: str, index_name: str, pinecone_api_key: str):
        self.app_name = "pebblo-identity-rag-1"
        self.index_name = index_name
        self.pinecone_api_key = pinecone_api_key

        # Load documents
        print("Loading RAG documents ...")
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
        """
        Create embeddings from documents
        """
        embeddings = OpenAIEmbeddings()
        vectordb = create_pinecone_index(
            self.pinecone_api_key, self.index_name, embeddings, self.documents
        )
        return vectordb

    def ask(self, question: str, auth: dict):
        # Prepare retriever QA chain
        retriever = PebbloRetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vectordb.as_retriever(),
            verbose=True,
            auth_context=auth,
        )
        return retriever.invoke(question)


if __name__ == "__main__":
    # TODO: pass the actual GoogleDrive folder id
    # folder_id = "1sd0RqMMJKidf9Pb4YRCI2-NH4Udj885k"

    folder_id = ""
    index_name = "identity-enabled-rag"
    pinecone_api_key = os.environ.get("PINECONE_API_KEY")
    rag_app = PebbloIdentityRAG(folder_id, index_name, pinecone_api_key)

    prompt = "What criteria are used to evaluate employee performance during performance reviews?"
    print(f"Query:\n{prompt}")

    user_1 = "user@clouddefense.io"
    auth = {
        "authorized_identities": get_authorized_identities(user_1),
    }
    response = rag_app.ask(prompt, auth)
    print(f"Response:\n{response}")
