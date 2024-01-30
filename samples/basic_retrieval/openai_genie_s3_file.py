from dotenv import load_dotenv
load_dotenv()
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import S3FileLoader
from pebblo_langchain.langchain_community.document_loaders.pebblo import PebbloSafeLoader
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_openai.llms import OpenAI
from langchain.schema import Document
from langchain_community.vectorstores import Chroma
from langchain.vectorstores.utils import filter_complex_metadata

import logging
from typing import List

logging.basicConfig(level=20)

class OpenAIGenieS3:
    def __init__(self, bucket: str, key: str):
        self.app_name = "rahul_s3_file_app_2"
        self.loader = PebbloSafeLoader(
            S3FileLoader(bucket, key),
            self.app_name, "rahul", "some_App_Description"
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
    bucket = "rahul-bucket-98998"
    key = "fake_data_new121(1).csv"
    genie = OpenAIGenieS3(bucket, key)
    prompt = "What does 213.85.121.199 mean?"
    response = genie.ask(prompt)
    print(f"Response:\n{response}")
