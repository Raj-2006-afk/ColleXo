-- College Societies Platform Database Schema
-- MySQL 5.7+ or MariaDB 10.2+

-- Drop tables if they exist (for clean reinstall)
DROP TABLE IF EXISTS form_responses;
DROP TABLE IF EXISTS society_forms;
DROP TABLE IF EXISTS societies;
DROP TABLE IF EXISTS users;

-- Users table (supports admin, society, and optional student accounts)
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('admin', 'society', 'student') NOT NULL DEFAULT 'society',
    is_active TINYINT(1) DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_role (role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Societies table (one registration per society enforced by unique constraints)
CREATE TABLE societies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NULL,
    name VARCHAR(255) NOT NULL UNIQUE,
    slug VARCHAR(255) NOT NULL UNIQUE,
    short_desc VARCHAR(512),
    long_desc TEXT,
    category ENUM('cultural', 'technical', 'sports', 'literary', 'social', 'other') DEFAULT 'other',
    contact_email VARCHAR(255) NOT NULL,
    contact_phone VARCHAR(20),
    faculty_incharge VARCHAR(255),
    logo_path VARCHAR(512) DEFAULT 'placeholder-logo.png',
    social_instagram VARCHAR(255),
    social_twitter VARCHAR(255),
    social_facebook VARCHAR(255),
    social_linkedin VARCHAR(255),
    website_url VARCHAR(512),
    is_approved TINYINT(1) DEFAULT 0,
    is_active TINYINT(1) DEFAULT 1,
    views_count INT DEFAULT 0,
    members_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_slug (slug),
    INDEX idx_category (category),
    INDEX idx_approved (is_approved),
    INDEX idx_active (is_active),
    UNIQUE KEY unique_society_registration (name, contact_email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Society Forms (recruitment/registration forms created by societies)
CREATE TABLE society_forms (
    id INT AUTO_INCREMENT PRIMARY KEY,
    society_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    form_schema JSON NOT NULL COMMENT 'Stores field definitions as JSON array',
    is_active TINYINT(1) DEFAULT 1,
    max_submissions INT DEFAULT NULL COMMENT 'NULL = unlimited',
    submissions_count INT DEFAULT 0,
    start_date DATETIME DEFAULT NULL,
    end_date DATETIME DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (society_id) REFERENCES societies(id) ON DELETE CASCADE,
    INDEX idx_society (society_id),
    INDEX idx_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Form Responses (student submissions)
CREATE TABLE form_responses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    form_id INT NOT NULL,
    submission_data JSON NOT NULL COMMENT 'Stores form field responses as JSON',
    submitter_email VARCHAR(255) NOT NULL,
    submitter_name VARCHAR(255),
    submitter_phone VARCHAR(20),
    files_json JSON NULL COMMENT 'Stores uploaded file metadata',
    ip_address VARCHAR(45),
    user_agent TEXT,
    honeypot_value VARCHAR(255) COMMENT 'Anti-bot field - should be empty',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (form_id) REFERENCES society_forms(id) ON DELETE CASCADE,
    INDEX idx_form (form_id),
    INDEX idx_email (submitter_email),
    INDEX idx_created (created_at),
    UNIQUE KEY unique_submission (form_id, submitter_email) COMMENT 'Prevent duplicate submissions'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create default admin user (password: admin123 - CHANGE THIS!)
-- Password hash for 'admin123' using bcrypt
INSERT INTO users (email, password_hash, role, is_active) 
VALUES ('admin@college.edu', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMeshwqfBdH1h5kZhW0VJbZjCy', 'admin', 1);
