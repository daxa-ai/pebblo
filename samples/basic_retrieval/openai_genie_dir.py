from dotenv import load_dotenv
load_dotenv()
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import DaxaSafeLoader
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_openai import OpenAI
from langchain.schema import Document
from langchain.schema.output import LLMResult
from langchain_community.vectorstores import Chroma
from langchain.vectorstores.utils import filter_complex_metadata

import logging

logging.basicConfig(level=10)

from typing import Any, List, Optional, Sequence

class OpenAIGenieDir:
    def __init__(self, dir_path: str):
        self.loader = DaxaSafeLoader(
            DirectoryLoader(dir_path, loader_cls=PyPDFLoader, show_progress=True),
            "hrproductivity_app_1", "rahul", "data_description"
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
    dir_path = "../data/pdfs/"
    genie = OpenAIGenieDir(dir_path)
    # prompt = "When liquid templates are evaluated?"
    # Response: When source files are rendered.
    # prompt = "What happens during the build process?"
    # Response: During the build process, magicbook will transfer all files located in images to the asset folder of each build and replace the image src attribute appropriately.
    # prompt = "What does digest option do?"
    # Response:  The digest option adds a md5 checksum of the image content to the filename, to allow you to set long caching headers for a production website.
    # prompt = "What is the capital of California?"
    prompt = "What some guides for pdfkit?"
    response = genie.ask(prompt)
    print(f"Response:\n{response}")

