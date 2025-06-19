import customtkinter as ctk

class PO_Home(ctk.CTkFrame):
    '''
    =====================================================================================================
    Function: def __init__(self, parent, controller=None)
    Description: 
    This function initializes the PO_Home frame, which is a subclass of CTkFrame
    It sets up the frame to fill the parent window and configures its appearance.
    It creates a title label and three statistic boxes to display quick stats.
    =====================================================================================================
    '''
    def __init__(self, parent, controller=None):
        super().__init__(parent)
        self.controller = controller
        self.configure(fg_color="white")

        # Title
        title = ctk.CTkLabel(self, text="QUICK STATS", font=("Arial", 24, "bold"), text_color="#4A2C14")
        title.pack(pady=(20, 10))

        # Stats grid
        stats_frame = ctk.CTkFrame(self, fg_color="white")
        stats_frame.pack(pady=20)

        self.registered_box = self.create_stat_box(stats_frame, "Products Registered", "2", "#FCE5E5")
        self.pending_box = self.create_stat_box(stats_frame, "Products Pending Approval", "0", "#F1F0FB")
        self.approved_box = self.create_stat_box(stats_frame, "Products Approved", "1", "#FCE5E5")

        self.registered_box.grid(row=0, column=0, padx=10, pady=10)
        self.pending_box.grid(row=0, column=1, padx=10, pady=10)
        self.approved_box.grid(row=0, column=2, padx=10, pady=10)
    '''
    =====================================================================================================
    Function: def create_stat_box(self, parent, title, value, color):
    Description: 
    This function creates a statistic box with a title, value, and background color.
    It returns the created box.
    =====================================================================================================
    '''
    def create_stat_box(self, parent, title, value, color):
        box = ctk.CTkFrame(parent, width=200, height=120, fg_color=color, corner_radius=15)
        box.grid_propagate(False)

        label_title = ctk.CTkLabel(box, text=title, font=("Arial", 14, "bold"), text_color="#4A2C14")
        label_title.pack(pady=(15, 5))

        label_value = ctk.CTkLabel(box, text=value, font=("Arial", 24, "bold"), text_color="#4A2C14")
        label_value.pack()

        return box

# Standalone mode
if __name__ == "__main__":
    ctk.set_appearance_mode("light")  # Optional
    root = ctk.CTk()
    root.title("Home")
    root.geometry("1200x800")

    frame = PO_Home(root)
    frame.pack(fill="both", expand=True)

    root.mainloop()
