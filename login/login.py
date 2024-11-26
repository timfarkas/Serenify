import tkinter as tk
from tkinter import messagebox
import subprocess # This allows us to open other files
import sys
import os
# project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "database"))
# sys.path.append(project_root)  # Add the project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import Database  # Import Database
# from database.entities import Appointment  
# from database.dataStructs import Row  
# import patient.patientMain
# import admin.adminFunctions
# import mhwp.mhwpMain
# from sessions import Session


class LoginPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("600x600")

        self.db = Database(verbose=True)
        # Initialize the session instance 
        # self.session = Session()  

        # H1 equivalent
        h1_label = tk.Label(root, text="Signing in.", font=("Arial", 24, "bold"))
        h1_label.pack()

        # Radio buttons for role selection
        self.user_role = tk.StringVar(value="admin")  # Default radio button is "admin"
        self.role_label = tk.Label(root, text="Please select your user type:")
        self.role_label.pack()
        roles = ["admin", "mhwp", "patient"]
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
        # Check credentials (replace with real validation logic)
        if self.correctDetails(username, password, role):
            # self.sessionStart()
            self.findMainPage(username, password, role)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
    
    def correctDetails(self, username, password, role):
        try:
            self.db = Database()
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
            exec(open("admin/adminFunctions.py").read())
            self.root.destroy()
        elif role == "mhwp":
            exec(open("mhwp/mhwpMain.py").read())
            self.root.destroy()
        elif role == "patient": 
            exec(open("patient/patientMain.py").read())
            self.root.destroy()
        else:
            messagebox.showerror("Error", "Role not recognised.")

    def newPatientPage(self):
        subprocess.Popen(["python3", "patient/patientNew.py"])
        self.root.destroy()

    def passwordResetPage(self):
        subprocess.Popen(["python3", "login/resetPassword.py"])
        self.root.destroy()

    # def sessionStart(self):
    #     username = self.username_entry.get()
    #     # self.db = Database()
    #     user_relation = self.db.getRelation("User")
    #     user_data = user_relation.getRowsWhereEqual('username',username)
    #     if user_data:
    #         user = user_data[0]
    #         user_id = user[0] 
    #         self.session.set("user_id", user_id)
    #         print(f"User ID {user_id} has been set in the session.")
    #     else:
    #         messagebox.showerror("Login Error", "User not found in the database.")
 
# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = LoginPage(root)
    root.mainloop()