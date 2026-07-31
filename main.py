from fastapi import FastAPI
import os

app = FastAPI()


@app.on_event("startup")
def startup_event():
    creds = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")

    if creds:
        with open("/tmp/service-account.json", "w") as f:
            f.write(creds)

        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = (
            "/tmp/service-account.json"
        )


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
        ),
        "google_credentials_file": os.getenv(
            "GOOGLE_APPLICATION_CREDENTIALS"
        )
    }


@app.get("/debug")
def debug():
    import subprocess

    try:
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