from pydantic import BaseModel
from typing import List, Optional

from fastapi import FastAPI
from google.analytics.data_v1beta import (
    BetaAnalyticsDataClient,
    RunReportRequest,
    DateRange,
    Metric,
    Dimension
)
from google.analytics.data_v1beta.types import (
    Filter,
    FilterExpression
)
import os

app = FastAPI(
    servers=[
        {
            "url": "https://ga4-copilot-mcp.onrender.com"
        }
    ]
)

class ReportRequest(BaseModel):
    dimensions: List[str] = []
    metrics: List[str]

    start_date: str = "30daysAgo"
    end_date: str = "today"

    limit: int = 25

    filter_field: Optional[str] = None
    filter_value: Optional[str] = None


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
    
@app.get("/conversions")
def conversions():

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
                    name="eventName"
                )
            ],

            metrics=[
                Metric(
                    name="eventCount"
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

                "event_name":
                    row.dimension_values[0]
                    .value,

                "event_count":
                    row.metric_values[0]
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

@app.get("/organic-landing-pages")
def organic_landing_pages():

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

            dimension_filter={
                "filter": {
                    "field_name": "sessionMedium",
                    "string_filter": {
                        "value": "organic"
                    }
                }
            },

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


"""
@app.post("/report")
def report(request: ReportRequest):

    try:

        if not request.metrics:
            return {
                "success": False,
                "error": "At least one metric is required."
            }

        property_id = os.getenv(
            "GA4_PROPERTY_ID"
        )

        client = BetaAnalyticsDataClient()

        report_request = RunReportRequest(
            property=f"properties/{property_id}",

            date_ranges=[
                DateRange(
                    start_date=request.start_date,
                    end_date=request.end_date
                )
            ],

            dimensions=[
                Dimension(name=d)
                for d in request.dimensions
            ],

            metrics=[
                Metric(name=m)
                for m in request.metrics
            ],

            limit=request.limit
        )

        # Apply optional filter
        if request.filter_field and request.filter_value:

            report_request.dimension_filter = (
                FilterExpression(
                    filter=Filter(
                        field_name=request.filter_field,

                        string_filter=Filter.StringFilter(
                            value=request.filter_value
                        )
                    )
                )
            )

        response = client.run_report(
            report_request
        )

        response = client.run_report(
            report_request
        )

        results = []

        for row in response.rows:

            result = {}

            for i, dimension in enumerate(
                request.dimensions
            ):
                result[dimension] = (
                    row.dimension_values[i].value
                )

            for i, metric in enumerate(
                request.metrics
            ):
                result[metric] = (
                    row.metric_values[i].value
                )

            results.append(result)

        return {
            "success": True,
            "results": results
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }
    """