<p align="center">
  <img src="https://github.com/daxa-ai/pebblo/blob/main/docs/gh_pages/static/img/pebblo-logo-name.jpg?raw=true" />
</p>

---
[![GitHub](https://img.shields.io/badge/GitHub-pebblo-blue?logo=github)](https://github.com/daxa-ai/pebblo)
[![MIT license](https://img.shields.io/badge/license-MIT-brightgreen.svg)](http://opensource.org/licenses/MIT)
[![Documentation](https://img.shields.io/badge/Documentation-pebblo-blue?logo=read-the-docs)](https://daxa-ai.github.io/pebblo/)

[![PyPI](https://img.shields.io/pypi/v/pebblo?logo=pypi)](https://pypi.org/project/pebblo/)
![PyPI - Downloads](https://img.shields.io/pypi/dm/pebblo)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pebblo?logo=python&logoColor=gold)

[![Discord](https://img.shields.io/discord/1199861582776246403?logo=discord)](https://discord.gg/wyAfaYXwwv)
[![Twitter Follow](https://img.shields.io/twitter/follow/daxa_ai)](https://twitter.com/daxa_ai)
---


**Pebblo** enables developers to safely load data and promote their Gen AI app to deployment without worrying about the organization’s compliance and security requirements. The project identifies semantic topics and entities found in the loaded data and summarizes them on the UI or a PDF report.

Pebblo has these components.

1. Pebblo Server - a REST api application with topic-classifier, entity-classifier and reporting features
1. Pebblo SafeLoader - a thin wrapper to Gen-AI framework's data loaders
1. Pebblo SafeRetriever - a retrieval QA chain that enforces identity and semantic rules on Vector database retrieval before LLM inference

## Pebblo Server

### Installation
 
#### Using `pip`

```bash
pip install pebblo --extra-index-url https://packages.daxa.ai/simple/
```

#### Download python package
Alternatively, download and install the latest Pebblo python `.whl` package from URL https://packages.daxa.ai/pebblo/0.1.13/pebblo-0.1.13-py3-none-any.whl

Example:
```bash
curl -LO "https://packages.daxa.ai/pebblo/0.1.13/pebblo-0.1.13-py3-none-any.whl" 
pip install pebblo-0.1.13-py3-none-any.whl
```
### Run Pebblo Server

```bash
pebblo
```

Pebblo Server now listens to `localhost:8000` to accept Gen-AI application data snippets for inspection and reporting.

##### Pebblo Optional Flags

- `--config <file>`: specify a configuration file in yaml format.


See [configuration](docs/gh_pages/docs/config.md) guide for knobs to control Pebblo Server behavior like enabling snippet anonymization, selecting specific report renderer, etc.

### Using Docker

```bash
docker run -p 8000:8000 docker.daxa.ai/daxaai/pebblo
```

Local UI can be accessed by pointing the browser to `https://localhost:8000`.

See [installation](docs/gh_pages/docs/installation.md) guide for details on how to pass custom config.yaml and accessing PDF reports in the host machine.

### Troubleshooting

Refer to [troubleshooting](docs/gh_pages/docs/troubleshooting.md) guide.

## Pebblo SafeLoader

### Langchain

`Pebblo SafeLoader` is natively supported in Langchain framework. It is available in Langchain versions `>=0.1.7`

#### Enable Pebblo in Langchain Application

Add `PebbloSafeLoader` wrapper to the existing Langchain document loader(s) used in the RAG application. `PebbloSafeLoader` is interface compatible with Langchain `BaseLoader`. The application can continue to use `load()` and `lazy_load()` methods as it would on an Langchain document loader.

Here is the snippet of Lanchain RAG application using `CSVLoader` before enabling `PebbloSafeLoader`.

```python
    from langchain.document_loaders.csv_loader import CSVLoader

    loader = CSVLoader(file_path)
    documents = loader.load()
    vectordb = Chroma.from_documents(documents, OpenAIEmbeddings())
```

The Pebblo SafeLoader can be enabled with few lines of code change to the above snippet.

```python
    from langchain.document_loaders.csv_loader import CSVLoader
    from langchain_community.document_loaders.pebblo import PebbloSafeLoader

    loader = PebbloSafeLoader(
                CSVLoader(file_path),
                name="acme-corp-rag-1", # App name (Mandatory)
                owner="Joe Smith", # Owner (Optional)
                description="Support productivity RAG application", # Description (Optional)
    )
    documents = loader.load()
    vectordb = Chroma.from_documents(documents, OpenAIEmbeddings())
```

See [here](https://github.com/srics/pebblo/tree/main/pebblo_safeloader) for samples with Pebblo SafeLoader enabled RAG applications and [this](https://daxa-ai.github.io/pebblo/rag) document for more details.

## Pebblo SafeRetriever

### Langchain


PebbloRetrievalQA chain uses a SafeRetrieval to enforce that the snippets used for in-context are retrieved
only from the documents authorized for the user and semantically allowed for the Gen-AI application.

Here is a sample code for the PebbloRetrievalQA with `authorized_identities` from the user accessing the RAG
application, passed in `auth_context`.

```python
from langchain_community.chains import PebbloRetrievalQA
from langchain_community.chains.pebblo_retrieval.models import AuthContext, ChainInput

safe_rag_chain = PebbloRetrievalQA.from_chain_type(
    llm=llm,
    app_name="pebblo-safe-retriever-demo",
    owner="Joe Smith",
    description="Safe RAG demo using Pebblo",
    chain_type="stuff",
    retriever=vectordb.as_retriever(),
    verbose=True,
)

def ask(question: str, auth_context: dict):
    auth_context_obj = AuthContext(**auth_context)
    chain_input_obj = ChainInput(query=question, auth_context=auth_context_obj)
    return safe_rag_chain.invoke(chain_input_obj.dict())
```

See [here](https://github.com/srics/pebblo/tree/main/pebblo_saferetriever) for samples with Pebblo SafeRetriever enabled RAG applications and [this](https://daxa-ai.github.io/pebblo/retrieval_chain) document for more details.

# Contribution

Pebblo is a open-source community project. If you want to contribute see [Contributor Guidelines](https://github.com/daxa-ai/pebblo/blob/main/CONTRIBUTING.md) for more details.

# License

Pebblo is released under the MIT License
