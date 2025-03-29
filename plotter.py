import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Function for getting data from Database
def fetch_data(timeframe, report_id, report_name):

    # Declaring target table
    targetTable = f"Expenses_Report_{report_id}"

    # """Fetch expense data based on the selected timeframe."""
    conn = sqlite3.connect("expense_tracker.db")  # Adjust to your DB file
    cursor = conn.cursor()

    # SQL query based on timeframe
    if timeframe == "Daily":
        cursor.execute(f"SELECT category, SUM(amount) FROM {targetTable} WHERE date = DATE('now') GROUP BY category")
    elif timeframe == "Weekly":
        cursor.execute(f"SELECT category, SUM(amount) FROM {targetTable} WHERE date BETWEEN DATE('now', '-6 days') AND DATE('now') GROUP BY category")
    elif timeframe == "Monthly":
        cursor.execute(f"SELECT category, SUM(amount) FROM {targetTable} WHERE date BETWEEN DATE('now', '-29 days') AND DATE('now') GROUP BY category")

    data = cursor.fetchall()
    conn.close()

    # Call function to Write the CSV File
    write_data(data)

    # Call function to generate the pie chart
    create_chart(timeframe, report_id, report_name)
    
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
