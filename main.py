from fastapi import FastAPI
import os
import json

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
    return {"status": "running"}


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


@app.get("/package-files")
def package_files():
    import subprocess

    try:
        result = subprocess.check_output(
            ["pip", "show", "-f", "google-analytics-mcp"],
            text=True
        )

        return {"files": result}

    except Exception as e:
        return {"error": str(e)}