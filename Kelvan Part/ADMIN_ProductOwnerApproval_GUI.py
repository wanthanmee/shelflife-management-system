import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw
import customtkinter as ctk

# Initialize app
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("1920x1080")
app.title("Dashboard")


# Main Content Area
main_area = ctk.CTkFrame(app, fg_color="white")
main_area.pack(expand=True, fill="both")

title_label = ctk.CTkLabel(main_area, text="REGISTER PRODUCT", font=("Arial", 30, "bold"), text_color="#5B3E2B")
title_label.place(x=100, y=80)

from tkinter import ttk, messagebox
from tkcalendar import DateEntry

# --- Main Frame Content ---
content_frame = tk.Frame(main_area, bg="#FAE6E6", bd=0)
content_frame.place(x=100, y=170, width=1000, height=600)

# Search + Filters Frame
search_filter_frame = tk.Frame(content_frame, bg="#FAE6E6")
search_filter_frame.pack(pady=10, fill="x", padx=20)

# Search Entry
search_var = tk.StringVar()
search_entry = tk.Entry(search_filter_frame, textvariable=search_var, font=("Arial", 12), width=40)
search_entry.pack(side="left", padx=(0, 10))

# Filter Combobox
filter_var = tk.StringVar(value="All")
filter_combo = ttk.Combobox(search_filter_frame, textvariable=filter_var, values=["All", "Pending", "Approved", "Denied"], width=15, state="readonly")
filter_combo.pack(side="left", padx=(0, 10))

# Date Filter
calendar_label = tk.Label(search_filter_frame, text="Date:", font=("Arial", 12), bg="#FAE6E6")
calendar_label.pack(side="left")

date_entry = DateEntry(search_filter_frame, width=15, background='darkblue', foreground='white', borderwidth=2)
date_entry.pack(side="left", padx=(5, 0))


# --- Scrollable List of Product Owners with Approve/Deny Buttons using .place() ---

# Container with scrollbar
canvas_frame = tk.Frame(content_frame, bg="#FAE6E6")
canvas_frame.place(x=0, y=100, width=1000, height=500)  # Adjust size as needed

canvas = tk.Canvas(canvas_frame, bg="#FAE6E6", highlightthickness=0)
canvas.place(x=0, y=0, width=980, height=500)

scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
scrollbar.place(x=980, y=0, height=500)

scrollable_frame = tk.Frame(canvas, bg="#FAE6E6")
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

def on_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

scrollable_frame.bind("<Configure>", on_configure)

# Sample Product Owners
sample_owners = [
    {"name": "Alice Johnson"},
    {"name": "Bob Smith"},
    {"name": "Charlie Davis"},
    {"name": "Diana Prince"},
    {"name": "Evan Brown"},
    {"name": "Fiona Lee"},
    {"name": "George King"},
]

def approve_owner(owner_name):
    messagebox.showinfo("Approved", f"{owner_name} has been approved.")

def deny_owner(owner_name):
    messagebox.showinfo("Denied", f"{owner_name} has been denied.")

# Dynamically create owner frames
def display_owners():
    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    frame_width = 920
    frame_height = 80
    frame_color = "#FFFFFF"
    y_spacing = 15

    total_height = len(sample_owners) * (frame_height + y_spacing)
    scrollable_frame.config(width=frame_width + 20, height=total_height)

    for idx, owner in enumerate(sample_owners):
        y_position = idx * (frame_height + y_spacing)

        owner_frame = tk.Frame(scrollable_frame, bg=frame_color, bd=2, relief="ridge")
        owner_frame.place(x=10, y=y_position, width=frame_width, height=frame_height)

        name_label = tk.Label(owner_frame, text=owner["name"], font=("Arial", 16, "bold"), bg=frame_color, anchor="w")
        name_label.place(x=20, y=20)

        # Approve Button
        approve_btn = tk.Button(
            owner_frame, text="Approve", bg="#A3D9A5", fg="black",
            font=("Arial", 12), width=10,
            command=lambda n=owner["name"]: approve_owner(n)
        )
        approve_btn.place(x=frame_width - 200, y=20)

        # Deny Button
        deny_btn = tk.Button(
            owner_frame, text="Deny", bg="#F88B8B", fg="black",
            font=("Arial", 12), width=10,
            command=lambda n=owner["name"]: deny_owner(n)
        )
        deny_btn.place(x=frame_width - 100, y=20)

# Make sure scrollregion is updated when contents change
def on_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

scrollable_frame.bind("<Configure>", on_configure)
canvas.bind("<Configure>", lambda e: canvas.itemconfig("inner_frame", width=e.width))

# Use a tagged window for better resizing
canvas.delete("all")  # clear previous content if any
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", tags="inner_frame")

display_owners()


app.mainloop()
