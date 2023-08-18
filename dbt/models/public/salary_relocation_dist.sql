SELECT
    ua.relocation,
    AVG(jp.minimum_range) AS avg_salary
FROM {{ ref('stg_user_area') }} ua
JOIN {{ ref('stg_job_postings') }} jp 
ON ua.matched_object_id = jp.matched_object_id
GROUP BY ua.relocation