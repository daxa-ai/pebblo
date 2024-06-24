## PebbloSafeLoader sample app with Identity and Semantic metadata

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

3. Copy the `.env.sample` file to `.env` and populate the necessary environment variable.

> Note: You need to set `PEBBLO_CLASSIFIER_URL` only if your `Pebblo Server` is running somewhere other than the default URL
> of `http://localhost:8000`.

4. Update the `pebblo_safeload.py` file with the following details:

- _folder_id_: Google Drive folder ID where the documents are stored


5. Run PebbloSafeLoader sample app

```console
$ python3 pebblo_safeload.py
```

6. Retrieve the Pebblo PDF report in `$HOME/.pebblo/pebblo-identity-sematic-loader-pinecone/pebblo_report.pdf` file path on the system
   where `Pebblo Server` is running.

7. To access the Pebblo UI, point the browser to `https://localhost:8000/pebblo`  or `host:port/pebblo` if you are running the server on a different
   host.