## Identity and Semantic Enforcement using Pebblo

This solution uses the following daxa/langchain branch:

- pebblo_0.1.15: https://github.com/daxa-ai/langchain/tree/pebblo_0.1.15

### Prerequisites

1. Sign up and set up your account on Pinecone (https://www.pinecone.io/).

### Instructions

1. Create Python virtual-env

```console
$ python3 -m venv .venv
$ source .venv/bin/activate
```

2. Install dependencies

```console
$ pip3 install -r requirements.txt
```

3. Install langchain-core and langchain-community from the branch `pebblo_0.1.15`

```console  
$ git clone https://github.com/daxa-ai/langchain.git
$ cd langchain
$ git fetch && git checkout pebblo_0.1.15
$ cd libs/community
$ pip3 install langchain-community .
$ cd ../core
$ pip3 install langchain-core .
```

4. Copy the `.env.sample` file to `.env` and populate the necessary environment variable.

5. Update the `pebblo_identity-n-semantic-rag.py` file with the following details:

- _folder_id_: Google Drive folder ID where the documents are stored
- _service_acc_def_: Google service account credentials file path
- _ing_user_email_def_: Google Drive Admin/Ingestion user email ID


5. Run langchain sample app PebbloSafeLoader and PebbloRetrievalQA

```console
$ python3 pebblo_identity-n-semantic-rag.py
```

6. Retrieve the Pebblo PDF report in `$HOME/.pebblo/pebblo-identity-n-semantic-loader-pinecone/pebblo_report.pdf` file path on the system
   where `Pebblo Server` is
   running.

7. To access the Pebblo UI, point the browser to `https://localhost:8000/pebblo`  or `host:port/pebblo` if you are running the server on a different
   host. 
