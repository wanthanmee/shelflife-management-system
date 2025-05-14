import tkinter as tk
from customtkinter import CTk
from PO_Login import LoginPage
from PO_ProductRegister import ProductRegistrationPage 

class MainApp(CTk):
    def __init__(self):
        super().__init__()
        
        # Configure the main window
        self.title("Product Management System")
        self.geometry("1920x1080")
        
        # Create a container frame for all pages
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        
        # Dictionary to hold all frames/pages
        self.frames = {}
        
        # Initialize the login page
        login_page = LoginPage(self.container, self)
        self.frames["LoginPage"] = login_page
        
        # Start with the login page
        self.show_frame("LoginPage")
        
    def show_frame(self, page_name):
        """Show a frame for the given page name"""
        frame = self.frames[page_name]
        frame.place(x=0, y=0)
        frame.tkraise()
        
    def show_product_registration(self, owner_id=None):
        """Create and show the product registration page"""
        # Create the product registration page if it doesn't exist yet
        if "ProductRegistrationPage" not in self.frames:
            product_page = ProductRegistrationPage(self.container, self, owner_id)
            self.frames["ProductRegistrationPage"] = product_page
        
        self.show_frame("ProductRegistrationPage")
        
    def back_to_login(self):
        """Return to the login page"""
        self.show_frame("LoginPage")

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()