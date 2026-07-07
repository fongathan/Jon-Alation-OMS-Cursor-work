-- QUERY 5: Top Search Terms (last 90 days)
-- Save result as: compose-exports/05_top_searches.csv

SELECT
  name          AS query_text,
  COUNT(*)      AS search_count
FROM public.search_queries
WHERE ts_created  >= NOW() - INTERVAL '90 days'
  AND name IS NOT NULL
  AND name <> ''
  AND LENGTH(name) > 2
GROUP BY 1
ORDER BY 2 DESC
LIMIT 20;
