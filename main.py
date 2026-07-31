from fastapi import FastAPI
from google.analytics.data_v1beta import (
    BetaAnalyticsDataClient,
    RunReportRequest,
    DateRange,
    Metric,
    Dimension
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
    
@app.get("/traffic")
def traffic():

    try:

        property_id = os.getenv(
            "GA4_PROPERTY_ID"
        )

        client = BetaAnalyticsDataClient()

        request = RunReportRequest(
            property=f"properties/{property_id}",

            date_ranges=[
                DateRange(
                    start_date="30daysAgo",
                    end_date="today"
                )
            ],

            dimensions=[
                Dimension(
                    name="sessionSource"
                ),
                Dimension(
                    name="sessionMedium"
                )
            ],

            metrics=[
                Metric(
                    name="sessions"
                ),
                Metric(
                    name="totalUsers"
                )
            ]
        )

        response = client.run_report(
            request
        )

        results = []

        for row in response.rows:

            results.append({

                "source":
                    row.dimension_values[0]
                    .value,

                "medium":
                    row.dimension_values[1]
                    .value,

                "sessions":
                    row.metric_values[0]
                    .value,

                "users":
                    row.metric_values[1]
                    .value

            })

        return {
            "success": True,
            "results": results
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }
    
@app.get("/landing-pages")
def landing_pages():

    try:

        property_id = os.getenv(
            "GA4_PROPERTY_ID"
        )

        client = BetaAnalyticsDataClient()

        request = RunReportRequest(
            property=f"properties/{property_id}",

            date_ranges=[
                DateRange(
                    start_date="30daysAgo",
                    end_date="today"
                )
            ],

            dimensions=[
                Dimension(
                    name="landingPagePlusQueryString"
                )
            ],

            metrics=[
                Metric(
                    name="sessions"
                ),
                Metric(
                    name="totalUsers"
                )
            ],

            limit=25
        )

        response = client.run_report(
            request
        )

        results = []

        for row in response.rows:

            results.append({

                "landing_page":
                    row.dimension_values[0]
                    .value,

                "sessions":
                    row.metric_values[0]
                    .value,

                "users":
                    row.metric_values[1]
                    .value

            })

        return {
            "success": True,
            "results": results
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }