# Identity-enabled RAG using PebbloRetrievalQA

PebbloRetrievalQA is a Retrieval chain with Identity & Semantic Enforcement for question-answering against a vector database.

This document covers how to retrieve documents with Identity & Semantic Enforcement.

To start, we will load documents with authorization metadata into an in-memory Qdrant vector database we want to use and then use it as a retriever in
PebbloRetrievalQA.

Next, we will define an "ask" function that loads the PebbloRetrievalQA chain using the retriever and provided auth_context.
Finally, we will ask it questions with authorization context for authorized users and unauthorized users.

PebbloRetrievalQA enables safe retrieval with Identity & Semantic Enforcement.

## Setup

### Dependencies

We need Langchain, langchain-community, langchain-openai and a Qdrant client for this walkthrough.

```bash
%pip install --upgrade --quiet  langchain langchain-community langchain-openai qdrant_client
```

### Identity-aware Data Ingestion

Here we are using Qdrant as a vector database; however, you can use any of the supported vector databases.

**PebbloRetrievalQA chain supports the following vector databases:**

1. Qdrant
1. Pinecone

**Load vector database with authorization information in metadata:**

In this step, we capture the authorization information of the source document into the `authorized_identities` field within the metadata of the
VectorDB
entry for each chunk.

_NOTE: To use the PebbloRetrievalQA chain, you always need to place authorization metadata in the `authorized_identities` field, which must be a list
of strings._

The Pebblo SafeLoader can be enabled with few lines of code change to the above snippet.

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
from langchain.chains import PebbloRetrievalQA
from langchain.chains.pebblo_retrieval.models import AuthContext, ChainInput

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

We ingested data for authorized identities ["hr-support", "hr-leadership"], so a user with the
authorized identity/group "hr-support" should receive the correct answer.

```python
auth = {
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

Since the user's authorized identity/group "eng-support" is not included in the authorized identities ["hr-support", "hr-leadership"], we should not
receive an answer.

```python
auth = {
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
