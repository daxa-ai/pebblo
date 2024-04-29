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
3. Run your [Pebblo server](https://github.com/daxa-ai/pebblo/tree/main?tab=readme-ov-file#pebblo-server). Export PEBBLO_CLASSIFIER_URL in os env.
```console
$ export PEBBLO_CLASSIFIER_URL="http://localhost:8000/"
```

3. Run python script

```console
python3 llama_pebblo_multilreaders.py --reader_type <PDFReader/CSVReader/DocxReader/SimpleDirectoryReader> --input <input_file/directory_path>
```

4. Script will print the URl for report. Please open the URL in browser. 
> Note: Pebblo process the data asynchronously. Report generation might take some based on data size. Please keep refreshing the page to get the report.