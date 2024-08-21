# Pebblo Safe DataReader for LlamaIndex

This document describes how to augment your existing Llama DocumentReader with Pebblo Safe DocumentReader to get deep data visibility on the types of Topics and Entities ingested into the Gen-AI LlamaIndex application. For details on `Pebblo Daemon` see this [pebblo server](daemon.md) document.

Pebblo Safe DocumentReader enables safe data ingestion for Llama `DocumentReader`. This is done by wrapping the document reader call with `Pebblo Safe DocumentReader`

## How to Pebblo enable Document Reading?

Assume a LlamaIndex RAG application snippet using `CSVReader` to read a CSV document for inference.

Here is the snippet of Document loading using `CSVReader`

```
from pathlib import Path
from llama_index.readers.file import CSVReader
reader = CSVReader()
documents = reader.load_data(file=Path('data/corp_sens_data.csv'))
print(documents)
```

The Pebblo SafeReader can be installed and enabled with few lines of code change to the above snippet.

### Install PebbloSafeReader

```
pip install llama-index-readers-pebblo
```

### Use PebbloSafeReader

```
from pathlib import Path
from llama_index.readers.pebblo import PebbloSafeReader
from llama_index.readers.file import CSVReader
reader = CSVReader()
pebblo_reader = PebbloSafeReader(reader,
    name="acme-corp-rag-1", # App name (Mandatory)
    owner="Joe Smith", # Owner (Optional)
    description="Support productivity RAG application"),
    documents = pebblo_reader.load_data(file=Path('data/corp_sens_data.csv')
)
```

A data report with all the findings, both Topics and Entities, will be generated and available for inspection in the `Pebblo Server`. See this [pebblo server](daemon.md) for further details.

Note: By default Pebblo Server runs at localhost:8000. If your Pebblo Server is running at some other location for eg. a docker container etc, put the correct URL in `PEBBLO_CLASSIFIER_URL` env variable. ref: [server-configurations](config.md#server)

```bash
export PEBBLO_CLASSIFIER_URL="<pebblo-server-host:pebblo-server-port>"
```

## Supported Document Readers

The following LlamaIndex DocumentReaders are currently supported.

1. PDFReader
1. DocxReader
1. CSVReader


> Note : _Most other LlamaIndex document readers that implement load_data() method should work. The above list indicates the ones that are explicitly tested. If you have successfully tested a particular DocumentReader other than this list above, please consider raising a PR.