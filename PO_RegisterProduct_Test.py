from customtkinter import *
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox, ttk
from datetime import datetime
from tkcalendar import DateEntry
import openpyxl
from openpyxl import Workbook
import os
import uuid
import sqlite3

file_name = "ProductRecords.xlsx"  # Excel file path


class ProductRegistration(CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(width=1920, height=1080)

        # Variables
        self.productName_var = tk.StringVar()
        self.description_var = tk.StringVar()
        self.testingDate_var = tk.StringVar()
        self.maturityDate_var = tk.StringVar()

        # Build UI
        self.build_ui()

    def build_ui(self):
        # Product Details Frame

        # Sidebar
        self.product_frame = CTkFrame(self, fg_color="#FCEBEB", width=1000, height=300, corner_radius=20)
        self.product_frame.place(x=100, y=150)
        self.product_frame.pack_propagate(False)

        CTkLabel(self.product_frame, text="Product Details", font=("Arial", 25, "bold"), text_color="#5B3E2B").place(x=20, y=30)
        CTkLabel(self.product_frame, text="Product Name:", font=("Arial", 16)).place(x=20, y=80)
        CTkEntry(self.product_frame, width=800, height=30, textvariable=self.productName_var).place(x=150, y=80)

        CTkLabel(self.product_frame, text="Description:", font=("Arial", 16)).place(x=20, y=140)
        CTkEntry(self.product_frame, width=800, height=100, textvariable=self.description_var).place(x=150, y=140)

        # Date Frame
        self.date_frame = CTkFrame(self, fg_color="#F0EFF8", width=1000, height=250, corner_radius=20)
        self.date_frame.place(x=100, y=490)
        self.date_frame.pack_propagate(False)

        CTkLabel(self.date_frame, text="Date Selection", font=("Arial", 25, "bold"), text_color="#5B3E2B").place(x=20, y=30)

        CTkLabel(self.date_frame, text="Testing Date:", font=("Arial", 16)).place(x=20, y=80)
        self.testing_date_entry = DateEntry(self.date_frame, width=18, background='pink', foreground='white', borderwidth=2, textvariable=self.testingDate_var)
        self.testing_date_entry.place(x=150, y=80)

        CTkLabel(self.date_frame, text="Maturity Date:", font=("Arial", 16)).place(x=20, y=130)
        self.maturity_date_entry = DateEntry(self.date_frame, width=18, background='pink', foreground='white', borderwidth=2, textvariable=self.maturityDate_var)
        self.maturity_date_entry.place(x=150, y=130)

        # Save Button
        CTkButton(self.date_frame, text="Save Product", command=self.save_data, font=("Arial", 18), fg_color="#95d194", hover_color="#FDC09A").place(x=550, y=180)
        #Clear Button
        CTkButton(self.date_frame, text="Clear Form", command=self.clear_form, font=("Arial", 18),fg_color="#f16c6c", hover_color="#FDC09A").place(x=800,y=180)

    def save_data(self):
        productName = self.productName_var.get()
        description = self.description_var.get()
        testingDate = self.testingDate_var.get()
        maturityDate = self.maturityDate_var.get()

        if not productName or not description or not testingDate or not maturityDate:
            messagebox.showerror("Error", "All fields are required!")
            return

        submissionDate = datetime.now().strftime("%Y-%m-%d")
        batch_id = str(uuid.uuid4())[:8]
        test_completed = "No"
        test_id = str(uuid.uuid4())[:8]
        date_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        updated_by = "System"

        base_directory = "TestResults"
        batch_directory = os.path.join(base_directory, submissionDate, batch_id)
        os.makedirs(batch_directory, exist_ok=True)
        testResultLocation = os.path.join(batch_directory, f"{productName}_results.txt")

        # Save to Excel
        if not os.path.exists(file_name):
            wb = Workbook()
            ws = wb.active
            ws.append(["Batch ID", "Product Name", "Description", "Submission Date", "Testing Date",
                       "Maturity Date", "Test Completed", "Test ID", "Test Result Location", "Date Updated", "Updated By"])
        else:
            wb = openpyxl.load_workbook(file_name)
            ws = wb.active

        ws.append([batch_id, productName, description, submissionDate, testingDate, maturityDate,
                   test_completed, test_id, testResultLocation, date_updated, updated_by])
        wb.save(file_name)

        # Save to SQLite
        try:
            conn = sqlite3.connect('ProductRegistration.db')
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS products (
                    batch_id TEXT, product_name TEXT, description TEXT, submission_date TEXT,
                    testing_date TEXT, maturity_date TEXT, test_completed TEXT, test_id TEXT,
                    test_result_location TEXT, date_updated TEXT, updated_by TEXT
                )
            ''')

            cursor.execute('''
                INSERT INTO products (
                    batch_id, product_name, description, submission_date,
                    testing_date, maturity_date, test_completed, test_id,
                    test_result_location, date_updated, updated_by
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (batch_id, productName, description, submissionDate, testingDate,
                  maturityDate, test_completed, test_id, testResultLocation, date_updated, updated_by))

            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred while saving to database:\n{e}")
            return

        messagebox.showinfo("Success", f"Product saved!\nResult location:\n{testResultLocation}")
        self.clear_form()

    def clear_form(self):
        self.productName_var.set("")
        self.description_var.set("")
        self.testingDate_var.set("")
        self.maturityDate_var.set("")

#Create an instance of the ProductRegistration class
#The ProductRegistration frame is created, however it's not attached to any parent window. We need to start the driver program to see the GUI. 
#We need to start the main event loop and create a parent window to see the GUI.
'''
obj = ProductRegistration(None, None)
'''

if __name__ == "__main__":
    app = CTk()  # Create the root window
    app.geometry("1200x800")  # Set desired size
    app.title("Product Registration")

    # Create and pack the frame into the window
    product_page = ProductRegistration(app, None)
    product_page.pack(fill="both", expand=True)

    app.mainloop()  # Start the main loop
