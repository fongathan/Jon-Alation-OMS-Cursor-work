-- QUERY 2: Top Users by Curation Activity (last 90 days)
-- Save result as: compose-exports/02_top_users.csv

SELECT
  u.display_name,
  u.user_email                                                               AS email,
  COUNT(CASE WHEN f.flag_type = 'ENDORSEMENT' THEN 1 END)                   AS endorsements,
  COUNT(CASE WHEN f.flag_type = 'DEPRECATION' THEN 1 END)                   AS deprecations,
  COUNT(CASE WHEN f.flag_type = 'WARNING'     THEN 1 END)                   AS warnings,
  COUNT(*)                                                                   AS total_flags
FROM public.flags f
JOIN public.users u ON u.user_id = f.user_id
WHERE f.ts_created >= NOW() - INTERVAL '90 days'
  AND f.ts_deleted  IS NULL
  AND u.is_active    = true
GROUP BY u.user_id, u.display_name, u.user_email
ORDER BY total_flags DESC
LIMIT 20;
