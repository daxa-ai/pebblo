# Safe Retriever for LangChain

***Semantic Enforcement RAG using PebbloRetrievalQA***

`PebbloRetrievalQA` is a Retrieval chain with Identity & Semantic Enforcement for question-answering against a vector database.

This document covers how to retrieve documents with Semantic Enforcement.

**Steps:**

- **Loading Documents with Semantic metadata:** The process starts by loading documents with semantic metadata.
- **Using supported Vector database** `PebbloRetrievalQA` chain requires a Vector database that supports rich metadata filtering capability. Pick one
  from the supported Vector database vendor list shown below in this document.
- **Initializing PebbloRetrievalQA Chain:**  After loading the documents, the PebbloRetrievalQA chain is initialized. This chain uses the retriever (
  created from the vector database) and an LLM.
- **The 'ask' Function:**  The 'ask' function is used to pose questions to the system. This function accepts a question and an semantic_context as
  input and returns the answer using the PebbloRetrievalQA chain. The semantic context contains the topics and entities that should be denied within
  the context used to generate a response.
- **Posing Questions:** Finally, questions are posed to the system. The system retrieves answers based on the semantic metadata in the documents
  and the semantic_context provided in the 'ask' function.

## Setup

### Dependencies

The walkthrough requires Langchain, langchain-community, langchain-openai, and a Qdrant client.

```bash
%pip install --upgrade --quiet  langchain langchain-community langchain-openai qdrant_client
```

### Identity-aware Data Ingestion

In this scenario, Qdrant is being utilized as a vector database. However, the flexibility of the system allows for the use of any supported vector
databases.

**PebbloRetrievalQA chain supports the following vector databases:**

1. Qdrant
1. Pinecone

**Load vector database with semantic information in metadata:**

In this phase, the semantic topics and entities of the original document are captured and stored in the `pebblo_semantic_topics`
and `pebblo_semantic_entities` fields respectively within the metadata of
each chunk in the VectorDB entry.

_It's important to note that to use the PebbloRetrievalQA chain, semantic metadata must always be placed in the `pebblo_semantic_topics`
and `pebblo_semantic_entities` fields._

```python
from langchain_community.vectorstores.qdrant import Qdrant
from langchain_core.documents import Document
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_openai.llms import OpenAI

llm = OpenAI()
embeddings = OpenAIEmbeddings()
collection_name = "pebblo-semantic-rag"

page_content = """
**ACME Corp Financial Report**

**Overview:**
ACME Corp, a leading player in the merger and acquisition industry, presents its financial report for the fiscal year ending December 31, 2020. 
Despite a challenging economic landscape, ACME Corp demonstrated robust performance and strategic growth.

**Financial Highlights:**
Revenue soared to $50 million, marking a 15% increase from the previous year, driven by successful deal closures and expansion into new markets. 
Net profit reached $12 million, showcasing a healthy margin of 24%.

**Key Metrics:**
Total assets surged to $80 million, reflecting a 20% growth, highlighting ACME Corp's strong financial position and asset base. 
Additionally, the company maintained a conservative debt-to-equity ratio of 0.5, ensuring sustainable financial stability.

**Future Outlook:**
ACME Corp remains optimistic about the future, with plans to capitalize on emerging opportunities in the global M&A landscape. 
The company is committed to delivering value to shareholders while maintaining ethical business practices.

**Bank Account Details:**
For inquiries or transactions, please refer to ACME Corp's US bank account:
Account Number: 123456789012
Bank Name: Fictitious Bank of America
"""

documents = [
    Document(
        **{
            "page_content": page_content,
            "metadata": {
                "pebblo_semantic_topics": ["financial-report"],
                "pebblo_semantic_entities": ["us-bank-account-number"],
                "page": 0,
                "source": "https://drive.google.com/file/d/xxxxxxxxxxxxx/view",
                "title": "ACME Corp Financial Report.pdf",
            },
        }
    )
]

print("Loading vectordb...")

vectordb = Qdrant.from_documents(
    documents,
    embeddings,
    location=":memory:",
    collection_name=collection_name,
)

print("Vectordb loaded.")
```

## Retrieval with Semantic Enforcement

