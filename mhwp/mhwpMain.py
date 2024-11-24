import tkinter as tk
import subprocess

root = tk.Tk()
root.title("mhwp")

# H1 equivalent
h1_label = tk.Label(root, text="Welcome back practioner", font=("Arial", 24, "bold"))
h1_label.pack()

# Table of patients
patient = tk.Label(root, text="List of current patients:", font=("Arial", 12, "bold"))
patient.pack()

patient1 = tk.Label(root, text="patient1", font=("Arial", 12, "bold"))
patient1.pack()
patient1_button = tk.Button(root, text="Add/view patient info")
patient1_button.pack()
patient2 = tk.Label(root, text="patient2", font=("Arial", 12, "bold"))
patient2.pack()
patient2_button = tk.Button(root, text="Add/view patient info")
patient2_button.pack()
patient3 = tk.Label(root, text="patient3", font=("Arial", 12, "bold"))
patient3.pack()
patient3_button = tk.Button(root, text="Add/view patient info")
patient3_button.pack()

# List of bookings accepted
assignPatient = tk.Label(root, text="Current bookings:", font=("Arial", 12, "bold"))
assignPatient.pack()

# Bookings requested
assignPatient = tk.Label(root, text="Requested bookings:", font=("Arial", 12, "bold"))
assignPatient.pack()

see_request_button1 = tk.Button(root, text="View")  
see_request_button2 = tk.Button(root, text="View")  
see_request_button3 = tk.Button(root, text="View")  
see_request_button4 = tk.Button(root, text="View")  
see_request_button1.pack()
see_request_button2.pack()
see_request_button3.pack()
see_request_button4.pack()

#Buttons
dashboard_button = tk.Button(root, text="Patient dashboard") 
dashboard_button.pack()

# logout button
logout_button = tk.Button(root, text="Logout", command=self.exitUser) 
logout_button.pack()

def exitUser(self):
    subprocess.Popen(["python3", "login/logout.py"])
    self.root.destroy()

        ######### Inputs #########
        # username = self.username_entry.get()
        # password = self.password_entry.get()
        # role = self.user_role.get()

# Run the application
root.mainloop()