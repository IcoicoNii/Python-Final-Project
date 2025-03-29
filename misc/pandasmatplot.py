import expenseTrackerAppdb as db
import pandas as pd
import sqlite3

def createCSV(report_id):
    #Declare Variables
    targetTable = f"Expenses_Report_{report_id}"

    # Establish Connection
    conn = sqlite3.connect("expense_tracker.db")
    cursor = conn.cursor()

    # SQL Statement
    cursor.execute(f"SELECT category, amount FROM {targetTable}")
    report = cursor.fetchall()
    conn.close()

    # File Handling for CSV
    with open("data.csv", 'w+') as f:
        f.writelines("Category,Amount\n")
        for expense in report:
            f.writelines(f"{expense[0]},{expense[1]}\n")

def readCSV():
    data = pd.read_csv("data.csv")
    

createCSV(1)


