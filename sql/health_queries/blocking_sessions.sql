-- ============================================
-- Blocking Session Monitoring
-- Autonomous AI DBA Operations Platform
-- ============================================

SELECT TOP 10

    session_id,

    blocking_session_id,

    wait_type,

    wait_time,

    status

FROM sys.dm_exec_requests

WHERE blocking_session_id <> 0;