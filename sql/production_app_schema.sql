/* =========================================================
   Production Application Database Schema
   Autonomous AI DBA Operations Platform
   Target: Microsoft SQL Server / Azure SQL
   ========================================================= */

IF NOT EXISTS (SELECT 1 FROM sys.schemas WHERE name = 'aidba')
BEGIN
    EXEC('CREATE SCHEMA aidba');
END;
GO

IF OBJECT_ID('aidba.Users', 'U') IS NULL
BEGIN
    CREATE TABLE aidba.Users (
        UserId INT IDENTITY(1,1) PRIMARY KEY,
        Username NVARCHAR(100) NOT NULL UNIQUE,
        DisplayName NVARCHAR(200) NOT NULL,
        RoleName NVARCHAR(50) NOT NULL,
        PasswordHash NVARCHAR(500) NOT NULL,
        PasswordSalt NVARCHAR(200) NOT NULL,
        IsActive BIT NOT NULL DEFAULT 1,
        CreatedAt DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
        UpdatedAt DATETIME2 NULL,
        LastLoginAt DATETIME2 NULL
    );
END;
GO

IF OBJECT_ID('aidba.ApprovalRequests', 'U') IS NULL
BEGIN
    CREATE TABLE aidba.ApprovalRequests (
        ApprovalId NVARCHAR(100) NOT NULL PRIMARY KEY,
        RequestTitle NVARCHAR(300) NOT NULL,
        ActionName NVARCHAR(150) NOT NULL,
        RiskLevel NVARCHAR(50) NOT NULL,
        RequestedBy NVARCHAR(100) NULL,
        Status NVARCHAR(50) NOT NULL DEFAULT 'PENDING',
        PayloadJson NVARCHAR(MAX) NULL,
        CreatedAt DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
        UpdatedAt DATETIME2 NULL,
        ApprovedBy NVARCHAR(100) NULL,
        ApprovedAt DATETIME2 NULL,
        RejectedBy NVARCHAR(100) NULL,
        RejectedAt DATETIME2 NULL
    );
END;
GO

IF OBJECT_ID('aidba.ExecutionHistory', 'U') IS NULL
BEGIN
    CREATE TABLE aidba.ExecutionHistory (
        ExecutionId BIGINT IDENTITY(1,1) PRIMARY KEY,
        ApprovalId NVARCHAR(100) NULL,
        ActionName NVARCHAR(150) NOT NULL,
        ExecutionStatus NVARCHAR(50) NOT NULL,
        ExecutedBy NVARCHAR(100) NULL,
        ResultJson NVARCHAR(MAX) NULL,
        ExecutedAt DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME()
    );
END;
GO

IF OBJECT_ID('aidba.AuditLog', 'U') IS NULL
BEGIN
    CREATE TABLE aidba.AuditLog (
        AuditId BIGINT IDENTITY(1,1) PRIMARY KEY,
        EventType NVARCHAR(150) NOT NULL,
        EventSource NVARCHAR(150) NULL,
        Username NVARCHAR(100) NULL,
        Severity NVARCHAR(50) NOT NULL DEFAULT 'INFO',
        Message NVARCHAR(MAX) NOT NULL,
        MetadataJson NVARCHAR(MAX) NULL,
        CreatedAt DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME()
    );
END;
GO

IF OBJECT_ID('aidba.NotificationHistory', 'U') IS NULL
BEGIN
    CREATE TABLE aidba.NotificationHistory (
        NotificationId BIGINT IDENTITY(1,1) PRIMARY KEY,
        Channel NVARCHAR(50) NOT NULL,
        Subject NVARCHAR(300) NULL,
        Recipient NVARCHAR(500) NULL,
        Status NVARCHAR(50) NOT NULL,
        ErrorMessage NVARCHAR(MAX) NULL,
        CreatedAt DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME()
    );
END;
GO