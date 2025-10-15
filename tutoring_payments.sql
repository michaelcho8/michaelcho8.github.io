-- Tutoring Payment Tracking Database Schema
-- SQLite database for tracking student payments and sessions

-- Students table to store basic student information
CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT,
    parent_name TEXT,
    parent_email TEXT,
    package_type TEXT CHECK(package_type IN ('Individual', 'Weekly', 'Intensive')),
    hourly_rate DECIMAL(10,2) DEFAULT 50.00,
    created_date DATE DEFAULT CURRENT_DATE,
    is_active BOOLEAN DEFAULT 1
);

-- Sessions table to track individual tutoring sessions
CREATE TABLE sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    session_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    duration_hours DECIMAL(4,2) NOT NULL,
    subject TEXT NOT NULL,
    session_cost DECIMAL(10,2) NOT NULL,
    notes TEXT,
    status TEXT CHECK(status IN ('Scheduled', 'Completed', 'Cancelled', 'No-Show')) DEFAULT 'Scheduled',
    created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id)
);

-- Payments table to track all payments received
CREATE TABLE payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    payment_date DATE NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    payment_method TEXT CHECK(payment_method IN ('Cash', 'Check', 'Venmo', 'Zelle', 'Bank Transfer', 'Other')),
    reference_number TEXT, -- Check number, transaction ID, etc.
    notes TEXT,
    created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id)
);

-- Monthly packages table for tracking package-based billing
CREATE TABLE monthly_packages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    package_type TEXT CHECK(package_type IN ('Weekly', 'Intensive')) NOT NULL,
    month_year TEXT NOT NULL, -- Format: "2025-10"
    total_sessions INTEGER NOT NULL,
    completed_sessions INTEGER DEFAULT 0,
    package_cost DECIMAL(10,2) NOT NULL,
    is_paid BOOLEAN DEFAULT 0,
    payment_due_date DATE,
    notes TEXT,
    created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id),
    UNIQUE(student_id, month_year)
);

-- Create indexes for better performance
CREATE INDEX idx_students_email ON students(email);
CREATE INDEX idx_sessions_student_date ON sessions(student_id, session_date);
CREATE INDEX idx_payments_student_date ON payments(student_id, payment_date);
CREATE INDEX idx_monthly_packages_student_month ON monthly_packages(student_id, month_year);

-- Insert some sample data for testing
INSERT INTO students (name, email, parent_email, package_type, hourly_rate) VALUES
('Alex Johnson', 'alex.johnson@email.com', 'parent.johnson@email.com', 'Weekly', 50.00),
('Sarah Chen', 'sarah.chen@email.com', 'chen.family@email.com', 'Individual', 50.00),
('Mike Rodriguez', 'mike.rodriguez@email.com', 'rodriguez.parents@email.com', 'Intensive', 50.00);

-- Views for common queries
-- Outstanding balance view
CREATE VIEW student_balance AS
SELECT 
    s.id,
    s.name,
    s.email,
    COALESCE(SUM(sess.session_cost), 0) as total_owed,
    COALESCE(SUM(p.amount), 0) as total_paid,
    (COALESCE(SUM(sess.session_cost), 0) - COALESCE(SUM(p.amount), 0)) as balance_due
FROM students s
LEFT JOIN sessions sess ON s.id = sess.student_id AND sess.status = 'Completed'
LEFT JOIN payments p ON s.id = p.student_id
WHERE s.is_active = 1
GROUP BY s.id, s.name, s.email;

-- Monthly revenue view
CREATE VIEW monthly_revenue AS
SELECT 
    strftime('%Y-%m', session_date) as month,
    COUNT(*) as sessions_completed,
    SUM(session_cost) as revenue,
    SUM(duration_hours) as total_hours
FROM sessions 
WHERE status = 'Completed'
GROUP BY strftime('%Y-%m', session_date)
ORDER BY month DESC;

-- Payment summary view
CREATE VIEW payment_summary AS
SELECT 
    strftime('%Y-%m', payment_date) as month,
    COUNT(*) as payment_count,
    SUM(amount) as total_received,
    payment_method,
    COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY strftime('%Y-%m', payment_date)) as percentage
FROM payments
GROUP BY strftime('%Y-%m', payment_date), payment_method
ORDER BY month DESC, total_received DESC;