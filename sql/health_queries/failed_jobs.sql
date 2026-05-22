-- ============================================
-- Failed SQL Jobs Monitoring
-- Autonomous AI DBA Operations Platform
-- ============================================

SELECT TOP 10

    name,

    enabled,

    date_created

FROM msdb.dbo.sysjobs

ORDER BY date_created DESC;