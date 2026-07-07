-- QUERY 4: Monthly MAU and Average Daily Views (last 12 months)
-- Save result as: compose-exports/04_dau_mau_monthly.csv

SELECT
  TO_CHAR(DATE_TRUNC('month', ts_created), 'Mon ''YY')  AS month,
  DATE_TRUNC('month', ts_created)::date                  AS month_date,
  COUNT(DISTINCT user_id)                                AS mau,
  ROUND(COUNT(*)::numeric
    / NULLIF(COUNT(DISTINCT DATE_TRUNC('day', ts_created)), 0), 0)           AS avg_daily_views
FROM public.visits
WHERE ts_created >= NOW() - INTERVAL '12 months'
  AND user_id IS NOT NULL
GROUP BY 1, 2
ORDER BY 2;
