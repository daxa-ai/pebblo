---
slug: /
---

# Overview

Pebblo enables developers to safely load data and promote their Gen AI app to deployment without worrying about the organization’s compliance and security requirements. The project identifies semantic topics and entities found in the loaded data and summarizes them on the UI or a PDF report.

![Pebblo Overview](../../static/img/pebblo-overview.webp)

# Benefits

1. Identify semantic topics and entities in your data loaded in RAG applications
1. Accelerate time-to-production by effortlessly meeting your organization’s data compliance requirements
1. Mitigate security risks arising from data poisoning and emerging threats.
1. Comply with regulations such as the EU AI Act with custom reports and data records
1. Support for a wide range of Gen AI development frameworks and data loaders

# Components

Pebblo has two components.

1. Pebblo Server - a REST api application with topic-classifier, entity-classifier and reporting
1. Pebblo Safe DataLoader - a thin wrapper to Gen-AI framework's data loaders

`Pebblo Safe DataLoader` currently support Langchain framework. Support for other frameworks like LlamaIndex, Haystack will be added in the upcoming releases.

# Documentation

- [Installation](installation.md)
- [Development Environment](development.md)
- [Pebblo Server](daemon.md)
- [Safe DataLoader for Langchain](rag.md)
- [Configuration](config.md)
- [Reports](reports.md)
- [Troubleshooting](troubleshooting.md)

<img referrerpolicy="no-referrer-when-downgrade" src="https://static.scarf.sh/a.png?x-pxid=5e0e30b5-5738-4d87-90d7-ff7e5324200c" />
