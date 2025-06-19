from customtkinter import *
import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
import openpyxl
from openpyxl import Workbook
import os
from datetime import datetime
import uuid



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

save_button = tk.Button(button_frame, text="Save to Excel", command=save_data, width=15, bg="#4CAF50", fg="white", font=("Helvetica", 12))
save_button.grid(row=0, column=0, padx=5)

clear_button = tk.Button(button_frame, text="Clear", command=clear_form, width=15, bg="#f44336", fg="white", font=("Helvetica", 12))
clear_button.grid(row=0, column=1, padx=5)

root.mainloop()