import tkinter as tk
from tkinter import messagebox
from database import Database

class PatientDeletionApp:
    def __init__(self, root):
        self.db = Database()
        self.root = root
        self.patient_vars = {}
        self.users = self.db.getRelation('Users').getRowsWhereEqual("type", "Patient")
        self.create_ui()

    def create_ui(self):
        self.root.title("Delete Patients")

        # H1 equivalent
        h1_label = tk.Label(self.root, text="Welcome back admin", font=("Arial", 24, "bold"))
        h1_label.pack()
        
        # instruction label
        docToPatient = tk.Label(self.root, text="Choose the patient(s) to delete:", font=("Arial", 12, "bold"))
        docToPatient.pack()

        # Creating checkbox for each patient
        for user in self.users:
            patient_name = f"{user[4]} {user[5]}"
            patient_var = tk.BooleanVar()
            check_button = tk.Checkbutton(self.root, text=patient_name, variable=patient_var)
            check_button.pack(anchor="w")

            # store the id associated with the patient
            self.patient_vars[user[0]] = patient_var

        # Delete Button 
        delete_button = tk.Button(self.root, text="Delete patient", command=self.delete_patient)  
        delete_button.pack()

    def delete_patient(self):
        userRelation = self.db.getRelation('Users')
        deleted_count = 0
        
        #loop through patient IDs and check if checkbox is selected
        for user_id, var in self.patient_vars.items():
            if var.get():
                userRelation.dropRows(id=user_id)
                deleted_count += 1
        
        #user feedback
        if deleted_count > 0:
            messagebox.showinfo("Success", f"Success, {deleted_count} patient(s) deleted")
        else:
            messagebox.showinfo("No Selection", "No patient deleted, please try again")

    def close_db(self):
        self.db.close()

# create main window
root = tk.Tk()

app = PatientDeletionApp(root)

# Run the application
root.mainloop()

db.close() # Save the database state and closes it 


# check_var = tk.BooleanVar()

    ####### Back button - needs completing #######
    # self.back_button = tk.Button(root, text="Login", command=self.backButton)
    # self.back_button.pack()

    # def backButton(self):
    #     subprocess.Popen(["python3", "adminMain.py"])
    #     self.root.destroy()

