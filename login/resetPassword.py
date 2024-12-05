import tkinter as tk
from tkinter import messagebox
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import Database
import pandas as pd
import subprocess


class ResetPage():
    def __init__(self, root=None):
        self.root = root
        self.root.title("Reset Password")
        self.root.geometry("400x300")

        # Title 
        h1_label = tk.Label(root, text="Reset your password", font=("Arial", 24, "bold"))
        h1_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Initialising a fieldset to gather user info
        fieldset = tk.LabelFrame(root, text="Enter your username and new password below", padx=10, pady=10)
        fieldset.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        # Username field
        self.username_label = tk.Label(root, text="Username:")
        self.username_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.username_entry = tk.Entry(root)
        self.username_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        # New password field
        self.new_password_label = tk.Label(root, text="New Password:")
        self.new_password_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.new_password_entry = tk.Entry(root, show="*")
        self.new_password_entry.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

        # Reset button
        self.reset_button = tk.Button(root, text="Reset", command=lambda: self.changePassword(self.username_entry.get(), self.new_password_entry.get()))
        self.reset_button.grid(row=4, column=0, columnspan=2, pady=10)

        # Login button
        self.login_button = tk.Button(root, text="Return to login", command=self.returnToLogin)
        self.login_button.grid(row=5, column=0, columnspan=2, pady=10)

    def changePassword(self, username, password):
        # Open the database
        db = Database()
        print('This should only execute once the user clicks submit...')
        if self.match_in_database(username):
            matching_ids = self.match_in_database(username)
            if matching_ids:  # Check if any IDs matched
                self.updatePassword(matching_ids[0], password) # We update that users password to their new input
            db.close()
            print("Password successfully changed")
            messagebox.showinfo("Success", "Password successfully changed")
        else: # Else statement used so that username must already be in the database
            print("No information found under the chosen username")
            messagebox.showerror("Reset failed", "No information found under the chosen username")
            db.close() # Important to close database so that it saves changes
    
    def match_in_database(self, username):
        # Check if the provided details match the database
        db = Database()
        user_info = db.getRelation("User")
        matching_ids = user_info.getIDsWhereEqual('username', username)
        print(matching_ids)
        db.close()
        return matching_ids

    def updatePassword(self, id, password):
        # Update the entered usernames password with their new input
        db = Database()
        userRelation = db.getRelation('User')
        print(f"Updating password for user_id: {id}")
        userRelation.editFieldInRow(id, targetAttribute='password', value=password)
        db.printAll()
        db.close()
        print(f"Password updated and database saved successfully.")
    
    # Takes user to the login page
    def returnToLogin(self):
        subprocess.Popen(["python3", "-m", "login.login"])
        self.root.destroy()

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = ResetPage(root=root)

    root.mainloop()