from datetime import datetime, timedelta
import random
import sqlite3 as sql
 
# # ORDERED DATES
# def generate_last_30_days():
#     """Generates a list of the last 30 days in YYYY-MM-DD format."""
#     last_30_days = []
#     today = datetime.today()
    
#     for i in range(30):
#         date = today - timedelta(days=i)
#         last_30_days.append(date.strftime("%Y-%m-%d"))
    
#     return last_30_days

# # Example usage:
# dates = generate_last_30_days()
# print(dates)

# RANDOM DATES
def generate_dates():
    last_30_days = [(datetime.today() - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(30)]
    chosen_dates = random.choices(last_30_days, k=35)  # Some dates appear more frequently
    return chosen_dates[:30]  # Ensure only 30 dates are returned

dates = generate_dates()
# print(dates)  # Check frequency distribution

def generate_random_categories():
    """Generates a list of 30 random expense categories."""
    categories = ["Travel", "Food", "Clothes", "Bills", "Health", "Personal"]
    random_categories = [random.choice(categories) for _ in range(30)]
    return random_categories

# Example usage:
random_expenses = generate_random_categories()
# print()
# print()
# print()
# print()
# print(random_expenses)  # Prints a list of 30 random categories

def generate_expenses_with_intervals():
    """Generates a list of 30 random expense amounts between 200 and 1000 with intervals of 50 or 150."""
    possible_values = [x for x in range(200, 1050, 50)] + [x for x in range(200, 1150, 150)]
    unique_values = sorted(set(possible_values))  # Remove duplicates and sort

    return [random.choice(unique_values) for _ in range(30)]

# Example usage:
expense_values = generate_expenses_with_intervals()
# print()
# print()
# print(expense_values)  # Prints a list of 30 random values with specified intervals

# for i in range(30):
#     print(f"ID: {i+1} | Date: {dates[i]} | Categories: {random_expenses[i]} | Amount: {expense_values[i]}" )

conn = sql.connect("expense_tracker.db")
cursor = conn.cursor()

for i in range(30):
    cursor.execute("INSERT INTO Expenses_Report_3 (expense_id, date, category, amount) VALUES (?, ?, ?, ?)", (i + 1, dates[i], random_expenses[i], expense_values[i]))
    print("Inserted")

conn.commit()
conn.close()