## Pebblo Safe Retriever

This solution uses:

- PostgreSQL 15.7
- langchain-community from daxa-ai/langchain branch(https://github.com/daxa-ai/langchain/tree/daxa_3.1)

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

3. Install langchain-community from the branch `daxa_3.1`

```console  
$ git clone https://github.com/daxa-ai/langchain.git
$ cd langchain
$ git fetch && git checkout daxa_3.1
$ cd libs/community
$ pip3 install langchain-community .
```

4. Copy the `.env.sample` file to `.env` and populate the necessary environment variable.

```console
$ cat .env
OPENAI_API_KEY=""
PEBBLO_CLASSIFIER_URL="http://localhost:8000/"
```

> Note: You need to set `PEBBLO_CLASSIFIER_URL` only if your `Pebblo Server` is running somewhere other than the default URL
> of `http://localhost:8000`.

4. Run Pebblo Safe Rag sample app

```console
$ python3 pebblo_saferag.py
```

5. Retrieve the Pebblo PDF report in `$HOME/.pebblo/pebblo-identity-loader/pebblo_report.pdf` file path on the system where `Pebblo Server`
   is running.
