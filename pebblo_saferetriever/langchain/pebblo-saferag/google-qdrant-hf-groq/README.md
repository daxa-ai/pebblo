# Pebblo Open Source SafeRAG Demo

A secure and semantic Retrieval-Augmented Generation (RAG) pipeline that combines multiple powerful components to provide a robust, privacy-focused document retrieval and question-answering system.

## Core Components

- **Document Source**: Google Drive integration for document ingestion
- **Security**: PebbloSafeLoader for semantic filtering and access control
- **Vector Store**: Qdrant for efficient document retrieval
- **Embeddings**: Local HuggingFace embeddings for semantic search
- **LLM**: Groq-powered Llama 3.3 for high-quality responses

## Prerequisites

1. Google Service Account with access to target Drive folder
2. Qdrant vector database instance
3. Required Python packages (see requirements.txt)
4. GROQ API key (set in .env file)

## Setup Instructions

### 1. Configure Environment

- Set up Google Drive authentication:
  - Follow the guide at: https://python.langchain.com/docs/integrations/document_loaders/google_drive/
  - Create a service account and download credentials
  - Share your target Google Drive folder with the service account email

- Configure API Keys:
  - Create a `.env` file in the project root
  - Add your GROQ API key: `GROQ_API_KEY=your_api_key_here`

- Update `constant.py` with your configuration:
  - Set `SERVICE_ACCOUNT_PATH` to your Google service account credentials
  - Set `INPUT_FOLDER_ID` to your Google Drive folder ID
  - Configure other settings as needed

### 2. Start Required Services

#### Qdrant Vector Database
```bash
docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant
```

#### Pebblo Server
```bash
pip install pebblo
pebblo --config-file config.yaml
```

### 3. Run the Application

```bash
python pebblo_opensource_saferag.py
```

## Features

- **Secure Document Ingestion**: Semantic filtering during document loading
- **Identity-Based Access Control**: User-level permissions and authentication
- **Content Filtering**: Topic and entity-based content filtering
- **Interactive Interface**: User-friendly query interface
- **Real-time Search**: Efficient semantic search and retrieval
- **Privacy-Focused**: Local embeddings and secure data handling

## Project Structure

```
pebblo_google_drive_opensource/
├── pebblo_opensource_saferag.py  # Main application file
├── constant.py                   # Configuration settings
├── utils.py                      # Utility functions
├── google_auth.py               # Google authentication utilities
├── .env                         # Environment variables
└── README.md                    # This file
```

## Security and Privacy

This implementation prioritizes security and privacy while maintaining high-quality retrieval and generation capabilities. Key security features include:

- Semantic filtering of sensitive content
- Identity-based access control
- Local embedding generation
- Secure API key management
- Privacy-preserving document processing

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
