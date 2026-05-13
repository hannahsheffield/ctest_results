SELECT
    test_id,
    product_name,
    test_type,
    channel_name,
    country_code,
    start_date,
    end_date,
    campaign_name,

    TRIM(creative_name) AS creative_name,

    preview_link,
    is_control,

    test_metric,
    baseline_metric_value,

    minimum_effect_of_interest,
    statistical_confidence,
    statistical_power,
    sample_size

FROM
    `PARAM-SCHEDULE-TABLE`

WHERE
    test_id = PARAM-TEST-BATCH-NUMBER

    AND start_date BETWEEN
        "PARAM-START-DATE"
        AND "PARAM-END-DATE"
