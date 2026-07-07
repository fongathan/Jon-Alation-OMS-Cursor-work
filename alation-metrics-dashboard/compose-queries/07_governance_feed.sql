-- QUERY 7: Recent Governance Activity Feed
-- Save result as: compose-exports/07_governance_feed.csv

SELECT
  f.flag_type,
  f.user_name                                         AS curator,
  COALESCE(rt.name, 'Unknown object')                 AS object_name,
  COALESCE(ds.name, '')                               AS datasource,
  TO_CHAR(f.ts_created, 'YYYY-MM-DD')                 AS event_date
FROM public.flags f
LEFT JOIN public.rdbms_tables      rt ON rt.id = f.object_id
                                      AND rt.ts_deleted IS NULL
LEFT JOIN public.rdbms_datasources ds ON ds.id = rt.ds_id
                                      AND ds.ts_deleted IS NULL
WHERE f.ts_deleted IS NULL
ORDER BY f.ts_created DESC
LIMIT 20;
