import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import simpledialog, messagebox
import sqlite3
import re

# Function for getting data from Database
def fetch_data(timeframe, report_id, report_name):
    # Declaring target table
    targetTable = f"Expenses_Report_{report_id}"

    # Connect to the database
    conn = sqlite3.connect("expense_tracker.db")  # Adjust to your DB file
    cursor = conn.cursor()

    # SQL query based on timeframe
    data = []
    
    if timeframe == "Daily":
        while True:
            selected_date = simpledialog.askstring("Select Date", "Enter date (YYYY-MM-DD):")
            if selected_date is None:  
                return None  # If the user cancels, exit the function

            date_pattern = r"^\d{4}-\d{2}-\d{2}$"
            if not re.match(date_pattern, selected_date):
                messagebox.showwarning("Input Error", "Date must be in YYYY-MM-DD format.")
                continue  # Ask again if the format is incorrect
            else:
                break  # Exit loop if the format is valid

        cursor.execute(f"SELECT category, SUM(amount) FROM {targetTable} WHERE date = ? GROUP BY category", (selected_date,))
    
    elif timeframe == "Weekly":
        cursor.execute(f"""
            SELECT category, SUM(amount) 
            FROM {targetTable} 
            WHERE date BETWEEN DATE('now', '-6 days') AND DATE('now') 
            GROUP BY category
        """)
    
    elif timeframe == "Monthly":
        cursor.execute(f"""
            SELECT category, SUM(amount) 
            FROM {targetTable} 
            WHERE date BETWEEN DATE('now', '-30 days') AND DATE('now') 
            GROUP BY category
        """)

    # Fetch data
    data = cursor.fetchall()
    conn.close()

    # Debugging: Print data to check if it's fetching correctly
    print(f"Fetched Data for {timeframe}: {data}")

    # Check if data is empty and stop execution
    if not data:
        messagebox.showinfo("No Data", f"No data available for the selected {timeframe.lower()} timeframe.")
        return None  # Return None explicitly if no data

    # Proceed only if data exists
    write_data(data)
    create_chart(timeframe, report_id, report_name)

    return data  # Return data for further validation
    
# Function for CSV file creation
def write_data(data):
    with open("data.csv", 'w+') as f:
        f.writelines("category,amount\n")
        for list in data:
            f.writelines(f"{list[0]},{list[1]}\n")

# Function for pie chart creation
def create_chart(timeframe, report_id, report_name):
    # Read File
    data = pd.read_csv("data.csv")

    # Declare Data
    values = data['amount']
    labels = data['category']
    mycolors = ['#283618', '#606c38','#aabf64', '#bc6c25', '#dda15e', '#cdcab4'] 
    
    # Formatter to show values instead of percentages
    def autopct_format(values):
        def my_format(pct):
            total = sum(values)
            val = int(round(pct*total/100.0))
            return '{v:d}'.format(v=val)
        return my_format

    # Plot
    fig, ax = plt.subplots(figsize=(5, 4))

    ax.pie(values, 
        labels=labels, 
        colors = mycolors, 
        autopct = autopct_format(values), 
        pctdistance=0.8,
        textprops={'fontsize': 10, 'color': 'black', 'family': 'Montserrat'})
    plt.title(f"{timeframe} Expense Pie Chart for\nReport #{report_id} : {report_name}\n", fontsize=14, fontweight="bold", ha="center")

    centre_circle = plt.Circle((0, 0), 0.60, fc="white")
    ax.add_artist(centre_circle)

    # Ensure the pie remains circular
    ax.axis("equal")

    # Adjust layout for better centering
    fig.tight_layout()

    # Save the figure (Ensuring all elements fit properly)
    plt.savefig("figure.png", bbox_inches='tight')

    plt.close()
