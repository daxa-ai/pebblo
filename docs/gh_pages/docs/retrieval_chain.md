# Safe Retriever for LangChain
***Identity-enabled RAG using PebbloRetrievalQA***

`PebbloRetrievalQA` is a Retrieval chain with Identity & Semantic Enforcement for question-answering against a vector database.

This document covers how to retrieve documents with Identity & Semantic Enforcement.

**Steps:**

- **Loading Documents with Authorization metadata:** The process starts by loading documents with option to pull additional authorization metadata turned on. See supported loader specific documentation for exact input field (typically `load_auth=True`),
- **Using supported Vector database** `PebbloRetrievalQA` chain requires a Vector database that supports rich metadata filtering capability. Pick one from the supported Vector database vendor list shown below in this document.
- **Initializing PebbloRetrievalQA Chain:**  After loading the documents, the PebbloRetrievalQA chain is initialized. This chain uses the retriever (
  created from the vector database) and an LLM.
- **The 'ask' Function:**  The 'ask' function is used to pose questions to the system. This function accepts a question and an auth_context as input
  and returns the answer using the PebbloRetrievalQA chain. The auth_context contains the identity and authorization groups of the user accessing the
  application.
- **Posing Questions:** Finally, questions are posed to the system. The system retrieves answers based on the authorization metadata in the documents
  and the auth_context provided in the 'ask' function.

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
1. Postgres(utilizing the pgvector extension)

**Load vector database with authorization information in metadata:**

In this phase, the authorization details of the original document are captured and stored in the `authorized_identities` field within the metadata of
each chunk in the VectorDB entry.

_It's important to note that to use the PebbloRetrievalQA chain, authorization metadata must always be placed in the `authorized_identities`
field._

```python
from langchain_community.vectorstores.qdrant import Qdrant
from langchain_core.documents import Document
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_openai.llms import OpenAI

llm = OpenAI()
embeddings = OpenAIEmbeddings()
collection_name = "pebblo-identity-rag"

page_content = """
Performance Report: John Smith
Employee Information:
    •Name: John Smith
    •Employee ID: JS12345
    •Department: Sales
    •Position: Sales Representative
    •Review Period: January 1, 2023 - December 31, 2023

Performance Summary: 
John Smith has demonstrated commendable performance as a Sales Representative during the review period. 
He consistently met and often exceeded sales targets, contributing signiﬁcantly to the department's success. 
His dedication, professionalism, and collaborative approach have been instrumental in fostering positive 
relationships with clients and colleagues alike.

Key Achievements:
•Exceeded sales targets by 20% for the ﬁscal year, demonstrating exceptional sales acumen and strategic planning skills.
•Successfully negotiated several high-value contracts, resulting in increased revenue and client satisfaction.
•Proactively identiﬁed opportunities for process improvement within the sales team, 
    leading to streamlined workﬂows and enhanced efﬁciency.
•Received positive feedback from clients and colleagues for excellent communication skills, responsiveness, and customer service.
    Areas for Development: While John's performance has been exemplary overall, 
there are opportunities for further development in certain areas:
•Continued focus on expanding product knowledge to better address client needs and provide tailored solutions.
•Enhancing time management skills to prioritize tasks effectively and maximize productivity during busy periods.
•Further development of leadership abilities to support and mentor junior team members within the sales department.

Conclusion: In conclusion, John Smith has delivered outstanding results as a Sales Representative at ACME Corp. 
His dedication, performance, and commitment to excellence reﬂect positively on the organization." 
"""

documents = [
    Document(
        **{
            "page_content": page_content,
            "metadata": {
                "authorized_identities": ["hr-support", "hr-leadership"],
                "page": 0,
                "source": "https://drive.google.com/file/d/xxxxxxxxxxxxx/view",
                "title": "Performance Report- John Smith.pdf",
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

## Retrieval with Identity & Semantic Enforcement

PebbloRetrievalQA chain uses a SafeRetrieval to enforce that the snippets used for in-context are retrieved
only from the documents authorized for the user.
To achieve this, the Gen-AI application needs to provide an authorization context for this retrieval chain.
This `auth_context` should be filled with the identity and authorization groups of the user accessing the Gen-AI app.

Here is the sample code for the PebbloRetrievalQA with `authorized_identities` from the user accessing the RAG
application, passed in `auth_context`.

```python
from langchain_community.chains import PebbloRetrievalQA
from langchain_community.chains.pebblo_retrieval.models import AuthContext, ChainInput

# Initialize PebbloRetrievalQA chain
qa_chain = PebbloRetrievalQA.from_chain_type(
    llm=llm,
    app_name="pebblo-identity-and-semantic-retriever",
    owner="Joe Smith",
    description="Identity and Semantic filtering using PebbloSafeLoader, and PebbloRetrievalQA",
    chain_type="stuff",
    retriever=vectordb.as_retriever(),
    verbose=True,
)

def ask(question: str, auth_context: dict):
    """
    Ask a question to the PebbloRetrievalQA chain
    """
    auth_context_obj = AuthContext(**auth_context) if auth_context else None
    chain_input_obj = ChainInput(query=question, auth_context=auth_context_obj)
    return qa_chain.invoke(chain_input_obj.dict())
```

### Questions by Authorized User

Data has been ingested for the authorized identities ["hr-support", "hr-leadership"].
Therefore, a user who belongs to the "hr-support" authorized identity or group should be able to receive the correct answer.

```python
auth = {
    "user_id": "hr-user@acme.org",
    "authorized_identities": [
        "hr-support",
    ]
}

question = "Please share the performance report for John Smith?"
resp = ask(question, auth)
print(f"Question: {question}\n\nAnswer: {resp['result']}\n")
```

Output:

```bash
Question: Please share the performance summary for John Smith?

Answer: 
John Smith has demonstrated commendable performance as a Sales Representative during the review period. 
He consistently met and often exceeded sales targets, contributing signiﬁcantly to the department's success. 
His dedication, professionalism, and collaborative approach have been instrumental in fostering positive 
relationships with clients and colleagues alike.
```

### Questions by Unauthorized User

Since the user's authorized identity/group "eng-support" is not included in the authorized identities ["hr-support", "hr-leadership"], they should not
expect to receive an answer.

```python
auth = {
    "user_id": "eng-user@acme.org",
    "authorized_identities": [
        "eng-support",
    ]
}

question = "Please share the performance report for John Smith?"
resp = ask(question, auth)
print(f"Question: {question}\n\nAnswer: {resp['result']}\n")
```

Output:

```bash
Question: Please share the performance summary for John Smith?

Answer: 
I don't know, I'm sorry.
```
