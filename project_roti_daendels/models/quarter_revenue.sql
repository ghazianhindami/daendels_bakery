
{{ config(materialized='table') }}


SELECT
    EXTRACT('year' FROM a.order_datetime) AS trans_year,
    EXTRACT('quarter' FROM a.order_datetime) AS trans_quarter,
    a.*,
    b.branch_name,
    b.city_name
FROM 
    orders a
LEFT JOIN (SELECT * FROM branches LEFT JOIN cities ON branches.city_id = cities.city_id ) b ON
    a.branch_id = b.branch_id
WHERE a.order_status = 'Voltooid'
ORDER BY 3 ASC