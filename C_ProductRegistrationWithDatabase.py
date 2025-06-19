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

#database setup
def setup_database():
    #create a database connection and cursor
    conn = sqlite3.connect('ProductRegistration.db') 
    cursor = conn.cursor()

    try:
        # Create a table if it doesn't exist
        cursor.execute('''
            CREATE TABLE products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                batch_id TEXT NOT NULL UNIQUE,
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
                status TEXT DEFAULT 'Pending',
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

# Excel file setup
file_name = "productData.xlsx"

if not os.path.exists(file_name):
    wb = Workbook()
    ws = wb.active
    ws.append(["Batch_ID", "Product Name", "Description", "Submission Date", "Testing Date", "Maturity Date", "Test Completed", "Test_ID", "Test Result Location", "Date Updated", "Updated By"])  # Header
    wb.save(file_name)

# Function to save data
def save_data():
    productName = productName_var.get()
    description = description_var.get()
    testingDate = testingDate_var.get()
    maturityDate = maturityDate_var.get()

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
    wb = openpyxl.load_workbook(file_name)
    ws = wb.active
    ws.append([batch_id, productName, description, submissionDate, testingDate, maturityDate, test_completed, test_id, testResultLocation, date_updated, updated_by])  # Append data
    wb.save(file_name)

    # Save data to SQLite database
    try:
        conn = sqlite3.connect('ProductRegistration.db')
        cursor = conn.cursor()

        # Insert data into the database
        cursor.execute('''
            INSERT INTO products (
                batch_id, product_name, description, submission_date,
                testing_date, maturity_date, test_completed, test_id,
                test_result_location, date_updated, updated_by
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            batch_id, productName, description, submissionDate,
            testingDate, maturityDate, test_completed, test_id,
            testResultLocation, date_updated, updated_by
        ))

        conn.commit()
        conn.close()

    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred while saving to database:\n{e}")
        return

    # Inform the user and clear the form
    messagebox.showinfo("Success", f"Data saved to Excel!\nTest results will be stored at:\n{testResultLocation}")
    clear_form()

# Function to clear the form
def clear_form():
    productName_var.set("")
    description_var.set("")
    testingDate_var.set("")
    maturityDate_var.set("")

# Center the window
def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

'''
def build_product_details_frame():
    product_frame = ctk.CTkFrame(main_area, fg_color="#FCEBEB", width=1000, height=300, corner_radius=20)
    product_frame.place(x=100, y=150)
    product_frame.pack_propagate(False)

    product_details_label = ctk.CTkLabel(product_frame, text="Product Details", font=("Arial", 25, "bold"), text_color="#5B3E2B")
    product_details_label.place(x=20, y=30)

    product_label = ctk.CTkLabel(product_frame, text="Product Name:", font=("Arial", 16))
    product_label.place(x=20, y=80)
    product_entry = ctk.CTkEntry(product_frame, width=800, height= 30)
    product_entry.place(x=150, y=80)

    desc_label = ctk.CTkLabel(product_frame, text="Description:", font=("Arial", 16))
    desc_label.place(x=20, y=140)
    desc_entry = ctk.CTkEntry(product_frame, width=800, height=100)
    desc_entry.place(x=150, y=140)

    # ------------------ Date Selection Frame ------------------
    date_frame = ctk.CTkFrame(main_area, fg_color="#F0EFF8", width=1000, height=250, corner_radius=20)
    date_frame.place(x=100, y=490)
    date_frame.pack_propagate(False)

    date_details_label = ctk.CTkLabel(date_frame, text="Date Selection", font=("Arial", 25,  "bold"), text_color="#5B3E2B")
    date_details_label.place(x=20, y=30)

    testing_label = ctk.CTkLabel(date_frame, text="Testing Date:", font=("Arial", 16))
    testing_label.place(x=20, y=80)
    testing_date = DateEntry(date_frame, width=18, background='pink', foreground='white', borderwidth=2)
    testing_date.place(x=150, y=80)

    maturity_label = ctk.CTkLabel(date_frame, text="Maturity Date:", font=("Arial", 16))
    maturity_label.place(x=20, y=130)
    maturity_date = DateEntry(date_frame, width=18, background='pink', foreground='white', borderwidth=2)
    maturity_date.place(x=150, y=130)
'''

# GUI setup
root = tk.Tk()
root.title("Product Registration Form")
root.configure(bg="#f0f0f0")  # Light gray background

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

root.geometry(f"{screen_width}x{screen_height}")

# Center the window
center_window(root)

# Title Frame
title_frame = tk.Frame(root, bg="#4CAF50")  # Green background
title_frame.pack(fill="x")

title_label = tk.Label(title_frame, text="Product Registration", font=("Helvetica", 24, "bold"), bg="#4CAF50", fg="white")
title_label.pack(pady=10)

# Product Details Frame
product_frame = tk.LabelFrame(root, text="Product Details", font=("Helvetica", 18, "bold"), bg="#f0f0f0", padx=10, pady=10)
product_frame.pack(padx=10, pady=10, fill="both")

tk.Label(product_frame, text="Product Name:", font=("Helvetica", 12), bg="#f0f0f0").grid(row=0, column=0, sticky="w", padx=5, pady=5)
tk.Label(product_frame, text="Description:", font=("Helvetica", 12), bg="#f0f0f0").grid(row=1, column=0, sticky="w", padx=5, pady=5)

productName_var = tk.StringVar()
description_var = tk.StringVar()

tk.Entry(product_frame, textvariable=productName_var, width=30).grid(row=0, column=1, padx=5, pady=5)
tk.Entry(product_frame, textvariable=description_var, width=30).grid(row=1, column=1, padx=5, pady=5)

# Date Selection Frame
date_frame = tk.LabelFrame(root, text="Date Selection", font=("Helvetica", 18, "bold"), bg="#f0f0f0", padx=10, pady=10)
date_frame.pack(padx=10, pady=10, fill="both")

tk.Label(date_frame, text="Testing Date:", font=("Helvetica", 12), bg="#f0f0f0").grid(row=0, column=0, sticky="w", padx=5, pady=5)
tk.Label(date_frame, text="Maturity Date:", font=("Helvetica", 12), bg="#f0f0f0").grid(row=1, column=0, sticky="w", padx=5, pady=5)

testingDate_var = tk.StringVar()
maturityDate_var = tk.StringVar()

testingDate_entry = DateEntry(date_frame, textvariable=testingDate_var, date_pattern="yyyy-mm-dd", width=27)
testingDate_entry.grid(row=0, column=1, padx=5, pady=5)

maturityDate_entry = DateEntry(date_frame, textvariable=maturityDate_var, date_pattern="yyyy-mm-dd", width=27)
maturityDate_entry.grid(row=1, column=1, padx=5, pady=5)

# Buttons
button_frame = tk.Frame(root, bg="#f0f0f0")
button_frame.pack(pady=10)

save_button = tk.Button(button_frame, text="Submit Product", command=save_data, width=15, bg="#4CAF50", fg="white", font=("Helvetica", 12))
save_button.grid(row=0, column=0, padx=5)

clear_button = tk.Button(button_frame, text="Clear", command=clear_form, width=15, bg="#f44336", fg="white", font=("Helvetica", 12))
clear_button.grid(row=0, column=1, padx=5)

root.mainloop()


