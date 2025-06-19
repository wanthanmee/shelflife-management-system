import customtkinter as ctk
from PIL import Image, ImageTk, ImageDraw
import tkinter as tk
from tkinter import filedialog, messagebox
import os

# Import your existing modules
from PO_Home_Final import PO_Home
from PO_ProductRegister_Final import ProductRegistration
from PO_ProductList_Final import ProductListPage

class App(ctk.CTk):
    '''
    =====================================================================================================
    Constructor: def __init__(self)
    Description: 
    This function initializes the main application window for the Shelf Life Management System.
    It sets the title, geometry, and main layout with a sidebar and content area.
    =====================================================================================================
    '''    
    def __init__(self):
        super().__init__()

        self.title("Shelf Life Management System - Product Owner")
        self.geometry("1920x1080")
        self.configure(fg_color="white")

        # Store current profile image path
        self.current_profile_image = None

        # Main layout: 2 columns → sidebar (left), content area (right)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.create_sidebar()
        self.create_content_area()
        self.create_frames()

        # Show home page by default
        self.show_frame("PO_Home")
    
    '''
    =====================================================================================================
    Function: def create_sidebar(self)
    Description: 
    This function creates the sidebar for the application, including a profile section,
    navigation buttons, and a profile picture change option.
    =====================================================================================================
    '''
    def create_sidebar(self):
        # Sidebar with matching color from your design
        self.sidebar = ctk.CTkFrame(self,
                                     width=270, fg_color="#FBC3A5", corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="ns")
        self.sidebar.grid_propagate(False)
        self.sidebar.grid_rowconfigure(10, weight=1)  # Allow bottom spacing

        # Profile section container
        profile_container = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        profile_container.grid(row=0, column=0, pady=(30, 20), padx=20, sticky="ew")

        # Profile picture button (clickable) - using circular image like your dashboard
        self.profile_size = 100
        self.create_default_profile_image()
        
        # Create a tkinter label for the profile image (to match your dashboard style)
        self.profile_label = tk.Label(profile_container, bg="#FBC3A5", borderwidth=0, cursor="hand2")
        self.profile_label.pack(pady=(0, 15))
        self.profile_label.bind("<Button-1>", lambda e: self.open_profile_page())
        
        # Display default profile image
        default_img_path = "C:/Users/user/PycharmProjects/Semster 5/Software Engineering/Dashboard Icons/profile_icon.png"
        self.display_profile_image(default_img_path)

        # Welcome text - Fixed font specification
        self.welcome_label = ctk.CTkLabel(
            profile_container, 
            text="Welcome, Name", 
            font=("Arial", 18),  # Removed "italic" style that was causing issues
            text_color="black"
        )
        self.welcome_label.pack()

        # Load icons
        self.load_icons()

        # Navigation menu
        nav_container = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        nav_container.grid(row=1, column=0, pady=(20, 0), padx=15, sticky="ew")

        # Navigation buttons with proper icons and styling from your dashboard
        self.nav_buttons_data = [
            ("Home", self.home_icon, self.show_home),
            ("Product Registration", self.register_icon, self.show_register),
            ("Product List", self.list_icon, self.show_list),
            ("Mailbox", self.mailbox_icon, self.show_mailbox),
        ]

        self.nav_buttons = []
        for i, (text, icon, command) in enumerate(self.nav_buttons_data):
            btn = ctk.CTkButton(
                nav_container,
                text=f"  {text}",
                command=command,
                anchor="w",
                width=220,
                height=50,
                corner_radius=25,
                fg_color="white" if text == "Home" else "#FBC3A5",
                text_color="black",
                hover_color="#f8b78f",
                font=("Arial", 14),  # Removed "bold" style
                image=icon,
                compound="left"
            )
            btn.pack(pady=5, padx=10)
            self.nav_buttons.append(btn)

        # Add profile picture change button at bottom
        change_pic_btn = ctk.CTkButton(
            self.sidebar,
            text="📷 Change Profile Picture",
            command=self.change_profile_picture,
            fg_color="#CD853F",
            hover_color="#D2B48C",
            text_color="white",
            font=("Arial", 12),
            height=35,
            width=200
        )
        change_pic_btn.grid(row=11, column=0, pady=(0, 30), padx=20)

    def load_icons(self):
        """Load navigation icons from your specified paths"""
        try:
            base_path = "C:/Users/user/PycharmProjects/Semster 5/Software Engineering/Dashboard Icons/"
            self.home_icon = ctk.CTkImage(light_image=Image.open(f"{base_path}SE home.jpeg"), size=(40, 40))
            self.register_icon = ctk.CTkImage(light_image=Image.open(f"{base_path}SE register.jpeg"), size=(40, 40))
            self.list_icon = ctk.CTkImage(light_image=Image.open(f"{base_path}SE list.jpeg"), size=(40, 40))
            self.mailbox_icon = ctk.CTkImage(light_image=Image.open(f"{base_path}SE mail.jpeg"), size=(40, 40))
        except Exception as e:
            print(f"Error loading icons: {e}")
            # Fallback to emoji icons if files not found
            self.home_icon = None
            self.register_icon = None
            self.list_icon = None
            self.mailbox_icon = None

    def create_circular_image(self, image_path, size):
        """Create circular image like in your dashboard"""
        try:
            img = Image.open(image_path).resize((size, size), Image.Resampling.LANCZOS).convert("RGBA")
            mask = Image.new("L", (size, size), 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, size, size), fill=255)
            circular_img = Image.new("RGBA", (size, size))
            circular_img.paste(img, (0, 0), mask=mask)
            return circular_img
        except Exception as e:
            print(f"Error creating circular image: {e}")
            return None

    def change_profile_picture(self):
        """Allow user to change profile picture"""
        file_path = filedialog.askopenfilename(
            title="Select Profile Picture",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            try:
                # Update the profile image using the circular image method
                circular_img = self.create_circular_image(file_path, self.profile_size)
                if circular_img:
                    profile_image_tk = ImageTk.PhotoImage(circular_img)
                    self.profile_label.configure(image=profile_image_tk)
                    self.profile_label.image = profile_image_tk
                    self.current_profile_image = file_path
                
                messagebox.showinfo("Success", "Profile picture updated successfully!")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {str(e)}")

    def display_profile_image(self, image_path):
        """Display profile image in circular format"""
        if os.path.exists(image_path):
            circular_img = self.create_circular_image(image_path, self.profile_size)
            if circular_img:
                profile_image_tk = ImageTk.PhotoImage(circular_img)
                self.profile_label.configure(image=profile_image_tk)
                self.profile_label.image = profile_image_tk  # Prevent garbage collection
        else:
            # Create default circular image if file doesn't exist
            self.create_default_profile_image()
            if hasattr(self, 'default_profile_tk'):
                self.profile_label.configure(image=self.default_profile_tk)
                self.profile_label.image = self.default_profile_tk

    def create_default_profile_image(self):
        """Create a default profile image"""
        try:
            # Create a default circular profile image
            img = Image.new('RGB', (self.profile_size, self.profile_size), color='#8B4513')
            # Add a simple user icon representation
            draw = ImageDraw.Draw(img)
            
            # Draw a simple person silhouette
            center = self.profile_size // 2
            # Head (circle)
            head_radius = self.profile_size // 6
            draw.ellipse([center - head_radius, center - head_radius - 10, 
                         center + head_radius, center + head_radius - 10], fill='white')
            # Body (rounded rectangle)
            body_width = self.profile_size // 3
            body_height = self.profile_size // 3
            draw.ellipse([center - body_width, center, 
                         center + body_width, center + body_height], fill='white')
            
            # Convert to circular
            circular_img = self.create_circular_image_from_pil(img, self.profile_size)
            if circular_img:
                self.default_profile_tk = ImageTk.PhotoImage(circular_img)
        except Exception as e:
            print(f"Error creating default profile image: {e}")

    def create_circular_image_from_pil(self, img, size):
        """Create circular image from PIL image"""
        try:
            mask = Image.new("L", (size, size), 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, size, size), fill=255)
            circular_img = Image.new("RGBA", (size, size))
            circular_img.paste(img, (0, 0), mask=mask)
            return circular_img
        except Exception as e:
            print(f"Error creating circular image from PIL: {e}")
            return None

    def open_profile_page(self):
        """Open profile page when profile picture is clicked"""
        # Create a simple profile popup window
        profile_window = ctk.CTkToplevel(self)
        profile_window.title("Profile Settings")
        profile_window.geometry("400x300")
        profile_window.configure(fg_color="white")
        
        # Center the window
        profile_window.transient(self)
        profile_window.grab_set()
        
        # Profile content - Fixed font specification
        title_label = ctk.CTkLabel(
            profile_window, 
            text="Profile Settings", 
            font=("Arial", 20),  # Removed "bold" style
            text_color="#8B4513"
        )
        title_label.pack(pady=20)
        
        # Show current profile image
        if hasattr(self, 'profile_label') and hasattr(self.profile_label, 'image'):
            current_img = getattr(self.profile_label, 'image', None)
            if current_img:
                profile_display = tk.Label(profile_window, image=current_img, bg="white")
                profile_display.pack(pady=10)
        
        # Name entry
        name_frame = ctk.CTkFrame(profile_window, fg_color="transparent")
        name_frame.pack(pady=10, padx=20, fill="x")
        
        ctk.CTkLabel(name_frame, text="Name:", font=("Arial", 14)).pack(anchor="w")
        name_entry = ctk.CTkEntry(name_frame, placeholder_text="Enter your name", width=300)
        name_entry.pack(pady=5)
        name_entry.insert(0, "Name")  # Default value
        
        # Buttons
        button_frame = ctk.CTkFrame(profile_window, fg_color="transparent")
        button_frame.pack(pady=20)
        
        def save_profile():
            new_name = name_entry.get().strip()
            if new_name:
                self.welcome_label.configure(text=f"Welcome, {new_name}")
                messagebox.showinfo("Success", "Profile updated successfully!")
                profile_window.destroy()
            else:
                messagebox.showwarning("Warning", "Please enter a valid name!")
        
        save_btn = ctk.CTkButton(
            button_frame,
            text="Save Changes",
            command=save_profile,
            fg_color="#8B4513",
            hover_color="#A0522D"
        )
        save_btn.pack(side="left", padx=10)
        
        change_pic_btn = ctk.CTkButton(
            button_frame,
            text="Change Picture",
            command=lambda: [self.change_profile_picture(), profile_window.focus()],
            fg_color="#CD853F",
            hover_color="#D2B48C"
        )
        change_pic_btn.pack(side="right", padx=10)

    def create_content_area(self):
        # Content Frame (for page switching)
        self.container = ctk.CTkFrame(self, fg_color="white", corner_radius=0)
        self.container.grid(row=0, column=1, sticky="nsew")

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

    def create_frames(self):
        # Dictionary of frames
        self.frames = {}

        for F in (PO_Home, ProductRegistration, ProductListPage):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            frame.grid(row=0, column=0, sticky="nsew")
            self.frames[page_name] = frame

    def show_frame(self, page_name):
        """Show the selected frame and update button states"""
        frame = self.frames[page_name]
        frame.tkraise()
        
        # Update button colors to show active state (matching your dashboard style)
        for i, (text, icon, command) in enumerate(self.nav_buttons_data):
            if (page_name == "PO_Home" and text == "Home") or \
               (page_name == "ProductRegistration" and text == "Product Registration") or \
               (page_name == "ProductListPage" and text == "Product List"):
                # Active button - white background like in your dashboard
                self.nav_buttons[i].configure(fg_color="white", text_color="black")
            else:
                # Inactive button - transparent background
                self.nav_buttons[i].configure(fg_color="#FBC3A5", text_color="black")

    def show_home(self):
        self.show_frame("PO_Home")

    def show_register(self):
        self.show_frame("ProductRegistration")

    def show_list(self):
        self.show_frame("ProductListPage")

    def show_mailbox(self):
        # Placeholder for mailbox functionality
        messagebox.showinfo("Mailbox", "Mailbox functionality coming soon!")
        print("Mailbox clicked")


if __name__ == "__main__":
    # Set appearance mode to light for consistency
    ctk.set_appearance_mode("light")
    app = App()
    app.mainloop()