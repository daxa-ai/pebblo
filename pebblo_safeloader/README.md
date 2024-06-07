# Overview

`Pebblo SafeLoader` provides visibility and enforcement for Semantic, Entity, and Identity of data ingested into RAG applications.

Pebblo Safeloader enables safe data ingestion for Langchain document loader. This is done by wrapping the document loader call with `Pebblo Safe DataLoader`.

The Pebblo SafeLoader can be enabled with few lines of code change to the above snippet.

```python
    from langchain_community.document_loaders import CSVLoader
    from langchain_community.document_loaders.pebblo import PebbloSafeLoader

    loader = PebbloSafeLoader(
                CSVLoader(file_path),
                name="RAG app 1", # App name (Mandatory)
                owner="Joe Smith", # Owner (Optional)
                description="Support productivity RAG application", # Description (Optional)
    )
    documents = loader.load()
    vectordb = Chroma.from_documents(documents, OpenAIEmbeddings())
```

## LangChain

`Pebblo SafeLoader` is upstreamed to LangChain as special Document Loader.

Refer to LangChain documentation at:
https://python.langchain.com/docs/integrations/document_loaders/pebblo
