import tkinter as tk
from tkinter import messagebox
import subprocess # This allows us to open other files

class LoginPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("400x300")


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
        self.login_button = tk.Button(root, text="New Patient", command=self.newPatientPage)
        self.login_button.pack()

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

    def handle_login(self):
        # Retrieve inputs
        username = self.username_entry.get()
        password = self.password_entry.get()
        role = self.user_role.get()

        # Check credentials (replace with real validation logic)
        if self.correctDetails(username, password, role):
            self.findMainPage(role)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
    
    def correctDetails(self, username, password, role):
        ################ THESE MUST BE REPLACED WITH DATABASE DATA!!!!!!!! ##############
        if role == "admin" and username == "admin" and password == "admin123":
            return True
        elif role == "mhwp" and username == "mhwp" and password == "mhwp123":
            return True
        elif role == "patient" and username == "patient" and password == "patient123":
            return True
        else:
            return False

    def findMainPage(self, role):
        # Takes user to the main page
        if role == "admin":
            subprocess.Popen(["python3", "admin/adminMain.py"])
            self.root.destroy()
        elif role == "mhwp":
            subprocess.Popen(["python3", "mhwp/mhwpMain.py"])
            self.root.destroy()
        elif role == "patient": 
            subprocess.Popen(["python3", "patient/patientMain.py"])
            self.root.destroy()
        else:
            messagebox.showerror("Error", "Role not recognised.")

    def newPatientPage(self):
        subprocess.Popen(["python3", "patient/patientNew.py"])
        self.root.destroy()

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = LoginPage(root)
    root.mainloop()