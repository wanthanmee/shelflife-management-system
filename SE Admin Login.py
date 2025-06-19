from customtkinter import *
import tkinter as tk
from PIL import Image, ImageTk

# Set the appearance mode and default color theme
set_appearance_mode("light")
set_default_color_theme("blue")

# Create the main window
root = CTk()
root.geometry("1920x1080")
root.title("Signup Page")
root.resizable(False, False)
root.attributes("-fullscreen", True)

# Define screen dimensions
screen_width = 1920
screen_height = 1080

# Left and right frame widths (swapped in this case)
left_frame_width = 800
right_frame_width = 1120  # 1920 - 800 = 1120

# Create right and left frames (positions swapped)
right_frame = CTkFrame(root, width=right_frame_width, height=screen_height, fg_color="white")
right_frame.place(x=0, y=0)
left_frame = CTkFrame(root, width=left_frame_width, height=screen_height)
left_frame.place(x=right_frame_width, y=0)


# Load and set background image on the left frame
def set_background_image(frame, image_path, width, height):
    try:
        image = Image.open(image_path)
        image = image.resize((width, height), Image.LANCZOS)  # Resize the image to fit the frame
        bg_image = ImageTk.PhotoImage(image)

        label = tk.Label(frame, image=bg_image)
        label.image = bg_image  # Keep a reference to avoid garbage collection
        label.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        print(f"Error loading image: {e}")


# Set background image
set_background_image(left_frame, "C:/Users/tanji/Downloads/IMG_2084.jpg", left_frame_width, screen_height)

# Fonts (Adjusted sizes for better visibility)
font_header = ("Arial", 56, "bold")
font_label = ("Arial", 20)
font_input = ("Arial", 20)
font_button = ("Arial", 28)

# Create slides for fields
slides = [CTkFrame(right_frame, width=right_frame_width, height=screen_height, fg_color="white") for _ in range(2)]
current_slide = 0


# Function to switch between slides
def show_slide(index):
    global current_slide
    slides[current_slide].place_forget()  # Hide the current slide
    slides[index].place(x=0, y=0)  # Show the new slide
    current_slide = index


# First slide (Username, Full Name, Phone Number, IC Number)
username_label = CTkLabel(slides[0], text="Username", font=font_label, text_color="#666666", fg_color="white")
username_label.place(x=150, y=280)

username_entry = CTkEntry(slides[0], width=800, height=60, font=font_input, corner_radius=20, border_color="#CCCCCC",
                          fg_color="white", text_color="#000000")
username_entry.place(x=150, y=325)

fullname_label = CTkLabel(slides[0], text="Fullname", font=font_label, text_color="#666666", fg_color="white")
fullname_label.place(x=150, y=410)

fullname_entry = CTkEntry(slides[0], width=800, height=60, font=font_input, corner_radius=20, border_color="#CCCCCC",
                          fg_color="white", text_color="#000000")
fullname_entry.place(x=150, y=450)

phone_label = CTkLabel(slides[0], text="Phone Number", font=font_label, text_color="#666666", fg_color="white")
phone_label.place(x=150, y=530)

phone_entry = CTkEntry(slides[0], width=800, height=60, font=font_input, corner_radius=20, border_color="#CCCCCC",
                       fg_color="white", text_color="#000000")
phone_entry.place(x=150, y=570)

ic_label = CTkLabel(slides[0], text="IC Number", font=font_label, text_color="#666666", fg_color="white")
ic_label.place(x=150, y=650)

ic_entry = CTkEntry(slides[0], width=800, height=60, font=font_input, corner_radius=20, border_color="#CCCCCC",
                    fg_color="white", text_color="#000000")
ic_entry.place(x=150, y=685)

# Second slide (Email, Password, Confirm Password)
email_label = CTkLabel(slides[1], text="Email Address", font=font_label, text_color="#666666", fg_color="white")
email_label.place(x=150, y=280)

email_entry = CTkEntry(slides[1], width=800, height=60, font=font_input, corner_radius=20, border_color="#CCCCCC",
                       fg_color="white", text_color="#000000")
email_entry.place(x=150, y=325)

password_label = CTkLabel(slides[1], text="Password", font=font_label, text_color="#666666", fg_color="white")
password_label.place(x=150, y=410)

password_entry = CTkEntry(slides[1], width=800, height=60, font=font_input, corner_radius=20, border_color="#CCCCCC",
                          fg_color="white", text_color="#000000", show="*")
password_entry.place(x=150, y=450)

con_password_label = CTkLabel(slides[1], text="Confirm Password", font=font_label, text_color="#666666",
                              fg_color="white")
con_password_label.place(x=150, y=530)

con_password_entry = CTkEntry(slides[1], width=800, height=60, font=font_input, corner_radius=20,
                              border_color="#CCCCCC",
                              fg_color="white", text_color="grey", show="*")
con_password_entry.place(x=150, y=570)

# "Next" and "Back" buttons for slide navigation
next_button = CTkButton(slides[0], text="Next →", font=font_button, text_color="black", fg_color="transparent",
                        hover_color="#c89ef2", corner_radius=20, width=140, height=40, command=lambda: show_slide(1))
next_button.place(x=800, y=760)

back_button = CTkButton(slides[1], text="Back ←", font=font_button, text_color="#000000", fg_color="transparent",
                        hover_color="#c89ef2", corner_radius=20, width=140, height=40, command=lambda: show_slide(0))
back_button.place(x=800, y=760)

# Sign up header and labels
signup_header = CTkLabel(right_frame, text="Welcome Back", font=font_header, text_color="#000000", fg_color="white")
signup_header.place(x=150, y=150)


# Login Button on the left frame
login_button = CTkButton(right_frame, text="LOGIN", font=font_button, text_color="white", fg_color="#c2b8ae",
                         hover_color="#0056b3", width=800, height=60, border_width=2,
                         border_color="#c2b8ae")
login_button.place(x=150, y=850)

# Show the first slide initially
show_slide(0)

# Start the main loop
root.mainloop()
