from sessions import Session
import tkinter as tk
import subprocess 


#We need to have a function that triggers closing session as well ???
#And we need to grab user_id from login as well


class AppMeta(type):
    ### Meta class ###
    def __call__(cls, *args, **kwargs):
        instance = super().__call__(*args, **kwargs)
        instance.start()
        return instance

class App(tk.Tk, metaclass=AppMeta):
    ### Initializing application ###
    def __init__(self):
        super().__init__()
        self.title("Serenity Application")
        self.geometry("300x200")
        
    def start(self):
        # Create a Label with a welcome message
        welcome_label = tk.Label(self, text="Welcome to Serenity", font=("Arial", 16))
        welcome_label.pack(pady=20)
        
        # Create a Login button that opens the login screen
        login_button = tk.Button(self, text="Login", command=self.open_login)
        login_button.pack(pady=10)
        
    def open_login(self):
        subprocess.Popen(["python3", "login/login.py"])
        # self.root.destroy()
        
if __name__ == "__main__":
    ### INITIALIZE SESSION 
    # (do this just once when opening the app)
    session = Session()
    session._initialize()

    app = App()
    app.mainloop()

    ### SET ID AND ROLE (DO THIS AFTER EACH SUCCESSFUL LOGIN)
    session.setId(4)
    session.setRole("MHWP")

    ### SET EXTRA DETAILS, e.g. isDisabled
    session.set("isDisabled", True)

    session.close() ## this saves the session
