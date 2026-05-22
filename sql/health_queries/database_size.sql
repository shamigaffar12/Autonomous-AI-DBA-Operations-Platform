-- ============================================
-- Database Size Monitoring
-- Autonomous AI DBA Operations Platform
-- ============================================

SELECT

    DB_NAME(database_id) AS database_name,

    CAST(SUM(size) * 8 / 1024 AS DECIMAL(10,2))
    AS size_mb

FROM sys.master_files

GROUP BY database_id

ORDER BY size_mb DESC;