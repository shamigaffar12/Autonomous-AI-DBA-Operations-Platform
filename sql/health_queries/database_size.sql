-- ============================================
-- Database Size Monitoring
-- Autonomous AI DBA Operations Platform
-- ============================================

SELECT

    DB_NAME() AS database_name,

    CAST(
        SUM(size) * 8.0 / 1024
        AS DECIMAL(10,2)
    ) AS size_mb

FROM sys.database_files;