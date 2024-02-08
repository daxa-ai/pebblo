# Pebblo Daemon

`Pebblo Daemon` is a REST API application that exposes API endpoints for Pebblo Safe DataLoader to connect. This component provides deep data visibility on the types of Topics and Entities ingested into the Gen-AI application. It uses the snippets received from the `Pebblo Safe DataLoader` to run through both a Topic Classifier and Entity Classifier to produce the insights and reporting. For more details on how to Pebblo enable your Langchain application see this [Pebblo Safe DataLoader for Langchain](rag.md) document.

By default `Pebblo Daemon` runs at `localhost:8000`. The `Pebblo Safe DataLoader` by default connects to this hostname and port. If the daemon is running in a different port or a different hostname, the `Pebblo Safe DataLoader` env variable `PEBBLI_CLASSIFIER_URL` need to set to the correct URL.

## Report Generation

A separate `Data Report` will be generated for every complete document load operation. A subsequent document loader, either done periodically (say everyday, every week, etc) or on-demand will not overwrite a previous load's `Data Report`.

## Report Location

By default all the reports will be stored in a `.pebblo` in the home directory of the system running `Pebblo Daemon`. Separate subdirectories named with the RAG application name is used when multiple RAG applications uses the same `Pebblo Daemon`.

```bash

$ cd $HOME/.pebblo
$ tree
├── acme-corp-rag-1
│   ├── pebblo_report.pdf
│   ├── bfd46d34-42c7-4819-846c-f54b3620f540
│   │   ├── metadata
│   │   │   └── metadata.json
│   │   └── report.json
```
