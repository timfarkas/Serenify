import tkinter as tk
from tkinter import messagebox # Users can recieve messages when errors/changes occur when using the site
import subprocess # This allows us to open other files
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import Database  # Import Database
from admin.adminFunctions import AdminMainPage # Linking our admin module to the login
from mhwp.mhwp_dashboard import MHWPDashboard # Linking our mhwp module to the login
from patient.patientMain import Patient # Linking our patient module to the login
from database.dataStructs import Row  
from sessions import Session


class LoginPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("400x400") # Give the page certain sizes

        self.db = Database(verbose=True)
        # Initialize the session instance 
        self.session = Session()  
        self.session.open()

        # H1 equivalent
        h1_label = tk.Label(root, text="Signing in.", font=("Arial", 24, "bold"))
        h1_label.pack()

        # Radio buttons for role selection
        self.user_role = tk.StringVar(value="admin")  # Default radio button is "admin"
        self.role_label = tk.Label(root, text="Please select your user type:")
        self.role_label.pack()
        roles = ["Admin", "MHWP", "Patient"]
        for role in roles:
            tk.Radiobutton(root, text=role.capitalize(), variable=self.user_role, value=role).pack()

        # New patient button
        self.new_button = tk.Button(root, text="New Patient", command=self.newPatientPage)
        self.new_button.pack()

        # Username and password fields
        self.username_label = tk.Label(root, text="Username:")
        self.username_label.pack()
        self.username_entry = tk.Entry(root)
        self.username_entry.pack()
        self.password_label = tk.Label(root, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack()

        # Login button
        self.login_button = tk.Button(root, text="Login", command=self.handle_login)
        self.login_button.pack()

        # Reset password button
        self.reset_button = tk.Button(root, text="Forgotten your password?", command=self.passwordResetPage)
        self.reset_button.pack()

    def handle_login(self):
        # Retrieve inputs
        username = self.username_entry.get()
        password = self.password_entry.get()
        role = self.user_role.get()

        try:
            # Query the database for the user
            user_relation = self.db.getRelation("User")
            user_data = user_relation.getRowsWhereEqual('username', username)
            if not user_data:  # If the user is not found
                messagebox.showerror("Login Failed", "Username not found. Please check your input.")
                return

            # Otherwise, if found, retrieve the user information.
            user_data = user_data[0]
            # Verify the password
            if user_data[3] != password:  # Now we check the password used is correct
                messagebox.showerror("Login Failed", "Invalid password. Please try again.")
                return
            
            if user_data[6] != role:  # Check the role chosen is also correct to the users type
                messagebox.showerror("Login Failed", "Incorrect role. Please try again.")
                return
            
            # If username, password, and role are valid, extract user details as session variables
            for key, value in zip(user_data.labels, user_data.values):
                if key != "password":
                    self.session.set(key=key, value=value)
            # Navigate to the appropriate page based on the user's role
            self.session.close()
            self.findMainPage(username, password, role)

        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def correctDetails(self, username, password, role):
        try:

            self.db.printAll()
            # Query the database for the user
            user_relation = self.db.getRelation("User")
            user_data = user_relation.getRowsWhereEqual('username',username)

            return bool( user_data[0][3] == password)  # Return True if a matching user is found
        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred while checking credentials: {e}")
            return False

    def findMainPage(self, username, password, role):
        # Takes user to the admin main page
        if role == "Admin":
            self.session.open()
            self.session.setRole('Admin')
            self.session.close()
            self.root.destroy()
            self.db.close()
            AdminMainPage()
        # Takes user to the MHWP main page
        elif role == "MHWP":
            self.session.open()
            self.session.setRole('MHWP')
            self.session.close()
            self.root.destroy()
            self.db.close()
            MHWPDashboard()
        # Takes user to the Patient main page
        elif role == "Patient":
            self.session.open()
            self.session.setRole('Patient')
            self.session.close()
            self.root.destroy()
            self.db.close()
            Patient()

        else:
            messagebox.showerror("Error", "Role not recognised.")
    # Takes user to the new patient page
    def newPatientPage(self):
        subprocess.Popen(["python3", "-m", "patient.patientNew"])
        self.root.destroy()
    # Takes user to the reset password page
    def passwordResetPage(self):
        subprocess.Popen(["python3", "-m", "login.resetPassword"])
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginPage(root)
    root.mainloop()