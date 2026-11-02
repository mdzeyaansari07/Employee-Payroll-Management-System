CREATE DATABASE IF NOT EXISTS payroll_db;
USE payroll_db;

CREATE TABLE IF NOT EXISTS employees (
    employee_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    department VARCHAR(80) NOT NULL,
    email VARCHAR(120),
    phone VARCHAR(20),
    basic_salary DECIMAL(12,2) NOT NULL,
    allowance DECIMAL(12,2) NOT NULL DEFAULT 0,
    deduction DECIMAL(12,2) NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS payroll (
    payroll_id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT NOT NULL,
    pay_date DATE NOT NULL,
    basic_salary DECIMAL(12,2) NOT NULL,
    allowance DECIMAL(12,2) NOT NULL DEFAULT 0,
    deduction DECIMAL(12,2) NOT NULL DEFAULT 0,
    gross_salary DECIMAL(12,2) NOT NULL,
    net_salary DECIMAL(12,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_payroll_employee FOREIGN KEY (employee_id)
      REFERENCES employees(employee_id) ON DELETE RESTRICT,
    UNIQUE KEY unique_employee_pay_month (employee_id, pay_date)
);

-- Optional sample employee:
INSERT INTO employees (full_name, department, email, phone, basic_salary, allowance, deduction)
VALUES ('Rahul Sharma', 'IT', 'rahul@example.com', '9876543210', 30000, 2500, 860);
