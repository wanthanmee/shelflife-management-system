
import customtkinter as ctk
from PIL import Image, ImageTk
from PO_Home_Final import PO_Home
from PO_ProductRegister_Final import ProductRegistration
from PO_ProductList_Final import ProductListPage

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Shelf Life Management System - Product Owner")
        self.geometry("1920x1080")
        self.configure(fg_color="white")

        # Main layout: 2 columns → sidebar (left), content area (right)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=250, fg_color="#FBC3A7")
        self.sidebar.grid(row=0, column=0, sticky="ns")
        self.sidebar.grid_propagate(False)

        #self.profile_pic = ctk.CTkLabel(self.sidebar, text="", image=ctk.CTkImage(light_image=None, size=(100, 100)))
        self.profile_pic = ctk.CTkLabel(self.sidebar, text="")
        self.profile_pic.pack(pady=(20, 10))

        self.welcome_label = ctk.CTkLabel(self.sidebar, text="Welcome, Name", font=("Arial", 16, "italic"))
        self.welcome_label.pack(pady=(0, 30))

        # Sidebar buttons
        self.nav_buttons = [
            ("Home", self.show_home),
            ("Product Registration", self.show_register),
            ("Product List", self.show_list),
            ("Mailbox", self.show_mailbox),  # Placeholder
        ]

        for text, command in self.nav_buttons:
            btn = ctk.CTkButton(self.sidebar, text=text, command=command, anchor="w", width=200, height=40)
            btn.pack(pady=5, padx=10)

        # Content Frame (for page switching)
        self.container = ctk.CTkFrame(self, fg_color="white")
        self.container.grid(row=0, column=1, sticky="nsew") #ensure that the children frames can expand to fill the space in the container

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Dictionary of frames
        self.frames = {}

        for F in (PO_Home, ProductRegistration, ProductListPage):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            frame.grid(row=0, column=0, sticky="nsew") #nsew ensures the frame fills the entire container
            self.frames[page_name] = frame

        self.show_frame("PO_Home")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def show_home(self):
        self.show_frame("PO_Home")

    def show_register(self):
        self.show_frame("ProductRegistration")

    def show_list(self):
        self.show_frame("ProductListPage")

    def show_mailbox(self):
        # Optional placeholder
        print("Mailbox clicked")


if __name__ == "__main__":
    #ctk.set_appearance_mode("light")  # Optional
    app = App()
    app.mainloop()


