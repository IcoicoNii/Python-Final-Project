import tkinter as tk
from tkinter import CENTER, simpledialog, messagebox, PhotoImage, ttk, font
from PIL import Image, ImageTk
import expenseTrackerAppdb as db
import re
import plotter
import datetime

class ExpenseTrackerApp:
    # MAIN WINDOW
    def __init__(self, root):
        # WINDOW
        self.root = root
        self.root.title("Expense Tracker App")
        self.root.geometry("800x500+400+300")
        self.root.configure(bg = "#283618")
        
        # FRAME FOR ALL TO CENTER EVERYTHING
        self.frame = tk.Frame(root, bg = "#283618")
        self.frame.pack(expand=True)

        # MAIN TITLE
        self.mainTitleImg = PhotoImage(file = "mainWindowTitle.png")
        self.maintitle = tk.Label(self.frame, image = self.mainTitleImg, bg = "#283618")
        self.maintitle.pack(pady=20)

        # START TRACKING BUTTON
        self.startButtonImg = PhotoImage(file = "./buttons/startTrackingBtn.png")
        self.button1 = tk.Button(self.frame, image = self.startButtonImg, command=self.dashboard, bg = "#283618")
        self.button1.pack(pady=5)

        # QUIT BUTTON
        self.quitButtonImg = PhotoImage(file = "./buttons/quitBtn.png")        
        self.button2 = tk.Button(self.frame, image = self.quitButtonImg, command=self.quit_program, bg = "#283618")
        self.button2.pack(pady=5)

        # CALL CENTER FUNCTION
        self.center_window(self.root)

    # TO CENTER THE WINDOW CONTENT
    def center_window(self, window):
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")

    # TO SHOW DASHBOARD WINDOW
    def dashboard(self):
        # DASHBOARD WINDOW
        self.root.withdraw()
        self.new_window = tk.Toplevel()
        self.new_window.title("Dashboard")
        self.new_window.geometry("800x500")
        self.new_window.configure(bg = "#283618")
        
        # FRAME FOR ALL
        frame = tk.Frame(self.new_window, bg = "#283618")
        frame.pack(expand=True)
        
        #BACK TO MAIN WINDOW
        self.backmenuBtnImg = PhotoImage(file = "./buttons/backMenuBtn.png")
        back_button = tk.Button(self.new_window, image = self.backmenuBtnImg, command=self.back_to_main, bg = "#606c38")
        back_button.place(relx=0.05, rely=0.05, anchor="nw")

        # TITLE
        self.dashTitle = PhotoImage(file = "dashboardTitle.png")
        title_label = tk.Label(frame, image = self.dashTitle, bg = "#283618")
        title_label.pack(pady=5)

        # LISTBOX WITH COLUMNS
        tree_frame = tk.Frame(frame, bg = "#283618")
        tree_frame.pack(pady=10)
        
        # CONFIGURE THE STYLE OF HEADING IN TREEVIEW WIDGET
        s = ttk.Style()
        s.theme_use('clam')
        s.configure('Treeview.Heading', background="#606c38", font=('Montserrat', 12, 'bold'), foreground = "#fefae0")
        s.configure('Treeview', rowheight=40, font=('Montserrat', 12))

        # DECLARE TREEVIEW (Instead of Listbox in order to have headings and columns)
        self.tree = ttk.Treeview(tree_frame, columns=("Report No.", "Name", "Total Expense"), show="headings", height=5)
        self.tree.heading("Report No.", text="Report No.")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Total Expense", text="Total Expense")
        self.tree.column("Report No.", width=100, anchor=tk.CENTER)
        self.tree.column("Name", width=200, anchor=tk.CENTER)
        self.tree.column("Total Expense", width=150, anchor=tk.E)
        self.tree.pack()
        
        # BIND COMMAND TO OPEN THE SELECTED REPORT
        self.tree.bind("<Double-1>", self.open_report_window)

        # TO DISPLAY FETCHED REPORTS
        reportsToDisplay = db.get_all_reports()
        for list in reportsToDisplay:
            self.tree.insert("", tk.END, values=(list[0] ,list[1] ,float(list[2]),))

        # BUTTONS
        button_frame = tk.Frame(frame,bg = "#283618")
        button_frame.pack() 

        # ADD REPORT BUTTON
        self.addReportBtnImg = PhotoImage(file = "./buttons/addReportBtn.png")
        addReport_button = tk.Button(button_frame, image = self.addReportBtnImg, command=self.add_report, bg = "#606c38")
        addReport_button.pack(side=tk.LEFT, padx=5)
        
        # REMOVE REPORT BUTTON
        self.removeReportBtnImg = PhotoImage(file = "./buttons/removeReportBtn.png")
        removeReport_button = tk.Button(button_frame, image = self.removeReportBtnImg, command=self.remove_report, bg = "#606c38")
        removeReport_button.pack(side=tk.LEFT, padx=5)

        # CALL CENTER FUNCTION
        self.center_window(self.new_window)

    # ADD REPORT FUNCTION
    def add_report(self):
        # ASK FOR REPORT NAME
        report_name = simpledialog.askstring("Add Report", "Enter report name:")
        
        # SHOW REPORT ON THE TREEVIEW
        if report_name:
            report_no = len(self.tree.get_children()) + 1
            total_expense = 0.00

            # ENSURE REPORT_NO IS UNIQUE BY INCREMENTING IF NECESSARY
            while db.report_exists(report_no):  
                report_no += 1  

            # Add the report to the database
            db.add_report_to_db(report_no, report_name, total_expense)

            # Insert into the UI tree
            self.tree.insert("", tk.END, values=(report_no, report_name, total_expense))
    
    # REMOVE REPORT FUNCTION
    def remove_report(self):
        # ASSIGN SELECTED TO A VARIABLE
        selected = self.tree.selection()

        # Check if there's a selected, otherwise return warning
        if not selected:
            messagebox.showwarning("No Selection", "Please select a report to delete.")
            return

        # Ask for confirmation
        confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete the selected report(s)?")
        if not confirm:
            return  # Exit if user cancels

        # List for report_nos to be removed to pass on database
        removed_report_nos = []

        # Get the values inside the selected and remove them from the treeview UI
        for item in selected:
            values = self.tree.item(item, "values")  # Get report details
            if values:
                removed_report_nos.append(values[0])  # Store only report_no

            self.tree.delete(item)

        # Remove each report from the database
        for report_no in removed_report_nos:
            db.delete_report(report_no)

    # GO BACK TO MAIN WINDOW FUNCTION
    def back_to_main(self):
        self.new_window.destroy()
        self.root.deiconify()

    # QUIT THE PROGRAM
    def quit_program(self):
        self.root.quit()

    # OPENED REPORT WINDOW
    def open_report_window(self, event):
        # ASSIGN SELECTED TO A VARIABLE
        selected_item = self.tree.selection()

        if selected_item:
            # Declare initial variables
            self.report_values = self.tree.item(selected_item, "values")
            report_no = self.report_values[0]
            report_name = self.report_values[1]
            self.new_window.withdraw()
            
            # Opened Report Window
            report_window = tk.Toplevel()
            report_window.title(f"Report #{report_no} : {report_name}")
            report_window.geometry("800x500")
            report_window.configure(bg = "#283618")

            # FRAME FOR ALL
            container = tk.Frame(report_window, bg = "#283618")
            container.pack(expand=True)

            # BACK TO DASHBOARD BUTTON
            self.backDashboardBtnImg = PhotoImage(file="./buttons/backDashboardBtn.png")
            back_dashboard_button = tk.Button(report_window, image=self.backDashboardBtnImg, command=lambda: self.back_to_dashboard(report_window), bg = "#606c38")
            back_dashboard_button.place(relx = 0.05, rely = 0.05)

            # REPORT LABELS
            reportNoLabel = tk.Label(report_window, text = f"REPORT #{report_no}", font = ("Space Mono", 16, "normal"), bg = "#283618", fg = "#dda15e")
            reportNoLabel.place(relx=0.5,rely = 0.13, anchor = tk.CENTER)

            #TITLE FRAME
            title_frame = tk.Frame(container, bg = "#283618")
            title_frame.pack()

            # TITLE
            self.reportNameLabel = tk.Label(title_frame, text = f"{report_name.upper()}", font = ("Montserrat", 32, "bold"), bg = "#283618", fg = "#fefae0")
            self.reportNameLabel.grid(row=0, column=0)

            # EDIT BUTTON
            self.editReportNameBtnImg = PhotoImage(file="./buttons/editReportBtn.png")
            editReportNameBtnImg = tk.Button(title_frame, image = self.editReportNameBtnImg, command = lambda:self.changeReportName(self.report_values[0]), bg = "#606c38")
            editReportNameBtnImg.grid(row = 0, column = 1, padx = 10)

            # TREE FRAME
            tree_frame = tk.Frame(container)
            tree_frame.pack(pady=0)
        
            # DECLARE TREEVIEW (Instead of Listbox in order to have headings and columns)
            self.expense_tree = ttk.Treeview(tree_frame, columns=("Expense No.","Date", "Category", "Amount"), show="headings", height=5)

            # Define a tag with a different background color
            self.expense_tree.tag_configure("new_entry", background="#ffd6a8") # COLOR OF THE NEW INSERTED ENTRY
            
            self.expense_tree.heading("Expense No.", text="Expense No. ▲▼", command=lambda: self.sort_treeview("Expense No."))
            self.expense_tree.heading("Date", text="Date ▲▼", command=lambda: self.sort_treeview("Date"))
            self.expense_tree.heading("Category", text="Category ▲▼", command=lambda: self.sort_treeview("Category"))
            self.expense_tree.heading("Amount", text="Amount ▲▼", command=lambda: self.sort_treeview("Amount"))
            
            self.expense_tree.column("Expense No.", width=150, anchor=tk.CENTER)
            self.expense_tree.column("Date", width=110, anchor=tk.CENTER)
            self.expense_tree.column("Category", width=120, anchor=tk.CENTER)
            self.expense_tree.column("Amount", width=130, anchor=tk.CENTER)
            self.expense_tree.pack()

            # To display fetched reports
            expensesToDisplay = db.get_expenses_for_report(report_no)
            # print(expensesToDisplay)
            for list in expensesToDisplay:
                self.expense_tree.insert("", tk.END, values=(list[0], list[1] ,list[2] , list[3]))

            # BUTTONS FRAME
            button_frame = tk.Frame(container, bg = "#283618")
            button_frame.pack(pady=10)

            # ADD EXPENSE BUTTON
            self.addExpenseButtonImg = PhotoImage(file="./buttons/addExpenseBtn.png")
            add_button = tk.Button(button_frame, image=self.addExpenseButtonImg, command=self.add_expense, bg = "#606c38")
            add_button.pack(side=tk.LEFT, padx=5)

            # REMOVE EXPENSE BUTTON
            self.removeExpenseButtonImg = PhotoImage(file="./buttons/removeExpenseBtn.png")
            remove_button = tk.Button(button_frame, image=self.removeExpenseButtonImg, command = self.remove_expense, bg = "#606c38")
            remove_button.pack(side=tk.LEFT, padx=5)
            
            # SHOW GRAPH BUTTON
            self.showGraphImg = PhotoImage(file = './buttons/showGraphBtn.png')
            graph_button = tk.Button(button_frame, image = self.showGraphImg, command = self.show_graph, bg = "#606c38")
            graph_button.pack(side = tk.LEFT, padx=5)

            # BIND A COMMAND TO THE SELECTED TO UPDATE THE EXPENSE
            self.expense_tree.bind("<Double-1>", self.update_expense)

            # CALL CENTER FUNCTION
            self.center_window(report_window)
    

    # FUNCTION TO SORT THE CONTENT OF EXPENSE REPORTS
    def sort_treeview(self, col, reverse=False):
        """Sort treeview column when clicked on the heading."""
        data = [(self.expense_tree.set(item, col), item) for item in self.expense_tree.get_children("")]
        
        # Try to sort numerically, if applicable
        try:
            data.sort(key=lambda x: float(x[0]), reverse=reverse)
        except ValueError:
            data.sort(reverse=reverse)

        # Rearrange items in sorted order
        for index, (val, item) in enumerate(data):
            self.expense_tree.move(item, '', index)

        # Toggle sort order for next click
        self.expense_tree.heading(col, command=lambda: self.sort_treeview(col, not reverse))

    # FUNCTION TO CHANGE REPORT NAME
    def changeReportName(self, report_id):
        changed_name = simpledialog.askstring("Change Report Name", "Change Report Name to:")
        if changed_name:  # Ensure it's not None (user didn't cancel)
            db.changeReportName(report_id, changed_name)
            self.reportNameLabel.config(text=changed_name.upper())

    # SHOW GRAPH FUNCTION
    def show_graph(self):
        # SHOW GRAPH WINDOW
        graph_window = tk.Toplevel(self.root)
        graph_window.title("Expense Graph")
        graph_window.geometry("800x500")
        graph_window.configure(bg = "#283618")

        # FRAME FOR ALL
        container = tk.Frame(graph_window, bg = "#283618")
        container.pack(expand=True)
        
        # REPORT LABELS
        report_label = tk.Label(container, text="Expense Pie Chart Figure for", font=("Space Mono", 14, 'bold'), bg = "#283618", fg = '#dda15e')
        report_label.pack()

        report_name_label = tk.Label(container, text = f"{self.report_values[1].upper()}", font=("Montserrat", 32, 'bold'), bg = "#283618", fg = "#fefae0")
        report_name_label.pack()

        # TRY TO LOAD A PLACEHOLDER IMAGE
        try:
            placeholder_img = Image.open("placeholder.png")  # Ensure you have a placeholder image
            placeholder_img = placeholder_img.resize((400, 300), Image.LANCZOS)
            self.img = ImageTk.PhotoImage(placeholder_img)
        except Exception as e:
            self.img = None  # If placeholder not found, set to None

        # Create a frame to hold the figure with placeholder
        self.figure_label = tk.Label(container, image=self.img, bg="#283618")
        self.figure_label.pack(expand=True, pady=5)

        # BUTTONS FRAME
        button_frame = tk.Frame(container, bg="#283618")
        button_frame.pack(pady=5)

        def update_graph(timeframe):
            # Fetch data first
            data = plotter.fetch_data(timeframe, self.report_values[0], self.report_values[1])  
            
            # If no data is found, show alert and stop execution
            if not data:
                return  # Exit the function early

            # UPDATE THE IMAGE ON THE OPENED GRAPH WINDOW
            try:
                img = Image.open('figure.png')
                img = img.resize((400, 300), Image.LANCZOS)
                self.img = ImageTk.PhotoImage(img)  # Keep a reference to prevent garbage collection

                self.figure_label.configure(image=self.img)  # Update the displayed image
                self.figure_label.image = self.img  # Keep reference

            except Exception as e:
                self.figure_label.configure(text="Error loading image", image=None)


        # TIMELINE BUTTONS
        # DAILY BUTTON
        self.dailyButtonImg = PhotoImage(file = "./buttons/dailyBtn.png")
        dailyBtn = tk.Button(button_frame, image = self.dailyButtonImg, bg = "#606c38", command= lambda: update_graph("Daily"))
        dailyBtn.grid(row=0, column=0, padx = 3)

        # WEEKLY BUTTON
        self.weeklyButtonImg = PhotoImage(file = "./buttons/weeklyBtn.png")
        weeklyBtn = tk.Button(button_frame, image = self.weeklyButtonImg, bg = "#606c38", command= lambda: update_graph("Weekly"))
        weeklyBtn.grid(row=0, column=1, padx = 3)

        # MONTHLY BUTTON
        self.monthlyButtonImg = PhotoImage(file = "./buttons/monthlyBtn.png")
        monthlyBtn = tk.Button(button_frame, image = self.monthlyButtonImg, bg = "#606c38", command= lambda: update_graph("Monthly"))
        monthlyBtn.grid(row=0, column=2, padx = 3)

        # CALL CENTER FUNCTION
        self.center_window(graph_window)
        
    # ADD EXPENSE FUNCTION WITH CENTERED CONTENT
    def add_expense(self):
        # ADD EXPENSE WINDOW
        add_expense_window = tk.Toplevel()
        add_expense_window.title("Add Expense")
        add_expense_window.geometry("400x300")
        add_expense_window.configure(bg = "#283618")

        # FRAME FOR ALL
        container = tk.Frame(add_expense_window, bg = "#283618")
        container.pack(expand=True)

        # ADD EXPENSE WINDOW LABELS
        tk.Label(container, text="Add Expense for", font=('Space Mono', 12, 'bold'), bg = "#283618", fg = "#dda15e").pack()
        tk.Label(container, text=f"{self.report_values[1].upper()}", font=('Montserrat', 24, 'bold'), bg = "#283618", fg = "#fefae0").pack()
        
        # FRAME FOR THE CONTENT
        frame = tk.Frame(container, bg = "#283618")
        frame.pack(pady=10)
        
        # DECLARE ENTRY WIDTH FOR NUMBER OF CHARACTERS USER CAN INPUT
        entry_width = 20
        
        # DATE ENTRY
        tk.Label(frame, text="Date (YYYY-MM-DD):", bg = "#283618", font = ("Montserrat", 10), fg = "#fefae0").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        date_entry = tk.Entry(frame, width=entry_width, justify="center")
        date_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # CATEGORY ENTRY
        tk.Label(frame, text="Category:", bg="#283618", font=("Montserrat", 10), fg="#fefae0").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        category_var = tk.StringVar()
        category_dropdown = ttk.Combobox(frame, textvariable=category_var, values=["Travel", "Food", "Clothes", "Bills", "Health", "Personal"], width=entry_width - 2, state="readonly")
        category_dropdown.grid(row=1, column=1, padx=5, pady=5)

        # AMOUNT
        tk.Label(frame, text="Amount:", bg = "#283618", font = ("Montserrat", 10), fg = "#fefae0").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        amount_entry = tk.Entry(frame, width=entry_width, justify="center")
        amount_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # SAVE EXPENSE FUNCTION
        def save_expense():
            # GET VALUES FROM THE ENTRIES
            date = date_entry.get()
            category = category_var.get()
            amount = amount_entry.get()

            # Validate date format (YYYY-MM-DD)
            date_pattern = r"^\d{4}-\d{2}-\d{2}$"
            if not re.match(date_pattern, date):
                messagebox.showwarning("Input Error", "Date must be in YYYY-MM-DD format.")
                return

            # Validate that the date is not in the future
            today = datetime.date.today()
            try:
                entered_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
                if entered_date > today:
                    messagebox.showwarning("Input Error", "Date cannot be later than today.")
                    return
            except ValueError:
                messagebox.showwarning("Input Error", "Invalid date entered.")
                return

            # Validate amount (must be a float)
            try:
                amount = float(amount)
            except ValueError:
                messagebox.showwarning("Input Error", "Amount must be a valid number.")
                return

            # RECORD TO THE DATABASE
            if date and category and amount:
                latest_expense_no = db.get_latest_id(self.report_values[0])  # Get max ID
                expense_no = latest_expense_no + 1  # Always starts at 1 if no expenses exist
                
                db.add_expense_to_db(expense_no, self.report_values[0], date, category, amount)
                self.expense_tree.insert("", 0, values=(expense_no, date, category, amount), tags=("new_entry",))
                add_expense_window.destroy()
            else:
                messagebox.showwarning("Input Error", "All fields must be filled!")
            

        # SAVE BUTTON
        self.saveBtnImg = tk.PhotoImage(file="./buttons/saveExpenseBtn.png")
        save_button = tk.Button(container, image=self.saveBtnImg, command=save_expense, bg = "#606c38")
        save_button.pack(pady=10)
        
        # UPDATE TOTAL EXPENSES
        db.update_total_expense(self.report_values[0])
        
        # CALL CENTER FUNCTION
        self.center_window(add_expense_window)

    # REMOVE EXPENSE FUNCTION
    def remove_expense(self):
        selected = self.expense_tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select an expense to delete.")
            return

        # Ask for confirmation
        confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete the selected expense(s)?")
        if not confirm:
            return  # Exit if user cancels

        # DECLARE A LIST FOR REMOVED EXPENSES ID FOR DATABASE PURPOSE
        removed_expense_nos = []

        # GET VALUES ON THE SELECTED AND DELETE THE SELECTED ON THE TREEVIEW UI
        for item in selected:
            values = self.expense_tree.item(item, "values")  # Get expense details
            if values:
                removed_expense_nos.append(values[0])  # Store only expense_no

            self.expense_tree.delete(item)


        print(removed_expense_nos)

        # Remove each expense from the database
        for expense_no in removed_expense_nos:
            db.delete_expense(self.report_values[0], expense_no)
        
        # UPDATE THE TOTAL EXPENSE ON THE REPORT FROM THE DATABASE
        db.update_total_expense(self.report_values[0])

    
    # BACK TO DASHBOARD FUNCTION
    def back_to_dashboard(self, report_window):
        report_window.destroy()
        self.new_window.deiconify()
        self.center_window(self.new_window)

        # UPDATE TOTAL EXPENSE SO THAT DASHBOARDS ARE REAL TIME
        db.update_total_expense(self.report_values[0])

        # Clear the tree before inserting new values
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Fetch and display updated reports
        reportsToDisplay = db.get_all_reports()

        # print(reportsToDisplay)
        for report in reportsToDisplay:
            self.tree.insert("", tk.END, values=(report[0], report[1], report[2]))

    # UPDATE EXPENSE FUNCTION
    def update_expense(self, event):
        # GET THE SELECTED ITEM
        selected_item = self.expense_tree.selection()
        
        # IF NO SELECTION IS MADE, RETURN
        if not selected_item:
            return

        # SET VARIABLES
        values = self.expense_tree.item(selected_item, "values")
        if not values:
            return

        # UPDATE EXPENSE WINDOW
        update_expense_window = tk.Toplevel()
        update_expense_window.title("Update Expense")
        update_expense_window.geometry("400x300")
        update_expense_window.configure(bg = "#283618")

        # FRAME FOR ALL
        container = tk.Frame(update_expense_window, bg = "#283618")
        container.pack(expand=True)

        # EXPENSE LABELS
        tk.Label(container, text="Update Expense for", font=('Space Mono', 12, 'bold'), bg = "#283618", fg = "#dda15e").pack()
        tk.Label(container, text=f"{self.report_values[1].upper()}", font=('Montserrat', 24, 'bold'), bg = "#283618", fg = "#fefae0").pack()
        
        # FRAME FOR THE CONTENT
        frame = tk.Frame(container, bg = "#283618")
        frame.pack(pady=10)
        
        # SET ENTRY WIDTH --- NUMBER OF CHARACTERS USER CAN INPUT
        entry_width = 20
        
        # DATE ENTRY
        tk.Label(frame, text="Date (YYYY-MM-DD):", bg = "#283618", font = ("Montserrat", 10), fg = "#fefae0").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        date_entry = tk.Entry(frame, width=entry_width, justify="center")
        date_entry.insert(0, values[1])
        date_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # CATEGORY ENTRY
        tk.Label(frame, text="Category:", bg = "#283618", font = ("Montserrat", 10), fg = "#fefae0").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        category_var = tk.StringVar()
        category_dropdown = ttk.Combobox(frame, textvariable=category_var, values=["Travel", "Food", "Clothes", "Bills", "Health", "Personal"], width=entry_width - 2, state="readonly")
        category_dropdown.set(values[2])
        category_dropdown.grid(row=1, column=1, padx=5, pady=5)
        
        # AMOUNT ENTRY
        tk.Label(frame, text="Amount:", bg = "#283618", font = ("Montserrat", 10), fg = "#fefae0").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        amount_entry = tk.Entry(frame, width=entry_width, justify="center")
        amount_entry.insert(0, values[3])
        amount_entry.grid(row=2, column=1, padx=5, pady=5)
                
        # SAVE UPDATE FUNCTION
        def save_update():
            # GET VALUES FROM THE ENTRIES
            new_date = date_entry.get()
            new_category = category_var.get()
            new_amount = amount_entry.get()

            # Validate date format (YYYY-MM-DD)
            date_pattern = r"^\d{4}-\d{2}-\d{2}$"
            if not re.match(date_pattern, new_date):
                messagebox.showwarning("Input Error", "Date must be in YYYY-MM-DD format.")
                return

            # Validate that the date is not in the future
            today = datetime.date.today()
            try:
                entered_date = datetime.datetime.strptime(new_date, "%Y-%m-%d").date()
                if entered_date > today:
                    messagebox.showwarning("Input Error", "Date cannot be later than today.")
                    return
            except ValueError:
                messagebox.showwarning("Input Error", "Invalid date entered.")
                return

            # Validate amount (must be a float)
            try:
                new_amount = float(new_amount)
            except ValueError:
                messagebox.showwarning("Input Error", "Amount must be a valid number.")
                return

            # GET THE CURRENT SELECTION
            selected_items = self.expense_tree.selection()  # Returns a tuple of selected item IDs

            # Ensure something is selected
            if not selected_items:
                messagebox.showwarning("Selection Error", "No expense selected for updating.")
                return

            selected_item = selected_items[0]  # Get first selected item

            # Extract values from the selected row
            values = self.expense_tree.item(selected_item, "values")

            if values:
                expense_no = values[0]  # Extract expense_no from the selected row

                # Update the Treeview with new values
                self.expense_tree.item(selected_item, values=(expense_no, new_date, new_category, new_amount))

                # Update the database
                db.update_expense_to_db(expense_no, self.report_values[0], new_date, new_category, new_amount)

                # Close the update expense window
                update_expense_window.destroy()

                # Update total expense in the database
                db.update_total_expense(self.report_values[0])
            else:
                messagebox.showwarning("Selection Error", "Selected item does not exist.")

        # SAVE BUTTON
        self.saveBtnImg = tk.PhotoImage(file="./buttons/saveExpenseBtn.png")
        save_button = tk.Button(container, image=self.saveBtnImg, command=save_update)
        save_button.pack(pady=10)
        
        # CALL CENTER FUNCTION
        self.center_window(update_expense_window)


# RUN THE PROGRAM
if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()