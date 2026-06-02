{{ config(materialized='view') }}

WITH source AS (

    SELECT *
    FROM {{ source('stg', 'customers') }}

)
,

renamed AS (

    SELECT
        customer_id AS customer_id,
        first_name AS first_name,
        last_name AS last_name,
        concat(first_name, ' ', last_name) AS full_name,
        email AS email,
        phone AS phone_number,
            date_of_birth AS date_of_birth,
            gender AS gender,
            address AS address,
            postal_code AS postal_code,
            city_id AS city_id,
            join_date AS join_date,
            loyalty_points AS loyalty_points,
            loyalty_tier AS loyalty_tier,
            is_loyalty_member AS is_loyalty_member,
            newsletter_opt_in AS newsletter_opt_in,
            preferred_branch_id AS preferred_branch_id

    FROM source

)
SELECT *
FROM renamed