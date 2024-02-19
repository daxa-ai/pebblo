import logging
from typing import List

from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.schema import Document
from langchain.vectorstores.utils import filter_complex_metadata
from langchain_community.vectorstores import Chroma
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_openai.llms import OpenAI
from pebblo_langchain.langchain_community.document_loaders.pebblo import PebbloSafeLoader

load_dotenv()
logging.basicConfig(level=10)


class OpenAIGenieCsv:
    def __init__(self, file_path: str):
        self.loader = PebbloSafeLoader(
            CSVLoader(file_path), "Dinesh_Automation_Testing_CSVLoader", "Dinesh Kumar S",
            "CSV Loader Working as expected"
        )
        self.documents = self.loader.load()
        self.filtered_docs = filter_complex_metadata(self.documents)
        self.vectordb = self.embeddings(self.filtered_docs)
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
        return self.retriever.run(query)


if __name__ == "__main__":
    file_path = "./data/sens_data.csv"
    genie = OpenAIGenieCsv(file_path)
    prompt = "What does 213.85.121.199 mean?"
    response = genie.ask(prompt)
    print(f"Response:\n{response}")
