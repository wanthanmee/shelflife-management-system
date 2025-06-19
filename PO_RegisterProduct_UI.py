import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw
import customtkinter as ctk
from tkcalendar import DateEntry

# Initialize app
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("1920x1080")
app.title("Dashboard")

# Sidebar
sidebar_width = 550
sidebar = ctk.CTkFrame(app, width=sidebar_width, corner_radius=0, fg_color="#FDC09A")
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

# --- Circular profile image creation ---
def create_circular_image(image_path, size):
    img = Image.open(image_path).resize((size, size), Image.LANCZOS).convert("RGBA")
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size, size), fill=255)
    circular_img = Image.new("RGBA", (size, size))
    circular_img.paste(img, (0, 0), mask=mask)
    return circular_img

# --- Display Profile Image ---
profile_size = 170
profile_label = tk.Label(sidebar, bg="#FBC3A5", borderwidth=0)

def display_profile_image(image_path):
    if os.path.exists(image_path):
        circular_img = create_circular_image(image_path, profile_size)
        profile_image_tk = ImageTk.PhotoImage(circular_img)
        profile_label.configure(image=profile_image_tk)
        profile_label.image = profile_image_tk
        profile_label.place(x=sidebar_width//2 - profile_size//2, y=50)

# Display default image
default_img = "C:/Users/user/PycharmProjects/Semster 5/Software Engineering/Dashboard Icons/profile_icon.png"
display_profile_image(default_img)

# Welcome Text
welcome_label = ctk.CTkLabel(sidebar, text="Welcome, Name", font=("Arial", 25, "italic"), text_color="black", justify="center")
welcome_label.place(x=sidebar_width//2 - 95, y=260)


# Load icons (adjust paths and sizes as needed)
home_icon = ctk.CTkImage(light_image=Image.open("C:/Users/user/PycharmProjects/Semster 5/Software Engineering/Dashboard Icons/SE home 1.jpeg"), size=(60, 60))
register_icon = ctk.CTkImage(light_image=Image.open("C:/Users/user/PycharmProjects/Semster 5/Software Engineering/Dashboard Icons/SE register 1.jpeg"), size=(63, 63))
list_icon = ctk.CTkImage(light_image=Image.open("C:/Users/user/PycharmProjects/Semster 5/Software Engineering/Dashboard Icons/SE list.jpeg"), size=(60, 60))
mailbox_icon = ctk.CTkImage(light_image=Image.open("C:/Users/user/PycharmProjects/Semster 5/Software Engineering/Dashboard Icons/SE mail.jpeg"), size=(60, 60))

# Define font
button_font = ("Arial", 20)

# Sidebar Buttons with icons
btn_home = ctk.CTkButton(
    sidebar, text="  Home", anchor="w", width=700,
    fg_color="#FDC09A", text_color="black", hover_color="#f8b78f", font=button_font, corner_radius=70,
    image=home_icon, compound="left"
)
btn_home.place(x=50, y=370)

btn_register = ctk.CTkButton(
    sidebar, text="  Product Registration", anchor="w", width=700,
    fg_color="white", text_color="black", hover_color="#f8b78f", font=button_font, corner_radius=70,
    image=register_icon, compound="left"
)
btn_register.place(x=57, y=480)

btn_list = ctk.CTkButton(
    sidebar, text="  Product List", anchor="w", width=700,
    fg_color="#FDC09A", text_color="black", hover_color="#f8b78f", font=button_font, corner_radius=70,
    image=list_icon, compound="left"
)
btn_list.place(x=59, y=590)

btn_mailbox = ctk.CTkButton(
    sidebar, text="  Mailbox", anchor="w", width=700,
    fg_color="#FDC09A", text_color="black", hover_color="#f8b78f", font=button_font, corner_radius=70,
    image=mailbox_icon, compound="left"
)
btn_mailbox.place(x=60, y=700)

# Main Content Area
main_area = ctk.CTkFrame(app, fg_color="white")
main_area.pack(expand=True, fill="both")

# Quick Stats Title
title_label = ctk.CTkLabel(main_area, text="REGISTER PRODUCT", font=("Arial", 30, "bold"), text_color="#5B3E2B")
title_label.place(x=100, y=80)



# ------------------ Product Details Frame ------------------
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

from tkinter import messagebox
from datetime import datetime

# ------------------ Submit Button with Validation ------------------

def submit_form():
    name = product_entry.get().strip()
    description = desc_entry.get().strip()
    testing = testing_date.get_date()
    maturity = maturity_date.get_date()

    if not name:
        messagebox.showerror("Validation Error", "Product name is required.")
        return
    if not description:
        messagebox.showerror("Validation Error", "Product description is required.")
        return
    if testing > maturity:
        messagebox.showerror("Validation Error", "Testing date cannot be after maturity date.")
        return

    # Success - You can add saving to a database here
    messagebox.showinfo("Success", f"Product '{name}' registered successfully!")

submit_button = ctk.CTkButton(
    main_area, text="Submit", command=submit_form,
    font=("Arial", 18), fg_color="#95d194", text_color="white", hover_color="#FDC09A", width=200, height=50, corner_radius=15
)
submit_button.place(x=400, y=790)

def clear_form():
    product_entry.delete(0, tk.END)
    desc_entry.delete(0, tk.END)
    # Optionally reset dates to today
    today = datetime.today()
    testing_date.set_date(today)
    maturity_date.set_date(today)


# Clear Button
clear_button = ctk.CTkButton(
    main_area, text="Clear", command=clear_form,
    font=("Arial", 18), fg_color="#f16c6c", text_color="white",hover_color="#FDC09A", width=200, height=50, corner_radius=15
)
clear_button.place(x=620, y=790)


app.mainloop()
