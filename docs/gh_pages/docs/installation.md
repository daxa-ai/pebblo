# Installation

> **Note**  
> Please note that Pebblo requires Python version 3.9 or above to function optimally.

## Using `pip`

```bash
pip install pebblo --extra-index-url https://packages.daxa.ai/simple/
```

### Run Pebblo server

```
$ pebblo
```

Pebblo server now listens to `localhost:8000` to accept Gen-AI application data snippets for inspection and reporting.
Pebblo UI interface would be available on `http://localhost:8000/pebblo`

See [troubleshooting](troubleshooting.md) for any issues.

#### Configuration flags (Optional)

- `--config <file>`: Specifies a custom configuration file in yaml format.

```bash
pebblo [--config /path/to/config.yaml]
```


## Using Docker 

```bash
docker run -p 8000:8000 docker.daxa.ai/daxaai/pebblo
```

Local UI can be accessed by pointing the browser to `https://localhost:8000`.

To pass a specific configuration file and to access PDF reports iin the host machine outside the docker container, use the following command with mounted volumes for config.yaml and the report folder.

```bash
docker run \
    -v /path/to/pebblo/config.yaml:/opt/pebblo/config/config.yaml \
    -v /path/to/pebblo_cached:/opt/.pebblo \
    -p 8000:8000 docker.daxa.ai/daxaai/pebblo:latest \
        --config /opt/pebblo/config/config.yaml
```

## Using Kubernetes
Apply below k8s manifiest files in sequence to run the pebblo server on k8s cluster. 
```bash
kubectl apply -f deploy/k8s-deploy/config.yaml

kubectl apply -f deploy/k8s-deploy/pvc.yaml

kubectl apply -f deploy/k8s-deploy/deploy.yaml

kubectl apply -f deploy/k8s-deploy/service.yaml
```
Use `kubectl logs <pod_name>` to get the logs from pebblo server. 

**Note-** Setup the nginx ingress controller to expose the pebblo server.

# Enhanced PDF reporting

Pebblo supports two PDF rendering options:

1. `xhtml2pdf` (default)
1. `weasyprint`

This is selected using `renderer` setting in the config.yaml

`weasyprint` produces an enhanced visual look and feel. This renderer option requires the following additional prerequisites. This is needed for PDF report generation,

### Install weasyprint library

```sh
pip install weasyprint
```

### Install Pango library

#### Mac OSX

```
brew install pango
```

#### Linux (debian/ubuntu)

```
sudo apt-get install libpango-1.0-0 libpangoft2-1.0-0
```

