import pytest
from collections import Counter

from modules.campaign import Campaign


network_campaign_name = (
    "gamea_android_networka_video_cpi_test258"
)

network_channel_name = "network_a"

social_campaign_name = (
    "GAMEA_UKCA_01_ANDROID_TEST258_AA_BROAD_NETWORKC_CPI_20230308_MASTER"
)

social_channel_name = "network_c"

start_date = "2023-03-01"
end_date = "2023-03-21"


def test_network_campaign_get_performance():
    campaign = Campaign(
        name=network_campaign_name,
        channel_name=network_channel_name,
        start_date=start_date,
        end_date=end_date
    )

    performance = campaign.get_performance()

    unique_creatives = sorted(
        performance["creative_concept_name"]
        .unique()
        .tolist()
    )

    assert unique_creatives == sorted([
        "asset_001_gamea_variant_a",
        "asset_002_gamea_variant_b",
        "asset_000_gamea_control"
    ])


def test_social_campaign_get_performance():
    campaign = Campaign(
        name=social_campaign_name,
        channel_name=social_channel_name,
        start_date=start_date,
        end_date=end_date
    )

    performance = campaign.get_performance()

    unique_creatives = sorted(
        performance["creative_concept_name"]
        .unique()
        .tolist()
    )

    assert unique_creatives == sorted([
        "asset_101_gamea_variant_a",
        "asset_102_gamea_variant_b",
        "asset_103_gamea_variant_c",
        "asset_104_gamea_variant_d"
    ])
