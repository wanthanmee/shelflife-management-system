import customtkinter as ctk
import sqlite3
from tkinter import messagebox
from login_db import hash_password, create_database

# Set appearance and scaling
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Create main window (full screen)
app = ctk.CTk()
app.title("Login System")
app.attributes("-fullscreen", True)  # Make it full screen

# Get screen width to compute frame width
screen_width = app.winfo_screenwidth()
white_width = int(screen_width * 0.50)

# Left white frame (¾ of screen)
left_frame = ctk.CTkFrame(master=app, width=white_width, fg_color="#FCF9F9")
left_frame.pack(side="left", fill="both")

# Right gray frame (¼ of screen)
right_frame = ctk.CTkFrame(master=app, fg_color="#EAEAF4")
right_frame.pack(side="right", fill="both", expand=True)

# Inner frame to center the login elements
center_frame = ctk.CTkFrame(master=left_frame, fg_color="transparent")
center_frame.place(relx=0.5, rely=0.5, anchor="center")

# Welcome text
welcome_label = ctk.CTkLabel(
    master=center_frame, text="Welcome!", font=("Arial", 28, "bold"), text_color="black"
)
welcome_label.pack(pady=(0, 10))

# Instruction text
instruction_label = ctk.CTkLabel(
    master=center_frame,
    text="Please log in to access the system",
    font=("Arial", 16),
    text_color="gray",
)
instruction_label.pack(pady=(0, 30))

# Username entry
username_entry = ctk.CTkEntry(
    master=center_frame,
    placeholder_text="Username",
    width=400,
    height=40,
    corner_radius=10,
)
username_entry.pack(pady=10)

# Password entry
password_entry = ctk.CTkEntry(
    master=center_frame,
    placeholder_text="Password",
    show="*",
    width=400,
    height=40,
    corner_radius=10,
)
password_entry.pack(pady=10)


# Login button
def login():
    username = username_entry.get()
    password = password_entry.get()

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    hashed_pw = hash_password(password)
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_pw))
    result = cursor.fetchone()

    conn.close()

    if result:
        messagebox.showinfo(title="Login Successful", message="Welcome Admin.")
    else:
        messagebox.showerror(title="Login Unsuccessful", message="Username or Password incorrect.")


login_button = ctk.CTkButton(
    master=center_frame,
    text="LOGIN",
    width=400,
    height=40,
    corner_radius=10,
    fg_color="#654633",
    hover_color="#503524",
    text_color="white",
    command=login
)

login_button.pack(pady=30)

create_database()
app.mainloop()
