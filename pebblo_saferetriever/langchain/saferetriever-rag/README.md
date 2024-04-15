## Semantic Enforcement using Pebblo

This solution uses the following two proposed PRs:

1. Add semantic info to metadata, classified by pebblo-server
   https://github.com/daxa-ai/langchain/pull/16
2. daxa-langchain: Introduce SafeRetriever for Identity and Semantic enforcement
   https://github.com/daxa-ai/langchain/pull/28

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

> Note: You need to set `PEBBLO_CLASSIFIER_URL` only if your `Pebblo Server` is running somewhere other than the default URL
> of `http://localhost:8000`.

4. Run langchain sample app PebbloSafeLoader and SafeRetriever

```console
$ python3 saferetriever_semantic_rag.py
```

5. Retrieve the Pebblo PDF report in `$HOME/.pebblo/pebblo-sematic-rag/pebblo_report.pdf` file path on the system where `Pebblo Server` is running.
