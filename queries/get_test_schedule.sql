SELECT
    ctest_number,
    title_reporting_name,
    test_type,
    channel_name,
    attribution_country_code,
    start_date,
    end_date,
    campaign_name,
    TRIM(creative_name) AS creative_name,
    web_view_link,
    is_control,
    test_metric,
    test_metric_baseline_value,
    minimum_effect_interest,
    stat_confidence,
    stat_power,
    sample_size

FROM
    `PARAM-SCHEDULE-TABLE`
WHERE
    start_date BETWEEN "PARAM-START-DATE" AND "PARAM-END-DATE"
    AND campaign_name = "PARAM-CAMPAIGN-NAME"
    AND channel_name = "PARAM-CHANNEL-NAME"
