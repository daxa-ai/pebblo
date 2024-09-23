# Pebblo Text Loader

This is a sample application that demonstrates how to use the `Pebblo Text Loader` to load the text data
with the `Pebblo Safe Loader` into `Postgres` Vector Database.

\* This solution uses predefined text data and metadata from the utility functions to demonstrate the loading of
in-memory text data using Pebblo Safe Loader. Real-world applications can use this solution to load text data from
various sources.

**PebbloTextLoader**: PebbloTextLoader is a loader for text data. Since PebbloSafeLoader is a wrapper around document
loaders, this loader is used to load text data directly into Documents.

**This solution uses:**

- PostgreSQL 15.7
- langchain-community from daxa-ai/langchain branch(pebblo-0.1.19)

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

3. Install langchain-community from the branch `pebblo-0.1.19`

```console
$ git clone https://github.com/daxa-ai/langchain.git
$ cd langchain
$ git fetch && git checkout pebblo-0.1.19
$ cd libs/community
$ pip3 install langchain-community .
```

4. Copy the `.env.sample` file to `.env` and populate the necessary environment variable. The `.env` file should look
   like this:

```console
$ cat .env
# OpenAI credentials
OPENAI_API_KEY=<YOUR OPENAI API KEY>

# Postgres configuration
PG_CONNECTION_STRING = "postgresql://<USERNAME>:<PASSWORD>@<HOST>:<PORT>/<DATABASE-NAME>"
```

5. Run Pebblo Safe Loader sample app

```console
$ python3 pebblo_safeload.py
```

6. Retrieve the Pebblo PDF report in `$HOME/.pebblo/pebblo-safe-loader-text-loader/pebblo_report.pdf` file path on the
   system where `Pebblo Server` is running.
