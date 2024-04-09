
## Identity Enforcement using Pebblo

This solution uses the following two proposed PRs to LangChain:

1. community: add authorization identities to GoogleDriveLoader #18813
   https://github.com/langchain-ai/langchain/pull/18813

2. langchain: add PebbloRetrievalQA chain with Identity & Semantic enforcement #19991
   https://github.com/langchain-ai/langchain/pull/19991

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

> Note: requirements.txt includes the necessary `pebblo-langchain` package

3. Populate your `OPENAI_API_KEY` and, if needed, `PEBBLO_CLASSIFIER_URL` in .env file.

```console
$ cat .env
OPENAI_API_KEY=""
PEBBLO_CLASSIFIER_URL="http://localhost:8000/"
```
> Note: You need to set `PEBBLO_CLASSIFIER_URL` only if your `Pebblo Server` is running somewhere other than the default URL of `http://localhost:8000`.

4. Run langchain sample app Pebblo SafeLoader and Pebblo SafeRetriever

```console
$ python3 pebblo_identity_rag.py
```

5. Retrieve the Pebblo PDF report in `$HOME/.pebblo/pebblo-identity-rag-1/pebblo_report.pdf` file path on the system where `Pebblo Server` is running.
