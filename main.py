from fastapi import FastAPI
from google.analytics.data_v1beta import (
    BetaAnalyticsDataClient,
    RunReportRequest,
    DateRange,
    Metric
)
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
        "service": "ga4-api",
        "status": "running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "project_id": os.getenv("GOOGLE_PROJECT_ID"),
        "ga4_property_id": os.getenv("GA4_PROPERTY_ID")
    }


@app.get("/summary")
def summary():
    try:

        property_id = os.getenv("GA4_PROPERTY_ID")

        client = BetaAnalyticsDataClient()

        request = RunReportRequest(
            property=f"properties/{property_id}",
            date_ranges=[
                DateRange(
                    start_date="30daysAgo",
                    end_date="today"
                )
            ],
            metrics=[
                Metric(name="sessions"),
                Metric(name="totalUsers"),
                Metric(name="screenPageViews")
            ]
        )

        response = client.run_report(request)

        return {
            "success": True,
            "sessions":
                response.rows[0].metric_values[0].value,
            "users":
                response.rows[0].metric_values[1].value,
            "pageviews":
                response.rows[0].metric_values[2].value
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }