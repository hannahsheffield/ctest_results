from google.cloud.bigquery import SchemaField
from google.cloud.bigquery.enums import SqlTypeNames


# =========================
# BigQuery Configuration
# =========================

BQ_BILLING_PROJECT_ID = "your-gcp-project-id"

LIVE_RESULTS_TABLE = (
    "your-production-project.analytics_dataset.ab_test_results"
)

LIVE_RESULTS_TABLE_DEV = (
    "your-dev-project.analytics_dataset.ab_test_results_dev"
)

EXPERIMENTAL_RESULTS_TABLE = (
    "your-dev-project.analytics_dataset.experimental_ab_test_results"
)


# =========================
# Output Columns
# =========================

LIVE_RESULTS_COLUMNS = [
    "campaign_name",
    "network",
    "test_id",
    "test_type",
    "product_name",
    "device_group",
    "countries",
    "target_demographic",
    "test_kpi",
    "creative_name",
    "metric_value",
    "creative_dimensions",
    "is_control",
    "first_impression_date",
    "total_impressions",
    "total_clicks",
    "total_installs",
    "total_cost",
    "day_2_returners",
    "ctr",
    "cti",
    "iti",
    "iti_difference",
    "cpi",
    "it2dr",
    "it2dr_difference",
    "result",
    "result_difference_lower_confidence_interval",
    "result_difference_upper_confidence_interval",
    "creative_preview_link",
    "video_plays",
    "video_plays_25",
    "video_plays_50",
    "video_plays_75",
    "video_plays_100"
]

EXPERIMENTAL_RESULTS_COLUMNS = [
    "campaign_name",
    "network",
    "test_id",
    "test_type",
    "product_name",
    "device_group",
    "countries",
    "target_demographic",
    "test_kpi",
    "creative_name",
    "metric_value",
    "creative_dimensions",
    "is_control",
    "first_impression_date",
    "total_impressions",
    "total_clicks",
    "total_installs",
    "total_cost",
    "day_2_returners",
    "ctr",
    "cti",
    "iti",
    "iti_difference",
    "cpi",
    "it2dr",
    "it2dr_difference",
    "result",
    "result_difference_lower_confidence_interval",
    "result_difference_upper_confidence_interval"
]


# =========================
# Dashboard Formatting
# =========================

NETWORK_BACKGROUND_COLORS = {
    "network_a": "#cfe2f3",
    "network_b": "#d9d2e9",
    "network_c": "#d9d2e9",
}

RESULT_COLOR_CODES = {
    "Significant Winner": "#35a152",
    "Significant Loser": "#ff1919",
    "Non-Significant Winner": "#a4edb7",
    "Non-Significant Loser": "#f77c7c",
}


# =========================
# Statistical Configuration
# =========================

STATISTICAL_CONFIDENCE_BY_CHANNEL = {
    "network_a": 0.7,
    "network_b": 0.9,
    "network_c": 0.9
}

STATISTICAL_CONFIDENCE_PARAMS = {
    "0.9": 1.645,
    "0.7": 1.035
}
