import tkinter as tk
from tkinter import messagebox
import subprocess # This allows us to open other files
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import Database  # Import Database
from admin.adminFunctions import AdminMainPage
from mhwp.mhwp_dashboard import MHWPDashboard
from patient.patientMain import Patient
# from database.entities import Appointment
from database.dataStructs import Row  
from sessions import Session

class LoginPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("400x400")

        self.db = Database(verbose=True)
        # Initialize the session instance 
        self.session = Session()  
        self.session.open()

        # H1 equivalent
        h1_label = tk.Label(root, text="Please sign in", font=("Arial", 24, "bold"))
        h1_label.pack()

        # Radio buttons for role selection
        # self.user_role = tk.StringVar(value="admin")  # Default radio button is "admin"
        # self.role_label = tk.Label(root, text="Please select your user type:")
        # self.role_label.pack()
        # roles = ["Admin", "MHWP", "Patient"]
        # for role in roles:
        #     tk.Radiobutton(root, text=role.capitalize(), variable=self.user_role, value=role).pack()

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

        # New patient button
        self.new_button = tk.Button(root, text="New Patient", command=self.newPatientPage)
        self.new_button.pack()

    def handle_login(self):
        # Retrieve inputs
        username = self.username_entry.get()
        password = self.password_entry.get()
        # selected_role = self.user_role.get()

        try:
            # Query the database for the user
            user_relation = self.db.getRelation("User")
            user_data = user_relation.getRowsWhereEqual('username', username)

            if not user_data:  # Check if no user was found before indexing
                messagebox.showerror("Login Failed", "Username not found. Please check your input.")
                return

            # Gets the first matching username
            user_data = user_data[0]

            password_index = 3  
            # role_index = 6      

            # Verify the password
            if user_data[password_index] != password:
                messagebox.showerror("Login Failed", "Invalid password. Please try again.")
                return

            # # Verify the role
            # if user_data[role_index] != selected_role:
            #     messagebox.showerror("Login Failed", f"Invalid role selection. You are registered as a {user_data[role_index]}.")
            #     return

            # Successful login
            for key, value in zip(user_data.labels, user_data.values):  
                if key != "password":
                    self.session.set(key=key, value=value)

            self.findMainPage(username, password)

        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def correctDetails(self, username, password):
        try:
            
            # self.db.printAll()
            # Query the database for the user
            user_relation = self.db.getRelation("User")
            user_data = user_relation.getRowsWhereEqual('username',username)
           
            return bool( user_data[0][3] == password)  # Return True if a matching user is found
        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred while checking credentials: {e}")
            return False
        


    def findMainPage(self, username, password, role):
        # Takes user to the main page
        if role == "admin":
            self.session.open()
            self.session.setRole('Admin')
            self.session.close()
            self.root.destroy()
            self.db.close()
            AdminMainPage()
            # exec(open("admin/adminFunctions.py").read())
        elif role == "mhwp":
            self.session.open()
            self.session.setRole('MHWP')
            self.session.close()
            self.root.destroy()
            self.db.close()
            MHWPDashboard()
            # exec(open("mhwp/mhwp_dashboard.py").read())
        elif role == "patient":
            self.session.open()
            self.session.setRole('Patient')
            self.session.close()
            self.root.destroy()
            self.db.close()
            Patient()

        else:
            messagebox.showerror("Error", "Role not recognised.")

    def newPatientPage(self):
        subprocess.Popen(["python3", "-m", "patient.patientNew"])
        self.root.destroy()

    def passwordResetPage(self):
        subprocess.Popen(["python3", "-m", "login.resetPassword"])
        self.root.destroy()
 
# Run the login page
if __name__ == "__main__":
    root = tk.Tk()
    app = LoginPage(root)
    root.mainloop()