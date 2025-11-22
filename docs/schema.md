# ColleXo - Database Schema

## Overview

ColleXo uses MySQL database with 4 main tables following the ER diagram specifications.

---

## Tables

### 1. USERS

Stores all user information including students, society heads, and admins.

| Column        | Type         | Constraints                 | Description                     |
| ------------- | ------------ | --------------------------- | ------------------------------- |
| user_id       | INT          | PRIMARY KEY, AUTO_INCREMENT | Unique user identifier          |
| user_name     | VARCHAR(255) | NOT NULL                    | User's full name                |
| user_email    | VARCHAR(255) | UNIQUE, NOT NULL            | User's email address            |
| user_password | VARCHAR(255) | NOT NULL                    | Hashed password (bcrypt)        |
| user_role     | ENUM         | NOT NULL                    | Role: student/societyHead/admin |
| created_at    | DATETIME     | DEFAULT CURRENT_TIMESTAMP   | Account creation timestamp      |

**Relationships:**

- One-to-Many with SOCIETIES (as society head)
- One-to-Many with APPLICATIONS (as applicant)

---

### 2. SOCIETIES

Stores information about college societies/clubs.

| Column             | Type         | Constraints                 | Description                          |
| ------------------ | ------------ | --------------------------- | ------------------------------------ |
| society_id         | INT          | PRIMARY KEY, AUTO_INCREMENT | Unique society identifier            |
| society_name       | VARCHAR(255) | UNIQUE, NOT NULL            | Society name                         |
| tagline            | VARCHAR(500) | NULL                        | Short descriptive tagline            |
| description        | TEXT         | NULL                        | Detailed description                 |
| category           | VARCHAR(100) | NULL                        | Category (Technical, Cultural, etc.) |
| logo_url           | VARCHAR(500) | NULL                        | Logo image path                      |
| member_count       | INT          | DEFAULT 0                   | Number of members                    |
| admission_open     | BOOLEAN      | DEFAULT TRUE                | Accepting new members?               |
| admission_deadline | DATE         | NULL                        | Application deadline                 |
| society_head_id    | INT          | FOREIGN KEY → users.user_id | Society head user ID                 |
| created_at         | DATETIME     | DEFAULT CURRENT_TIMESTAMP   | Society creation timestamp           |

**Relationships:**

- Many-to-One with USERS (society head)
- One-to-Many with FORMS
- One-to-Many with APPLICATIONS

**Indexes:**

- PRIMARY KEY on society_id
- UNIQUE on society_name
- FOREIGN KEY on society_head_id

---

### 3. FORMS

Recruitment/application forms created by societies.

| Column       | Type         | Constraints                        | Description                  |
| ------------ | ------------ | ---------------------------------- | ---------------------------- |
| form_id      | INT          | PRIMARY KEY, AUTO_INCREMENT        | Unique form identifier       |
| society_id   | INT          | FOREIGN KEY → societies.society_id | Parent society               |
| title        | VARCHAR(255) | NOT NULL                           | Form title                   |
| status       | ENUM         | DEFAULT 'draft'                    | Form status: draft/published |
| created_at   | DATETIME     | DEFAULT CURRENT_TIMESTAMP          | Form creation timestamp      |
| published_at | DATETIME     | NULL                               | Publication timestamp        |

**Relationships:**

- Many-to-One with SOCIETIES
- One-to-Many with APPLICATIONS

**Indexes:**

- PRIMARY KEY on form_id
- FOREIGN KEY on society_id

---

### 4. APPLICATIONS

Student applications to societies through forms.

| Column           | Type     | Constraints                        | Description                                   |
| ---------------- | -------- | ---------------------------------- | --------------------------------------------- |
| application_id   | INT      | PRIMARY KEY, AUTO_INCREMENT        | Unique application identifier                 |
| user_id          | INT      | FOREIGN KEY → users.user_id        | Applicant user ID                             |
| society_id       | INT      | FOREIGN KEY → societies.society_id | Target society                                |
| form_id          | INT      | FOREIGN KEY → forms.form_id        | Application form used                         |
| application_date | DATE     | NOT NULL                           | Date of application                           |
| status           | ENUM     | DEFAULT 'pending'                  | Status: pending/shortlisted/accepted/rejected |
| submitted_at     | DATETIME | DEFAULT CURRENT_TIMESTAMP          | Submission timestamp                          |

**Relationships:**

- Many-to-One with USERS (applicant)
- Many-to-One with SOCIETIES
- Many-to-One with FORMS

**Indexes:**

- PRIMARY KEY on application_id
- FOREIGN KEY on user_id
- FOREIGN KEY on society_id
- FOREIGN KEY on form_id

---

## Relationships Summary

```
USERS (1) ←→ (1) SOCIETIES [society_head_id]
  A society head manages one society

SOCIETIES (1) ←→ (N) FORMS [society_id]
  A society can have multiple recruitment forms

FORMS (1) ←→ (N) APPLICATIONS [form_id]
  A form can receive multiple applications

USERS (1) ←→ (N) APPLICATIONS [user_id]
  A student can submit multiple applications

SOCIETIES (1) ←→ (N) APPLICATIONS [society_id]
  A society receives multiple applications
```

---

## Data Initialization

### Seed Data (Auto-created on first run)

**Default Admin:**

- Email: `admin@collexo.com`
- Password: `admin123`
- Role: admin

**Sample Society Heads:**

1. John Doe (`john@collexo.com`, password: `head123`)
2. Jane Smith (`jane@collexo.com`, password: `head123`)

**Sample Student:**

- Email: `student@collexo.com`
- Password: `student123`

**Sample Societies:**

1. Tech Club - Technical society
2. Drama Society - Cultural society

**Sample Form:**

- Tech Club Recruitment 2025 (Published)

---

## Database Connection

**Configuration:**

- Host: `localhost`
- Port: `3306` (default MySQL)
- Database: `collexo`
- User: `root`
- Password: `` (empty)

**Auto-initialization:**
The application automatically:

1. Creates the database if it doesn't exist
2. Creates all tables with proper schema
3. Seeds initial data if tables are empty
4. Establishes foreign key relationships

---

## Queries Examples

### Get all societies with head info:

```sql
SELECT s.*, u.user_name as head_name
FROM societies s
LEFT JOIN users u ON s.society_head_id = u.user_id
ORDER BY s.created_at DESC;
```

### Get application statistics for a society:

```sql
SELECT
    COUNT(*) as total,
    SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) as pending,
    SUM(CASE WHEN status = 'accepted' THEN 1 ELSE 0 END) as accepted
FROM applications
WHERE society_id = ?;
```

### Get user's applications with details:

```sql
SELECT a.*, s.society_name, f.title as form_title
FROM applications a
JOIN societies s ON a.society_id = s.society_id
JOIN forms f ON a.form_id = f.form_id
WHERE a.user_id = ?
ORDER BY a.submitted_at DESC;
```

---

## Maintenance

### Backup Command:

```bash
mysqldump -u root collexo > backup.sql
```

### Restore Command:

```bash
mysql -u root collexo < backup.sql
```

### Reset Database:

```sql
DROP DATABASE IF EXISTS collexo;
-- Then restart the application to recreate
```

---

_Schema Version: 1.0_
_Last Updated: November 2025_
