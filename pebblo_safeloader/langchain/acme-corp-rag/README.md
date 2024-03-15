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
> Note: You need to set `PEBBLO_CLASSIFIER_URL` only if your `Pebblo Daemon` is running somewhere other than the default URL of `http://localhost:8000`.

4. Run langchain sample app _without_ Pebblo Safe DataLoader and make sure it successfully produces a valid response.

```console
$ python3 acme_corp_rag.py
```

5. Run langchain sample app _with_ Pebblo Safe DataLoader

```console
$ python3 acme_corp_rag_pebblo.py
```

6. Retrieve the Pebblo PDF report in `$HOME/.pebblo/acme_corp_rag/pebblo_report.pdf` file path on the system where `Pebblo Daemon` is running.