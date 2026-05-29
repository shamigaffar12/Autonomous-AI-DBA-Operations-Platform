-- ============================================
-- Long Running Query Monitoring
-- Autonomous AI DBA Operations Platform
-- ============================================

SELECT

    session_id,
    status,
    command,
    cpu_time,
    total_elapsed_time,
    blocking_session_id,
    wait_type

FROM sys.dm_exec_requests

WHERE

    session_id > 50

    AND total_elapsed_time > 30000

ORDER BY total_elapsed_time DESC;