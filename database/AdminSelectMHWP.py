import tkinter as tk
from tkinter import messagebox
from database import Database
from AdminEditPatient import UserEditApp

class MHWPSelectionApp:
    def __init__(self, root):
        self.db = Database()
        self.root = root
        self.MHWP_vars = {}
        self.users = self.db.getRelation('Users').getRowsWhereEqual("type", "MHWP")
        self.create_ui()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_ui(self):
        self.root.title("Select MHWP")

        # H1 equivalent
        h1_label = tk.Label(self.root, text="Welcome back admin", font=("Arial", 24, "bold"))
        h1_label.pack()
        
        # instruction label
        docToMHWP = tk.Label(self.root, text="Choose the MHWP to edit:", font=("Arial", 12, "bold"))
        docToMHWP.pack()

        # creating checkbox for each MHWP
        for user in self.users:
            MHWP_name = f"{user[4]} {user[5]}"
            MHWP_var = tk.BooleanVar()
            check_button = tk.Checkbutton(self.root, text=MHWP_name, variable=MHWP_var)
            check_button.pack(anchor="w")

            # store the id associated with the MHWP
            self.MHWP_vars[user[0]] = MHWP_var

        # select Button 
        select_button = tk.Button(self.root, text="Select MHWP", command=self.edit_MHWP)  
        select_button.pack()

    def edit_MHWP(self):
        selected_MHWP_id = None
        for user_id, MHWP_var in self.MHWP_vars.items():
            if MHWP_var.get():
                selected_MHWP_id = user_id
                break
        if selected_MHWP_id:
            self.root.withdraw()
            edit_window = tk.Toplevel(self.root)
            app = UserEditApp(edit_window, selected_MHWP_id)
        else:
            messagebox.showinfo("No MHWP Selected", "No MHWP selected, please try again.")

    def on_close(self):
        self.db.close()
        self.root.destroy()

# create main window
root = tk.Tk()

app = MHWPSelectionApp(root)

# Run the application
root.mainloop()


# check_var = tk.BooleanVar()

    ####### Back button - needs completing #######
    # self.back_button = tk.Button(root, text="Login", command=self.backButton)
    # self.back_button.pack()

    # def backButton(self):
    #     subprocess.Popen(["python3", "adminMain.py"])
    #     self.root.destroy()

