# Overview

`Pebblo SafeRetriever` provides visibility and enforcement for Semantic, Entity, and Identity of context retrieval for RAG applications.

### Identity Enforcement

Identity Enforcement needs two parts:

1. Identity aware data retrieval and vector DB ingestion
2. Identity enforcement on the retrieval chain

#### Identity-aware SafeLoader

Here is the sample code for `GoogleDriveLoader` with `load_auth` parameter set to `True`.

```python
        self.loader = PebbloSafeLoader(
            GoogleDriveLoader(
                folder_id=folder_id,
                token_path="./google_token.json",
                recursive=True,
                file_loader_cls=UnstructuredFileIOLoader,
                file_loader_kwargs={"mode": "elements"},
                load_auth=True,
            ),
            name=self.app_name,  # App name (Mandatory)
            owner="Joe Smith",  # Owner (Optional)
            description="Identity enabled SafeLoader and SafeRetrival app using Pebblo",  # Description (Optional)
        )
```

#### SafeRetrieval

Here is the sample code for `Pebblo SafeRetriever` with `authorized_groups` from the user accessing RAG application passed in `auth_context`

```python
    auth = {
        "authorized_groups": [
            "joe@acme.io",
            "hr-group@acme.io",
            "us-employees-group@acme.io",
    ]}
    retriever = PebbloRetrievalQA.from_chain_type(
        llm=self.llm,
        chain_type="stuff",
        retriever=self.vectordb.as_retriever(),
        verbose=True,
        auth_context=auth,
    )
```

## LangChain

This solution uses the following two private LangChain packages:

* langchain-0.1.12-pebbloretriever
* langchain-community-0.1.12-pebbloretriever

Here are the two corresponding PRs in the LangChain for this feature:

1. community: add authorization identities to GoogleDriveLoader #18813
https://github.com/langchain-ai/langchain/pull/18813

1. langchain: add PebbloRetrievalQA chain with Identity & Semantic enforcement #18812
https://github.com/langchain-ai/langchain/pull/18812
