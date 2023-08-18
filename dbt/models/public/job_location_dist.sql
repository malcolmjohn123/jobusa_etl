SELECT
    position_location_display,
    COUNT(*) AS num_postings
FROM {{ ref('stg_job_postings') }}
GROUP BY position_location_display