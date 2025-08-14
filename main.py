from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from monitoring.metrics import ( start_metrics_server )
from security.auth import AuthMiddleware
from utils.logging_config import setup_logging
from dotenv import load_dotenv
from routes.webhook import router as webhook_router
from routes.repos import router as repos_router
from routes.collections import router as collections_router
from routes.routes import router
import logging

load_dotenv()

setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    title="GitHub Multi-Agent",
    description="Automate code fix based on GitHub issue webhook",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(AuthMiddleware)

app.include_router(router)
app.include_router(webhook_router)
app.include_router(repos_router)
app.include_router(collections_router)

start_metrics_server(8001)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        log_config={
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                },
            },
            "handlers": {
                "default": {
                    "formatter": "default",
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stdout",
                },
            },
            "root": {
                "level": "INFO",
                "handlers": ["default"],
            },
        }
    )