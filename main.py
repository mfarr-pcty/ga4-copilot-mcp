@app.get("/mcp-files")
def mcp_files():
    import subprocess

    try:
        result = subprocess.check_output(
            ["pip", "show", "-f", "mcp"],
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