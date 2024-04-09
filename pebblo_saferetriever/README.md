# Overview

`Pebblo SafeRetriever` provides visibility and enforcement for Semantic, Entity, and Identity of context retrieval for RAG applications.

### Identity Enforcement

Identity Enforcement needs two parts:

1. Identity aware data retrieval and vector DB ingestion
2. Identity enforcement on the retrieval chain

#### Identity-aware SafeLoader

Here is the sample code for `GoogleDriveLoader` with `load_auth` parameter set to `True`.

```python
        self.loader = PebbloSafeLoader(
            GoogleDriveLoader(
                folder_id=folder_id,
                token_path="./google_token.json",
                recursive=True,
                file_loader_cls=UnstructuredFileIOLoader,
                file_loader_kwargs={"mode": "elements"},
                load_auth=True,
            ),
            name=self.app_name,  # App name (Mandatory)
            owner="Joe Smith",  # Owner (Optional)
            description="Identity enabled SafeLoader and SafeRetrival app using Pebblo",  # Description (Optional)
        )
```

#### SafeRetrieval

Here is the sample code for `Pebblo SafeRetriever` with `authorized_groups` from the user accessing RAG application passed in `auth_context`

```python
    auth = {
        "authorized_identities": [
            "joe@acme.io",
            "hr-group@acme.io",
            "us-employees-group@acme.io",
    ]}
    retriever = PebbloRetrievalQA.from_chain_type(
        llm=self.llm,
        chain_type="stuff",
        retriever=self.vectordb.as_retriever(),
        verbose=True,
        auth_context=auth,
    )
```

## LangChain

This solution requires the following two private LangChain packages:

* langchain
* langchain-community

### Installation

The above two packages with `GoogleDriveLoader` with authorized identities and `PebbloRetrievalQA` chain with identity enforcement can be installed using the following steps.

```
$ git clone -b pebblo_identity_saferetriever https://github.com/daxa-ai/langchain.git
$ cd langchain

# Install updated langchain-community package that has all document loaders,
# including GoogleDriveLoader with authorized-identities feature
$ (cd libs/community; pip install .)

# Install updated langchain package that has the new PebbloRetreivalQA chain
$ (cd libs/langchain; pip install .)
```


### Pull requests

Here are the two corresponding PRs in the LangChain for this feature:

1. community: add authorization identities to GoogleDriveLoader #18813
   https://github.com/langchain-ai/langchain/pull/18813
2. langchain: add PebbloRetrievalQA chain with Identity & Semantic enforcement #19991
   https://github.com/langchain-ai/langchain/pull/19991

## Note:
GoogleDriveLoader comes with some prerequisites. Please refer [this](https://python.langchain.com/docs/integrations/document_loaders/google_drive#prerequisites) section or follow below steps:

### Prerequisites for GoogleDriveLoader

1. Create a Google Cloud project or use an existing project
2. Enable the [Google Drive API](https://console.cloud.google.com/flows/enableapi?apiid=drive.googleapis.com)
3. Refer [Authorize credentials for desktop app](https://developers.google.com/drive/api/quickstart/python#authorize_credentials_for_a_desktop_application) or follow below section to download `credentials.json`.

    a. save `credentials.json` file using above step at `~/.credentials/credentials.json` path.

    b. put the absolute path of crdentials.json file in a `GOOGLE_APPLICATION_CREDENTIALS` environment variable.
    ```bash
    export GOOGLE_APPLICATION_CREDENTIALS="$HOME/.credentials/credentials.json"
    ```
4. Customize OAuth consent screen for your project: https://console.cloud.google.com/apis/credentials/consent


#### To Authorize credentials for a desktop application

To authenticate end users and access user data in your app, you need to create one or more OAuth 2.0 Client IDs. A client ID is used to identify a single app to Google's OAuth servers. If your app runs on multiple platforms, you must create a separate client ID for each platform.

 - In the Google Cloud console, go to Menu menu > APIs & Services > Credentials.
    [Go to Credentials](https://console.cloud.google.com/apis/credentials)
 - Click Create Credentials > OAuth client ID.
 - Click Application type > Desktop app.
 - In the Name field, type a name for the credential. This name is only shown in the Google Cloud console.
 - Click Create. The OAuth client created screen appears, showing your new Client ID and Client secret.
 - Click OK. The newly created credential appears under OAuth 2.0 Client IDs.
 - Save the downloaded JSON file as credentials.json, and move the file `~/.credentials/credentials.json` path.

### How to run?

#### Pre-requisite:
Download and save credentials.json for your GCP project at `~/.credentials/credentials.json`


#### Steps to run:
1. Setup virtual env and install `langchain/identity-rag/requirements.txt`.
```
pip install -r langchain/identity-rag/requirements.txt
```

2. Run the application

```
python3 langchain/identity-rag/pebblo_identity_rag.py
```

3. It will need following inputs:
   1. For the ingestion user:
      1. Admin email address : For listing groups to know the identity.
      2. service-account.json path : Service account credentials file for your google account with enough permissions.
      3. Folder Id : Folder id where the documents to be loaded are stored.
   2. End user email address, against which the identity would be matched.
   3. Prompt by the end user.

Based on all the inputs, it will load the data from given Google Drive folder and
based on the input prompt and it will respond according to
the user level permissions for that user.
