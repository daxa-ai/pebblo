import logging
from typing import List

from dotenv import load_dotenv

load_dotenv()

from langchain.chains import RetrievalQA
from langchain_community.document_loaders import DataFrameLoader
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_openai.llms import OpenAI
from langchain.schema import Document
from langchain_community.vectorstores import Chroma
from langchain.vectorstores.utils import filter_complex_metadata
import pandas as pd
from pebblo_langchain.langchain_community.document_loaders.pebblo import PebbloSafeLoader

logging.basicConfig(level=20)


class OpenAIGenieDf:
    def __init__(self, file_path: str):
        self.df = pd.read_csv(file_path)
        self.loader = PebbloSafeLoader(
            DataFrameLoader(self.df, page_content_column="Credit Card Number"),
            "Dinesh DataFrame Loader", " Dinesh Kumar S", "Dinesh Testing DataFrame Loader"
        )
        # TODO: set source path
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
    file_path = "../data/sens_data.csv"
    genie = OpenAIGenieDf(file_path)
    # prompt = "When liquid templates are evaluated?"
    # Response: When source files are rendered.
    # prompt = "What happens during the build process?"
    # Response: During the build process, magicbook will transfer all files located in images to the asset folder of each build and replace the image src attribute appropriately.
    # prompt = "What does digest option do?"
    # Response:  The digest option adds a md5 checksum of the image content to the filename, to allow you to set long caching headers for a production website.
    # prompt = "What is the capital of California?"
    prompt = "What does 213.85.121.199 mean?"
    response = genie.ask(prompt)
    print(f"Response:\n{response}")
