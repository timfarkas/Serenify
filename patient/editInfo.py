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
# db.close()

##SHOULD WE ADD EMERGENCY CONTACT NAME except just email
current_user_id = 4 #change when sessions become active 
## Hashing passwords??

class EditInfo:
    def __init__(self, root, current_user_id):
        self.root = root
        self.root.title("Patient")
        self.root.geometry("500x700")
        self.current_user_id = current_user_id

        # Title label
        self.title_label = tk.Label(root, text="Personal Information", font=("Arial", 24, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=6, pady=10)

        self.t_label = tk.Label(root, text="Edit your personal information here:", font=("Arial", 12))
        self.t_label.grid(row=1, column=0, columnspan = 6, pady=10)

        # UI components
        self.create_widgets()
        self.load_current_info()

    def create_widgets(self):
        # Create entry fields and labels for name, email, passwords, first name, last name, emergency contact email
        self.username_label = tk.Label(self.root, text="Username:")
        self.username_label.grid(row=2, column=0, padx=10, pady=10)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.grid(row=2, column=1, padx=10, pady=10)

        self.email_label = tk.Label(self.root, text="Email:")
        self.email_label.grid(row=3, column=0, padx=10, pady=10)
        self.email_entry = tk.Entry(self.root)
        self.email_entry.grid(row=3, column=1, padx=10, pady=10)

        self.old_password_label = tk.Label(root, text="Old Password")
        self.old_password_label.grid(row=4, column=0, padx=10, pady=10)
        self.old_password_entry = tk.Entry(root, show="*")
        self.old_password_entry.grid(row=4, column=1, padx=10, pady=10)

        self.new_password_label = tk.Label(root, text="New Password")
        self.new_password_label.grid(row=5, column=0, padx=10, pady=10)
        self.new_password_entry = tk.Entry(root, show="*")
        self.new_password_entry.grid(row=5, column=1, padx=10, pady=10)

        self.confirm_password_label = tk.Label(root, text="Confirm New Password")
        self.confirm_password_label.grid(row=6, column=0, padx=10, pady=10)
        self.confirm_password_entry = tk.Entry(root, show="*")
        self.confirm_password_entry.grid(row=6, column=1, padx=10, pady=10)

        self.fname_label = tk.Label(self.root, text="First Name:")
        self.fname_label.grid(row=7, column=0, padx=10, pady=10)
        self.fname_entry = tk.Entry(self.root)
        self.fname_entry.grid(row=7, column=1, padx=10, pady=10)

        self.lname_label = tk.Label(self.root, text="Last Name:")
        self.lname_label.grid(row=8, column=0, padx=10, pady=10)
        self.lname_entry = tk.Entry(self.root)
        self.lname_entry.grid(row=8, column=1, padx=10, pady=10)

        self.emergency_contact_name_label = tk.Label(self.root, text="Emergency Contact Name:")
        self.emergency_contact_name_label.grid(row=9, column=0, padx=10, pady=10)
        self.emergency_contact_name_entry = tk.Entry(self.root)
        self.emergency_contact_name_entry.grid(row=9, column=1, padx=10, pady=10)
        
        self.emergency_contact_email_label = tk.Label(self.root, text="Emergency Contact Email:")
        self.emergency_contact_email_label.grid(row=10, column=0, padx=10, pady=10)
        self.emergency_contact_email_entry = tk.Entry(self.root)
        self.emergency_contact_email_entry.grid(row=10, column=1, padx=10, pady=10)
    
        
        # Update Button
        self.update_button = tk.Button(self.root, text="Update Information", command=self.update_info)
        self.update_button.grid(row=11, column=0, columnspan=2, pady=20)

        #Back button
        self.back_button = tk.Button(root, text="Back to the main page", command=self.backButton)
        self.back_button.grid(row=12, column=0, columnspan=2, pady=5)


    def backButton(self):
        subprocess.Popen(["python3", "mhwpMain.py"])
        self.root.destroy()
    
    def load_current_info(self):
        db = Database()
        user_info = db.getRelation("User")
        user_info = user_info.getRowsWhereEqual('user_id', self.current_user_id)
        user_info = pd.DataFrame(user_info)
        if not user_info.empty:
            #Accessing the columns using the numeric index
            #1 - username; 2 - email; 3 - password; 4 - first name; 5 - last name; 
            #8 - emergency contact name; 9 - emergency contact email
            # keeping password entries empty 
            self.username_entry.insert(0, user_info.iloc[0][1] if pd.notna(user_info.iloc[0][1]) else "")
            self.email_entry.insert(0, user_info.iloc[0][2] if pd.notna(user_info.iloc[0][2]) else "")
            self.fname_entry.insert(0, user_info.iloc[0][4] if pd.notna(user_info.iloc[0][4]) else "")
            self.lname_entry.insert(0, user_info.iloc[0][5] if pd.notna(user_info.iloc[0][5]) else "")
            self.emergency_contact_name_entry.insert(0, user_info.iloc[0][8] if pd.notna(user_info.iloc[0][8]) else "")
            self.emergency_contact_email_entry.insert(0, user_info.iloc[0][7] if pd.notna(user_info.iloc[0][7]) else "")
        else:
            messagebox.showerror("Error", "User not found in the database.")

    def match_in_database(self, username, email, new_password, fname, lname, emergency_contact_name, emergency_contact_email):
        # Check if the provided details match the database
        db = Database()
        user_info = db.getRelation("User")
        user_info = user_info.getRowsWhereEqual('user_id', self.current_user_id)
        user_info = pd.DataFrame(user_info)

        if not user_info.empty:
            # Compare input data with current database values
            db_username = user_info.iloc[0][1]
            db_email = user_info.iloc[0][2]
            db_password = user_info.iloc[0][3]
            db_fname = user_info.iloc[0][4]
            db_lname = user_info.iloc[0][5]
            db_emergency_contact_name = user_info.iloc[0][8]
            db_emergency_contact_email = user_info.iloc[0][7]

            # If any field is different, we allow the update
            return (username != db_username or email != db_email or new_password != db_password or 
                    fname != db_fname or lname != db_lname or emergency_contact_email != db_emergency_contact_email or emergency_contact_name != db_emergency_contact_name)
        else:
            return False

    def update_info (self):
        # Retrieve data from the entry fields
        username = self.username_entry.get()
        email = self.email_entry.get()
        self.old_password = self.old_password_entry.get()
        new_password = self.new_password_entry.get()
        self.confirm_password = self.confirm_password_entry.get()
        fname = self.fname_entry.get()
        lname = self.lname_entry.get()
        emergency_contact_email = self.emergency_contact_email_entry.get()
        emergency_contact_name = self.emergency_contact_name_entry.get()

        db = Database()
        user = db.getRelation("User")
        user = user.getRowsWhereEqual('user_id', self.current_user_id)
        user = pd.DataFrame(user)
        current_password = user.iloc[0][3]
        x = user.iloc[0][6] # Want to preserve all other information in database
        y = user.iloc[0][9]
        # z = user.iloc[0][10] #what if i want to preserve disabled info in case its TRUE ? im getting error if i use it

        if  self.match_in_database(username, email, new_password, fname, lname, emergency_contact_email, emergency_contact_name):
               # If the password fields are not empty, will require password verification
            if new_password or self.confirm_password:
                # Check if the old password was entered correctly
                if self.old_password != current_password:
                    messagebox.showerror("Password Mismatch", "The old password you entered is incorrect.")
                    return

                # Check if the new password and confirmation match
                if new_password != self.confirm_password:
                    messagebox.showerror("Password Mismatch", "The new passwords do not match.")
                    return

            newValues =(username, email, new_password if new_password else current_password, fname, lname, x, emergency_contact_email, emergency_contact_name, y, False)
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

    def backButton(self):
        subprocess.Popen(["python3", "patient/patientMain.py"])
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = EditInfo(root, current_user_id)
    root.mainloop()
# db = Database()
# print("Getting and printing relation 'User':")
# userRelation = db.getRelation('User')
# print(userRelation)