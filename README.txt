EMPLOYEE PAYROLL MANAGEMENT SYSTEM
===================================

TECHNOLOGIES
- Python + Flask
- MySQL
- HTML, CSS and JavaScript

REQUIREMENTS
- Python 3 installed
- MySQL Server installed and running
- VS Code (recommended)

SETUP IN VS CODE (Windows)
1. Extract this ZIP file.
2. Open the extracted Employee_Payroll_Management_System folder in VS Code.
3. Open Terminal > New Terminal.
4. Create a virtual environment:
      py -m venv .venv
5. Activate it in PowerShell:
      .\.venv\Scripts\Activate.ps1
   If PowerShell blocks activation, use Command Prompt:
      .venv\Scripts\activate.bat
6. Install dependencies:
      python -m pip install -r requirements.txt
7. Open MySQL Workbench or MySQL command line.
8. Run the complete database.sql script.
9. Open app.py and edit DB_CONFIG:
      user: your MySQL username (usually root)
      password: your actual MySQL password
   Do not leave YOUR_MYSQL_PASSWORD unchanged.
10. Run the application:
      python app.py
11. Open this address in your browser:
      http://127.0.0.1:5000

FEATURES
- Dashboard with employee count and total generated net payroll
- Add and delete employees
- Search employee directory
- Generate monthly payroll
- Automatic net salary calculation
- Payroll history

PAYROLL FORMULA
Net Salary = Basic Salary + Allowances - Deductions

NOTES
- The database script creates the database and tables.
- Sample employees are inserted by database.sql.
- One employee can have one payroll record per month. Re-running a
  payroll for the same employee and month will be rejected by MySQL.
- This is an educational starter project. For real deployment, add
  authentication, CSRF protection, role permissions and production settings.
