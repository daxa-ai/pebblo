import os
import time

from dotenv import load_dotenv
from pinecone import Pinecone, PodSpec

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")


def create_pinecone_index(pinecone_index_name: str, recreate: bool = False):
    """
    Create a new Pinecone index
    """

    # configure client
    pc = Pinecone(api_key=PINECONE_API_KEY)
    # Update the environment/PodSpec to match the one you have access to
    environment = "gcp-starter"
    spec = PodSpec(environment=environment)

    # check for and delete index if already exists
    if pinecone_index_name in pc.list_indexes().names():
        if not recreate:
            print(f"Index {pinecone_index_name} already exists. skipping...")
            return
        else:
            #  Delete and create a new index
            print(f"Deleting and recreating index: {pinecone_index_name} ...")
            pc.delete_index(pinecone_index_name)
            print(f"Deleted index: {pinecone_index_name}.")

    print(f"Creating index: {pinecone_index_name}...")
    # create a new index
    pc.create_index(
        pinecone_index_name,
        dimension=1536,  # dimensionality of text-embedding-ada-002
        metric="dotproduct",
        spec=spec,
    )

    # wait for index to be initialized
    while not pc.describe_index(pinecone_index_name).status["ready"]:
        time.sleep(1)

    index = pc.Index(pinecone_index_name)
    index.describe_index_stats()
