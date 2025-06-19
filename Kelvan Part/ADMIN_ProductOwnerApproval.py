from customtkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkfont
from tkinter import ttk
import sqlite3

'''
Additional Features: 
+Filter by Registration Date
+Filter by Owner Name in Search Bar
'''
DB_NAME = "ProductRegistration.db"


class ProductOwnerDetailPage(CTkToplevel):
    def __init__(self, master, owner_data):
        super().__init__(master)
        self.owner_data = owner_data
        self.title("Product Owner Details")
        self.geometry("600x500")

        # Make window modal
        self.transient(master)
        self.grab_set()

        self.build_ui()

    def build_ui(self):
        # Title
        title_label = CTkLabel(self, text="Product Owner Details", font=("Arial", 24))
        title_label.pack(pady=20)

        # Details frame
        details_frame = CTkFrame(self)
        details_frame.pack(padx=20, pady=10, fill="both", expand=True)

        # Owner details
        labels = ["Owner ID:", "Email:", "Name:", "Status:", "Registered At:"]
        for i, (label, value) in enumerate(zip(labels, self.owner_data)):
            # Label
            CTkLabel(details_frame, text=label, font=("Arial", 14, "bold")).pack(pady=(10, 0))
            # Value
            CTkLabel(details_frame, text=str(value), font=("Arial", 12)).pack()

        # Buttons frame
        buttons_frame = CTkFrame(self)
        buttons_frame.pack(pady=20, fill="x")

        # Approve button
        approve_button = CTkButton(
            buttons_frame,
            text="Approve",
            command=self.approve_owner,
            fg_color="green",
            hover_color="dark green"
        )
        approve_button.pack(side="left", padx=10, expand=True)

        # Deny button
        deny_button = CTkButton(
            buttons_frame,
            text="Deny",
            command=self.deny_owner,
            fg_color="red",
            hover_color="dark red"
        )
        deny_button.pack(side="right", padx=10, expand=True)

    def update_status(self, new_status):
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()

            # Update the status in the database
            cursor.execute(
                "UPDATE product_owners SET status = ? WHERE owner_id = ?",
                (new_status, self.owner_data[0])
            )
            conn.commit()
            conn.close()

            # Update the status in the owner_data
            self.owner_data = list(self.owner_data)
            self.owner_data[3] = new_status

            # Show success message
            messagebox.showinfo("Success", f"Status updated to {new_status}")

            # Refresh the main window's data
            if hasattr(self.master, 'load_data'):
                self.master.load_data()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to update status: {e}")

    def approve_owner(self):
        self.update_status("Approved")

    def deny_owner(self):
        self.update_status("Denied")


class ProductListPage(CTkFrame):
    '''
    =====================================================================================================
    Constructor: def __init__(self, master)
    Description:
    This function initializes the Product Owners List page.
    It sets up the main frame and calls the build_ui function to create the UI elements.
    =====================================================================================================
    '''

    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack(fill="both", expand=True)
        self.build_ui()

    '''
    =====================================================================================================
    Function: def build_ui(self)
    Description: 
    This function builds the UI for the Product Owners List page.
    It includes a title, search bar, status filter, and a treeview to display product owner data.
    =====================================================================================================
    '''

    def build_ui(self):
        # Title
        title_label = CTkLabel(self, text="Product Owners List", font=("Arial", 24))
        title_label.pack(pady=10)

        # Setup bold heading font style
        style = ttk.Style()
        default_font = tkfont.nametofont("TkHeadingFont")
        bold_heading_font = default_font.copy()
        bold_heading_font.configure(weight="bold")
        style.configure("Treeview.Heading", font=bold_heading_font)

        # Search bar
        search_frame = CTkFrame(self)
        search_frame.pack(pady=5, padx=20, fill="x")

        # Search label
        search_label = CTkLabel(search_frame, text="Search:")
        search_label.pack(side="left")

        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda *args: self.load_data())

        self.search_entry = CTkEntry(
            search_frame,
            placeholder_text="Search Owner Name",
            textvariable=self.search_var
        )
        self.search_entry.pack(side="left", padx=(0, 10), fill="x", expand=True)
        self.search_entry.bind("<KeyRelease>", lambda event: self.load_data())

        # Status filter
        self.status_filter_var = tk.StringVar(value="All")
        self.status_dropdown = CTkOptionMenu(search_frame, values=["All", "Pending", "Approved", "Denied"],
                                             variable=self.status_filter_var, command=lambda x: self.load_data())
        self.status_dropdown.pack(side="left")

        # Treeview
        self.tree = ttk.Treeview(self, columns=("owner_id", "email", "name", "status", "registered_at"),
                                 show="headings")
        self.tree.pack(padx=20, pady=10, fill="both", expand=True)

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.replace("_", " ").title())
            self.tree.column(col, anchor="center")

        # Scrollbar
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Row click
        self.tree.bind("<Double-1>", self.on_row_double_click)

        # Load data
        self.load_data()

    '''
    =====================================================================================================
    Function: def load_data(self)
    Description: 
    This function loads data from the SQLite database into the treeview.
    It applies filters based on the search term and status filter.
    =====================================================================================================
    '''

    def load_data(self):
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()

            query = '''
            SELECT owner_id, email, name, status, registered_at
            FROM product_owners
            WHERE 1=1
            '''
            params = []

            # Search filter
            search_term = self.search_var.get().strip()
            if search_term:
                query += " AND (\"name\" LIKE ?)"
                like_term = f"%{search_term}%"
                params += [like_term]

            # Status filter
            selected_status = self.status_filter_var.get()
            if selected_status in ["Pending", "Approved", "Denied"]:
                query += " AND \"status\" = ?"
                params.append(selected_status)

            cursor.execute(query, params)
            rows = cursor.fetchall()

            # Clear old data
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Insert new rows
            for row in rows:
                self.tree.insert("", "end", values=row)

            conn.close()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to load data:\n{e}")

    '''
    =====================================================================================================
    Function: def on_row_double_click(self, event)
    Description: 
    This function handles the double-click event on a row in the treeview.
    It retrieves the data of the selected row and prints it.
    =====================================================================================================
    '''

    def on_row_double_click(self, event):
        selected_item = self.tree.focus()
        if selected_item:
            row_data = self.tree.item(selected_item, "values")
            ProductOwnerDetailPage(self, row_data)


'''
=====================================================================================================
Run the app.
This is the main entry point of the application.
It sets the appearance mode and default color theme, creates the main window, and starts the application.
=====================================================================================================
'''
if __name__ == "__main__":
    set_appearance_mode("light")
    set_default_color_theme("blue")

    root = CTk()
    root.title("Product Owners List Viewer")
    root.geometry("1920x1080")

    app = ProductListPage(root)
    root.mainloop()

'''The workflow is now:
1. Double-click on any product owner in the main list
2. A new window opens showing all their details
3. Click either "Approve" or "Deny" to update their status
4. The status is immediately updated in the database
5. The main list is refreshed to show the new status
6. A success message is shown
Features of the detail window:
1. Modal window (you must close it before interacting with the main window)
2. Clean layout with labels and values
3. Clearly visible action buttons
4. Error handling for database operations
5. Automatic refresh of the main list when changes are made
'''

''' When inserting a new product owner, please set the status to pending. '''

