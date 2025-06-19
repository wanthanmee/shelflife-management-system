import os
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import sqlite3
import customtkinter as ctk
from datetime import datetime

DB_NAME = "ProductRegistration.db"

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("1600x900")
app.title("Product Owner Approval Dashboard")


def display_owners():
    # Clear current display
    for widget in owners_scrollable_frame.winfo_children():
        widget.destroy()
    
    owners = fetch_product_owners()
    date_str = datetime.now().strftime("%Y-%m-%d")
    date_label.configure(text=f"Current Date: {date_str}")

    if not owners:
        empty_label = ctk.CTkLabel(owners_scrollable_frame, 
                                  text="No product owners found", 
                                  font=("Arial", 14))
        empty_label.pack(pady=50)
        return

    # Create owner cards
    for owner in owners:
        owner_id, name, email, status, registered_at = owner
        
        # Card frame
        card_frame = ctk.CTkFrame(owners_scrollable_frame, 
                                 border_width=1,
                                 border_color="#D3D3D3",
                                 corner_radius=8)
        card_frame.pack(fill="x", padx=5, pady=5)
        
        # Selection checkbox
        chk_var = tk.IntVar(value=1 if owner_id in selected_owners else 0)
        chk = ctk.CTkCheckBox(card_frame, 
                              text="", 
                              variable=chk_var,
                              command=lambda oid=owner_id: toggle_selection(oid))
        chk.pack(side="left", padx=10)
        
        # Owner info
        info_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
        info_frame.pack(side="left", fill="x", expand=True, padx=5)
        
        # Name and status
        name_label = ctk.CTkLabel(info_frame, 
                                 text=name,
                                 font=("Arial", 14, "bold"))
        name_label.pack(anchor="w")
        
        # Email and registration date
        details_label = ctk.CTkLabel(info_frame,
                                    text=f"{email}\nRegistered: {registered_at}",
                                    font=("Arial", 12),
                                    text_color="#666666")
        details_label.pack(anchor="w")
        
        # Status indicator
        status_color = {
            "Pending": "#F39C12",
            "Approved": "#27AE60",
            "Denied": "#E74C3C"
        }.get(status, "#3498DB")
        
        status_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
        status_frame.pack(side="right", padx=10)
        
        status_label = ctk.CTkLabel(status_frame,
                                   text=status,
                                   fg_color=status_color,
                                   corner_radius=4,
                                   text_color="white",
                                   font=("Arial", 12, "bold"),
                                   width=80)
        status_label.pack(pady=5)
        
        # Action buttons
        btn_frame = ctk.CTkFrame(status_frame, fg_color="transparent")
        btn_frame.pack()
        
        approve_btn = ctk.CTkButton(btn_frame,
                                   text="Approve",
                                   fg_color="#27AE60",
                                   width=80,
                                   command=lambda oid=owner_id: update_status(oid, "Approved"))
        approve_btn.pack(pady=2)
        
        deny_btn = ctk.CTkButton(btn_frame,
                                text="Deny",
                                fg_color="#E74C3C",
                                width=80,
                                command=lambda oid=owner_id: update_status(oid, "Denied"))
        deny_btn.pack(pady=2)

def delete_selected():
    if not selected_owners:
        messagebox.showwarning("Warning", "No owners selected")
        return
        
    if messagebox.askyesno("Confirm", f"Delete {len(selected_owners)} selected owners permanently?"):
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            
            # Log deletions to audit table
            cursor.executemany("""
                INSERT INTO PO_delete_audit_log (owner_id, deleted_by, deleted_at)
                VALUES (?, ?, datetime('now'))
            """, [(oid, "admin") for oid in selected_owners])
            
            # Perform deletion
            cursor.executemany("DELETE FROM product_owners WHERE owner_id = ?", 
                             [(oid,) for oid in selected_owners])
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", f"Deleted {len(selected_owners)} owners")
            selected_owners.clear()
            delete_btn.configure(state="disabled")
            display_owners()
            display_audit_log()  # Refresh audit log after deletion
        except Exception as e:
            messagebox.showerror("Error", f"Deletion failed: {e}")


# ===================== MAIN UI ==========================
main_frame = ctk.CTkFrame(app, fg_color="white")
main_frame.pack(expand=True, fill="both", padx=20, pady=20)

# Header Section
header_frame = ctk.CTkFrame(main_frame, fg_color="white")
header_frame.pack(fill="x", pady=(0, 20))

title_label = ctk.CTkLabel(header_frame, 
                          text="PRODUCT OWNER APPROVAL DASHBOARD",
                          font=("Arial", 24, "bold"), 
                          text_color="#2E4053")
title_label.pack(side="left")

