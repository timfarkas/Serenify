import tkinter as tk
from tkinter import messagebox
import subprocess
# import Login ######## THIS NEEDS TO BE CORRECTED #######

class ResetPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Logout")
        self.root.geometry("400x300")

        h1_label = tk.Label(root, text="Reset your password!", font=("Arial", 24, "bold"))
        h1_label.pack()

        fieldset = tk.LabelFrame(root, text="Please enter your email", padx=10, pady=10)
        fieldset.pack(padx=10, pady=10)

        self.name_label = tk.Label(fieldset, text="Email:")
        self.name_label.grid(row=0, column=0)
        self.name_entry = tk.Entry(fieldset)
        self.name_entry.grid(row=0, column=1)

        # Reset button
        self.reset_button = tk.Button(root, text="Reset", command=self.validateEmail)
        self.reset_button.pack()

        # Login button
        self.login_button = tk.Button(root, text="Return", command=self.returnToLogin)
        self.login_button.pack()
    
    def validateEmail(self):
        checkEmail = self.name_entry.get() # Collect users email entered in fieldset
        if self.correctDetails(checkEmail): ######## This must be changed to fit with database data
            messagebox.showerror("Success!", "Sending a password reset link to your email now.")
            subprocess.Popen(["python3", "login.py"])
            self.root.destroy()
        else:
            messagebox.showerror("Error", "No user with this email address.")

    def correctDetails(self, email):
        return email == 'example123@gmail.com' ####### Hard-coded currently - Will use database 

    def returnToLogin(self):
        subprocess.Popen(["python3", "login.py"])
# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = ResetPage(root)
    root.mainloop()