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
    import pkg_resources

    packages = [p.key for p in pkg_resources.working_set]

    return {
        "credentials_present": bool(
            os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
        ),
        "google_analytics_mcp_installed":
            "google-analytics-mcp" in packages,
        "analytics_packages": [
            p for p in packages
            if "analytics" in p.lower()
        ]
    }