# Action buttons
action_frame = ctk.CTkFrame(header_frame, fg_color="white")
action_frame.pack(side="right")

delete_btn = ctk.CTkButton(action_frame, 
                         text="Delete Selected", 
                         fg_color="#E74C3C", 
                         width=120,
                         state="disabled", 
                         command=delete_selected)
delete_btn.pack(side="left", padx=5)

# Search and Filter Section
filter_frame = ctk.CTkFrame(main_frame, fg_color="white")
filter_frame.pack(fill="x", pady=(0, 10))

# Current date display
date_str = datetime.now().strftime("%Y-%m-%d")
date_label = ctk.CTkLabel(filter_frame, 
                         text=f"Current Date: {date_str}", 
                         font=("Arial", 12))
date_label.pack(side="left", padx=10)

# Search entry
search_var = tk.StringVar()
search_entry = ctk.CTkEntry(filter_frame, 
                           placeholder_text="Search by name...",
                           textvariable=search_var, 
                           width=300)
search_entry.pack(side="left", padx=10)

# Status filter
filter_var = tk.StringVar(value="All")
status_filter = ctk.CTkComboBox(filter_frame, 
                               variable=filter_var,
                               values=["All", "Pending", "Approved", "Denied"],
                               width=150)
status_filter.pack(side="left", padx=10)

# Date filter
# Date range filter frame
date_filter_frame = ctk.CTkFrame(filter_frame, fg_color="white")
date_filter_frame.pack(side="left", padx=10)

# From date
from_date_frame = ctk.CTkFrame(date_filter_frame, fg_color="white")
from_date_frame.pack(side="left", padx=5)

from_label = ctk.CTkLabel(from_date_frame, text="From:")
from_label.pack(side="left")

from_date_var = tk.StringVar()
from_date_entry = DateEntry(from_date_frame, 
                          width=12, 
                          background='darkblue',
                          foreground='white', 
                          borderwidth=2,
                          date_pattern='y-mm-dd',
                          textvariable=from_date_var)
from_date_entry.pack(side="left", padx=5)

# To date
to_date_frame = ctk.CTkFrame(date_filter_frame, fg_color="white")
to_date_frame.pack(side="left", padx=5)

to_label = ctk.CTkLabel(to_date_frame, text="To:")
to_label.pack(side="left")

to_date_var = tk.StringVar()
to_date_entry = DateEntry(to_date_frame, 
                        width=12, 
                        background='darkblue',
                        foreground='white', 
                        borderwidth=2,
                        date_pattern='y-mm-dd',
                        textvariable=to_date_var)
to_date_entry.pack(side="left", padx=5)

# Clear dates button
clear_dates_btn = ctk.CTkButton(date_filter_frame,
                               text="Clear Dates",
                               width=100,
                               command=lambda: [from_date_var.set(""), to_date_var.set(""), display_owners()])
clear_dates_btn.pack(side="left", padx=10)

# Create a StringVar to hold the selected date
date_selected = tk.StringVar()

clear_date_btn = ctk.CTkButton(date_filter_frame,
                              text="Clear",
                              width=60,
                              command=lambda: [date_selected.set(""), display_owners()])
clear_date_btn.pack(side="left", padx=5)



date_filter_var = tk.StringVar()
# date_entry = DateEntry(date_filter_frame, 
#                       width=12, 
#                       background='darkblue',
#                       foreground='white', 
#                       borderwidth=2,
#                       date_pattern='y-mm-dd',
#                       textvariable=date_filter_var)
# date_entry.pack(side="left", padx=5)

# clear_date_btn = ctk.CTkButton(date_filter_frame,
#                               text="Clear",
#                               width=60,
#                               command=lambda: date_filter_var.set(""))
# clear_date_btn.pack(side="left", padx=5)

refresh_btn = ctk.CTkButton(filter_frame, 
                           text="Refresh", 
                           width=80,
                           command=display_owners)
refresh_btn.pack(side="left", padx=10)

# Main content area (split view)
content_frame = ctk.CTkFrame(main_frame)
content_frame.pack(expand=True, fill="both")

# Owners panel (left)
owners_frame = ctk.CTkFrame(content_frame)
owners_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

owners_label = ctk.CTkLabel(owners_frame, 
                           text="PRODUCT OWNERS",
                           font=("Arial", 14, "bold"))
owners_label.pack(anchor="w", pady=(0, 10))

# Owners scrollable area
owners_canvas = tk.Canvas(owners_frame, bg="#FAE6E6", highlightthickness=0)
owners_scroll = ttk.Scrollbar(owners_frame, orient="vertical", command=owners_canvas.yview)
owners_scrollable_frame = ctk.CTkFrame(owners_canvas)

