-- ============================================
-- Long Running Query Monitoring
-- Autonomous AI DBA Operations Platform
-- ============================================

SELECT TOP 10

    session_id,

    status,

    command,

    cpu_time,

    total_elapsed_time,

    blocking_session_id,

    wait_type

FROM sys.dm_exec_requests

WHERE total_elapsed_time > 10000

ORDER BY total_elapsed_time DESC;