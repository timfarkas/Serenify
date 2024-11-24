import tkinter as tk
import subprocess
import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "database"))
sys.path.append(project_root)  # Add the project root to sys.path

from database.database import Database  # Import Database

class New_patient():

    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("600x600")

        self.db = Database(verbose=True)
    
        patient_root = tk.Toplevel()  # Toplevel for the patient window
        patient_root.title("New Patient Submission")

        h1_label = tk.Label(patient_root, text="Sign up", font=("Arial", 24, "bold"))
        h1_label.pack()

        h2_label = tk.Label(patient_root, text="Welcome! Please fill out the below:", font=("Arial", 18, "bold"))
        h2_label.pack()

        fieldset = tk.LabelFrame(patient_root, text="Personal Information", padx=10, pady=10)
        fieldset.pack(padx=10, pady=10)

        name_label = tk.Label(fieldset, text="Name:")
        name_label.grid(row=0, column=0)
        name_entry = tk.Entry(fieldset)
        name_entry.grid(row=0, column=1)

        age_label = tk.Label(fieldset, text="Age:")
        age_label.grid(row=1, column=0)
        age_entry = tk.Entry(fieldset)
        age_entry.grid(row=1, column=1)

        age_label = tk.Label(fieldset, text="Home address:")
        age_label.grid(row=2, column=0)
        age_entry = tk.Entry(fieldset)
        age_entry.grid(row=2, column=1)

        age_label = tk.Label(fieldset, text="Diagnosis:")
        age_label.grid(row=3, column=0)
        age_entry = tk.Entry(fieldset)
        age_entry.grid(row=3, column=1)

        age_label = tk.Label(fieldset, text="Email:")
        age_label.grid(row=4, column=0)
        age_entry = tk.Entry(fieldset)
        age_entry.grid(row=4, column=1)

        age_label = tk.Label(fieldset, text="Mobile:")
        age_label.grid(row=5, column=0)
        age_entry = tk.Entry(fieldset)
        age_entry.grid(row=5, column=1)

        age_label = tk.Label(fieldset, text="ICE name and mobile:")
        age_label.grid(row=6, column=0)
        age_entry = tk.Entry(fieldset)
        age_entry.grid(row=6, column=1)

        complete_button = tk.Button(root, text="Logout", command=completeUser)
        complete_button.grid(row=11, column=0, columnspan = 6, pady=5)


        def completeUser(self):
            subprocess.Popen(["python3", "patient/patientMain.py"])
            self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()  # Creates a root window if running standalone
    app = New_patient(root)
    root.mainloop() 