The PebbloRetrievalQA chain uses SafeRetrieval to ensure that the snippets used in context are retrieved only from documents that comply with the
provided semantic context.
To achieve this, the Gen-AI application must provide a semantic context for this retrieval chain.
This `semantic_context` should include the topics and entities that should be denied for the user accessing the Gen-AI app.

Below is a sample code for PebbloRetrievalQA with `topics_to_deny` and `entities_to_deny`. These are passed in `semantic_context` to the chain input.

```python
from typing import Optional, List
from langchain_community.chains import PebbloRetrievalQA
from langchain_community.chains.pebblo_retrieval.models import (
    ChainInput,
    SemanticContext,
)

# Initialize PebbloRetrievalQA chain
qa_chain = PebbloRetrievalQA.from_chain_type(
    llm=llm,
    app_name="pebblo-semantic-retriever-rag",
    owner="Joe Smith",
    description="Semantic filtering using PebbloSafeLoader, and PebbloRetrievalQA",
    chain_type="stuff",
    retriever=vectordb.as_retriever(),
    verbose=True,
)


def ask(
    question: str,
    topics_to_deny: Optional[List[str]] = None,
    entities_to_deny: Optional[List[str]] = None,
):
    """
    Ask a question to the PebbloRetrievalQA chain
    """
    semantic_context = dict()
    if topics_to_deny:
        semantic_context["pebblo_semantic_topics"] = {"deny": topics_to_deny}
    if entities_to_deny:
        semantic_context["pebblo_semantic_entities"] = {"deny": entities_to_deny}

    semantic_context_obj = (
        SemanticContext(**semantic_context) if semantic_context else None
    )
    chain_input_obj = ChainInput(query=question, semantic_context=semantic_context_obj)
    return qa_chain.invoke(chain_input_obj.dict())
```

## Ask questions

### Without semantic enforcement

Since no semantic enforcement is applied, the system should return the answer.

```python
topic_to_deny = []
entities_to_deny = []
question = "Please share the financial performance of ACME Corp for 2020"
resp = ask(question, topics_to_deny=topic_to_deny, entities_to_deny=entities_to_deny)
print(
    f"Topics to deny: {topic_to_deny}\nEntities to deny: {entities_to_deny}\n"
    f"Question: {question}\nAnswer: {resp['result']}\n"
)
```

Output:

```bash
Topics to deny: []
Entities to deny: []
Question: Please share the financial performance of ACME Corp for 2020
Answer: 
ACME Corp had a strong financial performance in 2020, with a 15% increase in revenue to $50 million and a net profit of $12 million, 
indicating a healthy margin of 24%. The company also saw a 20% growth in total assets, reaching $80 million. 
ACME Corp maintained a conservative debt-to-equity ratio of 0.5, ensuring financial stability. 
The company has plans to capitalize on emerging opportunities in the global M&A landscape and is committed to delivering value 
to shareholders while maintaining ethical business practices. 
```

### Deny financial-report topic

Data has been ingested with the topics: ["financial-report"].
Therefore, a app that denies the "financial-report" topic should not receive an answer.

```python
topic_to_deny = ["financial-report"]
entities_to_deny = []
question = "Please share the financial performance of ACME Corp for 2020"
resp = ask(question, topics_to_deny=topic_to_deny, entities_to_deny=entities_to_deny)
print(
    f"Topics to deny: {topic_to_deny}\nEntities to deny: {entities_to_deny}\n"
    f"Question: {question}\nAnswer: {resp['result']}\n"
)
```

Output:

```bash
Topics to deny: ['financial-report']
Entities to deny: []
Question: Please share the financial performance of ACME Corp for 2020
Answer:  Unfortunately, I do not have access to that information.
```

### Deny us-bank-account-number entity

Since the entity "us-bank-account-number" is denied, the system should not return the answer.

```python
topic_to_deny = []
entities_to_deny = ["us-bank-account-number"]
question = "Please share the financial performance of ACME Corp for 2020"
resp = ask(question, topics_to_deny=topic_to_deny, entities_to_deny=entities_to_deny)
print(
    f"Topics to deny: {topic_to_deny}\nEntities to deny: {entities_to_deny}\n"
    f"Question: {question}\nAnswer: {resp['result']}\n"
)
```

Output:

```bash
Topics to deny: []
Entities to deny: ['us-bank-account-number']
Question: Please share the financial performance of ACME Corp for 2020
Answer:  Unfortunately, I do not have access to that information.
```
