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


@app.get("/credentials")
def credentials():
    try:
        with open("/tmp/service-account.json", "r") as f:
            creds = json.load(f)

        return {
            "success": True,
            "project_id": creds.get("project_id"),
            "client_email": creds.get("client_email")
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


@app.get("/ga-test")
def ga_test():
    try:
        from google.analytics.data_v1beta import BetaAnalyticsDataClient

        client = BetaAnalyticsDataClient()

        return {
            "success": True,
            "message": "Google Analytics client created successfully"
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }