WITH
standard_campaign_performance AS (

    SELECT
        f_creative.device_class AS device_group,
        f_creative.network AS network,
        d_product.product_short_name AS product_name,

        CASE
            WHEN f_creative.creative_id IS NULL
            THEN f_creative.creative_name_raw
            ELSE REGEXP_EXTRACT(
                d_creative.creative_name,
                '^[^_]*_([^_]*_[^_]*_[^_]*_[^_]*)'
            )
        END AS creative_concept_name,

        CONCAT("asset_", d_creative.creative_id) AS creative_id_value,

        f_creative.campaign_name AS campaign_name,
        d_creative.preview_link AS creative_link,
        d_creative.resolution AS creative_dimensions,

        CASE
            WHEN f_creative.creative_id IS NULL
            THEN f_creative.creative_name_raw
            ELSE d_creative.creative_name
        END AS creative_name,

        COALESCE(
            SUM(f_creative.num_impression),
            0
        ) AS total_impressions,

        COALESCE(
            SUM(f_creative.num_first_install),
            0
        )
        + COALESCE(SUM(f_creative.num_reinstall), 0)
        + COALESCE(SUM(f_creative.num_reopen), 0)
            AS total_installs,

        COALESCE(
            SUM(f_creative.cost_usd),
            0
        ) AS total_cost,

        COALESCE(
            SUM(f_creative.num_click),
            0
        ) AS total_clicks,

        DATE(
            MIN(
                CASE
                    WHEN f_creative.num_impression > 0
                    THEN CAST(f_creative.activity_date AS TIMESTAMP)
                    ELSE NULL
                END
            )
        ) AS first_impression_date,

        COALESCE(
            SUM(
                CASE
                    WHEN DATE_DIFF(
                        f_creative.activity_date,
                        f_creative.install_date,
                        DAY
                    ) = 1
                    THEN f_creative.num_returner
                    ELSE 0
                END
            ),
            0
        ) AS day_2_returners,

        COALESCE(
            SUM(
                CASE
                    WHEN DATE_DIFF(
                        f_creative.activity_date,
                        f_creative.install_date,
                        DAY
                    ) = 1
                    THEN f_creative.num_returner
                    ELSE 0
                END
            ),
            0
        )
        /
        NULLIF(
            COALESCE(
                SUM(
                    CASE
                        WHEN DATE_DIFF(
                            DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY),
                            f_creative.install_date,
                            DAY
                        ) >= 1
                        THEN (
                            COALESCE(f_creative.num_first_install, 0)
                            + COALESCE(f_creative.num_reinstall, 0)
                            + COALESCE(f_creative.num_reopen, 0)
                        )
                    END
                ),
                0
            ),
            0
        ) AS day_2_retention

    FROM
        `project.dataset.standard_creative_performance_daily` AS f_creative

        LEFT JOIN
            `project.dataset.product_dimension` AS d_product
            USING (product_id)

        LEFT JOIN
            `project.dataset.creative_dimension` AS d_creative
            USING (creative_id)

    WHERE
        f_creative.install_date BETWEEN
            "PARAM-START-DATE"
            AND "PARAM-END-DATE"

        AND f_creative.acquisition_category = "Paid"
        AND f_creative.network IN ("network_a", "network_b")
        AND f_creative.campaign_name = "PARAM-CAMPAIGN-NAME"
        AND f_creative.campaign_acquisition_type = "User Acquisition"
        AND f_creative.device_class = "Android"

    GROUP BY
        1,2,3,4,5,6,7,8,9

    HAVING
        creative_name <> "Missing Creative Data"
        AND creative_name <> "Creative Alignment"
        AND total_cost > 0
)

SELECT
    device_group,
    network,
    product_name,
    creative_concept_name,
    creative_id_value,
    campaign_name,
    creative_link,
    creative_dimensions,
    TRIM(creative_name) AS creative_name,
    total_impressions,
    total_installs,
    total_cost,
    total_clicks,
    first_impression_date,
    day_2_returners,
    day_2_retention

FROM
    standard_campaign_performance;
