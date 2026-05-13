SELECT
  results.product_name AS product_name,
  results.campaign_name AS campaign_name,
  results.iti_difference AS iti_difference,

  CASE
    WHEN creatives.preview_link IS NULL
    THEN 'no_link'
    ELSE creatives.preview_link
  END AS web_view_link,

  CAST(results.test_id AS STRING) AS test_id,

  CAST(
    results.first_impression_date AS STRING
  ) AS first_impression_date,

  results.test_type AS test_type,
  results.result AS result,
  results.network AS channel_name,
  results.creative_name AS creative_name,
  results.iti AS iti

FROM
  `PARAM-RESULTS-TABLE` AS results

LEFT JOIN
  `project.dataset.creative_dimension` AS creatives

ON
  CAST(
    REGEXP_EXTRACT(
      results.creative_id_value,
      r'asset_(.+)'
    ) AS INT64
  ) = creatives.creative_id

WHERE
  results.test_id = PARAM-TEST-BATCH-NUMBER

ORDER BY
  results.product_name ASC,
  results.iti_difference DESC
