-- QUERY 1: Summary KPIs
-- Save result as: compose-exports/01_summary.csv

SELECT
  (SELECT COUNT(DISTINCT user_id)
   FROM public.visits
   WHERE ts_created >= NOW() - INTERVAL '30 days')                           AS mau,

  (SELECT COUNT(DISTINCT user_id)
   FROM public.visits
   WHERE ts_created >= NOW() - INTERVAL '90 days')                           AS users_90d,

  (SELECT COUNT(*)
   FROM public.search_queries
   WHERE ts_created >= NOW() - INTERVAL '90 days')                           AS searches_90d,

  (SELECT COUNT(*)
   FROM public.visits
   WHERE ts_created >= NOW() - INTERVAL '90 days')                           AS page_views_90d,

  (SELECT ROUND(COUNT(*)::numeric / NULLIF(COUNT(DISTINCT DATE_TRUNC('day', ts_created)), 0), 0)::int
   FROM public.visits
   WHERE ts_created >= NOW() - INTERVAL '90 days')                           AS avg_daily_views,

  (SELECT COUNT(*)
   FROM public.users
   WHERE date_joined >= NOW() - INTERVAL '90 days'
     AND is_active = true)                                                    AS new_users_90d,

  (SELECT COUNT(*)
   FROM public.flags
   WHERE flag_type  = 'DEPRECATION'
     AND ts_deleted IS NULL
     AND ts_created >= NOW() - INTERVAL '90 days')                           AS deprecations_90d,

  (SELECT COUNT(*) FROM public.article WHERE ts_deleted IS NULL)             AS articles_total,
  (SELECT COUNT(*) FROM public.terms   WHERE ts_deleted IS NULL)             AS terms_total,
  (SELECT COUNT(*) FROM public.rdbms_tables WHERE ts_deleted IS NULL)        AS tables_total,

  (SELECT COUNT(*)
   FROM public.rdbms_tables
   WHERE ts_deleted IS NULL
     AND description IS NOT NULL AND description <> '')                      AS tables_described,

  (SELECT COUNT(*)
   FROM public.rdbms_tables
   WHERE ts_deleted IS NULL
     AND cardinality(steward) > 0)                                           AS tables_stewarded,

  (SELECT COUNT(DISTINCT object_id)
   FROM public.flags
   WHERE flag_type = 'ENDORSEMENT' AND ts_deleted IS NULL)                   AS tables_endorsed;
