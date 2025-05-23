-- Baze Internship Database System Schema

-- Users table (base table for all user types)
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    full_name TEXT NOT NULL,
    phone TEXT,
    user_type TEXT NOT NULL CHECK(user_type IN ('student', 'hod', 'supervisor', 'admin')),
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

-- Students table (extends users)
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    user_id INTEGER UNIQUE NOT NULL,
    student_id TEXT UNIQUE NOT NULL,
    department TEXT NOT NULL,
    level TEXT NOT NULL CHECK(level IN ('200', '300', '400')),
    matriculation_number TEXT UNIQUE NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- HODs/Department Supervisors table
CREATE TABLE IF NOT EXISTS hods (
    id INTEGER PRIMARY KEY,
    user_id INTEGER UNIQUE NOT NULL,
    staff_id TEXT UNIQUE NOT NULL,
    department TEXT NOT NULL,
    designation TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Organization Supervisors table
CREATE TABLE IF NOT EXISTS organization_supervisors (
    id INTEGER PRIMARY KEY,
    user_id INTEGER UNIQUE NOT NULL,
    organization_name TEXT NOT NULL,
    organization_address TEXT,
    position TEXT,
    department TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Internship Placements table
CREATE TABLE IF NOT EXISTS internship_placements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    organization_name TEXT NOT NULL,
    organization_address TEXT NOT NULL,
    department TEXT NOT NULL,
    supervisor_name TEXT NOT NULL,
    supervisor_email TEXT NOT NULL,
    supervisor_phone TEXT,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    status TEXT DEFAULT 'active' CHECK(status IN ('active', 'completed', 'terminated')),
    assigned_hod_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (assigned_hod_id) REFERENCES hods(id)
);

-- Attendance table
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    placement_id INTEGER NOT NULL,
    date DATE NOT NULL,
    status TEXT NOT NULL CHECK(status IN ('present', 'absent', 'late', 'excused')),
    check_in_time TIME,
    check_out_time TIME,
    remarks TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (placement_id) REFERENCES internship_placements(id) ON DELETE CASCADE,
    UNIQUE(student_id, date)
);

-- Weekly Logs table
CREATE TABLE IF NOT EXISTS weekly_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    placement_id INTEGER NOT NULL,
    week_number INTEGER NOT NULL,
    week_start_date DATE NOT NULL,
    week_end_date DATE NOT NULL,
    activities TEXT NOT NULL,
    skills_learned TEXT,
    challenges TEXT,
    supervisor_comment TEXT,
    hod_comment TEXT,
    status TEXT DEFAULT 'draft' CHECK(status IN ('draft', 'submitted', 'reviewed')),
    submitted_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (placement_id) REFERENCES internship_placements(id) ON DELETE CASCADE
);

-- File Uploads table
CREATE TABLE IF NOT EXISTS file_uploads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    placement_id INTEGER NOT NULL,
    file_type TEXT NOT NULL CHECK(file_type IN ('workflow_chart', 'workspace_photo', 'document', 'completion_letter')),
    file_name TEXT NOT NULL,
    file_path TEXT NOT NULL,
    description TEXT,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (placement_id) REFERENCES internship_placements(id) ON DELETE CASCADE
);

-- Evaluations table
CREATE TABLE IF NOT EXISTS evaluations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    placement_id INTEGER NOT NULL,
    evaluator_id INTEGER NOT NULL,
    evaluator_type TEXT NOT NULL CHECK(evaluator_type IN ('hod', 'supervisor')),
    punctuality INTEGER CHECK(punctuality BETWEEN 1 AND 5),
    communication INTEGER CHECK(communication BETWEEN 1 AND 5),
    professionalism INTEGER CHECK(professionalism BETWEEN 1 AND 5),
    technical_skills INTEGER CHECK(technical_skills BETWEEN 1 AND 5),
    initiative INTEGER CHECK(initiative BETWEEN 1 AND 5),
    overall_rating INTEGER CHECK(overall_rating BETWEEN 1 AND 5),
    comments TEXT,
    recommendation TEXT,
    evaluated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (placement_id) REFERENCES internship_placements(id) ON DELETE CASCADE,
    FOREIGN KEY (evaluator_id) REFERENCES users(id)
);

-- Notifications table
CREATE TABLE IF NOT EXISTS notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    message TEXT NOT NULL,
    type TEXT NOT NULL CHECK(type IN ('reminder', 'alert', 'info', 'warning')),
    is_read BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    read_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Activity Log table (for audit trail)
CREATE TABLE IF NOT EXISTS activity_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    action TEXT NOT NULL,
    entity_type TEXT,
    entity_id INTEGER,
    ip_address TEXT,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Create indexes for better performance
CREATE INDEX idx_students_department ON students(department);
CREATE INDEX idx_placements_student ON internship_placements(student_id);
CREATE INDEX idx_placements_status ON internship_placements(status);
CREATE INDEX idx_attendance_student_date ON attendance(student_id, date);
CREATE INDEX idx_weekly_logs_student ON weekly_logs(student_id);
CREATE INDEX idx_notifications_user ON notifications(user_id, is_read);
CREATE INDEX idx_activity_logs_user ON activity_logs(user_id);

-- Create views for common queries
CREATE VIEW IF NOT EXISTS active_internships AS
SELECT 
    ip.*,
    s.student_id,
    s.department as student_department,
    s.level,
    u.full_name as student_name,
    u.email as student_email
FROM internship_placements ip
JOIN students s ON ip.student_id = s.id
JOIN users u ON s.user_id = u.id
WHERE ip.status = 'active';

CREATE VIEW IF NOT EXISTS student_attendance_summary AS
SELECT 
    s.id as student_id,
    s.student_id as student_number,
    u.full_name,
    COUNT(CASE WHEN a.status = 'present' THEN 1 END) as days_present,
    COUNT(CASE WHEN a.status = 'absent' THEN 1 END) as days_absent,
    COUNT(CASE WHEN a.status = 'late' THEN 1 END) as days_late,
    COUNT(a.id) as total_days
FROM students s
JOIN users u ON s.user_id = u.id
LEFT JOIN attendance a ON s.id = a.student_id
GROUP BY s.id;