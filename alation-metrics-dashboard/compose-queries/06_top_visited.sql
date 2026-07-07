-- QUERY 6: Most-Viewed Catalog Objects (last 90 days)
-- Save result as: compose-exports/06_top_visited.csv

SELECT
  COALESCE(rt.name, art.title, t.title, 'Unknown')  AS object_name,
  v.object_type,
  COUNT(*)                                           AS views
FROM public.visits v
LEFT JOIN public.rdbms_tables rt  ON rt.id  = v.object_id
                                  AND rt.ts_deleted IS NULL
                                  AND v.object_type = 'table'
LEFT JOIN public.article      art ON art.id = v.object_id
                                  AND art.ts_deleted IS NULL
                                  AND v.object_type = 'article'
LEFT JOIN public.terms        t   ON t.id   = v.object_id
                                  AND t.ts_deleted IS NULL
                                  AND v.object_type = 'glossary_term'
WHERE v.ts_created  >= NOW() - INTERVAL '90 days'
  AND v.object_id   IS NOT NULL
  AND v.object_type IS NOT NULL
GROUP BY 1, 2
ORDER BY 3 DESC
LIMIT 20;
