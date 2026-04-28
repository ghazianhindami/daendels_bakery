{{ config(materialized='table') }}

WITH prev_year AS (

SELECT
	*,
	LAG(revenue) OVER(
	PARTITION BY city_name,trans_quarter
	ORDER BY trans_year)prev_quarter
FROM {{ ref('quarter_revenue2') }} )

SELECT
	*,
	(revenue-prev_quarter)/prev_quarter AS yoy_growth
FROM 
    prev_year