-- QUERY 8: Daily Search Volume (last 90 days)
-- Save result as: compose-exports/08_search_daily.csv

SELECT
  DATE_TRUNC('day', ts_created)::date  AS day,
  COUNT(*)                             AS searches
FROM public.search_queries
WHERE ts_created >= NOW() - INTERVAL '90 days'
GROUP BY 1
ORDER BY 1;
