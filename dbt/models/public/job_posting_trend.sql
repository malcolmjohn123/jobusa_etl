SELECT
    extract('year' from publication_start_date) AS posting_year,
    extract('month' from publication_start_date) AS posting_month,
    COUNT(*) AS num_postings
FROM {{ ref('stg_job_postings') }}
GROUP BY posting_year,posting_month
ORDER BY posting_year,posting_month