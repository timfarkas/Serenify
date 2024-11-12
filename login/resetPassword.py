import tkinter as tk
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
        self.reset_button = tk.Button(root, text="Reset", command=self.resetButton)
        self.reset_button.pack()
    
    def validateEmail(self):
        checkEmail = self.name_entry.get() # Collect users email entered in fieldset
        if self.correctDetails(checkEmail): # This must be changed to fit with database data
            self.resetButton()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def correctDetails(self):
        if self.name_entry == 'example123@gmail.com':
            print("This email is in our database! Sending you a password reset link now")
            return True


    def resetButton(self):
        subprocess.Popen(["python3", "login.py"])
        self.root.destroy()

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = ResetPage(root)
    root.mainloop()