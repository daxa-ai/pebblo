from typing import List

# Fill-in OPENAI_API_KEY in .env file
# in this directory before proceeding
from dotenv import load_dotenv
from langchain.chains import PebbloRetrievalQA
from langchain.schema import Document
from langchain_community.document_loaders import (
    GoogleDriveLoader,
    UnstructuredFileIOLoader,
)
from langchain_community.document_loaders.pebblo import PebbloSafeLoader
from langchain_community.vectorstores.qdrant import Qdrant
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_openai.llms import OpenAI

from google_auth import get_authorized_identities

load_dotenv()


class PebbloIdentityRAG:
    def __init__(self, folder_id: str, collection_name: str):
        self.app_name = "pebblo-identity-rag-1"
        self.collection_name = collection_name

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
        self.vectordb = self.embeddings(self.documents)
        print("Finished hydrating Vector DB ...\n")

        # Prepare LLM
        self.llm = OpenAI()

    def embeddings(self, docs: List[Document]):
        embeddings = OpenAIEmbeddings()
        vectordb = Qdrant.from_documents(
            docs,
            embeddings,
            location=":memory:",
            collection_name=self.collection_name,
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
    collection_name = "identity-enabled-rag"
    rag_app = PebbloIdentityRAG(folder_id, collection_name)

    prompt = "What criteria are used to evaluate employee performance during performance reviews?"
    print(f"Query:\n{prompt}")

    user_1 = "user@clouddefense.io"
    auth = {
        "authorized_identities": get_authorized_identities(user_1),
    }

    response = rag_app.ask(prompt, auth)
    print(f"Response:\n{response}")
