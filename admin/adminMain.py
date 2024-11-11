import tkinter as tk

root = tk.Tk()
root.title("Admin")

# H1 equivalent
h1_label = tk.Label(root, text="Welcome back admin.", font=("Arial", 24, "bold"))
h1_label.pack()

# Table of doctors and their patients
docToPatient = tk.Label(root, text="List of current patients and their doctor:", font=("Arial", 12, "bold"))
docToPatient.pack()
change_button = tk.Button(root, text="Re-Assign")  
change_button.pack()

# Assignment variable to add patients to doctors
assignPatient = tk.Label(root, text="Assign new patients to doctors:", font=("Arial", 12, "bold"))
assignPatient.pack()
# List of new patients goes here #########
# Button to change assignment:
change_button = tk.Button(root, text="Assign")  
change_button.pack()

#Buttons
delete_button = tk.Button(root, text="Delete patient(s)", command='') 
disable_button = tk.Button(root, text="Disable patient(s)")  
summary_button = tk.Button(root, text="Summarise an individual")  
delete_button.pack()
disable_button.pack()
summary_button.pack() 

logout_button = tk.Button(root, text="Logout", command=self.exitUser) 
logout_button.pack()

    def exitUser(self):
        pass
        ######### Inputs #########
        # username = self.username_entry.get()
        # password = self.password_entry.get()
        # role = self.user_role.get()

# Run the application
root.mainloop()