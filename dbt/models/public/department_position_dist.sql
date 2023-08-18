SELECT
    department_name,
    position_title,
    AVG(minimum_range) AS average_salary,
    MIN(minimum_range) AS minimum_salary,
    MAX(maximum_range) AS maximum_salary
FROM {{ ref('stg_job_postings') }}
GROUP BY department_name, position_title