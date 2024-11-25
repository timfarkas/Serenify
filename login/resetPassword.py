import tkinter as tk
from tkinter import messagebox
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# from database.entities import Patient
from database import Database
import pandas as pd
import subprocess
from database.initDBwithDummyData import initDummyDatabase
### Initialize the database with dummy data and save it
db = Database(overwrite=True)  ### this causes the database to be initialized from scratch and overwrites any changes
initDummyDatabase(db)

current_user_id = 4

class ResetPage:
    def __init__(self, root, current_user_id):
        self.root = root
        self.root.title("Reset Password")
        self.root.geometry("400x300")
        self.current_user_id = current_user_id
        

        h1_label = tk.Label(root, text="Reset your password", font=("Arial", 24, "bold"))
        h1_label.pack()

        fieldset = tk.LabelFrame(root, text="Enter your username and new password below", padx=10, pady=10)
        fieldset.pack(padx=10, pady=10)

        self.username_label = tk.Label(self.root, text="Username:")
        self.username_label.grid(row=2, column=0, padx=10, pady=10)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.grid(row=2, column=1, padx=10, pady=10)
        
        self.new_password_label = tk.Label(root, text="New Password")
        self.new_password_label.grid(row=5, column=0, padx=10, pady=10)
        self.new_password_entry = tk.Entry(root, show="*")
        self.new_password_entry.grid(row=5, column=1, padx=10, pady=10)

        # Reset button
        self.reset_button = tk.Button(root, text="Reset", command=self.validateUsername)
        self.reset_button.pack()

        # Login button
        self.login_button = tk.Button(root, text="Return to login", command=self.returnToLogin)
        self.login_button.pack()
    
    def match_in_database(self, username, new_password):
        # Check if the provided details match the database
        db = Database()
        user_info = db.getRelation("User")
        user_info = user_info.getRowsWhereEqual('user_id', self.current_user_id)
        user_info = pd.DataFrame(user_info)

        if not user_info.empty:
            # Compare input data with current database values
            db_username = user_info.iloc[0][1]
            db_password = user_info.iloc[0][3]

            # If any field is different, we allow the update
            return (new_password != db_password)
        else:
            return False

    def update_info (self):
        # Retrieve data from the entry fields
        username = self.username_entry.get()
        self.old_password = self.old_password_entry.get()
        new_password = self.new_password_entry.get()
        self.confirm_password = self.confirm_password_entry.get()

        db = Database()
        user = db.getRelation("User")
        user = user.getRowsWhereEqual('user_id', self.current_user_id)
        user = pd.DataFrame(user)
        current_password = user.iloc[0][3]
        x = user.iloc[0][6] # Want to preserve all other information in database
        y = user.iloc[0][9]
        # z = user.iloc[0][10] #what if i want to preserve disabled info in case its TRUE ? im getting error if i use it

        if  self.match_in_database(username, new_password):
               # If the password fields are not empty, will require password verification
            if new_password or self.confirm_password:
                # Check if the old password was entered correctly
                if self.old_password != current_password:
                    messagebox.showerror("Password Mismatch", "The old password you entered is incorrect.")
                    return

            newValues = (username, new_password if new_password else current_password)
            try:
                # Try to perform the update
                user = db.getRelation("User")
                user.editRow(primaryKey=self.current_user_id, newValues=list(newValues))
                db.close() #to save the database
                # Mask the password with asterisks
                masked_password = '*' * len(new_password)
                messagebox.showinfo(
                "Information Updated",
                'Information updated successfully')
            except (IndexError, ValueError, TypeError) as e:
                # Handle specific exceptions raised by editRow
                messagebox.showerror("Update Failed", f"Error updating information: {str(e)}")

        else:
            messagebox.showerror("Update Failed", "No new information found.")


    def returnToLogin(self):
        exec(open("login.py").read())
        self.root.destroy()

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = ResetPage(root, current_user_id)
    root.mainloop()