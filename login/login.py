import tkinter as tk
from tkinter import messagebox
import subprocess # This allows us to open other files

class LoginPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("400x300")


        # H1 equivalent
        h1_label = tk.Label(root, text="Sign up", font=("Arial", 24, "bold"))
        h1_label.pack()

        # Radio buttons for role selection
        self.role_label = tk.Label(root, text="Select Role:")
        self.role_label.pack()
        roles = ["admin", "doctor", "patient", "new patient"]
        for role in roles:
            tk.Radiobutton(root, text=role.capitalize(), variable=self.user_role, value=role).pack()

        # Set default role to None
        self.user_role = tk.StringVar(value="admin")  # Default radio button is "admin"
        
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
        login_button = tk.Button(root, text="Login")
        login_button.pack()

    def findMainPage(self, role):
        # Takes user to the main page
        if role == "admin" #FINISHHHHHHHHHH
class findMainPage():
    def __init__(self, name_entry, password_entry):
        self.name_entry = name_entry
        self.password_entry = password_entry

    def adminDirect(self):
        if name_entry == name_entry logged in pandas:
    if password_entry == password_entry in pandas:
        print('Login successful!')
        Need to link this to the radio buttons
    def patientDirect(self):
        if name_entry == name_entry logged in pandas:
    if password_entry == password_entry in pandas:
        print('Login successful!')
        Need to link this to the radio buttons
    def newPatientDirect(self):
        if name_entry == name_entry logged in pandas:
    if password_entry == password_entry in pandas:
        print('Login successful!')
        Need to link this to the radio buttons
    def mhwpDirect(self):
        if name_entry == name_entry logged in pandas:
    if password_entry == password_entry in pandas:
        print('Login successful!')
        Need to link this to the radio buttons
    

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = LoginPage(root)
    root.mainloop()