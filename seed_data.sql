-- ColleXo - Seed Data for Testing
-- Run this after schema.sql to populate with sample data

-- Sample societies (approved)
INSERT INTO societies (user_id, name, slug, short_desc, long_desc, category, contact_email, contact_phone, faculty_incharge, is_approved, is_active, members_count, views_count) VALUES
(NULL, 'Computer Science Society', 'computer-science-society', 'Fostering innovation and technology excellence among students', 'The Computer Science Society is dedicated to promoting technical skills, innovation, and collaboration among computer science students. We organize hackathons, workshops, coding competitions, and tech talks throughout the year.', 'technical', 'css@college.edu', '1234567890', 'Dr. Sarah Johnson', 1, 1, 150, 1250),
(NULL, 'Drama Club', 'drama-club', 'Bringing stories to life through theater and performance', 'Our Drama Club provides a creative platform for students passionate about theater, acting, and stage production. We organize plays, street performances, and participate in intercollegiate competitions.', 'cultural', 'drama@college.edu', '1234567891', 'Prof. Michael Brown', 1, 1, 85, 890),
(NULL, 'Robotics Club', 'robotics-club', 'Building the future with robotics and automation', 'The Robotics Club focuses on hands-on learning in robotics, automation, and embedded systems. Members work on projects ranging from line-following robots to advanced autonomous systems.', 'technical', 'robotics@college.edu', '1234567892', 'Dr. Emily Chen', 1, 1, 120, 1050),
(NULL, 'Literary Society', 'literary-society', 'Celebrating the written word through poetry, prose, and debate', 'The Literary Society promotes reading, writing, and intellectual discourse. We host poetry slams, book clubs, writing workshops, and debate competitions.', 'literary', 'literary@college.edu', '1234567893', 'Prof. David Wilson', 1, 1, 95, 780),
(NULL, 'Basketball Team', 'basketball-team', 'Shooting hoops and building champions', 'Our Basketball Team represents the college in intercollegiate tournaments and promotes fitness, teamwork, and sportsmanship among students.', 'sports', 'basketball@college.edu', '1234567894', 'Coach Robert Taylor', 1, 1, 45, 620);

-- Sample form for Computer Science Society
INSERT INTO society_forms (society_id, title, description, form_schema, is_active, max_submissions, submissions_count) VALUES
(1, 'Membership Registration 2025', 'Join the Computer Science Society and be part of our amazing tech community!', 
'[{"name":"year","type":"select","label":"Year of Study","placeholder":"","required":true,"options":["First Year","Second Year","Third Year","Fourth Year"]},{"name":"branch","type":"text","label":"Branch/Department","placeholder":"e.g., Computer Science","required":true,"options":[]},{"name":"skills","type":"checkbox","label":"Programming Languages You Know","placeholder":"","required":false,"options":["Python","Java","C++","JavaScript","Go","Rust"]},{"name":"interests","type":"textarea","label":"Why do you want to join CSS?","placeholder":"Tell us about your interests...","required":true,"options":[]},{"name":"resume","type":"file","label":"Upload Resume (Optional)","placeholder":"","required":false,"options":[]}]', 
1, NULL, 12);

-- Sample form for Drama Club
INSERT INTO society_forms (society_id, title, description, form_schema, is_active, submissions_count) VALUES
(2, 'Annual Play Auditions', 'Auditions for our annual theater production. All roles available!',
'[{"name":"experience","type":"radio","label":"Previous Acting Experience","placeholder":"","required":true,"options":["Beginner","Intermediate","Advanced"]},{"name":"role_preference","type":"select","label":"Preferred Role Type","placeholder":"","required":false,"options":["Lead Role","Supporting Role","Ensemble","Behind the Scenes"]},{"name":"special_skills","type":"textarea","label":"Special Skills (singing, dancing, accents, etc.)","placeholder":"","required":false,"options":[]},{"name":"availability","type":"checkbox","label":"Available Days for Rehearsals","placeholder":"","required":true,"options":["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]}]',
1, 18);

-- Sample submissions for Computer Science Society
INSERT INTO form_responses (form_id, submission_data, submitter_email, submitter_name, submitter_phone, ip_address, created_at) VALUES
(1, '{"year":"Second Year","branch":"Computer Science","skills":["Python","JavaScript"],"interests":"I am passionate about web development and want to learn more about full-stack technologies.","resume":"resume_john.pdf"}', 'john.doe@college.edu', 'John Doe', '9876543210', '192.168.1.1', NOW() - INTERVAL 2 DAY),
(1, '{"year":"Third Year","branch":"Information Technology","skills":["Java","Python","C++"],"interests":"Interested in competitive programming and algorithm design. Want to participate in hackathons.","resume":""}', 'jane.smith@college.edu', 'Jane Smith', '9876543211', '192.168.1.2', NOW() - INTERVAL 1 DAY),
(1, '{"year":"First Year","branch":"Computer Engineering","skills":["C++","Python"],"interests":"New to college and eager to learn about software development and collaborate on projects.","resume":""}', 'alex.wong@college.edu', 'Alex Wong', '9876543212', '192.168.1.3', NOW());

UPDATE society_forms SET submissions_count = 3 WHERE id = 1;

-- Additional admin user (if needed for testing)
-- Password: testadmin123
INSERT INTO users (email, password_hash, role, is_active) VALUES
('testadmin@college.edu', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMeshwqfBdH1h5kZhW0VJbZjCy', 'admin', 1);
