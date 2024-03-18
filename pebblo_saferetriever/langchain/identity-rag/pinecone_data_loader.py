import time

from langchain_community.vectorstores import Pinecone as PineconeVectorStore
from pinecone import Pinecone, PodSpec, ServerlessSpec


def create_pinecone_index(
    pinecone_api_key, index_name, embeddings, documents
) -> PineconeVectorStore:
    """
    Create a Pinecone index and load documents into it
    """
    # configure client
    pc = Pinecone(api_key=pinecone_api_key)

    use_serverless = True
    if use_serverless:
        spec = ServerlessSpec(cloud="aws", region="us-west-2")
    else:
        environment = "gcp-starter"
        # if not using a starter index, you should specify a pod_type too
        spec = PodSpec(environment=environment)

    # check for and delete index if already exists
    if index_name in pc.list_indexes().names():
        print(f"Index {index_name} already exists. ")
        #  Delete and create a new index
        pc.delete_index(index_name)
        print(f"Deleted index {index_name}.")

    print(f"Creating index {index_name}...")
    # create a new index
    pc.create_index(
        index_name,
        dimension=1536,  # dimensionality of text-embedding-ada-002
        metric="dotproduct",
        spec=spec,
    )

    # wait for index to be initialized
    while not pc.describe_index(index_name).status["ready"]:
        time.sleep(1)

    index = pc.Index(index_name)
    index.describe_index_stats()

    print("Creating embeddings and Loading docs into index...")
    texts = [t.page_content for t in documents]
    metadatas = [t.metadata for t in documents]

    vector_store = PineconeVectorStore.from_texts(
        texts, embeddings, metadatas=metadatas, index_name=index_name
    )
    # wait for index to be initialized
    print("Waiting for index to be ready...")
    time.sleep(15)

    print("Done!")
    return vector_store
