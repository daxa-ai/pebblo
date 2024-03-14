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

Pebblo has two components.

1. Pebblo Server - a REST api application with topic-classifier, entity-classifier and reporting features
1. Pebblo Safe DataLoader - a thin wrapper to Gen-AI framework's data loaders

## Pebblo Server

### Installation


```bash
pip install pebblo
```

### Run Pebblo Server

```bash
pebblo
```

Pebblo Server now listens to `localhost:8000` to accept Gen-AI application data snippets for inspection and reporting.

#### Pebblo Optional Flags

- `--config <file>`: specify a configuration file in yaml format.


See [configuration](docs/gh_pages/docs/config.md) guide for knobs to control Pebblo Server behavior like enabling snippet anonymization, selecting specific report renderer, etc.

#### Troubleshooting

Refer to [troubleshooting](docs/gh_pages/docs/troubleshooting.md) guide.

## Pebblo Safe DataLoader

### Langchain

`Pebblo Safe DataLoader` is natively supported in Langchain framework. It is available in Langchain versions `>=0.1.7`

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

See [here](https://github.com/srics/pebblo/tree/main/samples) for samples with Pebblo enabled RAG applications and [this](https://daxa-ai.github.io/pebblo/rag) document for more details.

# Contribution

Pebblo is a open-source community project. If you want to contribute see [Contributor Guidelines](https://github.com/daxa-ai/pebblo/blob/main/CONTRIBUTING.md) for more details.

# License

Pebblo is released under the MIT License
