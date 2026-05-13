import pytest
from collections import Counter

from modules.abtest import ABTest


campaign_name = "gamea_android_networka_video_cpi_test258"
channel_name = "network_a"
start_date = "2023-03-01"
end_date = "2023-03-21"


def test_get_schedule():
    abtest = ABTest(
        name=campaign_name,
        channel_name=channel_name,
        start_date=start_date,
        end_date=end_date
    )

    schedule = abtest.get_schedule()
    unique_creatives = sorted(
        schedule["creative_name"].unique().tolist()
    )

    assert unique_creatives == sorted([
        "asset_001_gamea_variant_a_video_1080x1920_en.mp4",
        "asset_002_gamea_variant_b_video_1080x1920_en.mp4",
        "asset_000_gamea_control_video_1080x1920_en.mp4"
    ])


def test_get_results():
    abtest = ABTest(
        name=campaign_name,
        channel_name=channel_name,
        start_date=start_date,
        end_date=end_date
    )

    schedule = abtest.get_schedule()
    performance = abtest.get_performance()
    results = abtest.get_results(schedule, performance)

    results_list = list(
        zip(
            results["creative_name"],
            results["result"]
        )
    )

    sorted_results_list = sorted(
        results_list,
        key=lambda item: item[0]
    )

    assert sorted_results_list == [
        (
            "asset_000_gamea_control_video_1080x1920_en.mp4",
            "Control network_a"
        ),
        (
            "asset_001_gamea_variant_a_video_1080x1920_en.mp4",
            "Non-Significant Winner"
        ),
        (
            "asset_002_gamea_variant_b_video_1080x1920_en.mp4",
            "Non-Significant Winner"
        )
    ]
