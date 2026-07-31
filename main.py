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
        "project