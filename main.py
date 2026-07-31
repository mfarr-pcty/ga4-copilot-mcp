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
        "ga4_property_id_present": bool(
            os.getenv("GA4_PROPERTY_ID")
        ),
        "credentials_present": bool(
            os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
        ),
        "google_credentials_file": os.getenv(
            "GOOGLE_APPLICATION_CREDENTIALS"
        )
    }


@app.get("/transport-test")
def transport_test():
    tests = [
        ["ga4-mcp-server", "--help"],
        ["ga4-mcp-server", "--transport", "streamable-http"],
        ["ga4-mcp-server", "--transport"],
        ["ga4-mcp-server", "--host"],
    ]

    results = []

    for cmd in tests:
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=10
            )

            results.append({
                "command": " ".join(cmd),
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr
            })

        except Exception as e:
            results.append({
                "command": " ".join(cmd),
                "error": str(e)
            })

    return {
        "results": results
    }

@app.get("/run-ga4")
def run_ga4():
    import subprocess

    try:
        result = subprocess.run(
            ["ga4-mcp-server"],
            capture_output=True,
            text=True,
            timeout=15,
            env={
                **os.environ,
                "GOOGLE_APPLICATION_CREDENTIALS":
                    "/tmp/service-account.json"
            }
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