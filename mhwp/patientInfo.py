import sys
import os
import tkinter as tk
from tkinter import messagebox
import subprocess # This allows us to open other files
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.entities import PatientRecord
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


    def load_patient_records(self, event=None):
        """Loads selected patient's records into the text box."""
        selected_index = self.patient_listbox.curselection()
        if not selected_index:
            return

        selected_patient = self.patients.iloc[selected_index[0]]
        patient_id = selected_patient[0]
        #db.close()

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
        # Get selected patient index and validate selection
        selected_index = self.patient_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("No Patient Selected", "Please select a patient to save notes.")
            return
        # Extract patient ID and new note text
        patient_id = int(self.patients.iloc[selected_index[0]][0]) # manually typecasting as otherwise it throws a type error
        new_note = self.notes_entry.get()
        if not new_note:
            messagebox.showwarning("Incomplete Data", "Please provide notes.")
            return

        try:
            # Connect to database and get existing records
            db = Database()
            records_relation = db.getRelation("PatientRecord")
            existing_records = records_relation.getRowsWhereEqual('patient_id', patient_id)

            #Initialise variables for existing data
            existing_notes = ""
            conditions = []
            if existing_records:
                existing_notes = existing_records[0][3]
                conditions = existing_records[0][4]

            # Combine existing notes with new note
            combined_notes = f"{existing_notes}\nDiagnosis: ['Depression']\n\nNotes: {new_note}" if existing_notes else new_note

            # Create and save new patient record
            new_record = PatientRecord(
                patient_id=patient_id,
                mhwp_id=3,
                notes=combined_notes,
                conditions=conditions if conditions else []
            )
            print("Before save:", self.record)
            db.insert_patient_record(new_record)
            print("After save:", db.getRelation("PatientRecord").getRowsWhereEqual('patient_id', patient_id))

            # Cleanup and refresh display
            db.close()
            db = Database()
            self.load_patient_records(None)
            self.notes_entry.delete(0, tk.END)
            messagebox.showinfo("Success", "Notes saved successfully")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save notes: {str(e)}")


    def save_diagnosis(self):
        """Saves the notes for the selected patient."""
        # Get selected patient index and validate selection
        selected_index = self.patient_listbox.curselection()
        print("Patient selection:", self.patients.iloc[selected_index[0]])
        if not selected_index:
            messagebox.showwarning("No Patient Selected", "Please select a patient to save notes.")
            return

        # Extract patient ID and new diagnosis
        patient_id = int(self.patients.iloc[selected_index[0]][0]) # manually typecasting as otherwise it throws a type error
        new_diagnosis = self.diagnosis_entry.get()

        if not new_diagnosis:
            messagebox.showwarning("Incomplete Data", "Please provide a diagnosis.")
            return

        try:
            # Connect to database and get existing records
            db = Database()
            records_relation = db.getRelation("PatientRecord")
            existing_records = records_relation.getRowsWhereEqual('patient_id', patient_id)

            # Initialise variables for existing data
            existing_notes = ""
            conditions = []
            if existing_records:
                latest_record = existing_records[-1]
                existing_notes = "No notes" if not latest_record[3].strip() else latest_record[3]
                conditions = [new_diagnosis]
            else:
                existing_notes = "No notes"
                conditions = [new_diagnosis]

            # Create and save new patient record
            new_record = PatientRecord(
                patient_id=patient_id,
                mhwp_id=3,
                notes=existing_notes,
                conditions=conditions
            )

            # Save record and refresh display
            db.insert_patient_record(new_record)
            db.close()
            db = Database()
            self.load_patient_records(None)
            self.diagnosis_entry.delete(0, tk.END)
            messagebox.showinfo("Success", "Diagnosis saved successfully")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save diagnosis: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = PatientRecords(root)
    root.mainloop()
