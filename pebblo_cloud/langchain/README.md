# Overview

`Pebblo Cloud` provides multiple features like policy, slack/jira integrations, etc.

Pebblo Cloud can be enabled by adding API key in the Pebblo SafeLoader and Pebblo SafeRetriever initializations. 

```python
    from langchain_community.document_loaders import CSVLoader
    from langchain_community.document_loaders.pebblo import PebbloSafeLoader

    loader = PebbloSafeLoader(
                CSVLoader(file_path),
                name="RAG app 1", # App name (Mandatory)
                owner="Joe Smith", # Owner (Optional)
                description="Support productivity RAG application", # Description (Optional),
                api_key="<api-key>" # API key(Optional),
    )
    documents = loader.load()
    vectordb = Qdrant.from_documents(documents, embeddings)
```