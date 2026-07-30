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
    import importlib.util

    analytics_mcp_installed = (
        importlib.util.find_spec("analytics_mcp")
        is not None
    )

    return {
        "credentials_present": bool(
            os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
        ),
        "analytics_mcp_installed": analytics_mcp_installed
    }