"""Constantes do sistema"""

# GitHub
GITHUB_WEBHOOK_SECRET = "set-your-own"
READY_FOR_DEVELOPMENT_COLUMN = "Ready for Development"

# Ollama
OLLAMA_CODE_MODEL = "codellama:7b"
OLLAMA_TIMEOUT = 300  # 5 minutos

# Gemini
GEMINI_MODEL = "gemini-pro"
GEMINI_MAX_TOKENS = 2048

# Git
DEFAULT_BRANCH_PREFIX = "auto-update"
COMMIT_MESSAGE_TEMPLATE = "Auto-update: {change_type} in {file_path}"

# RAG
VECTOR_STORE_PATH = "./vector_store"
SIMILARITY_THRESHOLD = 0.7
MAX_SEARCH_RESULTS = 3