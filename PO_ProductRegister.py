from customtkinter import *
import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
import openpyxl
from openpyxl import Workbook
import os
from datetime import datetime
import uuid
import sqlite3

# Database setup
def setup_database():
    # Create a database connection and cursor
    conn = sqlite3.connect('ProductRegistration.db') 
    cursor = conn.cursor()

    try:
        # Create a table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                batch_id TEXT NOT NULL,
                product_name TEXT NOT NULL,
                description TEXT,
                submission_date TEXT DEFAULT CURRENT_TIMESTAMP,
                testing_date TEXT NOT NULL,
                maturity_date TEXT NOT NULL,
                test_completed TEXT DEFAULT 'No',
                test_id TEXT,
                test_result_location TEXT,
                date_updated TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_by TEXT,
                owner_id INTEGER,
                approved TEXT DEFAULT 'No',
                FOREIGN KEY (owner_id) REFERENCES product_owners(owner_id)
            )
        ''')
        
        conn.commit()

    except sqlite3.Error as e:
        print(f"Error creating table: {e}")
        
    finally:
        cursor.close()
        conn.close()

setup_database()

class ProductRegistrationPage(CTkFrame):
    def __init__(self, parent, controller, owner_id=None):
        super().__init__(parent)
        self.controller = controller
        self.owner_id = owner_id
        self.configure(width=1920, height=1080)
        self.place(x=0, y=0)

        # Initialize variables
        self.productName_var = tk.StringVar()
        self.description_var = tk.StringVar()
        self.testingDate_var = tk.StringVar()
        self.maturityDate_var = tk.StringVar()
        
        # Excel file setup
        self.file_name = "productData.xlsx"
        
        if not os.path.exists(self.file_name):
            wb = Workbook()
            ws = wb.active
            ws.append(["Batch_ID", "Product Name", "Description", "Submission Date", 
                      "Testing Date", "Maturity Date", "Test Completed", "Test_ID", 
                      "Test Result Location", "Date Updated", "Updated By"])  # Header
            wb.save(self.file_name)
            
        self.build_ui()

    def save_data(self):
        productName = self.productName_var.get()
        description = self.description_var.get()
        testingDate = self.testingDate_var.get()
        maturityDate = self.maturityDate_var.get()

        if not productName or not description or not testingDate or not maturityDate:
            messagebox.showerror("Error", "All fields except Submission Date are required!")
            return

        # Automatically set Submission Date to today's date
        submissionDate = datetime.now().strftime("%Y-%m-%d")

        # Automatically generate additional fields
        batch_id = str(uuid.uuid4())[:8]  # Generate a unique Batch_ID
        test_completed = "No"  # Default value
        test_id = str(uuid.uuid4())[:8]  # Generate a unique Test_ID
        date_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Current timestamp
        updated_by = "System"  # Default value for 'By'

        # Generate the test result location dynamically
        base_directory = "TestResults"
        batch_directory = os.path.join(base_directory, submissionDate, batch_id)
        os.makedirs(batch_directory, exist_ok=True)  # Create directories if they don't exist
        testResultLocation = os.path.join(batch_directory, f"{productName}_results.txt")

        # Save data to Excel
        wb = openpyxl.load_workbook(self.file_name)
        ws = wb.active
        ws.append([batch_id, productName, description, submissionDate, testingDate, 
                  maturityDate, test_completed, test_id, testResultLocation, 
                  date_updated, updated_by])  # Append data
        wb.save(self.file_name)

        # Save data to SQLite database
        try:
            conn = sqlite3.connect('ProductRegistration.db')
            cursor = conn.cursor()

            # Check if the table exists, if not create it
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    batch_id TEXT NOT NULL,
                    product_name TEXT NOT NULL,
                    description TEXT,
                    submission_date TEXT,
                    testing_date TEXT NOT NULL,
                    maturity_date TEXT NOT NULL,
                    test_completed TEXT DEFAULT 'No',
                    test_id TEXT,
                    test_result_location TEXT,
                    date_updated TEXT,
                    updated_by TEXT,
                    owner_id INTEGER,
                    approved TEXT DEFAULT 'No',
                    FOREIGN KEY (owner_id) REFERENCES product_owners(owner_id)
                )
            ''')

            # Insert the data
            cursor.execute('''
                INSERT INTO products (
                    batch_id, product_name, description, submission_date,
                    testing_date, maturity_date, test_completed, test_id,
                    test_result_location, date_updated, updated_by, owner_id
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                batch_id, productName, description, submissionDate,
                testingDate, maturityDate, test_completed, test_id,
                testResultLocation, date_updated, updated_by, self.owner_id
            ))

            conn.commit()
            conn.close()

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred while saving to database:\n{e}")
            return

        # Inform the user and clear the form
        messagebox.showinfo("Success", f"Data saved successfully!\nTest results will be stored at:\n{testResultLocation}")
        self.clear_form()

    def clear_form(self):
        self.productName_var.set("")
        self.description_var.set("")
        self.testingDate_var.set("")
        self.maturityDate_var.set("")

    def build_ui(self):
        # Set appearance for CustomTkinter
        set_appearance_mode("light")
        set_default_color_theme("green")

        self.configure(fg_color="#f0f0f0")  # Light gray background

        # Title Frame
        title_frame = CTkFrame(self, fg_color="#4CAF50")  # Green background
        title_frame.pack(fill="x")

        title_label = CTkLabel(
            title_frame, 
            text="Product Registration", 
            font=("Helvetica", 24, "bold"), 
            text_color="white"
        )
        title_label.pack(pady=10)

        # Product Details Frame
        product_frame = CTkFrame(self, fg_color="#f0f0f0")
        product_frame.pack(padx=10, pady=10, fill="both")
        
        product_title = CTkLabel(
            product_frame,
            text="Product Details",
            font=("Helvetica", 18, "bold"),
            text_color="#333333"
        )
        product_title.grid(row=0, column=0, columnspan=2, sticky="w", padx=5, pady=5)

        CTkLabel(product_frame, text="Product Name:", font=("Helvetica", 12), text_color="#333333").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        CTkLabel(product_frame, text="Description:", font=("Helvetica", 12), text_color="#333333").grid(row=2, column=0, sticky="w", padx=5, pady=5)

        product_name_entry = CTkEntry(
            product_frame, 
            textvariable=self.productName_var, 
            width=300,
            height=30,
            corner_radius=5
        )
        product_name_entry.grid(row=1, column=1, padx=5, pady=5)
        
        description_entry = CTkEntry(
            product_frame, 
            textvariable=self.description_var, 
            width=300,
            height=30,
            corner_radius=5
        )
        description_entry.grid(row=2, column=1, padx=5, pady=5)

        # Date Selection Frame
        date_frame = CTkFrame(self, fg_color="#f0f0f0")
        date_frame.pack(padx=10, pady=10, fill="both")
        
        date_title = CTkLabel(
            date_frame,
            text="Date Selection",
            font=("Helvetica", 18, "bold"),
            text_color="#333333"
        )
        date_title.grid(row=0, column=0, columnspan=2, sticky="w", padx=5, pady=5)

        CTkLabel(date_frame, text="Testing Date:", font=("Helvetica", 12), text_color="#333333").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        CTkLabel(date_frame, text="Maturity Date:", font=("Helvetica", 12), text_color="#333333").grid(row=2, column=0, sticky="w", padx=5, pady=5)

        # We'll use a frame to contain the DateEntry widget since it's not a CTk widget
        testing_date_frame = CTkFrame(date_frame, fg_color="#f0f0f0")
        testing_date_frame.grid(row=1, column=1, padx=5, pady=5)
        
        maturity_date_frame = CTkFrame(date_frame, fg_color="#f0f0f0")
        maturity_date_frame.grid(row=2, column=1, padx=5, pady=5)
        
        testingDate_entry = DateEntry(
            testing_date_frame, 
            textvariable=self.testingDate_var, 
            date_pattern="yyyy-mm-dd", 
            width=27
        )
        testingDate_entry.pack(fill="both", expand=True)

        maturityDate_entry = DateEntry(
            maturity_date_frame, 
            textvariable=self.maturityDate_var, 
            date_pattern="yyyy-mm-dd", 
            width=27
        )
        maturityDate_entry.pack(fill="both", expand=True)

        # Buttons
        button_frame = CTkFrame(self, fg_color="#f0f0f0")
        button_frame.pack(pady=20)

        save_button = CTkButton(
            button_frame, 
            text="Submit Product", 
            command=self.save_data, 
            width=150,
            height=40,
            fg_color="#4CAF50", 
            hover_color="#45a049",
            text_color="white", 
            font=("Helvetica", 12),
            corner_radius=8
        )
        save_button.grid(row=0, column=0, padx=10)

        clear_button = CTkButton(
            button_frame, 
            text="Clear", 
            command=self.clear_form, 
            width=150,
            height=40,
            fg_color="#f44336", 
            hover_color="#d32f2f",
            text_color="white", 
            font=("Helvetica", 12),
            corner_radius=8
        )
        clear_button.grid(row=0, column=1, padx=10)