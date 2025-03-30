import sqlite3

# Create Database
def initialize_db():
    conn = sqlite3.connect('expense_tracker.db')
    cursor = conn.cursor()

    # Create Reports table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Reports (
            report_id INTEGER PRIMARY KEY AUTOINCREMENT,
            report_name TEXT NOT NULL,
            report_total INTEGER
        )
    ''')

    # # Create Expenses table with a foreign key to Reports
    # cursor.execute('''
    #     CREATE TABLE IF NOT EXISTS Expenses (
    #         expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
    #         report_id INTEGER NOT NULL,
    #         date TEXT NOT NULL,
    #         category TEXT NOT NULL,
    #         amount REAL NOT NULL,
    #         FOREIGN KEY (report_id) REFERENCES Reports(report_id)
    #     )
    # ''')

    conn.commit()
    conn.close()
    print("Database initialized and tables created (if they didn't already exist).")

# Add Report to Database Function
def add_report_to_db(report_no, report_name, total_expense):
    conn = sqlite3.connect('expense_tracker.db')
    cursor = conn.cursor()

    create_expenseTable_forReportNo(report_no)

    # Check if the report_id already exists
    cursor.execute("SELECT report_id FROM Reports WHERE report_id = ?", (report_no,))
    existing_report = cursor.fetchone()

    if existing_report:
        conn.close()
        return False  # Report already exists

    cursor.execute("INSERT INTO Reports VALUES (?, ?, ?)", (report_no, report_name, total_expense))
    conn.commit()
    conn.close()
    return True  # Successfully added report

# Get All Reports Function to Get All Reports for Display on the Dashboard
def get_all_reports():
    conn = sqlite3.connect('expense_tracker.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Reports")
    reports = cursor.fetchall()
    conn.close()
    return reports

# Add Expense Function to Add the Expense on the Database on the Table of the current report_id
def add_expense_to_db(expense_id, report_id, date, category, amount):
    conn = sqlite3.connect('expense_tracker.db')
    cursor = conn.cursor()
    targetTable = f"Expenses_Report_{report_id}"
    cursor.execute(
        f"INSERT INTO {targetTable} (expense_id, date, category, amount) VALUES (?, ?, ?, ?)",
        (expense_id, date, category, amount),
    )
    conn.commit()
    conn.close()
    print(f"Expense added to report {report_id}: {expense_id} - {category}: P{amount} on {date}.")

# Update Expense Function to Update the Expense based on expense_id on the Database on the Table of the current report_id
def update_expense_to_db(expense_id, report_id, date, category, amount):
    conn = sqlite3.connect('expense_tracker.db')
    cursor = conn.cursor()
    
    target_table = f"Expenses_Report_{report_id}"

    # Update the specific expense in the associated report table
    cursor.execute(
        f"""
        UPDATE {target_table} 
        SET date = ?, category = ?, amount = ? 
        WHERE expense_id = ?
        """,
        (date, category, amount, expense_id),
    )

    conn.commit()
    conn.close()
    print(f"Expense ID {expense_id} updated in table '{target_table}'.")


# Get expenses for the current report to display on the report window of the selected report
def get_expenses_for_report(report_id):
    conn = sqlite3.connect('expense_tracker.db')
    cursor = conn.cursor()
    targetTable = f"Expenses_Report_{report_id}"

    cursor.execute(f"SELECT expense_id, date, category, amount FROM {targetTable} ORDER BY date DESC")
    expenses = cursor.fetchall()
    conn.close()
    return expenses

# Delete the selected function from Database
def delete_expense(report_id, expense_id):
    conn = sqlite3.connect('expense_tracker.db')
    cursor = conn.cursor()
    
    target_table = f"Expenses_Report_{report_id}"  # Dynamically select the correct table
    cursor.execute(f"DELETE FROM {target_table} WHERE expense_id = ?", (expense_id,))
    
    conn.commit()
    conn.close()
    print(f"Expense with ID {expense_id} deleted from {target_table}.")

# Delete the Selected Report and the Expense Table associated with the Report_id (CASCADE DELETE)
def delete_report(report_id):
    conn = sqlite3.connect('expense_tracker.db')
    cursor = conn.cursor()
    
    # Drop the expense table associated with the report
    target_table = f"Expenses_Report_{report_id}"
    cursor.execute(f"DROP TABLE IF EXISTS {target_table}")
    
    # Delete the report entry from Reports table
    cursor.execute("DELETE FROM Reports WHERE report_id = ?", (report_id,))
    
    conn.commit()
    conn.close()
    print(f"Report with ID {report_id} and its associated table '{target_table}' deleted.")

# Check if report already exists for ID validation
def report_exists(report_no):
    conn = sqlite3.connect('expense_tracker.db')
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM Reports WHERE report_id = ?", (report_no,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

# Get latest expense ID from the expenses_report{report_id} table to ensure integrity constraint
def get_latest_id(report_id):
    conn = sqlite3.connect('expense_tracker.db')
    cursor = conn.cursor()
    targetTable = f"Expenses_Report_{report_id}"

    cursor.execute(f"SELECT MAX(expense_id) FROM {targetTable}")
    max_id = cursor.fetchone()[0]  # Fetch the first column of the result

    conn.close()

    return max_id if max_id is not None else 0  # Return 0 if no records exist

# Create expense table associated with report number
# This is created the moment the report is created
def create_expenseTable_forReportNo(report_id):
    conn = sqlite3.connect('expense_tracker.db')
    cursor = conn.cursor()
    
    table_name = f"Expenses_Report_{report_id}"  # Dynamic table name based on report_id
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()
    print(f"Table '{table_name}' created successfully (if it didn't already exist).")

# Update the total expense of the report to reflect it on the dashboard real time
def update_total_expense(report_id):
    conn = sqlite3.connect('expense_tracker.db')
    cursor = conn.cursor()
    target_table = f"Expenses_Report_{report_id}"
    
    # Calculate the total sum of amounts from the expenses table
    cursor.execute(f"SELECT SUM(amount) FROM {target_table}")
    total = cursor.fetchone()[0]  # Fetch result

    # Ensure total is not None (set to 0 if there are no expenses)
    total = total if total is not None else 0.0  

    # Update the total_expense in the Reports table
    cursor.execute("UPDATE Reports SET report_total = ? WHERE report_id = ?", (total, report_id))

    conn.commit()
    conn.close()

    print(f"Updated total expense for Report ID {report_id}: {total}")

def changeReportName(report_id, changed_name):
    conn = sqlite3.connect('expense_tracker.db')
    cursor = conn.cursor()

    # Change the Target Report Name
    cursor.execute(f"UPDATE Reports SET report_name = ? WHERE report_id = ?", (changed_name, report_id))

    conn.commit()
    conn.close()

    print(f"Report ID #{report_id} name changed to '{changed_name}'")

initialize_db()