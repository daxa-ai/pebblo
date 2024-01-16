from dotenv import load_dotenv
load_dotenv()
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import DaxaSafeLoader
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_openai.llms import OpenAI
from langchain.schema import Document
from langchain_community.vectorstores import Chroma
from langchain.vectorstores.utils import filter_complex_metadata


from typing import List
import logging

logging.basicConfig(level=10)

class OpenAIGenieDir:
    def __init__(self, file_path: str):
        self.loader = DaxaSafeLoader(PyPDFLoader(file_path),"Pypdf_app_1")
        self.documents = []
        for x in self.loader.lazy_load():
            self.documents.extend(x)
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
    file_path = "../data/guide.pdf"
    genie = OpenAIGenieDir(file_path)
    # prompt = "When liquid templates are evaluated?"
    # Response: When source files are rendered.
    # prompt = "What happens during the build process?"
    # Response: During the build process, magicbook will transfer all files located in images to the asset folder of each build and replace the image src attribute appropriately.
    # prompt = "What does digest option do?"
    # Response:  The digest option adds a md5 checksum of the image content to the filename, to allow you to set long caching headers for a production website.
    # prompt = "What is the capital of California?"
    prompt = "give me basic features of pdfkit?"
    response = genie.ask(prompt)
    print(f"Response:\n{response}")
