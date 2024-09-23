# Pebblo Safe DataLoader for Langchain

This document describes how to augment your existing Langchain DocumentLoader with Pebblo Safe DataLoader to get deep data visibility on the types of Topics and Entities ingested into the Gen-AI Langchain application. For details on `Pebblo Server` see this [pebblo server](daemon.md) document.

Pebblo Safeloader enables safe data ingestion for Langchain document loader<sup>1</sup>. This is done by wrapping the document loader call with `Pebblo Safe DataLoader`.

## How to Pebblo enable Document Loading?

Assume a Langchain RAG application snippet using `CSVLoader` to read a CSV document for inference.

Here is the snippet of Lanchain RAG application using `CSVLoader`.

```python
    from langchain_community.document_loaders import CSVLoader

    loader = CSVLoader(file_path)
    documents = loader.load()
    vectordb = Chroma.from_documents(documents, OpenAIEmbeddings())
```

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

A data report with all the findings, both Topics and Entities, will be generated and available for inspection in the `Pebblo Server`. See this [pebblo server](daemon.md) for further details.

Note: By default Pebblo Server runs at localhost:8000. If your Pebblo Server is running at some other location for eg. a docker container etc, put the correct URL in `PEBBLO_CLASSIFIER_URL` env variable. ref: [server-configurations](config.md#server)

```bash
export PEBBLO_CLASSIFIER_URL="<pebblo-server-host:pebblo-server-port>"
```

## Parameters
PebbloSafeLoader takes the following parameters:

| Parameter          | Type          | Description                                                                                                                                                                                   |
|:-------------------|:--------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| name               | str           | Name of the application; should be unique across the loader and retriever applications.                                                                                                       |
| owner              | str           | (**Optional**, Default: None) Owner of the application.                                                                                                                                       |
| description        | str           | (**Optional**, Default: None) Description of the application.                                                                                                                                 |
| loader             | DocumentLoader| Langchain DocumentLoader.                                                                                                                                                                     |
| api_key            | str           | (**Optional**, Default: None) API Key for Pebblo Cloud; if not provided, PebbloSafeLoader will look for `PEBBLO_API_KEY` in the environment. If found, documents will be sent to Pebblo Cloud.|
| load_semantic      | bool          | (**Optional**, Default: False) Indicates whether to include semantic metadata in the documents being loaded into VectorDB.                                                                    |
| classifier_url     | str           | (**Optional**, Default: http://localhost:8000) URL of the Pebblo Classifier Server.                                                                                                           |
| classifier_location| str           | (**Optional**, Default: local) Location of the classifier, local or cloud.                                                                                                                    |
| anonymize_snippets | bool          | (**Optional**, Default: False) Indicates whether to anonymize snippets in the document.                                                                                                       |


## Supported Document Loaders

The following Langchain DocumentLoaders are currently supported.

1. DirectoryLoader
1. JSONLoader
1. CSVLoader
1. DataFrameLoader
1. S3FileLoader
1. S3DirLoader
1. UnstructuredMarkdownLoader
1. UnstructuredPDFLoader
1. UnstructuredFileLoader
1. UnstructuredAPIFileLoader
1. UnstructuredExcelLoader
1. AmazonTextractPDFLoader
1. GCSFileLoader
1. GoogleDriveLoader
1. PyPDFDirectoryLoader
1. PyPDFLoader
1. SharePointLoader

> Note <sup>1</sup>: _Most other Langchain document loaders that implement load() and lazy_load() methods should work. The above list indicates the ones that are explicitly tested. If you have successfully tested a particular DocumentLoader other than this list above, please consider raising an PR._

<img referrerpolicy="no-referrer-when-downgrade" src="https://static.scarf.sh/a.png?x-pxid=663e4c29-b156-42a6-b49e-359111bfbd5b" />
