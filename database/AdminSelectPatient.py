import tkinter as tk
from tkinter import messagebox
from database import Database
from AdminEditPatient import UserEditApp

class PatientSelectionApp:
    def __init__(self, root):
        self.db = Database()
        self.root = root
        self.patient_vars = {}
        self.users = self.db.getRelation('Users').getRowsWhereEqual("type", "Patient")
        self.create_ui()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_ui(self):
        self.root.title("Edit Patients")

        # H1 equivalent
        h1_label = tk.Label(self.root, text="Welcome back admin", font=("Arial", 24, "bold"))
        h1_label.pack()
        
        # instruction label
        docToPatient = tk.Label(self.root, text="Choose the patient(s) to edit:", font=("Arial", 12, "bold"))
        docToPatient.pack()

        # creating checkbox for each patient
        for user in self.users:
            patient_name = f"{user[4]} {user[5]}"
            patient_var = tk.BooleanVar()
            check_button = tk.Checkbutton(self.root, text=patient_name, variable=patient_var)
            check_button.pack(anchor="w")

            # store the id associated with the patient
            self.patient_vars[user[0]] = patient_var

        # select Button 
        select_button = tk.Button(self.root, text="Select patient", command=self.edit_patient)  
        select_button.pack()

    def edit_patient(self):
        selected_patient_id = None
        for user_id, patient_var in self.patient_vars.items():
            if patient_var.get():
                selected_patient_id = user_id
                break
        if selected_patient_id:
            self.root.withdraw()
            edit_window = tk.Toplevel(self.root)
            app = UserEditApp(edit_window, selected_patient_id)
        else:
            messagebox.showinfo("No Patient Selected", "No Patient selected, please try again.")

    def on_close(self):
        self.db.close()
        self.root.destroy()

# create main window
root = tk.Tk()

app = PatientSelectionApp(root)

# Run the application
root.mainloop()


# check_var = tk.BooleanVar()

    ####### Back button - needs completing #######
    # self.back_button = tk.Button(root, text="Login", command=self.backButton)
    # self.back_button.pack()

    # def backButton(self):
    #     subprocess.Popen(["python3", "adminMain.py"])
    #     self.root.destroy()

