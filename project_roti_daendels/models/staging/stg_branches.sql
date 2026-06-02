{{ config(materialized='view') }}

WITH source AS (

    SELECT *
    FROM {{ source('stg', 'branches') }}

),

renamed AS (

    SELECT
        branch_id AS branch_id,
        branch_name AS branch_name,
        address AS branch_address,
        city_id AS city_id,
        postal_code AS postal_code_branch,
        email AS email_branch,
        phone AS phone_branch,
        opened_date AS opened_date_branch,
        size_category AS size_category_branch,
        seating_capacity AS seating_capacity_branch,
        is_active AS is_active_branch,
        latitude AS latitude_branch,
        longitude AS longitude_branch
    FROM source

)
SELECT *
FROM renamed