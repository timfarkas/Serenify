import sys
import os
import tkinter as tk
from tkinter import messagebox, ttk
import subprocess # This allows us to open other files
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.entities import PatientRecord
from database import Database
from sessions import Session
import pandas as pd



# Fix diagnosis --> appends to all records; what if they want to change diagnosis instead of only adding next one
# Ask if they want to change diagnosis or add diagnosis to preexisting records 

class PatientRecords:
    def __init__(self, user_id=None):
        # Initialize the session instance 
        # self.session = Session()
        # self.session.open()
        # self.current_user_id = self.session.getId()
        self.current_user_id = 3
        self.root =  tk.Tk()
        self.root.title("Patient Records")
        self.root.geometry("700x700")

        self.title_label = tk.Label(self.root, text=f"Patient Records", font=("Arial", 24, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=2, pady=5)

        # Load conditions from conditions.txt
        self.conditions_list = self.load_conditions("conditions.txt")

       # Search Patient Section
        self.patient_list_frame = tk.LabelFrame(self.root, text="Search Patient", padx=2, pady=5)
        self.patient_list_frame.grid(row=1, column=0, padx=2, pady=5, sticky="n")

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
        self.record_frame = tk.LabelFrame(self.root, text="Records", padx=2, pady=5)
        self.record_frame.grid(row=1, column=1, padx=2, pady=5, sticky="n")

        self.record_text = tk.Text(self.record_frame, height=15, width=50)
        self.record_text.pack(padx=5, pady=5)
        self.record_text.config(state=tk.DISABLED)

        # Notes Section
        self.note_frame = tk.LabelFrame(self.root, text="Add Notes and Diagnosis", padx=2, pady=5)
        self.note_frame.grid(row=2, column=0, columnspan=2, padx=2, pady=5)

        # Notes Entry
        tk.Label(self.note_frame, text="Notes:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.notes_entry = tk.Text(self.note_frame, width=50, height=5)
        self.notes_entry.grid(row=0, column=1, padx=5, pady=5)

        # Diagnosis Dropdown
        tk.Label(self.note_frame, text="Diagnosis:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.diagnosis_var = tk.StringVar()
        self.diagnosis_dropdown = ttk.Combobox(self.note_frame, textvariable=self.diagnosis_var, width=47)
        self.diagnosis_dropdown['values'] = self.conditions_list
        self.diagnosis_dropdown.grid(row=1, column=1, padx=5, pady=5)

        self.save_button = tk.Button(self.note_frame, text="Save", command=self.save_diagnosis_and_notes)
        self.save_button.grid(row=2, column=1, pady=10, sticky="e")

        self.root.mainloop()

    def load_conditions(self, filename):
        """Loads mental health conditions from a text file."""
        try:
            with open(filename, 'r') as file:
                conditions = [line.strip() for line in file.readlines() if line.strip()]
                return conditions
        except FileNotFoundError:
            messagebox.showerror("Error", f"File '{filename}' not found.")
            return []

    def load_patient_records(self, event=None):
        """Loads selected patient's records into the text box."""
        selected_index = self.patient_listbox.curselection()
        if not selected_index:
            return

        selected_patient = self.patients.iloc[selected_index[0]]
        patient_id = selected_patient[0]

        # Loading patient data
        db = Database()
        self.record = db.getRelation("PatientRecord")
        self.record = self.record.getRowsWhereEqual('patient_id', patient_id)
        self.record = pd.DataFrame(self.record)
        db.close()

        # Check if the record is not empty
        if not self.record.empty:
            self.record_text.config(state=tk.NORMAL)
            self.record_text.delete("1.0", tk.END)

            for _, row in self.record.iterrows():
                notes = row[3]
                diagnosis = row[4]

                # Displaying the extracted data
                self.record_text.insert(tk.END, f"Notes: {notes}\n")
                self.record_text.insert(tk.END, f"Diagnosis: {', '.join(diagnosis)}\n\n")

            self.record_text.config(state=tk.DISABLED)
        else:
            # If no records are found
            messagebox.showerror("Error", "No records found for the selected patient.")

    def save_diagnosis_and_notes(self):
        """Save combined notes and diagnosis for the selected patient."""
        selected_index = self.patient_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("No Patient Selected", "Please select a patient.")
            return

        patient_id = int(self.patients.iloc[selected_index[0]][0])
        new_notes = self.notes_entry.get("1.0", tk.END).strip()
        new_diagnosis = self.diagnosis_var.get().strip()

        if not new_notes and not new_diagnosis:
            messagebox.showwarning("Incomplete Data", "Please provide notes or select a diagnosis.")
            return

        try:
            # Connect to database and save
            db = Database()
            records_relation = db.getRelation("PatientRecord")
            existing_records = records_relation.getRowsWhereEqual('patient_id', patient_id)

            # Handle existing conditions
            conditions = []
            if existing_records:
                latest_record = existing_records[-1]
                conditions = latest_record[4] if latest_record[4] else []
            if new_diagnosis:
                if new_diagnosis not in conditions:
                    # Ask the user whether to replace or add
                    response = messagebox.askyesno(
                        "Update Diagnosis",
                        "Would you like to replace the existing diagnosis with the new one? (Yes to replace, No to add)"
                    )
                    if response:  # Replace
                        conditions = [new_diagnosis]
                    else:  # Add
                        conditions.append(new_diagnosis)
                else:
                    messagebox.showinfo("Information", "The selected diagnosis already exists.")
                    
            # Create and save new patient record
            new_record = PatientRecord(
                patient_id=patient_id,
                mhwp_id=3,
                notes=new_notes,
                conditions=conditions
            )
            db.insert_patient_record(new_record)
            db.close()

            # Refresh display
            self.load_patient_records(None)
            self.notes_entry.delete("1.0", tk.END)
            self.diagnosis_var.set("")
            messagebox.showinfo("Success", "Notes and diagnosis saved successfully.")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save notes and diagnosis: {str(e)}")


if __name__ == "__main__":
    app = PatientRecords()