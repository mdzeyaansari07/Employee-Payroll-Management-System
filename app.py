from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error
from decimal import Decimal, InvalidOperation
from datetime import date

app = Flask(__name__)
app.secret_key = "change-this-secret-key"

# Update these values to match your local MySQL installation.
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "YOUR_MYSQL_PASSWORD",
    "database": "employee_payroll"
}

def get_db():
    return mysql.connector.connect(**DB_CONFIG)

def money(value):
    try:
        return Decimal(str(value or "0"))
    except InvalidOperation:
        return Decimal("0")

@app.route("/")
def index():
    conn = get_db()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT COUNT(*) AS total FROM employees")
    total_employees = cur.fetchone()["total"]
    cur.execute("SELECT COALESCE(SUM(net_salary), 0) AS total FROM payroll")
    total_paid = cur.fetchone()["total"]
    cur.execute("""
        SELECT p.id, e.name, p.pay_month, p.basic_salary, p.allowances,
               p.deductions, p.net_salary, p.created_at
        FROM payroll p JOIN employees e ON e.id = p.employee_id
        ORDER BY p.id DESC LIMIT 5
    """)
    recent_payroll = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("index.html", total_employees=total_employees,
                           total_paid=total_paid, recent_payroll=recent_payroll)

@app.route("/employees")
def employees():
    conn = get_db()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM employees ORDER BY id DESC")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("employees.html", employees=rows)

@app.route("/employees/add", methods=["POST"])
def add_employee():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    department = request.form.get("department", "").strip()
    designation = request.form.get("designation", "").strip()
    basic_salary = money(request.form.get("basic_salary"))
    if not name or not email or basic_salary <= 0:
        flash("Enter a name, email and a valid basic salary.", "error")
        return redirect(url_for("employees"))
    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO employees (name, email, department, designation, basic_salary)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, email, department, designation, basic_salary))
        conn.commit()
        flash("Employee added successfully.", "success")
    except Error as exc:
        conn.rollback()
        flash(f"Could not add employee: {exc}", "error")
    finally:
        cur.close()
        conn.close()
    return redirect(url_for("employees"))

@app.route("/employees/delete/<int:employee_id>", methods=["POST"])
def delete_employee(employee_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM employees WHERE id = %s", (employee_id,))
    conn.commit()
    cur.close()
    conn.close()
    flash("Employee deleted.", "success")
    return redirect(url_for("employees"))

@app.route("/payroll", methods=["GET", "POST"])
def payroll():
    conn = get_db()
    cur = conn.cursor(dictionary=True)
    if request.method == "POST":
        employee_id = request.form.get("employee_id")
        pay_month = request.form.get("pay_month")
        allowances = money(request.form.get("allowances"))
        deductions = money(request.form.get("deductions"))
        cur.execute("SELECT id, basic_salary FROM employees WHERE id = %s", (employee_id,))
        employee = cur.fetchone()
        if not employee or not pay_month or allowances < 0 or deductions < 0:
            flash("Please enter valid payroll details.", "error")
        else:
            basic = money(employee["basic_salary"])
            net = basic + allowances - deductions
            if net < 0:
                flash("Deductions cannot exceed basic salary plus allowances.", "error")
            else:
                try:
                    cur.execute("""
                        INSERT INTO payroll
                        (employee_id, pay_month, basic_salary, allowances, deductions, net_salary)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (employee_id, pay_month, basic, allowances, deductions, net))
                    conn.commit()
                    flash(f"Payroll generated. Net salary: ₹{net:,.2f}", "success")
                except Error as exc:
                    conn.rollback()
                    flash(f"Could not generate payroll: {exc}", "error")
    cur.execute("SELECT id, name, basic_salary FROM employees ORDER BY name")
    employee_rows = cur.fetchall()
    cur.execute("""
        SELECT p.*, e.name FROM payroll p
        JOIN employees e ON e.id = p.employee_id
        ORDER BY p.id DESC
    """)
    payroll_rows = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("payroll.html", employees=employee_rows, payroll=payroll_rows,
                           today=date.today().strftime("%Y-%m"))

if __name__ == "__main__":
    app.run(debug=True)
