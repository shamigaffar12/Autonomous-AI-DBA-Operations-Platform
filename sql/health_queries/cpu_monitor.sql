-- ============================================
-- CPU Monitoring
-- Autonomous AI DBA Operations Platform
-- ============================================

SELECT TOP 10

    session_id,
    status,
    cpu_time,
    total_elapsed_time,
    reads,
    writes,
    logical_reads

FROM sys.dm_exec_requests

WHERE session_id > 50

ORDER BY cpu_time DESC;