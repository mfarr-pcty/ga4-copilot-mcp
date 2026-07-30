from fastapi import FastAPI
import os

app = FastAPI()

@app.get("/")
def home():
    return {
        "status": "running",
        "service": "ga4-mcp"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "project_id": os.getenv("GOOGLE_PROJECT_ID"),
        "credentials_present": bool(os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON"))
    }