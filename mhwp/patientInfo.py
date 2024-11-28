import sys
import os
import tkinter as tk
from tkinter import messagebox
import subprocess # This allows us to open other files
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import Database
# from database.entities import User, PatientRecord
# from database.initDBwithDummyData import initDummyDatabase
# from sessions import Session
import pandas as pd

# ## Initialize the database with dummy data and save it
# db = Database(overwrite=True)  ### this causes the database to be initialized from scratch and overwrites any changes
# initDummyDatabase(db)
# db.close()

#mhwp_id = 3

class PatientRecords:
    def __init__(self, root, user_id=None):
        # Initialize the session instance 
        # self.session = Session()
        # self.session.open()
        # self.current_user_id = self.session.getId()

        self.root = root
        self.root.title("Patient Records")
        self.root.geometry("700x700")

        self.title_label = tk.Label(root, text=f"Patient Records", font=("Arial", 24, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=2, pady=5)

        #Search Patient Section
        self.patient_list_frame = tk.LabelFrame(root, text="Search Patient", padx=2, pady=5)
        self.patient_list_frame.grid(row=1, column=0, padx=2, pady=5, sticky = "n")

        self.patient_listbox = tk.Listbox(self.patient_list_frame, height=10, width=25)
        self.patient_listbox.pack(side=tk.LEFT, padx=2, pady=5)
        self.patient_listbox.bind('<<ListboxSelect>>', self.load_patient_records)

        self.scrollbar = tk.Scrollbar(self.patient_list_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.patient_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.patient_listbox.yview)

        # Populate List with Patients
        db = Database()
        self.patients = db.getRelation("User")
        self.patients = self.patients.getRowsWhereEqual('type', 'Patient')
        self.patients = pd.DataFrame(self.patients)
        for _, row in self.patients.iterrows():
            user_id = row[0]
            first_name = row[4]
            last_name = row[5]
            full_name = f"{user_id} {first_name} {last_name}"
            self.patient_listbox.insert(tk.END, full_name)

        # Patient Records Section
        self.record_frame = tk.LabelFrame(root, text="Records", padx=2, pady=5)
        self.record_frame.grid(row=1, column=1, padx=2, pady=5, sticky="n")

        self.record_text = tk.Text(self.record_frame, height=15, width=30)
        self.record_text.pack(padx=5, pady=5)
        self.record_text.config(state=tk.DISABLED)

        # Notes Section
        self.note_frame = tk.LabelFrame(root, text="Add Notes", padx=2, pady=5)
        self.note_frame.grid(row=2, column=0, padx=2, pady=5)

        tk.Label(self.note_frame, text="Notes:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.notes_entry = tk.Entry(self.note_frame, width=20)
        self.notes_entry.grid(row=0, column=1, padx=5, pady=5)

        self.save_note_button = tk.Button(self.note_frame, text="Save Note", command=self.save_note)
        self.save_note_button.grid(row=1, column=1, pady=10, sticky="e")

        #Diagnosis Section
        self.note_frame = tk.LabelFrame(root, text="Add or Edit Diagnosis", padx=2, pady=5)
        self.note_frame.grid(row=2, column=1, padx=2, pady=5)

        tk.Label(self.note_frame, text="Diagnosis:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.diagnosis_entry = tk.Entry(self.note_frame, width=20)
        self.diagnosis_entry.grid(row=0, column=1, padx=5, pady=5)

        self.save_button = tk.Button(self.note_frame, text="Save", command=self.save_diagnosis)
        self.save_button.grid(row=2, column=1, pady=10, sticky="e")


    def load_patient_records(self, event):
        """Loads selected patient's records into the text box."""
        selected_index = self.patient_listbox.curselection()
        if not selected_index:
            return

        selected_patient = self.patients.iloc[selected_index[0]]
        patient_id = selected_patient[0] 

        #Loading patient data
        db = Database()
        self.record = db.getRelation("PatientRecord")
        self.record = self.record.getRowsWhereEqual('patient_id', patient_id)
        self.record = pd.DataFrame(self.record)
        # Check if the record is not empty
        if not self.record.empty:
            self.record_text.config(state=tk.NORMAL)
            self.record_text.delete("1.0", tk.END)

            for _, row in self.record.iterrows():
                notes = row[3]
                diagnosis = row[4]

                # Displaying the extracted data
                self.record_text.insert(tk.END, f"Notes: {notes}\n")
                self.record_text.insert(tk.END, f"Diagnosis: {diagnosis}\n\n")
            
            self.record_text.config(state=tk.DISABLED)
        else:
            # If no records are found
            messagebox.showerror("Error", "User not found in the database.")

    def save_note(self):
        """Saves the notes for the selected patient."""
        selected_index = self.patient_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("No Patient Selected", "Please select a patient to save notes.")
            return

        patient_id = self.patients[selected_index[0]]["user_id"]
        notes = self.notes_entry.get()
        
        if not notes:
            messagebox.showwarning("Incomplete Data", "Please provide a note.")
            return

        ####### Save to database

    def save_diagnosis(self):
        """Saves the notes for the selected patient."""
        selected_index = self.patient_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("No Patient Selected", "Please select a patient to save notes.")
            return

        patient_id = self.patients[selected_index[0]]["user_id"]
        diagnosis = self.diagnosis_entry.get()

        if not diagnosis:
            messagebox.showwarning("Incomplete Data", "Please provide a diagnosis.")
            return
        
        ######## Save to database


if __name__ == "__main__":
    root = tk.Tk()
    app = PatientRecords(root)
    root.mainloop()
