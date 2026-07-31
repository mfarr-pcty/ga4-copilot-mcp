from fastapi import FastAPI
import subprocess

app = FastAPI()


@app.get("/")
def home():
    return {"status": "running"}


@app.get("/entry-points")
def entry_points():
    try:
        result = subprocess.check_output(
            [
                "cat",
                "/opt/render/project/src/.venv/lib/python3.14/site-packages/google_analytics_mcp-2.8.4.dist-info/entry_points.txt"
            ],
            text=True
        )

        return {
            "success": True,
            "entry_points": result
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }