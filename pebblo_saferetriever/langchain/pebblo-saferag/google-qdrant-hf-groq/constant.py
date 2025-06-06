from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

LLM_NAME = "llama-3.3-70b-versatile"
LOADER_APP_NAME = "py_data_demo_loader"
RETRIEVAL_APP_NAME = "py_data_demo_retriever"
COLLECTION_NAME = "py_data_demo_collection"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
VECTOR_DB_URL = "http://localhost:6333"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SERVICE_ACCOUNT_PATH = ""
KEY_PATH = ""
INPUT_FOLDER_ID = ""
INGESTION_USER_EMAIL_ADDRESS = ""
TOKEN_PATH = ""
