{{ config(materialized='table') }}

with final AS (
    SELECT * FROM {{ ref('fct_rfm_scored_1y') }}
    UNION ALL
    SELECT * FROM {{ ref('fct_rfm_scored_6m') }}
    UNION ALL
    SELECT * FROM {{ ref('fct_rfm_scored_3m') }}
    UNION ALL
    SELECT * FROM {{ ref('fct_rfm_scored_1m') }}
    UNION ALL
    SELECT * FROM {{ ref('fct_rfm_scored_1w') }}
    UNION ALL
    SELECT * FROM {{ ref('fct_rfm_scored_all') }}
)

SELECT
  customer_id,
  period,
  recency,
  frequency,
  ROUND(monetary::numeric, 2)       AS monetary,
  r_score,
  f_score,
  m_score,
  CONCAT(r_score, f_score, m_score) AS rfm_segment,
  (r_score + f_score + m_score)     AS rfm_total,
  CASE
    WHEN r_score >= 4 AND f_score >= 4 AND m_score >= 4 THEN 'Champions'
    WHEN r_score >= 3 AND f_score >= 3                  THEN 'Loyal Customers'
    WHEN r_score >= 4 AND f_score <= 2                  THEN 'New Customers'
    WHEN r_score >= 3 AND f_score <= 3 AND m_score >= 3 THEN 'Potential Loyalists'
    WHEN r_score <= 2 AND f_score >= 3 AND m_score >= 3 THEN 'At Risk'
    WHEN r_score <= 2 AND f_score >= 4 AND m_score >= 4 THEN 'Cant Lose Them'
    WHEN r_score <= 2 AND f_score <= 2                  THEN 'Lost / Hibernating'
    ELSE                                                     'Need Attention'
  END AS customer_segment
FROM final
ORDER BY period, rfm_total DESC
