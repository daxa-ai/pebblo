
# Overview

Pebblo enables developers to safely load data and promote their Gen AI app to deployment without worrying about the organization’s compliance and security requirements. The project identifies semantic topics and entities found in the loaded data and summarizes them on the UI or a PDF report.

![Pebblo Overview](/pebblo-docs/assets/img/pebblo-overview.jpg)

# Benefits

1. Identify semantic topics and entities in your data loaded in RAG applications
1. Accelerate time-to-production by effortlessly meeting your organization’s data compliance requirements
1. Mitigate security risks arising from data poisoning and emerging threats.
1. Comply with regulations such as the EU AI Act with custom reports and data records
1. Support for a wide range of Gen AI development frameworks and data loaders

# Components

Pebblo has two components.

1. Pebblo Daemon - a REST api application with topic-classifier, entity-classifier and reporting
1. Pebblo Safe DataLoader - a thin wrapper to Gen-AI framework's data loaders

`Pebblo Safe DataLoader` currently support Langchain framework. Support for other frameworks like LlamaIndex, Haystack will be added in the upcoming releases.

# Documentation

- [Installation](/pebblo-docs/installation.html)
- [Development Environment](/pebblo-docs/development.html)
- [Pebblo Daemon](/pebblo-docs/daemon.html)
- [Pebblo Safe DataLoader for Langchain](/pebblo-docs/rag.html)
- [Reports](/pebblo-docs/reporting.html)
