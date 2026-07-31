from fastapi import FastAPI
import os
import json
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
    return {
        "status": "running",
        "service": "ga4-mcp"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "project_id": os.getenv("GOOGLE_PROJECT_ID"),
        "ga4_property_id_present": bool(os.getenv("GA4_PROPERTY_ID")),
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


@app.get("/debug")
def debug():
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
    try:
        result = subprocess.check_output(
            ["pip", "show", "-f", "google-analytics-mcp"],
            text=True
        )

        return {
            "success": True,
            "files": result
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


@app.get("/server-help")
def server_help():
    try:
        result = subprocess.run(
            ["ga4-mcp-server", "--help"],
            capture_output=True,
            text=True,
            timeout=15
        )

        return {
            "success": True,
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }