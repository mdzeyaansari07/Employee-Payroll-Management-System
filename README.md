# Employee Payroll Management System

A simple full-stack payroll website built with HTML, CSS, JavaScript, Python (Flask), and MySQL.

## Features
- Dashboard with employee count and current-month payroll total
- Add and delete employee records
- Search employees by name, department, or email
- Generate payroll using `Net Salary = Basic Salary + Allowance - Deduction`
- View recent payroll records
- MySQL database with parameterized SQL queries

## Requirements
- Python 3.10+
- MySQL Server and MySQL Workbench (or MySQL command line)
- Visual Studio Code

## Setup in Windows / VS Code

1. Install Python and MySQL Server. Open this folder in VS Code.
2. Start the MySQL server.
3. Open MySQL Workbench or the MySQL command line and run the complete `schema.sql` file.
4. Open `app.py`. In `DB_CONFIG`, replace `YOUR_MYSQL_PASSWORD` with your MySQL root password. If you use a different MySQL username, update `user` too.
5. Open the VS Code terminal in this project folder and run:

   ```bash
   py -m venv venv
   venv\\Scripts\\activate
   pip install -r requirements.txt
   ```

   If PowerShell blocks activation, use Command Prompt terminal, or run `venv\\Scripts\\python.exe -m pip install -r requirements.txt`.

6. Start the website:

   ```bash
   python app.py
   ```

7. Open this address in your browser: http://127.0.0.1:5000

## Important notes
- This starter project is intended for local academic/demo use. It does not include user login, role permissions, payslip PDF generation, tax rules, or production security hardening.
- Change `app.secret_key` before deployment. Do not publish database passwords to GitHub.
- Payroll is calculated from the salary values stored on the employee record. Update those values in MySQL if they change.
- The unique employee/pay-month constraint prevents generating duplicate payroll for the same employee and month.
- Employees with payroll history cannot be deleted until their payroll records are handled.
