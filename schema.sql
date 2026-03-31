-- Job Application Tracker
-- schema.sql: Run this file to create your database and all tables

CREATE DATABASE IF NOT EXISTS job_tracker;
USE job_tracker;

-- Table 1: companies
CREATE TABLE IF NOT EXISTS companies (
    company_id   INT PRIMARY KEY AUTO_INCREMENT,
    company_name VARCHAR(100) NOT NULL,
    industry     VARCHAR(50),
    website      VARCHAR(200),
    city         VARCHAR(50),
    state        VARCHAR(50),
    notes        TEXT,
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table 2: jobs
CREATE TABLE IF NOT EXISTS jobs (
    job_id       INT PRIMARY KEY AUTO_INCREMENT,
    company_id   INT NOT NULL,
    job_title    VARCHAR(100) NOT NULL,
    job_type     ENUM('Full-time', 'Part-time', 'Contract', 'Internship'),
    salary_min   INT,
    salary_max   INT,
    job_url      VARCHAR(300),
    date_posted  DATE,
    requirements JSON,
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES companies(company_id) ON DELETE CASCADE
);

-- Table 3: applications
CREATE TABLE IF NOT EXISTS applications (
    application_id    INT PRIMARY KEY AUTO_INCREMENT,
    job_id            INT NOT NULL,
    application_date  DATE NOT NULL,
    status            ENUM('Applied','Screening','Interview','Offer','Rejected','Withdrawn') DEFAULT 'Applied',
    resume_version    VARCHAR(50),
    cover_letter_sent BOOLEAN DEFAULT FALSE,
    interview_data    JSON,
    created_at        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (job_id) REFERENCES jobs(job_id) ON DELETE CASCADE
);

-- Table 4: contacts
CREATE TABLE IF NOT EXISTS contacts (
    contact_id   INT PRIMARY KEY AUTO_INCREMENT,
    company_id   INT NOT NULL,
    contact_name VARCHAR(100) NOT NULL,
    title        VARCHAR(100),
    email        VARCHAR(100),
    phone        VARCHAR(20),
    linkedin_url VARCHAR(200),
    notes        TEXT,
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES companies(company_id) ON DELETE CASCADE
);

-- Sample data for testing
INSERT INTO companies (company_name, industry, website, city, state) VALUES
('TechCorp', 'Software', 'https://techcorp.com', 'Austin', 'TX'),
('DataCo', 'Data Analytics', 'https://dataco.com', 'Miami', 'FL'),
('StartupXYZ', 'Fintech', 'https://startupxyz.com', 'New York', 'NY');

INSERT INTO jobs (company_id, job_title, job_type, salary_min, salary_max, date_posted, requirements) VALUES
(1, 'Software Developer', 'Full-time', 80000, 110000, '2025-03-01', '["Python", "SQL", "Flask"]'),
(2, 'Data Analyst', 'Full-time', 70000, 95000, '2025-03-05', '["SQL", "Tableau", "Python"]'),
(3, 'Backend Engineer', 'Contract', 60, 80, '2025-03-10', '["Python", "REST APIs", "Docker"]');

INSERT INTO applications (job_id, application_date, status, resume_version, cover_letter_sent) VALUES
(1, '2025-03-03', 'Interview', 'v2', TRUE),
(2, '2025-03-07', 'Applied', 'v2', FALSE),
(3, '2025-03-12', 'Screening', 'v3', TRUE);

INSERT INTO contacts (company_id, contact_name, title, email) VALUES
(1, 'Jane Smith', 'Engineering Manager', 'jane@techcorp.com'),
(2, 'Bob Lee', 'HR Recruiter', 'bob@dataco.com');