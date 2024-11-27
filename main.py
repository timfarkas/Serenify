from sessions import Session
import tkinter as tk
import subprocess 


#We need to have a function that triggers closing session as well ???
#And we need to grab user_id from login as well


class App(tk.Tk):
    ### Initializing application ###
    def __init__(self):
        super().__init__()
        self.title("Serenify Application")
        self.geometry("300x200")
        self.start()
        
    def start(self):
        # Create a Label with a welcome message
        welcome_label = tk.Label(self, text="Welcome to Serenify", font=("Arial", 16))
        welcome_label.pack(pady=20)
        
        # Create a Login button that opens the login screen
        login_button = tk.Button(self, text="Login", command=self.open_login)
        login_button.pack(pady=10)
        
    def open_login(self):
        self.destroy()
        subprocess.Popen(["python3", "login/login.py"])
        
        
if __name__ == "__main__":
    
    ### INITIALIZE SESSION 
    session = Session()
    session._initialize()
    
    app = App()
    app.mainloop()
