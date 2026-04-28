{{ config(materialized='table') }}

SELECT
    a.trans_year,
    a.trans_quarter,
    SUM(a.total_amount) revenue,
    a.city_name
FROM
    {{ ref('quarter_revenue') }} a
GROUP BY 1,2,4
ORDER BY 1,2,3 DESC