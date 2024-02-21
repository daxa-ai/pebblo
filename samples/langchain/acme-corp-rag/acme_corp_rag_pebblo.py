from langchain.chains import RetrievalQA
from langchain.document_loaders.csv_loader import CSVLoader
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_openai.llms import OpenAI
from langchain.schema import Document
from langchain_community.vectorstores import Chroma
from langchain_community.vectorstores.utils import filter_complex_metadata
from typing import List

from langchain_community.document_loaders.pebblo import PebbloSafeLoader

# Fill-in OPENAI_API_KEY in .env file
# in this directory before proceeding

from dotenv import load_dotenv
load_dotenv()

class AcmeCorpRAG:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.app_name = "acme-corp-rag-1"

        # Load documents

        print("Loading RAG documents ...")
        self.loader = PebbloSafeLoader(
            CSVLoader(self.file_path),
            name="acme-corp-rag-1", # App name (Mandatory)
            owner="Joe Smith",      # Owner (Optional)
            description="Support productivity RAG application", # Description (Optional)
        )
        self.documents = self.loader.load()
        self.filtered_docs = filter_complex_metadata(self.documents)
        print(f"Loaded {len(self.documents)} documents ...\n")

        # Load documents into VectorDB

        print("Hydrating Vector DB ...")
        self.vectordb = self.embeddings(self.filtered_docs)
        print("Finished hydrating Vector DB ...\n")

        # Prepare retriever QA chain

        llm = OpenAI()
        self.retriever = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=self.vectordb.as_retriever(),
            verbose=True
        )

    @staticmethod
    def embeddings(docs: List[Document]):
        embeddings = OpenAIEmbeddings()
        vectordb = Chroma.from_documents(docs, embeddings)
        return vectordb

    def ask(self, query: str):
        return self.retriever.invoke(query)


if __name__ == "__main__":
    rag_app = AcmeCorpRAG("./data/topic_data.csv")
    prompt = "What is adaptive pacing system?"
    print(f"Query:\n{prompt}")
    response = rag_app.ask(prompt)
    print(f"Response:\n{response}")
