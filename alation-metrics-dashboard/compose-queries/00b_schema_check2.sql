-- QUERY 0b: Schema Check (remaining tables)
-- Just look at results on screen, no need to download

SELECT table_name, column_name, data_type
FROM information_schema.columns
WHERE table_schema = 'public'
  AND table_name IN ('users', 'visits', 'search_queries', 'rdbms_tables', 'terms')
ORDER BY table_name, ordinal_position;
