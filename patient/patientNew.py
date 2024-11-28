import tkinter as tk
import subprocess
from tkinter import messagebox
import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "database"))
sys.path.append(project_root)  # Add the project root to sys.path
from database.database import Database  # Import Database

class New_patient():
    def __init__(self, root):
        self.root = root
        self.root.title("New Patient Registration")
        self.root.geometry("600x600")

        self.db = Database(verbose=True)
    
        patient_root = tk.Toplevel()  # Toplevel for the patient window
        patient_root.title("New Patient Submission")

        h1_label = tk.Label(patient_root, text="Sign up", font=("Arial", 24, "bold"))
        h1_label.pack()

        h2_label = tk.Label(patient_root, text="Welcome! Please fill out the below:", font=("Arial", 18, "bold"))
        h2_label.pack()

        # Personal information fieldset
        form_frame = tk.Frame(patient_root)
        form_frame.pack(padx=10, pady=10)

        fieldset = tk.LabelFrame(form_frame, text="Personal Information", padx=10, pady=10)
        fieldset.grid(row=0, column=0, padx=10, pady=10)

        # Input fields stored
        self.fName_entry = tk.Entry(fieldset)
        self.lName_entry = tk.Entry(fieldset)
        self.age_entry = tk.Entry(fieldset)
        self.address_entry = tk.Entry(fieldset)
        self.diagnosis_entry = tk.Entry(fieldset)
        self.email_entry = tk.Entry(fieldset)
        self.mobile_entry = tk.Entry(fieldset)
        self.ice_entry = tk.Entry(fieldset)
        self.username_entry = tk.Entry(fieldset)
        self.password_entry = tk.Entry(fieldset)

        # Grid layout for form fields
        tk.Label(fieldset, text="First Name:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.fName_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(fieldset, text="Last Name:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.lName_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(fieldset, text="Age:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.age_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(fieldset, text="Home Address:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.address_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(fieldset, text="Diagnosis:").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.diagnosis_entry.grid(row=4, column=1, padx=5, pady=5)

        tk.Label(fieldset, text="Email:").grid(row=5, column=0, sticky="w", padx=5, pady=5)
        self.email_entry.grid(row=5, column=1, padx=5, pady=5)

        tk.Label(fieldset, text="Mobile:").grid(row=6, column=0, sticky="w", padx=5, pady=5)
        self.mobile_entry.grid(row=6, column=1, padx=5, pady=5)

        tk.Label(fieldset, text="ICE Name and Mobile:").grid(row=7, column=0, sticky="w", padx=5, pady=5)
        self.ice_entry.grid(row=7, column=1, padx=5, pady=5)

        tk.Label(fieldset, text="Username:").grid(row=8, column=0, sticky="w", padx=5, pady=5)
        self.username_entry.grid(row=8, column=1, padx=5, pady=5)

        tk.Label(fieldset, text="Password:").grid(row=9, column=0, sticky="w", padx=5, pady=5)
        self.password_entry.grid(row=9, column=1, padx=5, pady=5)

        # Submit Button
        complete_button = tk.Button(patient_root, text="Submit Information", command=self.submit_user)
        complete_button.pack(pady=5)

        # Login Button
        complete_button = tk.Button(patient_root, text="Login", command=self.completeUser)
        complete_button.pack(pady=5)

        db = Database()
        db.printAll()
        db.close()
    
    def submit_user(self):
        # Retrieve input values and add them to the database
        fName = self.fName_entry.get()
        lName = self.lName_entry.get()
        age = self.age_entry.get()
        address = self.address_entry.get()
        diagnosis = self.diagnosis_entry.get()
        email = self.email_entry.get()
        mobile = self.mobile_entry.get()
        ice = self.ice_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Validate inputs (example: ensure required fields are filled)
        if not fName or not lName or not age or not email or not mobile:
            tk.messagebox.showerror("Error", "Please fill out all required fields.")
            return

        try:
            # Insert data into the database
            user_data = {
                "username": email,  # Example: using email as username
                "email": email,
                "password": "defaultpassword123",  # Set default password (later to be changed by user)
                "fName": fName,  # Assume first name is the first word
                "lName": lName,  # Rest as last name
                "type": "patient",
                "emergency_contact_email": ice.split()[-1],  # Assume last word is mobile number
                "emergency_contact_name": " ".join(ice.split()[:-1]),  
                "specialization": diagnosis,  
                "is_disabled": False,
            }

            # Add to the database
            self.db.user.insert(user_data)
            self.db.close()  # Save the changes to the database
            tk.messagebox.showinfo("Success", "New patient registered successfully!")

        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to register patient: {e}")

        
            newValues =(username, email, password, fName, lName, address, age, diagnosis)
        try:
            db = Database()
            # Try to perform the update
            user = db.getRelation("User")
            user.insertRow(newValues=list(newValues))
            db.close() #to save the database
            messagebox.showinfo(
            "Information Updated",
            'Information updated successfully')
        except (IndexError, ValueError, TypeError) as e:
            # Handle specific exceptions raised by editRow
            messagebox.showerror("Update Failed", f"Error adding new patient: {str(e)}")

        else:
            messagebox.showerror("Update Failed", "No new information found.")

    def completeUser(self):
        subprocess.Popen(["python3", "login/login.py"])
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()  # Creates a root window if running standalone
    app = New_patient(root)
    root.mainloop() 