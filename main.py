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
        "credentials_present": bool(
            os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
        )
    }


@app.get("/debug")
def debug():
    try:
        import subprocess

        result = subprocess.check_output(
            ["pip", "show", "google-analytics-mcp"],
            text=True
        )

        return {
            "installed": True,
            "details": result
        }

    except Exception as e:
        return {
            "installed": False,
            "error": str(e)
        }