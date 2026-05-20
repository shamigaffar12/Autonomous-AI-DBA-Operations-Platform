# Database Planning Document  
## Autonomous AI DBA Operations Platform

As part of the initial development phase of the Autonomous AI DBA Operations Platform, the following database structure has been planned to support monitoring, incident management, AI-driven analysis, remediation workflows, and operational reporting.

The proposed schema is designed to keep the platform modular, scalable, and suitable for future enhancements.

---

# 1. incidents

The `incidents` table will be used to maintain records of issues identified within database environments. These incidents may be generated automatically through monitoring tools or detected by AI-based analysis modules.

| Column Name | Data Type | Purpose |
|---|---|---|
| incident_id | UUID | Unique ID for each incident |
| title | VARCHAR | Short description of the issue |
| severity | VARCHAR | Incident priority level |
| status | VARCHAR | Current incident state |
| created_at | TIMESTAMP | Incident creation timestamp |
| resolved_at | TIMESTAMP | Resolution timestamp |
| source | VARCHAR | Monitoring source or detection system |

---

# 2. alerts

The `alerts` table is intended to store real-time alerts generated from monitoring systems, threshold breaches, or anomaly detection services.

| Column Name | Data Type | Purpose |
|---|---|---|
| alert_id | UUID | Unique identifier for alert |
| alert_type | VARCHAR | Type/category of alert |
| severity | VARCHAR | Alert severity level |
| message | TEXT | Alert details |
| generated_at | TIMESTAMP | Alert generation time |

---

# 3. monitoring_snapshots

This table will contain periodic monitoring statistics collected from databases and infrastructure systems for performance analysis and historical tracking.

| Column Name | Data Type | Purpose |
|---|---|---|
| snapshot_id | UUID | Unique snapshot ID |
| database_name | VARCHAR | Database being monitored |
| cpu_usage | FLOAT | CPU utilization |
| memory_usage | FLOAT | Memory utilization |
| active_sessions | INTEGER | Number of active database sessions |
| captured_at | TIMESTAMP | Time when snapshot was captured |

---

# 4. rca_reports

The `rca_reports` table will store Root Cause Analysis reports prepared using AI-based investigation workflows and incident correlation mechanisms.

| Column Name | Data Type | Purpose |
|---|---|---|
| rca_id | UUID | Unique RCA report ID |
| incident_id | UUID | Related incident reference |
| root_cause | TEXT | Root cause identified by AI |
| confidence_score | FLOAT | Confidence level of analysis |
| generated_at | TIMESTAMP | Report generation timestamp |

---

# 5. remediation_plans

This table will manage remediation recommendations and recovery actions suggested by the AI engine or operational workflows.

| Column Name | Data Type | Purpose |
|---|---|---|
| remediation_id | UUID | Unique remediation ID |
| incident_id | UUID | Associated incident |
| remediation_steps | TEXT | Suggested resolution steps |
| automation_possible | BOOLEAN | Indicates whether automation is feasible |
| created_at | TIMESTAMP | Creation timestamp |

---

# 6. approvals

The `approvals` table is planned to support governance and approval processes before executing critical remediation activities in production environments.

| Column Name | Data Type | Purpose |
|---|---|---|
| approval_id | UUID | Unique approval identifier |
| remediation_id | UUID | Linked remediation request |
| approver_name | VARCHAR | Name of approver |
| approval_status | VARCHAR | Approval decision |
| approved_at | TIMESTAMP | Approval timestamp |

---

# 7. audit_logs

This table will store audit records for tracking activities performed within the platform by users, administrators, or AI agents.

| Column Name | Data Type | Purpose |
|---|---|---|
| log_id | UUID | Unique log record ID |
| action | VARCHAR | Action performed |
| performed_by | VARCHAR | User or system responsible |
| action_time | TIMESTAMP | Action execution time |
| details | TEXT | Additional information |

---

# 8. daily_handover

The `daily_handover` table will maintain automatically generated daily operational summaries to assist DBA teams during shift transitions and reporting activities.

| Column Name | Data Type | Purpose |
|---|---|---|
| handover_id | UUID | Unique handover ID |
| summary | TEXT | Daily operational summary |
| pending_issues | TEXT | Pending tasks or unresolved issues |
| generated_at | TIMESTAMP | Report generation time |

---


# Summary

The planned database structure aims to provide a centralized and organized foundation for the Autonomous AI DBA Operations Platform.  
The schema has been designed to support intelligent monitoring, automated analysis, operational governance, remediation workflows, and long-term scalability of the system.