owners_scrollable_frame.bind(
    "<Configure>",
    lambda e: owners_canvas.configure(
        scrollregion=owners_canvas.bbox("all")
))

owners_canvas.create_window((0, 0), window=owners_scrollable_frame, anchor="nw")
owners_canvas.configure(yscrollcommand=owners_scroll.set)

owners_canvas.pack(side="left", fill="both", expand=True)
owners_scroll.pack(side="right", fill="y")

# Audit log panel (right)
audit_frame = ctk.CTkFrame(content_frame, width=400)
audit_frame.pack(side="right", fill="both")

audit_label = ctk.CTkLabel(audit_frame, 
                          text="DELETION AUDIT LOG",
                          font=("Arial", 14, "bold"))
audit_label.pack(anchor="w", pady=(0, 10))

# Audit log scrollable area
audit_canvas = tk.Canvas(audit_frame, bg="#FAE6E6", highlightthickness=0)
audit_scroll = ttk.Scrollbar(audit_frame, orient="vertical", command=audit_canvas.yview)
audit_scrollable_frame = ctk.CTkFrame(audit_canvas)

audit_scrollable_frame.bind(
    "<Configure>",
    lambda e: audit_canvas.configure(
        scrollregion=audit_canvas.bbox("all")
))

audit_canvas.create_window((0, 0), window=audit_scrollable_frame, anchor="nw")
audit_canvas.configure(yscrollcommand=audit_scroll.set)

audit_canvas.pack(side="left", fill="both", expand=True)
audit_scroll.pack(side="right", fill="y")

# ===================== CORE FUNCTIONS =====================
selected_owners = set()

def toggle_selection(owner_id):
    if owner_id in selected_owners:
        selected_owners.remove(owner_id)
    else:
        selected_owners.add(owner_id)
    delete_btn.configure(state="normal" if selected_owners else "disabled")

def fetch_product_owners():
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        query = """SELECT owner_id, name, email, status, 
                  strftime('%Y-%m-%d', registered_at) 
                  FROM product_owners WHERE 1=1"""
        params = []

        if search_var.get():
            query += " AND name LIKE ?"
            params.append(f"%{search_var.get()}%")

        if filter_var.get() != "All":
            query += " AND status = ?"
            params.append(filter_var.get())

        # Date range filtering
        if from_date_var.get() and to_date_var.get():
            query += " AND date(registered_at) BETWEEN ? AND ?"
            params.extend([from_date_var.get(), to_date_var.get()])
        elif from_date_var.get():
            query += " AND date(registered_at) >= ?"
            params.append(from_date_var.get())
        elif to_date_var.get():
            query += " AND date(registered_at) <= ?"
            params.append(to_date_var.get())

        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        return rows
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch data:\n{e}")
        return []
def update_status(owner_id, new_status):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("UPDATE product_owners SET status = ? WHERE owner_id = ?", 
                      (new_status, owner_id))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", f"Status updated to {new_status}")
        display_owners()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to update status: {e}")

def display_audit_log():
    # Clear current audit log display
    for widget in audit_scrollable_frame.winfo_children():
        widget.destroy()
    
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM PO_delete_audit_log ORDER BY deleted_at DESC LIMIT 50")
        logs = cursor.fetchall()
        conn.close()

        if not logs:
            empty_label = ctk.CTkLabel(audit_scrollable_frame, 
                                      text="No deletion records found",
                                      font=("Arial", 12))
            empty_label.pack(pady=20)
            return

        for log in logs:
            log_id, owner_id, deleted_by, deleted_at = log
            
            log_frame = ctk.CTkFrame(audit_scrollable_frame,
                                   border_width=1,
                                   border_color="#D3D3D3",
                                   corner_radius=8)
            log_frame.pack(fill="x", padx=5, pady=3)
            
            log_text = f"ID: {owner_id} | {deleted_at.split()[0]}\nDeleted by: {deleted_by}"
            log_label = ctk.CTkLabel(log_frame,
                                    text=log_text,
                                    font=("Arial", 11),
                                    anchor="w",
                                    justify="left")
            log_label.pack(fill="x", padx=10, pady=5)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to load audit log: {e}")

# ===================== DISPLAY OWNERS ====================

# ===================== EVENT BINDINGS =====================
search_var.trace_add("write", lambda *args: display_owners())
status_filter.bind("<<ComboboxSelected>>", lambda e: display_owners())
#date_filter_var.trace_add("write", lambda *args: display_owners())
from_date_var.trace_add("write", lambda *args: display_owners())
to_date_var.trace_add("write", lambda *args: display_owners())
# ===================== INITIALIZATION =====================
display_owners()
display_audit_log()

# ===================== MAIN LOOP ==========================
app.mainloop()