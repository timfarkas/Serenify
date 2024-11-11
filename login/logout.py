import tkinter as tk
import subprocess
# import Login ######## THIS NEEDS TO BE CORRECTED #######

class LogoutPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Logout")
        self.root.geometry("400x300")

        h1_label = tk.Label(root, text="Logout successful!", font=("Arial", 24, "bold"))
        h1_label.pack()

        # Login button
        self.login_button = tk.Button(root, text="Login", command=self.loginButton)
        self.login_button.pack()

    def exitUser(self):
        pass
        ######### Inputs #########
        # username = self.username_entry.get()
        # password = self.password_entry.get()
        # role = self.user_role.get()

    def loginButton(self):
        subprocess.Popen(["python3", "login.py"])
        self.root.destroy()

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = LogoutPage(root)
    root.mainloop()