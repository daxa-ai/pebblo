# Using Pebblo Report

## Installation
To use Pebblo Report, you need to install Pebblo and configure a classifier. You can use either the vLLM-based Pebblo Classifier v3 or AWS Bedrock.

### Step 1: Install Pebblo
```bash
pip install pebblo
```

### Step 2: Setup Model Server

#### Setting Model Server with vLLM

To use vLLM-based Pebblo Classifier v3, start the vLLM server with the following command:
```bash
docker run --runtime nvidia --gpus all \
    -v ~/.cache/huggingface:/root/.cache/huggingface \
    --env "HUGGING_FACE_HUB_TOKEN=<secret>" \
    -p 8000:8000 \
    --ipc=host \
    vllm/vllm-openai:latest \
    --model daxa-ai/pebblo_classifier_v3 \
    --max-model-len=3000 \
    --gpu_memory_utilization=0.95
```

#### Set Environment Variables for vLLM
```bash
export MODEL_NAME=daxa-ai/pebblo_classifier_v3
export HOSTED_VLLM_API_KEY=vllm-placeholder-key
export BACKEND=vllm
export API_BASE_URL=<http://llm_server:8000/v1>
```

#### Use AWS Bedrock as Model Server

If using AWS Bedrock, ensure the service is accessible and configured properly.

#### Set Environment Variables for Bedrock
```bash
export AWS_ACCESS_KEY_ID=<AWS_ACCESS_KEY_ID>
export AWS_SECRET_ACCESS_KEY=<AWS_SECRET_ACCESS_KEY>
export AWS_DEFAULT_REGION=<region>
export MODEL_NAME=<model_name>
export BACKEND=bedrock
```

#### Alternate Setup: Using Docker Compose
Alternatively, you can clone the repository and use Docker Compose to start both the Pebblo server and the model server. You can set environment variables as described above to either use bedrock or vllm.
```bash
git clone https://github.com/daxa-ai/pebblo.git
cd pebblo/deploy/docker
docker-compose up --build -d
```

### Step 3: Start Pebblo Server
If you are not using docker compose, start the Pebblo server manually:
```bash
pebblo
```

### Step 4. Installing Pebblo Reporter
Once Pebblo and the classifier are set up, install the Pebblo Reporter package:
```bash
pip install pebblo-reporter
```

### Step 5. Running Pebblo Report
To generate a report, use the following command:
```bash
pebblo-report -o <pdf/json> -f <file-path> -u http://<pebblo-server-url>/tools/document_report
```
### Example:
```bash
pebblo-report -o pdf -f /path/to/file.pdf -u http://pebblo-server:9000/tools/document_report
```

This command generates a report in the specified format (PDF or JSON) using the given file and uploads it to the provided document report URL.