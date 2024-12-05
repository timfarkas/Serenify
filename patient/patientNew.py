import tkinter as tk
import subprocess
from tkinter import messagebox
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import Database  # Import Database
from database.entities import Patient

class New_patient():
    def __init__(self, root):
        self.root = root
        self.root.title("New Patient Submission")
        # self.root.geometry("400x600")

        self.db = Database(verbose=True)
    
        # self.root = tk.Toplevel()  # Toplevel for the patient window
        # self.root.title("New Patient Submission")

        h1_label = tk.Label(self.root, text="Sign up", font=("Arial", 24, "bold"))
        h1_label.grid(row=0, column=0, columnspan=2, pady=(10, 5), sticky="nsew")

        h2_label = tk.Label(self.root, text="Welcome! Please fill out the below:", font=("Arial", 18, "bold"))
        h2_label.grid(row=1, column=0, columnspan=2, pady=(0, 10))

        # Personal information fieldset
        fieldset = tk.LabelFrame(self.root, text="Personal Information", padx=10, pady=10)
        fieldset.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        tk.Label(fieldset, text="First Name:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.fName_entry = tk.Entry(fieldset)
        self.fName_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(fieldset, text="Last Name:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.lName_entry = tk.Entry(fieldset)
        self.lName_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(fieldset, text="Email:").grid(row=5, column=0, sticky="w", padx=5, pady=5)
        self.email_entry = tk.Entry(fieldset)
        self.email_entry.grid(row=5, column=1, padx=5, pady=5)

        tk.Label(fieldset, text="ICE Email:").grid(row=7, column=0, sticky="w", padx=5, pady=5)
        self.ice_entry = tk.Entry(fieldset)
        self.ice_entry.grid(row=7, column=1, padx=5, pady=5)

        tk.Label(fieldset, text="ICE Name:").grid(row=8, column=0, sticky="w", padx=5, pady=5)
        self.iceName_entry = tk.Entry(fieldset)
        self.iceName_entry.grid(row=8, column=1, padx=5, pady=5)

        tk.Label(fieldset, text="Username:").grid(row=9, column=0, sticky="w", padx=5, pady=5)
        self.username_entry = tk.Entry(fieldset)
        self.username_entry.grid(row=9, column=1, padx=5, pady=5)

        tk.Label(fieldset, text="Password:").grid(row=10, column=0, sticky="w", padx=5, pady=5)
        self.password_entry = tk.Entry(fieldset, show="*")
        self.password_entry.grid(row=10, column=1, padx=5, pady=5)

        # Buttons at the bottom
        complete_button = tk.Button(self.root, text="Submit Information", command=self.submit_user)
        complete_button.grid(row=3, column=0, columnspan=2, pady=(10, 5))

        login_button = tk.Button(self.root, text="Login", command=self.backToLogin)
        login_button.grid(row=4, column=0, columnspan=2, pady=(0, 10))

    
    def submit_user(self):
        # Retrieve input values and add them to the database
        db = Database()
        fName = self.fName_entry.get()
        lName = self.lName_entry.get()
        email = self.email_entry.get()
        
        emergency_contact_email = self.ice_entry.get()
        emergency_contact_name = self.iceName_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Validate inputs (example: ensure required fields are filled)
        if not fName or not lName or not email:
            tk.messagebox.showerror("Error", "Please fill out all required fields.")
            return
        
        attributeList = (username, email, password, fName, lName, 'Patient', emergency_contact_email, emergency_contact_name, None, False)
        
        try:
            # Try to perform the update
            db = Database()
            user = db.getRelation("User")
            user.insertRow(attributeList=list(attributeList))
            db.close() #to save the database
            messagebox.showinfo(
            "Information Updated",
            'Information updated successfully')
        except (IndexError, ValueError, TypeError) as e:
            # Handle specific exceptions raised by editRow
            messagebox.showerror("Update Failed", f"Error adding new patient: {str(e)}")

    def backToLogin(self):
        subprocess.Popen(["python3", "-m", "login.login"])
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()  # Creates a root window if running standalone
    app = New_patient(root)
    root.mainloop()

####### Used for debugging
# db = Database()
# print("Getting and printing relation 'User':")
# userRelation = db.getRelation('User')
# print(userRelation)