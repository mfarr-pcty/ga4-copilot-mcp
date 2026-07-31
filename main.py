from fastapi import FastAPI
import os
import subprocess

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
        "credentials_present": bool(
            os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
        )
    }


@app.get("/mcp-version")
def mcp_version():
    try:
        result = subprocess.check_output(
            ["pip", "show", "mcp"],
            text=True
        )

        return {
            "success": True,
            "details": result
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }