-- QUERY 3: Monthly Curation Trend (last 12 months)
-- Save result as: compose-exports/03_curation_monthly.csv

SELECT
  TO_CHAR(DATE_TRUNC('month', ts_created), 'Mon ''YY')  AS month,
  DATE_TRUNC('month', ts_created)::date                  AS month_date,
  COUNT(CASE WHEN flag_type = 'ENDORSEMENT' THEN 1 END)  AS endorsed,
  COUNT(CASE WHEN flag_type = 'DEPRECATION' THEN 1 END)  AS deprecated,
  COUNT(CASE WHEN flag_type = 'WARNING'     THEN 1 END)  AS warned
FROM public.flags
WHERE ts_created >= NOW() - INTERVAL '12 months'
  AND ts_deleted  IS NULL
GROUP BY 1, 2
ORDER BY 2;
