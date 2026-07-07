-- QUERY 0: Schema Check — run this first to see actual column names
-- No need to save as CSV, just look at the results

SELECT table_name, column_name, data_type
FROM information_schema.columns
WHERE table_schema = 'public'
  AND table_name IN ('users', 'visits', 'flags', 'search_queries',
                     'rdbms_tables', 'article', 'terms', 'search_clicks',
                     'rdbms_datasources')
ORDER BY table_name, ordinal_position;
