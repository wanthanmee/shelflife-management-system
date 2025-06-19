import os
import tkinter as tk
from customtkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw
import customtkinter as ctk


class ProductOwnerDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Dashboard")
        self.geometry("1920x1080")

        # Sidebar
        self.sidebar_width = 550
        self.sidebar = ctk.CTkFrame(self, width=self.sidebar_width, corner_radius=0, fg_color="#FBC3A5")
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Profile image
        self.profile_size = 170
        self.profile_label = tk.Label(self.sidebar, bg="#FBC3A5", borderwidth=0)
        self.profile_label.place(x=self.sidebar_width // 2 - self.profile_size // 2, y=50)

        # Display default image
        default_img = "C:/Users/user/PycharmProjects/Semster 5/Software Engineering/Dashboard Icons/profile_icon.png"
        self.display_profile_image(default_img)

        # Welcome text
        welcome_label = ctk.CTkLabel(self.sidebar, text="Welcome, Name", font=("Arial", 25, "italic"), text_color="black", justify="center")
        welcome_label.place(x=self.sidebar_width // 2 - 95, y=260)

        # Icons
        self.load_icons()

        # Sidebar Buttons
        button_font = ("Arial", 20)
        self.create_sidebar_button("  Home", self.home_icon, 370, button_font)
        self.create_sidebar_button("  Product Registration", self.register_icon, 480, button_font)
        self.create_sidebar_button("  Product List", self.list_icon, 590, button_font)
        self.create_sidebar_button("  Mailbox", self.mailbox_icon, 700, button_font)

        # Main area
        self.main_area = ctk.CTkFrame(self, fg_color="white")
        self.main_area.pack(expand=True, fill="both")

        # Quick stats title
        title_label = ctk.CTkLabel(self.main_area, text="QUICK STATS", font=("Arial", 30, "bold"), text_color="#5B3E2B")
        title_label.place(x=100, y=80)

        # Stats container
        self.stats_frame = ctk.CTkFrame(self.main_area, fg_color="white", width=2000, height=2000)
        self.stats_frame.place(x=90, y=160)
        self.stats_frame.pack_propagate(False)

        self.create_stat_box("Products Registered", 2, "#FCEBEB", 0, 20)
        self.create_stat_box("Products Pending Approval", 0, "#F0EFF8", 420, 20)
        self.create_stat_box("Products Approved", 1, "#FCEBEB", 840, 20)

    def load_icons(self):
        self.home_icon = ctk.CTkImage(light_image=Image.open("C:/Users/user/PycharmProjects/Semster 5/Software Engineering/Dashboard Icons/SE home.jpeg"), size=(60, 60))
        self.register_icon = ctk.CTkImage(light_image=Image.open("C:/Users/user/PycharmProjects/Semster 5/Software Engineering/Dashboard Icons/SE register.jpeg"), size=(63, 63))
        self.list_icon = ctk.CTkImage(light_image=Image.open("C:/Users/user/PycharmProjects/Semster 5/Software Engineering/Dashboard Icons/SE list.jpeg"), size=(60, 60))
        self.mailbox_icon = ctk.CTkImage(light_image=Image.open("C:/Users/user/PycharmProjects/Semster 5/Software Engineering/Dashboard Icons/SE mail.jpeg"), size=(60, 60))

    def create_sidebar_button(self, text, icon, y, font):
        button = ctk.CTkButton(
            self.sidebar,
            text=text,
            anchor="w",
            width=700,
            fg_color="white" if "Home" in text else "#FBC3A5",
            text_color="black",
            hover_color="#f8b78f",
            font=font,
            corner_radius=70,
            image=icon,
            compound="left"
        )
        button.place(x=50 if "Home" in text else 57 if "Registration" in text else 59 if "List" in text else 60, y=y)

    def create_circular_image(self, image_path, size):
        img = Image.open(image_path).resize((size, size), Image.LANCZOS).convert("RGBA")
        mask = Image.new("L", (size, size), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size, size), fill=255)
        circular_img = Image.new("RGBA", (size, size))
        circular_img.paste(img, (0, 0), mask=mask)
        return circular_img

    def display_profile_image(self, image_path):
        if os.path.exists(image_path):
            circular_img = self.create_circular_image(image_path, self.profile_size)
            profile_image_tk = ImageTk.PhotoImage(circular_img)
            self.profile_label.configure(image=profile_image_tk)
            self.profile_label.image = profile_image_tk  # Prevent garbage collection

    def create_stat_box(self, label, value, color, x, y):
        frame = ctk.CTkFrame(self.stats_frame, fg_color=color, width=400, height=250, corner_radius=20)
        frame.place(x=x, y=y)
        frame.pack_propagate(False)

        label_widget = ctk.CTkLabel(frame, text=label, font=("Arial", 20, "bold"), text_color="#5B3E2B", wraplength=360, justify="center")
        label_widget.place(relx=0.5, y=30, anchor="center")

        value_widget = ctk.CTkLabel(frame, text=str(value), font=("Arial", 36, "bold"), text_color="#5B3E2B")
        value_widget.place(relx=0.5, y=90, anchor="center")

        return frame

#Run the application frame in main window 
if __name__ == "__main__":
    app = ProductOwnerDashboard()  # No need to pass parent
    app.mainloop()
